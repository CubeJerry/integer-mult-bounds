#!/usr/bin/env python3
"""Replay the actual occupied Fourier circuit as position, diagonal, and one-bit-H slots."""
from __future__ import annotations

import argparse
import cmath
import math
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from random import Random


HALF = 1 / math.sqrt(2)
PHI = math.sin(math.pi / 258)


def unit(num, den):
    return cmath.exp(2j * math.pi * (num % den) / den)


def inv_permutation(index):
    inverse = [None] * len(index)
    for i, j in enumerate(index):
        assert 0 <= j < len(index) and inverse[j] is None
        inverse[j] = i
    assert all(i is not None for i in inverse)
    return tuple(inverse)


@dataclass(frozen=True)
class Op:
    # Permutation payload is a gather map, output -> input. An edge is (ordered i,j,kind,z).
    kind: str
    payload: tuple


def inverse_op(op):
    if op.kind == "P":
        return Op("P", inv_permutation(op.payload))
    if op.kind == "D":
        return Op("D", tuple(x.conjugate() for x in op.payload))
    assert op.kind == "E"
    return Op("E", tuple((i, j, kind, z.conjugate()) for i, j, kind, z in op.payload))


def inverse_word(operations):
    return tuple(inverse_op(op) for op in reversed(operations))


@lru_cache(maxsize=None)
def raw_axis(a):
    r = 1 << ((2 * a - 2).bit_length())
    n = 2 * r

    def diagonal(entries):
        return Op("D", tuple(entries) + (1.,) * (n - len(entries)))

    def edges(entries):
        return Op("E", tuple(entries))

    q = r.bit_length() - 1
    reverse = [int(format(i, f"0{q}b")[::-1], 2) for i in range(r)]
    fft = [Op("P", tuple(reverse) + tuple(range(r, 2 * r)))]
    for stage in range(1, q + 1):
        step = 1 << stage
        half = step // 2
        fft.append(diagonal([unit(i % half, step) if i % step >= half else 1. for i in range(r)]))
        fft.append(edges((i, i + half, "H", 0j) for i in range(r) if i % step < half))
    roots = []
    for xi in range(r):
        lam = sum(unit(-h*h*r + 2*a*xi*h, 2*a*r) for h in range(1-a, a)) / math.sqrt(a)
        z = PHI * lam
        assert abs(z) < 0.5
        roots.append(z)
    lifted_pairs = edges((xi, r + xi, "L", z) for xi, z in enumerate(roots))
    chirp = diagonal([unit(j*j, 2*a) for j in range(a)])
    v = (chirp, *fft, lifted_pairs, *inverse_word(fft), chirp)
    first = diagonal([-1.] * a)
    second = diagonal([1.] * a + [-1.] * (n-a))
    # Chronological operations for [(V(2P-I)V*)(I-2P)]^64 V.
    b = v + ((first,) + inverse_word(v) + (second,) + v) * 64
    d1 = diagonal([unit(j*j+(a % 2)*j, 2*a) for j in range(a)])
    d3 = diagonal([unit(j*j-(a % 2)*j, 2*a) for j in range(a)])
    d2 = diagonal([sum(unit(-j*j-(a % 2)*j+2*h*j, 2*a) for j in range(a))
                   / math.sqrt(a) for h in range(a)])
    return (d3, *b, d2, *inverse_word(b), d1), n


@lru_cache(maxsize=None)
def pair_phases(kind, z):
    if kind == "H":
        return ((1., 1.), (1., 1.), (1., 1.))
    if kind == "I":
        return ((1., -1j), (unit(1, 8), unit(-1, 8)), (1., -1j))
    assert kind == "L"
    v = math.sqrt(1 - abs(z)**2)
    q00, q01, q10 = (z+v)*HALF, (v-z.conjugate())*HALF, (z-v)*HALF
    c, s = abs(q00), abs(q01)
    g = q00/c
    din = (1., q01/(1j*s*g))
    dmid = (c+1j*s, c-1j*s)
    dout = (g, q10/(1j*s))
    return din, dmid, dout


