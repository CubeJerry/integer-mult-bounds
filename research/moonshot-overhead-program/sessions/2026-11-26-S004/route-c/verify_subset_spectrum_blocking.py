#!/usr/bin/env python3
"""Exact subset-spectrum blocking, including characteristic-two F16."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib, json, random

from verify_inverse_query_commutator import Field, eye, inverse, multiply, rank
from verify_phase_block_rank import phase, boundary, block_part, complete_blocks, difference


class F16:
    order = 16

    @staticmethod
    def add(a, b):
        return a ^ b

    @staticmethod
    def sub(a, b):
        return a ^ b

    @staticmethod
    def neg(a):
        return a

    @staticmethod
    def mul(a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & 16:
                a ^= 19
        return out

    def power(self, a, n):
        out = 1
        while n:
            if n & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            n >>= 1
        return out

    def inv(self, a):
        assert a
        return self.power(a, 14)


def kron(a, b, f):
    return [[f.mul(x, y) for x in ra for y in rb] for ra in a for rb in b]


def tensor_power(a, n, f):
    out = [[1]]
    for _ in range(n):
        out = kron(out, a, f)
    return out


def sum_matrices(terms, f):
    out = [[0]*len(terms[0][0]) for _ in terms[0]]
    for term in terms:
        out = [[f.add(x, y) for x, y in zip(ra, rb)] for ra, rb in zip(out, term)]
    return out


def local_basis(exponents, block_size, r, zeta, chosen, f):
    words = list(product(exponents, repeat=block_size))
    by_product = {sum(w) % r: w for w in chosen}
    assert len(chosen) == r and len(by_product) == r
    assert all(w in words for w in chosen)
    selected = [by_product[h] for h in range(r)]
    singletons = [w for w in words if w not in selected]
    assert len(singletons) + r == len(words)
    n, ix = len(words), {w: i for i, w in enumerate(words)}
    u = [[0]*n for _ in range(n)]
    ui = [[0]*n for _ in range(n)]
    characteristic_r = 0
    for _ in range(r):
        characteristic_r = f.add(characteristic_r, 1)
    r_inverse = f.inv(characteristic_r)
    for h, word in enumerate(selected):
        for j in range(r):
            u[ix[word]][j] = f.power(zeta, h*j % r)
            ui[j][ix[word]] = f.mul(r_inverse, f.power(zeta, -h*j % r))
    for j, word in enumerate(singletons, r):
        u[ix[word]][j] = ui[j][ix[word]] = 1
    assert multiply(ui, u, f) == eye(n, f)
    return words, u, ui, singletons


def diagonal_conjugate(values, u, ui, f):
    return multiply(ui, [[f.mul(v, x) for x in row] for v, row in zip(values, u)], f)


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for j in range(total+1):
        for tail in compositions(total-j, parts-1):
            yield (j,)+tail


def boundary_fraction(k, r, d):
    if k == 0 or d == 0:
        return Fraction(0)
    total = 0
    for c in compositions(k, r):
        top = sorted(c, reverse=True)
        if top[0]-top[1] <= 2*d:
            count = factorial(k)
            for v in c:
                count //= factorial(v)
            total += count
    return Fraction(total, r**k)


def poisson_binomial(thetas):
    out = [Fraction(1)]
    for theta in thetas:
        nxt = [Fraction(0)]*(len(out)+1)
        for k, p in enumerate(out):
            nxt[k] += p*(1-theta)
            nxt[k+1] += p*theta
        out = nxt
    return out


def main():
    counts, rng = Counter(), random.Random(2026112601)
    f16 = F16()
    for a, b, c in product(range(16), repeat=3):
        assert f16.mul(a, f16.add(b, c)) == f16.add(f16.mul(a, b), f16.mul(a, c))
        counts['f16_distributivity'] += 1
    for a in range(1, 16):
        assert f16.mul(a, f16.inv(a)) == 1
    assert [f16.power(8, j) for j in range(5)] == [1, 8, 12, 10, 15]

    cases = [
        (3, Field(4), 2, (1, 2), 2, [(1, 1), (1, 2), (2, 2)], 3),
        (5, f16, 8, (0, 1, 4), 2, [(4, 4), (4, 0), (0, 0), (0, 1), (1, 1)], 2),
        (5, f16, 8, (1, 4), 4, [tuple([1]*j+[4]*(4-j)) for j in range(5)], 1),
    ]
    profiles = []
    for r, f, zeta, exponents, ell, chosen, groups in cases:
        words, u, ui, singletons = local_basis(exponents, ell, r, zeta, chosen, f)
        n = len(words)
        target_local = diagonal_conjugate([f.power(zeta, sum(w) % r) for w in words], u, ui, f)
        for j in range(r):
            assert [target_local[i][j] for i in range(n)] == [int(i == (j+1) % r) for i in range(n)]
            counts['local_regular_cycle_columns'] += 1
        for coordinate in range(ell):
            for power in range(1, r):
                query = diagonal_conjugate([f.power(zeta, power*w[coordinate] % r) for w in words], u, ui, f)
                for i, row in enumerate(query):
                    for j, val in enumerate(row):
                        if (i < r) != (j < r) or (i >= r and j >= r and i != j):
                            assert not val
                        if i < r and j < r:
                            assert val == query[(i-j) % r][0]
                        counts['local_query_invariant_entries'] += 1
        full_words = list(product(words, repeat=groups))
        full_indices = list(product(range(n), repeat=groups))
        ug, uig = tensor_power(u, groups, f), tensor_power(ui, groups, f)
        total = n**groups
        phases, bad_columns = [], []
        for indices in full_indices:
            alpha = tuple(i for i in indices if i < r)
            phases.append(phase(alpha, r) if alpha else r)
            bad_columns.append(bool(alpha) and boundary(alpha, r, 1))
        exceptional = len(singletons)**groups
        phase_counts = Counter(phases)
        assert all(phase_counts[j] == (total-exceptional)//r for j in range(r))
        assert phase_counts[r] == exceptional
        counts['dimension_weighted_sector_counts'] += 1
        values = [f.power(zeta, sum(sum(w) for w in point) % r) for point in full_words]
        target = diagonal_conjugate(values, ug, uig, f)
        for i, row in enumerate(target):
            for j, value in enumerate(row):
                if value:
                    assert phases[i] == (phases[j]+1) % r if phases[j] < r else phases[i] == r
                    counts['global_target_sector_transitions'] += 1
        scalar_queries = []
        for coordinate in range(ell*groups):
            block, inside = divmod(coordinate, ell)
            scalar_queries.append(diagonal_conjugate(
                [f.power(zeta, point[block][inside] % r) for point in full_words], ug, uig, f))
        w = 2
        phases2 = [p for p in phases for _ in range(w)]
        ident = eye(total, f)
        e00, e01, e11 = [[1, 0], [0, 0]], [[0, 1], [0, 0]], [[0, 0], [0, 1]]
        g = sum_matrices([kron(scalar_queries[0], e00, f), kron(scalar_queries[-1], e11, f),
                          kron(ident, e01, f), kron(scalar_queries[1], e01, f)], f)
        gi = inverse(g, f)
        assert gi is not None
        gz = block_part(g, phases2)
        delta = rank(difference(g, gz, f), f)
        boundary_size = sum(bad_columns)
        assert delta <= w*boundary_size
        completed = complete_blocks(gz, phases2, r+1, f)
        completed_inverse = inverse(completed, f)
        assert rank(difference(gi, completed_inverse, f), f) <= 2*delta
        counts['actual_subset_inverse_completions'] += 1
        target2 = kron(target, eye(w, f), f)
        assert rank(difference(target2, gz, f), f)*r >= (r-1)*(total-exceptional)*w
        numerator = sum_matrices([kron(q, [[rng.randrange(f.order) for _ in range(w)] for _ in range(w)], f)
                                 for q in [ident]+scalar_queries], f)
        assert multiply(numerator, g, f) != multiply(g, numerator, f)
        numerator_zero = block_part(numerator, phases2)
        da = rank(difference(numerator, numerator_zero, f), f)
        assert da <= w*boundary_size
        for left in (False, True):
            prediction = multiply(gi, numerator, f) if left else multiply(numerator, gi, f)
            comparison = multiply(completed_inverse, numerator_zero, f) if left else multiply(numerator_zero, completed_inverse, f)
            assert comparison == block_part(comparison, phases2)
            assert rank(difference(prediction, comparison, f), f) <= da+2*delta
            assert (rank(difference(target2, prediction, f), f)+da+2*delta)*r >= (r-1)*(total-exceptional)*w
            counts['noncommuting_actual_subset_fraction_bounds'] += 1
        # A genuine rank-one port couples the exceptional and regular strata.
        good = next(i for i, p in enumerate(phases2) if p == 0)
        bad = next(i for i, p in enumerate(phases2) if p == r)
        port = eye(total*w, f)
        port[good][bad] = f.add(port[good][bad], 1)
        actual = multiply(gi, multiply(port, g, f), f)
        comparison = multiply(completed_inverse, gz, f)
        assert rank(difference(actual, comparison, f), f) <= 3*delta+1
        assert (rank(difference(target2, actual, f), f)+3*delta+1)*r >= (r-1)*(total-exceptional)*w
        counts['ports_mixing_actual_strata'] += 1
        theta = Fraction(r, n)
        mixture = poisson_binomial([theta]*groups)
        eta = sum(p*boundary_fraction(k, r, 1) for k, p in enumerate(mixture))
        assert eta == Fraction(boundary_size, total)
        profiles.append({'r':r, 'old_coordinates':ell*groups, 'physical_dimension':total,
                         'regular_fraction_per_group':str(theta), 'exceptional_dimension':exceptional,
                         'exact_boundary_fraction':str(eta), 'actual_query_offblock_rank':delta})
        counts['actual_dimension_mixture_identities'] += 1

    # Multiplicity counts, with distinct nontrivial eigenspaces retained.
    for qs in product((2, 4, 8, 16), repeat=4):
        distribution = Counter({0:1})
        retained = 1
        total = 1
        for q in qs:
            local = {0:q, 1:q*(q-1)//2, 4:q*(q-1)//2}
            nxt = Counter()
            for a, ca in distribution.items():
                for b, cb in local.items():
                    nxt[(a+b) % 5] += ca*cb
            distribution = nxt
            retained *= q*(q-1)//2
            total *= q*q
        assert sum(distribution.values()) == total
        assert all(distribution[a] >= retained for a in range(5))
        theta = Fraction(5*retained, total)
        assert theta >= Fraction(5, 256)
        assert theta == 5*__import__('functools').reduce(lambda a,b:a*b, (Fraction(q-1,2*q) for q in qs), Fraction(1))
        counts['unequal_physical_multiplicity_blocks'] += 1

    for r, theta in ((3,Fraction(3,4)), (5,Fraction(5,9)), (5,Fraction(5,16)), (5,Fraction(5,256))):
        for groups in range(1,17):
            thetas = [theta if j % 2 else (theta+1)/2 for j in range(groups)]
            distribution = poisson_binomial(thetas)
            mu = sum(thetas)
            assert sum(distribution) == 1
            assert sum(k*p for k,p in enumerate(distribution)) == mu
            pi0 = __import__('functools').reduce(lambda a,b:a*b,(1-t for t in thetas),Fraction(1))
            assert distribution[0] == pi0
            assert sum(p for k,p in enumerate(distribution) if 2*k < mu) <= 4/mu
            for d in (0,1,2):
                eta = sum(p*boundary_fraction(k,r,d) for k,p in enumerate(distribution))
                assert 0 <= eta <= 1
                if d == 0:
                    assert eta == 0
                counts['poisson_binomial_boundary_profiles'] += 1

    # Five arbitrary vectors are not necessarily a cyclic regular piece.
    repeated_products = [w for w in product((1,4), repeat=4) if sum(w)%5 == 0][:5]
    assert len(repeated_products) == 5 and len({sum(w)%5 for w in repeated_products}) == 1
    assert rank([[0]*5 for _ in range(5)], f16) == 0  # T-I on this invalid proposed piece.
    q = 128
    pq = Fraction(q-1, 2*q)
    two_group_min = min(pq*pq, 2*Fraction(1,q)*pq)
    assert 5*two_group_min < Fraction(5,9)
    result = {'status':'passed', 'seed':2026112601,
              'arithmetic':'exact F4, F16 and rational/integer multiplicities',
              'counts':dict(counts), 'profiles':profiles,
              'negative_controls':['five selected points with repeated target roots are not regular',
                                   'uniform three-value weights cannot replace physical fixed-point multiplicities'],
              'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope':'Subset-to-regular blocking and actual-dimension rank controls; no physical transform-cost claim'}
    Path('subset-spectrum-blocking-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
