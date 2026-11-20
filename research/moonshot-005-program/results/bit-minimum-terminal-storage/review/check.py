#!/usr/bin/env python3
"""Review minimum F certificates by directly ranking enlarged singleton systems."""
import argparse
from collections import Counter,defaultdict
import gzip,hashlib,json
import numpy as np
from pathlib import Path

G="9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"
R="6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036"
F="282f16cd16f99f71fe0d2ad6c97c3138e3263be4adf8e46ad9182ebd12146f01"
K={"SPREAD":"513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0",
   "MIXED":"8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a"}
def need(x,s):
    if not x: raise ValueError(s)
def contents(path,h):
    raw=gzip.decompress(path.read_bytes());need(hashlib.sha256(raw).hexdigest()==h,"payload pin")
    return raw
def mult(x,y):
    r=0
    while y:
        if y&1:r^=x
        y>>=1;x<<=1
        if x&64:x^=67
    return r
P=np.array([[mult(x,y)for y in range(64)]for x in range(64)],dtype=np.uint8)
inv=np.array([0]+[list(P[x]).index(1)for x in range(1,64)],dtype=np.uint8)
wt=np.array([sum(mult(a,1<<t).bit_count()for t in range(6))for a in range(64)])
def times(a,b):
    out=np.zeros((len(a),b.shape[1]),dtype=np.uint8)
    for s in range(a.shape[1]):out^=P[a[:,s,None],b[s,None,:]]
    return out
def rank(m):
    v=m.copy(); r=0
    for c in range(v.shape[1]):
        nn=np.flatnonzero(v[r:,c])
        if not len(nn):continue
        k=r+int(nn[0]);v[[r,k]]=v[[k,r]]
        pivot=P[inv[v[r,c]],v[r,c:]]
        v[r+1:,c:]^=P[v[r+1:,c,None],pivot[None,:]]
        r+=1
        if r==len(v):break
    return r
