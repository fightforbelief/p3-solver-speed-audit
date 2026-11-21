"""Independent tabular reconstruction of pair selection and schedule costs on archived rows."""
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import pandas as pd


def check(root, out):
    datasets = pd.read_csv(out/"datasets.csv").set_index("scenario")
    replays = pd.read_csv(out/"replays.csv").set_index(["scenario","slice_pct"])
    capped = pd.read_csv(out/"capped.csv").set_index(["scenario","slice_pct"])
    for name, info in datasets.iterrows():
        lines = (root/"inputs"/name/"algorithm_runs.arff").read_text().splitlines()
        start = next(i for i, l in enumerate(lines) if l.strip().lower()=="@data")+1
        d = pd.read_csv(root/"inputs"/name/"algorithm_runs.arff", header=None, skiprows=start,
                        names=["id","rep","solver","time","status"])
        d = d[d.rep.eq(1)].copy()
        cutoff = int(re.search(r"(?m)^algorithm_cutoff_time:\s*(\d+)",
                               (root/"inputs"/name/"description.txt").read_text()).group(1))
        good = d.status.str.strip().eq("ok") & d.time.between(0,cutoff)
        times = d.assign(t=d.time.where(good)).pivot(index="id",columns="solver",values="t")
        train = [int(hashlib.sha256(i.encode()).hexdigest()[:16],16)%5 == 0 for i in times.index]
        ranking = times.loc[train].fillna(10*cutoff).sum().sort_index().sort_values(kind="stable")
        b, a = ranking.index[:2]
        assert (b,a)==(info.backup,info["first"])
        test = times.loc[[not t for t in train], [a,b]]
        # All released panels have complete records for this solver pair.
        counts = d[d.solver.isin([a,b])].groupby("id").size()
        assert (counts.loc[test.index]==2).all() and len(test)==info["pair"]==info.test
        for fraction in (1,5,10):
            slot = cutoff*fraction/100
            solved_fast = test[a].le(slot)
            attempt = test[a].where(solved_fast,slot)
            backup = test[b].fillna(cutoff)
            elapsed = attempt + backup.where(~solved_fast,0)
            primary = test[b].notna()
            row = replays.loc[(name,fraction)]
            allrow = capped.loc[(name,fraction)]
            assert row.n == primary.sum() and row.failures == (~solved_fast & primary).sum()
            assert row.solved_beyond_primary == (solved_fast & ~primary).sum()
            assert math.isclose(elapsed[primary].sum()/backup[primary].sum(),row.paired_ratio,rel_tol=1e-10)
            assert math.isclose(elapsed.sum()/backup.sum(),allrow.actual,rel_tol=1e-10)
            assert (solved_fast|primary).sum() == allrow.schedule_solved
    manifest = json.loads((out/"manifest.json").read_text())
    for name, sha in manifest["output_sha256"].items():
        assert hashlib.sha256((out/name).read_bytes()).hexdigest()==sha
    print("Verified primary and full-panel replay for all 18 settings, solver choices and output hashes.")


if __name__ == "__main__":
    check(Path(sys.argv[1]),Path(sys.argv[2]))
