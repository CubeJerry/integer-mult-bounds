"""Exact source-bound integer lifts for depth-27 recovery relations.

Prepared for @CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
The source matrix and earlier mode-preserving recovery results retain their
#5444/#6327/#6660 attribution. No predecessor verifier is imported.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

FIXTURE_SHA256 = "2ca4d7550fcae5b757ec500f87aee1d2ef9f64b59e4abe2bda93319521304af8"
LATTICE_ROWS = (3, 5, 6, 7, 8, 9, 10, 31)
N = 112
RANK = 104


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def combine(vectors: list[int], coefficients: int) -> int:
    out = 0
    while coefficients:
        low = coefficients & -coefficients
        out ^= vectors[low.bit_length() - 1]
        coefficients ^= low
    return out


def extend(vectors: list[int], dimension: int) -> list[int]:
    out = list(vectors)
    require(rank(out) == len(out), "dependent prescribed basis")
    for i in range(dimension):
        vector = 1 << i
        if rank(out + [vector]) > len(out):
            out.append(vector)
    require(len(out) == dimension, "basis does not span ambient space")
    return out


def coordinate_reader(basis: list[int]):
    pivots: dict[int, tuple[int, int]] = {}
    for i, vector in enumerate(basis):
        coefficients = 1 << i
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (vector, coefficients)
                break
            row, mask = pivots[pivot]
            vector ^= row
            coefficients ^= mask
        require(vector != 0, "coordinate basis dependent")

    def coordinates(vector: int) -> int:
        coefficients = 0
        while vector:
            pivot = vector.bit_length() - 1
            require(pivot in pivots, "vector outside coordinate span")
            row, mask = pivots[pivot]
            vector ^= row
            coefficients ^= mask
        return coefficients

    return coordinates


def inverse_rational(matrix: list[list[int]]) -> list[list[Fraction]]:
    dimension = len(matrix)
    a = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(dimension)]
         for i, row in enumerate(matrix)]
    for column in range(dimension):
        pivot = next((i for i in range(column, dimension) if a[i][column]), None)
        require(pivot is not None, "singular lattice-row basis")
        a[column], a[pivot] = a[pivot], a[column]
        scalar = a[column][column]
        a[column] = [x / scalar for x in a[column]]
        for i in range(dimension):
            if i != column:
                scalar = a[i][column]
                a[i] = [x - scalar * y for x, y in zip(a[i], a[column])]
    return [row[dimension:] for row in a]


def load_source(path: Path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "source fixture hash")
    columns = json.loads(raw)["mode_columns"]
    require(len(columns) == 8 and all(len(c) == N for c in columns), "source shape")
    require(all(type(x) is int for c in columns for x in c), "source integer domain")
    rows = [list(row) for row in zip(*columns)]
    require(all(sum(a * b for a, b in zip(columns[i], columns[j])) == 56 * (i == j)
                for i in range(8) for j in range(8)), "source Gram identity")
    return columns, rows


def source_lattice(rows: list[list[int]]):
    """Return the literal Z^112=ker(M^T) direct-sum lattice splitting.

    The 104 kernel coordinates are the non-pivot physical coordinates. Every
    source row is checked to be an integral combination of the eight pivot
    rows. This stronger check is new; merely checking 2e_i is not enough.
    """
    basis = [[rows[p][mode] for p in LATTICE_ROWS] for mode in range(8)]
    inverse = inverse_rational(basis)
    coefficients = []
    for row in rows:
        entries = [sum(inverse[i][j] * row[j] for j in range(8)) for i in range(8)]
        require(all(x.denominator == 1 for x in entries), "source row outside integer lattice basis")
        coefficients.append([int(x) for x in entries])
    require(all((2 * x).denominator == 1 for row in inverse for x in row), "2Z8 image inclusion")
    free = [i for i in range(N) if i not in LATTICE_ROWS]
    require(len(free) == RANK, "kernel dimension")
    for j in free:
        require(all(rows[j][mode] == sum(coefficients[j][i] * rows[p][mode]
                    for i, p in enumerate(LATTICE_ROWS)) for mode in range(8)), "kernel column")
    return free, coefficients


def relation_maps() -> list[list[int]]:
    """27 rank-three maps F2^4 -> even syndrome hyperplane, balanced kernels."""
    even_basis = [9, 10, 12]
    kernels = [k for k in range(1, 16) for _ in range(1 if k <= 3 else 2)]
    maps = []
    for kernel in kernels:
        annihilator: list[int] = []
        for row in range(1, 16):
            if (row & kernel).bit_count() % 2 == 0 and rank(annihilator + [row]) > len(annihilator):
                annihilator.append(row)
        require(len(annihilator) == 3, "rank-three annihilator")
        columns = [combine(even_basis, sum(((row >> i) & 1) << j
                   for j, row in enumerate(annihilator))) for i in range(4)]
        require(rank(columns) == 3, "rank-three relation map")
        require([u for u in range(1, 16) if combine(columns, u) == 0] == [kernel], "relation kernel")
        require(all(x.bit_count() % 2 == 0 for x in columns), "even relation images")
        maps.append(columns)
    return maps


def quotient_images(maps: list[list[int]]) -> list[list[int]]:
    dimension = 4 * len(maps)
    relations = [sum(maps[j][i] << (4 * j) for j in range(len(maps))) for i in range(4)]
    require(rank(relations) == 4, "relation-space dimension")
    require(all(sum(bool((combine(relations, u) >> (4 * j)) & 15) for j in range(len(maps))) >= 2
                for u in range(1, 16)), "single-stage relation forbidden")
    pivots: dict[int, int] = {}
    for row in relations:
        while row:
            p = row.bit_length() - 1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    free = [i for i in range(dimension) if i not in pivots]

    def reduce(row):
        for p in sorted(pivots, reverse=True):
            if (row >> p) & 1:
                row ^= pivots[p]
        return sum(((row >> p) & 1) << j for j, p in enumerate(free))

    images = [[reduce(1 << (4 * j + i)) for i in range(4)] for j in range(len(maps))]
    require(all(rank(block) == 4 for block in images), "individual image injection")
    require(rank([x for block in images for x in block]) == RANK, "whole image rank104")
    require(all(combine([x for block in images for x in block], row) == 0 for row in relations), "quotient relation equation")
    return images


def align_images(images: list[list[int]], actual: list[int]) -> list[list[int]]:
    coordinates = coordinate_reader(extend(images[0], RANK))
    target = extend(actual, RANK)
    out = [[combine(target, coordinates(v)) for v in block] for block in images]
    require(out[0] == actual, "first cumulative frame must be identity")
    return out


def lift_operations(source: list[int], target: list[int]):
    read = coordinate_reader(extend(source, RANK))
    basis = extend(target, RANK)
    columns = [combine(basis, read(1 << i)) for i in range(RANK)]
    rows = [sum(((columns[j] >> i) & 1) << j for j in range(RANK)) for i in range(RANK)]
    operations = []
    for j in range(RANK):
        pivot = next((i for i in range(j, RANK) if (rows[i] >> j) & 1), None)
        require(pivot is not None, "binary matrix singular")
        if pivot != j:
            rows[pivot], rows[j] = rows[j], rows[pivot]
            operations.append(("swap", pivot, j))
        for i in range(RANK):
            if i != j and ((rows[i] >> j) & 1):
                rows[i] ^= rows[j]
                operations.append(("add", i, j))
    require(rows == [1 << i for i in range(RANK)], "binary elimination")
    return operations


def apply_kernel_lift(values: list[int], operations, inverse=False) -> list[int]:
    out = list(values)
    for kind, i, j in (operations if inverse else reversed(operations)):
        if kind == "swap":
            out[i], out[j] = out[j], out[i]
        else:
            out[i] += out[j] if inverse else -out[j]
    return out


def apply_frame(vector, operations, free, coefficients, inverse=False):
    kernel = [vector[j] for j in free]
    complement = [vector[p] + sum(coefficients[j][i] * vector[j] for j in free)
                  for i, p in enumerate(LATTICE_ROWS)]
    moved = apply_kernel_lift(kernel, operations, inverse)
    out = [0] * N
    for j, value in zip(free, moved):
        out[j] = value
    for i, p in enumerate(LATTICE_ROWS):
        out[p] = complement[i] - sum(coefficients[j][i] * out[j] for j in free)
    return out


def construct(path: Path):
    columns, rows = load_source(path)
    free, coefficients = source_lattice(rows)
    source_columns = [sum((columns[j][i] & 1) << k for k, i in enumerate(free)) for j in range(8)]
    chosen: list[int] = []
    chosen_indices = []
    for i, vector in enumerate(source_columns):
        if rank(chosen + [vector]) > len(chosen):
            chosen.append(vector)
            chosen_indices.append(i)
    require(len(chosen) == 4, "source binary rank4")
    read = coordinate_reader(chosen)
    source_coefficients = [read(v) for v in source_columns]
    # Chosen quotient representatives are individual unit vectors, so parity
    # of a syndrome is exactly ordinary parity of its four coordinates.
    require(all((mask.bit_count() - 1) % 2 == 0 for mask in source_coefficients), "quotient parity chart")
    maps = relation_maps()
    images = align_images(quotient_images(maps), chosen)
    operations = [lift_operations(chosen, image) for image in images]
    require(operations[0] == [], "first integer frame identity")
    for block, ops in zip(images, operations):
        for j, column in enumerate(columns):
            moved = apply_frame(column, ops, free, coefficients)
            actual = sum((moved[i] & 1) << k for k, i in enumerate(free))
            require(actual == combine(block, source_coefficients[j]), "integer lift image")
            require(all(sum(rows[i][m] * moved[i] for i in range(N)) == 56 * (m == j)
                        for m in range(8)), "integer lift preserves actual source modes")
            require(apply_frame(moved, ops, free, coefficients, True) == column, "integer lift inverse")
    return {"columns": columns, "rows": rows, "free": free,
            "coefficients": coefficients, "images": images,
            "maps": maps, "operations": operations,
            "source_coefficients": source_coefficients,
            "chosen_indices": chosen_indices}
