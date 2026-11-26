"""Exact two-way checks of the relative-trace radix and its Pascal reduction."""
from collections import Counter
from math import isqrt
from random import Random
import json


def divide(f, divisor):
    """Ordinary binary polynomial long division, high coefficient first."""
    quotient = 0
    while f.bit_length() >= divisor.bit_length():
        degree = f.bit_length() - divisor.bit_length()
        quotient ^= 1 << degree
        f ^= divisor << degree
    return quotient, f


def digits(f, divisor, count):
    out = []
    for _ in range(count):
        f, remainder = divide(f, divisor)
        out.append(remainder)
    assert f == 0
    return out


def horner(rows, shifts):
    value = 0
    for row in reversed(rows):
        previous = value
        value = row
        for shift in shifts:
            value ^= previous << shift
    return value


def pack(rows, width):
    return sum(value << (width*j) for j, value in enumerate(rows))


def unpack(value, width, count):
    mask = (1 << width) - 1
    return [(value >> (j*width)) & mask for j in range(count)]


def rotate(word, distance, width):
    distance %= width
    return ((word << distance) | (word >> (width-distance))) & ((1 << width)-1)


def pascal(rows):
    out = rows.copy()
    step = 1
    while step < len(out):
        for start in range(0, len(out), 2*step):
            for j in range(step):
                out[start+j] ^= out[start+j+step]
        step *= 2
    return out


def shear(rows, slope, width):
    winding = [rotate(row, j*slope, width) for j, row in enumerate(rows)]
    transformed = pascal(winding)
    return [rotate(row, -i*slope, width) for i, row in enumerate(transformed)]


def convert(rows, forward):
    """Index j*h+k; forward maps ordinary coefficients to trace digits."""
    axis = len(rows)
    h = axis**2
    wide = shear(shear(rows, 1, 2*h), axis, 2*h)
    mask = (1 << h) - 1
    out = []
    previous = 0
    for word in wide:
        high = word >> h
        result = (word & mask) ^ previous
        if forward:
            result ^= (high << axis) ^ (high << 1)
        assert result.bit_length() <= h
        out.append(result)
        previous = high
    assert previous == 0
    return out


def source_prefix(f, axis):
    c = axis.bit_length() - 1
    depth = min(c-1, isqrt(3*c))
    rows = [f]
    divisors = []
    for level in range(depth):
        power = 1 << (c-2-level)
        divisor = 0
        for e in (1, 2, axis, 2*axis, axis**2, 2*axis**2):
            divisor ^= 1 << (e*power)
        next_rows = []
        for row in rows:
            quotient, remainder = divide(row, divisor)
            next_rows.extend([remainder, quotient])
        rows = next_rows
        divisors.append(divisor)
    return rows, divisors


def undo_source_prefix(rows, divisors):
    for divisor in reversed(divisors):
        shifts = []
        terms = divisor
        while terms:
            lowest = terms & -terms
            shifts.append(lowest.bit_length()-1)
            terms ^= lowest
        rows = [horner(rows[i:i+2], shifts) for i in range(0,len(rows),2)]
    return rows[0]


def omega(word):
    """Multiply by w in the basis 1,w with w²=w+1, across all packed bits."""
    x, y = word
    return y, x ^ y


def scale(rows, x_power, z_power):
    """Substitute w^x_power X and w^z_power Z in a GF(4) rectangle."""
    out = []
    for j, word in enumerate(rows):
        low, high = word
        powers = [word, omega(word), omega(omega(word))]
        xs, ys = 0, 0
        for residue in range(3):
            mask = sum(1 << k for k in range(residue,(low | high).bit_length(),3))
            u, v = powers[(residue*x_power + j*z_power) % 3]
            xs ^= u & mask
            ys ^= v & mask
        out.append((xs,ys))
    return out


def actual_synthesis4(rows):
    axis = len(rows)
    def component(part):
        f = horner([row[part] for row in rows], [axis**2,axis,1])
        return unpack(f,axis**2,axis)
    return list(zip(component(0),component(1)))


def recovered_pascal(rows, c):
    axis = 1 << c
    assert c % 2 and len(rows) <= axis//8
    guarded = [(value << (axis-j),0) for j,value in enumerate(rows)]
    padded = guarded + [(0,0)]*(axis-len(rows))
    def conjugated(data, x, z):
        return scale(actual_synthesis4(scale(data,x,z)),-x,-z)
    first = conjugated(padded,0,1)
    second = conjugated(first,1,1+axis)
    assert all(y == 0 for x,y in second)
    assert all(word == (0,0) for word in second[len(rows):])
    out = []
    for i,(word,_) in enumerate(second[:len(rows)]):
        assert word % (1 << (axis-i)) == 0
        out.append(word >> (axis-i))
    return out


def main():
    rng = Random(7261126)
    counts = Counter()
    for c in range(1,7):
        axis = 1 << c
        h = axis**2
        n = axis*h
        shifts = [h,axis,1]
        t = sum(1 << j for j in shifts)
        inputs = [0,1,1 << (n-1),(1 << n)-1,rng.getrandbits(n),rng.getrandbits(n)]
        for f in inputs:
            ordinary = unpack(f,h,axis)
            out = convert(ordinary,True)
            assert horner(out,shifts) == f and convert(out,False) == ordinary
            counts['forward_first'] += 1
            if c <= 4:
                assert digits(f,t,axis) == out
                counts['ordinary_long_divisions'] += axis
                assert undo_source_prefix(*source_prefix(f,axis)) == f
                counts['source_prefix_roundtrips'] += 1
            independent = unpack(rng.getrandbits(n),h,axis)
            joined = convert(independent,False)
            assert pack(joined,h) == horner(independent,shifts)
            assert convert(joined,True) == independent
            counts['inverse_first'] += 1
        if c in (5,6):
            # The paid prefix leaves unexpanded S levels in these two cases.
            rows, divisors = source_prefix(0,axis)
            width = n // len(rows)
            assert len(divisors) < c-1
            independent = [sum(1 << j for j in rng.sample(range(width), 4))
                           for _ in rows]
            value = undo_source_prefix(independent,divisors)
            assert source_prefix(value,axis)[0] == independent
            trace = convert(unpack(value,h,axis),True)
            value_back = pack(convert(trace,False),h)
            assert source_prefix(value_back,axis)[0] == independent
            counts['nonterminal_source_prefix_independent_blocks'] += len(rows)
            counts['nonterminal_source_prefix_compositions'] += 1
        if c <= 3:
            for bit in range(n):
                basis = unpack(1 << bit,h,axis)
                assert convert(basis,True) == digits(1 << bit,t,axis)
                assert pack(convert(basis,False),h) == horner(basis,shifts)
                counts['basis_bits_both_ways'] += 1
    for c,width,lanes,samples in [(3,1,7,8),(5,4,41,18),(7,16,73,6)]:
        for _ in range(samples):
            rows = [rng.getrandbits(lanes) for _ in range(width)]
            target = [0]*width
            for i in range(width):
                for j,x in enumerate(rows):
                    if i & j == i:
                        target[i] ^= x
            assert recovered_pascal(rows,c) == target
            counts['converse_independent_lane_bits'] += lanes*width
            counts['converse_paired_syntheses_GF4'] += 1
    print(json.dumps(dict(sorted(counts.items())), indent=2))


if __name__ == '__main__':
    main()
