"""Exact, standalone model for the fixed PR598 norm-six encoder experiment.

Golay generator, Leech line ordering and the direction recipe: DominikScholz,
PR598, with its cited Bannai--Sloane and SageMath sources. New integer-valued
coefficient coordinates and random-access implementation: CubeJerry, with
substantial OpenAI assistance. Apache-2.0; see NOTICE.md.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
from typing import Iterable, Sequence

RIGHT_ROWS = (
    "101011100011", "111110010010", "110100101011", "110001110110",
    "110011011001", "011001101101", "001100110111", "101101111000",
    "010110111100", "001011011110", "101110001101", "010111000111",
)
PAIRS = tuple((i, j) for i in range(24) for j in range(24) if i != j)
TRIPLES = tuple(combinations(range(24), 3))
COORDINATE_PAIRS = tuple(combinations(range(24), 2))
FEATURES = 2600
LINES = 98280


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def dot(a: Sequence[int], b: Sequence[int]) -> int:
    require(len(a) == len(b), "dot-product dimensions")
    return sum(x * y for x, y in zip(a, b))


@lru_cache(maxsize=1)
def geometry() -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    generators = tuple((1 << i) | sum(int(c) << (12 + j)
                       for j, c in enumerate(row))
                       for i, row in enumerate(RIGHT_ROWS))
    require(all((a & b).bit_count() % 2 == 0
                for a in generators for b in generators), "Golay orthogonality")
    words = []
    for message in range(4096):
        word = 0
        for i in range(12):
            if message >> i & 1:
                word ^= generators[i]
        words.append(word)
    require(len(set(words)) == 4096, "Golay dimension")
    require(dict(Counter(w.bit_count() for w in words)) ==
            {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}, "Golay weights")
    octads = tuple(tuple(i for i in range(24) if w >> i & 1)
                   for w in words if w.bit_count() == 8)
    require(set(t for o in octads for t in combinations(o, 3)) == set(TRIPLES),
            "octads must cover every triple for the injectivity proof")
    return tuple(words), octads


@lru_cache(maxsize=8192)
def line(index: int) -> tuple[int, ...]:
    """The exact canonical line order of PR598, without a NumPy dependency."""
    require(type(index) is int and 0 <= index < LINES, "line index")
    words, octads = geometry()
    v = [0] * 24
    if index < 552:
        pair, sign = divmod(index, 2)
        i, j = COORDINATE_PAIRS[pair]
        v[i], v[j] = 4, (4 if sign == 0 else -4)
    elif index < 49128:
        octad, choice = divmod(index - 552, 64)
        mask = 2 * choice  # the first nonzero coordinate is positive
        signs = [-2 if mask >> j & 1 else 2 for j in range(7)]
        signs.append(-2 if mask.bit_count() % 2 else 2)
        for i, s in zip(octads[octad], signs):
            v[i] = s
    else:
        block, choice = divmod(index - 49128, 24)
        message, special = ((2 * block, choice + 1) if choice < 23
                            else (2 * block + 1, 0))
        word = words[message]
        v = [-1 if word >> i & 1 else 1 for i in range(24)]
        v[special] *= -3
    require(dot(v, v) == 32, "minimal-line norm")
    require(next(x for x in v if x) > 0, "canonical line orientation")
    return tuple(v)


def direction(pair: Sequence[int]) -> tuple[int, ...]:
    require(len(pair) == 3 and all(type(x) is int for x in pair), "pair shape")
    i, j, sign = pair
    require(sign in (-1, 1), "pair sign")
    x, y = line(i), line(j)
    require(dot(x, y) == -8 * sign, "pair must give a norm-six direction")
    a = tuple(u + sign * v for u, v in zip(x, y))
    if next(u for u in a if u) < 0:
        a = tuple(-u for u in a)
    require(dot(a, a) == 48, "direction norm")
    return a


def coordinates(a: Sequence[int]) -> tuple[int, ...]:
    """E_a(x)=((a.x)^3-256(a.x))/3 = A(x).C(a), for x.x=32.

    A: 24 features (x_i^3-31*x_i)/3, 552 ordered x_i*x_j^2,
    then 2024 lexicographic x_i*x_j*x_k. No division by 3 occurs at
    run time in the scalar circuit: these are precomputed integer constants.
    """
    require(len(a) == 24 and all(type(x) is int for x in a), "direction coordinates")
    cubes = [x ** 3 for x in a]
    numerators = [31 * c - 256 * x for c, x in zip(cubes, a)]
    require(all(v % 3 == 0 for v in numerators), "integer-valued coefficient")
    offset = [v // 3 for v in numerators]
    result = [32 * c - 256 * x for c, x in zip(cubes, a)]
    result.extend(a[i] * a[j] ** 2 + offset[i] for i, j in PAIRS)
    result.extend(2 * a[i] * a[j] * a[k] for i, j, k in TRIPLES)
    require(len(result) == FEATURES, "feature count")
    return tuple(result)


def features(x: Sequence[int]) -> tuple[int, ...]:
    require(len(x) == 24 and dot(x, x) == 32, "feature domain")
    numerators = [v ** 3 - 31 * v for v in x]
    require(all(v % 3 == 0 for v in numerators), "integer-valued feature")
    return (tuple(v // 3 for v in numerators)
            + tuple(x[i] * x[j] ** 2 for i, j in PAIRS)
            + tuple(x[i] * x[j] * x[k] for i, j, k in TRIPLES))


def pairing(a: Sequence[int], b: Sequence[int]) -> int:
    t = dot(a, b)
    require(t % 8 == 0, "integral Leech pairing")
    return (t // 8 + 1) % 2


def binary_rank(rows: Iterable[int]) -> int:
    pivots: dict[int, int] = {}
    for value in rows:
        while value:
            p = value.bit_length() - 1
            if p in pivots:
                value ^= pivots[p]
            else:
                pivots[p] = value
                break
    return len(pivots)
