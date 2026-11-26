#!/usr/bin/env python3
"""Exact finite-field and occupied-orbit checks, not a full tape executor."""
from pathlib import Path
from math import comb
import hashlib
import json

class Field:
    def __init__(self, p):
        self.p = p
        self.q = p * p
        self.nu = next(x for x in range(2, p) if pow(x, (p-1)//2, p) == p-1)
    def add(self, x, y):
        p = self.p
        return (x % p + y % p) % p + p * ((x//p + y//p) % p)
    def neg(self, x):
        p = self.p
        return (-x % p) % p + p * (-(x//p) % p)
    def sub(self, x, y):
        return self.add(x, self.neg(y))
    def mul(self, x, y):
        p = self.p
        a, b, c, d = x % p, x//p, y % p, y//p
        return (a*c+self.nu*b*d) % p + p*((a*d+b*c) % p)
    def power(self, x, n):
        out = 1
        while n:
            if n & 1:
                out = self.mul(out, x)
            x = self.mul(x, x)
            n >>= 1
        return out
    def inv(self, x):
        assert x
        return self.power(x, self.q-2)
    def div(self, x, y):
        return self.mul(x, self.inv(y))

def diagonal(x, y):
    return [[x, 0], [0, y]]

def mm(f, a, b):
    return [[f.add(f.mul(a[i][0], b[0][j]), f.mul(a[i][1], b[1][j]))
             for j in range(2)] for i in range(2)]

def word(f, matrices):
    out = diagonal(1, 1)
    for matrix in matrices:
        out = mm(f, out, matrix)
    return out

def inverse(f, matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    delta = f.inv(f.sub(f.mul(a, d), f.mul(b, c)))
    return [[f.mul(delta, d), f.mul(delta, f.neg(b))],
            [f.mul(delta, f.neg(c)), f.mul(delta, a)]]

def parameters(f, r, ii):
    one, minus = 1, f.neg(1)
    a = f.div(ii, r)
    rr = f.mul(ii, f.add(r, one))
    c = [[a, a], [a, f.neg(a)]]
    aa = diagonal(f.neg(2), f.neg(f.mul(2, ii)))
    bb = diagonal(f.div(f.add(rr, 1), 2), f.div(f.sub(rr, 1), 2))
    jj = diagonal(f.inv(rr), 1)
    s = [[1, 1], [f.sub(r, 1), f.neg(f.add(r, 1))]]
    t = inverse(f, s)
    return dict(C=c, A=aa, B=bb, J=jj, S=s, T=t,
                E=diagonal(1, minus), M=diagonal(minus, minus),
                Q=[[0,1],[1,0]], D=diagonal(ii, f.neg(ii)), a=a)

def matrix_checks():
    count = 0
    cases = []
    for p in [3, 5, 7, 11, 13, 17, 19, 31]:
        f = Field(p)
        roots_r = [x for x in range(f.q) if f.mul(x, x) == 2]
        roots_i = [x for x in range(f.q) if f.mul(x, x) == p-1]
        assert len(roots_r) == len(roots_i) == 2
        for r in roots_r:
            for ii in roots_i:
                v = parameters(f, r, ii)
                c = v['C']
                assert word(f, [c,c]) == diagonal(p-1,p-1)
                assert word(f, [c,c,c,c]) == diagonal(1,1)
                assert word(f, [v['A'],c,v['B'],c,v['J']]) == v['S']
                assert word(f, [v['T'],c,v['S']]) == v['D']
                assert word(f, [inverse(f,v['J']),inverse(f,c),inverse(f,v['B']),
                                inverse(f,c),inverse(f,v['A'])]) == v['T']
                assert word(f, [v['M'],c,v['E'],c]) == v['Q']
                count += 6
        cases.append((f, parameters(f, roots_r[0], roots_i[0])))
    return count, cases

def local(f, vector, m, j, matrix, fixed=1, radix=3, suffix=2):
    n = radix ** (2*m)
    out = [0] * len(vector)
    left, right = radix ** j, radix ** (m+j)
    for index, value in enumerate(vector):
        address = (index // suffix) % n
        h, k = address // left % radix, address // right % radix
        if h == k:
            out[index] = f.mul(fixed, value)
        elif h < k:
            other = index + ((k-h)*left+(h-k)*right)*suffix
            out[index] = f.add(f.mul(matrix[0][0],value),
                               f.mul(matrix[0][1],vector[other]))
            out[other] = f.add(f.mul(matrix[1][0],value),
                               f.mul(matrix[1][1],vector[other]))
    return out

def all_pairs(f, vector, m, matrix, fixed=1):
    for j in range(m):
        vector = local(f, vector, m, j, matrix, fixed)
    return vector

def global_word(f, vector, m, matrices):
    for matrix in reversed(matrices):
        vector = all_pairs(f, vector, m, matrix)
    return vector

def row_apply(f, matrix, vector):
    width = len(vector)//2
    return [f.add(f.mul(matrix[i][0],vector[k]),
                  f.mul(matrix[i][1],vector[width+k]))
            for i in range(2) for k in range(width)]

def vadd(f, a, b):
    return [f.add(x,y) for x,y in zip(a,b)]

def mscale(f, scalar, matrix):
    return [[f.mul(scalar,x) for x in row] for row in matrix]

def madd(f, a, b):
    return [[f.add(x,y) for x,y in zip(rowa,rowb)] for rowa,rowb in zip(a,b)]

def pencil(f, v, vector, m):
    def coef(seed):
        return [[(seed+1)%f.q,(seed*2+1)%f.q],
                [(seed*3+2)%f.q,(seed*seed+3)%f.q]]
    direct = row_apply(f,coef(0),vector)
    compiled = direct[:]
    for j in range(m):
        a1,a2,a3 = (coef(3*j+k) for k in (1,2,3))
        power = vector
        for matrix in (a1,a2,a3):
            power = local(f,power,m,j,v['C'])
            direct = vadd(f,direct,row_apply(f,matrix,power))
        diff = madd(f,a1,mscale(f,f.neg(1),a3))
        compiled = vadd(f,compiled,row_apply(f,mscale(f,f.neg(1),a2),vector))
        swapped = local(f,vector,m,j,v['Q'])
        compiled = vadd(f,compiled,row_apply(f,mscale(f,v['a'],diff),swapped))
        # U-L is zero on the equality records; K is one there and zero elsewhere.
        signed = local(f,vector,m,j,diagonal(1,f.neg(1)),fixed=0)
        equal = local(f,vector,m,j,diagonal(0,0),fixed=1)
        compiled = vadd(f,compiled,row_apply(f,mscale(f,v['a'],diff),signed))
        kcoef = madd(f,mscale(f,f.sub(1,v['a']),diff),
                    mscale(f,2,madd(f,a2,a3)))
        compiled = vadd(f,compiled,row_apply(f,kcoef,equal))
    assert compiled == direct
    return len(vector)

def orbit_checks(cases):
    totals = dict(global_word_outputs=0,pencil_outputs=0,
                  negative_controls=0, independent_rows=2,
                  suffix_spectators=2)
    for f,v in cases:
        for m in [1,2,3]:
            n = 4 * 3 ** (2*m)
            vectors = [[(k*k+3*k+1)%f.q for k in range(n)],
                       [(7*k+5)%f.q for k in range(n)]]
            # Complete basis replay for the smallest physical shape, with all
            # equal and unequal field pairs, independent rows, and spectators.
            if m == 1:
                vectors += [[int(k==j) for k in range(n)] for j in range(n)]
            for vector in vectors:
                c=v['C']
                assert global_word(f,vector,m,[v['A'],c,v['B'],c,v['J']]) == \
                    all_pairs(f,vector,m,v['S'])
                assert global_word(f,vector,m,[inverse(f,v['J']),inverse(f,c),
                    inverse(f,v['B']),inverse(f,c),inverse(f,v['A'])]) == \
                    all_pairs(f,vector,m,v['T'])
                assert global_word(f,vector,m,[v['T'],c,v['S']]) == \
                    all_pairs(f,vector,m,v['D'])
                assert global_word(f,vector,m,[v['M'],c,v['E'],c]) == \
                    all_pairs(f,vector,m,v['Q'])
                totals['global_word_outputs'] += 4*n
                totals['pencil_outputs'] += pencil(f,v,vector,m)
            test=[1]*n
            assert global_word(f,test,m,[c,v['E'],c]) != all_pairs(f,test,m,v['Q'])
            assert all_pairs(f,test,m,v['D'],fixed=v['D'][0][0]) != \
                all_pairs(f,test,m,v['D'])
            totals['negative_controls'] += 2
    return totals

def generalized_binom(n,k):
    value=1
    for j in range(1,k+1):
        value=value*(n-j+1)//j
    return value

def predictor_checks(cases):
    checks=0
    for f,v in cases:
        p=f.p
        ii=v['D'][0][0]
        for count in range(25):
            for u in range(-5,6):
                for degree in range(13):
                    t=1
                    while p**t<=degree:
                        t+=1
                    lucas=0
                    direct=0
                    for h in range(degree+1):
                        coefficient=1
                        for k in range(t):
                            digit=(count-u)//(p**k)%p
                            hdigit=h//(p**k)%p
                            coefficient=coefficient*comb(digit,hdigit)%p
                        power=f.power(f.sub(ii,1),h)
                        lucas=f.add(lucas,f.mul(power,coefficient))
                        direct=f.add(direct,f.mul(power,generalized_binom(count-u,h)%p))
                    assert lucas==direct
                    phase=f.power(ii,u%4)
                    if u<=count<=u+degree:
                        assert f.mul(phase,lucas)==f.power(ii,count%4)
                    checks+=1
        # The four Fourier projectors are an affine pencil in C's powers.
        for exponent in range(4):
            projector=[[0,0],[0,0]]
            power=diagonal(1,1)
            for h in range(4):
                scalar=f.mul(f.inv(4%p),f.power(ii,(-exponent*h)%4))
                projector=madd(f,projector,mscale(f,scalar,power))
                power=mm(f,power,v['C'])
            expected=diagonal(int(exponent==1),int(exponent==3))
            assert word(f,[v['T'],projector,v['S']])==expected
    f,v=cases[0]
    assert f.p==3
    assert generalized_binom(3,3)%3==1 and generalized_binom(3%3,3)%3==0
    assert f.power(v['D'][0][0],3)!=1
    return dict(count_offset_newton_cases=checks,fourier_projectors=4*len(cases),
                missing_initial_base_three_high_digit_control=1)

def matrix_inverse(f, matrix):
    n=len(matrix)
    rows=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if rows[i][col])
        rows[col],rows[pivot]=rows[pivot],rows[col]
        scale=f.inv(rows[col][col])
        rows[col]=[f.mul(scale,x) for x in rows[col]]
        for i in range(n):
            if i!=col:
                scalar=rows[i][col]
                rows[i]=[f.sub(x,f.mul(scalar,y)) for x,y in zip(rows[i],rows[col])]
    return [row[n:] for row in rows]

def mv(f, matrix, vector):
    out=[]
    for row in matrix:
        total=0
        for scalar,value in zip(row,vector):
            total=f.add(total,f.mul(scalar,value))
        out.append(total)
    return out

def repair_checks(cases):
    count=0
    outside=0
    wrong_transpose=0
    for f,v in cases:
        for selected in [[0,1],[1,3,6],[0,2,5,7]]:
            s=len(selected)
            h=[[f.power(node,k) for node in range(8)] for k in range(s)]
            restricted=[[row[j] for j in selected] for row in h]
            vi=matrix_inverse(f,restricted)
            vit=list(map(list,zip(*vi)))
            ht=list(map(list,zip(*h)))
            for phase in range(4):
                z=f.power(v['D'][0][0],phase)
                gap=[0]*8
                for j in selected[1:]:
                    gap[j]=(j+f.p)%f.q or 1
                # selected[0] has zero actual gap inside the containing set.
                inverse_gap=[f.power(gap[j],f.q-2) for j in selected]
                assert inverse_gap[0]==0
                for basis in range(9):
                    x=[int(j==basis) if basis<8 else (3*j+1)%f.q for j in range(8)]
                    error=[f.mul(g,value) for g,value in zip(gap,x)]
                    recovered=mv(f,vi,mv(f,h,error))
                    lifted_input=[f.mul(g,e) for g,e in zip(inverse_gap,recovered)]
                    zz=mv(f,ht,mv(f,vit,lifted_input))
                    predicted=[f.mul(f.add(z,g),value) for g,value in zip(gap,x)]
                    result=[f.add(f.sub(y,f.mul(f.add(z,g),w)),f.mul(z,w))
                            for y,g,w in zip(predicted,gap,zz)]
                    assert result==[f.mul(z,value) for value in x]
                    assert zz[selected[0]]==0
                    outside+=int(any(zz[j] for j in range(8) if j not in selected))
                    wrong=mv(f,ht,mv(f,vi,lifted_input))
                    if any(f.mul(g,f.sub(value,w)) for g,value,w in zip(gap,x,wrong)):
                        wrong_transpose+=1
                    count+=8
    assert outside and wrong_transpose
    return dict(corrected_output_entries=count,
                zero_gap_containing_sets=4*3*len(cases),
                nonzero_outside_lift_examples=outside,
                rejected_wrong_transpose_examples=wrong_transpose)

def main():
    matrices,cases=matrix_checks()
    report={"status":"passed","exact_field_matrix_identities":matrices,
            "primes":[f.p for f,_ in cases],"orbit_checks":orbit_checks(cases),
            "predictor_checks":predictor_checks(cases),
            "repair_checks":repair_checks(cases),
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "scope":"Finite identities and complete occupied-orbit pencils; no full tape multiplier."}
    Path(__file__).with_name('order-four-closure-verification.json').write_text(
        json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
