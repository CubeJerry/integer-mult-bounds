#!/usr/bin/env python3
"""Exact primitive replay for the fixed-prefix Gaussian-dyadic compiler theorem.

No external arithmetic package or author/root compiler is imported.  The finite
examples verify the constructive identities; the all-size claim is in PROOF.md.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from collections import Counter
import json
from pathlib import Path

@dataclass(frozen=True)
class G:
    a: F = F(0)
    b: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))
    def __add__(self, other):
        other = cast(other)
        return G(self.a + other.a, self.b + other.b)
    __radd__ = __add__
    def __neg__(self): return G(-self.a, -self.b)
    def __sub__(self, other): return self + -cast(other)
    def __mul__(self, other):
        other = cast(other)
        return G(self.a*other.a-self.b*other.b, self.a*other.b+self.b*other.a)
    __rmul__ = __mul__
    def inverse(self):
        n = self.a*self.a + self.b*self.b
        assert n
        return G(self.a/n, -self.b/n)
    def __truediv__(self, other): return self * cast(other).inverse()
    def __bool__(self): return bool(self.a or self.b)
    def enc(self): return [str(self.a), str(self.b)]

def cast(x): return x if isinstance(x, G) else G(x)
ZERO, ONE, I, PI = G(), G(1), G(0, 1), G(1, 1)

def dyadic_integer_form(x):
    """x=(a+ib)/2**k; rejects coefficients outside R."""
    x = cast(x)
    ds = [x.a.denominator, x.b.denominator]
    assert all(z > 0 and z & (z-1) == 0 for z in ds)
    k = max(z.bit_length()-1 for z in ds)
    return int(x.a * 2**k), int(x.b * 2**k), k

def valuation_and_unit(x):
    assert x
    a, b, k = dyadic_integer_form(x)
    v = -2*k
    while (a-b) % 2 == 0:
        a, b = (a+b)//2, (b-a)//2
        v += 1
    return v, a*a+b*b == 1

def unit_terms(x):
    """Finite signed Gaussian powers-of-two expansion, never divide by x."""
    a, b, k = dyadic_integer_form(x)
    ans = []
    for integer, phase in [(a, ONE), (b, I)]:
        sign = -1 if integer < 0 else 1
        integer = abs(integer)
        for j in range(integer.bit_length()):
            if (integer >> j) & 1:
                c = phase * F(sign*2**j, 2**k)
                assert valuation_and_unit(c)[1]
                ans.append(c)
    assert sum(ans, ZERO) == x
    return ans

def identity(n): return [[ONE if a == b else ZERO for b in range(n)] for a in range(n)]
def matmul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]
def determinant(m):
    a = [row[:] for row in m]
    ans = ONE
    for j in range(len(a)):
        p = next((r for r in range(j, len(a)) if a[r][j]), None)
        if p is None: return ZERO
        if p != j: a[j], a[p], ans = a[p], a[j], -ans
        pivot = a[j][j]
        ans = ans*pivot
        for r in range(j+1, len(a)):
            c = a[r][j]/pivot
            a[r] = [x-c*y for x,y in zip(a[r],a[j])]
    return ans

def mono_identity(d): return (tuple(range(d)), (ONE,)*d)
def mono_inverse(m):
    p, z = m
    q, w = [0]*len(p), [ZERO]*len(p)
    for a,b in enumerate(p): q[b], w[b] = a, z[a].inverse()
    return tuple(q), tuple(w)
def mono_phase(d, at, phase):
    z = [ONE]*d
    z[at] = phase
    return tuple(range(d)), tuple(z)

def monomial_term(dst, src, c, mono):
    assert dst != src and valuation_and_unit(c)[1]
    return [('SCALE', src, c), ('MONO', src, mono), ('ADD', dst, src),
            ('MONO', src, mono_inverse(mono)), ('SCALE', src, c.inverse())]

def block_selector(dst, src, row, col, coefficient, d):
    """Compile X_dst += coefficient E_row,col X_src into literal primitives."""
    assert dst != src
    p = list(range(d))
    p[row], p[col] = p[col], p[row]
    plus = (tuple(p), (ONE,)*d)
    signs = [ONE]*d
    signs[row] = -ONE
    minus = (tuple(p), tuple(signs))
    word = []
    for c in unit_terms(coefficient):
        word += monomial_term(dst, src, c/2, plus)
        word += monomial_term(dst, src, -c/2, minus)
    return word

def elementary(row, col, r, d, banks):
    """Coordinate shear I+r E_row,col; uses no additional bank."""
    assert row != col and banks >= 2
    a, x = divmod(row, d)
    b, y = divmod(col, d)
    if a != b: return block_selector(a, b, x, y, r, d)
    helper = (a+1) % banks
    # Q=E_yy, P=r E_xy; QP=0 and PQ=P.
    return (block_selector(helper, a, y, y, ONE, d)
            + block_selector(a, helper, x, y, r, d)
            + block_selector(helper, a, y, y, -ONE, d)
            + block_selector(a, helper, x, y, -r, d))

def apply(word, d, banks):
    a = identity(d*banks)
    stats = Counter()
    for op in word:
        stats[op[0]] += 1
        if op[0] == 'ADD':
            _, dst, src = op
            assert dst != src and 0 <= dst < banks and 0 <= src < banks
            for j in range(d): a[d*dst+j] = [x+y for x,y in zip(a[d*dst+j],a[d*src+j])]
        elif op[0] == 'SCALE':
            _, bank, c = op
            assert valuation_and_unit(c)[1]
            for j in range(d): a[d*bank+j] = [c*x for x in a[d*bank+j]]
        elif op[0] == 'MONO':
            _, bank, (p,z) = op
            assert sorted(p) == list(range(d))
            assert all(t in (ONE,-ONE,I,-I) for t in z)
            old = [row[:] for row in a[d*bank:d*(bank+1)]]
            for j in range(d): a[d*bank+j] = [z[j]*x for x in old[p[j]]]
        else: raise AssertionError(op)
    return a, dict(stats)

def inverse_word(word):
    out = []
    for op in reversed(word):
        if op[0] == 'SCALE': out.append(('SCALE', op[1], op[2].inverse()))
        elif op[0] == 'MONO': out.append(('MONO', op[1], mono_inverse(op[2])))
        else:
            _, dst, src = op
            out += [('SCALE', src, -ONE), ('ADD', dst, src), ('SCALE', src, -ONE)]
    return out

def elementary_matrix(n, row, col, r):
    m = identity(n)
    m[row][col] = r
    return m

def paired_diagonal(row, col, u, d, banks):
    # w(u) w(-1) = diag(u,u^-1), with matrix products acting rightmost first.
    factors = [(row,col,u),(col,row,-u.inverse()),(row,col,u),
               (row,col,-ONE),(col,row,ONE),(row,col,-ONE)]
    word = []
    for a,b,c in reversed(factors): word += elementary(a,b,c,d,banks)
    return word

def reduce_sl(matrix):
    """Construct actual elementary row reductions by Gaussian-integer Euclid.

    Denominator clearing selects integer quotients only; it does not alter a
    bank or introduce a scaling primitive. Return the chronological factors
    taking matrix to the identity.
    """
    a = [row[:] for row in matrix]
    assert determinant(a) == ONE
    operations = []
    pivots = []
    def add(row,col,r):
        if not r: return
        a[row] = [x+r*y for x,y in zip(a[row],a[col])]
        operations.append((row,col,r))
    def signed_swap(row,col):
        add(row,col,ONE); add(col,row,-ONE); add(row,col,ONE)
    def paired(row,col,u):
        factors = [(row,col,u),(col,row,-u.inverse()),(row,col,u),
                   (row,col,-ONE),(col,row,ONE),(row,col,-ONE)]
        for x,y,r in reversed(factors): add(x,y,r)
    def nearest(x):
        # Any nearest Gaussian integer is a valid Euclidean quotient.
        def rnd(q): return (2*q.numerator+q.denominator)//(2*q.denominator)
        return G(rnd(x.a),rnd(x.b))
    n=len(a)
    for j in range(n-1):
        h=max(dyadic_integer_form(a[r][j])[2] for r in range(j,n))
        for r in range(j+1,n):
            while a[r][j]:
                x,y=a[j][j]*2**h,a[r][j]*2**h
                assert x.a.denominator==x.b.denominator==1
                assert y.a.denominator==y.b.denominator==1
                q=nearest(x/y)
                remainder=x-q*y
                assert remainder.a**2+remainder.b**2 < y.a**2+y.b**2
                add(j,r,-q)
                signed_swap(j,r)
        g=a[j][j]
        assert valuation_and_unit(g)[1]
        pivots.append(g.enc())
        paired(j,j+1,g.inverse())
        assert a[j][j]==ONE and all(not a[r][j] for r in range(j+1,n))
    assert a[-1][-1]==ONE
    for j in reversed(range(1,n)):
        for r in range(j): add(r,j,-a[r][j])
    assert a==identity(n)
    return operations,pivots

def run():
    reports = []
    for d,banks,entries,k in [
        (2,2,[(0,1,G(3)),(0,2,G(F(3,8),F(5,8))),(3,2,G(F(-3,4),F(1,2)))],1),
        (3,2,[(0,2,G(F(1,4),F(1,2))),(4,1,G(0,-3)),(3,5,G(5))],-1),
        (4,3,[(0,3,G(3)),(4,9,G(F(3,8),F(5,8))),(8,11,G(-5,2))],2),
    ]:
        n = d*banks
        word, expected = [], identity(n)
        for row,col,r in entries:
            w = elementary(row,col,r,d,banks)
            actual, _ = apply(w,d,banks)
            e = elementary_matrix(n,row,col,r)
            assert actual == e
            if row//d == col//d:
                helper = ((row//d+1)%banks)*d
                assert actual[helper:helper+d] == identity(n)[helper:helper+d]
            word += w
            expected = matmul(e,expected)
        scalar = ONE
        for _ in range(abs(k)): scalar = scalar*(PI if k >= 0 else PI.inverse())
        word += [('SCALE',0,scalar),('MONO',0,mono_phase(d,0,I))]
        s = identity(n)
        for j in range(d): s[j][j] = scalar*(I if j == 0 else ONE)
        expected = matmul(s,expected)
        actual, stats = apply(word,d,banks)
        assert actual == expected
        det = determinant(actual)
        valuation, unit = valuation_and_unit(det)
        assert unit and valuation == d*k
        assert apply(word+inverse_word(word),d,banks)[0] == identity(n)
        bad = list(word)
        bad.pop(next(j for j,x in enumerate(bad) if x[0] == 'ADD'))
        assert apply(bad,d,banks)[0] != expected
        reports.append({'d':d,'banks':banks,'word_length':len(word),'operations':stats,
                        'determinant':det.enc(),'pi_valuation':valuation,
                        'all_columns':n,'inverse_replayed':True,'omitted_ADD_rejected':True})
    paired = []
    for row,col in [(0,1),(0,4)]:
        word = paired_diagonal(row,col,PI,4,2)
        expected = identity(8)
        expected[row][row],expected[col][col] = PI,PI.inverse()
        actual,stats = apply(word,4,2)
        assert actual == expected and determinant(actual) == ONE
        paired.append({'coordinates':[row,col],'operations':stats,'determinant_one':True})
    obstructions=[]
    for d,x in [(2,PI),(3,PI),(4,G(2))]:
        m=identity(2*d);m[0][0]=x
        val,unit=valuation_and_unit(determinant(m))
        assert unit and val % d
        obstructions.append({'d':d,'diagonal_entry':x.enc(),'pi_valuation':val,
                             'invertible_over_R':True,'compiler_obstruction':True})
    for x in [G(3),G(F(3,8),F(5,8)),G(F(1,4),F(1,2))]:
        assert not valuation_and_unit(x)[1]
        assert sum(unit_terms(x),ZERO)==x
    # Tail identity check on a genuine internal shear, all arbitrary columns.
    w=elementary(0,1,G(3),2,2)
    a,_=apply(w,2,2)
    tensor=[[a[i//2][j//2] if i%2==j%2 else ZERO for j in range(8)] for i in range(8)]
    expected=identity(8);expected[0][2]=G(3);expected[1][3]=G(3)
    assert tensor==expected
    # A determinant-one matrix whose first pivot is a nonunit and whose
    # unimodular-column gcd is pi. This forces real Euclid and paired scaling.
    target=identity(4)
    target[0][0],target[0][1]=3*PI,PI.inverse()
    target[1][0],target[1][1]=2*PI,PI.inverse()
    reductions,pivots=reduce_sl(target)
    compiled=[]
    for row,col,r in reversed(reductions): compiled += elementary(row,col,-r,2,2)
    actual,stats=apply(compiled,2,2)
    assert actual==target
    assert apply(compiled+inverse_word(compiled),2,2)[0]==identity(4)
    return {'status':'PASS','theorem_scope':'R=Z[i,1/2], fixed finite d, b>=2 equal-prefix banks; exact unit SCALE/root-four MONO/whole-bank ADD; no extra bank',
            'examples':reports,'paired_unit_normalizations':paired,'valuation_obstructions':obstructions,
            'nonunit_coefficients_expanded_into_units':True,'tail_identity_control_N':2,
            'euclidean_compilation':{'matrix':[[x.enc() for x in row] for row in target],
                'unit_pivots':pivots,'elementary_factors':len(reductions),
                'literal_operations':stats,'all_columns':4,'inverse_replayed':True},
            'all_sizes_proved_in':'PROOF.md','finite_examples_are_not_exhaustive_classification':True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=Path(__file__).with_name('CERTIFICATE.json'))
    args=p.parse_args()
    result=run()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'out':str(args.out),'examples':len(result['examples'])}))
if __name__=='__main__':main()
