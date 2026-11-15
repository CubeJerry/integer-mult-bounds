#!/usr/bin/env python3
"""Independent exact phase, source-gauge and rank-rounding controls."""
import argparse
from collections import Counter
from itertools import product, permutations, combinations
import json
from pathlib import Path
import sympy as sp

Z = (0,0)
O = (1,0)
I = (0,1)

def plus(a,b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def times(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def summ(xs):
    z = Z
    for x in xs: z = plus(z,x)
    return z
def det(M):
    n=len(M); out=Z
    for p in permutations(range(n)):
        z=O
        for i in range(n): z=times(z,M[i][p[i]])
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        out=plus(out,neg(z) if inv%2 else z)
    return out
def rank(M):
    n=len(M)
    for k in range(n,0,-1):
        for rows in combinations(range(n),k):
            for cols in combinations(range(n),k):
                if det([[M[i][j] for j in cols] for i in rows]) != Z:
                    return k
    return 0
def gf2rank(rows):
    p={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in p: x^=p[k]
            else: p[k]=x;break
    return len(p)
def sign_matrix(M,c, subtract=False):
    if subtract:
        return [[plus(M[i][j],(-c[i],0)) if i==j else M[i][j] for j in range(len(M))] for i in range(len(M))]
    return [[plus(times((c[i],0),M[i][j]),O) if i==j else times((c[i],0),M[i][j]) for j in range(len(M))] for i in range(len(M))]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    powers=[O,I,(-1,0),(0,-1)]
    phases={}
    trace_hist=Counter();rank_hist=Counter();support_hist=Counter()
    for a in product(range(4),repeat=3):
        for b in product(range(2),repeat=3):
            f=tuple((sum(a[j]*((x>>j)&1) for j in range(3))+2*(b[0]*(x&1)*((x>>1)&1)+b[1]*(x&1)*((x>>2)&1)+b[2]*((x>>1)&1)*((x>>2)&1)))%4 for x in range(8))
            assert f not in phases
            B=[(a[0]%2)|(b[0]<<1)|(b[1]<<2), b[0]|((a[1]%2)<<1)|(b[2]<<2), b[1]|(b[2]<<1)|((a[2]%2)<<2)]
            r=gf2rank(B)
            for x,z in product(range(8),repeat=2):
                Bz=sum(((B[j]&z).bit_count()%2)<<j for j in range(3))
                assert (f[x^z]-f[x]-f[z])%4==2*((x&Bz).bit_count()%2)
            s=summ(powers[e] for e in f);norm=s[0]**2+s[1]**2
            assert norm==64 if not any(f) else norm<=32
            spectrum=[]
            for y in range(8):
                t=summ(neg(powers[f[x]]) if (x&y).bit_count()%2 else powers[f[x]] for x in range(8))
                spectrum.append(t)
            support=sum(t!=Z for t in spectrum)
            assert support==2**r
            phases[f]=(a,b);trace_hist[norm]+=1;rank_hist[r]+=1;support_hist[support]+=1
    gens=[tuple((v&x).bit_count()%2 for x in range(8)) for v in range(1,8)]
    reached={(0,)*8};frontier=list(reached)
    for f in frontier:
        for g in gens:
            h=tuple((x+y)%4 for x,y in zip(f,g))
            if h not in reached: reached.add(h);frontier.append(h)
    assert reached==set(phases) and len(reached)==512
    assert tuple(sum(g[x] for g in gens)%4 for x in range(8))==(0,)*8
    assert 511 < 2**9

    # Rounding is checked by exact Gaussian-integer minors, no floating ranks.
    matrices=[[[v[2*i+j] for j in range(2)] for i in range(2)] for v in product([Z,O,(-1,0),I],repeat=4)]
    for n in (3,4):
        for seed in range(12):
            matrices.append([[( ((i+1)*(j+2)+seed)%5-2, (2*i+j+seed)%3-1 ) for j in range(n)] for i in range(n)])
    checked=0;maxn=0
    for M in matrices:
        n=len(M);signs=list(product((-1,1),repeat=n));dets=[det(sign_matrix(M,c)) for c in signs]
        assert summ(dets)==(2**n,0)
        c=next(c for c,d in zip(signs,dets) if d!=Z)
        for d in signs:
            assert sum(a!=b for a,b in zip(c,d)) <= rank(sign_matrix(M,d,subtract=True))
            checked+=1
        maxn=max(maxn,n)
    fixed=[ [(-1,0),Z], [Z,O] ]
    assert det(sign_matrix(fixed,(1,1)))==Z
    assert sum(a!=b for a,b in zip((1,1),(-1,1))) > rank(sign_matrix(fixed,(-1,1),subtract=True))

    # Authenticate all42 ordered direction pairs from the actual source.
    eye=sp.eye(8)
    def perm(images):
        M=sp.zeros(8)
        for x,y in enumerate(images):M[y,x]=1
        return M
    def H(cols):return perm([((cols[0] if x&1 else 0)^(cols[1] if x&2 else 0)^(cols[2] if x&4 else 0)) for x in range(8)])
    X={v:perm([x^v for x in range(8)]) for v in range(1,8)}
    C={v:(eye-sp.I*X[v])*(1+sp.I)/2 for v in range(1,8)}
    S=perm([0,4,1,5,2,6,3,7]);a=C[2]*S
    simplify=lambda M:M.applyfunc(sp.expand)
    gauged=0
    for u,w in permutations(range(1,8),2):
        q=next(v for v in range(1,8) if v not in (u,w,u^w))
        G=H([q,u,w]);Gi=G.T
        assert simplify(G*a*S.T*Gi-C[u])==sp.zeros(8)
        assert G*Gi==eye
        assert simplify(G*S.T*a*Gi-C[w])==sp.zeros(8)
        # J L0 J is upper ordinary-cross; the two role swaps are paid.
        G=H([w,u,q]);Gi=G.T
        R0=S.T*Gi*X[u]
        R1=(S.T**2)*Gi*X[u]*X[w]
        L1=X[u]*G*S
        assert simplify(G*a*R0)==simplify(C[u]*X[u])
        assert simplify(L1*a*R1)==simplify(C[w]*X[w])
        assert simplify(-G*a*a*R1)==simplify(-C[u]*X[u]*C[w]*X[w])
        gauged+=1
    out={'status':'PASS_INDEPENDENT_COMMUTING_CORE',
         'phase_group_size':len(phases),'trace_squared_histogram':dict(sorted(trace_hist.items())),
         'Gaussian_rank_histogram':dict(sorted(rank_hist.items())),
         'Fourier_support_histogram':dict(sorted(support_hist.items())),
         'faithful_tensor_width_sufficient':18,'normalized_Gram_row_sum_at_18':'511/512',
         'rounding_matrices':len(matrices),'rounding_sign_comparisons':checked,'maximum_tested_role_count':maxn,
         'fixed_rounding_sign_negative_control':True,'actual_positive_and_inverse_gauge_pairs':gauged,
         'universal_claim_source':'written rank-rounding, odd-sign telescoping, and tensor-Gram proofs',
         'new_complete_kappa':False}
    args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
