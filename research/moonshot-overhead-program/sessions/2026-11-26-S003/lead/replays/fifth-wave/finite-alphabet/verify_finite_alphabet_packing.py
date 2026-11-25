#!/usr/bin/env python3
"""Finite complete-identity codec tests, including an odd ring with nilpotents."""
from itertools import islice
from pathlib import Path
import hashlib
import json
import random


class Algebra:
    def __init__(self, q, dual=False):
        self.q, self.dual = q, dual
        self.b, self.s = q.bit_length() - 1, (q - 1).bit_length()
        self.unit = 4 if dual else (2 if q > 2 else 1)
        self.inverse_unit = 7 if dual else pow(self.unit, -1, q)

    def add(self, a, b):
        if self.dual:
            return (a % 3 + b % 3) % 3 + 3 * ((a // 3 + b // 3) % 3)
        return (a + b) % self.q

    def neg(self, a):
        if self.dual:
            return (-a % 3) % 3 + 3 * ((-(a // 3)) % 3)
        return -a % self.q

    def mul(self, a, b):
        if self.dual:
            a0, a1, b0, b1 = a % 3, a // 3, b % 3, b // 3
            return a0 * b0 % 3 + 3 * ((a0 * b1 + a1 * b0) % 3)
        return a * b % self.q


def pack_passes(raw, rows, omega, algebra):
    b, s = algebra.b, algebra.s
    assert len(raw) == rows * b * omega
    out = [0] * (rows * omega * s)
    for c in range(b):
        source, chosen = iter(raw), []
        for _ in range(rows):
            list(islice(source, c * omega))
            chosen.extend(islice(source, omega))
            list(islice(source, (b - c - 1) * omega))
        assert next(source, None) is None
        incoming, old, fresh = iter(chosen), iter(out), []
        for _ in range(rows * omega):
            for bit in range(s):
                previous = next(old)
                fresh.append(next(incoming) if bit == c else previous)
        assert next(incoming, None) is None and next(old, None) is None
        out = fresh
    return out


def values_from_bits(bits, width):
    assert len(bits) % width == 0
    return [sum(bits[start + c] << c for c in range(width))
            for start in range(0, len(bits), width)]


def bits_from_values(values, width):
    return [(value >> c) & 1 for value in values for c in range(width)]


def unpack_bits(bits, rows, omega, b, s):
    out = []
    for row in range(rows):
        for c in range(b):
            for pos in range(omega):
                out.append(bits[(row * omega + pos) * s + c])
    return out


def permute_values(values, rows, side):
    omega = side * side
    return [values[row * omega + y * side + x]
            for row in range(rows) for x in range(side) for y in range(side)]


def mix(values, rows, omega, algebra, inverse=False):
    out = list(values)
    if not inverse:
        out = [algebra.mul(algebra.unit, x) for x in out]
    for row in range(0, rows - 1, 2):
        for pos in range(omega):
            j, k = row * omega + pos, (row + 1) * omega + pos
            out[j] = algebra.add(out[j], algebra.neg(out[k]) if inverse else out[k])
    if inverse:
        out = [algebra.mul(algebra.inverse_unit, x) for x in out]
    return out


def full_binary_program(raw, binary_rows, side, algebra):
    omega, b = side * side, algebra.b
    padded_rows = ((binary_rows + b - 1) // b) * b
    padded = list(raw) + [0] * ((padded_rows - binary_rows) * omega)
    rows = padded_rows // b
    packed = pack_passes(padded, rows, omega, algebra)
    values = values_from_bits(packed, algebra.s)
    values = mix(values, rows, omega, algebra)
    values = permute_values(values, rows, side)
    values = mix(values, rows, omega, algebra, inverse=True)
    assert all(x < 1 << b for x in values)
    result = unpack_bits(bits_from_values(values, algebra.s), rows, omega, b, algebra.s)
    assert not any(result[binary_rows * omega:])
    return result[:binary_rows * omega]


def main():
    rng = random.Random(267327)
    counts = dict(algebras=0, packing_shapes=0, independent_inputs=0,
                  nested_codec_calls=0, outside_input_subset=0,
                  premature_truncation_rejected=0, incomplete_identity_rejected=0)
    algebras = [Algebra(q) for q in (2, 3, 5, 7, 11, 13, 17, 31, 61, 127)]
    algebras.append(Algebra(9, dual=True))
    for algebra in algebras:
        assert algebra.mul(algebra.unit, algebra.inverse_unit) == 1
        assert algebra.b <= algebra.s <= 2 * algebra.b
        counts['algebras'] += 1
        for rows, side in ((2, 2), (3, 3)):
            omega, b, s = side * side, algebra.b, algebra.s
            length = rows * b * omega
            samples = [[rng.randrange(2) for _ in range(length)] for _ in range(12)]
            samples += [[int(i == j) for i in range(length)] for j in range(min(length, 32))]
            counts['packing_shapes'] += 1
            for raw in samples:
                packed = pack_passes(raw, rows, omega, algebra)
                assert len(packed) * b == len(raw) * s
                assert unpack_bits(packed, rows, omega, b, s) == raw
                values = values_from_bits(packed, s)
                middle = mix(values, rows, omega, algebra)
                counts['outside_input_subset'] += any(v >= 1 << b for v in middle)
                # A different codec permutes all bits of current parent records.
                middle_bits = bits_from_values(middle, s)
                component_rows = unpack_bits(middle_bits, rows, omega, s, s)
                child = algebras[(counts['independent_inputs'] + 3) % len(algebras)]
                transported = full_binary_program(component_rows, rows * s, side, child)
                restored_bits = [(transported[(row * s + c) * omega + pos])
                                 for row in range(rows) for pos in range(omega) for c in range(s)]
                transported_values = values_from_bits(restored_bits, s)
                assert transported_values == permute_values(middle, rows, side)
                final = mix(transported_values, rows, omega, algebra, inverse=True)
                assert all(v < 1 << b for v in final)
                got = unpack_bits(bits_from_values(final, s), rows, omega, b, s)
                expected = permute_values(raw, rows * b, side)
                assert got == expected
                counts['nested_codec_calls'] += 1
                counts['independent_inputs'] += 1
                wrong_mid = [v % (1 << b) for v in middle]
                wrong_final = mix(permute_values(wrong_mid, rows, side), rows, omega, algebra, inverse=True)
                counts['premature_truncation_rejected'] += wrong_final != final
                counts['incomplete_identity_rejected'] += transported_values != final
    assert counts['outside_input_subset'] > 0
    assert counts['premature_truncation_rejected'] > 0
    assert counts['incomplete_identity_rejected'] > 0
    # The final algebra is not a field: epsilon is nonzero and square-zero.
    assert algebras[-1].mul(3, 3) == 0 and 3 != 0
    source = Path(__file__)
    result = dict(status='pass', counts=counts,
                  scope='Literal packing scans and complete algebra/permutation identities, including nested codecs; not a complete tape algorithm.',
                  checker_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    source.with_name('finite-alphabet-packing-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
