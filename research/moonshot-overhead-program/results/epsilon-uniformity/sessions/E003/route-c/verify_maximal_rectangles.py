#!/usr/bin/env python3
"""Exact finite checks of the maximal-rectangle and bulk-thinning statements."""
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def bit_indices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def universe(q, k):
    words = list(product(range(q), repeat=k))
    index = {word: i for i, word in enumerate(words)}
    neighbors = [sum(1 << j for j, y in enumerate(words)
                     if all(a != b for a, b in zip(x, y))) for x in words]
    return words, index, neighbors


def product_mask(sides, index):
    return sum(1 << index[word] for word in product(*sides))


def rank_f2(rows):
    pivots = {}
    for row in rows:
        while row:
            col = row.bit_length() - 1
            if col not in pivots:
                pivots[col] = row
                break
            row ^= pivots[col]
    return len(pivots)


def rank_mod(rows, n, p):
    matrix = [[(row >> j) & 1 for j in range(n)] for row in rows]
    rank = 0
    for j in range(n):
        pivot = next((i for i in range(rank, n) if matrix[i][j]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][j], -1, p)
        matrix[rank] = [(x * inv) % p for x in matrix[rank]]
        for i in range(rank + 1, n):
            factor = matrix[i][j]
            if factor:
                matrix[i] = [(x - factor * y) % p
                             for x, y in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


def classify(q, k):
    words, index, neighbors = universe(q, k)
    n = len(words)
    common = [(1 << n) - 1] * (1 << n)
    maximal = set()
    for mask in range(1, 1 << n):
        bit = mask & -mask
        common[mask] = common[mask ^ bit] & neighbors[bit.bit_length() - 1]
    for mask in range(1, 1 << n):
        dest = common[mask]
        if dest and common[dest] == mask:
            maximal.add((mask, dest))
    predicted = set()
    for cuts in product(range(1, (1 << q) - 1), repeat=k):
        source = [[j for j in range(q) if (cut >> j) & 1] for cut in cuts]
        dest = [[j for j in range(q) if not ((cut >> j) & 1)] for cut in cuts]
        predicted.add((product_mask(source, index), product_mask(dest, index)))
    assert maximal == predicted
    assert len(maximal) == ((1 << q) - 2) ** k
    sizes = [a.bit_count() * b.bit_count() for a, b in maximal]
    assert min(sizes) == (q - 1) ** k
    return {"q": q, "k": k, "source_subsets": (1 << n) - 1,
            "maximal_rectangles": len(maximal), "minimum_size_product": min(sizes)}


def check_partition(q, k, rectangles, words, index, neighbors):
    n = len(words)
    covered = [0] * n
    left, right = [0] * n, [0] * n
    for a, b in rectangles:
        assert a and b
        for x in bit_indices(a):
            assert b & ~neighbors[x] == 0, "unsupported rectangle"
            assert covered[x] & b == 0, "overlapping partition edges"
            covered[x] |= b
            left[x] += 1
        for y in bit_indices(b):
            right[y] += 1
    assert covered == neighbors
    return max(left), max(right)


def opposing_stars(q, k, r):
    words, index, neighbors = universe(q, k)
    rectangles = []
    for anchor in words:
        a = [[j for j in range(q) if j != v] if i < r else [v]
             for i, v in enumerate(anchor)]
        b = [[v] if i < r else [j for j in range(q) if j != v]
             for i, v in enumerate(anchor)]
        rectangles.append((product_mask(a, index), product_mask(b, index)))
    left, right = check_partition(q, k, rectangles, words, index, neighbors)
    assert (left, right) == ((q - 1) ** r, (q - 1) ** (k - r))
    assert left * right == (q - 1) ** k
    rank = rank_f2(neighbors) if q % 2 == 0 else rank_mod(neighbors, len(words), 101)
    assert rank == len(words)
    return {"q": q, "k": k, "source_complement_coordinates": r,
            "rectangles": len(rectangles), "edges": len(words) * (q - 1) ** k,
            "source_load": left, "destination_load": right, "rank": rank}


def first_difference(q, k):
    assert q & (q - 1) == 0
    letters = []
    size = q // 2
    while size:
        for start in range(0, q, 2 * size):
            a = list(range(start, start + size))
            b = list(range(start + size, start + 2 * size))
            letters.extend(((a, b), (b, a)))
        size //= 2
    words, index, neighbors = universe(q, k)
    rectangles = [(product_mask([x[0] for x in factors], index),
                   product_mask([x[1] for x in factors], index))
                  for factors in product(letters, repeat=k)]
    return words, index, neighbors, rectangles


def refine_by_checksum(rectangles, words):
    refined = []
    for a, b in rectangles:
        sources = [sum(1 << i for i in bit_indices(a) if sum(words[i]) % 2 == parity)
                   for parity in (0, 1)]
        destinations = [sum(1 << i for i in bit_indices(b) if sum(words[i]) % 2 == parity)
                        for parity in (0, 1)]
        refined.extend((x, y) for x in sources for y in destinations if x and y)
    return refined


def extension(q, k, a, b, words, index):
    projections = [sorted({words[x][i] for x in bit_indices(a)}) for i in range(k)]
    complement = [[j for j in range(q) if j not in side] for side in projections]
    ahat, bhat = product_mask(projections, index), product_mask(complement, index)
    assert a & ~ahat == b & ~bhat == 0
    return ahat, bhat


def bulk_check(q, k, refine=False):
    words, index, neighbors, rectangles = first_difference(q, k)
    if refine:
        rectangles = refine_by_checksum(rectangles, words)
    la, lb = check_partition(q, k, rectangles, words, index, neighbors)
    n, b0square = len(words), (q - 1) ** k
    absolute_rows, density_rows = [0] * n, [0] * n
    absolute_small = density_small = nonproduct = 0
    for a, b in rectangles:
        ahat, bhat = extension(q, k, a, b, words, index)
        ab, hh = a.bit_count() * b.bit_count(), ahat.bit_count() * bhat.bit_count()
        assert hh >= b0square
        for mask in (a, b):
            projections = [{words[x][i] for x in bit_indices(mask)} for i in range(k)]
            hull_size = 1
            for side in projections:
                hull_size *= len(side)
            nonproduct += hull_size != mask.bit_count()
        if ab <= 4 * la * lb:
            absolute_small += 1
            for x in bit_indices(a):
                absolute_rows[x] ^= b
        if ab * b0square <= 4 * la * lb * hh:
            density_small += 1
            for x in bit_indices(a):
                density_rows[x] ^= b
    ar, dr = rank_f2(absolute_rows), rank_f2(density_rows)
    assert 2 * ar >= n and 2 * dr >= n
    assert absolute_small >= ar and density_small >= dr
    if refine and k > 1:
        assert nonproduct > 0
    return {"q": q, "k": k, "checksum_refinement": refine,
            "rectangles": len(rectangles), "loads": [la, lb],
            "nonproduct_sides": nonproduct,
            "absolute_small_rectangles": absolute_small, "absolute_small_rank": ar,
            "density_small_rectangles": density_small, "density_small_rank": dr,
            "rank_floor": n // 2, "density_threshold_nonvacuous": 4 * la * lb < b0square}


def unsupported_control():
    q, k = 8, 2
    words, index, neighbors = universe(q, k)
    all_letters = list(range(q))
    letters = [(all_letters, all_letters)] + [([i], [i]) for i in range(q)]
    rectangles = [(product_mask([f[0] for f in factors], index),
                   product_mask([f[1] for f in factors], index))
                  for factors in product(letters, repeat=k)]
    rows, left, right = [0] * len(words), [0] * len(words), [0] * len(words)
    unsupported = 0
    for a, b in rectangles:
        bad = False
        for x in bit_indices(a):
            rows[x] ^= b
            left[x] += 1
            bad |= bool(b & ~neighbors[x])
        for y in bit_indices(b):
            right[y] += 1
        unsupported += bad
    assert rows == neighbors
    assert max(left + right) == 4 < q - 1
    assert unsupported
    return {"q": q, "k": k, "rectangles": len(rectangles),
            "load": 4, "supported_maximal_floor": q - 1,
            "unsupported_rectangles": unsupported, "exact_F2_identity": True}


def main():
    classifications = [classify(q, k) for q, k in
                       [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (4, 1), (4, 2)]]
    stars = [opposing_stars(q, k, r) for q, k in
             [(2, 3), (3, 2), (3, 4), (4, 2), (4, 4), (8, 2), (16, 2)]
             for r in range(k + 1)]
    bulk = [bulk_check(4, 2), bulk_check(16, 2), bulk_check(512, 1),
            bulk_check(4, 2, True), bulk_check(16, 2, True)]
    assert any(x['density_threshold_nonvacuous'] for x in bulk)
    assert any(x['absolute_small_rectangles'] < x['rectangles'] for x in bulk)
    _, _, neighbors = universe(4, 2)
    exceptional_rank = rank_mod(neighbors, 16, 3)
    assert exceptional_rank == 9 < 16
    unsupported = unsupported_control()
    receipt = {"status": "passed", "maximal_classifications": classifications,
               "source_subsets_examined": sum(x['source_subsets'] for x in classifications),
               "sharp_partitions": stars, "bulk_rank_checks": bulk,
               "negative_controls": {
                   "characteristic_three_C4_squared_rank": exceptional_rank,
                   "unsupported_cancellation": unsupported},
               "scope": "Finite exact checks; universal restrictions use the companion proof.",
               "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ['MAXIMAL-RECTANGLE-OBSTRUCTION.md', Path(__file__).name]}}
    (ROOT / 'maximal-rectangle-verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
