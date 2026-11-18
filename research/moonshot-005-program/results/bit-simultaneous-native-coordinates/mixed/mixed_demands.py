#!/usr/bin/env python3
"""Independent full-rank and synchronized-row mixed-demand tests on the balanced DAG."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
from multiprocessing import Pool
import gzip,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import maximum_flow,breadth_first_order
from layout import need

def prepare(w,f):
    global AA,DD,RR,DH,DU,hx,xx,sy,adj,KREQ
    KREQ=5760;AA=[set(a) for a in w['A2']];DD=[set(d) for d in w['D4']];DU=w['dual_D4'];RR=w['root_table'];u=dict(f['factors'])
    nn=[len(a&set(range(111))) for a in AA];xx=[12//m+u.get(h,0) if m else 0 for h,m in enumerate(nn)]
    hx=[m*x for m,x in zip(nn,xx)];sy=[max(8-x,0) for x in xx]
    DH=[set() for d in DD]
    for _,d,h,*_ in w['routes']:
        if h is not None:DH[d].add(h)
    adj=[{i for i,r in enumerate(RR[:111]) if sum(a*b for a,b in zip(RR[j],r))==0} for j in range(111)]

def solve(arg):
    j,k=arg;hs={h for h,a in enumerate(AA) if j in a};ds={d for d,a in enumerate(DD) if j in a};ks=set.union(*(DH[DU[d]] for d in ds));rec=sorted(adj[j]);n=len(rec)
    state={};inds=[]
    for z,ss in [('h',hs),('d',ds),('k',ks),('f',set(rec))]:
        for v in sorted(ss):state[z,v]=len(state)
    layers=len(state);src=2*layers;sink=src+1;t=src+2;ir=[];ic=[];iv=[]
    def add(a,b,c):
        if c:ir.append(a);ic.append(b);iv.append(c)
    for node in range(layers):add(node,node+layers,12000)
    for h in hs:
        tt=state['h',h];add(src,tt,45*xx[h]);add(src,tt+layers,45*sy[h])
    for d in ds:
        dn=state['d',d]
        for h in hs&DH[d]:
            hn=state['h',h];add(hn,dn,hx[h]);add(hn+layers,dn+layers,24-hx[h])
        for v in DH[DU[d]]:
            kn=state['k',v];add(dn,kn,24-hx[v]);add(dn+layers,kn+layers,hx[v])
    for v in ks:
        kn=state['k',v]
        for i in AA[v]&adj[j]:
            fn=state['f',i];add(kn,fn,45*sy[v]);add(kn+layers,fn+layers,45*xx[v])
    terms=[]
    for i in rec:
        idx=len(iv);terms.append(idx);add(state['f',i]+layers,sink,max(1,k))
    # Reuse the compressed matrix graph and locate the exact terminal-sink entries.
    G=coo_matrix((iv,(ir,ic)),shape=(t,t),dtype=np.int32).tocsr();locs=[]
    for i in rec:
        fn=state['f',i]+layers;lo,hi=G.indptr[fn:fn+2];idx=lo+np.searchsorted(G.indices[lo:hi],sink);need(G.indices[idx]==sink,'terminal edge');locs.append(idx)
    rows=[]
    for i,idx in zip(rec,locs):
        G.data[idx]=KREQ;f=maximum_flow(G,src,sink);v=int(f.flow_value);want=KREQ+(n-1)*k
        arcs=G.tocoo();used=np.asarray(f.flow[arcs.row,arcs.col]).ravel()
        need(np.all(used>=0) and np.all(used<=arcs.data),'true directed primal capacities')
        divergence=np.asarray(f.flow.sum(axis=1)).ravel();claimed=np.zeros(t,dtype=np.int64);claimed[src]=v;claimed[sink]=-v
        need(np.array_equal(divergence,claimed),'flow conservation on every physical time-expanded chart')
        if v!=want:
            res=G-f.flow;res.eliminate_zeros();S=breadth_first_order(res,src,directed=True,return_predecessors=False);mark=np.zeros(t,dtype=np.bool_);mark[S]=1
            co=G.tocoo();bound=int(co.data[mark[co.row]&~mark[co.col]].sum());need(bound==v,'dual witness for unsaturated mixed path set')
        rows.append([j,i,v,want]);G.data[idx]=k
    return rows

if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--factor',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--k',type=int,required=True);p.add_argument('--workers',type=int,default=4);p.add_argument('--donors',type=int,default=111);a=p.parse_args();raw=gzip.decompress(a.layout.read_bytes());f=a.factor.read_bytes()
    need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','atlas pin');prepare(json.loads(raw),json.loads(f))
    with Pool(a.workers) as pool:allrows=pool.map(solve,[(j,a.k) for j in range(a.donors)])
    rows=sum(allrows,[]);defects=Counter(target-v for j,i,v,target in rows)
    datum=json.dumps(rows,separators=(',',':')).encode()+b'\n';base=a.out/f'MIXED-{a.k}';a.out.mkdir(exist_ok=True,parents=True);base.with_suffix('.json.gz').write_bytes(gzip.compress(datum,mtime=0))
    result={'k':a.k,'cases':len(rows),'donors':a.donors,'full_rank_request':KREQ,'cases_meeting_all_demands':defects[0],'defects':dict(sorted(defects.items())),'table_sha256':sha256(datum).hexdigest(),'factor_sha256':sha256(f).hexdigest(),'primal_certificates_checked':len(rows),'needed_path_proof_positive':defects[0]==len(rows)}
    base.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
