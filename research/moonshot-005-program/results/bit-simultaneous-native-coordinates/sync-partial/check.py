#!/usr/bin/env python3
"""Exact integer Y-only review of simultaneous per-donor delivery to all neighbouring terminals."""
import argparse
import gzip
import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import maximum_flow, breadth_first_order


def require(test,msg):
    if not test:raise ValueError(msg)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--layout',type=Path,required=True);cli.add_argument('--factor',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();raw=gzip.decompress(args.layout.read_bytes());w=json.loads(raw)
    require(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native layout')
    f=json.loads(args.factor.read_bytes());den=f['denominator'];t=dict(f['factors']);L=12*den
    H=[set(h)for h in w['A2']];D=[set(d)for d in w['D4']];R=w['root_table'];dual=w['dual_D4']
    N=[set(i for i in range(111)if sum(a*b for a,b in zip(R[i],R[j]))==0)for j in range(111)]
    middle=[set()for _ in D]
    for _,d,h,*_ in w['routes']:
        if h is not None:middle[d].add(h)
    native=set(range(111));sizes=[len(h&native)for h in H]
    he=[(6//m*den if m else 0)+t.get(h,0) for h,m in enumerate(sizes)]
    sy=[max(4*den-x,0) for x in he];hx=[a*b for a,b in zip(he,sizes)]
    require(den==2 and min(L-x for x in hx)>=6 and all(len(s)==16 for s in middle),'routing contract')
    results=[]
    for j in range(111):
        src=0;off_h=1;off_d=off_h+len(H);off_k=off_d+len(D);off_i=off_k+len(H)
        sink=off_i+111;node_count=sink+1
        hs={h for h,q in enumerate(H) if j in q}
        ds={d for d,q in enumerate(D) if j in q}
        ks=set.union(*(middle[dual[d]]for d in ds))
        rows=[];cols=[];values=[]
        def edge(u,v,c):
            if c:
                rows.append(u);cols.append(v);values.append(c)
        for h in hs:edge(src,off_h+h,45*sy[h])
        for d in ds:
            for h in hs&middle[d]:edge(off_h+h,off_d+d,L-hx[h])
            for k in middle[dual[d]]:edge(off_d+d,off_k+k,hx[k])
        for k in ks:
            for i in H[k]&N[j]:edge(off_k+k,off_i+i,45*he[k])
        def flow(k, audit=False):
            rr=rows+[off_i+i for i in sorted(N[j])]
            cc=cols+[sink]*len(N[j]);vv=values+[k]*len(N[j])
            g=coo_matrix((vv,(rr,cc)),shape=(node_count,node_count),dtype=np.int64).tocsr()
            f=maximum_flow(g,src,sink)
            value=int(f.flow_value)
            if audit:
                arcs=g.tocoo()
                used=np.asarray(f.flow[arcs.row,arcs.col]).ravel()
                require(np.all(used>=0) and np.all(used<=arcs.data),'primal capacity')
                divergence=np.asarray(f.flow.sum(axis=1)).ravel()
                expected=np.zeros(node_count,dtype=np.int64);expected[src]=value;expected[sink]=-value
                require(np.array_equal(divergence,expected),'primal conservation')
                residual=g-f.flow
                residual.eliminate_zeros()
                reached=breadth_first_order(residual,src,directed=True,return_predecessors=False)
                source_side=np.zeros(node_count,dtype=bool);source_side[reached]=True
                cut=int(arcs.data[source_side[arcs.row]&~source_side[arcs.col]].sum())
                require(not source_side[sink] and cut==value,'residual dual cut')
            return value
        cap=sum(45*sy[h]for h in hs);n=len(N[j])
        a,b=0,cap//n+1
        while b-a>1:
            m=(a+b)//2
            if flow(m)==m*n:a=m
            else:b=m
        fv=flow(a,audit=True);nextv=flow(a+1,audit=True)
        require(fv==a*n and nextv<(a+1)*n,'strict exact max-flow bracket')
        results.append({'donor':j,'neighbours':n,'real_Y_inlets':cap,'maximum_common_independent_outputs':a,'flow_at_threshold':fv,'flow_at_next':nextv})
    hist=Counter(r['maximum_common_independent_outputs']for r in results)
    result={'base_layout_sha256':hashlib.sha256(raw).hexdigest(),'factor_sha256':hashlib.sha256(args.factor.read_bytes()).hexdigest(),
            'baseline_paid_field_slots_per_role':5760,'late_local_maps_only':True,'verified_primal_flows_and_equal_capacity_cuts':222,'adjacent_donor_receiver_pairs':sum(map(len,N)),
            'uniform_native_row_count':min(hist),'per_donor_thresholds_histogram':dict(sorted(hist.items())),'results':results}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('all-111 globally synchronized output row lower bound',min(hist),'max',max(hist),'per donor',sorted(hist.items()))

if __name__=='__main__':
    main()
