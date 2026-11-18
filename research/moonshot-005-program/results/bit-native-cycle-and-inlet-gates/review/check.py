#!/usr/bin/env python3
"""Second implementation of the S023 native cycle and source-cut checks."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def binary_rank(rows):
    rows=list(rows)
    pivot=0
    for col in range(111):
        candidates=[i for i in range(pivot,len(rows)) if rows[i]>>col&1]
        if not candidates: continue
        q=candidates[0];rows[pivot],rows[q]=rows[q],rows[pivot]
        for i in range(pivot+1,len(rows)):
            if rows[i]>>col&1: rows[i]^=rows[pivot]
        pivot+=1
    return pivot

PRIME=101
def mm(A,B):
    return [[sum(a*b for a,b in zip(r,c))%PRIME for c in zip(*B)] for r in A]
def eye():return [[1,0],[0,1]]
def inverse(A):
    a,b=A[0];c,d=A[1];v=pow((a*d-b*c)%PRIME,-1,PRIME)
    return [[d*v%PRIME,-b*v%PRIME],[-c*v%PRIME,a*v%PRIME]]
def basis(q):
    return mm([[1,q%PRIME],[0,1]],[[1,0],[(q*q+1)%PRIME,1]])
def rank_mod(rows):
    rows=[r[:] for r in rows];pivot=0
    for c in range(2):
        hit=next((i for i in range(pivot,len(rows)) if rows[i][c]%PRIME),None)
        if hit is None:continue
        rows[pivot],rows[hit]=rows[hit],rows[pivot]
        v=pow(rows[pivot][c],-1,PRIME);rows[pivot]=[x*v%PRIME for x in rows[pivot]]
        for i in range(pivot+1,len(rows)):
            q=rows[i][c];rows[i]=[(a-q*b)%PRIME for a,b in zip(rows[i],rows[pivot])]
        pivot+=1
    return pivot

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    pg=a.repo/'research/moonshot-005-program'
    native=pg/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    factor=pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json'
    nb=native.read_bytes();fb=factor.read_bytes()
    require(sha256(nb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
    require(sha256(fb).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7','factor pin')
    R=[tuple(r) for r in json.loads(nb)['native_roots']]
    dot=lambda u,v:sum(x*y for x,y in zip(u,v))
    N=[{j for j,s in enumerate(R) if dot(r,s)==0} for r in R]
    O=[sum(1<<j for j in n) for n in N];K=[v^(1<<i) for i,v in enumerate(O)]
    require(binary_rank(K)==9 and binary_rank(O)==108,'two native ranks')
    require(all(binary_rank([r&~o for r in K])==9 for o in O),'canonical restriction')
    core=N[0];anc={i:min(N[i]&core) for i in range(1,111)}
    par={j:min(i for i,n in enumerate(N) if j in n) for j in range(111) if j not in core}
    tree={(0,j) for j in core}|set(anc.items())|{(i,j) for j,i in par.items()}
    cycles=[];known=set(tree)
    for iscore in (True,False):
        for i,n in enumerate(N):
            for j in sorted(n):
                if (j in core)!=iscore or (i,j) in tree:continue
                h=0 if iscore else par[j]
                d=anc[i] if iscore else min(core&N[i]&N[h])
                require({(h,j),(h,d),(i,d)}<=known,'three established edges')
                require((i,j) not in known,'unique new edge')
                known.add((i,j));cycles.append((i,j,h,d))
    require(len(tree)==221 and len(cycles)==6249 and len(known)==6470,'native graph dimensions')
    RR=[basis(3*i+2) for i in range(111)];CC=[basis(7*j+4) for j in range(111)]
    positive={(i,j):mm(RR[i],CC[j]) for i in range(111) for j in N[i]}
    def cycle(B,c):
        i,j,h,d=c
        return mm(mm(mm(B[i,j],inverse(B[h,j])),B[h,d]),inverse(B[i,d]))
    require(all(cycle(positive,c)==eye() for c in cycles),'ordered positive products over F101')
    require(any(mm(mm(mm(positive[i,j],inverse(positive[h,j])),inverse(positive[i,d])),positive[h,d])!=eye() for i,j,h,d in cycles[:300]),'reject incorrect multiplication order')
    defect_edge=cycles[-1][:2];defect={(i,j):eye() for i in range(111) for j in N[i]};defect[defect_edge]=[[1,0],[0,2]]
    equations=[]
    for H in defect.values():
        equations.extend([[(H[r][c]-int(r==c))%PRIME for r in range(2)] for c in range(2)])
    require(rank_mod(equations)==1,'exact common fixed space one')
    B={(i,j):mm(mm(RR[i],H),CC[j]) for (i,j),H in defect.items()}
    require(any(cycle(B,c)!=eye() for c in cycles),'detect nontrivial holonomy')
    # This independently constructed common row is preserved by all tree-normalized blocks.
    for (i,j),v in B.items():
        Li=mm([[1,0],[0,0]],inverse(RR[i]))
        require(mm(Li,v)[0]==CC[j][0],'one common row under arbitrary noncommuting gauges')
    # Reflection closure, using exact root addition rather than Gram-triple enumeration.
    full=set(R)
    changed=True
    while changed:
        changed=False
        for x,y in combinations(tuple(full),2):
            d=dot(x,y)
            if abs(d)!=2:continue
            z=tuple(v-(d//2)*u for u,v in zip(x,y))
            if next(v for v in z if v)<0:z=tuple(-v for v in z)
            if z not in full:full.add(z);changed=True
    full=R+sorted(full-set(R));require(len(full)==120,'root completion')
    ix={r:i for i,r in enumerate(full)};planes=set()
    for i,j in combinations(range(120),2):
        d=dot(full[i],full[j])
        if abs(d)!=2:continue
        z=tuple(y-(d//2)*x for x,y in zip(full[i],full[j]))
        if next(v for v in z if v)<0:z=tuple(-v for v in z)
        planes.add(tuple(sorted((i,j,ix[z]))))
    planes=sorted(planes,key=lambda p:sum(1<<j for j in p));require(len(planes)==1120,'A2 count')
    fac=dict(json.loads(fb)['factors']);weight=[]
    for h,H in enumerate(planes):
        m=sum(v<111 for v in H);x=12//m+fac.get(h,0) if m else 0;weight.append((x,max(8,x)))
    e=Counter();tot=Counter()
    for j in range(111):
        pencil=[h for h,H in enumerate(planes) if j in H]
        require(len(pencil)==28 and sum(weight[h][0] for h in pencil)==128,'actual donor slots')
        for i in N[j]:
            visible=[h for h in pencil if all(dot(R[i],full[v])==0 for v in planes[h])]
            require(len(visible)==16,'visible pencil')
            e[45*sum(weight[h][0] for h in visible)]+=1
            tot[45*sum(weight[h][1] for h in visible)]+=1
    require(min(e)==2880 and max(e)==3600 and dict(tot)=={5760:6110,5940:360},'independent inlet census')
    result={'status':'PASS_INDEPENDENT_NATIVE_CYCLE_AND_INLET_REVIEW','geometry_method':'integer reflection closure','matrix_control_field':101,'common_partial_dimension':1,'all_6249_positive_cycles':True,'ordered_product_mutation_rejected':True,'nontrivial_cycle_detected':True,'tree_edges':len(tree),'four_cycles':len(cycles),'early_cut_histogram':dict(sorted(e.items())),'total_cut_histogram':dict(sorted(tot.items())),'canonical_rank':9,'target_rank':108,'review_scope':'Independent mathematical review and fresh second implementations; no materialized balanced coefficient assignment and no new kappa.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