def field_obs(word,row_to_d):
    """Return 45 raw singleton output rows by input owner, before any quotient."""
    chosen=[]; op={}
    for ph,inp,out in word["stripes"]:
        n=len(inp); powers=np.ones((n,n),dtype=np.uint8); nodes=np.arange(1,n+1,dtype=np.uint8)
        for t in range(1,n):powers[t]=P[powers[t-1],nodes]
        for row,u in zip(powers,out):op[u]={w:int(v)for w,v in zip(inp,row)}
        if ph=="Y":chosen+=out[:2*n//3]
    for e,l in word["early_cache_to_late"]:
        for w,v in op[e].items():op[l][w]=op[l].get(w,0)^v
    late=sorted(u for ph,_,out in word["stripes"]if ph=="Y"for u in out)
    order=sorted(chosen)+sorted(set(late)-set(chosen))
    need(len(order)==45 and len(chosen)==30,"irreducible singleton/bands")
    return order,op

def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--k",type=Path,required=True)
    p.add_argument("--f",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();b=a.repo/"research/moonshot-005-program/results"
    geo=json.loads(contents(b/"bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",G))
    corpus=[json.loads(l)for l in contents(b/"bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz",R).splitlines()]
    weights=json.loads(contents(a.f/"WORDS.json.gz",F))
    H=list(map(set,geo["A2"]));D=list(map(set,geo["D4"]));roots=geo["root_table"]
    orth=[{j for j,y in enumerate(roots)if sum(a*b for a,b in zip(x,y))==0}for x in roots]
    native=set(range(111));by_K=defaultdict(list);visits=defaultdict(list);row_to_d={}
    for p,i,c,h,d,k,_,term in corpus:
        oid=(53280 if p=="Y"else 0)+480*i+c
        if k is None:continue
        by_K[k].append(oid);row_to_d[oid]=d
        if term is not None:visits[term,k,p].append(oid)
    result={};states={}
    for mode,kpin in K.items():
        kw=json.loads(contents(a.k/(mode+"-OWNERS.json.gz"),kpin))
        inp=json.loads(json.dumps(weights[mode]));counts=Counter();deficits=Counter();prices=Counter()
        ordinary=extended=0;largest_dim=0;negative=None
        for i,w_list in inp:
            rank_cap=len(w_list);w=np.array(w_list,dtype=np.uint8)
            es=[];ys=[];sing=None;eo=[];yo=[]
            for h,P0 in enumerate(H):
                if i not in P0:continue
                early=sorted(visits[i,h,"X"]);late=sorted(visits[i,h,"Y"])
                if early:
                    need(len(early)==len(late)==15,"normal dual bands")
                    es.append(h);eo+=early
                if len(late)==45:
                    order,M=field_obs(kw[str(h)],row_to_d);sing=(h,len(ys),M,order)
                    need(set(order)==set(late),"singleton actual late owners")
                    late=order
                ys.extend([h]*(len(late)//15));yo+=late
            need(len(ys)==32 and len(set(yo))==480 and set(yo)==set(range(53280+480*i,53280+480*(i+1))),"all Ys")
            ne=len(es);need(len(set(eo))==15*ne,"all early Ys' actual X counterparts")
            C=inv[np.arange(rank_cap)[:,None]^(32+np.arange(ne)[None,:])]
            U=P[inv[np.arange(32)[:,None]^(32+np.arange(rank_cap)[None,:])],w[None,:]]
            S=times(U,C); m=0
            prices["snapshot_add"]+=15*int(wt[C].sum())
            prices["late_add"]+=15*int(wt[U].sum())
            for j in sorted(orth[i]&native):
                lc=[s for s,h in enumerate(ys)if H[h]<=orth[j]]
                ec=[s for s,h in enumerate(es)if H[h]<=orth[j]]
                missing=[s for s in range(32)if s not in lc]
                d=len(ec);deficits[15*d]+=1; m=max(m,d)
                if sing is None or sing[1]not in lc:
                    n=S[np.ix_(missing,ec)]
                    need(n.shape==(d,d)and rank(n)==d,"ordinary direct elimination")
                    ordinary+=1
                    continue
                h,t,M,order=sing;keep=missing+list(range(t,t+3));sz=15*d+30
                obs=sorted(u for u in by_K[h]if j in D[row_to_d[u]])
                need(len(obs)==30 and len(keep)*15==sz,"raw unquotiented square")
                z=np.zeros((sz,sz),dtype=np.uint8)
                eye=np.eye(15,dtype=np.uint8)
                z[:,:15*d]=np.kron(S[np.ix_(keep,ec)],eye)
                z[-45:,15*d:]=np.array([[M[u].get(v,0)for v in obs]for u in order],dtype=np.uint8)
                need(rank(z)==sz,"full raw singleton system")
                if negative is None:
                    mutant=z.copy();mutant[:,:15]=0
                    rr=rank(mutant)
                    need(rr<=sz-15,"lost capture stripe")
                    negative={"rows":sz,"positive_rank":sz,"delete_one_15_channel":rr}
                extended+=1;largest_dim=max(largest_dim,sz)
            need(m==rank_cap,"a native donor witnesses each allocated maximum")
            counts[15*m]+=1
        need((ordinary,extended)==(6110,360),"all foreign pairs")
        need(counts=={225:5,240:106}and deficits=={180:488,195:2010,210:2515,225:1269,240:188},"minima")
        result[mode]={"direct_ordinary_checks":ordinary,"direct_unreduced_singleton_systems":extended,
                      "maximum_singleton_system_size":largest_dim,"minimum_widths":dict(counts),
                      "minimum_field_count":sum(x*y for x,y in counts.items()),"deficits":dict(deficits),
                      "bank3840_capture_ADD":8*prices["snapshot_add"],"bank3840_delivery_ADD":8*prices["late_add"],
                      "bank3840_INIT_dirty_CLEAR":8*6*sum(x*y for x,y in counts.items()),"control":negative}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(result)
if __name__=="__main__":main()