def fibres(shape, axis):
    stride = math.prod(shape[:axis])
    width = shape[axis]
    return tuple(tuple(start+offset+j*stride for j in range(width))
                 for start in range(0, math.prod(shape), stride*width) for offset in range(stride))


def assign(fibre_list, batch, a, size):
    count = len(fibre_list) // 8
    first = batch * count
    donors = [i for f, fibre in enumerate(fibre_list) if not first <= f < first+count for i in fibre]
    tuples = []
    for j, fibre in enumerate(fibre_list[first:first+count]):
        lo = j * (size-a)
        tuples.append(tuple(fibre[:a]) + tuple(donors[lo:lo+size-a]))
    all_sites = [i for sites in tuples for i in sites]
    assert len(all_sites) == len(set(all_sites)) == count*size
    return tuples


ONE_H = Op("W", ())


def lower(raw, tuples, volume):
    if raw.kind == "D":
        full = [1.] * volume
        for sites in tuples:
            for j, coef in zip(sites, raw.payload):
                full[j] = coef
        return (Op("D", tuple(full)),)
    if raw.kind == "P":
        gather = list(range(volume))
        for sites in tuples:
            for dst, src in enumerate(raw.payload):
                gather[sites[dst]] = sites[src]
        inv_permutation(gather)
        return (Op("P", tuple(gather)),)
    assert raw.kind == "E"
    required = [(sites[i], sites[j], kind, z) for sites in tuples for i, j, kind, z in raw.payload]
    occupied = {i for a, b, _, _ in required for i in (a, b)}
    assert len(occupied) == 2*len(required)
    unused = iter([j for j in range(volume) if j not in occupied])
    required.extend((i, next(unused), "I", 0j) for i in unused)
    required.sort(key=lambda edge: edge[0])
    assert len(required) == volume // 2
    route = tuple(i for a, b, _, _ in required for i in (a, b))
    inv = inv_permutation(route)
    din, mid, dout = (list() for _ in range(3))
    for i, j, kind, z in required:
        for dest, two in zip((din, mid, dout), pair_phases(kind, z)):
            dest.extend(two)
    return (Op("P", route), Op("D", tuple(din)), ONE_H, Op("D", tuple(mid)), ONE_H,
            Op("D", tuple(dout)), ONE_H, Op("P", inv))


def block_schedule(axes, selected_axes=None, selected_batches=tuple(range(8)), adjoint=False):
    assert 4 <= len(axes) <= 7
    shape = tuple(1 << ((a-1).bit_length()) for a in axes)
    volume = math.prod(shape)
    order = list(range(len(axes))) if selected_axes is None else list(selected_axes)
    batches = list(selected_batches)
    if adjoint:
        order.reverse()
        batches.reverse()
    for axis in order:
        a = axes[axis]
        template, size = raw_axis(a)
        if adjoint:
            template = inverse_word(template)
        fibre_list = fibres(shape, axis)
        assert len(fibre_list) >= 8 and (len(fibre_list) % 8) == 0
        for batch in batches:
            tuples = assign(fibre_list, batch, a, size)
            memo = {}
            for raw in template:
                if raw not in memo:
                    memo[raw] = lower(raw, tuples, volume)
                yield from memo[raw]


def synchronize(*schedules):
    cursors = list(map(iter, schedules))
    current = [next(s, None) for s in cursors]
    while any(x is not None for x in current):
        for kind in ("P", "D", "W"):
            slot = [x if x is not None and x.kind == kind else None for x in current]
            if any(x is not None for x in slot):
                yield kind, slot
                for i, x in enumerate(slot):
                    if x is not None:
                        current[i] = next(cursors[i], None)


def local_gate(op, vector):
    if op.kind == "P":
        return [vector[i] for i in op.payload]
    if op.kind == "D":
        return [x*z for x, z in zip(vector, op.payload)]
    out = [0j] * len(vector)
    for i in range(0, len(vector), 2):
        a, b = vector[i], vector[i+1]
        out[i], out[i+1] = (a+b)*HALF, (a-b)*HALF
    return out


