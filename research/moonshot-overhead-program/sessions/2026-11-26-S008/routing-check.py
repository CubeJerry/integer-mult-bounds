"""Exact finite checks for the S008 cross-anchor constructions (Python stdlib)."""

from collections import Counter
from itertools import combinations, product
from math import prod
from random import Random
import json


def half(x, y, b, t, destination):
    """Whether y belongs to the source or opposite half at bit b of x."""
    return (y >> (t - b)) == ((x >> (t - b)) ^ int(destination))


def has_endpoint(label, base, state, d, t, destination):
    offsets, depths = state
    for a, (row, origin) in enumerate(zip(label, base)):
        for i, (value, x) in enumerate(zip(row, origin)):
            if a >= d or i >= d:
                if value != x:
                    return False
            elif i == 0:
                if value != (x + (offsets[a] if destination else 0)) % (2**t):
                    return False
            elif not half(x, value, depths[a * (d - 1) + i - 1], t, destination):
                return False
    return True


def target(base, state, d, t):
    offsets, depths = state
    x = [list(row) for row in base]
    for a in range(d):
        x[a][0] = (x[a][0] + offsets[a]) % (2**t)
        for i in range(1, d):
            x[a][i] ^= 1 << (t - depths[a * (d - 1) + i - 1])
    return x


def gram(left, right, d, dest_left, dest_right, modulus):
    """Read the oriented Gram entries from the original rational B2 form."""
    k = sum(sum(x != y for x, y in zip(a, b)) == d for a, b in zip(left, right))
    signs_left = (-1, 1) if dest_left else (1, -1)
    signs_right = (-1, 1) if dest_right else (1, -1)
    inv4 = pow(4, -1, modulus)
    # Columns (e ± z_v)/2. Only equal-outer-coordinate feature blocks pair.
    zz = 2 - 4 * pow(d, -1, modulus) * k
    return tuple((2 + s * t * zz) * inv4 % modulus for s in signs_left for t in signs_right)


IDENTITY = (1, 0, 0, 1)


def check_pair(base, first, second, d, t):
    if first[1] != second[1]:
        j = next(i for i, (b, c) in enumerate(zip(first[1], second[1])) if b != c)
        if first[1][j] > second[1][j]:
            first, second = second, first
        a, offset = divmod(j, d - 1)
        i = offset + 1
        left = [list(word) for word in base]
        right = target(base, second, d, t)
        left[a][i] = right[a][i]
        dest_left = False
        kind = 'cross'
    else:
        a = next(i for i, (v, w) in enumerate(zip(first[0], second[0])) if v != w)
        left = target(base, first, d, t)
        right = target(base, second, d, t)
        for i in range(1, d):
            right[a][i] ^= 1
        dest_left = True
        kind = 'destinations'
    assert has_endpoint(left, base, first, d, t, dest_left)
    assert has_endpoint(right, base, second, d, t, True)
    for modulus in (3, 9, 27):
        assert gram(base, left, d, False, dest_left, modulus) == IDENTITY
        assert gram(base, right, d, False, True, modulus) == IDENTITY
        assert gram(left, right, d, dest_left, True, modulus) != IDENTITY
    return kind


def check_family(d, t, exhaustive=True):
    rng = Random(61 * d + 7 * t)
    q, h = 2**t, 2 * d - 1
    base = tuple(tuple(rng.randrange(q) for _ in range(h)) for _ in range(h))
    size = (q - 1)**d * (t - 1)**(d * (d - 1))
    if exhaustive:
        states = list(product(product(range(1, q), repeat=d),
                              product(range(1, t), repeat=d * (d - 1))))
        assert len(states) == size
        pairs = combinations(states, 2)
    else:
        def one():
            return (tuple(rng.randrange(1, q) for _ in range(d)),
                    tuple(rng.randrange(1, t) for _ in range(d * (d - 1))))
        def sample():
            for _ in range(512):
                a, b = one(), one()
                if a != b:
                    yield a, b
                if a[0] != b[0]:
                    yield a, (b[0], a[1])
        pairs = sample()
    witnesses = Counter(check_pair(base, a, b, d, t) for a, b in pairs)
    if exhaustive:
        assert sum(witnesses.values()) == size * (size - 1) // 2
    return dict(d=d, t=t, states=size, exhaustive=exhaustive, witnesses=witnesses)


def check_positive_coarsening(d, t):
    q, h = 2**t, 2 * d - 1
    zero = tuple((0,) * h for _ in range(h))
    leaf = (t,) * (d * (d - 1))
    destinations = [target(zero, (offset, leaf), d, t) for offset in product(range(1, q), repeat=d)]
    assert all(gram(zero, w, d, False, True, 3) == IDENTITY for w in destinations)
    checked = 0
    for v, w in combinations(destinations, 2):
        assert gram(v, w, d, True, True, 3) == IDENTITY
        checked += 1
    return dict(d=d, t=t, merged_cells=len(destinations), compatible_pairs=checked)


