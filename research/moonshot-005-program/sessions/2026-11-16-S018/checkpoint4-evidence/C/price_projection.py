#!/usr/bin/env python3
"""Directed rational movement prices using exact integer 200th roots."""
import argparse
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


def root_floor(n, k):
    lo, hi = 0, 1 << ((n.bit_length()+k-1)//k)
    while lo+1 < hi:
        m = (lo+hi)//2
        if m**k <= n:
            lo = m
        else:
            hi = m
    if not (lo**k <= n < (lo+1)**k):
        raise ValueError("root enclosure")
    return lo


def powers(d, scale):
    if d == 1:
        return Fraction(1), Fraction(1)
    z = root_floor(d**199 * scale**200, 200)
    return Fraction(z, scale), Fraction(z+1, scale)


def moment(profile, scale=10**42):
    lo = hi = Fraction(0)
    for d, count in profile.items():
        a, b = powers(int(d), scale)
        lo += count*(a if count >= 0 else b)
        hi += count*(b if count >= 0 else a)
    return lo, hi


def dec(x):
    with localcontext() as c:
        c.prec = 80
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def record(pair):
    return {"rational": [str(q) for q in pair], "decimal": [dec(q) for q in pair]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    r = json.loads(a.result.read_text())
    old = r["before"]["movement_profile"]
    new = r["after"]["movement_profile"]
    delta = {d: new.get(d,0)-old.get(d,0) for d in set(old)|set(new)}
    delta = {int(d): c for d,c in delta.items() if c}
    if sum(d*c for d,c in delta.items()) != 0:
        raise ValueError("rank volume changed")
    qo, qn, change = moment(old), moment(new), moment(delta)
    gate = {127: 37, 64: 74, 1: -74}
    for j in range(1,9):
        gate[1+7*j] = gate.get(1+7*j,0)+74
        gate[7*j] = gate.get(7*j,0)-74
    lo, hi = moment(gate)
    limit = (lo/6, hi/6)
    room = (limit[0]-qn[1], limit[1]-qn[0])
    result = {
        "status": "PASS_EXACT_RELEASED_CARRIER_MOVEMENT_PRICE",
        "word_sha256": r["word_sha256"],
        "exponent": "199/200", "integer_root_scale": 10**42,
        "before": record(qo), "after": record(qn),
        "signed_profile_change": dict(sorted(delta.items())),
        "signed_rank_volume_change": 0,
        "moment_change": record(change),
        "limiting_necessary_allowance": record(limit),
        "limiting_necessary_room": record(room),
        "scope": "Every raw native-to-Hub closure MOVE is included. These are complete partial-word movement prices. Limiting room is necessary, not a completed supplier or finite-multiplicity margin. All ordinary/source/ownership/precision/compiler/recursive obligations remain.",
    }
    a.out.write_text(json.dumps(result, indent=2)+"\n")
    print(result["status"], result["after"]["decimal"], result["limiting_necessary_room"]["decimal"])


if __name__ == "__main__":
    main()
