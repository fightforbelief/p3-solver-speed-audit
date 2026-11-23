# Replicating the solver audit

Use Python 3.12.10 from the extracted directory. The fetch and replay programs use the Python standard library. The tests and independent reconstruction additionally require pytest 9.2.0 and pandas 3.1.0.

```sh
python -m pip install pytest==9.2.0 pandas==3.1.0
python study/fetch.py
python -m pytest -q study
python study/replay.py --out reproduction
python verification/check.py . reproduction
python verification/allocation.py > allocation-reproduced.json
```

The fetcher downloads twelve files from the authors' ASlib repository at revision `551b22beef8df17de59286b4822ef720e0aa4d6f` and verifies their SHA-256 hashes. The runtime-ratio and interval tables in `reproduction` should match the corresponding CSV and JSON files in `results`. `verification/check.py` independently reconstructs solver selection and paired times for every scenario and time slice. The separate allocation program reads the pinned data and validates the primary optimum against the original pooled analysis. Compare its JSON values with `results/allocation_comparison.json`. On Windows, use a UTF-8 redirect or capture stdout in Python if comparing file bytes.

`results/replays.csv` contains the primary panel, `audits.csv` the partial audit intervals, and `capped.csv` the full evaluation population. The `width_ns` field in the allocation comparison is the exact integer width in nanoseconds. `PROTOCOL.md` records the planned comparisons and identifies the post hoc sensitivities. The original execution records are in `verification/runs.json` and the additional run in `verification/allocation_run.json`.
