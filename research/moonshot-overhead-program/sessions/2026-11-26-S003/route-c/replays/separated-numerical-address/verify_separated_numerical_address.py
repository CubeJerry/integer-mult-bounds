#!/usr/bin/env python3
"""Exact endpoint identity and query-dependent address support checks.

This does not implement a joint star-transposition sum or prove a tape lower
bound. It tests the source-derived local obstruction in the companion note.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def mm(a, b):
    n = len(a)
    return [[sum((a[i][h] * b[h][j] for h in range(n)), Q(0))
             for j in range(n)] for i in range(n)]


def bits(t):
    return tuple((t >> i) & 1 for i in range(4))


def sign(t):
    return -1 if t & 1 else 1


def diagonal(values):
    return [[Q(values[i] if i == j else 0) for j in range(16)]
            for i in range(16)]


def local_permutation(t):
    xj, x0, zj, z0 = bits(t)
    return z0 | (zj << 1) | (x0 << 2) | (xj << 3)


def field_swap(t, left, right, f):
    mask = (1 << f) - 1
    delta = ((t >> (left*f)) ^ (t >> (right*f))) & mask
    return t ^ (delta << (left*f)) ^ (delta << (right*f))


def global_middle(t, j, m, f):
    # Field order X_1,...,X_m,X_0,Z_1,...,Z_m,Z_0.
    xj, x0, zj, z0 = j, m, m+1+j, 2*m+1
    moved = field_swap(field_swap(t, xj, z0, f), zj, x0, f)
    mask = (1 << f) - 1
    field = lambda i: (t >> (i*f)) & mask
    parity = ((field(xj) & field(zj)) ^
              (field(x0) & field(z0))).bit_count() & 1
    return moved, sign(parity)


def column_middle(t, j, m, f):
    result = t
    phase = 1
    positions = (j, m, m+1+j, 2*m+1)
    for c in range(f):
        digit = sum(((t >> (p*f+c)) & 1) << i
                    for i, p in enumerate(positions))
        moved = local_permutation(digit)
        inp, out = bits(digit), bits(moved)
        phase *= sign(inp[0]*inp[2] + out[0]*out[2])
        for i, p in enumerate(positions):
            result &= ~(1 << (p*f+c))
            result |= ((moved >> i) & 1) << (p*f+c)
    return result, phase


def main():
    haux = []
    kernel = []
    for out in range(16):
        sj, s0, tj, t0 = bits(out)
        hrow, krow = [], []
        for inp in range(16):
            xj, x0, zj, z0 = bits(inp)
            hrow.append(Q(sign(x0*s0+z0*t0), 2)
                        if xj == sj and zj == tj else Q(0))
            exponent = (xj+s0)*(t0+zj)+(x0+sj)*(tj+z0)
            krow.append(Q(sign(exponent), 4))
        haux.append(hrow)
        kernel.append(krow)
    daux = diagonal([sign(bits(t)[1]*bits(t)[3]) for t in range(16)])
    dj = diagonal([sign(bits(t)[0]*bits(t)[2]) for t in range(16)])
    perm = [[Q(int(i == local_permutation(j))) for j in range(16)]
            for i in range(16)]
    esource = mm(haux, daux)
    edest = mm(daux, haux)
    middle = mm(mm(dj, perm), dj)
    assert mm(mm(edest, middle), esource) == kernel
    identity = diagonal([1]*16)
    assert mm(esource, edest) == identity
    assert mm(edest, esource) == identity
    assert mm(mm(esource, kernel), edest) == middle

    negative_controls = 0
    # All diagonal phases preserve support, so no fixed permutation can
    # represent two different query supports; tested globally below.
    assert mm(mm(edest, perm), esource) != kernel
    negative_controls += 1
    assert mm(mm(edest, middle), edest) != kernel
    negative_controls += 1
    wrong_perm = [[Q(int(i == field_swap(j, 0, 3, 1)))
                   for j in range(16)] for i in range(16)]
    assert mm(mm(edest, mm(mm(dj, wrong_perm), dj)), esource) != kernel
    negative_controls += 1

    cases = []
    checks = 0
    support_witnesses = 0
    for m, f in ((1, 1), (3, 1), (5, 1), (3, 2)):
        count = 1 << (2*(m+1)*f)
        for j in range(m):
            seen = set()
            active = {j, m, m+1+j, 2*m+1}
            inactive_mask = sum(((1 << f)-1) << (i*f)
                                for i in range(2*(m+1)) if i not in active)
            for t in range(count):
                image, phase = global_middle(t, j, m, f)
                assert (image, phase) == column_middle(t, j, m, f)
                assert (image & inactive_mask) == (t & inactive_mask)
                assert global_middle(image, j, m, f) == (t, phase)
                seen.add(image)
                checks += 1
            assert len(seen) == count
            for other in range(m):
                if other == j:
                    continue
                witness = 1 << (j*f)
                assert global_middle(witness, j, m, f)[0] != \
                    global_middle(witness, other, m, f)[0]
                support_witnesses += 1
        cases.append({"m": m, "f": f, "full_addresses": count,
                      "query_maps": m})
    negative_controls += support_witnesses

    # Exact squared version of the regular-price cancellation.
    cancellation_checks = 0
    for m in (3, 7, 31, 127, 1023):
        for dim in (2, 3, 7, 31):
            arity = 2*(m+dim-1)
            for f in (2, 4, 16, 1024):
                a = arity*f
                assert Q(m*(1+f), 1+a) <= Q(3, 4)
                cancellation_checks += 1

    result = {
        "status": "PASS",
        "exact_kernel_entries": 256,
        "full_global_query_outputs": checks,
        "support_witnesses": support_witnesses,
        "negative_controls": negative_controls,
        "regular_price_cancellation_checks": cancellation_checks,
        "cases": cases,
        "scope": "Exact endpoint identity and literal query-map obstruction; no joint executor or runtime lower bound.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = Path(__file__).with_name("separated-numerical-address-verification.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
