#!/usr/bin/env python3
"""Exact triadic ring and residual checks; not a tape-time simulation."""
from itertools import product
from pathlib import Path
from random import Random
import json

COUNTS = {}

def inc(key, n=1):
    COUNTS[key] = COUNTS.get(key, 0)+n

def ordinary(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c

def reduce_ring(poly, n, modulus):
    c = list(poly)+[0]*max(0, 2*n-len(poly))
    for j in range(len(c)-1, 2*n-1, -1):
        value = c[j]
        c[j-n] -= value
        c[j-2*n] -= value
    return [x % modulus for x in c[:2*n]]

def add(a, b, modulus):
    return [(x+y) % modulus for x, y in zip(a, b)]

def scale(a, scalar, modulus):
    return [x*scalar % modulus for x in a]

def shift(a, power, n, modulus):
    return reduce_ring([0]*(power % (3*n))+list(a), n, modulus)

def naive(a, b, n, modulus):
    return reduce_ring(ordinary(a, b), n, modulus)

def fft(values, step, n, modulus, inverse=False):
    length = len(values)
    if length == 1:
        return [values[0].copy()]
    sub = [fft(values[r::3], 3*step, n, modulus, inverse) for r in range(3)]
    out = [[0]*(2*n) for _ in range(length)]
    inv3 = pow(3, -1, modulus) if inverse else 1
    for j in range(length//3):
        for t in range(3):
            index = j+t*(length//3)
            v = sub[0][j].copy()
            v = add(v, shift(sub[1][j], step*index, n, modulus), modulus)
            v = add(v, shift(sub[2][j], 2*step*index, n, modulus), modulus)
            out[index] = scale(v, inv3, modulus)
    return out

def direct_dft(values, step, n, modulus):
    out = []
    for j in range(len(values)):
        value = [0]*(2*n)
        for i, x in enumerate(values):
            value = add(value, shift(x, step*i*j, n, modulus), modulus)
        out.append(value)
    return out

def embed(blocks, k, m, modulus):
    out = [[0]*(2*m) for _ in range(3*k)]
    inv3 = pow(3, -1, modulus)
    for i, value in enumerate(blocks):
        for offset, factor in ((0, 2), (k, -1), (2*k, -1)):
            j = (i+offset) % (3*k)
            out[j] = add(out[j], scale(value, factor*inv3, modulus), modulus)
    return out

def triadic(a, b, n, modulus):
    assert len(a) == len(b) == 2*n
    if n <= 3:
        return naive(a, b, n, modulus)
    exponent, v = 0, n
    while v > 1:
        assert v % 3 == 0
        exponent, v = exponent+1, v//3
    m, k = 3**((exponent+1)//2), 3**(exponent//2)
    assert m*k == n and m % k == 0
    ablocks = [a[i*m:(i+1)*m]+[0]*m for i in range(2*k)]
    bblocks = [b[i*m:(i+1)*m]+[0]*m for i in range(2*k)]
    fa = fft(embed(ablocks, k, m, modulus), m//k, m, modulus)
    fb = fft(embed(bblocks, k, m, modulus), m//k, m, modulus)
    pointwise = []
    active = 0
    for j in range(3*k):
        if j % 3 == 0:
            assert not any(fa[j]) and not any(fb[j])
            pointwise.append([0]*(2*m))
            inc("zero_frequency_certificates")
        else:
            pointwise.append(triadic(fa[j], fb[j], m, modulus))
            active += 1
    assert active == 2*k
    inc("exact_two_k_child_invoices")
    recovered = fft(pointwise, -m//k, m, modulus, inverse=True)
    ucoeffs = [row.copy() for row in recovered[:2*k]]
    for j in range(2*k, 3*k):
        negative = scale(recovered[j], -1, modulus)
        ucoeffs[j-k] = add(ucoeffs[j-k], negative, modulus)
        ucoeffs[j-2*k] = add(ucoeffs[j-2*k], negative, modulus)
    flat = [0]*(2*n+m)
    for i, value in enumerate(ucoeffs):
        for j, x in enumerate(value):
            flat[i*m+j] += x
    result = reduce_ring(flat, n, modulus)
    assert result == naive(a, b, n, modulus)
    inc("recursive_cyclotomic_products")
    return result

def convolution_mod(a, b, modulus):
    h = max(len(a), len(b))
    n = 1
    while n < h:
        n *= 3
    result = triadic([x % modulus for x in a]+[0]*(2*n-len(a)),
                     [x % modulus for x in b]+[0]*(2*n-len(b)), n, modulus)
    result = result[:len(a)+len(b)-1]
    assert result == [x % modulus for x in ordinary(a, b)]
    return result

def main():
    rng = Random(2026112609)
    for bits in (1, 2, 3, 5):
        modulus = 1 << bits
        for m in (1, 3, 9):
            k = 1
            while k <= m:
                length, step = 3*k, m//k
                one = [1]+[0]*(2*m-1)
                for j in range(1, length):
                    total = [0]*(2*m)
                    for i in range(length):
                        total = add(total, shift(one, step*i*j, m, modulus), modulus)
                    assert not any(total)
                    inc("principal_root_orthogonality_sums")
                values = [[rng.randrange(modulus) for _ in range(2*m)]
                          for _ in range(length)]
                transformed = fft(values, step, m, modulus)
                assert transformed == direct_dft(values, step, m, modulus)
                assert fft(transformed, -step, m, modulus, inverse=True) == values
                inc("fft_direct_and_inverse_controls")
                k *= 3
        for n in (1, 3, 9, 27, 81):
            for _ in range(3):
                a = [rng.randrange(modulus) for _ in range(2*n)]
                b = [rng.randrange(modulus) for _ in range(2*n)]
                assert triadic(a, b, n, modulus) == naive(a, b, n, modulus)
                inc("complete_cyclotomic_product_cases")
        for value in range(modulus):
            c = next(c for c in range(3) if (value+c*modulus) % 3 == 0)
            quotient = (value+c*modulus)//3
            assert 0 <= quotient < modulus and 3*quotient % modulus == value
            inc("exact_division_by_three_controls")

    for h in (2, 5, 10, 28):
        for bound in (1, 3, 8):
            a = [rng.randrange(256) for _ in range(h)]
            b = [rng.randrange(256) for _ in range(h)]
            actual = ordinary(a, b)+[0]
            error = [rng.randrange(-bound, bound+1) for _ in actual]
            candidate = [x-y for x, y in zip(actual, error)]
            modulus = 1 << (2*bound).bit_length()
            residues = convolution_mod(a, b, modulus)+[0]
            recovered = [(x-y) % modulus for x, y in zip(residues, candidate)]
            recovered = [x if 2*x < modulus else x-modulus for x in recovered]
            assert recovered == error
            assert [x+y for x, y in zip(candidate, recovered)] == actual
            inc("complete_bounded_amplitude_corrections")
            positive = [rng.randrange(2*modulus) for _ in actual]
            low = [x % modulus for x in positive]
            assert (sum(low) == sum(positive)) == all(x < modulus for x in positive)
            inc("positive_mass_alias_certificates")

    # Exact ceiling-recursion controls for the normalized bit invoice.
    invoice = [1, 1]
    for ell in range(2, 2049):
        invoice.append(2*invoice[(ell+1)//2]+ell)
        assert invoice[ell] <= 4*ell*(1+(ell-1).bit_length())
        inc("ceiling_recursion_bounds")

    # The absolute error promise needs M>2B, not merely M>=2B.
    assert (-2) % 4 == 2 % 4 and -2 != 2
    inc("strict_centered_modulus_control")
    # Dropping the amplitude promise aliases a nonzero residual to zero.
    assert 16 % 16 == 0
    inc("unpromised_modulus_alias_control")
    # Signed errors defeat the positive mass certificate.
    assert sum([16, -16]) == 0 and [x % 16 for x in (16, -16)] == [0, 0]
    inc("signed_mass_false_certificate_control")
    # Choosing n too small changes an ordinary product into a ring residue.
    assert reduce_ring([0]*6+[1], 3, 8) != [0]*6+[1]
    inc("ordinary_embedding_degree_control")

    for h in (1, 2, 3):
        for _ in range(20):
            u = 3
            matrix = [[rng.randrange(-3, 4) for _ in range(h)] for _ in range(h)]
            values = [u*u*sum(matrix[j][k]*a[j]*b[k] for j in range(h) for k in range(h))
                      for a in product((0, 1), repeat=h) for b in product((0, 1), repeat=h)]
            amplitude = max(abs(x) for x in values)
            frobenius_sq = sum(x*x for row in matrix for x in row)
            assert 16*amplitude**2 >= u**4*frobenius_sq
            inc("bilinear_amplitude_gate_controls")

    result = {"status": "all exact finite controls passed", "seed": 2026112609,
              "scope": "cyclotomic arithmetic, FFT identities and correction; not a tape simulation",
              "counts": COUNTS}
    Path(__file__).with_name("bounded-amplitude-verification.json").write_text(
        json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
