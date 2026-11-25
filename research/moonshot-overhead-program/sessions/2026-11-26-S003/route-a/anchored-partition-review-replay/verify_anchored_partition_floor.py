"""Finite exact controls for AP; no full multiplier or JR search."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json


def one_coordinate(q):
    t = q.bit_length() - 1
    assert q == 1 << t
    out = []
    for depth in range(t):
        for prefix in range(1 << depth):
            for bit in range(2):
                a = tuple(x for x in range(q)
                          if x >> (t - depth - 1) == 2 * prefix + bit)
                b = tuple(x for x in range(q)
                          if x >> (t - depth - 1) == 2 * prefix + 1 - bit)
                out.append((a, b))
    return out


def tensor_partition(q, k):
    return [(tuple(product(*(r[0] for r in rs))),
             tuple(product(*(r[1] for r in rs))))
            for rs in product(one_coordinate(q), repeat=k)]


def refine(rectangles):
    out = []
    for left, right in rectangles:
        ls = [tuple(x for x in left if sum(x) % 2 == parity)
              for parity in range(2)]
        rs = [tuple(x for x in right if sum(x) % 2 == parity)
              for parity in range(2)]
        out.extend((a, b) for a in ls for b in rs if a and b)
    return out


def inspect(q, k, rectangles, exact=True):
    vertices = tuple(product(range(q), repeat=k))
    lload, rload, edges = Counter(), Counter(), Counter()
    nonproducts = 0
    for left, right in rectangles:
        assert left and right
        projections = []
        for side in (left, right):
            sizes = [len({x[i] for x in side}) for i in range(k)]
            cartesian_size = 1
            for size in sizes:
                cartesian_size *= size
            nonproducts += cartesian_size > len(side)
            projections.append([{x[i] for x in side} for i in range(k)])
        assert all(not (projections[0][i] & projections[1][i])
                   for i in range(k))
        assert len(left) * len(right) * 4 ** k <= q ** (2 * k)
        lload.update(left)
        rload.update(right)
        for a in left:
            for b in right:
                assert all(x != y for x, y in zip(a, b))
                edges[a, b] += 1
    expected = (q * (q - 1)) ** k
    assert len(edges) == expected
    if exact:
        assert set(edges.values()) == {1}
    sl, sr = sum(lload.values()), sum(rload.values())
    assert (2 ** k * expected) ** 2 <= q ** (2 * k) * sl * sr
    assert all(lload[x] and rload[x] for x in vertices)
    return dict(q=q, k=k, rectangles=len(rectangles), edges=expected,
                source_incidence=sl, destination_incidence=sr,
                maximum_load=max(max(lload.values()), max(rload.values())),
                nonproduct_sides=nonproducts)


def main():
    cases = []
    for q, top_k in ((2, 5), (4, 3), (8, 2)):
        for k in range(1, top_k + 1):
            rects = tensor_partition(q, k)
            cases.append(inspect(q, k, rects))
            cases.append(inspect(q, k, refine(rects)))
    star = [
        (tuple((x, b) for x in range(4) if x != a),
         tuple((a, y) for y in range(4) if y != b))
        for a in range(4) for b in range(4)
    ]
    cases.append(inspect(4, 2, star))
    assert cases[-1]['maximum_load'] == 3
    cases.append(inspect(4, 2, star + star, exact=False))
    anchored = []
    for q in (2, 4, 8, 16):
        t = q.bit_length() - 1
        for d in (2, 4, 8, 16, 32):
            h = 2 * d - 1
            rho = Fraction(2 * (q - 1), q)
            cell_count = comb(h, d) * q ** (h - d) * q * (q - 1)
            sl = cell_count * q ** (d - 1) * t ** (d - 1)
            inner = Fraction(sl, q ** h)
            assert inner == comb(h, d) * (q - 1) * t ** (d - 1)
            inner_floor = comb(h, d) * (q - 1) * rho ** (d - 1)
            assert inner >= inner_floor
            outer = comb(h, d) * inner ** d
            outer_floor = comb(h, d) ** (d + 1) * (q - 1) ** d * rho ** (d * (d - 1))
            assert outer >= outer_floor >= 2 ** (d * d - 1)
            assert comb(h, d) >= 2 ** (d - 1)
            anchored.append(dict(q=q, d=d, inner_load=int(inner),
                                 outer_load_bits=outer.numerator.bit_length()))

    parameter_count = 0
    for x in range(1, 1025):
        for d in (2, 4, 8, 16, 32, 64):
            d2 = d * d
            t = (2 * d2 - 2 + x + d2 - 1) // d2
            h = 2 * d - 1
            assert t * d2 >= 2 * d2 - 2 + x
            assert h * t * d >= x
            lower = max(Fraction(x, d), Fraction(d2 - 1))
            assert lower ** 3 >= Fraction(3, 4) * x * x
            parameter_count += 1

    controls = []
    try:
        inspect(4, 1, tensor_partition(4, 1)[1:])
    except AssertionError:
        controls.append('omitted rectangle fails exact cover')
    else:
        raise AssertionError('omitted rectangle was accepted')
    try:
        inspect(4, 1, [(((0,), (1,)), ((0,), (2,)))])
    except AssertionError:
        controls.append('shared coordinate projection is rejected')
    else:
        raise AssertionError('invalid support was accepted')
    a = ((0, 0, 0), (1, 1, 0))
    b = ((1, 0, 1), (0, 1, 1))
    supports = {tuple(i for i in range(3) if u[i] != v[i])
                for u in a for v in b}
    assert all(len(s) == 2 for s in supports) and len(supports) > 1
    controls.append('cross-cell far rectangle lies outside retained placement')
    assert max(Fraction(2, 2), Fraction(3)) ** 3 < Fraction(3, 4) * 1024 ** 2
    controls.append('removed rank guard defeats claimed x-dependent floor')

    source = Path(__file__)
    report = dict(status='passed', claim_scope='finite exact AP controls only',
                  source_sha256=sha256(source.read_bytes()).hexdigest(),
                  cover_cases=cases, cover_case_count=len(cases),
                  verified_edges=sum(c['edges'] for c in cases),
                  nonproduct_sides=sum(c['nonproduct_sides'] for c in cases),
                  anchored_profiles=anchored, parameter_profiles=parameter_count,
                  controls=controls, jr_proved=False, full_multiplier_run=False)
    dest = source.with_name('anchored-partition-floor-verification.json')
    dest.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in
                     ('status', 'source_sha256', 'cover_case_count',
                      'verified_edges', 'nonproduct_sides', 'parameter_profiles',
                      'controls')}))


if __name__ == '__main__':
    main()
