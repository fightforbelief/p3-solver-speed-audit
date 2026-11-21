"""Retrieve public ASlib inputs at the study revision."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
REVISION = "551b22beef8df17de59286b4822ef720e0aa4d6f"
SCENARIOS = ("ASP-POTASSCO", "BNSL-2016", "CSP-2010", "MIP-2016", "QBF-2016", "SAT11-INDU")
FILES = ("description.txt", "algorithm_runs.arff")


def fetch(relative):
    source = f"https://raw.githubusercontent.com/coseal/aslib_data/{REVISION}/{relative}"
    with urlopen(source, timeout=60) as response:
        content = response.read()
    destination = ROOT / "inputs" / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return relative, hashlib.sha256(content).hexdigest()


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        hashes = dict(pool.map(fetch, (f"{s}/{f}" for s in SCENARIOS for f in FILES)))
    manifest = ROOT / "input_hashes.json"
    if manifest.exists() and json.loads(manifest.read_text()) != hashes:
        raise ValueError("Retrieved data differ from the archived checksums")
    print(json.dumps(hashes, indent=2))
