#!/usr/bin/env python3
"""Finite reference check for the grouped-residue / fixed ambient monomial word seam."""

import json
import random


def pmul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def pdiv(a, b):
    if not b:
        raise ZeroDivisionError
    quotient = 0
    while a.bit_length() >= b.bit_length():
        shift = a.bit_length() - b.bit_length()
        quotient ^= 1 << shift
        a ^= b << shift
    return quotient, a


def pgcd(a, b):
    while b:
        a, b = b, pdiv(a, b)[1]
    return a


def inverse_mod(a, modulus):
    r, s, u, v = modulus, a, 0, 1
    while s:
        quotient, remainder = pdiv(r, s)
        r, s, u, v = s, remainder, v, u ^ pmul(quotient, v)
    assert r == 1
    return pdiv(u, modulus)[1]


def field_modulus(b):
    for h in range((1 << b) + 1, 2 << b, 2):
        u = 2
        for i in range(1, b + 1):
            u = pdiv(pmul(u, u), h)[1]
            if i <= b // 2 and pgcd(h, u ^ 2) != 1:
                break
        else:
            if u == 2:
                return h
    raise AssertionError("no irreducible modulus")


def powers_of_sigma(value, count, mul):
    words = []
    for _ in range(count):
        words.append(value)
        value = mul(value, value)
    return words


def xor_words(words):
    result = 0
    for word in words:
        result ^= word
    return result


def combinations(columns, bits):
    return xor_words(x for i, x in enumerate(columns) if bits >> i & 1)


def left_inverse(columns, b):
    """Reduce [A | I_b] to [I; 0] with row operations, returning d left rows."""
    d = len(columns)
    rows = [sum(((x >> j) & 1) << i for i, x in enumerate(columns))
            | (1 << (j + d)) for j in range(b)]
    for i in range(d):
        pivot = next((j for j in range(i, b) if rows[j] >> i & 1), None)
        if pivot is None:
            raise ValueError("dependent columns")
        rows[i], rows[pivot] = rows[pivot], rows[i]
        for j in range(b):
            if j != i and rows[j] >> i & 1:
                rows[j] ^= rows[i]
    assert all(row % (1 << d) == (1 << j if j < d else 0) for j, row in enumerate(rows))
    return [row >> d for row in rows[:d]]


def reps(b, h):
    q = 1 << b
    c = b // 3

    def mul(x, y):
        return pdiv(pmul(x, y), h)[1]

    for gamma in range(1, q):
        orbit = powers_of_sigma(gamma, b, mul)
        try:
            left_inverse(orbit, b)
        except ValueError:
            continue
        break
    else:
        raise AssertionError("no normal element")

    subbasis = [orbit[j] ^ orbit[j + c] ^ orbit[j + 2 * c] for j in range(c)]
    assert xor_words(subbasis) == 1
    wordmask = (1 << c) - 1
    remaining = set(range(0, 1 << c, 2))
    result = []
    while remaining:
        start = min(remaining)
        y = start
        words = []
        while True:
            remaining.remove(y)
            words.append(y)
            y = ((y << 1) & wordmask) | (y >> (c - 1))
            if y & 1:
                y ^= wordmask
            if y == start:
                break
        alpha = combinations(subbasis, start)
        s = mul(alpha, alpha) ^ alpha
        ground_orbit = powers_of_sigma(s, len(words), mul)
        assert len(set(ground_orbit)) == len(words) and mul(ground_orbit[-1], ground_orbit[-1]) == s
        for word, expected in zip(words, ground_orbit):
            anchor = combinations(subbasis, word)
            assert mul(anchor, anchor) ^ anchor == expected
        polynomial = [1]
        for root in ground_orbit:
            out = [0] * (len(polynomial) + 1)
            for j, a in enumerate(polynomial):
                out[j] ^= mul(root, a)
                out[j + 1] ^= a
            polynomial = out
        assert all(x in (0, 1) for x in polynomial)
        minimal = sum(x << j for j, x in enumerate(polynomial))
        columns = [1]
        for _ in range(1, len(words)):
            columns.append(mul(columns[-1], s))
        result.append((s, len(words), minimal, columns, left_inverse(columns, b)))
    assert sum(group[1] for group in result) == 1 << (c - 1)
    return mul, result


def transpose_rows(rows, width):
    return [sum(((row >> j) & 1) << i for i, row in enumerate(rows)) for j in range(width)]


def batch_product(input_rows, coefficient_rows, width, counts):
    """Multiply row-packed A times B. Pad last tile to width then discard its padding."""
    output = []
    for start in range(0, len(input_rows), width):
        batch = input_rows[start:start + width]
        tile = batch + [0] * (width - len(batch))
        out = xor_batch_rank7(tile, coefficient_rows, width)
        output.extend(out[:len(batch)])
        counts["matrix_tiles"] += 1
        counts["short_final_tiles"] += len(batch) < width
    return output


def xor_batch_rank7(left, right, width):
    """Strassen over F2, solely to test the same ordered bilinear block recursion."""
    m = 1 << (width - 1).bit_length()

    def add(a, b):
        return [x ^ y for x, y in zip(a, b)]

    def split(a, n):
        half = n // 2
        mask = (1 << half) - 1
        return ([x & mask for x in a[:half]], [x >> half for x in a[:half]],
                [x & mask for x in a[half:]], [x >> half for x in a[half:]])

    def product(a, b, n):
        if n <= 4:
            return [combinations(b, x) for x in a]
        half = n // 2
        a11, a12, a21, a22 = split(a, n)
        b11, b12, b21, b22 = split(b, n)
        p1 = product(add(a11, a22), add(b11, b22), half)
        p2 = product(add(a21, a22), b11, half)
        p3 = product(a11, add(b12, b22), half)
        p4 = product(a22, add(b21, b11), half)
        p5 = product(add(a11, a12), b22, half)
        p6 = product(add(a21, a11), add(b11, b12), half)
        p7 = product(add(a12, a22), add(b21, b22), half)
        c11 = add(add(p1, p4), add(p5, p7))
        c12 = add(p3, p5)
        c21 = add(p2, p4)
        c22 = add(add(p1, p2), add(p3, p6))
        return [x | (y << half) for x, y in zip(c11 + c21, c12 + c22)]

    return product(left + [0] * (m - len(left)), right + [0] * (m - len(right)), m)[:width]


