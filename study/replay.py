"""Replay the fixed design using exact integer nanosecond costs."""
import argparse
import csv
import hashlib
import json
import platform
import random
import re
import statistics
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from design import Panel, allocate
from fetch import ROOT, SCENARIOS

TICKS = 10**9
BUDGETS = (0, 1, 5, 10, 25, 50)


def instance_hash(name):
    return int.from_bytes(hashlib.sha256(name.encode()).digest()[:8], "big")


def dataset(scenario):
    path = ROOT / "inputs" / scenario
    cutoff = int(re.search(r"(?m)^algorithm_cutoff_time:\s*(\d+)", (path / "description.txt").read_text()).group(1)) * TICKS
    rows = defaultdict(dict)
    with (path / "algorithm_runs.arff").open(encoding="utf-8") as f:
        for line in f:
            if line.strip().lower() == "@data":
                break
        for row in csv.reader(f, skipinitialspace=True):
            if not row or row[0].startswith("%"):
                continue
            name, rep, alg, time, status = (s.strip().strip("'") for s in row)
            if rep != "1":
                continue
            if alg in rows[name]:
                raise ValueError((scenario, name, alg))
            t = None if time == "?" else int((Decimal(time)*TICKS).to_integral_value())
            solved = status == "ok" and t is not None and 0 <= t <= cutoff
            rows[name][alg] = t if solved else None
    train = sorted(i for i in rows if instance_hash(i)%5 == 0)
    test = sorted(set(rows)-set(train))
    algorithms = sorted({a for i in train for a in rows[i]})

    def penalty(alg):
        times = (rows[i].get(alg) for i in train)
        return sum(10*cutoff if t is None else t for t in times)

    backup, first = sorted(algorithms, key=lambda a: (penalty(a), a))[:2]
    eligible = [i for i in test if first in rows[i] and backup in rows[i]]
    info = dict(scenario=scenario, training=len(train), test=len(test), pair=len(eligible),
                algorithms=len(algorithms), backup=backup, first=first, cutoff_s=cutoff/TICKS)
    return [(rows[i][first], rows[i][backup]) for i in eligible], cutoff, info


def stats(panel, flags, query, upfront, total):
    lo, hi = panel.bounds({i: flags[i] for i in query})
    return [(lo+upfront)/total, (hi+upfront)/total, (hi-lo)/total,
            panel.worst_width(query)/total]


def summarize(scenario, records, cutoff, fraction):
    slot = cutoff*fraction//100
    matched = [(a,b) for a,b in records if b is not None]
    flags = [int(a is None or a > slot) for a,b in matched]
    base = [b for a,b in matched]
    upfront = sum(slot if f else a for (a,b), f in zip(matched, flags))
    panel = Panel(base, sum(flags))
    n, total = len(base), sum(base)
    actual = (upfront + sum(t*f for t,f in zip(base,flags)))/total
    extra = sum(b is None and a is not None and a <= slot for a,b in records)
    summary = dict(scenario=scenario, slice_pct=fraction, n=n, failures=sum(flags),
                   solved_beyond_primary=extra, baseline_s=total/TICKS, first_s=upfront/TICKS,
                   paired_ratio=actual, independence_ratio=upfront/total+sum(flags)/n)
    by_design = []
    for pct in BUDGETS:
        q = n*pct//100
        select = panel.select(q)
        rng = random.Random(instance_hash(f"{scenario}/{fraction}/{pct}"))
        designs = {"minimax":[set(select)], "slowest":[set(panel.order[n-q:])],
                   "uniform":[set(rng.sample(range(n), q)) for _ in range(200)]}
        for design, batch in designs.items():
            runs = [stats(panel, flags, query, upfront, total) for query in batch]
            if any(not lo-1e-12 <= actual <= hi+1e-12 or w > worst+1e-12
                   for lo,hi,w,worst in runs):
                raise ArithmeticError("inconsistent replay")
            lower, upper, width, worst = map(statistics.mean, zip(*runs))
            by_design.append(dict(scenario=scenario, slice_pct=fraction, budget_pct=pct,
                                  q=q, design=design, lower=lower, upper=upper, width=width,
                                  worst_width=worst, decisive=sum(hi<1 or lo>1 for lo,hi,_,_ in runs)/len(runs),
                                  queried_low=(panel.window(q)[1] if design=="minimax" else None)))
    return summary, by_design, panel


def capped_panel(scenario, records, cutoff, fraction):
    """Full evaluation panel under a fixed charge for an unsuccessful backup."""
    slot = cutoff*fraction//100
    flags = [int(a is None or a > slot) for a,b in records]
    costs = [cutoff if b is None else b for a,b in records]
    upfront = sum(slot if f else a for (a,b),f in zip(records,flags))
    panel = Panel(costs, sum(flags))
    total = sum(costs)
    q = len(costs)//10
    query = set(panel.select(q))
    lo,hi,width,worst = stats(panel,flags,query,upfront,total)
    solved = sum(b is not None for a,b in records)
    added = sum(b is None and not f for (a,b),f in zip(records,flags))
    return dict(scenario=scenario, slice_pct=fraction, n=len(costs), failures=sum(flags),
                reference_solved=solved, schedule_solved=solved+added, budget=q,
                actual=(upfront+sum(t*f for t,f in zip(costs,flags)))/total,
                independence=upfront/total+sum(flags)/len(flags),
                lower=lo, upper=hi, worst_width=worst,
                slowest_worst_width=panel.worst_width(set(panel.order[len(costs)-q:]))/total,
                queried_low=panel.window(q)[1])


def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((ROOT / "input_hashes.json").read_text())
    for name, expected in manifest.items():
        if hashlib.sha256((ROOT / "inputs" / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"input checksum mismatch: {name}")
    panels, details, experiments, metadata, capped = [], [], [], [], []
    for scenario in SCENARIOS:
        records, cutoff, info = dataset(scenario)
        metadata.append(info)
        for frac in (1,5,10):
            capped.append(capped_panel(scenario, records, cutoff, frac))
            summary, designs, panel = summarize(scenario, records, cutoff, frac)
            details.append(summary)
            experiments.extend(designs)
            if frac == 1:
                panels.append(panel)
    write(args.out / "capped.csv", capped)
    write(args.out / "datasets.csv", metadata)
    write(args.out / "replays.csv", details)
    write(args.out / "audits.csv", experiments)
    q0 = [len(p.order)//10 for p in panels]
    optimum, selected = allocate(panels, sum(q0))
    total = sum(sum(p.costs) for p in panels)
    pool = dict(scenarios=SCENARIOS, budget=sum(q0), proportional=q0, optimal=selected,
                proportional_width=sum(p.window(q)[0] for p,q in zip(panels,q0))/total,
                optimal_width=optimum/total, no_query_width=sum(p.window(0)[0] for p in panels)/total)
    (args.out / "pooled.json").write_text(json.dumps(pool, indent=2)+"\n", newline="\n")
    sources = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob("*.py"))}
    env = dict(python=platform.python_version(), platform=platform.platform(), sources=sources,
               inputs=manifest, output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                               for p in sorted(args.out.iterdir())})
    (args.out / "manifest.json").write_text(json.dumps(env,indent=2)+"\n", newline="\n")


if __name__ == "__main__":
    main()
