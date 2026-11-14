#!/usr/bin/env python3
"""Direct root-geometric certificate for the pivot92 fitting.

The primary certificate does not run the exploratory cover search. It
constructs covers from omitted roots and certifies the nine obstructions.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

NATIVE = "research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz"
PIN = "51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"

def need(c, msg):
    if not c: raise ValueError(msg)

def basis(rows):
    p = {}
    for r in rows:
        while r:
            j = r.bit_length()-1
            if j in p: r ^= p[j]
            else: p[j] = r; break
    return list(p.values())

def rank(rows, p=101):
    a = [[x % p for x in r] for r in rows]
    n = len(a[0]) if a else 0; at = 0
    for c in range(n):
        j = next((j for j in range(at,len(a)) if a[j][c]),None)
        if j is None: continue
        a[at],a[j] = a[j],a[at]; inv = pow(a[at][c],-1,p)
        a[at] = [inv*x % p for x in a[at]]
        for j in range(at+1,len(a)):
            t = a[j][c]
            if t: a[j] = [(x-t*y)%p for x,y in zip(a[j],a[at])]
        at += 1
        if at == n: break
    return at

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    raw=(args.repo/NATIVE).read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    n=json.loads(gzip.decompress(raw));R=[]
    for j in range(111):
        r=list(map(Fraction,n['frames'][str(n['start'][j])]['B'][0]));q=sum(x*x for x in r)
        s=(2 if q==1 else 1)*(1 if next(x for x in r if x)>0 else -1)
        r=[s*x for x in r];need(all(x.denominator==1 for x in r) and sum(x*x for x in r)==4,'integer root normalization');R.append(tuple(map(int,r)))
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    blocks=sorted({tuple(j for j,x in enumerate(r) if x) for r in R if sum(bool(x) for x in r)==4})
    need(len(blocks)==14,'four-support families')
    F=[tuple(2*int(a==b) for a in range(8)) for b in range(8)]
    for block in blocks:
        for signs in itertools.product((-1,1),repeat=3):
            r=[0]*8;r[block[0]]=1
            for a,s in zip(block[1:],signs):r[a]=s
            F.append(tuple(r))
    need(len(set(F))==120 and set(R)<=set(F),'completed root configuration')
    need(all(dot(a,b) in (-2,0,2) for a,b in itertools.combinations(F,2)),'full-root pair angles')
    missing=sorted(set(F)-set(R));need(len(missing)==9,'nine omitted roots')
    K=[sum(int(i==j or dot(a,b)==0)<<j for j,b in enumerate(R)) for i,a in enumerate(R)]
    pivot=92;h=K[pivot]
    A=[r & (h if h>>j&1 else ~h) for j,r in enumerate(K)]
    C=basis(K);Q=basis(C+[h&c for c in C])
    need(len(C)==9 and len(Q)==16 and len(basis(A))==15 and len(basis(A+C))==16,'fitting and enlargement ranks')
    need(all(row>>j&1 and not(row&~K[j]) for j,row in enumerate(A)),'native fitting mask')
    root=R[pivot];data=[]
    for j,row in enumerate(A):
        S=[t for t in range(111) if t!=j and row>>t&1]
        drop=next(a for a,x in enumerate(R[j]) if x)
        projected=[tuple(x for a,x in enumerate(R[t]) if a!=drop) for t in S]
        need(rank(projected)==7,'all foreign supports span receiver facet')
        quad=[tuple(v[a]*v[b] for a in range(7) for b in range(a,7)) for v in projected]
        entry=dict(receiver=j,foreign_support=S,foreign_rank=7)
        if j==pivot:
            need(rank(quad)==28,'canonical full quadratic span')
            entry.update(chi=2,reason='full quadratic rank28')
        elif dot(root,R[j])==0:
            common=[t for t in S if t!=pivot]
            need(all(dot(R[t],root)==dot(R[t],R[j])==0 for t in common),'orthogonal common flat')
            need(rank([R[t] for t in common])==6,'common flat spans rank6')
            entry.update(chi=1,reason='common rank6 flat plus pivot line',cover=[common,[pivot]],normals=[list(root),None])
        else:
            full=[r for r in F if dot(r,R[j])==0 and dot(r,root)!=0]
            need(len(full)==27,'full exclusive configuration size27')
            holes=[r for r in full if r not in R]
            if holes:
                z=holes[0];z=tuple((1 if dot(root,z)>0 else -1)*x for x in z)
                w=tuple(x-y for x,y in zip(z,root))
                need(dot(z,root)==2 and dot(z,z)==dot(w,w)==4,'oriented missing-root normals')
                need(rank([R[j],z])==rank([R[j],w])==2,'proper chart normals')
                left=[t for t in S if dot(R[t],z)==0];right=[t for t in S if t not in left]
                need(all(dot(R[t],w)==0 for t in right),'two missing-root charts cover all contacts')
                entry.update(chi=1,reason='omitted-root two-distance cover',cover=[left,right],normals=[list(z),list(w)],omitted_roots=[list(r) for r in holes])
            else:
                need(len(S)==27 and rank(quad)==27,'complete exclusive quadratic span27')
                # On the facet, Q(x)=||x||²-(root.x)² has rank7: the
                # root projection has squared norm3, giving eigenvalues
                # 1 six times and -2 once. This is a proof, not a numeric
                # eigenvalue check. All source roots satisfy Q=0 exactly.
                need(all(dot(R[t],R[t])==dot(root,R[t])**2 for t in S),'rank7 vanishing form')
                need(dot(root,R[j])**2==4,'projection squared norm3')
                entry.update(chi=2,reason='unique rank7 vanishing quadratic')
        data.append(entry)
    need(sum(d['chi'] for d in data)==120,'total proper-cover charge120')
    need([d['receiver'] for d in data if d['chi']==2]==[21,33,45,51,68,76,84,92,99],'nine irreducible rows')
    out=dict(status='PASS_AUTHOR_PIVOT92_ROOT_GEOMETRY',source_path=NATIVE,source_sha256=PIN,pivot=pivot,fitting_rank=15,canonical_enlargement_rank=16,canonical_quotient_dimension=7,chi=120,chi_histogram=dict(Counter(d['chi'] for d in data)),completed_root_count=120,omitted_roots=[list(r) for r in missing],rows=data,new_complete_kappa=False,physical_word_constructed=False)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','omitted_roots')}))

if __name__=='__main__':main()
