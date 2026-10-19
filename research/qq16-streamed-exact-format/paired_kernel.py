#!/usr/bin/env python3
"""Metered in-place Gaussian tensor reference with two-axis blocks.

Each ADD reads two real registers and writes one. Each HALVE reads one and
writes one. The nine dirty-owned scratch registers are overwritten before use
and returned zero once per native call. Array addressing is explicit Python,
not a physical tape implementation. @CubeJerry, Codex assistance.
Apache-2.0; the Gaussian tensor/parity identities are credited prior work.
"""
from collections import Counter


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Registers:
    def __init__(self, width, count):
        self.width = width
        self.values = [-(1 << (width - 1))] * count
        self.counts = Counter()

    def fit(self, value):
        require(-(1 << (self.width - 1)) <= value < 1 << (self.width - 1),
                "signed overflow")
        return value

    def add(self, slot, left, right, subtract=False):
        self.counts["add"] += 1
        self.values[slot] = self.fit(left - right if subtract else left + right)

    def half(self, slot):
        self.counts["halve"] += 1
        value = self.values[slot]
        require(value % 2 == 0, "inexact halving")
        return self.fit(value // 2)

    def close(self):
        for slot in range(len(self.values)):
            self.values[slot] = 0
            self.counts["clear"] += 1


def pair(bank, a, b, sign, r):
    # All array reads precede writes: four partials and one numerator slot.
    r.add(0, bank[a][0], bank[b][0])
    r.add(1, bank[a][1], bank[b][1])
    r.add(2, bank[a][0], bank[b][0], True)
    r.add(3, bank[a][1], bank[b][1], True)
    r.counts["array_read"] += 8
    destinations = (a, b) if sign == 1 else (b, a)
    for destination, subtract in zip(destinations, (True, False)):
        r.add(4, r.values[0], r.values[3], subtract)
        store_component(bank, destination, 0, r.half(4), r)
        r.add(4, r.values[1], r.values[2], not subtract)
        store_component(bank, destination, 1, r.half(4), r)


def store_component(bank, destination, component, value, r):
    # Tuple replacement represents one scalar-register write in the abstract
    # machine; Python object allocation/copying is not a measured RAM runtime.
    old = bank[destination]
    bank[destination] = (value, old[1]) if component == 0 else (old[0], value)
    r.counts["array_write"] += 1


def quad(bank, a, b, c, d, sign, r):
    # C x C in the address order 00,01,10,11. Eight partials consume all
    # original inputs before overwriting any destination; slot 8 is reused.
    r.add(0, bank[b][0], bank[c][0])       # u = br + cr
    r.add(1, bank[d][1], bank[a][1], True) # v = di - ai
    r.add(2, bank[b][1], bank[c][1])       # w = bi + ci
    r.add(3, bank[a][0], bank[d][0], True) # x = ar - dr
    r.add(4, bank[a][0], bank[d][0])       # p = ar + dr
    r.add(5, bank[c][1], bank[b][1], True) # q = ci - bi
    r.add(6, bank[a][1], bank[d][1])       # r = ai + di
    r.add(7, bank[b][0], bank[c][0], True) # s = br - cr
    r.counts["array_read"] += 16
    # C^- = XOR(1) C, so the negative block exchanges 00<->11,01<->10.
    destinations = (a, d, b, c) if sign == 1 else (d, a, c, b)
    recipes = ((0, 1, 2, 3, False), (0, 1, 2, 3, True),
               (4, 5, 6, 7, False), (4, 5, 6, 7, True))
    for destination, (i, j, k, l, subtract) in zip(destinations, recipes):
        r.add(8, r.values[i], r.values[j], subtract)
        store_component(bank, destination, 0, r.half(8), r)
        r.add(8, r.values[k], r.values[l], subtract)
        store_component(bank, destination, 1, r.half(8), r)


def transform(bank, displacements, sign, width, paired=True):
    """Disjoint bit-support directions: the caller pays address generation."""
    require(type(sign) is int and sign in (-1, 1), "native sign")
    require(displacements and len(bank) & (len(bank) - 1) == 0, "nonempty power-of-two bank")
    support = 0
    for delta in displacements:
        require(type(delta) is int and 0 < delta < len(bank) and delta & support == 0,
                "disjoint nonzero axis supports")
        support |= delta
    r = Registers(width, 9 if paired and len(displacements) >= 2 else 5)
    layer = 0
    while layer < len(displacements):
        first = displacements[layer]
        if paired and layer + 1 < len(displacements):
            second = displacements[layer + 1]
            for a in range(len(bank)):
                b, c, d = a ^ first, a ^ second, a ^ first ^ second
                if a == min(a, b, c, d):
                    quad(bank, a, b, c, d, sign, r)
            layer += 2
        else:
            for a in range(len(bank)):
                b = a ^ first
                if a < b:
                    pair(bank, a, b, sign, r)
            layer += 1
    r.close()
    require(all(x == 0 for x in r.values), "scalar scratch zero return")
    return r.counts


def expected(depth, size, paired):
    blocks = (depth + 1) // 2 if paired else depth
    return Counter(add=4 * blocks * size, halve=2 * blocks * size,
                   array_read=4 * blocks * size, array_write=2 * blocks * size,
                   clear=9 if paired and depth >= 2 else 5)
