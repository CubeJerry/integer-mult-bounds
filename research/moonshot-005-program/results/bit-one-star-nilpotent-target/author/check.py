#!/usr/bin/env python3
"""Explicit one-receiver nilpotent target. Algebraic, not a physical code."""
import argparse
import hashlib
import json
from pathlib import Path

def rank(rows):
    pivots={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in pivots: pivots[p]=x; break
            x ^= pivots[p]
    return len(pivots)

def action(rows,x): return sum(((row & x).bit_count()%2) << i for i,row in enumerate(rows))

def allocation(width,neighbors):
    w=(width+61)//62
    assert w>=2 and width>w
    U=list(range(width-w,width)); outside=list(range(width-w)); ports=sorted(neighbors)
    V={j:[None]*w for j in ports}
    # On U these are the open Jordan path and its single closing edge.
    for k in range(w-1): V[ports[0]][k]=U[k+1]
    V[ports[1]][w-1]=U[0]
    pos=0
    for j in ports:
        for k in range(w):
            if V[j][k] is None and pos<len(outside): V[j][k]=outside[pos]; pos+=1
    assert pos==len(outside)
    seen=[v for row in V.values() for v in row if v is not None]
    assert sorted(seen)==list(range(width))
    assert len(set(V[ports[0]]))==w and None not in V[ports[0]]
    J=[1 << (k+1) if k<w-1 else 0 for k in range(w)]
    E=[0]*(w-1)+[1]
    local=[]
    for j in ports:
        vu=[0 if s is None or s not in U else 1 << (s-U[0]) for s in V[j]]
        expect=J if j==ports[0] else E if j==ports[1] else [0]*w
        assert vu==expect
        assert rank([row ^ (1 << k) for k,row in enumerate(vu)])==w
        local.append(vu)
    assert rank([action(J,action(E,1 << k)) ^ action(E,action(J,1 << k)) for k in range(w)])==2
    return U,V,local

def small(width,N,K,a):
    U,V,_=allocation(width,N[a]); delta=[0]*(111*width); canon=[]
    for i in range(111):
        for k in range(width): canon.append(sum(1 << (j*width+k) for j in range(111) if (K[i] >> j)&1))
    for j,selected in V.items():
        for k,s in enumerate(selected):
            if s is not None: delta[a*width+U[k]] ^= 1 << (j*width+s)
    A=[x^y for x,y in zip(canon,delta)]
    h=len(U)
    assert rank(delta)==h and rank(A)==9*width+h and rank(canon+delta)==9*width+h
    # Actual b-by-b foreign blocks, including all their non-U columns.
    for j in N[a]:
        block=[1 << k for k in range(width)]
        for k,s in enumerate(V[j]):
            if s is not None: block[U[k]] ^= 1 << s
        assert rank(block)==width
    assert rank([0 if s is None else 1 << s for row in V.values() for s in row])==width
    return {'width':width,'h':h,'q':9*width+h,'r':h,'foreign_blocks_checked':62,'common_kernel_dimension':0}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    programme=args.repo/'research/moonshot-005-program'
    source=programme/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    budget_path=programme/'results/bit-canonical-quotient-repair/author/output/BUDGET.json'
    roots=json.loads(source.read_text())['native_roots']
    N=[{j for j,y in enumerate(roots) if i!=j and sum(u*v for u,v in zip(x,y))==0} for i,x in enumerate(roots)]
    K=[(1 << i)|sum(1 << j for j in N[i]) for i in range(111)]
    a=80; assert len(N[a])==62 and rank(K)==9
    outside=sum(1 << j for j in range(111) if j not in N[a])
    assert rank([row & outside for row in K])==9
    assert rank([row & (((1 << 111)-1) ^ (1 << a)) for row in K])==9
    controls=[small(b,N,K,a) for b in [64,124,125]]
    b=5760;U,V,_=allocation(b,N[a]);h=len(U);assert h==93
    budget=json.loads(budget_path.read_text())['every_r_zero_through_203'][h]
    compressedU,compressedV,_=allocation(1920,N[a]);assert len(compressedU)==31
    assert 31*5760==93*1920
    pins=[{'path':str(p.relative_to(args.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [source,budget_path]]
    result={'status':'PASS_ONE_STAR_NILPOTENT_TARGET','scope':'algebraic native target; no physical source realization',
            'receiver':a,'degree':62,'width':b,'h':h,'q':9*b+h,'r':h,'all_foreign_blocks_invertible':True,
            'common_left_rows':b-h,'flat_gauge_subsystem_dimension':0,'one_receiver_lower_bound':(b+61)//62,
            'compressed_width':1920,'compressed_h':31,'budget':budget,'small_controls':controls,'source_pins':pins}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'SELECTORS.json').write_text(json.dumps({'receiver':a,'width':b,'U':U,'V':V,'compressed_U':compressedU,'compressed_V':compressedV},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'h':h,'q':9*b+h,'first_even_m':budget['first_even_m']}))
if __name__=='__main__':main()
