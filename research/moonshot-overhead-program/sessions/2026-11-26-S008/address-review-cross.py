#!/usr/bin/env python3
"""Independent finite checks of the two-cut and box-confined cross-anchor statements."""
from itertools import combinations, product
from math import comb


def dot(x, y):
    return (x[0]*y[0]+x[1]*y[1]+x[2]*y[3]+x[3]*y[2]) % 3


def add(x, y):
    return tuple((a+b) % 3 for a, b in zip(x, y))


def mult(c, x):
    return tuple(c*a % 3 for a in x)


def triples(points):
    """Unordered partitions of the nine reserve elements into unordered triples."""
    if not points:
        yield ()
        return
    head = points[0]
    for i, j in combinations(points[1:], 2):
        remaining = tuple(t for t in points if t not in (head, i, j))
        for rest in triples(remaining):
            yield ((head, i, j),) + rest


def prefix_flags():
    ambient = tuple(product(range(3), repeat=4))
    indices = {z:i for i, z in enumerate(ambient)}
    pairs = [((1, 0, 0, 0), (0, 1, 0, 0)), ((1, 0, 1, 0), (0, 1, 0, 0)),
             ((1, 0, 0, 1), (0, 1, 0, 0))]
    all_flags = []
    nonlinear = []
    identity = (1, 0, 0, 1)
    gram = lambda p, q: tuple(dot(x,y) for x in p for y in q)
    assert all(gram(pairs[0], p) == identity for p in pairs)
    assert gram(pairs[1], pairs[2]) != identity
    for p, q in pairs:
        reserve = tuple(x for x in ambient if dot(x, p) == dot(x, q) == 0)
        mains = tuple(add(mult(i,p), mult(j,q)) for i, j in product(range(3), repeat=2))
        flags = set()
        affine = 0
        for partition in triples(reserve):
            fine, coarse = [], []
            if all(add(add(x, y), z) == (0, 0, 0, 0) for x, y, z in partition):
                affine += 1
            for block in partition:
                merged = 0
                for main in mains:
                    mask = sum(1 << indices[add(y, main)] for y in block)
                    assert mask.bit_count() == 3 and not (merged & mask)
                    fine.append(mask)
                    merged |= mask
                coarse.append(merged)
            flags.add((tuple(sorted(coarse)), tuple(sorted(fine))))
        assert len(flags) == 280 and affine == 4
        all_flags.append(flags)
        nonlinear.append(len(flags)-affine)
    ab, ac = all_flags[0] & all_flags[1], all_flags[0] & all_flags[2]
    assert len(ab) == len(ac) == 1 and not (ab & ac)
    return len(all_flags[0]), nonlinear[0], len(ab), len(ac), len(ab & ac)


def arbitrary_correlations():
    words = list(product(range(2), repeat=2))
    labels = list(product(words, words))
    def bad(left, right):
        return any(all(a != b for a, b in zip(x, y)) for x, y in zip(left, right))
    conflicts = [sum(1 << j for j, y in enumerate(labels) if bad(x, y)) for x in labels]
    diagonals = {(0, 0), (1, 1)}
    clique = sum(1 << i for i, x in enumerate(labels) if all(y in diagonals for y in x))
    assert clique.bit_count() == 4
    legal = [False] * (1 << len(labels))
    legal[0] = True
    nonempty, correlated, largest = 0, 0, 0
    for mask in range(1, len(legal)):
        first = (mask & -mask).bit_length()-1
        rest = mask ^ (1 << first)
        legal[mask] = legal[rest] and not (conflicts[first] & rest)
        if not legal[mask]:
            continue
        nonempty += 1
        assert (mask & clique).bit_count() <= 1
        side = [x for i, x in enumerate(labels) if mask & (1 << i)]
        p, q = ({x[i] for x in side} for i in range(2))
        for segment in (p,q):
            assert all(not all(a != b for a,b in zip(x,y)) for x,y in combinations(segment,2))
        if len(side) < len(p)*len(q):
            correlated += 1
        largest = max(largest, len(side))
    assert correlated > 0 and largest == 4
    return len(legal), nonempty, correlated, clique.bit_count()


def ordered_bells(d):
    numbers = [1]
    for n in range(1, d+1):
        numbers.append(sum(comb(n, j) * numbers[n-j] for j in range(1, n+1)))
    return numbers


def depth_sum(d, t):
    # Independent shifted-tail identity, using only d terms instead of t depth levels.
    f = ordered_bells(d)
    tail = sum(comb(d,j)*t**(d-j)*f[j] for j in range(1,d+1))
    return (f[d] << t) - tail


def floor_log_ratio(top, bottom):
    exponent = top.bit_length()-bottom.bit_length()
    assert exponent >= 0
    return exponent-1 if top < bottom << exponent else exponent


def arities():
    for d in range(1,11):
        for t in range(1,65):
            direct = sum((b**d-(b-1)**d) << (t-b) for b in range(1,t+1))
            assert depth_sum(d,t) == direct
    rows = []
    for d in [4, 8, 16, 32, 64]:
        t = 8*d*(d.bit_length()-1)
        exponent = d*d*(t-2)
        u0 = exponent+1
        v = (u0+1).bit_length()
        assert d**3*v <= u0 < (2*d)**3*v
        assert (t-1)*d*d <= exponent+2*d*d-2 < t*d*d
        new = depth_sum(d,t)
        old = ((1 << t)-1)*t**(d-1)
        alternate = old//t
        rows.append((d, t, exponent, floor_log_ratio(old**d,new**d),
                     floor_log_ratio(alternate**d,new**d), exponent >= 2**17))
    assert rows[0][3:] == (47,23,False)
    assert rows[3][3:] == (5947,5617,True)
    return rows


if __name__ == '__main__':
    print('flags per endpoint, nonlinear flags, two pair intersections, triple intersection:', prefix_flags())
    print('arbitrary sides checked, nonempty legal sides, non-product legal sides, clique size:',
          arbitrary_correlations())
    print('d, t, log2(m−1), floor log2(old/new), floor log2(cross/new), active nonbase arity:')
    for row in arities():
        print(row)
