"""Mixed 3-by-5 Fourier convolution on Z/4[t]/(t^4+t+1)[z]/z^3."""
from random import Random
import json

E, R, N = 4, 3, 15
GRID = [5*(j%3)+(j%5) for j in range(N)]


def digits(x):
    return [(x>>(2*i))&3 for i in range(E)]


def packed(v):
    return sum((x&3)<<(2*i) for i,x in enumerate(v))


DIGITS=[digits(i) for i in range(256)]
ADD=[[packed([x+y for x,y in zip(a,b)]) for b in DIGITS] for a in DIGITS]


def raw_product(a,b):
    v=[0]*7
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            v[i+j]+=x*y
    for i in range(6,3,-1):
        v[i-4]-=v[i]
        v[i-3]-=v[i]
    return packed(v[:4])


MUL=[[raw_product(a,b) for b in DIGITS] for a in DIGITS]
NEG=[packed([-x for x in a]) for a in DIGITS]


def power(x,k):
    z=1
    while k:
        if k&1:
            z=MUL[z][x]
        x=MUL[x][x]
        k//=2
    return z


ROOT=power(4,16)
assert power(ROOT,15)==1 and all(power(ROOT,15//p)!=1 for p in (3,5))
ROOTS={p:power(ROOT,15//p) for p in (3,5)}
assert ADD[ADD[power(ROOTS[3],2)][ROOTS[3]]][1]==0


def jadd(a,b):
    return [ADD[x][y] for x,y in zip(a,b)]


def jmul(a,b):
    c=[0]*R
    for i in range(R):
        for j in range(R-i):
            c[i+j]=ADD[c[i+j]][MUL[a[i]][b[j]]]
    return c


def axis(v,p,inverse=False,skip_norm=False):
    groups=([[5*i+k for i in range(p)] for k in range(5)] if p==3 else
            [[5*k+i for i in range(p)] for k in range(3)])
    out=[[0]*R for _ in range(N)]
    norm=(p%4 if inverse and not skip_norm else 1)
    weights=[[MUL[norm][power(ROOTS[p],(-k*j if inverse else k*j)%p)]
              for j in range(p)] for k in range(p)]
    for group in groups:
        for k,dst in enumerate(group):
            for j,src in enumerate(group):
                w=weights[k][j]
                for h in range(R):
                    out[dst][h]=ADD[out[dst][h]][MUL[w][v[src][h]]]
    return out


def transform(v,inverse=False,skip_norm=False):
    return axis(axis(v,3,inverse,skip_norm),5,inverse,skip_norm)


def grid_mul(a,b,skip_norm=False):
    return transform([jmul(x,y) for x,y in zip(a,b)],True,skip_norm)


def packing(v):
    out=[[0]*R for _ in range(N)]
    for i,x in enumerate(v):
        basis=i%2
        h=i//2%2
        j=i//4
        out[GRID[j]][h]=ADD[out[GRID[j]][h]][x<<(2*basis)]
    return out


def gather(v,n):
    out=[0]*(2*n-1)
    for j,addr in enumerate(GRID):
        for h,c in enumerate(v[addr]):
            for a,x in enumerate(DIGITS[c]):
                i=a+2*h+4*j
                if i<len(out):
                    out[i]=(out[i]+x)%4
    return out


def school(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]=(out[i+j]+x*y)%4
    return out


def main():
    rng=Random(724716)
    counts=dict(ring_scalar_two_shear_cases=0,nonzero_nonunits_checked=0,
                dense_cyclic_jet_coefficients=0,dense_cyclic_ring_coordinates=0,
                packed_basis_pairs=0,packed_output_coefficients=0,
                dense_packed_pairs=0,norm_omission_failures=0,root_order=15)
    for coeff in range(256):
        def unit(x):
            return any(d&1 for d in DIGITS[x])
        s=next(v for v in (1,ROOTS[3],power(ROOTS[3],2)) if unit(ADD[coeff][NEG[v]]))
        t=ADD[coeff][NEG[s]]
        assert unit(s) and unit(t)
        if coeff and not unit(coeff):
            counts['nonzero_nonunits_checked']+=1
            assert MUL[coeff][coeff]==0
        for source in range(256):
            target=175
            assert ADD[ADD[target][MUL[t][source]]][MUL[s][source]]==ADD[target][MUL[coeff][source]]
            counts['ring_scalar_two_shear_cases']+=1
    assert counts['nonzero_nonunits_checked']==15
    for _ in range(16):
        a=[[[rng.randrange(256) for _ in range(R)] for _ in range(N)] for _ in range(2)]
        left,right=a
        freq=grid_mul(transform(left),transform(right))
        actual=[[0]*R for _ in range(N)]
        for i in range(N):
            for j in range(N):
                k=GRID[(i+j)%N]
                actual[k]=jadd(actual[k],jmul(left[GRID[i]],right[GRID[j]]))
        assert freq==actual
        counts['dense_cyclic_jet_coefficients']+=R*N
        counts['dense_cyclic_ring_coordinates']+=R*N*E
    n=24
    spec={}
    for scalar in (1,2,3):
        for i in range(n):
            a=[0]*n
            a[i]=scalar
            spec[i,scalar]=transform(packing(a))
    for i in range(n):
        for j in range(n):
            for x,y in ((1,1),(1,2),(2,2),(2,3),(3,3)):
                actual=[0]*(2*n-1)
                actual[i+j]=x*y%4
                output=gather(grid_mul(spec[i,x],spec[j,y]),n)
                assert actual==output
                counts['packed_basis_pairs']+=1
                counts['packed_output_coefficients']+=len(output)
    for _ in range(32):
        a=[rng.randrange(4) for _ in range(n)]
        b=[rng.randrange(4) for _ in range(n)]
        left,right=transform(packing(a)),transform(packing(b))
        expected=school(a,b)
        assert gather(grid_mul(left,right),n)==expected
        assert gather(grid_mul(left,right,True),n)!=expected
        counts['dense_packed_pairs']+=1
        counts['norm_omission_failures']+=1
        counts['packed_output_coefficients']+=len(expected)
    print(json.dumps(counts,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
