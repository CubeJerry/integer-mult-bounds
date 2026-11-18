#!/usr/bin/env python3
"""Exact physical flow witnesses for seventy mixed native coordinates."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import maximum_flow,breadth_first_order

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR_HASH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
B=5760
def need(q,msg):
    if not q:raise ValueError(msg)
def mask(q):return sum(1<<i for i in q)
def bits(z):
    while z:
        b=z&-z;yield b.bit_length()-1;z^=b
def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--factor',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--k',type=int,default=70);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    lr=gzip.decompress(a.layout.read_bytes());fr=a.factor.read_bytes();need(sha256(lr).hexdigest()==LAYOUT_HASH and sha256(fr).hexdigest()==FACTOR_HASH,'source pins');w=json.loads(lr);f=json.loads(fr);need(f['denominator']==2,'balanced scale');u=dict(f['factors']);R=w['root_table'];A=list(map(mask,w['A2']));D=list(map(mask,w['D4']));native=(1<<111)-1
    F=[mask(j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R];dindex={d:i for i,d in enumerate(D)};dual=[]
    for d in D:
        q=(1<<120)-1
        for j in bits(d):q&=F[j]
        dual.append(dindex[q])
    need(dual==w['dual_D4'],'recomputed D4 complements');DH=[{h for h,H in enumerate(A)if H&d==H}for d in D];need(all(len(hs)==16 for hs in DH),'D4 plane population')
    m=[(H&native).bit_count()for H in A];x=[12//v+u.get(h,0)if v else 0 for h,v in enumerate(m)];hx=[v*z for v,z in zip(m,x)];sy=[max(8-z,0)for z in x]
    mixed=[];late=[];counts=[];failures=[];primal=0;max_nodes=0;max_arcs=0
    def certify(G,src,sink,target):
        nonlocal primal
        flow=maximum_flow(G,src,sink);v=int(flow.flow_value);co=G.tocoo();used=np.asarray(flow.flow[co.row,co.col]).ravel();need(np.all(used>=0)and np.all(used<=co.data),'directed physical capacities')
        div=np.asarray(flow.flow.sum(axis=1)).ravel();want=np.zeros(G.shape[0],dtype=np.int64);want[src]=v;want[sink]=-v;need(np.array_equal(div,want),'conservation at every early/late chart');primal+=1
        cut=None
        if v!=target:
            res=G-flow.flow;res.eliminate_zeros();reach=breadth_first_order(res,src,directed=True,return_predecessors=False);mark=np.zeros(G.shape[0],dtype=np.bool_);mark[reach]=1;cut=int(co.data[mark[co.row]&~mark[co.col]].sum());need(cut==v,'matching exact dual cut')
        return v,cut
    for j in range(111):
        hs={h for h,H in enumerate(A)if H>>j&1};ds={d for d,DD in enumerate(D)if DD>>j&1};ks=set.union(*(DH[dual[d]]for d in ds));receivers=sorted(bits(F[j]&native));degree=len(receivers);c=sum(45*sy[h]for h in hs)
        need(len(hs)==28 and sum(45*x[h]for h in hs)==B,'real source early slots');counts.append([j,degree,c,c//(degree-1)])
        ids={}
        for typ,ss in [('h',hs),('d',ds),('k',ks),('f',set(receivers))]:
            for v in sorted(ss):ids[typ,v]=len(ids)
        layer=len(ids);src=2*layer;sink=src+1;ir=[];ic=[];iv=[]
        def edge(s,t,cap):
            if cap:ir.append(s);ic.append(t);iv.append(cap)
        for n in range(layer):edge(n,n+layer,12000)
        early_source=[]
        for h in sorted(hs):
            early_source.append((src,ids['h',h]));edge(src,ids['h',h],45*x[h]);edge(src,ids['h',h]+layer,45*sy[h])
        for d in sorted(ds):
            dn=ids['d',d]
            for h in sorted(hs&DH[d]):
                hn=ids['h',h];edge(hn,dn,hx[h]);edge(hn+layer,dn+layer,24-hx[h])
            for k in sorted(DH[dual[d]]):
                kn=ids['k',k];edge(dn,kn,24-hx[k]);edge(dn+layer,kn+layer,hx[k])
        for k in sorted(ks):
            for i in sorted(set(bits(A[k]))&set(receivers)):
                kn=ids['k',k];fn=ids['f',i];edge(kn,fn,45*sy[k]);edge(kn+layer,fn+layer,45*x[k])
        for i in receivers:edge(ids['f',i]+layer,sink,a.k)
        G=coo_matrix((iv,(ir,ic)),shape=(sink+1,sink+1),dtype=np.int32).tocsr();max_nodes=max(max_nodes,sink+1);max_arcs=max(max_arcs,len(G.data))
        def location(s,t):
            lo,hi=G.indptr[s:s+2];ix=lo+int(np.searchsorted(G.indices[lo:hi],t));need(ix<hi and G.indices[ix]==t,'located exact physical arc');return ix
        terminal=[location(ids['f',i]+layer,sink)for i in receivers];source_ix=[location(s,t)for s,t in early_source]
        for i,ix in zip(receivers,terminal):
            G.data[ix]=B;target=B+(degree-1)*a.k;value,cut=certify(G,src,sink,target);mixed.append([j,i,value,target]);G.data[ix]=a.k
            if cut is not None:failures.append({'type':'mixed','donor':j,'receiver':i,'flow':value,'target':target,'cut':cut})
        old=G.data[source_ix].copy();G.data[source_ix]=0;chosen=None
        for i,ix in zip(receivers,terminal):
            G.data[ix]=0;target=(degree-1)*a.k;value,cut=certify(G,src,sink,target);G.data[ix]=a.k
            if value==target:chosen=[j,i,value,target];break
        need(chosen is not None,'one all-but-one late witness for every donor');late.append(chosen);G.data[source_ix]=old
        print('donor',j,'degree',degree,'late',c,'mixed',len(mixed),'exception',chosen[1],flush=True)
    raw=json.dumps({'mixed':mixed,'late_all_but_one':late},separators=(',',':')).encode()+b'\n';(a.out/'FLOWS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    mixed_defects=Counter(want-got for _,_,got,want in mixed);ceiling=min(t[3]for t in counts);worst=[t for t in counts if t[3]==ceiling];wbits=30;M=111*B*wbits;C=9*B*wbits
    result={'status':'PASS_SEVENTY_MIXED_COORDINATE_FLOW_WITNESSES'if not failures else'FAIL','k':a.k,'layout_uncompressed_sha256':LAYOUT_HASH,'factor_sha256':FACTOR_HASH,'mixed_cases':len(mixed),'mixed_defect_histogram':dict(sorted(mixed_defects.items())),'all_but_one_late_cases':len(late),'all_primal_capacities_and_divergences_checked':primal,'flow_table_uncompressed_sha256':sha256(raw).hexdigest(),'maximum_compressed_graph_nodes':max_nodes,'maximum_compressed_graph_arcs':max_arcs,'source_count_method_ceiling':ceiling,'source_count_tight_donors':worst,'source_counts':counts,'field_degree_sufficient':wbits,'binary_X_public_records':M,'canonical_binary_owners':C,'whole_ADD_bound':17*M*M+50*M+111*C,'whole_INIT_and_dirty_CLEAR_each_bound':5*M+C,'whole_peak_total_records_bound':7*M+C,'new_MOVE':0,'all6470_B_blocks_invertible_claimed_by_separate_polynomial_proof':not failures,'full_native_synchronization':False,'new_complete_kappa':False,'failures':failures}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in['source_counts','failures']},indent=2))
if __name__=='__main__':main()
