#!/usr/bin/env python3
"""Certified complete partial-source movement invoice."""
import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    path = Path(__file__).with_name("retained") / "interval_price.py"
    spec = importlib.util.spec_from_file_location("retained_interval_price", path)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    receipt_bytes = (args.out / "RESULT.json").read_bytes()
    receipt = json.loads(receipt_bytes)
    profile = {int(k): v for k, v in receipt["profile"].items()}
    base = {1: 58, 2: 63, 3: 30, 4: 30, 5: 74, 6: 20, 7: 105, 8: 1}
    delta = Counter(profile)
    for k, v in base.items():
        delta[k] -= v
    assert {k: v for k, v in delta.items() if v} == {1: 9, 3: 9, 4: -6, 5: -1, 7: -1}
    budget = Counter({127: Fraction(37, 6), 64: Fraction(74, 6), 1: Fraction(-74, 6)})
    for j in range(1, 9):
        budget[1 + 7*j] += Fraction(74, 6)
        budget[7*j] -= Fraction(74, 6)
    room = budget.copy()
    for k, v in profile.items():
        room[k] -= v
    assert tool.interval(room)[0] > 7
    result = {"status": "PASS_EXACT_TWO_RETENTION_PARTIAL_INVOICE",
              "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
              "profile": profile, "moment_exponent": "199/200",
              "price": tool.report(tool.interval(profile)),
              "predecessor_price": tool.report(tool.interval(base)),
              "increment": tool.report(tool.interval(delta)),
              "limiting_movement_allowance": tool.report(tool.interval(budget)),
              "limiting_room": tool.report(tool.interval(room)),
              "scope": "Seventeen literal endpoints,94 unfinished endpoints; ordinary/storage and complete supplier/recursive costs remain separate; no new kappa"}
    (args.out / "PRICE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
