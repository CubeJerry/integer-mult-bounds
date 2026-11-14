#!/usr/bin/env python3
"""Exact finite corroboration; transcendence is a cited theorem, not an oracle.
Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
SPDX-License-Identifier: Apache-2.0
"""
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from math import gcd, prod, isqrt
from pathlib import Path
import json
import random


class CheckFailure(RuntimeError):
    pass


def require(value, message):
    if not value:
        raise CheckFailure(message)


def stein(a):
    return [[a[i][j] - (a[i - 1][j - 1] if i and j else 0)
             for j in range(len(a))] for i in range(len(a))]


def minor(a, keep):
    return [[a[i][j] for j in keep] for i in keep]


def determinant(a):
    """Exact fraction-free determinant, independent of the path formula."""
    if not a:
        return 1
    b = [row[:] for row in a]
    sign, old = 1, 1
    for k in range(len(b) - 1):
        pivot = next((i for i in range(k, len(b)) if b[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            b[k], b[pivot] = b[pivot], b[k]
            sign = -sign
        new = b[k][k]
        for i in range(k + 1, len(b)):
            for j in range(k + 1, len(b)):
                numerator = b[i][j] * new - b[i][k] * b[k][j]
                quotient = numerator / old if isinstance(numerator, Fraction) else numerator // old
                require(quotient * old == numerator, "exact Bareiss division")
                b[i][j] = quotient
            b[i][k] = 0
        old = new
    return sign * b[-1][-1]


def matching_paths(order, mask):
    n = len(order)
    require(n >= 2 and n & (n - 1) == 0 and sorted(order) == list(range(n)),
            "complete binary vertex order")
    require(0 < mask < n, "nonzero translation mask")
    pos = {x: i for i, x in enumerate(order)}
    mate = [pos[x ^ mask] for x in order]
    adjacency = [[] for _ in order]
    for i, j in enumerate(mate):
        if i < j:
            adjacency[i].append(j)
            adjacency[j].append(i)
            if j < n - 1:
                adjacency[i + 1].append(j + 1)
                adjacency[j + 1].append(i + 1)
    unseen, removed = set(range(n)), set()
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            x = stack.pop()
            if x not in component:
                component.add(x)
                stack.extend(adjacency[x])
        unseen -= component
        if all(len(adjacency[x]) == 2 for x in component):
            first = min(component)
            removed.update((first, mate[first]))
    remaining, paths = set(range(n)) - removed, []
    while remaining:
        start = min(x for x in remaining if sum(y in remaining for y in adjacency[x]) == 1)
        path, previous, current = [], None, start
        while current is not None:
            path.append(current)
            next_vertices = [y for y in adjacency[current] if y in remaining and y != previous]
            require(len(next_vertices) <= 1, "retained component is a path")
            previous, current = current, next_vertices[0] if next_vertices else None
        require(len(path) % 2 == 0, "even retained path")
        remaining -= set(path)
        paths.append(path)
    return paths


def trimmed_indices(paths, size):
    require(size >= 0 and size % 2 == 0, "even trimming size")
    require(size <= sum(map(len, paths)), "trimming capacity")
    keep = []
    left = size
    for path in paths:
        take = min(left, len(path))
        keep.extend(path[:take])
        left -= take
    require(left == 0, "exact requested trim")
    return sorted(keep)


def best_certificate(order):
    choices = [(sum(map(len, p)), v, p)
               for v in range(1, len(order)) for p in [matching_paths(order, v)]]
    return max(choices, key=lambda x: x[0])


def add_poly(a, b, sign=1):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, 0) + sign * value
        if not out[key]:
            del out[key]
    return out


def multiply_poly(a, b):
    out = {}
    for u, c in a.items():
        for v, d in b.items():
            key = tuple(x + y for x, y in zip(u, v))
            out[key] = out.get(key, 0) + c * d
    return {k: v for k, v in out.items() if v}


def gaussian_minor_polynomial(order, keep):
    """Literal determinant expansion, no graph-rank oracle."""
    dimension = len(order).bit_length() - 1
    def monomial(mask):
        return tuple(mask >> bit & 1 for bit in range(dimension))
    entries = []
    for i in keep:
        row = []
        for j in keep:
            value = {monomial(order[i] ^ order[j]): 1}
            if i and j:
                value = add_poly(value, {monomial(order[i - 1] ^ order[j - 1]): 1}, -1)
            row.append(value)
        entries.append(row)
    out = {}
    for p in permutations(range(len(keep))):
        parity = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
        term = {(0,) * dimension: (-1) ** parity}
        for i, j in enumerate(p):
            term = multiply_poly(term, entries[i][j])
            if not term:
                break
        out = add_poly(out, term)
    return out


def exponent_weights(denominators, targets):
    total = prod(denominators)
    return [u * (total // m) for m, u in zip(denominators, targets)]


def specialize(polynomial, denominators, targets):
    weights = exponent_weights(denominators, targets)
    out = {}
    for monomial, coefficient in polynomial.items():
        power = sum(a * b for a, b in zip(monomial, weights))
        out[power] = out.get(power, 0) + coefficient
    return {k: c for k, c in out.items() if c}


def crt_domain(denominators, targets):
    require(len(denominators) == len(targets) and denominators, "matching nonempty dimensions")
    require(all(isinstance(m, int) and not isinstance(m, bool) and m >= 2
                for m in denominators), "integer denominators at least two")
    require(all(isinstance(u, int) and not isinstance(u, bool) and u > 0
                for u in targets), "positive integer targets")
    require(all(gcd(m, n) == 1 for i, m in enumerate(denominators)
                for n in denominators[i + 1:]), "pairwise coprime denominators")
    require(all(gcd(m, u) == 1 for m, u in zip(denominators, targets)), "unit targets")


def exponent_boxes():
    families = [([3], [4]), ([3, 5], [8, 8]), ([3, 5, 7], [4, 8, 8]),
                ([5, 7, 11], [16, 16, 8]), ([7, 11, 13], [16, 8, 32]),
                ([3, 5, 7, 11], [8, 8, 16, 16]), ([9, 25, 49], [16, 32, 64])]
    result = []
    for denominators, targets in families:
        crt_domain(denominators, targets)
        weights = exponent_weights(denominators, targets)
        seen = {}
        for vector in product(*(range(m) for m in denominators)):
            power = sum(a * b for a, b in zip(vector, weights))
            require(power not in seen, "full guarded exponent-box injection")
            seen[power] = vector
        result.append({"denominators": denominators, "targets": targets,
                       "box_vectors": len(seen)})
    return result


def is_prime(n):
    return isinstance(n, int) and not isinstance(n, bool) and n >= 2 and all(
        n % k for k in range(2, isqrt(n) + 1))


def source_domain(primes, targets, alpha):
    require(all(is_prime(s) and s % 2 == 1 for s in primes), "odd source primes")
    require(len(set(primes)) == len(primes), "distinct source primes")
    require(all(isinstance(t, int) and not isinstance(t, bool) and t > 0 and
                t & (t - 1) == 0 for t in targets), "dyadic positive targets")
    require(isinstance(alpha, int) and not isinstance(alpha, bool) and alpha > 0,
            "common positive integer alpha")
    crt_domain(primes, targets)


def trimming_checks():
    orders = [list((0,) + tail) for d in (1, 2)
              for tail in permutations(range(1, 1 << d))]
    orders += [[0, 1, 2, 3, 7, 5, 6, 4], [0, 1, 2, 3, 4, 6, 5, 7],
               [0, 1, 3, 2, 6, 7, 5, 4]]
    rng = random.Random(20261114)
    for _ in range(32):
        order = list(range(8))
        rng.shuffle(order)
        orders.append(order)
    orders += [[11, 9, 3, 15, 1, 7, 2, 10, 13, 6, 4, 8, 12, 14, 5, 0],
               [0, 26, 11, 12, 2, 9, 19, 24, 25, 3, 14, 29, 31, 20, 10, 13,
                28, 23, 30, 15, 22, 27, 4, 17, 16, 21, 8, 1, 5, 7, 18, 6]]
    count = 0
    for order in orders:
        capacity, mask, paths = best_certificate(order)
        require(capacity >= 2 * ((len(order) + 7) // 5), "predecessor capacity")
        matrix = stein([[int(x ^ y == mask) for y in order] for x in order])
        for size in range(0, capacity + 1, 2):
            keep = trimmed_indices(paths, size)
            require(len(keep) == size, "trimmed principal size")
            require(abs(determinant(minor(matrix, keep))) == 1,
                    "every chosen even trimming has a unit minor")
            count += 1
    return {"orders": len(orders), "unit_minors": count, "seed": 20261114,
            "coverage": "all normalized d<=2, three fixed d3, 32 sampled d3, fixed d4/d5"}


def polynomial_checks():
    cases = [([0, 1], [3], [4], 3),
             ([0, 1, 2, 3], [3, 5], [8, 8], 3),
             ([0, 1, 3, 2], [5, 7], [8, 8], 5)]
    for order in ([0, 1, 2, 3, 7, 5, 6, 4], [0, 1, 2, 3, 4, 6, 5, 7],
                  [0, 1, 3, 2, 6, 7, 5, 4]):
        for primes in ([3, 5, 7], [5, 7, 11], [7, 11, 13]):
            cases.append((order, primes, [16, 16, 16], primes[0]))
    results = []
    for order, primes, targets, alpha in cases:
        source_domain(primes, targets, alpha)
        capacity, mask, paths = best_certificate(order)
        size = min(2 * ((len(order) + 7) // 5), min(primes) - 1)
        keep = trimmed_indices(paths, size)
        polynomial = gaussian_minor_polynomial(order, keep)
        key = tuple(size if mask >> bit & 1 else 0 for bit in range(len(primes)))
        require(abs(polynomial.get(key, 0)) == 1, "isolated unit coefficient")
        require(all(all(power < prime for power, prime in zip(monomial, primes))
                    for monomial in polynomial), "strict individual degree guard")
        specialized = specialize(polynomial, primes, targets)
        require(len(specialized) == len(polynomial) and specialized,
                "all nonzero monomials remain distinct after source substitution")
        weights = exponent_weights(primes, targets)
        for monomial, coefficient in polynomial.items():
            exponent = sum(x * y for x, y in zip(monomial, weights))
            require(specialized[exponent] == coefficient, "exact specialized coefficient")
        results.append({"order": order, "primes": primes, "targets": targets,
                        "alpha": alpha, "minor_size": size, "capacity": capacity,
                        "nonzero_terms": len(polynomial), "maximum_z_exponent": max(specialized)})
    return results


def source_exponent_checks():
    count = 0
    for prime, target in ((227, 256), (229, 256), (239, 256), (113, 128)):
        alpha = 3
        source_domain([prime], [target], alpha)
        rho = Fraction(target, prime)
        theta = rho - 1
        require(Fraction(7, 8) * target < prime <= Fraction(15, 16) * target,
                "literal p=2 fine-prime interval fixture")
        for anchor in (Fraction(1, 2), Fraction(3, 2), Fraction(21, 2)):
            nearest = theta * anchor + Fraction(1, 2)
            cell_offset = nearest.numerator // nearest.denominator
            beta0 = theta * anchor - cell_offset
            for x, y in product((Fraction(-1, 2), Fraction(1, 2)), repeat=2):
                h = y - x
                beta_x = beta0 + theta * x
                beta_y = beta0 + theta * y
                physical = -alpha ** 2 * ((rho * h + beta_x) ** 2 - beta_y ** 2)
                core = -alpha ** 2 * rho * h ** 2
                linear = -2 * alpha ** 2 * beta0 * h
                chirp = alpha ** 2 * theta * (x ** 2 - y ** 2)
                require(physical == core + linear + chirp, "exact narrow log coefficient")
                require(abs(beta_x) < Fraction(1, 2) and abs(beta_y) < Fraction(1, 2),
                        "same-cell beta range")
                shift = -beta0 / rho
                require(linear == 2 * alpha ** 2 * rho * shift * h,
                        "source column-minus-row shift sign")
                count += 1
    return count


def rational_gaussian(order, q):
    return [[prod((q[k] for k in range(len(q)) if (x ^ y) >> k & 1),
                  start=Fraction(1)) for y in order] for x in order]


def negative_controls():
    names = []
    require(specialize({(3, 0): 1, (0, 5): -1}, [3, 5], [8, 8]) == {},
            "degree-threshold collision")
    names.append("individual_prime_degree_threshold")
    require(specialize({(1, 0): 1, (0, 3): -1}, [9, 27], [32, 32]) == {},
            "noncoprime low-degree collision")
    names.append("distinct_odd_noncoprime_denominators")
    require(specialize({(1, 0): 1, (0, 1): -1}, [3, 5], [3, 5]) == {},
            "nonunit-target collision")
    names.append("nonunit_numerators")
    for denominators, targets in (([9, 27], [32, 32]), ([3, 5], [3, 5])):
        try:
            crt_domain(denominators, targets)
        except CheckFailure:
            pass
        else:
            raise CheckFailure("invalid CRT input accepted")
    source_domain([3, 5], [8, 8], 3)
    names.append("common_alpha_divisible_by_source_prime_is_allowed")
    for primes, targets, alpha in (([3, 5], [8, 8], 0), ([3, 3], [8, 8], 1),
                                   ([3, 5], [3, 8], 1), ([9, 25], [16, 32], 1)):
        try:
            source_domain(primes, targets, alpha)
        except CheckFailure:
            names.append("source_domain_rejection_" + str(len(names)))
        else:
            raise CheckFailure("invalid source input accepted")
    require(sum(c * Fraction(1, 2) ** e for e, c in {1: 2, 0: -1}.items()) == 0,
            "algebraic base may be a polynomial root")
    names.append("algebraic_surrogate_root")
    path = stein([[int(x ^ y == 1) for y in range(4)] for x in range(4)])
    require(determinant(minor(path, [0, 2])) == 0,
            "arbitrary even-size deletion need not preserve unit minor")
    names.append("nonprefix_vertex_deletion")
    h = rational_gaussian([0, 1, 3, 2], [Fraction(1, 2)] * 2)
    d = [1, 2, 3, 4]
    gauged = [[Fraction(d[i], d[j]) * h[i][j] for j in range(4)] for i in range(4)]
    require(determinant(stein(h)) == 0 and determinant(stein(gauged)) == Fraction(-3, 512),
            "ordinary rank not diagonal-similarity invariant")
    require(all(stein(h)[i][j] == 0 for i in range(1, 4) for j in range(1, 4))
            and determinant(minor(stein(h), [0, 1])) != 0, "ungauged rank exactly two")
    names.append("diagonal_similarity_changes_rank")
    full = rational_gaussian([0, 1, 2, 3], [Fraction(1, 2), Fraction(1, 3)])
    require(minor(stein(full), [1, 2]) != stein(minor(full, [1, 2])),
            "compressed shift differs from principal Stein minor")
    names.append("compressing_before_shift")
    rounded = [[Fraction(i == j) for j in range(4)] for i in range(4)]
    tiny = rational_gaussian([0, 1, 2, 3], [Fraction(1, 8), Fraction(1, 16)])
    require(all(abs(tiny[i][j] - rounded[i][j]) < Fraction(1, 2)
                for i in range(4) for j in range(4)), "literal coarse-rounding control")
    require(determinant(stein(tiny)) != 0 and determinant(stein(rounded)) == 0,
            "coarse rounding can erase exact nonzero determinant")
    names.append("coarse_rounding_changes_rank")
    return names


def authenticate():
    expected = {
        "inputs/A9-PROOF.md": "3e87c32b9cb3695dc42c2ef10da9c05e74d1742a37e49ce0fe5890ea093463dc",
        "inputs/FINE-PRIME-PADDING.md": "47d1b1b4df28aadda3cd6bdeb1fbc47290595e9208cd09c1a1f338520d33fdce",
        "inputs/GAUGEFREE-INTERIORS.md": "a7fc34302a70f8453f877a6433ffe2776457bf37b5d8bb262afcb6b198a935fc",
    }
    root = Path(__file__).parent
    for name, digest in expected.items():
        require(sha256((root / name).read_bytes()).hexdigest() == digest,
                "retained input authentication: " + name)
    return expected


def main():
    authenticated = authenticate()
    result = {
        "status": "PASS_FINE_PRIME_BINARY_CORE_RANK",
        "base_commit": "e54523517d0f03e58352e647c403a5af3e525a57",
        "predecessor_commit": "085b30f8e036f69421d5953d0993ac4974ec3f24",
        "pointwise_bound": "min(2 ceil((2^g+3)/5), min_i(s_i)-1)",
        "exponent_box_checks": exponent_boxes(),
        "trimmed_minor_checks": trimming_checks(),
        "literal_source_specialized_polynomials": polynomial_checks(),
        "exact_narrow_exponent_identities": source_exponent_checks(),
        "negative_controls": negative_controls(),
        "authenticated_inputs": authenticated,
        "scientific_hashes": {n: sha256((Path(__file__).parent / n).read_bytes()).hexdigest()
                              for n in ("PROOF.md", "verify.py")},
        "transcendence": "Cited Gelfond-Schneider theorem; no numerical transcendence oracle",
        "scope": "Exact unshifted normalized binary core only; no physical or rounding transfer; no kappa",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
