"""Post hoc, fixed-budget comparisons for the published ASlib panels."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


def hamilton(weights, total):
    quotas = [Fraction(total * w, sum(weights)) for w in weights]
    counts = [int(x) for x in quotas]
    order = sorted(range(len(weights)), key=lambda i: quotas[i] - counts[i], reverse=True)
    for i in order[:total - sum(counts)]:
        counts[i] += 1
    return counts


def main(root):
    sys.path.insert(0, str(root / "study"))
    from design import Panel, allocate
    from fetch import SCENARIOS
    from replay import dataset
    for file, expected in json.loads((root / "input_hashes.json").read_text()).items():
        if hashlib.sha256((root / "inputs" / file).read_bytes()).hexdigest() != expected:
            raise ValueError(f"unexpected input: {file}")
    report = []
    for fraction in (1, 5, 10):
        panels = []
        for name in SCENARIOS:
            records, cutoff, info = dataset(name)
            pairs = [(a,b) for a,b in records if b is not None]
            count = sum(a is None or a > cutoff*fraction//100 for a,b in pairs)
            panels.append(Panel([b for a,b in pairs], count))
        totals = [sum(p.costs) for p in panels]
        rows = [len(p.costs)//10 for p in panels]
        budget = sum(rows)
        work = hamilton(totals,budget)
        if any(q>len(p.costs) for p,q in zip(panels,work)):
            raise ValueError("the uncapped proportional rule exceeds a group size")
        widths = [[p.window(q)[0] for q in range(min(len(p.costs),budget)+1)] for p in panels]
        greedy = [0]*len(panels)
        for _ in range(budget):
            available = [i for i,q in enumerate(greedy) if q+1 < len(widths[i])]
            i = max(available, key=lambda i: widths[i][greedy[i]] - widths[i][greedy[i]+1])
            greedy[i] += 1
        best, optimal = allocate(panels,budget)
        values = {}
        for rule, quotas in dict(instance_share=rows,reference_time_share=work,
                                 marginal_greedy=greedy,exact=optimal).items():
            assert sum(quotas)==budget
            w = sum(curve[q] for curve,q in zip(widths, quotas))
            assert w >= best and (rule != "exact" or w==best)
            values[rule] = dict(queries=quotas, width_ns=w, normalized_width=w/sum(totals))
        report.append(dict(slice_pct=fraction, total_reference_ns=sum(totals), designs=values))
    previous = json.loads((root/"results"/"pooled.json").read_text())
    assert report[0]["designs"]["exact"]["queries"] == previous["optimal"]
    assert report[0]["designs"]["exact"]["normalized_width"] == previous["optimal_width"]
    print(json.dumps(dict(scenarios=SCENARIOS, comparisons=report), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    main(parser.parse_args().root.resolve())
