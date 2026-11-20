#!/usr/bin/env python3
"""Independent feedback inverse-formula and native partition-join review."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256,shake_256
from itertools import combinations
from pathlib import Path
import importlib.util,json
from ast import literal_eval
import numpy as np

def need(ok,message):
    if not ok:raise ValueError(message)

ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
b=args.repo/'research/moonshot-005-program/results'
spec=importlib.util.spec_from_file_location('root_geometry',b/'bit-coupled-native-geometric-h-source/review-b/construct.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ctx=m.context(args.repo,args.out/'arithmetic');F,f=ctx.field,ctx.arith
data=json.loads((b/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text());nodes=data['H_nodes']
rec=[i for i in range(111)if ctx.H[263]<=ctx.perp[i]];need(len(rec)==33,'actual receiver list')
donors=[0,61,62];Ks={};coefficient_hashes={}
for j in donors:
    V=np.zeros((3,48),dtype=np.uint8)
    for s in (3,6,7,9,10,11,12,13,15):V[:,3*s:3*s+3]=np.frombuffer(shake_256(f'native-polynomial-feedback/{j}/0/{s}'.encode()).digest(9),dtype=np.uint8).reshape(3,3)&63
    V[:,9:12]=[[0,1,0],[0,0,1],[1,0,0]];V[:,18:21]=np.diag([1,0,0])
    qs={h:np.kron(np.array([[f.power(nodes[h],p)for p in range(16)]],dtype=np.uint8),np.eye(3,dtype=np.uint8))^F.product[f.power(nodes[h],16)^1,V]for h in ctx.stars[j]}
    coefficient_hashes[j]=sha256(b''.join(qs[h].tobytes()for h in sorted(qs))).hexdigest();Ks[j]={}
    for i in rec:
        hs=ctx.views[j,i];need(263 in hs and len(hs)==16,'actual source view')
        off=[h for h in hs if h!=263];g=np.array(f.polynomial([nodes[h]for h in off]),dtype=np.uint8)
        P=np.array(f.polynomial([nodes[h]for h in hs]),dtype=np.uint8);C=P[:16].copy();C[0]^=1
        C=np.kron(C[:,None],np.eye(3,dtype=np.uint8));K0=np.kron(g[:,None],np.eye(3,dtype=np.uint8))
        K=K0^F.mm(C,F.mm(V,K0));E=np.vstack([qs[h]for h in off])
        need(not np.any(F.mm(V,C))and not np.any(F.mm(E,K)),'square-zero inverse fibre formula')
        need(F.rank(K)==3 and F.rank(E)==45 and F.rank(F.mm(qs[263],K))==3,'entire correct kernel and source cut')
        Ks[j][i]=K
join=lambda j,ss:F.rank(np.hstack([Ks[j][i]for i in ss]))
need(all([join(j,ss)for j in donors]==[6,6,6]for ss in combinations(rec,2)),'all proper pairs')
bad=[];hist=Counter()
for ss in combinations(rec,3):
    ranks=[join(j,ss)for j in donors];hist[str(ranks)]+=1
    if len(set(ranks))!=1:bad.append([list(ss),ranks])
expected=[[[52,73,98],[9,8,8]],[[53,75,96],[9,8,9]],[[54,74,98],[9,8,9]]]
need(bad==expected,'all minimal witnesses reconstructed independently')
union=[52,53,54,73,74,75,96,98];need([join(j,union)for j in donors]==[24,21,23],'combined witness')
rr=[84,85,86,87,92,93,94,95,96,97,98,99];R=F.null(np.hstack([Ks[0][i]for i in rr]));need(R.shape==(36,6),'six complete relations')
twist_ranks=[]
for s in range(6):
    blocks=[]
    for n,i in enumerate(rr):
        B=Ks[61][i].copy()
        for _ in range(s):B=F.product[B,B]
        blocks.append(F.product[B[:,:,None,None],R[3*n:3*n+3][None,None,:,:]].transpose(0,3,1,2).reshape(288,9))
    E=np.hstack(blocks);twist_ranks.append(F.rank(E))
need(twist_ranks==[108]*6,'all relative Frobenius transports excluded')
author=json.loads((Path(__file__).parents[1]/'output/RESULT.json').read_text())
need({str(j):v for j,v in coefficient_hashes.items()}==author['literal_source_sha256'],'same pinned sources, different fibre bases')
need(hist==Counter({str(list(literal_eval(k))):v for k,v in author['all_receiver_triples'].items()}),'complete triple histogram agrees')
result={'status':'PASS_ROOT_INDEPENDENT_FEEDBACK_PARTITION_REVIEW','source_cuts':99,'receiver_pairs':528,'receiver_triples':5456,'minimal_witnesses':bad,'union_rank_profile':[24,21,23],'six_transport_ranks':twist_ranks,'method':'explicit square-zero inverse fibres; C-field elimination; no new author executable import','new_complete_kappa':False}
(args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
