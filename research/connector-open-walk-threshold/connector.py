"""Open-walk certificates; @CubeJerry/OpenAI Codex, Apache-2.0.
The positive upward/downward split is apoursh's CrocSwap #6071 construction.
"""
from collections import Counter
from dataclasses import dataclass


def require(ok, message):
    if not ok:
        raise ValueError(message)


def path_bounds(k):
    require(type(k) is int and 1 <= k <= 4096, "dimension domain")
    if k == 1:
        return 1, 1, "one-coordinate"
    q, r = divmod(1 << (k - 1), k)
    lower = ((1 << k) - 2) // k + 1
    closed = 2 * (((1 << (k - 1)) + k - 1) // k)
    if lower == closed:
        return lower, lower, "counting-meets-closed"
    if r == 1:
        return lower, lower, "unique-maximum-deletion"
    require(closed == lower + 1, "one-unit bracket")
    return lower, closed, "open-one-unit-gap"


def inspect_walk(k, word):
    require(type(k) is int and 1 <= k <= 13, "walk dimension")
    require(isinstance(word, (list, tuple)), "transition sequence")
    require((1 << k) - 1 <= len(word) <= 1 << (k + 1), "walk length")
    vertex = 0
    seen = {0}
    flips = [0] * k
    up, down = [], []
    first = {0: (0, 0)}
    for j in word:
        require(type(j) is int and 0 <= j < k, "transition label")
        (down if vertex & (1 << j) else up).append(j)
        flips[j] += 1
        vertex ^= 1 << j
        seen.add(vertex)
        first.setdefault(vertex, (len(up), len(down)))
    require(len(seen) == 1 << k, "walk does not cover cube")
    return tuple(flips), tuple(up), tuple(down), first, vertex


@dataclass(frozen=True)
class Block:
    dimension: int
    characteristic: int
    source_word: tuple
    reads: tuple


def compile_block(k, c, word):
    require(type(c) is int and 2 <= c <= 1024, "characteristic domain")
    flips, up, down, first, _ = inspect_walk(k, word)
    require(max(flips) <= c, "characteristic below flip count")
    middle = tuple(j for j in range(k) for _ in range(c - flips[j]))
    source = up + middle + tuple(reversed(down))
    require(len(source) == k * c, "source-word length")
    reads = [()] * (1 << k)
    for mask in range(1, 1 << k):
        a, d = first[mask]
        reads[mask] = (a, k * c - d)
        require(0 <= a <= k * c - d <= k * c, "read chronology")
    return Block(k, c, source, tuple(reads))


def events(block):
    k, c = block.dimension, block.characteristic
    at = [[] for _ in range(len(block.source_word) + 1)]
    for mask in range(1, 1 << k):
        require(len(block.reads[mask]) == 2, "two productive reads")
        for t in block.reads[mask]:
            require(type(t) is int and 0 <= t <= len(block.source_word), "read boundary")
            at[t].append(mask)
        at[0].extend([mask] * (c - 2))
    for t, outputs in enumerate(at):
        for mask in outputs:
            yield "A", mask
        if t < len(block.source_word):
            yield "B", block.source_word[t]


def literal_prefix_audit(block):
    k, c = block.dimension, block.characteristic
    require(Counter(block.source_word) == Counter({j: c for j in range(k)}), "source multiplicity")
    prefixes = [[0] * k]
    for j in block.source_word:
        row = prefixes[-1].copy()
        row[j] += 1
        prefixes.append(row)
    for mask in range(1, 1 << k):
        a, b = block.reads[mask]
        require(0 <= a <= b <= k * c, "prefix chronology")
        actual = tuple((x + y) % c for x, y in zip(prefixes[a], prefixes[b]))
        require(actual == tuple((mask >> j) & 1 for j in range(k)), "wrong delivered mask")
    return (1 << k) - 1


def audit_events(block, stream):
    """Formal-source execution with arbitrary dirty baseline; no commuting maps."""
    k, c = block.dimension, block.characteristic
    count = Counter()
    z = [0] * k + [1]
    output = [[0] * (k + 1) for _ in range(1 << k)]
    for kind, index in stream:
        count[kind, index] += 1
        if kind == "B":
            require(type(index) is int and 0 <= index < k, "source event")
            z[index] = (z[index] + 1) % c
        else:
            require(kind == "A" and type(index) is int and 1 <= index < 1 << k, "output event")
            output[index] = [(a + b) % c for a, b in zip(output[index], z)]
    wanted_count = Counter({("B", j): c for j in range(k)})
    wanted_count.update({("A", m): c for m in range(1, 1 << k)})
    require(count == wanted_count, "complete-call multiplicity")
    require(z == [0] * k + [1], "dirty connector not restored")
    for mask in range(1, 1 << k):
        require(output[mask] == [(mask >> j) & 1 for j in range(k)] + [0], "full dirty operator identity")
    return sum(count.values())
