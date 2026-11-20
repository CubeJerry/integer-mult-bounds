#!/usr/bin/env python3
"""Independent exact noncommutative cancellation and physical prices for the joined native stars."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import numpy as np


def red(seq):
    out=[]
    for name,i,j,sign in seq:
        tok=(name,i,j,sign)
        if out and out[-1]==(name,i,j,-sign):out.pop()
        else:out.append(tok)
    return out


def inv(x):return [(n,i,j,-s)for n,i,j,s in reversed(x)]

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def one(a,root,temp):
    results=a.repo/'research/moonshot-005-program/results';bil=a.bilateral_author or results/'bit-global-source-facet-row-column/author';star=a.star_author or results/'bit-global-two-star-target/author';sys.path.insert(0,str(bil.resolve()));previous=load(bil/'check.py','transport');native=load(star/'native.py','physical_stars');first,_,f,_,s,late=previous.setup(a,temp);raw=json.loads((bil/'output/PARAMETERS.json').read_text());P=raw['output_dimensions'];U=s['tiers'];J=s['adj'];T=s['terms'];C=s['copy'];out=set(J[10]);g0=set(J[80]);anchors={i for i in out if P[i]==7 and set(C[64*T[i,10][0]:64*T[i,10][0]+64])<={0,1,5}};assert anchors=={3,27,38,81,84,88}
    def B(i,j):return [('B',i,j,1)]
    def t(i,j):return [('T',i,j,1)]if(i,j)in T else []
    G={j:inv(B(80,j))+t(80,j) for j in g0};H={i:t(i,10)+inv(B(i,10)) for i in out};edges={(80,j)for j in g0}|{(i,10)for i in out};leaves={}
    for j in sorted(set(range(111))-g0-{10}):
        i=min(anchors.intersection(J[j]));G[j]=inv(B(i,j))+inv(H[i]);edges.add((i,j));leaves[j]=i
    for i in sorted(set(range(111))-out-{80}):
        j=min(j for j in g0.intersection(J[i])if U[j]==7);H[i]=inv(G[j])+inv(B(i,j));edges.add((i,j))
    oldH=H.copy();H[80]=[];a0,j0=3,0;edges.add((a0,j0));Y=H[a0]+B(a0,j0)+G[j0];F=red(inv(t(a0,10))+Y+t(a0,10));G[10]=F
    def K(i):return red(t(i,10)+F+inv(t(i,10)))
    for i in out:H[i]=red(inv(K(i))+H[i]);
    for j,i in leaves.items():G[j]=red(G[j]+K(i))
    for i,j in edges:assert red(H[i]+B(i,j)+G[j])==t(i,j)
    assert len(edges)==221 and len(G)==len(H)==111
    vertices={(False,0)}
    while True:
        more=vertices|{(True,j) for i,j in edges if (False,i)in vertices}|{(False,i)for i,j in edges if(True,j)in vertices}
        if len(more)==len(vertices):break
        vertices=more
    assert len(vertices)==222
    primitive=json.loads((star/'output/RESULT.json').read_text())['primitive_edge_words'];cost={(n,*map(int,p.split(','))):v[key]for p,v in primitive.items() for n,key in [('B','native_forward_or_inverse_ADD'),('T','original_target_forward_or_inverse_ADD')]};used={(n,i,j)for path in list(H.values())+list(G.values())for n,i,j,_ in path};missing=sorted(used-set(cost));ss={};minor=np.eye(5760,dtype=np.uint8);pins=json.loads((star/'output/SOURCE-PINS.json').read_text());changed={}
    for n,i,j in missing:
        if n=='T':cost[n,i,j]=native.target_price(f,T[i,j]);continue
        if j not in ss:
            ss[j]=native.cached(a.source_cache/f'{j:03}.npz')if a.source_cache else previous.donor.verify_donor(j,f,first.coefficients,s,raw,late,minor)[1]
            assert native.source_pin(*ss[j])==pins[str(j)]
        L=np.load(late/f'L{j}.npy',mmap_mode='r');assert hashlib.sha256(L).hexdigest()==raw['donors'][str(j)]['late_transfer_sha256'];z=native.whole(f,s,i,j,L[J[j].index(i)],ss[j]);rec=native.price(f,z);cost[n,i,j]=rec['native_forward_or_inverse_ADD'];changed[f'{i},{j}']=rec
    fc=sum(cost[n,i,j] for path in H.values()for n,i,j,_ in red(path));sc=sum(cost[n,i,j] for path in G.values()for n,i,j,_ in red(path));assert (sc,fc)==(20550115164,26963815767)
    hist=Counter()
    for i,js in enumerate(J):
        protected={0,1,5}
        if i in out:protected.update(map(int,C[64*T[i,10][0]:64*(1+T[i,10][0])]))
        hist[(8-len(protected))*P[i]]+=sum((i,j)not in edges for j in js)
    return {'status':'PASS_INDEPENDENT_PHYSICAL_221_TREE_AND_PRICES','original_matrix_edges':len(edges),'visited_donor_and_receiver_vertices':len(vertices),'whole_nonflat_original_blocks':len(T),'new_source_forward_ADD':sc,'new_facet_forward_ADD':fc,'extra_forward_plus_reserved_inverse_ADD':2*(fc+sc),'proper_field_matrix_scalar_entries':len(edges)*3840**2,'native_input_survival':35,'original_output_rows_other_native_edges':hist,'earlier_primitives_reused':len(used)-len(missing),'independently_regenerated_new_edge_primitives':changed}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for n in ('bilateral-author','star-author','target-author','flat-author','cache-dir','late-cache','source-cache'):p.add_argument('--'+n,type=Path)
    a=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='independent-connected-stars-')as td:r=one(a,Path(__file__).resolve().parent,Path(td))
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('PASS',r['original_matrix_edges'],r['extra_forward_plus_reserved_inverse_ADD'])

if __name__=='__main__':main()
