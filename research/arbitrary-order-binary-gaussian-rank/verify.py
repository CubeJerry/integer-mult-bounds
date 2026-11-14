#!/usr/bin/env python3
"""Read-only exact corroboration for the stated arbitrary-order rank theorem.

Standard library only. The universal proof is PROOF.md, not finite coverage.
Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
SPDX-License-Identifier: Apache-2.0
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def validate_order(order):
    n = len(order)
    require(n >= 2 and n & (n - 1) == 0, "positive binary dimension")
    require(sorted(order) == list(range(n)), "order must contain every vertex once")
    return n


def shift_displacement(a, cyclic=False, plus=False):
    n = len(a)
    sign = 1 if plus else -1
    return [[a[i][j] + sign * (a[(i - 1) % n][(j - 1) % n]
            if cyclic or i > 0 and j > 0 else 0)
            for j in range(n)] for i in range(n)]


def translation_matrix(order, mask):
    return [[int(x ^ y == mask) for y in order] for x in order]


def principal(a, keep):
    return [[a[i][j] for j in keep] for i in keep]


def det_integer(a):
    """Fraction-free Bareiss, with exact divisibility checks."""
    n = len(a)
    if n == 0:
        return 1
    b = [list(row) for row in a]
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if b[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            b[k], b[pivot_row] = b[pivot_row], b[k]
            sign = -sign
        pivot = b[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = b[i][j] * pivot - b[i][k] * b[k][j]
                require(numerator % previous == 0, "Bareiss exact division")
                b[i][j] = numerator // previous
            b[i][k] = 0
        previous = pivot
    return sign * b[-1][-1]


def rank_mod2(a):
    rows = [sum((x & 1) << j for j, x in enumerate(row)) for row in a]
    rank = 0
    for col in range(len(a)):
        pivot = next((i for i in range(rank, len(rows))
                      if rows[i] >> col & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(rank + 1, len(rows)):
            if rows[i] >> col & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def rank_rational(a):
    b = [[Fraction(x) for x in row] for row in a]
    rank = 0
    for col in range(len(b[0])):
        pivot = next((i for i in range(rank, len(b)) if b[i][col]), None)
        if pivot is None:
            continue
        b[rank], b[pivot] = b[pivot], b[rank]
        factor = b[rank][col]
        b[rank] = [x / factor for x in b[rank]]
        for i in range(rank + 1, len(b)):
            factor = b[i][col]
            if factor:
                b[i] = [x - factor * y for x, y in zip(b[i], b[rank])]
        rank += 1
        if rank == len(b):
            break
    return rank


def inverse(a):
    n = len(a)
    b = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if b[i][col]), None)
        require(pivot is not None, "invertible test input")
        b[col], b[pivot] = b[pivot], b[col]
        factor = b[col][col]
        b[col] = [x / factor for x in b[col]]
        for i in range(n):
            if i != col:
                factor = b[i][col]
                b[i] = [x - factor * y for x, y in zip(b[i], b[col])]
    return [row[n:] for row in b]


def graph_data(order, mask):
    n = len(order)
    position = {x: i for i, x in enumerate(order)}
    mate = [position[x ^ mask] for x in order]
    original = [(i, mate[i]) for i in range(n) if i < mate[i]]
    shifted = [(i + 1, j + 1) for i, j in original if j < n - 1]
    adjacency = [[] for _ in order]
    for color, edges in ((1, original), (-1, shifted)):
        for i, j in edges:
            adjacency[i].append((j, color))
            adjacency[j].append((i, color))
    remaining, cycles, paths = set(range(n)), [], []
    while remaining:
        todo, component = [min(remaining)], set()
        while todo:
            x = todo.pop()
            if x not in component:
                component.add(x)
                todo.extend(y for y, _ in adjacency[x])
        remaining -= component
        degrees = [len(adjacency[x]) for x in component]
        if all(x == 2 for x in degrees):
            cycles.append(component)
        else:
            require(degrees.count(1) == 2 and set(degrees) <= {1, 2},
                    "one alternating open component")
            paths.append(component)
    require(len(paths) == 1 and len(paths[0]) % 2 == 0, "one even open path")
    excluded = set()
    for component in cycles:
        require(len(component) % 2 == 0, "even closed component")
        x = min(component)
        excluded.update((x, mate[x]))
        require(any(abs(i - mate[i]) != 1 for i in component),
                "each cycle spends a nonadjacent original edge")
    return {
        "cycles": len(cycles), "parallel": sum(len(x) == 2 for x in cycles),
        "adjacent": sum(j == i + 1 for i, j in original),
        "keep": [i for i in range(n) if i not in excluded],
        "parallel_pairs": {tuple(sorted(x)) for x in cycles if len(x) == 2},
    }


def check_order(order, rational=False):
    n = validate_order(order)
    multiplicity = Counter(order[i] ^ order[i - 1] for i in range(1, n))
    expected_parallel = Counter()
    for a in range(1, n):
        for b in range(a + 1, n):
            if order[a] ^ order[a - 1] == order[b] ^ order[b - 1]:
                expected_parallel[(order[a] ^ order[b], a, b)] += 1
    data = []
    seen_parallel = Counter()
    for mask in range(1, n):
        g = graph_data(order, mask)
        require(g["adjacent"] == multiplicity[mask], "direction multiplicity")
        require(g["cycles"] <= n // 2 - g["adjacent"], "first cycle bound")
        require(4 * g["cycles"] <= n - 2 + 2 * g["parallel"],
                "cycle size bound")
        a = shift_displacement(translation_matrix(order, mask))
        r = n - 2 * g["cycles"]
        require(len(g["keep"]) == r, "retained minor size")
        require(abs(det_integer(principal(a, g["keep"]))) == 1, "unit minor")
        require(rank_mod2(a) == r, "characteristic-two exact graph rank")
        if rational:
            require(rank_rational(a) == r, "rational exact graph rank")
        for x, y in g["parallel_pairs"]:
            seen_parallel[(mask, x, y)] += 1
        data.append(g)
    require(seen_parallel == expected_parallel, "parallel-cycle bijection")
    m = max(multiplicity.values())
    require(m <= n // 2 and sum(multiplicity.values()) == n - 1, "path counts")
    c = min(g["cycles"] for g in data)
    require(4 * c <= n + m - 3, "averaged cycle bound")
    bound = 2 * ((n + 7) // 5)
    require(n - 2 * c >= bound, "universal weaker bound")
    return data


def gaussian(order, q):
    def monomial(mask):
        value = Fraction(1)
        for bit, x in enumerate(q):
            if mask >> bit & 1:
                value *= x
        return value
    return [[monomial(x ^ y) for y in order] for x in order]


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def poly_add(a, b, sign=1):
    out = dict(a)
    for exponent, value in b.items():
        out[exponent] = out.get(exponent, 0) + sign * value
        if out[exponent] == 0:
            del out[exponent]
    return out


def poly_multiply(a, b):
    out = {}
    for x, c in a.items():
        for y, d in b.items():
            z = tuple(i + j for i, j in zip(x, y))
            out[z] = out.get(z, 0) + c * d
    return {x: c for x, c in out.items() if c}


def polynomial_minor(order, keep):
    d = len(order).bit_length() - 1
    def entry(i, j):
        e = tuple((order[i] ^ order[j]) >> bit & 1 for bit in range(d))
        out = {e: 1}
        if i and j:
            f = tuple((order[i - 1] ^ order[j - 1]) >> bit & 1 for bit in range(d))
            out = poly_add(out, {f: 1}, -1)
        return out
    result = {}
    for p in permutations(range(len(keep))):
        inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
        term = {(0,) * d: (-1) ** inversions}
        for i, j in enumerate(p):
            term = poly_multiply(term, entry(keep[i], keep[j]))
        result = poly_add(result, term)
    return result


def coefficient_checks():
    count = 0
    for d in (1, 2):
        n = 1 << d
        for tail in permutations(range(1, n)):
            order = (0,) + tail
            for mask in range(1, n):
                g = graph_data(order, mask)
                polynomial = polynomial_minor(order, g["keep"])
                r = len(g["keep"])
                target = tuple(r if mask >> bit & 1 else 0 for bit in range(d))
                a = shift_displacement(translation_matrix(order, mask))
                expected = det_integer(principal(a, g["keep"]))
                require(polynomial.get(target) == expected, "literal polynomial coefficient")
                require(abs(expected) == 1, "coefficient survives every characteristic")
                count += 1
    return count


def positive_fixtures():
    exceptional = (0, 1, 2, 3, 7, 5, 6, 4)
    gray = (0, 1, 3, 2, 6, 7, 5, 4)
    q_bad = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 5)]
    q_good = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 7)]
    rows = []
    for name, order in (("exceptional_order", exceptional), ("gray_order", gray)):
        for kind, q, expected in (("exceptional", q_bad, 6), ("nonexceptional", q_good, 8)):
            a = gaussian(order, q)
            e = shift_displacement(a)
            rank = rank_rational(e)
            require(rank == expected, "exact exceptional/nonexceptional tuple")
            ainv = inverse(a)
            reversal = [list(reversed(row)) for row in reversed(a)]
            inverse_rank = rank_rational(shift_displacement(ainv))
            reverse_rank = rank_rational(shift_displacement(reversal))
            require(inverse_rank == reverse_rank, "inverse/reversed forward rank identity")
            require(multiply(a, ainv) == [[int(i == j) for j in range(8)] for i in range(8)],
                    "exact inverse multiplication")
            rows.append({"name": name, "tuple": kind, "rank": rank,
                         "inverse_rank": inverse_rank, "reversed_rank": reverse_rank})
    kernels = [[0, Fraction(9, 5), Fraction(-9, 5), Fraction(7, 15),
                Fraction(-4, 3), -4, 1, 0],
               [0, Fraction(3, 5), Fraction(-3, 5), Fraction(-2, 5), -1, -2, 0, 1]]
    e = shift_displacement(gaussian(exceptional, q_bad))
    for vector in kernels:
        require(all(sum(x * y for x, y in zip(row, vector)) == 0 for row in e),
                "retained rational kernel vector")
    require(rank_rational(kernels) == 2, "independent kernel vectors")
    return rows


def tensor_generator_checks():
    count = 0
    for n in (2, 3, 5):
        u = [Fraction((-1) ** i * (i + 1), i + 2) for i in range(n)]
        v = [Fraction(i + 3, 2 * i + 1) for i in range(n)]
        low = [[u[i - j] if i >= j else 0 for j in range(n)] for i in range(n)]
        up = [[v[j - i] if j >= i else 0 for j in range(n)] for i in range(n)]
        a = multiply(low, up)
        require(shift_displacement(a) == [[x * y for y in v] for x in u],
                "ordinary lower-upper generator identity")
        count += 1
    return count


def negative_controls():
    names = []
    order = (0, 1, 2, 3)
    a = translation_matrix(order, 2)
    correct = shift_displacement(a)
    wrong = shift_displacement(a, plus=True)
    require(rank_rational(correct) == 2 and rank_rational(wrong) == 4,
            "parallel cancellation mutant detected")
    names.append("uncancelled_parallel_pair")
    require(det_integer(principal(correct, [0, 2, 3])) == 0,
            "one-vertex cycle deletion is singular")
    names.append("one_vertex_cycle_deletion")
    path = translation_matrix(order, 1)
    require(rank_rational(shift_displacement(path)) == 4 and
            rank_rational(shift_displacement(path, cyclic=True)) == 2,
            "cyclic-shift substitution detected")
    names.append("cyclic_instead_of_nilpotent_shift")
    dropped = shift_displacement(path)
    dropped[0][1] = 0
    require(det_integer(dropped) == 0, "dropped minor entry detected")
    names.append("dropped_determinant_entry")
    for value, expected in ((0, 1), (1, 2)):
        e = shift_displacement(gaussian(tuple(range(8)), [Fraction(value)] * 3))
        require(rank_rational(e) == expected, "nongeneric endpoint")
        names.append("all_parameters_" + str(value))
    hom = shift_displacement(gaussian((0, 1, 3, 2), [Fraction(1, 2)] * 2))
    require(rank_rational(hom) == 2, "interior homogeneous exception")
    names.append("positive_homogeneous_rank_two")
    missed = (0, 1, 2, 3, 4, 6, 5, 7)
    data = check_order(missed, rational=True)
    require(all(data[v - 1]["cycles"] > 0 for v in (1, 2, 4)) and
            min(x["cycles"] for x in data) == 0, "axis-only criterion failure")
    names.append("axis_only_connected_criterion")
    for bad in ((0,), (0, 1, 2), (0, 1, 1, 3)):
        try:
            validate_order(bad)
        except CheckFailure:
            names.append("malformed_order_" + str(len(names)))
        else:
            raise CheckFailure("malformed order accepted")
    return names


def higher_dimension_controls():
    orders = [
        [11, 9, 3, 15, 1, 7, 2, 10, 13, 6, 4, 8, 12, 14, 5, 0],
        [0, 26, 11, 12, 2, 9, 19, 24, 25, 3, 14, 29, 31, 20, 10, 13,
         28, 23, 30, 15, 22, 27, 4, 17, 16, 21, 8, 1, 5, 7, 18, 6],
    ]
    out = []
    for order in orders:
        data = check_order(order, rational=True)
        c = min(x["cycles"] for x in data)
        require(c > 0, "all-mask connected criterion fails on preserved order")
        out.append({"order": order, "minimum_closed_cycles": c,
                    "best_coefficient_rank": len(order) - 2 * c,
                    "theorem_bound": 2 * ((len(order) + 7) // 5)})
    return out


def finite_coverage():
    out, masks = [], 0
    for d in (1, 2, 3):
        n = 1 << d
        total = axis_covered = all_covered = 0
        distribution = Counter()
        for tail in permutations(range(1, n)):
            order = (0,) + tail
            data = check_order(order, rational=total < 12)
            min_cycles = min(x["cycles"] for x in data)
            all_covered += min_cycles == 0
            axis_covered += any(data[(1 << bit) - 1]["cycles"] == 0 for bit in range(d))
            distribution[n - 2 * min_cycles] += 1
            total += 1
            masks += n - 1
        out.append({"dimension": d, "orders": total,
                    "axis_connected": axis_covered, "some_mask_connected": all_covered,
                    "best_coefficient_rank_histogram": dict(sorted(distribution.items()))})
    require(out[-1]["orders"] == 5040 and out[-1]["axis_connected"] == 4368 and
            out[-1]["some_mask_connected"] == 5040, "frozen bounded coverage")
    return out, masks


def main():
    coverage, masks = finite_coverage()
    result = {
        "status": "PASS_ARBITRARY_ORDER_BINARY_GAUSSIAN_RANK",
        "base_commit": "e54523517d0f03e58352e647c403a5af3e525a57",
        "claim": "generic forward/inverse rank >= 2 ceil((N+3)/5) for every order",
        "all_dimension_proof": "PROOF.md; finite checks are corroboration",
        "normalized_finite_coverage": coverage,
        "translation_masks_checked": masks,
        "literal_polynomial_coefficient_checks": coefficient_checks(),
        "positive_exact_fixtures": positive_fixtures(),
        "higher_dimension_criterion_failures": higher_dimension_controls(),
        "ordinary_generator_identity_cases": tensor_generator_checks(),
        "negative_controls": negative_controls(),
        "scientific_hashes": {name: sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                              for name in ("PROOF.md", "verify.py")},
        "scope": "No full generic rank theorem, source admission, rounding margin, runtime or new kappa",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
