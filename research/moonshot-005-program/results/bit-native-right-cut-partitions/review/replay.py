#!/usr/bin/env python3
"""Forward coefficient extraction on each genuine D-input alphabet."""
import argparse,hashlib,importlib.util,json
from functools import lru_cache
from pathlib import Path
import numpy as np

def run(args):
    spec=importlib.util.spec_from_file_location('independent_cascade',args.canonical/'check.py')
    runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    alg=runner.load_replay(args.replay);engine=runner.Engine(args.stream_lib);alg.mm=engine.mm
    nat=alg.Native(args);E=np.eye(480,dtype=np.uint8);w=json.loads(args.labels.read_text());out={}
    @lru_cache(maxsize=156)
    def sections(i,j,mode,facet):
        ds=[d for d,S in enumerate(nat.D)if j in S and i in nat.D[nat.dual[d]]]
        assert len(ds)==60;message={};n=0
        for d in ds:
            ids=[u for u in nat.byd[d]['X']+nat.byd[d]['Y']if nat.rt[u][5]in nat.planes[i]]
            assert len(ids)==8
            for u in ids:message[u]=E[n];n+=1
        _,_,rs,minimum=nat.facet(message,i,mode);mat=minimum if facet=='min'else rs
        full=np.hstack([mat,E]);m=len(mat)
        for k in range(m):
            hit=np.flatnonzero(full[k:,k]);assert len(hit)
            v=k+int(hit[0]);full[[k,v]]=full[[v,k]];full[k]=alg.MUL[alg.INV[full[k,k]],full[k]]
            q=full[:,k].copy();q[k]=0;full^=alg.MUL[q[:,None],full[k,None,:]]
        assert np.array_equal(full[:,:m],E)
        return {d:full[8*q:8*q+8,m:].copy()for q,d in enumerate(ds)}
    for case,record in sorted(w['cases'].items()):
        mode,facet=case.split('_');ranks=[];hashes=[]
        for i in w['receivers']:
            Q=np.vstack([sections(i,j,mode,facet)[d]for j,d in record['labels']])
            ranks.append(len(alg.echelon(Q)[0]));hashes.append(hashlib.sha256(Q.tobytes()).hexdigest())
        assert ranks==record['ranks'];out[case]={'ranks':ranks,'stack_sha256':hashes}
        print(case,ranks,flush=True)
    args.out.mkdir(exist_ok=True,parents=True);(args.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','canonical','replay','h-words','d-words','k-words','f-words','stream-lib','labels','out'):p.add_argument('--'+n,type=Path,required=True)
    run(p.parse_args())
