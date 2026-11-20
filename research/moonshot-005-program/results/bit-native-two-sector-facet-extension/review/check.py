#!/usr/bin/env python3
"""Authenticate the six large-sector native terminals and their quotient equations."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
def run(p):
    a=Atlas(p.repo,p.k,p.d,p.lib);mm=a.ops.matmul;w=384
    z=np.load(p.quotient);K=np.load(p.data/'K.npz')['K'];assert list(z['roles'])==list(range(8))
    assert np.array_equal(mm(z['qe'],K),z['qa']);d=[]
    for i in range(6):
        e,E,y,Y=a.facet(i);selectE=np.flatnonzero(E[96:].any(axis=0));selectY=np.flatnonzero(Y[96:].any(axis=0))
        ei=np.array([e[t]for t in selectE]);yi=np.array([y[t]for t in selectY]);F=np.hstack([E[96:,selectE],Y[96:,selectY]])
        raw=np.load(p.data/f'S{i}.npz');assert np.array_equal(ei,raw['e']) and np.array_equal(yi,raw['y'])and np.array_equal(F,raw['fold'])
        demand=K[i*w:(i+1)*w].copy();demand[:,i*w:(i+1)*w]^=np.eye(w,dtype=np.uint8)
        assert np.array_equal(mm(F,raw['sens']),demand)
        pending={t for h in a.ks[i]for ph,src,dst in a.kr[str(h)]['stripes']if len(src)==36 for t in dst if (a.route[t][1]if ph=='Y'else a.route[t][7])==i}
        assert pending==set(ei)|set(yi)
        d.append({'i':i,'actual_early':len(ei),'actual_late':len(yi),'raw_F_sha256':hashlib.sha256(F.tobytes()).hexdigest(),'Schur_action_sha256':hashlib.sha256(demand.tobytes()).hexdigest()})
    p.out.mkdir(exist_ok=True,parents=True);(p.out/'RESULT.json').write_text(json.dumps({'native_field':67,'quotient_K_sha256':hashlib.sha256(K.tobytes()).hexdigest(),'all_quotient_equations':3072**2,'six_observer_equations':6*384*3072,'actual_facets':d},indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('repo','h','d','k','lib','quotient','data','out'):p.add_argument('--'+n,type=Path,required=True)
 x=p.parse_args();sys.path.insert(0,str(x.h));from transfer import Atlas;run(x)
