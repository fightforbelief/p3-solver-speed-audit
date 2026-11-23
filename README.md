# Which fallback flags should a solver benchmark recover?

**Yunjie Guo and Hanqing Yang.** If a presolver needs a backup on a known number of instances, the overall runtime depends on which ones they are. This paper derives the smallest worst-case interval an auditor can guarantee by recovering a limited number of flags. It gives the optimal batch, an adversarial bound for sequential designs, a shared-budget allocation, and a complexity boundary for unequal prices.

[ORL submission manuscript](submission/orl/manuscript.pdf) · [Journal decision and upload files](submission/orl/README.md) · [Original study report](paper/manuscript.pdf) · [Study design](PROTOCOL.md) · [Results and hashes](results/manifest.json)

## Findings

The six primary ASlib panels contain 3,968 reference-solved instances. Treating failures as uniformly paired with reference times predicted a speed advantage in all six. Full pairing gave one advantage, four slowdowns of 6.6%–12.2%, and one slowdown within 0.05% of parity. Including reference timeouts under an explicit fixed-slot policy changed the direction for CSP and SAT. With 394 equally priced checks, optimal allocation across the six panels reduced worst-case width by 43.8% relative to assigning 10% to each panel. With allocation proportional to reference time, the corresponding gain was 2.0%. Marginal greedy matched the exact optimum at all three slices. [Allocation comparisons](results/allocation_comparison.json). Within each primary panel the slowest-only design attained the optimal bound at the 10% budget.

This is an audit of finite recorded schedules. The experiments replay published solver records, with explicit time-slice and cold-restart assumptions. Industry-wide prevalence, fresh wall-clock speedups and learned-proxy accuracy require different evidence.

## Reproduce the study

Use Python 3.12.10. The replay and public-data fetcher use the standard library. The independent checker uses pandas 3.1.0 and the tests use pytest 9.2.0. From the repository root, use the project's interpreter for each command. On the research Windows host it is `.\.venv\Scripts\python.exe`.

```sh
python -m pip install pytest==9.2.0 pandas==3.1.0
python study/fetch.py
python -m pytest -q study
python study/replay.py --out reproduction
python verification/check.py . reproduction
```

The fetcher verifies twelve input hashes at the pinned [ASlib revision](https://github.com/coseal/aslib_data/tree/551b22beef8df17de59286b4822ef720e0aa4d6f). The output directory for a replay must be fresh. Compare its five result files to `results/`. The manifest also records environment and source hashes. The 200 random subsets at each budget use deterministic seeds derived from the scenario and configuration. Budget percentages are rounded down.

To reconstruct the manuscript assets from the archived results, run `python paper/render_data.py` with matplotlib 3.10.8. Compile `paper/manuscript.typ` in Typst 0.14.2 with the repository as root. The release PDF was produced with the Python binding `typst==0.14.6` using `typst.compile("paper/manuscript.typ", output="paper/manuscript.pdf", root=".")`.

## Inspect the evidence

| File | Contents |
| --- | --- |
| [replays.csv](results/replays.csv) | Fully paired and uniform-pairing ratios on reference-solved instances at three time slices |
| [audits.csv](results/audits.csv) | Audit endpoints, worst and realized widths, query counts and parity decisions at six budgets |
| [capped.csv](results/capped.csv) | All-instance fixed-slot sensitivity with both solved counts |
| [datasets.csv](results/datasets.csv) | Training and evaluation sizes, selected solvers and scenario cutoffs |
| [pooled.json](results/pooled.json) | Optimal and proportional allocations of the same budget |

The Windows project environment ran the five study tests and 26 previous P3 tests together (31 passed). The study tests enumerate compatible label completions, affordable query subsets and a small adaptive game, and check schedule accounting at a time-slice boundary. A separate pandas reconstruction confirmed solver choices and paired ratios for all 18 settings on the primary and full panels. Two Windows runs agreed on every original primary table entry and on the pooled allocation. The final analysis also includes the all-instance sensitivity. The earlier literature-screening snapshot and OPF pilot remain historical P3 work and supply no observations to these results.
