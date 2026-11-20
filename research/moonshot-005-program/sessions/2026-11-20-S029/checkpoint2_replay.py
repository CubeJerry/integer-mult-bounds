#!/usr/bin/env python3
"""Reproduce the five checkpoint-two packages against their committed evidence."""
import argparse
from hashlib import sha256
import gzip
import json
from pathlib import Path
import subprocess
import sys


def payload(path):
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--only", help="Reproduce one named job")
    args = parser.parse_args()
    repo = args.repo.resolve()
    base = repo / "research/moonshot-005-program/results"
    source = base / "bit-spread-h263-source"
    budget = base / "bit-covariant-single-grade-budget"
    k = base / "bit-gf64-actual-k-atlas"
    rs = base / "bit-spread-rs-physical-word"
    gauges = base / "bit-bipartite-component-gauges"
    jobs = [
        ("source", source/"author/check.py", source/"author/output", []),
        ("source-review", source/"review/check.py", source/"review/output", []),
        ("budget", budget/"author/check.py", budget/"author/output", []),
        ("budget-review", budget/"review/check.py", budget/"review/output", []),
        ("K", k/"author/construct.py", k/"author/output", []),
        ("K-review", k/"review/check.py", k/"review/output", ["--certs", k/"author/output"]),
        ("H", rs/"author/build.py", rs/"author/output", []),
        ("RS-source", rs/"author/rs_source.py", rs/"author/source-output", []),
        ("F", rs/"author/terminal.py", rs/"author/terminal-output", ["--k-words", k/"author/output"]),
        ("RS-review", rs/"review/check.py", rs/"review/output", ["--author", rs/"author", "--k-certs", k/"author/output"]),
        ("gauges", gauges/"review/check.py", gauges/"review/output", []),
    ]
    if args.only and args.only not in {j[0] for j in jobs}:
        raise SystemExit("unknown job")
    args.out.mkdir(parents=True, exist_ok=True)
    records = {}
    for name, script, expected, flags in jobs:
        if args.only and args.only != name:
            continue
        dest = (args.out/name).resolve()
        dest.mkdir(exist_ok=True)
        with (args.out/(name+".log")).open("w") as log:
            subprocess.run([sys.executable, "-B", script, "--repo", repo, "--out", dest, *flags],
                           check=True, stdout=log, stderr=subprocess.STDOUT)
        matched = {}
        for f in sorted(expected.iterdir()):
            # Some source packages carry a frozen input alongside their receipts.
            if name == "source" and f.name == "COEFFICIENTS.json.gz":
                continue
            actual = payload(dest/f.name)
            if actual != payload(f):
                raise ValueError(f"{name}: differing scientific payload {f.name}")
            matched[f.name] = sha256(actual).hexdigest()
        records[name] = matched
        print(name, len(matched), flush=True)
    (args.out/"VALIDATION.json").write_text(json.dumps(records, indent=2, sort_keys=True)+"\n")


if __name__ == "__main__":
    main()
