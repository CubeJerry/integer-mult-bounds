#!/usr/bin/env python3
"""Exact fixed-code comparison, not a physical dominance claim."""
import json,hashlib
from pathlib import Path
here=Path(__file__).resolve().parent
p=next(q for q in here.parents if (q/'STATE.json').exists())
source=p/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
roots=json.loads(source.read_text())['native_roots'];b0=[0,0,1,1,0,0,1,-1]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
h=[((dot(roots[72],r)+dot(b0,r))//2)%2 for r in roots]
C=[sum(1<<j for j,s in enumerate(roots)if i==j or dot(r,s)==0)for i,r in enumerate(roots)]
W=[row&sum(1<<j for j in range(111)if h[j]==h[i])for i,row in enumerate(C)]
def rank(rows):
    b={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in b:x^=b[k]
            else:b[k]=x;break
    return len(b)
assert rank(C)==9 and rank(W)==15
base=p/'results/bit-coupled-singular-delivery/worker-a/two-receiver-output'
result={}
for name in ['COUPLED-WORD.json','UNCOPLED-WORD.json']:
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    for o in json.loads((base/name).read_text())['operations']:
        if o[0]=='INIT':v[o[1]]=0
        elif o[0]=='ADD':v[o[2]]^=v[o[1]]
        elif o[0]=='CLEAR':del v[o[1]]
    G=[v[f'P{i}']for i in range(8)]+[1<<j for j in [16,19,38,49,50,56,57]]
    frames=[[0,15,31,35,40,41,106,110],[0,22,23,30,32,60,61,107]]
    result[name]={'word_sha256':hashlib.sha256((base/name).read_bytes()).hexdigest(),'rank_G':rank(G),'fixed_W_gap':rank(G+W)-rank(G),'fixed_C_gap':rank(G+C)-rank(G),'frame_ranks':[rank([sum(((x>>j)&1)<<i for i,j in enumerate(F))for x in G])for F in frames]}
assert [(result[n]['fixed_W_gap'],result[n]['fixed_C_gap'])for n in result]==[(8,9),(7,8)]
assert all(x['frame_ranks']==[5,5]and x['rank_G']==15 for x in result.values())
out={'status':'PASS_EXACT_SOURCE_VARIANT_COMPARISON','variants':result,'scope':'Fixed-code enlargement and exact frame ranks; source words independently replayed elsewhere. No physical decoder dominance or new kappa.'}
(here/'SOURCE-VARIANT-COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
