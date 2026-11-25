#!/usr/bin/env python3
"""Exact packed-batch index and recurrence checks; not a tape simulator."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json


def packing(radix, width):
    ell, old = 1, radix
    while old < width:
        ell += 1
        old *= radix
    new = width * ((old + width - 1) // width)
    return ell, old, new


cases = positions = controls = recurrences = 0
for b in (3, 5, 7, 11):
    for w in range(3, 129):
        ell, old, new = packing(b, w)
        assert old >= w and (ell == 1 or old // b < w)
        assert old <= new < 2 * old and new % w == 0
        assert ell <= w.bit_length()
        beta = Fraction(new, old)
        assert [(z // w, z % w) for z in range(new)] == list(
            product(range(new // w), range(w)))
        for suffix in (1, 2, 5):
            source = [(z, a) for z in range(old) for a in range(suffix)]
            packed = source + [(None, a) for z in range(old, new)
                               for a in range(suffix)]
            target = [packed[z * suffix + (suffix - 1 - a)]
                      for z in range(new) for a in range(suffix)]
            recovered = target[:old * suffix]
            expected = [(z, suffix - 1 - a)
                        for z in range(old) for a in range(suffix)]
            assert recovered == expected
            positions += len(target)
        if old % w:
            assert (old // w) * w < old
            controls += 1
        for groups in (4, 8, 16):
            assert beta / groups < Fraction(1, 2)
        m, k, c0 = 16, 16, 1
        base = ell + k
        majorant = max(2 * c0, base)
        values = [Fraction(0)]
        for e in range(1, 2049):
            f = (e - ell) // k
            value = Fraction(e) if f < 1 else c0 + beta * values[f]
            values.append(value)
            assert value ** 4 <= majorant ** 4 * e ** 3
            recurrences += 1
        cases += 1

# An intermediate row-mixing map need not preserve the genuine row set.
original = [1, 0, 1]
padded = original + [0]
partial = [padded[3], padded[1], padded[2], padded[0]]
assert partial[:3] != original
controls += 1

volume_checks = 0
for module in (1, 2, 4, 16, 256, 65536):
    for labels in (4, 8, 27):
        width = module * labels
        separate = module * Fraction(1, width)
        grouped = Fraction(module, width)
        assert separate == grouped == Fraction(1, labels)
        volume_checks += 1

result = {
    "status": "passed",
    "arithmetic": "integers and exact rational arithmetic",
    "packing_cases": cases,
    "padded_positions_checked": positions,
    "recurrence_cases": recurrences,
    "volume_preservation_cases": volume_checks,
    "negative_controls": controls,
    "scope": "Exact multi-digit packing, genuine-row preservation after a completed independent map, group volume accounting and finite rational recurrence majorants. No physical tape execution or compact-template premise is certified."
}
Path(__file__).with_name("packed-batch-verification.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
