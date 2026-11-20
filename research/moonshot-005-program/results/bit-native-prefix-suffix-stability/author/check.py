#!/usr/bin/env python3
"""Check weighted rectangle consequences at the genuine shared D input rows."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
import numpy as np
import gzip

def module(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def verify(args):
    a=Atlas(args.repo,args.k,args.d_charts,args.library)
    p=module(args.right_author/'check.py','isolated_right_replay')
    p.unpack=unpack;p.payload=payload;p.K_PINS=K_PINS;p.require=require;p.power=power
    p.Arithmetic=Arithmetic;p.TABLE=TABLE;p.INV=INV;p.coefficients=coefficients;p.k_row=k_row;p.inverse=inverse
    core=p.Right(args);u,v=0,14;J=[1,3,5,7,10,11,12,47]
    g=json.loads(gzip.decompress(args.weighted.read_bytes()) if args.weighted.suffix==".gz" else args.weighted.read_bytes());weights={tuple(z):0 for z in g['tree']}
    for edge,i,l,x,y,clique,c in g['closure']:weights[divmod(edge,111)]=c
    costs=[int(weights[u,j]+weights[v,j])for j in J]
    assert costs==[0,1,1,1,1,1,1,1]
    all_labels=[(j,d)for j in J for d,D in enumerate(a.D)if j in D and {u,v}<=a.D[a.dual[d]]]
    assert len(all_labels)==120;counts=Counter(d for _,d in all_labels);assert len(counts)==45
    reports={}
    for mode in ('spread','mixed'):
        for facet in ('rs','min'):
            A=[]
            for i in (u,v):
                rows=[]
                for j,d in all_labels:
                    M,ids=a.middle_matrix(d)
                    ins=[t for t,k in enumerate(ids)if a.route[k][3] in a.ks[j]]
                    outs=[t for t,k in enumerate(ids)if a.route[k][5] in a.ks[i]]
                    assert len(ins)==len(outs)==8
                    C=M[np.ix_(outs,ins)];Q=core.quotient(i,j,mode,facet)[d]
                    rows.append(a.ops.matmul(inverse(C),Q))
                A.append(np.vstack(rows))
            r0,r1=map(rank_fast,A);joint=rank_fast(np.hstack(A));gap=joint-min(r0,r1)
            assert (r0,r1)==(480,480) and gap>128*sum(costs)//8
            required=max(0,(8*gap-128*sum(costs)+63)//64);maxs=sorted(counts.values(),reverse=True)
            dchange=next(k for k in range(46)if sum(maxs[:k])>=required)
            reports[mode+'_'+facet]={'ranks':[r0,r1,joint],'columns_per_body':480,'rows_per_body':len(A[0]),
                'native_bound_7h':8*gap,'minimum_h':(8*gap+sum(costs)-1)//sum(costs),
                'return_q_at_3840':9*3840+(8*gap+sum(costs)-1)//sum(costs),'minimum_label_changes_if_h128':required,
                'minimum_actual_D_nodes_if_h128':dchange,'native_matrix_sha256':[hashlib.sha256(x.tobytes()).hexdigest()for x in A]}
            print(mode,facet,reports[mode+'_'+facet],flush=True)
    out={'receivers':[u,v],'donors':J,'weights':costs,'shared_45_D_label_multiplicities':dict(counts),'tests':reports}
    args.out.mkdir(exist_ok=True,parents=True);(args.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    pa=argparse.ArgumentParser()
    for n in ('repo','h-author','isolated-author','right-author','k','f','d-charts','weighted','out'):pa.add_argument('--'+n,type=Path,required=True)
    pa.add_argument('--library',type=Path);pa.add_argument('--inverse-library',type=Path);pa.add_argument('--fast-author',type=Path)
    args=pa.parse_args();sys.path.insert(0,str(args.h_author));sys.path.insert(0,str(args.isolated_author))
    from build import require,unpack,power
    from rs_source import coefficients
    from terminal import K_PINS,payload,k_row
    from transfer import Atlas,Arithmetic,INV,TABLE,rank_fast
    from body import inverse
    if args.inverse_library:
        f=module(args.fast_author/'fast.py','portable_inverse');engine=f.Arithmetic(args.inverse_library.resolve());inverse=engine.inverse
    verify(args)
