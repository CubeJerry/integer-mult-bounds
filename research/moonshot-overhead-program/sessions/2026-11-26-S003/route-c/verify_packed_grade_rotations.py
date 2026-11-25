#!/usr/bin/env python3
"""Independent exact packed-row check for B's scalar masked-rotation executor."""

from itertools import product
from math import prod
from pathlib import Path
import json


def grade_rotation_by_fibres(values, radices, grade, data_length):
    """Literal two-buffer rotation of each complete prefix fibre."""
    width = radices[grade]
    block = prod(radices[grade+1:])*data_length
    fibre = width*block
    assert len(values) % fibre == 0
    result = []
    for start in range(0, len(values), fibre):
        rest = values[start:start+(width-1)*block]
        last = values[start+(width-1)*block:start+fibre]
        result.extend(last)
        result.extend(rest)
    return result


def direct_index_rotation(values, radices, grade, data_length, prefixes):
    result = [None]*len(values)
    for prefix in range(prefixes):
        for coords in product(*(range(d) for d in radices)):
            oldrow = newrow = 0
            for i, (value, d) in enumerate(zip(coords, radices)):
                oldrow = oldrow*d+value
                newrow = newrow*d+((value+1) % d if i == grade else value)
            for data in range(data_length):
                old = (prefix*prod(radices)+oldrow)*data_length+data
                new = (prefix*prod(radices)+newrow)*data_length+data
                result[new] = values[old]
    return result


cases = entries = commuting = 0
for radices in [(2,), (2, 4), (4, 2, 2), (8, 2), (1, 2, 4)]:
    for data_length, prefixes in product([1, 3, 7], [1, 2]):
        values = list(range(prefixes*prod(radices)*data_length))
        for grade in range(len(radices)):
            observed = grade_rotation_by_fibres(values, radices, grade, data_length)
            expected = direct_index_rotation(values, radices, grade, data_length, prefixes)
            assert observed == expected
            cases += 1
            entries += len(values)
        for left, right in product(range(len(radices)), repeat=2):
            a = grade_rotation_by_fibres(
                grade_rotation_by_fibres(values, radices, left, data_length),
                radices, right, data_length)
            b = grade_rotation_by_fibres(
                grade_rotation_by_fibres(values, radices, right, data_length),
                radices, left, data_length)
            assert a == b
            commuting += 1

# Applying a row-dependent coefficient after the rotation is wrong.
values = [1, 1, 1, 1]
mask = [1, 0, 0, 0]
correct = grade_rotation_by_fibres([a*b for a,b in zip(values, mask)], (4,), 0, 1)
wrong = [a*b for a,b in zip(grade_rotation_by_fibres(values, (4,), 0, 1), mask)]
assert correct != wrong

result = {
    "status": "passed",
    "rotation_cases": cases,
    "exact_record_positions": entries,
    "commuting_grade_pairs": commuting,
    "wrong_mask_order_negative_controls_rejected": 1,
    "scope": "Finite packed-row permutation and input-mask checks only; mathematical scan and visited-space complexity argued separately, shared spatial query routing not tested.",
}
Path(__file__).with_name("packed-grade-rotation-verification.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
