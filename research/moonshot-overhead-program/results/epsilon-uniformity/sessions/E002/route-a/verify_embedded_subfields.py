#!/usr/bin/env python3
"""Exact finite Frobenius-kernel and local character-sum checks.
Not a physical tape-machine or an asymptotic complexity experiment.
"""
from __future__ import annotations
from hashlib import sha256
from itertools import combinations, islice
from math import gcd
from pathlib import Path
import json

COUNTS = dict(root_units=0, kernels=0, emitted_elements=0,
              closure_pairs=0, embedded_f4_roots=0, coefficients=0,
              wrong_exponent_rejections=0, nondivisibility_negatives=0,
              degree_alias_negatives=0)

class Field:
    def __init__(self, degree: int, modulus: int):
        self.degree, self.modulus, self.order = degree, modulus, 1 << degree
    def mul(self, a: int, b: int) -> int:
        value = 0
        while b:
            if b & 1:
                value ^= a
            b >>= 1
            a <<= 1
            if a & self.order:
                a ^= self.modulus
        return value
    def power(self, a: int, exponent: int) -> int:
        value = 1
        while exponent:
            if exponent & 1:
                value = self.mul(value, a)
            a = self.mul(a, a)
            exponent >>= 1
        return value
    def inverse(self, a: int) -> int:
        assert a != 0
        return self.power(a, self.order - 2)
    def add(self, values) -> int:
        answer = 0
        for value in values:
            answer ^= value
        return answer


def frobenius_kernel(field: Field, r: int) -> list[int]:
    s = field.degree
    columns = [field.power(1 << j, 1 << r) ^ (1 << j) for j in range(s)]
    rows = [sum(((columns[j] >> i) & 1) << j for j in range(s)) for i in range(s)]
    pivots = []
    rank = 0
    for col in range(s):
        chosen = next((i for i in range(rank, s) if (rows[i] >> col) & 1), None)
        if chosen is None:
            continue
        rows[rank], rows[chosen] = rows[chosen], rows[rank]
        for i in range(s):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        pivots.append(col)
        rank += 1
    basis = []
    for col in range(s):
        if col in pivots:
            continue
        vector = 1 << col
        for i, pivot in enumerate(pivots):
            if (rows[i] >> col) & 1:
                vector |= 1 << pivot
        assert field.power(vector, 1 << r) == vector
        basis.append(vector)
    return basis


def enumerate_span(basis: list[int]) -> list[int]:
    values = []
    for mask in range(1 << len(basis)):
        value = 0
        for i, vector in enumerate(basis):
            if (mask >> i) & 1:
                value ^= vector
        values.append(value)
    assert len(set(values)) == len(values)
    return values


def dense_coefficients(field: Field, nodes: tuple[int, ...], target: int) -> list[int]:
    result = [1]
    denominator = 1
    for node in nodes:
        if node == target:
            continue
        nxt = [0] * (len(result) + 1)
        for i, value in enumerate(result):
            nxt[i] ^= field.mul(node, value)
            nxt[i + 1] ^= value
        result = nxt
        denominator = field.mul(denominator, target ^ node)
    inverse = field.inverse(denominator)
    return [field.mul(value, inverse) for value in result]


def lagrange_value(field: Field, nodes: tuple[int, ...], target: int, point: int) -> int:
    value = 1
    for node in nodes:
        if node != target:
            value = field.mul(value, field.mul(point ^ node, field.inverse(target ^ node)))
    return value


def check_character_sum(field: Field, values: list[int]) -> None:
    q = len(values)
    if q > 16 or q < 4:
        return
    nodes = values[:min(q, 8)]
    check_count = min(3, q - 2)
    nonzero = [value for value in values if value]
    for size in range(1, check_count + 1):
        for subset in islice(combinations(nodes, size), 40):
            for target in subset:
                dense = dense_coefficients(field, subset, target)
                evaluations = [(point, lagrange_value(field, subset, target, point))
                               for point in nonzero]
                for i in range(check_count):
                    value = field.add(field.mul(field.power(point, q - 1 - i), ev)
                                      for point, ev in evaluations)
                    want = dense[i] if i < len(dense) else 0
                    assert value == want
                    COUNTS['coefficients'] += 1
                    wrong = field.add(field.mul(field.power(point, q - 1 + i), ev)
                                      for point, ev in evaluations)
                    COUNTS['wrong_exponent_rejections'] += wrong != want
    assert field.add(field.power(point, q - 1) for point in nonzero) == 1
    COUNTS['degree_alias_negatives'] += 1


def main() -> None:
    for degree, modulus in ((2, 0b111), (4, 0b10011), (8, 0b100011011)):
        field = Field(degree, modulus)
        # These exhaustive root checks validate the tiny test field only;
        # the subfield construction below does not use root enumeration.
        for value in range(1, field.order):
            assert field.mul(value, field.inverse(value)) == 1
            COUNTS['root_units'] += 1
        for r in range(1, degree + 1):
            if degree % r:
                continue
            basis = frobenius_kernel(field, r)
            assert len(basis) == r
            values = enumerate_span(basis)
            value_set = set(values)
            assert 0 in value_set and 1 in value_set
            assert len(values) == 1 << r
            for value in values:
                assert field.power(value, 1 << r) == value
                if value:
                    assert field.inverse(value) in value_set
                if r % 2 == 0 and field.mul(value, value) ^ value ^ 1 == 0:
                    COUNTS['embedded_f4_roots'] += 1
            for left in values:
                for right in values:
                    assert left ^ right in value_set
                    assert field.mul(left, right) in value_set
                    COUNTS['closure_pairs'] += 1
            COUNTS['kernels'] += 1
            COUNTS['emitted_elements'] += len(values)
            check_character_sum(field, values)
        for r in range(2, degree):
            if degree % r:
                basis = frobenius_kernel(field, r)
                assert len(basis) == gcd(r, degree) < r
                COUNTS['nondivisibility_negatives'] += 1
    assert COUNTS['wrong_exponent_rejections'] > 0
    root = Path(__file__).resolve().parent
    note = root / 'EMBEDDED-SUBFIELD-ENUMERATION.md'
    report = {
        'status': 'PASS_EXACT_SUBFIELD_COMPONENT',
        'counts': COUNTS,
        'note_sha256': sha256(note.read_bytes()).hexdigest(),
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Finite Frobenius kernels, distinct enumeration, closure and local Lagrange coefficients inside larger fields. Not physical machine execution or asymptotic proof.',
    }
    (root / 'embedded-subfield-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