def dyadic_boxes(t):
    for depth in range(1, t + 1):
        size = 2**(t - depth)
        for left in range(0, 2**t, 2 * size):
            a = tuple(range(left, left + size))
            b = tuple(range(left + size, left + 2 * size))
            yield depth, a, b
            yield depth, b, a


def check_partition(d, t):
    q = 2**t
    a_d = sum(2**(t - b) * (b**d - (b - 1)**d) for b in range(1, t + 1))
    counts_src, counts_dst = Counter(), Counter()
    witnessed, groups, edges = 0, 0, set()
    for box in product(dyadic_boxes(t), repeat=d):
        depths, ls, ks = zip(*box)
        pin = depths.index(max(depths))
        c = len(ls[pin])
        for sides in (ls, ks):
            clique = [tuple(axis[i] for axis in sides) for i in range(c)]
            assert all(all(a != b for a, b in zip(u, v)) for u, v in combinations(clique, 2))
            witnessed += 1
        for x, y in product(ls[pin], ks[pin]):
            l_axes, k_axes = list(ls), list(ks)
            l_axes[pin], k_axes[pin] = (x,), (y,)
            src, dst = list(product(*l_axes)), list(product(*k_axes))
            counts_src.update(src)
            counts_dst.update(dst)
            for side in (src, dst):
                assert all(v[pin] == side[0][pin] for v in side)
            for u, v in product(src, dst):
                assert all(a != b for a, b in zip(u, v)) and (u, v) not in edges
                edges.add((u, v))
            groups += 1
    assert len(edges) == (q * (q - 1))**d
    for counter in (counts_src, counts_dst):
        assert len(counter) == q**d and set(counter.values()) == {a_d}
    return dict(d=d, t=t, rectangles=groups, edges=len(edges), side_cliques=witnessed,
                narrowest_load=a_d, original_load=(q - 1) * t**(d - 1))


def check_comparisons():
    cases = 0
    for d in (2, 4, 8, 16, 32, 64):
        for t in range(2, 6 * d + 1):
            a = sum(2**(t - b) * (b**d - (b - 1)**d) for b in range(1, t + 1))
            assert max(2**(t - 1), t**d) <= a <= (2**t - 1) * t**(d - 1)
            assert a <= 2**(t + d) * prod(range(1, d + 1))
            if d == 2:
                assert a == 3 * 2**t - 2 * t - 3
            cases += 1
    return cases


def correlated_outer_cliques():
    # A box-confined side must avoid any far inner pair in any outer position.
    cases = comparisons = 0
    for d in (2, 4):
        for sizes in product(range(1, 4), repeat=d):
            local = [[tuple((j + 7*i) for i in range(d)) for j in range(c)] for c in sizes]
            clique = list(product(*local))
            assert len(clique) == prod(sizes)
            for x, y in combinations(clique, 2):
                assert any(all(a != b for a, b in zip(u, v)) for u, v in zip(x, y))
                comparisons += 1
            cases += 1
    return dict(boxes=cases, incompatible_product_pairs=comparisons)


def selected_arities():
    comparisons = []
    for d in (4, 8, 16, 32, 64):
        t = 8 * d * (d.bit_length() - 1)
        exponent = d**2 * (t - 2)  # m = 2**exponent + 1
        u0 = exponent + 1
        v0 = (u0 + 1).bit_length()
        assert d**3 * v0 <= u0 < (2 * d)**3 * v0
        # The real rank guard has RHS log2(m)+2d^2-2, strictly between
        # the following integer and its successor.
        lower = exponent + 2 * d**2 - 2
        assert (t - 1) * d**2 <= lower < t * d**2
        factor = sum(2**(t - b) * (b**d - (b - 1)**d) for b in range(1, t + 1))
        old = (2**t - 1) * t**(d - 1)
        cross = (2**t - 1) * t**(d - 2)
        comparisons.append(dict(
            d=d, t=t, m_minus_one_power=exponent,
            log2_old_new_floor=((old**d) // (factor**d)).bit_length() - 1,
            log2_cross_pinned_new_floor=((cross**d) // (factor**d)).bit_length() - 1))
    return comparisons


if __name__ == '__main__':
    print(json.dumps(dict(
        families=[check_family(2, 2), check_family(2, 3), check_family(4, 2),
                  check_family(4, 3, False), check_family(4, 6, False)],
        positive_controls=[check_positive_coarsening(2, 2), check_positive_coarsening(2, 3)],
        partitions=[check_partition(d, t) for d, t in ((2, 1), (2, 2), (2, 3), (2, 4),
                                                       (3, 2), (3, 3), (4, 1), (4, 2))],
        elementary_comparisons=check_comparisons(), selected_arities=selected_arities(),
        correlated_outer_cliques=correlated_outer_cliques()),
                     indent=2, sort_keys=True))
