#!/usr/bin/env python3
"""Verify the noncommutative rectangle propagation on the authenticated native support."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import itertools
import json
from pathlib import Path

GEOMETRY='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
WITNESS='721cf0c2833b256663db5b44ea00acd9e0fbe92aa3c3a875ba5d08724a2305f4'

def require(ok,label):
    if not ok:raise ValueError(label)

def det(rows):
    A=[list(r) for r in rows]
    sign,div=1,1
    for c in range(len(A)-1):
        k=next((i for i in range(c,len(A)) if A[i][c]),None)
        if k is None:return 0
        if c!=k:A[k],A[c]=A[c],A[k];sign=-sign
        for i in range(c+1,len(A)):
            for j in range(c+1,len(A)):
                num=A[c][c]*A[i][j]-A[i][c]*A[c][j]
                require(num%div==0,'fraction-free division')
                A[i][j]=num//div
        div=A[c][c]
    return sign*A[-1][-1]

def audit(w,K):
    n=len(K)
    O=[[int(i!=j and K[i][j]) for j in range(n)] for i in range(n)]
    edges={(i,j) for i in range(n) for j in range(n) if O[i][j]}
    parent=list(range(2*n))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    weights={}
    for i,j in w['tree']:
        a,b=root(i),root(n+j)
        require((i,j) in edges and a!=b,'foreign spanning tree')
        parent[a]=b;weights[i,j]=0
    require(len(weights)==221 and len({root(i) for i in range(2*n)})==1,'all bipartite endpoints')
    for e,i,j,a,b,C,k in w['closure']:
        unknown=divmod(e,n)
        cells={(i,a),(i,b),(j,a),(j,b)}
        require(len(cells)==4 and cells<=edges and unknown in cells and unknown not in weights,'fresh rectangle')
        require(len(C)==len(set(C))==8 and not (set(C)&{i,j,a,b}),'exterior rectangle')
        require(all(not O[u][v] for u,v in itertools.combinations(C,2)),'independent native pivots')
        require(all(not (O[r][c] and O[c][s]) for r,s in cells for c in C),'zero Schur cross terms')
        others=cells-{unknown}
        require(others<=weights.keys() and k==1+sum(weights[u] for u in others),'triangle rank cost')
        weights[unknown]=k
    require(set(weights)==edges,'all native proper cells')
    degree=Counter(weights.values())
    require(degree=={0:221,1:4668,2:405,3:1176},'weighted closure')
    diagonal=Counter()
    for key,(price,R,C) in w['diagonal_pivots'].items():
        i=int(key)
        require(len(set(R))==len(set(C))==9 and not set(R)&set(C) and i not in R+C,'disjoint diagonal sets')
        core=[[K[r][c] for c in C] for r in R]
        border=[[K[r][c] for c in C+[i]] for r in R+[i]]
        require(det(core)%2==1 and det(border)%2==0,'native characteristic-two Schur value')
        total=sum(weights.get((r,c),0) for r in R+[i] for c in C+[i])
        require(price==total,'diagonal cell price')
        diagonal[price]+=1
    require(set(map(int,w['diagonal_pivots']))==set(range(n)),'every native diagonal')
    o=w['odd_minor'];R,C=o['rows'],o['cols']
    require(len(set(R))==len(set(C))==10 and not set(R)&set(C),'disjoint odd minor')
    od=det([[O[r][c] for c in C] for r in R])
    op=sum(weights.get((r,c),0) for r in R for c in C)
    require(abs(od)==2 and od==o['det'] and op==o['weight']==7,'odd characteristic witness')
    return {'foreign_entries':len(edges),'tree_entries':221,'rectangle_witnesses':len(w['closure']),
            'edge_rank_error_multipliers':dict(degree),'diagonal_pivot_error_sums':dict(diagonal),
            'largest_simultaneous_native_error_multiplier':max(degree)+max(diagonal)+1,
            'odd_disjoint_minor_det':od,'odd_disjoint_minor_error_cost':op,
            'odd_characteristic_relative_excess_lower_bound':'1/8'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--certificate',type=Path,default=Path(__file__).parent/'output/WITNESS.json.gz')
    a=p.parse_args()
    path=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(path.read_bytes());data=gzip.decompress(a.certificate.read_bytes())
    require(sha256(raw).hexdigest()==GEOMETRY and sha256(data).hexdigest()==WITNESS,'source hashes')
    r=json.loads(raw)['root_table'][:111]
    K=[[int(i==j or sum(a*b for a,b in zip(x,y))==0) for j,y in enumerate(r)] for i,x in enumerate(r)]
    w=json.loads(data);out=audit(w,K)
    faults={}
    def control(name,patch):
        v=json.loads(data);patch(v)
        try:audit(v,K)
        except ValueError as e:faults[name]=str(e)
        else:raise ValueError('undetected '+name)
    control('one missing seed block',lambda v:v['tree'].pop())
    control('wrong first rectangle clique',lambda v:v['closure'][0].__setitem__(5,[v['closure'][0][1]]*8))
    control('one undebited unit of excess',lambda v:v['closure'][0].__setitem__(6,0))
    control('overlapping odd witness rows',lambda v:v['odd_minor']['cols'].__setitem__(0,v['odd_minor']['rows'][0]))
    out.update(geometry_sha256=GEOMETRY,witness_sha256=WITNESS,negative_controls=faults)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['edge_rank_error_multipliers'],out['diagonal_pivot_error_sums'])
if __name__=='__main__':main()
