#!/usr/bin/env python3
"""Independent exact combinatorial/coefficient audit; no author imports.

Default is read-only. --write explicitly saves the deterministic receipt.
Finite checks corroborate the separate universal proof review.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path
import random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def graph(order, mask):
    """Build both matchings directly from labels, keeping parallel edges."""
    n = len(order)
    require(n >= 2 and n & (n - 1) == 0, "power-of-two domain")
    require(sorted(order) == list(range(n)), "complete ordering")
    require(0 < mask < n, "nonzero translation mask")
    pos = {x: i for i, x in enumerate(order)}
    plus = [(i, pos[x ^ mask]) for i, x in enumerate(order) if i < pos[x ^ mask]]
    minus = [(i + 1, j + 1) for i, j in plus if j < n - 1]
    adjacency, matrix = [[] for _ in order], [[0] * n for _ in order]
    for i, j, sign in [(i, j, 1) for i, j in plus] + [(i, j, -1) for i, j in minus]:
        adjacency[i].append((j, sign)); adjacency[j].append((i, sign))
        matrix[i][j] += sign; matrix[j][i] += sign
    unseen, components = set(range(n)), []
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            i = stack.pop()
            if i in component:
                continue
            component.add(i)
            stack.extend(j for j, _ in adjacency[i] if j not in component)
        unseen -= component; components.append(sorted(component))
    cycles, paths, keep = [], [], []
    for comp in components:
        require(all(len(adjacency[i]) in (1, 2) for i in comp), "degrees")
        ends = [i for i in comp if len(adjacency[i]) == 1]
        require(len(comp) % 2 == 0, "even component")
        if ends:
            require(len(ends) == 2, "path endpoints")
            paths.append(comp); keep.extend(comp)
        else:
            cycles.append(comp)
            a = min(comp); b = min(j for j, _ in adjacency[a])
            keep.extend(i for i in comp if i not in (a, b))
    require(len(paths) == 1, "unique open component")
    for i in range(n):
        signs = [s for _, s in adjacency[i]]
        require(signs.count(1) == 1 and signs.count(-1) <= 1, "alternating colors")
    keep.sort()
    for i in keep:
        require(sum(j in keep for j, _ in adjacency[i]) in (1, 2), "retained paths")
    return dict(matrix=matrix, cycles=cycles, keep=keep, rank=len(keep),
                m=sum(j == i + 1 for i, j in plus), L=sum(len(c) == 2 for c in cycles))


def determinant(matrix):
    """Exact elimination, independent of the graph determinant formula."""
    a = [[Fraction(x) for x in row] for row in matrix]; answer = Fraction(1)
    for c in range(len(a)):
        pivot = next((i for i in range(c, len(a)) if a[i][c]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]; answer = -answer
        v = a[c][c]; answer *= v
        for i in range(c + 1, len(a)):
            f = a[i][c] / v
            for j in range(c + 1, len(a)):
                a[i][j] -= f * a[c][j]
            a[i][c] = 0
    return answer


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]; row = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]; v = a[row][c]
        for i in range(row + 1, len(a)):
            f = a[i][c] / v
            for j in range(c, len(a[0])):
                a[i][j] -= f * a[row][j]
        row += 1
        if row == len(a):
            break
    return row


def principal(matrix, keep):
    return [[matrix[i][j] for j in keep] for i in keep]


def exponent(mask, d):
    return tuple((mask >> k) & 1 for k in range(d))


def polynomial_minor(order, keep):
    """Full multivariate determinant via subset DP; no coefficient oracle."""
    d, r = (len(order) - 1).bit_length(), len(keep); zero = (0,) * d
    entries = []
    for i in keep:
        row = []
        for j in keep:
            entry = Counter({exponent(order[i] ^ order[j], d): 1})
            if i and j:
                entry[exponent(order[i - 1] ^ order[j - 1], d)] -= 1
            row.append({e: c for e, c in entry.items() if c})
        entries.append(row)
    dp = {0: {zero: 1}}
    for i in range(r):
        nxt = {}
        for used, poly in dp.items():
            for j in range(r):
                if used >> j & 1:
                    continue
                sign = -1 if (used >> (j + 1)).bit_count() % 2 else 1
                out = nxt.setdefault(used | (1 << j), {})
                for e, c in poly.items():
                    for f, b in entries[i][j].items():
                        key = tuple(x + y for x, y in zip(e, f))
                        out[key] = out.get(key, 0) + sign * c * b
        dp = {used: {e: c for e, c in p.items() if c} for used, p in nxt.items()}
    return dp[(1 << r) - 1]


def evaluate(poly, q):
    total = Fraction(0)
    for powers, coefficient in poly.items():
        term = Fraction(coefficient)
        for x, p in zip(q, powers):
            term *= x ** p
        total += term
    return total


def multiply_polys(left, right):
    out = Counter()
    for e, a in left.items():
        for f, b in right.items():
            out[tuple(x + y for x, y in zip(e, f))] += a * b
    return {e: a for e, a in out.items() if a}


def numerical_stein(order, q):
    def entry(i, j):
        v = Fraction(1)
        for k, x in enumerate(q):
            if (order[i] ^ order[j]) >> k & 1:
                v *= x
        return v
    return [[entry(i, j) - (entry(i - 1, j - 1) if i and j else 0)
             for j in range(len(order))] for i in range(len(order))]


def check_order(order, dense=False):
    n = len(order); directions = Counter(order[i] ^ order[i - 1] for i in range(1, n))
    m = max(directions.values()); cases = [graph(order, v) for v in range(1, n)]
    require(sum(g['m'] for g in cases) == n - 1, "direction sum")
    require(all(g['m'] == directions[v] for v, g in enumerate(cases, 1)), "direction indexing")
    require(sum(g['L'] for g in cases) == sum(x * (x - 1) // 2 for x in directions.values()),
            "parallel-pair double count")
    for g in cases:
        c = len(g['cycles'])
        require(c <= n // 2 - g['m'], "nonadjacent-edge injection")
        require(4 * c <= n - 2 + 2 * g['L'], "cycle packing")
        require(g['rank'] == n - 2 * c, "certificate size")
        if dense:
            require(rank(g['matrix']) == g['rank'], "signed graph rank")
            require(abs(determinant(principal(g['matrix'], g['keep']))) == 1, "unimodular minor")
    best = max(g['rank'] for g in cases)
    require(best >= 2 * m and 2 * best >= n - m + 3, "complementary bounds")
    require(best >= 2 * ((n + 7) // 5), "even-rounded lower bound")
    return cases


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    receipt = dict(status='PASS_INDEPENDENT_ARBITRARY_ORDER_REVIEW',
                   method='Independent multigraph components, Fraction elimination and multivariate subset-DP; no author imports.',
                   scope='Finite corroboration of the universal proof review; no fine-prime or rounded-source admission.')
    rows = []
    for n in (2, 4, 8):
        count, minimum = 0, n
        for tail in permutations(range(1, n)):
            cases = check_order((0,) + tail, dense=n <= 4)
            minimum = min(minimum, max(g['rank'] for g in cases)); count += 1
        rows.append(dict(N=n, normalized_orders=count, translation_graphs=count * (n - 1),
                         minimum_best_certificate=minimum))
    receipt['exhaustive_combinatorics'] = rows
    rng, rows = random.Random(91377), []
    for n in (16, 32, 64):
        minimum = n
        for _ in range(8):
            order = list(range(n)); rng.shuffle(order)
            cases = check_order(tuple(order))
            minimum = min(minimum, max(g['rank'] for g in cases))
        rows.append(dict(N=n, orders=8, translation_graphs=8 * (n - 1), minimum_best_certificate=minimum))
    receipt['larger_combinatorics'] = dict(seed=91377, cases=rows)
    symbolic_cases, terms = 0, 0
    fixtures = [((0,) + tail, mask) for tail in permutations(range(1, 4)) for mask in range(1, 4)]
    fixtures += [(order, mask) for order in ((0, 1, 3, 2, 6, 7, 5, 4),
                                            (0, 1, 2, 3, 7, 5, 6, 4)) for mask in (3, 5)]
    for order, mask in fixtures:
        g = graph(order, mask); d = (len(order) - 1).bit_length()
        poly = polynomial_minor(order, g['keep'])
        target = tuple(g['rank'] * b for b in exponent(mask, d))
        expected = determinant(principal(g['matrix'], g['keep']))
        require(poly.get(target, 0) == expected and abs(expected) == 1, 'isolated coefficient')
        require(poly[target] % 2 == 1, 'coefficient survives characteristic two')
        q = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 5))[:d]
        require(evaluate(poly, q) == determinant(principal(numerical_stein(order, q), g['keep'])),
                'independent polynomial evaluation')
        symbolic_cases += 1; terms += len(poly)
    receipt['exact_symbolic_minors'] = dict(cases=symbolic_cases, nonzero_terms_total=terms,
                                           isolated_coefficients='all +1 or -1; all odd modulo 2')
    exceptional = (0, 1, 2, 3, 7, 5, 6, 4)
    full_poly = polynomial_minor(exceptional, tuple(range(8)))
    factors = []
    for k in range(3):
        power = tuple(2 if i == k else 0 for i in range(3))
        factors.append({(0, 0, 0): 1, power: -1})
    factors.extend([{(1, 1, 0): 1, (1, 0, 1): sign, (0, 1, 1): sign} for sign in (-1, 1)])
    factored = {(0, 0, 0): 1}
    for f in factors:
        factored = multiply_polys(factored, multiply_polys(f, f))
    require(full_poly == factored, 'full exceptional determinant factorization')
    receipt['exceptional_determinant_factorization'] = dict(
        dimension=8, nonzero_terms=len(full_poly),
        exact_identity='prod_i(1-q_i^2)^2 * (ab-ac-bc)^2 * (ab+ac+bc)^2',
        method='full subset-DP determinant equals separately multiplied polynomial dictionaries')
    for order in ((0, 1, 3, 2, 6, 7, 5, 4), (0, 1, 2, 3, 7, 5, 6, 4)):
        check_order(order, dense=True)
    receipt['independent_dense_graph_rank_checks'] = 1 + 6 * 3 + 2 * 7
    controls = []
    try:
        graph((0, 1, 2, 3), 0)
    except RuntimeError:
        controls.append('zero translation mask rejected')
    else:
        raise RuntimeError('zero-mask control missed')
    g = graph((0, 1, 2, 3), 2)
    require(g['rank'] == 2 and len(g['cycles']) == 1, 'parallel fixture')
    p = [[int(i ^ j == 2) for j in range(4)] for i in range(4)]
    cyclic = [[p[i][j] - p[(i - 1) % 4][(j - 1) % 4] for j in range(4)] for i in range(4)]
    require(rank(cyclic) == 0, 'cyclic-shift control')
    controls.append('cyclic replacement loses the open-path boundary and rank certificate')
    bad = sorted(set(range(4)) - {min(g['cycles'][0])})
    require(determinant(principal(g['matrix'], bad)) == 0, 'one-deletion control')
    controls.append('removing only one cycle vertex makes the principal minor singular')
    gray, q = (0, 1, 3, 2), (Fraction(1, 2), Fraction(1, 2))
    require(rank(numerical_stein(gray, q)) == 2, 'equal positive tuple control')
    require(evaluate(polynomial_minor(gray, tuple(range(4))), q) == 0, 'variable-identification control')
    controls.append('equal positive parameters make Gray-order rank 2, below generic bound 4')
    order, q = (0, 1, 2, 3, 7, 5, 6, 4), (Fraction(1, 2), Fraction(1, 3), Fraction(1, 5))
    require(rank(numerical_stein(order, q)) == 6, 'distinct tuple is not full rank')
    controls.append('distinct positive parameters can have rank 6 instead of full rank 8')
    require(rank(numerical_stein(gray, (0, 0))) == 1, 'zero boundary')
    controls.append('zero parameter boundary lies outside the generic positive-domain claim')
    require(all((x * x + x) % 2 == 0 for x in (0, 1)), 'finite-field point control')
    controls.append('nonzero x^2+x vanishes at every F2 point; formal genericity is not finite-field existence')
    require(len(controls) == 7, 'control count'); receipt['controls'] = controls
    text = json.dumps(receipt, indent=2, sort_keys=True) + '\n'
    if args.write:
        args.write.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
