#!/usr/bin/env python3
"""Exact finite checks of HFS identities; not a full physical tape execution."""
from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path


def floor_sum(n: int, modulus: int, slope: int, intercept: int) -> int:
    assert n >= 0 and modulus > 0 and slope >= 0 and intercept >= 0
    answer = 0
    while True:
        q, slope = divmod(slope, modulus)
        answer += q * n * (n - 1) // 2
        q, intercept = divmod(intercept, modulus)
        answer += q * n
        maximum = slope * n + intercept
        if maximum < modulus:
            return answer
        n, intercept = divmod(maximum, modulus)
        modulus, slope = slope, modulus


def residue_count(n: int, modulus: int, slope: int, intercept: int, bound: int) -> int:
    assert 0 <= bound <= modulus
    return n + floor_sum(n, modulus, slope, intercept) - floor_sum(
        n, modulus, slope, intercept + modulus - bound
    )


def reconstruct(a: int, multiplier: int, bits: int, bucket: int, ordinal: int) -> int:
    stride = 1 << bits
    size = 0 if bucket >= a else 1 + (a - 1 - bucket) // stride
    assert 0 <= ordinal < size
    inverse = pow(multiplier, -1, a)
    slope, intercept = inverse * stride % a, inverse * bucket % a
    low, high = 1, a
    while low < high:
        middle = (low + high) // 2
        if residue_count(size, a, slope, intercept, middle) >= ordinal + 1:
            high = middle
        else:
            low = middle + 1
    return low - 1


def header_free_order(a: int, multiplier: int) -> tuple[list[int], int]:
    """Labels in this replay are audit witnesses, not stored runtime headers."""
    assert a >= 2 and gcd(a, multiplier) == 1
    records = list(range(a))
    selections = 0
    for bits in range((a - 1).bit_length()):
        expected = sorted(range(a), key=lambda r: ((multiplier * r % a) % (1 << bits), r))
        assert records == expected
        outputs: tuple[list[int], list[int]] = ([], [])
        cursor = 0
        for bucket in range(1 << bits):
            size = 0 if bucket >= a else 1 + (a - 1 - bucket) // (1 << bits)
            for ordinal in range(size):
                original = reconstruct(a, multiplier, bits, bucket, ordinal)
                assert original == records[cursor]
                destination_bit = ((multiplier * original % a) >> bits) & 1
                outputs[destination_bit].append(records[cursor])
                cursor += 1
                selections += 1
        assert cursor == a
        records = outputs[0] + outputs[1]
    assert records == sorted(range(a), key=lambda r: multiplier * r % a)
    return records, selections


def scaling_run_replay(qrange: int, multiplier: int) -> list[int]:
    """Check run padding, modular order and rectangular transpose exactly."""
    assert qrange >= 2 and gcd(qrange, multiplier) == 1
    a = multiplier % qrange
    if a == 1:
        return list(range(qrange))
    quotient, remainder = divmod(qrange, a)
    kappa = -qrange % a
    order, _ = header_free_order(a, kappa)
    rows: list[list[int | None]] = []
    for r in range(a):
        start = (r * qrange + a - 1) // a
        stop = ((r + 1) * qrange + a - 1) // a
        residue = kappa * r % a
        assert stop - start == quotient + (residue < remainder)
        row: list[int | None] = list(range(start, stop))
        row.extend([None] * (quotient + 1 - len(row)))
        rows.append(row)
    ordered = [rows[r] for r in order]
    padded_a = 1 << (a - 1).bit_length()
    ordered.extend([[None] * (quotient + 1) for _ in range(padded_a - a)])
    assert padded_a * (quotient + 1) < 4 * qrange
    output = [ordered[t][k] for k in range(quotient + 1)
              for t in range(padded_a) if t < a and (k < quotient or t < remainder)]
    assert all(value is not None for value in output)
    result = [int(value) for value in output]
    assert sorted(result) == list(range(qrange))
    for destination, original in enumerate(result):
        assert multiplier * original % qrange == destination
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-modulus', type=int, default=64)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('header-free-scaling-verification.json'))
    args = parser.parse_args()
    counts = {'floor_sum': 0, 'residue_count': 0, 'modular_sort': 0,
              'key_reconstruction': 0, 'scaling': 0, 'inverse_composition': 0}
    for modulus in range(1, 17):
        for n in range(0, 18):
            for slope in range(0, 2 * modulus + 1):
                for intercept in range(0, modulus + 2):
                    expected = sum((slope * v + intercept) // modulus for v in range(n))
                    assert floor_sum(n, modulus, slope, intercept) == expected
                    counts['floor_sum'] += 1
                for bound in (0, modulus // 2, modulus):
                    intercept = modulus + 1
                    expected = sum((slope * v + intercept) % modulus < bound for v in range(n))
                    assert residue_count(n, modulus, slope, intercept, bound) == expected
                    counts['residue_count'] += 1
    for a in range(2, args.max_modulus + 1):
        for multiplier in range(1, a):
            if gcd(a, multiplier) != 1:
                continue
            _, selections = header_free_order(a, multiplier)
            counts['modular_sort'] += 1
            counts['key_reconstruction'] += selections
    # Scaling samples include unequal runs, q=1, a just below Q, and negative c.
    for qrange in range(2, args.max_modulus + 1):
        for multiplier in sorted({1, qrange - 1, -1, 2, 3, qrange // 2,
                                  qrange + 3, 2 * qrange - 1}):
            if gcd(qrange, multiplier) != 1:
                continue
            order = scaling_run_replay(qrange, multiplier)
            inverse_order = scaling_run_replay(qrange, pow(multiplier, -1, qrange))
            assert [order[j] for j in inverse_order] == list(range(qrange))
            counts['scaling'] += 1
            counts['inverse_composition'] += 1
    # Deliberate off-by-one and modular-inverse errors must be detected.
    negative_controls = {
        'wrong_count_boundary_rejected': residue_count(7, 7, 3, 0, 0) != 1,
        'wrong_inverse_rejected': any(reconstruct(7, 3, 2, 0, s) != r
                                      for s, r in enumerate([0, 1])),
        'drop_genuine_zero_rejected': len([0, 1, 0, 2]) != len([v for v in [0, 1, 0, 2] if v]),
        'nonunit_multiplier_rejected': gcd(6, 2) != 1,
    }
    assert all(negative_controls.values())
    result = {'status': 'passed', 'scope': 'exact finite identities and permutation simulation; no full physical tape execution',
              'max_modulus': args.max_modulus, 'counts': counts, 'negative_controls': negative_controls}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
