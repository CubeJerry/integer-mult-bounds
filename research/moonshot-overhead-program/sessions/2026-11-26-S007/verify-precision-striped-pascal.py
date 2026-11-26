#!/usr/bin/env python3
"""Lift the previously certified modulo-four tangent generators to arbitrary precision."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
from random import Random
import runpy


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def diagonal(v):
    return [[u if i == j else 0 for j in range(len(v))] for i, u in enumerate(v)]


def mapped(f, a):
    return [[f(v) for v in row] for row in a]


def embed(m, triple):
    out = eye(4)
    for i, a in enumerate(triple):
        for j, b in enumerate(triple):
            out[a][b] = m[i][j]
    return out


class Ring:
    def __init__(self, h, base):
        self.h = h
        self.m = 1 << h
        self.mask = self.m - 1
        self.base = base
        self.w = self.from_residue(6)
        for _ in range(h.bit_length()):
            error = self.add(self.add(self.mul(self.w, self.w), self.w), 1)
            derivative = self.add(self.mul(2 % self.m, self.w), 1)
            self.w = self.sub(self.w, self.mul(error, self.unit_inverse(derivative)))
        assert self.add(self.add(self.mul(self.w, self.w), self.w), 1) == 0
        assert self.reduction(self.w) == 6 and self.power(self.w, 3) == 1
        self.d3 = [[self.power(self.w, i*j) for j in range(3)] for i in range(3)]

    def coeffs(self, x):
        return [(x >> (self.h*i)) & self.mask for i in range(4)]

    def packed(self, values):
        return sum((v & self.mask) << (self.h*i) for i, v in enumerate(values))

    def from_residue(self, x):
        return self.packed((x >> i) & 1 for i in range(4))

    def reduction(self, x):
        return sum((v & 1) << i for i, v in enumerate(self.coeffs(x)))

    @lru_cache(maxsize=120000)
    def add(self, x, y):
        if not x or not y:
            return x or y
        return self.packed(a+b for a,b in zip(self.coeffs(x), self.coeffs(y)))

    @lru_cache(maxsize=120000)
    def neg(self, x):
        return self.packed(-a for a in self.coeffs(x))

    def sub(self,x,y):
        return self.add(x,self.neg(y))

    @lru_cache(maxsize=120000)
    def mul(self, x, y):
        if not x or not y:
            return 0
        if x == 1 or y == 1:
            return y if x == 1 else x
        v = [0]*7
        for i,a in enumerate(self.coeffs(x)):
            for j,b in enumerate(self.coeffs(y)):
                v[i+j] += a*b
        for k in (6,5,4):
            v[k-4] -= v[k]
            v[k-3] -= v[k]
        return self.packed(v[:4])

    def power(self, x, n):
        out = 1
        while n:
            if n & 1:
                out = self.mul(out,x)
            x = self.mul(x,x)
            n >>= 1
        return out

    def unit_inverse(self, x):
        assert self.reduction(x)
        y = self.from_residue(self.base['finv'](self.reduction(x)))
        for _ in range(self.h.bit_length()):
            y = self.mul(y,self.sub(2 % self.m,self.mul(x,y)))
        assert self.mul(x,y) == 1
        return y

    def dot(self, a, b):
        z=0
        for x,y in zip(a,b):
            z=self.add(z,self.mul(x,y))
        return z

    def mm(self, a,b):
        return [[self.dot(row,col) for col in zip(*b)] for row in a]

    def compose(self, word):
        out = eye(4)
        for m in word:
            out = self.mm(out,m)
        return out

    def digit(self, x, t):
        vs=self.coeffs(x)
        assert all(v % (1 << t) == 0 for v in vs)
        return sum(((v >> t) & 1) << i for i,v in enumerate(vs))

    def baseword(self):
        reverse = list(reversed(eye(4)))
        word = [reverse]
        for left, ds, right, triple in self.base['factors']:
            word.append(embed(mapped(self.from_residue,left),triple))
            for j in range(4):
                for m in (self.d3,diagonal([1,self.w,self.w]),self.d3,self.base['J']):
                    word.append(embed(m,triple))
                if j<3:
                    word.append(embed(mapped(self.from_residue,diagonal(ds[j])),triple))
            word.append(embed(mapped(self.from_residue,right),triple))
        return word + [reverse]

    def tangent(self, specs):
        basis=[]
        dy_inverse = [[self.mul(pow(3,-1,self.m),self.power(self.w,(-i*j)%3))
                       for j in range(3)] for i in range(3)]
        assert self.mm(self.d3,dy_inverse) == eye(3)
        for triple, exponents, position in specs:
            s=[self.power(self.w,j) for j in exponents]
            left=embed(self.mm(diagonal(s),self.d3),triple)
            right=embed(self.mm(dy_inverse,diagonal([self.unit_inverse(x) for x in s])),triple)
            assert self.mm(left,right)==eye(4) and self.mm(right,left)==eye(4)
            direction=[[self.mul(left[i][position],right[position][j]) for j in range(4)] for i in range(4)]
            basis.append((left,right,position,direction))
        return basis


def inherited_basis(base):
    certified = base['basis_conjugates']()
    specs=[]
    roots=[1,6,base['fm'](6,6)]
    for B, _, k, _ in certified:
        triple=tuple(i for i in range(4) if any(i!=j and base['red'](B[i][j]) for j in range(4)))
        exps=tuple(roots.index(base['red'](B[i][triple[0]])) for i in triple)
        specs.append((triple,exps,k))
    return specs, [term[-1] for term in certified]


def trial(h, base, specs, directions):
    r=Ring(h,base)
    seed_word=r.baseword()
    initial=r.compose(seed_word)
    target=[[int((i&j)==i) for j in range(4)] for i in range(4)]
    assert mapped(r.reduction,initial)==target
    basis=r.tangent(specs)
    actual=[[r.reduction(x) for row in direction for x in row] for _,_,_,direction in basis]
    assert actual==directions
    unit=[1]*16
    wrong=[]
    def word_value():
        factors=[]
        for u,(_,_,_,a) in zip(unit,basis):
            c=r.sub(u,1)
            factors.append([[r.add(int(i==j),r.mul(c,a[i][j])) for j in range(4)] for i in range(4)])
        return r.mm(r.compose(factors),initial)
    for t in range(1,h):
        v=word_value()
        delta=[[r.digit(r.sub(target[i][j],v[i][j]),t) for j in range(4)] for i in range(4)]
        # Multiply residual digit by target^{-1} over F16. Here target^{-1}=target modulo two.
        norm=[[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    if target[k][j]:
                        norm[i][j] ^= delta[i][k]
        correction=base['solve'](directions,[x for row in norm for x in row])
        wrong.append(sum(x!=0 for x in correction))
        for i,digit in enumerate(correction):
            unit[i]=r.add(unit[i],r.mul(1<<t,r.from_residue(digit)))
            assert r.reduction(unit[i])==1
    assert word_value()==target
    # Re-evaluate the literal Fourier/diagonal factors, independently of I+(u-1)C assembly.
    word=[]
    for u,(b,bi,k,_) in zip(unit,basis):
        ds=[1]*4; ds[k]=u
        word.extend([b,diagonal(ds),bi])
    word.extend(seed_word)
    assert r.compose(word)==target
    rng=Random(717011+h)
    failures=0
    arbitrary_outputs=0
    for d in (2,4,5):
        n=1<<d
        for lane in range(2):
            inputs=[rng.randrange(r.m) for _ in range(n)]
            def apply(f):
                f=f.copy()
                for m in reversed(word):
                    for pair_axis in range(d//2):
                        stride=1<<(2*pair_axis)
                        previous=f.copy()
                        for i in range(n):
                            label=(i//stride)%4
                            start=i-label*stride
                            f[i]=r.dot(m[label],[previous[start+k*stride] for k in range(4)])
                if d%2:
                    half=1<<(d-1)
                    for i in range(half):
                        f[i]=r.add(f[i],f[i+half])
                return f
            transformed=apply(inputs)
            oracle=[sum(x for j,x in enumerate(inputs) if (i&j)==i)%r.m for i in range(n)]
            assert transformed==oracle
            neg=lambda x,i: r.neg(x) if (d-i.bit_count())%2 else x
            back=[neg(x,i) for i,x in enumerate(apply([neg(x,i) for i,x in enumerate(oracle)]))]
            assert back==inputs
            failures+=sum(x!=y for x,y in zip(apply(oracle),inputs))
            arbitrary_outputs+=n
    assert not h>1 or failures>0
    return dict(precision_bits=h,ring_modulus=r.m,cube_root_coefficients=r.coeffs(r.w),
                initial_wrong_matrix_entries=sum(x!=y for a,b in zip(initial,target) for x,y in zip(a,b)),
                corrections_nonzero_parameters_by_iteration=wrong,
                literal_fourier_slots=56,all_sixteen_ring_entries_exact=True,
                independent_tensor_output_coefficients=arbitrary_outputs,
                wrong_binary_involution_coefficients=failures,
                unit_parameters=[r.coeffs(x) for x in unit])


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-word', type=Path, default=Path(__file__).with_name('verify-mod-four-word.py'))
    args=parser.parse_args()
    base=runpy.run_path(str(args.base_word))
    specs,directions=inherited_basis(base)
    reports=[trial(h,base,specs,directions) for h in (1,3,4,8,16)]
    print(json.dumps({'tangent_rank_F16':len(specs),'specifications':specs,'cases':reports},indent=2))
