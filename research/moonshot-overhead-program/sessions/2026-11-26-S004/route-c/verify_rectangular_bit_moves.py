#!/usr/bin/env python3
"""Check the actual named-bit move sequence, not a final sorting oracle."""
from pathlib import Path
import hashlib
import json


def move_before(order, token, anchor):
    order.remove(token)
    order.insert(order.index(anchor), token)


def move_after(order, token, anchor):
    order.remove(token)
    order.insert(order.index(anchor) + 1, token)


def run(p, q, wrong=False):
    xs = [f"X{i}" for i in range(p)]
    ys = [f"Y{i}" for i in range(q)]
    order = ["P", *xs, "G", *ys, "B"]
    for bit in reversed(ys) if wrong else ys:
        move_before(order, bit, xs[0] if xs else "G")
    for bit in xs if wrong else reversed(xs):
        move_after(order, bit, "G")
    return order, ["P", *ys, "G", *xs, "B"]


def main():
    checked = rejected = 0
    for p in range(33):
        for q in range(33):
            actual, expected = run(p, q)
            assert actual == expected, (p, q, actual, expected)
            wrong, _ = run(p, q, wrong=True)
            if max(p, q) >= 2:
                assert wrong != expected, (p, q)
                rejected += 1
            checked += 1
    result = {"status": "passed", "named_bit_layout_cases": checked,
              "reversed_order_negative_controls": rejected,
              "includes_empty_fields": True,
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Exact permutation of named coordinate fields; tape-cost argument is in review"}
    Path(__file__).with_name("rectangular-bit-moves-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