def horner(bits, s, mul):
    value = 0
    for j in reversed(range(bits.bit_length())):
        value = mul(value, s) ^ ((bits >> j) & 1)
    return value


def ordinary_coset_remainder(f, q, trace_terms, s, mul):
    """Descending ordinary monic long division over the ambient field."""
    coeffs = [(f >> i) & 1 for i in range(q)]
    v = max(trace_terms)
    for n in range(q - 1, v - 1, -1):
        top = coeffs[n]
        if top:
            shift = n - v
            coeffs[shift] ^= mul(top, s)
            for j in trace_terms:
                coeffs[shift + j] ^= top
    assert not any(coeffs[v:])
    return coeffs[:v]


def run(b, counts):
    h = field_modulus(b)
    mul, groups = reps(b, h)
    rng = random.Random(b * 7937)
    c, q = b // 3, 1 << b
    v = 1 << (2 * c + 1)
    m = q // v
    trace = xor_words(1 << j for i in (1, 1 << c, 1 << (2 * c)) for j in (i, 2 * i))
    terms = [i for i in range(trace.bit_length()) if trace >> i & 1]
    assert terms[-1] == v
    f = rng.getrandbits(q)
    digits = []
    fwork = f
    for _ in range(m):
        fwork, rem = pdiv(fwork, trace)
        digits.append(rem)
    assert fwork == 0
    polys = transpose_rows(digits, v)
    oracle_grouped = []
    arbitrary_grouped = []
    product_of_minimals = 1
    for s, d, minimal, vectors, inverse_rows in groups:
        product_of_minimals = pmul(product_of_minimals, minimal)
        assert d == minimal.bit_length() - 1
        for small in range(1 << d):
            full = horner(small, s, mul)
            assert full == combinations(vectors, small)
            assert sum(((row & full).bit_count() % 2) << j for j, row in enumerate(inverse_rows)) == small
            counts["exhaustive_scalar_encodings"] += 1

        inverse_columns = transpose_rows(inverse_rows, b)
        grouped = [pdiv(p, minimal)[1] for p in polys]
        words = batch_product(grouped, vectors, b, counts)
        assert words == ordinary_coset_remainder(f, q, terms, s, mul)
        counts["ordinary_monic_remainder_coefficients"] += v
        assert batch_product(words, inverse_columns, b, counts) == grouped
        assert all(x == horner(w, s, mul) for x, w in zip(words, grouped))
        oracle_grouped.append(grouped)
        arbitrary = [rng.randrange(1 << d) for _ in range(v)]
        ambient = [horner(word, s, mul) for word in arbitrary]
        decoded = batch_product(ambient, inverse_columns, b, counts)
        assert decoded == arbitrary and batch_product(decoded, vectors, b, counts) == ambient
        arbitrary_grouped.append(decoded)
        counts["arbitrary_monomial_words_recovered"] += v
        if d > 1:
            assert horner(2, mul(s, s), mul) != horner(2, s, mul)
            counts["wrong_conjugate_controls"] += 1
        forbidden = next(x for x in range(1 << b) if x not in {horner(i, s, mul) for i in range(1 << d)})
        as_mixed = sum(((row & forbidden).bit_count() % 2) << j for j, row in enumerate(inverse_rows))
        assert horner(as_mixed, s, mul) != forbidden
        counts["outside_image_controls"] += 1

    assert product_of_minimals.bit_length() == m + 1
    selectors = []
    for _, _, minimal, _, _ in groups:
        cofactor, rem = pdiv(product_of_minimals, minimal)
        assert rem == 0
        selectors.append(pmul(cofactor, inverse_mod(cofactor, minimal)))
    for source, original in [(oracle_grouped, f), (arbitrary_grouped, None)]:
        gs = [pdiv(xor_words(pmul(a[k], e) for a, e in zip(source, selectors)),
                   product_of_minimals)[1] for k in range(v)]
        digit_grid = transpose_rows(gs, m)
        recovered = 0
        for digit in reversed(digit_grid):
            recovered = xor_words(recovered << t for t in terms) ^ digit
        if original is not None:
            assert recovered == original
        for i, (s, _, _, vectors, _) in enumerate(groups):
            assert ordinary_coset_remainder(recovered, q, terms, s, mul) == [
                combinations(vectors, x) for x in source[i]]
            counts["independent_CRT_reconstruction_coefficients"] += v
        counts["coefficient_order_reconstructions"] += 1
    return {"b": b, "field_modulus": hex(h), "orbit_degrees": [t[1] for t in groups],
            "coefficient_bits": q, "ambient_bits": b * v * len(groups)}


if __name__ == "__main__":
    counts = dict.fromkeys(["matrix_tiles", "short_final_tiles", "exhaustive_scalar_encodings",
                            "ordinary_monic_remainder_coefficients", "arbitrary_monomial_words_recovered",
                            "wrong_conjugate_controls", "outside_image_controls",
                            "independent_CRT_reconstruction_coefficients",
                            "coefficient_order_reconstructions"], 0)
    degrees = [run(b, counts) for b in (3, 6, 9, 12, 15)]
    print(json.dumps({"degrees": degrees, "counts": counts}, indent=2))
