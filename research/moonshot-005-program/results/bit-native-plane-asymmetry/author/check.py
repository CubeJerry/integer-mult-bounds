#!/usr/bin/env python3
"""Exact odd native witnesses and sharp seventeen-term square-zero controls."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path

def need(ok, message):
    if not ok:raise ValueError(message)

def bits(x):
    while x:
        b=x&-x;yield b.bit_length()-1;x-=b

def echelon(vectors):
    basis={}
    for v in vectors:
        while v:
            p=v.bit_length()-1
            if p in basis:v^=basis[p]
            else:basis[p]=v;break
    return basis

def reduce(v,basis):
    while v:
        p=v.bit_length()-1
        if p not in basis:return v
        v^=basis[p]
    return 0

def multiply(A,B):
    return [__import__('functools').reduce(int.__xor__,(B[j] for j in bits(r)),0) for r in A]

def add(A,B):return [a^b for a,b in zip(A,B)]
def identity(n):return [1<<j for j in range(n)]
def outer(u,v,n):return [v if u>>j&1 else 0 for j in range(n)]

def tensor(A,s):
    return [sum(1<<(j*s+t) for j in bits(row)) for row in A for t in range(s)]

def simplex_controls(s):
    n=16;ones=(1<<n)-1;Ns=[]
    for h in range(17):
        u=(1<<h) if h<16 else ones
        v=((1<<h)^ones) if h<16 else ones
        w=(1<<h) if h<16 else 1
        N=tensor(outer(u,v,n),s);E=tensor(outer(u,w,n),s);F=tensor(outer(u,w^v,n),s)
        need(multiply(N,N)==[0]*(n*s),'square-zero')
        need(len(echelon(N))==s,'rank-s discrepancy')
        need(multiply(E,E)==E and multiply(F,F)==F,'paired idempotents')
        need(multiply(E,F)==F and multiply(F,E)==E,'common image projections')
        need(add(E,F)==N,'difference of the projections')
        Ns.append(N)
    total=[0]*(n*s)
    for N in Ns:total=add(total,N)
    need(total==identity(n*s),'seventeen-term identity')
    for N in Ns:
        remaining=add(total,N)
        need(multiply(remaining,remaining)==identity(n*s),'all sixteen-term complements invertible')
        need(remaining!=identity(n*s),'a deleted term breaks identity')
    wrong=tensor(outer(1,1,n),s)
    need(multiply(wrong,wrong)!=[0]*(n*s),'wrong self-factor is not square-zero')
    return {'internal_width':s,'bank_dimension':n*s,'terms':17,'all_term_ranks':s,'total_rank':17*s,'all_sixteen_term_complements_invertible':True,'projection_realizations':True,'deletion_control_rejected':True,'wrong_square_zero_control_rejected':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    pg=a.repo/'research/moonshot-005-program'
    native=pg/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    layout=pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    factor=pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json'
    raw=native.read_bytes();lraw=gzip.decompress(layout.read_bytes());fraw=factor.read_bytes()
    need(sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
    need(sha256(lraw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    need(sha256(fraw).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7','factor pin')
    obj=json.loads(lraw);R=obj['root_table'];A=obj['A2'];fac=dict(json.loads(fraw)['factors']);native_mask=(1<<111)-1
    need(R[:111]==json.loads(raw)['native_roots'] and len(A)==1120,'native/root geometry match')
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    O=[sum(1<<j for j,r in enumerate(R) if dot(r,s)==0) for s in R]
    masks=[sum(1<<j for j in H) for H in A]
    singleton={next(j for j in H if j<111):masks[h] for h,H in enumerate(A) if sum(j<111 for j in H)==1}
    need(len(singleton)==11,'eleven singleton source planes')
    weights=[]
    for h,H in enumerate(A):
        m=sum(j<111 for j in H)
        need(h not in fac or m==3,'factor support')
        x=12//m+fac.get(h,0) if m else 0
        need((m==1 and max(8,x)==12) or (m!=1 and max(8,x)==8),'source bundle capacity')
        weights.append(max(8,x))
    witnesses=[];nos=[];tight_count=0
    for i in range(111):
        T=O[i]&native_mask
        for j,hm in singleton.items():
            if hm&O[i]==hm:T&=~(1<<j)
        visible=[h for h,hm in enumerate(masks) if hm&O[i]==hm]
        for j in bits(T):
            pen=[h for h in visible if j in A[h]]
            need(len(pen)==16 and sum(weights[h] for h in pen)*45==5760,'tight sixteen-coordinate source')
        tight_count+=T.bit_count();columns=[masks[h]&T for h in visible];basis=echelon(columns);res=reduce(T,basis)
        if not res:nos.append(i);continue
        witness=1<<(res.bit_length()-1)
        for p,v in sorted(basis.items()):
            if (witness&v).bit_count()%2:witness^=1<<p
        need(witness&T==witness and witness.bit_count()%2==1,'odd tight donor witness')
        paired=[]
        for h in visible:
            count=(masks[h]&witness).bit_count()
            need(count in (0,2),'even plane intersection')
            if count==2:paired.append([h,list(bits(masks[h]&witness))])
        need(len(paired)*2==16*witness.bit_count(),'all sixteen donor incidences paired')
        witnesses.append({'receiver':i,'tight_donors':list(bits(T)),'odd_donors':list(bits(witness)),'paired_planes':paired})
    need(len(witnesses)==87 and len(nos)==24 and tight_count==6110,'native witness and tight-pair census')
    data=(json.dumps({'schema':'odd-native-plane-witness-v1','witnesses':witnesses,'no_odd_witness_receivers':nos},sort_keys=True,separators=(',',':'))+'\n').encode()
    receipt={'status':'PASS_NATIVE_ODD_WITNESSES_AND_SHARP_PLANE_ASYMMETRY','native_sha256':sha256(raw).hexdigest(),'layout_uncompressed_sha256':sha256(lraw).hexdigest(),'factor_sha256':sha256(fraw).hexdigest(),'witnesses_uncompressed_sha256':sha256(data).hexdigest(),'receivers_with_odd_witness':87,'receivers_without_this_witness':nos,'tight_source_pairs':tight_count,'witness_size_histogram':dict(sorted(Counter(len(w['odd_donors']) for w in witnesses).items())),'minimum_distinct_nonzero_differences_per_witness':17,'inequality':'sum rank(N_H) >= 16s + max rank(N_H)','simplex_controls':[simplex_controls(s) for s in (1,2)],'scope':'Aligned quotient-source interface only; no completed native embedding, movement surcharge, or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'WITNESSES.json.gz').write_bytes(gzip.compress(data,mtime=0));(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
if __name__=='__main__':main()
