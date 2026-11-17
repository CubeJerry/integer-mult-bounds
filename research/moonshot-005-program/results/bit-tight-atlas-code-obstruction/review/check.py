#!/usr/bin/env python3
"""Check the atlas obstruction directly from native coordinates and 3x3 Gram minors."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from ordered_gauge import certificate as ordered_certificate


def require(test, reason):
    if not test:
        raise AssertionError(reason)


def distribution(values):
    return dict(sorted(Counter(values).items()))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            col = row.bit_length() - 1
            if col not in pivots:
                pivots[col] = row
                break
            row ^= pivots[col]
    return len(pivots)


def bitmask(roles):
    return sum(1 << j for j in roles)


def multiply(x, y):
    value = 0
    while y:
        if y & 1:
            value ^= x
        y >>= 1
        x <<= 1
        if x & 32:
            x ^= 0b100101
    return value


def cardinal_polynomial(nodes):
    polynomial = [1]
    for x in nodes:
        result = [0] * (len(polynomial) + 1)
        for exponent, coefficient in enumerate(polynomial):
            result[exponent] ^= multiply(coefficient, x)
            result[exponent + 1] ^= coefficient
        polynomial = result
    return polynomial


def controls():
    require(all(len({multiply(a, b) for b in range(32)}) == 32 for a in range(1,32)), 'GF(32)')
    s = set(range(16))
    t = (s - {7}) | {27}
    require(cardinal_polynomial(s - {7}) == cardinal_polynomial(t - {27}), 'changed removed node')
    require(cardinal_polynomial(s - {6}) != cardinal_polynomial(t - {6}), 'changed retained node')
    a = cardinal_polynomial(s - {3})
    b = cardinal_polynomial(s - {10})
    require(a != b and a[-1] == b[-1] == 1, 'different removed node at same 16-set')
    scaled = [multiply(7, c) for c in a]
    inv = next(c for c in range(1,32) if multiply(7, c) == 1)
    require([multiply(inv, c) for c in scaled] == a, 'row multiplier changes only normalization')
    # An invertible donor-specific input basis can transport b to a: because a,b
    # are monic, their difference has top coefficient zero. I+(a-b)e_top^T
    # is an involution in characteristic two and sends b to a.
    transport = lambda p: [x ^ multiply(p[-1], y ^ z) for x,y,z in zip(p,a,b)]
    require(transport(b) == a and transport(transport(b)) == b, 'input-gauge control')
    return ['one removed node differs', 'one retained node differs', 'distinct removed nodes with identical 16-set',
            'nonzero row multiplier', 'donor-specific invertible input transport']


def audit(native, cpp):
    data = native.read_bytes()
    require(hashlib.sha256(data).hexdigest() == '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e', 'native source')
    roots = list(map(tuple, json.loads(data)['native_roots']))
    require(len(set(roots)) == len(roots) == 111, 'native projective roots')
    supports = {tuple(i for i,x in enumerate(row) if x) for row in roots if sum(x != 0 for x in row) == 4}
    full = set(roots)
    for supp in supports:
        for tail in product((-1,1), repeat=3):
            r = [0] * 8
            for i, sign in zip(supp, (1,*tail)):
                r[i] = sign
            full.add(tuple(r))
    roots.extend(sorted(full - set(roots)))
    require(len(roots) == 120 and all(dot(r,r) == 4 for r in roots), 'parent root completion')
    require(all(next(x for x in r if x) > 0 for r in roots), 'canonical projectivization')
    d = [[dot(r,s) for s in roots] for r in roots]
    require({abs(d[i][j]) for i,j in combinations(range(120),2)} == {0,2}, 'native angular separation')
    planes = []
    multiplicity = Counter()
    for i,j,k in combinations(range(120),3):
        x,y,z = d[i][j],d[i][k],d[j][k]
        determinant = 64 + 2*x*y*z - 4*(x*x+y*y+z*z)
        if determinant == 0:
            require(abs(x) == abs(y) == abs(z) == 2, 'A2 Gram triple')
            planes.append((i,j,k))
            multiplicity.update(combinations((i,j,k),2))
    require(len(planes) == 1120 and set(multiplicity.values()) == {1}, 'unique A2 through a nonorthogonal pair')
    require(set(multiplicity) == {(i,j) for i,j in combinations(range(120),2) if d[i][j] != 0}, 'exact edge completion')
    active = [h for h in planes if h[0] < 111]
    N = [bitmask(j for j in range(111) if d[i][j] == 0) for i in range(111)]
    canonical = [n | (1 << i) for i,n in enumerate(N)]
    require(binary_rank(canonical) == 9, 'whole canonical bank')
    complement_ranks = distribution(binary_rank(word & ~n for word in canonical) for n in N)
    require(complement_ranks == {9:111}, 'outside-N inputs can cancel the full canonical bank')
    full_neighbours = [bitmask(j for j in range(120) if d[i][j] == 0) for i in range(111)]
    H = [bitmask(h) for h in active]
    H_perp = [bitmask(i for i,t in enumerate(full_neighbours) if h & t == h) for h in H]
    overlap = distribution((w & n).bit_count() for w in H_perp for n in N)
    require(min(overlap) > 0, 'a common receiver for every active plane and every donor')
    donor_pencils = [[k for k,h in enumerate(H) if h & (1 << j)] for j in range(111)]
    require(all(len(p) == 28 for p in donor_pencils), 'native full pencil')
    require(all(sum(bool(H_perp[k] & (1 << i)) for k in p) == 16
                for j,p in enumerate(donor_pencils) for i in range(111) if N[i] & (1 << j)), 'local 16-of-28 restrictions')
    with tempfile.TemporaryDirectory() as scratch:
        binary = Path(scratch)/'seed_closure'
        subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(binary)], check=True)
        rows = ''.join(' '.join(map(str,r)) + '\n' for r in roots[:111])
        output = subprocess.check_output([str(binary)], text=True, input=rows)
    seed_line, degree_line, rounds_line = [list(map(int,line.split())) for line in output.splitlines()]
    degrees = dict(zip(degree_line[::2],degree_line[1::2]))
    rounds = dict(zip(rounds_line[::2],rounds_line[1::2]))
    require(degrees == distribution(n.bit_count() for n in N), 'independent graph degrees')
    require(seed_line == [185428,6470] and sum(rounds.values()) == 185428 and max(rounds) == 3, 'all closure seeds')
    degree = min(degrees)
    colors = 28
    min_planes = (111 + 2) // 3
    large = (len(active) - colors * min_planes) // (degree - min_planes)
    require(len(active) == 1119 and degree == 55 and colors - large > 16, 'global contradiction')
    return {'native_sha256':hashlib.sha256(data).hexdigest(), 'A2':len(planes),
            'canonical_rank_restricted_outside_N':complement_ranks, 'ordered_GF64_gauge':ordered_certificate(H,H_perp),
            'active_plane_sizes':distribution(sum(j < 111 for j in h) for h in active),
            'native_receiver_degrees':degrees, 'seed_pair_first_full_rounds':rounds,
            'inert_singleton_seeds':seed_line[1], 'joint_plane_donor_normal_histogram':overlap,
            'color_classes':colors,'min_planes_per_color':min_planes,'max_large_colors':large,
            'universally_required_colors':colors-large,'available_receiver_colors':16,
            'independent_GF32_controls':controls()}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('native', type=Path)
    a=p.parse_args()
    print(json.dumps(audit(a.native,Path(__file__).with_name('seed_closure.cpp')),indent=2))