def global_gate(kind, slots, vector, d0, d1):
    s0, s1 = slots
    if kind == "P":
        a = s0.payload if s0 else range(d0)
        b = s1.payload if s1 else range(d1)
        return [vector[j*d0+i] for j in b for i in a]
    if kind == "D":
        a = s0.payload if s0 else (1.,)*d0
        b = s1.payload if s1 else (1.,)*d1
        return [z * a[i % d0] * b[i // d0] for i, z in enumerate(vector)]
    if s0:
        vector = local_gate(ONE_H, vector)
    if s1:
        result = [0j] * (d0*d1)
        for start in range(0, d0*d1, 2*d0):
            for j in range(start, start+d0):
                a, b = vector[j], vector[j+d0]
                result[j], result[j+d0] = (a+b)*HALF, (a-b)*HALF
        vector = result
    return vector


def reference(axes, vector, axis_order=None, batches=tuple(range(8)), adjoint=False):
    shape = tuple(1 << ((a-1).bit_length()) for a in axes)
    result = list(vector)
    if axis_order is None:
        axis_order = range(len(axes))
    for i in axis_order:
        a = axes[i]
        f = fibres(shape, i)
        n = len(f) // 8
        for b in batches:
            for row in f[b*n:(b+1)*n]:
                old = [result[j] for j in row[:a]]
                sign = -1 if adjoint else 1
                target = [sum(x * unit(sign*j*h, a) for h, x in enumerate(old))/math.sqrt(a)
                          for j in range(a)]
                for j, x in zip(row, target):
                    result[j] = x
    return result


def random_vector(n):
    rand = Random(3344+n)
    return [complex(rand.uniform(-1,1), rand.uniform(-1,1)) for _ in range(n)]


def compare(a, b):
    return max(abs(x-y) for x, y in zip(a, b))


def test_local():
    axes = (3, 2, 2, 2)
    actual = initial = random_vector(32)
    counts = Counter()
    for gate in block_schedule(axes):
        actual = local_gate(gate, actual)
        counts[gate.kind] += 1
    forward = compare(actual, reference(axes, initial))
    for gate in block_schedule(axes, adjoint=True):
        actual = local_gate(gate, actual)
    backward = compare(actual, initial)
    assert max(forward, backward) < 2e-9
    return counts, forward, backward


def test_sync(extended):
    axes0, axes1 = (2, 2, 2, 2), (2, 3, 2, 2)
    d0, d1 = 16, 32
    selected = (1,)
    batches = range(8) if extended else (3,)
    actual = initial = random_vector(d0*d1)
    counts, idle = Counter(), Counter()
    g0 = block_schedule(axes0, selected, batches)
    g1 = block_schedule(axes1, selected, batches)
    for kind, slots in synchronize(g0, g1):
        actual = global_gate(kind, slots, actual, d0, d1)
        counts[kind] += 1
        idle[sum(x is None for x in slots)] += 1
    expect = list(initial)
    for j in range(d1):
        region = slice(j*d0, (j+1)*d0)
        expect[region] = reference(axes0, expect[region], selected, batches)
    for i in range(d0):
        expect[i::d0] = reference(axes1, expect[i::d0], selected, batches)
    error = compare(actual, expect)
    assert error < 2e-9 and idle[0] and idle[1]
    return counts, idle, error


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--extended", action="store_true", help="replay all eight batches on the two-block tensor")
    args = parser.parse_args()
    counts, e1, e2 = test_local()
    print("complete four-axis forward and adjoint on arbitrary occupied values:",
          "forward elementary counts", dict(counts), "forward and round-trip errors", format(e1, ".3g"), format(e2, ".3g"))
    counts, idle, e = test_sync(args.extended)
    print("512-coordinate synchronized tensor, two occupied blocks:",
          dict(counts), "slots by number of idle blocks", dict(idle), "maximum pointwise error", format(e, ".3g"))
