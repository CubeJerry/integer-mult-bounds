#!/usr/bin/env python3
"""Independent literal Bell columns and nonlinear spectral-table verification."""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

def par(x): return x.bit_count() & 1
def dot(x,y): return par(x & y)
def sg(b): return 1-2*b
def rows(x,a,h): return [(x>>(i*h)) & ((1<<h)-1) for i in range(a)]
def pack(rs,h): return sum(z<<(i*h) for i,z in enumerate(rs))
def clean(d): return {k:v for k,v in d.items() if v}
def scaled(d,c): return clean({k:v*c for k,v in d.items()})
def bell(u,v,d): return {(z,z^u):sg(dot(v,z)) for z in range(1<<d)}

def lin(m,x,h):
    rs=rows(x,len(m),h)
    out=[]
    for mask in m:
        z=0
        for i,r in enumerate(rs):
            if mask>>i&1: z^=r
        out.append(z)
    return pack(out,h)

def inv(m):
    a=len(m)
    aug=[m[i]|(1<<(a+i)) for i in range(a)]
    for j in range(a):
        p=next((i for i in range(j,a) if aug[i]>>j&1),None)
        if p is None: return None
        aug[j],aug[p]=aug[p],aug[j]
        for i in range(a):
            if i!=j and aug[i]>>j&1: aug[i]^=aug[j]
    return [z>>a for z in aug]

def trans(m):
    return [sum(((m[i]>>j)&1)<<i for i in range(len(m))) for j in range(len(m))]

def quad(x,a,h,q):
    pairs,affine,c=q
    answer=0
    for t in range(h):
        column=sum(((x>>(i*h+t))&1)<<i for i in range(a))
        answer^=c^dot(affine,column)
        for i,j in pairs: answer^=((column>>i)&1)&((column>>j)&1)
    return answer

def polar(a,q):
    m=[0]*a
    for i,j in q[0]:
        m[i]^=1<<j
        m[j]^=1<<i
    return m

def replace(x,i,z,h):
    return (x & ~(((1<<h)-1)<<(i*h))) | (z<<(i*h))

def subgroup(shifts):
    # Tiny-test enumeration only. The written compiler uses elimination.
    coords={0:0}
    basis=[]
    for t in shifts:
        if t not in coords:
            b=1<<len(basis)
            basis.append(t)
            coords.update({x^t:c^b for x,c in list(coords.items())})
    members=[None]*(1<<len(basis))
    for x,c in coords.items(): members[c]=x
    return coords,members

def table(bits):
    return Fraction(1+sum((i+1)*b for i,b in enumerate(bits))
                    +3*bits[0]*bits[-1],2+sum(bits))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--proof",type=Path)
    args=parser.parse_args()
    count=defaultdict(int)
    for a,h in ((1,1),(2,1),(2,2),(3,1)):
        d=a*h
        pairs=list(combinations(range(a),2))
        for subset in range(1<<len(pairs)):
            pp=tuple(p for i,p in enumerate(pairs) if subset>>i&1)
            for affine,c in product(range(1<<a),(0,1)):
                q=(pp,affine,c)
                for u,v in product(range(1<<d),repeat=2):
                    out={xy:z*sg(quad(xy[0],a,h,q)^quad(xy[1],a,h,q))
                         for xy,z in bell(u,v,d).items()}
                    phase=quad(u,a,h,q)^((h&1)*c)
                    target=scaled(bell(u,v^lin(polar(a,q),u,h),d),sg(phase))
                    assert out==target
                    count["quadratic_basis_columns"]+=1
        for m in product(range(1<<a),repeat=a):
            mi=inv(m)
            if mi is None: continue
            for u,v in product(range(1<<d),repeat=2):
                out={(lin(m,x,h),lin(m,y,h)):z for (x,y),z in bell(u,v,d).items()}
                assert out==bell(lin(m,u,h),lin(trans(mi),v,h),d)
                count["linear_basis_columns"]+=1
        for i in range(a):
            for u,v in product(range(1<<d),repeat=2):
                ur,vr=rows(u,a,h)[i],rows(v,a,h)[i]
                out=defaultdict(int)
                for (x,y),z in bell(u,v,d).items():
                    xr,yr=rows(x,a,h)[i],rows(y,a,h)[i]
                    for p,q in product(range(1<<h),repeat=2):
                        out[(replace(x,i,p,h),replace(y,i,q,h))]+=z*sg(dot(xr,p)^dot(yr,q))
                target=scaled(bell(replace(u,i,vr,h),replace(v,i,ur,h),d),
                              (1<<h)*sg(dot(ur,vr)))
                assert clean(out)==target
                count["paired_walsh_basis_columns"]+=1
    for a,h in ((2,1),(2,2),(3,1),(4,1)):
        d=a*h
        qs=[(((0,1),),0,0),(((0,1),),1,1),((),(1<<a)-1,1)]
        if a>=3: qs += [(((0,2),),2,0),(((0,1),(0,2)),3,1)]
        for u in range(1<<d):
            shifts=[lin(polar(a,q),u,h) for q in qs]
            phases=[quad(u,a,h,q)^((h&1)*q[2]) for q in qs]
            coords,members=subgroup(shifts)
            s=(len(members)-1).bit_length()
            if s<len(qs): count["dependent_translation_fibres"]+=1
            if not s: count["zero_translation_fibres"]+=1
            eig=[table([p^dot(eta,coords[t]) for p,t in zip(phases,shifts)])
                 for eta in range(1<<s)]
            kernel=[sum((sg(dot(eta,z))*eig[eta] for eta in range(1<<s)),Fraction())/(1<<s)
                    for z in range(1<<s)]
            for v in range(1<<d):
                direct={xy:z*table([quad(xy[0],a,h,q)^quad(xy[1],a,h,q) for q in qs])
                        for xy,z in bell(u,v,d).items()}
                predicted=defaultdict(Fraction)
                for z,t in enumerate(members):
                    for xy,c in bell(u,v^t,d).items(): predicted[xy]+=kernel[z]*c
                assert clean(direct)==clean(predicted)
                count["nonlinear_table_basis_columns"]+=1
    # Diagonal phase is Bell-monomial only if its derivative in z is affine.
    for name,phase in (
        ("cubic",lambda z: ((z>>1)&1)*((z>>2)&1)),
        ("unequal_pair",lambda z: (z&1)*((z>>1)&1)),
    ):
        spectrum=[sum(sg(phase(z)^dot(v,z)) for z in range(8)) for v in range(8)]
        assert sum(value!=0 for value in spectrum)>1
        count[name+"_rejection_controls"]+=1
    here=Path(__file__).resolve().parent
    report={
        "status":"pass","counts":dict(count),
        "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "proof_sha256":hashlib.sha256(args.proof.read_bytes()).hexdigest() if args.proof else None,
        "scope":"Exact finite physical Bell columns, nonlinear rational table, dependency phases and negative controls; no tape runtime or full multiplier."
    }
    (here/"bell-independent-verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__": main()

