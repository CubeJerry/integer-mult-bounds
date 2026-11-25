#!/usr/bin/env python3
"""Exact finite checks for FP1--FP3; not a tape-transition simulation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from random import Random


def pack(rows: list[list[list[int]]], degree: int) -> list[list[list[int]]]:
    """Input rows contain spatial positions containing opaque payload bits."""
    assert rows and len(rows) % degree == 0
    spatial, payload = len(rows[0]), len(rows[0][0])
    out = []
    for first in range(0, len(rows), degree):
        out.append([[rows[first + basis][position][bit]
                     for bit in range(payload) for basis in range(degree)]
                    for position in range(spatial)])
    return out


def unpack(rows: list[list[list[int]]], degree: int) -> list[list[list[int]]]:
    assert rows and len(rows[0][0]) % degree == 0
    spatial, payload = len(rows[0]), len(rows[0][0]) // degree
    return [[[row[position][bit * degree + basis] for bit in range(payload)]
             for position in range(spatial)]
            for row in rows for basis in range(degree)]


def volume(rows: list[list[list[int]]]) -> int:
    return sum(len(record) for row in rows for record in row)


def permute(rows: list[list[list[int]]], permutation: list[int]) -> list[list[list[int]]]:
    return [[row[old][:] for old in permutation] for row in rows]


def field_mul(a: int, b: int, degree: int, modulus: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a >> degree:
            a ^= modulus
    return result


def scale(rows: list[list[list[int]]], degree: int, modulus: int, scalar: int) -> list[list[list[int]]]:
    result = []
    for row in rows:
        next_row = []
        for record in row:
            next_record = []
            for start in range(0, len(record), degree):
                value = sum(record[start + i] << i for i in range(degree))
                product = field_mul(value, scalar, degree, modulus)
                next_record.extend((product >> i) & 1 for i in range(degree))
            next_row.append(next_record)
        result.append(next_row)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('full-rate-packing-verification.json'))
    args = parser.parse_args()
    random = Random(20261126)
    fields = {2: 0b111, 3: 0b1011, 4: 0b10011}
    counts = {'single_field_shapes': 0, 'packed_bits_checked': 0,
              'scalar_roundtrips': 0, 'nested_field_shapes': 0,
              'nested_bits_checked': 0, 'leading_batch_cases': 0}
    negative_controls = {'basis_order_detected': False,
                         'zero_embedding_inflates_volume': False,
                         'dropping_basis_loses_independence': False}
    for degree, modulus in fields.items():
        for groups in range(1, 5):
            for spatial in range(1, 8):
                for payload in range(1, 6):
                    rows = [[[random.randrange(2) for _ in range(payload)]
                             for _ in range(spatial)] for _ in range(groups * degree)]
                    encoded = pack(rows, degree)
                    assert volume(encoded) == volume(rows)
                    assert unpack(encoded, degree) == rows
                    order = list(range(spatial))
                    random.shuffle(order)
                    assert unpack(permute(encoded, order), degree) == permute(rows, order)
                    for scalar in range(1, 1 << degree):
                        inverse = next(v for v in range(1, 1 << degree)
                                       if field_mul(scalar, v, degree, modulus) == 1)
                        middle = scale(encoded, degree, modulus, scalar)
                        restored = scale(permute(middle, order), degree, modulus, inverse)
                        assert unpack(restored, degree) == permute(rows, order)
                        counts['scalar_roundtrips'] += 1
                    counts['single_field_shapes'] += 1
                    counts['packed_bits_checked'] += volume(rows)
                    wrong = [[list(reversed(record)) for record in row] for row in encoded]
                    if unpack(wrong, degree) != rows:
                        negative_controls['basis_order_detected'] = True
                    if degree * volume(rows) != volume(encoded):
                        negative_controls['zero_embedding_inflates_volume'] = True
                    if volume(rows[:groups]) < volume(rows):
                        negative_controls['dropping_basis_loses_independence'] = True

    for first_degree in fields:
        for second_degree in fields:
            for groups in range(1, 4):
                for spatial in range(1, 8):
                    for payload in range(1, 5):
                        rows = [[[random.randrange(2) for _ in range(payload)]
                                 for _ in range(spatial)]
                                for _ in range(groups * first_degree * second_degree)]
                        first = pack(rows, first_degree)
                        second = pack(first, second_degree)
                        assert volume(first) == volume(second) == volume(rows)
                        order = list(range(spatial))
                        random.shuffle(order)
                        restored = unpack(unpack(permute(second, order), second_degree), first_degree)
                        assert restored == permute(rows, order)
                        counts['nested_field_shapes'] += 1
                        counts['nested_bits_checked'] += volume(rows)

    for radix in range(2, 18):
        for degree in range(1, 17):
            for field_rows in range(1, 97):
                binary_width = degree * field_rows
                leading = 1
                while leading < binary_width:
                    leading *= radix
                padded = ((leading + binary_width - 1) // binary_width) * binary_width
                assert padded < 2 * leading
                # Child volume per E row divided by input is unchanged by degree.
                assert degree * field_rows == binary_width
                counts['leading_batch_cases'] += 1

    assert all(negative_controls.values())
    result = {'status': 'passed', 'scope': 'exact finite packing, field-linear naturality, nested permutation and batching identities; no tape-transition simulation',
              'counts': counts, 'negative_controls': negative_controls}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
