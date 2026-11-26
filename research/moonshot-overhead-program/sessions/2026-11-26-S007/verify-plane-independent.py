#!/usr/bin/env python3
"""Independent end-to-end finite check of S007 root trace-plane evaluation and recovery."""
from pathlib import Path
from collections import Counter
from functools import reduce
from itertools import product
from operator import xor
from math import gcd
from random import Random
import json
import runpy

AR = runpy.run_path(str(Path(__file__).with_name('verify-fibre-join.py')))
RR = runpy.run_path(str(Path(__file__).with_name('verify-trace-rader.py')))
poly_div = AR['divmod_binary']
poly_mul = AR['xor_product']


def xsum(values):
    return reduce(xor, values, 0)


class Field:
    """Log tables only accelerate the oracle; construction uses literal binary reduction."""
    def __init__(self, b):
        self.b, self.size = b, 1 << b
        self.mod = AR['field_poly'](b)
        factors = RR['prime_divisors'](self.size - 1)
        self.gen = next(g for g in range(1, self.size)
                        if all(AR['power'](g, (self.size - 1) // p, self.mod) != 1 for p in factors))
        self.exp = [1]
        self.log = [None] * self.size
        for _ in range(1, self.size - 1):
            self.exp.append(AR['mul'](self.exp[-1], self.gen, self.mod))
        for i, v in enumerate(self.exp):
            self.log[v] = i
        assert all(v is not None for v in self.log[1:])

    def mul(self, x, y):
        if not x or not y:
            return 0
        return self.exp[(self.log[x] + self.log[y]) % (self.size - 1)]

    def pow(self, x, k):
        if not x:
            return int(k == 0)
        return self.exp[(self.log[x] * k) % (self.size - 1)]

    def eval(self, coeffs, x):
        val = 0
        for coeff in reversed(coeffs):
            val = self.mul(val, x) ^ coeff
        return val

    def binary_eval(self, bits, x):
        return self.eval([(bits >> j) & 1 for j in range(bits.bit_length())], x)

    def polynomial_product(self, p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, v in enumerate(p):
            for j, w in enumerate(q):
                out[i + j] ^= self.mul(v, w)
        return out

    def orbit(self, x):
        points = [x]
        t = self.mul(x, x)
        while t != x:
            points.append(t)
            t = self.mul(t, t)
        return points


def add_coeff(table, key, value):
    result = table.get(key, 0) ^ value
    if result:
        table[key] = result
    else:
        table.pop(key, None)


def shear(field, p, axis, scalar, cross):
    out = {}
    for indices, val in p.items():
        exponent = indices[axis]
        sub = exponent
        while True:
            dest = list(indices)
            dest[axis] = sub
            dest[1 - axis] += (exponent - sub) if cross else 0
            add_coeff(out, tuple(dest), field.mul(val, field.pow(scalar, exponent - sub)))
            if not sub:
                break
            sub = (sub - 1) & exponent
    return out


def scale(field, p, x, y):
    return {(i, j): field.mul(v, field.mul(field.pow(x, i), field.pow(y, j)))
            for (i, j), v in p.items()}


def affine(ctx, p, t, inv=False):
    field, a, v, w = ctx.field, ctx.a, ctx.v, ctx.w
    va, wa = field.pow(v, a), field.pow(w, a)
    upper = field.mul(field.pow(v, -1), w)
    lower = field.mul(field.pow(v, -1), va)
    diag = wa ^ field.mul(lower, w)
    assert diag
    if inv:
        p = shear(field, p, 0, upper, True)
        p = scale(field, p, field.pow(v, -1), field.pow(diag, -1))
        p = shear(field, p, 1, lower, True)
        p = shear(field, p, 0, t, False)
        p = shear(field, p, 1, field.pow(t, a), False)
    else:
        p = shear(field, p, 0, t, False)
        p = shear(field, p, 1, field.pow(t, a), False)
        p = shear(field, p, 1, lower, True)
        p = scale(field, p, v, diag)
        p = shear(field, p, 0, upper, True)
    assert all(i + j <= 2 * a - 2 for i, j in p)
    return p


def chirp(ctx, coeffs, inv=False):
    """Ordinary binary product at stride 2b-1, cyclic folding, field reduction."""
    field, m = ctx.field, ctx.a - 1
    root = field.pow(ctx.xi, -1 if inv else 1)
    half = pow(2, -1, m)
    if inv:
        zero, xs = coeffs[0], coeffs[1:]
    else:
        zero, xs = coeffs[0], [coeffs[0] ^ coeffs[-1], *coeffs[1:-1]]
    phases = [field.pow(root, (i*i*half) % m) for i in range(m)]
    stride = 2 * field.b - 1
    kernel = 0
    val = 0
    for i in range(m):
        kernel |= field.pow(phases[i], -1) << (stride * i)
        val |= field.mul(xs[i], phases[i]) << (stride * i)
    prod_bits = poly_mul(kernel, val)
    ys = [0] * m
    mask = (1 << stride) - 1
    for i in range(2*m - 1):
        raw = (prod_bits >> (stride * i)) & mask
        ys[i % m] ^= poly_div(raw, field.mod)[1]
    ys = [field.mul(phases[i], y) for i, y in enumerate(ys)]
    if inv:
        return [zero, *ys[1:], zero ^ ys[0]]
    return [zero, *ys]


def grid_fft(ctx, mat, inv=False):
    rows = [chirp(ctx, row, inv) for row in mat]
    cols = [chirp(ctx, list(col), inv) for col in zip(*rows)]
    return [list(row) for row in zip(*cols)]


def plane_forward(ctx, t, original):
    a = ctx.a
    p = {(i, j): original[i + a*j] for j in range(a) for i in range(a) if original[i + a*j]}
    p = affine(ctx, p, t)
    folded = [[0] * a for _ in range(a)]
    for (i, j), value in p.items():
        folded[i if i < a else i-a+1][j if j < a else j-a+1] ^= value
    return grid_fft(ctx, folded)


def plane_inverse(ctx, t, vals):
    a, h, field = ctx.a, ctx.h, ctx.field
    interp = grid_fft(ctx, vals, True)
    p = {(i,j):interp[i][j] for i, j in product(range(a), repeat=2) if interp[i][j]}
    q = affine(ctx, p, t, True)
    raw = [0] * (2*h-2*a+1)
    for (i,j), v in q.items():
        raw[i+a*j] ^= v
    result = (raw + [0]*h)[:h]
    for i, w in enumerate(raw[h:]):
        assert i+a < h
        result[i+a] ^= w
        result[i+1] ^= w
        result[i] ^= field.mul(t, w)
    return result


def literal_plane_remainder(ctx, f, t):
    # Ordinary univariate long division in K[X] against X^h+X^a+X+t.
    arr = [(f >> j) & 1 for j in range(max(ctx.h, f.bit_length()))]
    for j in reversed(range(ctx.h, len(arr))):
        lead = arr[j]
        k = j - ctx.h
        arr[k+ctx.a] ^= lead
        arr[k+1] ^= lead
        arr[k] ^= ctx.field.mul(t, lead)
    return arr[:ctx.h]


def mono_remainder(field, x, y, h):
    orbit = field.orbit(x)
    e = len(orbit)
    # h'(X), evaluated independently at x by Horner.
    derivative = sum(((h >> j) & 1) << (j-1) for j in range(1,e+1,2))
    denom = field.binary_eval(derivative, x)
    assert denom
    w = field.mul(y, field.pow(denom, -1))
    coeff = w
    level = []
    for z in orbit:
        level.append(([z,1], [coeff]))
        coeff = field.mul(coeff, coeff)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            if i+1 == len(level):
                nxt.append(level[i])
                continue
            p, a = level[i]
            q, b = level[i+1]
            aa, bb = field.polynomial_product(a,q), field.polynomial_product(b,p)
            nxt.append((field.polynomial_product(p,q), [x^y for x,y in zip(aa,bb)]))
        level = nxt
    hp, remainder = level[0]
    assert all(bit in (0,1) for bit in hp+remainder)
    assert sum(bit<<i for i,bit in enumerate(hp)) == h
    return sum(bit<<i for i,bit in enumerate(remainder))


class Context:
    def __init__(self,c):
        self.c, self.a, self.h = c, 1<<c, 1<<(2*c)
        self.q, self.field = 1<<(3*c), Field(3*c)
        field, a, h = self.field, self.a, self.h
        self.xi = field.pow(field.gen, (self.q-1)//(a-1))
        self.points = [0] + [field.pow(self.xi, i) for i in range(a-1)]
        assert len(self.points) == len(set(self.points)) == a
        kernel = [x for x in range(self.q) if x ^ field.pow(x,a) ^ field.pow(x,h) == 0]
        assert len(kernel) == h
        self.v = next(x for x in kernel if x)
        line = {field.mul(y,self.v) for y in self.points}
        self.w = next(x for x in kernel if x not in line)
        self.planes = {}
        all_seen = set()
        gamma = AR['normal'](3*c)
        sub = [gamma[i] ^ gamma[i+c] ^ gamma[i+2*c] for i in range(c)]
        actual_anchors = []
        self.twisted = 0
        for word in range(a//2):
            rotations = AR['fixed_word_orbit'](word, c)
            canonical = min(min(w, w ^ (a-1)) for w in rotations)
            if word != canonical:
                continue
            low = AR['from_word'](word, sub)
            actual_anchors.extend([low, low ^ 1])
            self.twisted += int((low ^ 1) in field.orbit(low))
        ordinary = sum(1 << gcd(c,j) for j in range(c)) // c
        paid = sum((1 << gcd(c,j)) * (1 + int((c // gcd(c,j))%2 == 0)) for j in range(c)) // c
        assert len(actual_anchors) == len(set(actual_anchors)) == paid == ordinary + self.twisted
        if c == 2:
            assert (ordinary, paid) == (3, 4)
        self.ordinary_count = ordinary
        for t in actual_anchors:
            grid = [[t ^ field.mul(self.v,y) ^ field.mul(self.w,z) for z in self.points]
                    for y in self.points]
            flat = [x for row in grid for x in row]
            assert len(set(flat)) == h and not set(flat) & all_seen
            assert all(x ^ field.pow(x,a) ^ field.pow(x,h) == t for x in flat)
            all_seen.update(flat)
            self.planes[t] = grid
        self.moduli = AR['fs_order'](3*c)
        self.by_point = {}
        self.by_poly = {}
        for x in sorted(all_seen):
            if x in self.by_point:
                continue
            orbit = field.orbit(x)
            hp = [1]
            for r in orbit:
                hp = field.polynomial_product(hp,[r,1])
            assert set(hp) <= {0,1}
            poly = sum(bit<<i for i,bit in enumerate(hp))
            self.by_poly[poly] = x
            for r in orbit:
                self.by_point[r] = poly
        assert set(self.moduli) == set(self.by_poly)
        assert len(self.by_point) == self.q
        self.idems = RR['crt_idempotents'](self.moduli, self.q)

    def canonical_residues(self, plane_values):
        out = {}
        for t, grid in self.planes.items():
            for i,j in product(range(self.a),repeat=2):
                x = grid[i][j]
                poly = self.by_point[x]
                if x != self.by_poly[poly]:
                    continue
                out[poly] = mono_remainder(self.field,x,plane_values[t][i][j],poly)
        assert set(out) == set(self.moduli)
        return [out[poly] for poly in self.moduli]

    def planes_from_residues(self, residues):
        by_mod = dict(zip(self.moduli,residues))
        return {t:[[self.field.binary_eval(by_mod[self.by_point[x]],x) for x in row] for row in grid]
                for t,grid in self.planes.items()}

    def join_scalar_planes(self, p):
        tr = (1<<self.h) | (1<<self.a) | 2
        all_t = {}
        for t, row in p.items():
            curr = row
            for z in self.field.orbit(t):
                if z in all_t:
                    assert all_t[z] == curr
                all_t[z] = curr
                curr = [self.field.mul(v,v) for v in curr]
            assert curr == row
        digits = [0] * self.a
        for i in range(self.h):
            coeffs = chirp(self,[all_t[z][i] for z in self.points],True)
            assert set(coeffs) <= {0,1}
            for j,bit in enumerate(coeffs):
                digits[j] |= bit<<i
        f = 0
        for d in reversed(digits):
            f = poly_mul(f,tr) ^ d
        return f


def main():
    rng = Random(0xAF41)
    count = Counter()
    for c in range(1,5):
        ctx = Context(c)
        field, a = ctx.field, ctx.a
        for t,grid in ctx.planes.items():
            arbitrary = [[rng.randrange(ctx.q) for _ in row] for row in grid]
            coeffs = plane_inverse(ctx, t, arbitrary)
            assert plane_forward(ctx,t,coeffs) == arbitrary
            assert all(field.eval(coeffs,x) == arbitrary[i][j]
                       for i,row in enumerate(grid) for j,x in enumerate(row))
            count['arbitrary_plane_grid_bits'] += ctx.h * 3*c
            count['univariate_Horner_on_arbitrary_grids'] += ctx.h
        inputs = [rng.getrandbits(ctx.q), (1<<(ctx.q-1))|1]
        if c<=2:
            inputs.extend(1<<i for i in range(ctx.q))
        for f in inputs:
            rems = {t:literal_plane_remainder(ctx,f,t) for t in ctx.planes}
            grids = {t:plane_forward(ctx,t,row) for t,row in rems.items()}
            for t, grid in ctx.planes.items():
                assert plane_inverse(ctx,t,grids[t]) == rems[t]
                for i,j in product(range(a),repeat=2):
                    x=grid[i][j]
                    direct=field.binary_eval(poly_div(f,ctx.by_point[x])[1],x)
                    assert direct == grids[t][i][j]
                    count['field_evaluations_from_literal_root_remainders'] += 1
            assert ctx.canonical_residues(grids) == [poly_div(f,p)[1] for p in ctx.moduli]
            assert ctx.join_scalar_planes(rems) == f
            count['forward_complete_true_FS1_root_polynomials'] += 1
        independent = [rng.getrandbits(h.bit_length()-1) for h in ctx.moduli]
        grids = ctx.planes_from_residues(independent)
        rems = {t:plane_inverse(ctx,t,grid) for t,grid in grids.items()}
        oracle = poly_div(xsum(poly_mul(e,u) for e,u in zip(ctx.idems,independent)),(1<<ctx.q)|2)[1]
        assert all(row == literal_plane_remainder(ctx,oracle,t) for t,row in rems.items())
        assert ctx.join_scalar_planes(rems) == oracle
        assert ctx.canonical_residues({t:plane_forward(ctx,t,row) for t,row in rems.items()}) == independent
        count['arbitrary_inverse_root_directory_bits'] += ctx.q
        count['arbitrary_inverse_root_FS1_factors'] += len(independent)
        count['proper_field_orbit_FS1_factors'] += sum(h.bit_length()-1<3*c for h in ctx.moduli)
        count['actual_S006_planes'] += len(ctx.planes)
        count['ordinary_Frobenius_plane_orbits'] += ctx.ordinary_count
        count['twisted_quotient_representatives'] += ctx.twisted
    print(json.dumps({'seed':'0xaf41','c':[1,2,3,4],'b':[3,6,9,12],'counts':dict(sorted(count.items()))},indent=2))


if __name__ == '__main__':
    main()
