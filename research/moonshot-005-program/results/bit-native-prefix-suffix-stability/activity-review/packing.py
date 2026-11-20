#!/usr/bin/env python3
"""Exact per-native-star packing bounds when every ordinary contact can lose one D."""
from pathlib import Path
import sys,argparse,gzip,json,itertools,hashlib
from collections import Counter
def packsets(candidates):
    n=len(candidates);masks=[m for d,m in candidates];compat=[0]*n
    for a in range(n):
        for b in range(a+1,n):
            if not(masks[a]&masks[b]):compat[a]|=1<<b
    cnt=Counter();witness=[]
    def visit(p,chosen):
        nonlocal witness
        cnt[len(chosen)]+=1
        if len(chosen)>len(witness):witness=chosen.copy()
        while p:
            b=p&-p;s=b.bit_length()-1;p^=b;visit(p&compat[s],chosen+[s])
    visit((1<<n)-1,[]);return dict(cnt),[candidates[r][0] for r in witness]
def main(p):
    base=p.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';raw=gzip.decompress(base.read_bytes());assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72';L=json.loads(raw);D=[set(x)&set(range(111))for x in L['D4']];opp=[D[q]for q in L['dual_D4']];bad={(7,80),(10,81),(80,96),(81,95)};bad|={(j,i)for i,j in bad}
    W={}
    for j in range(111):
        exc={i for i,q in bad if q==j}
        poss=[(d,sum(1<<i for i in opp[d]-exc))for d in range(3150)if j in D[d]]
        hist,wt=packsets(poss);W[j]={'max':len(wt),'histogram':hist,'saturating_local_family':wt}
        if j%15==0:print(j,len(wt),hist,flush=True)
    # D -> D^perp sends these same local packing bounds to the receiver side,
    # since the exceptional contact list is symmetric.
    n=sum(w['max']for w in W.values());mi=min(map(len,D));print('per-star sum',n,'minD',mi,'dead upper',n//mi,flush=True)
    price=json.loads(p.weights.read_text());v=price['weights'];assert len(v)==111 and all(type(k)is int and k>=0 for k in v)
    used=2*sum(v[j]*W[j]['max']for j in W);low=min(sum(v[j]for j in D[d])+sum(v[i]for i in opp[d]) for d in range(3150))
    assert low==price['minimum_per_D'] and used==price['twice_weighted_native_star_capacity'] and used//low==price['dead_D_upper']==40
    print('exact weighted local family bound',used,low,used//low,flush=True)
    p.out.mkdir(exist_ok=True,parents=True);(p.out/'STAR-PACK.json').write_text(json.dumps({'donor_and_receiver_limits':W,'sum':n,'minimum_native_D_size':mi,'uniform_coarse_dead_bound':n//mi},sort_keys=True,indent=1)+'\n')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--weights',type=Path,default=Path(__file__).parent/'output/STAR-COVER.json');main(a.parse_args())
