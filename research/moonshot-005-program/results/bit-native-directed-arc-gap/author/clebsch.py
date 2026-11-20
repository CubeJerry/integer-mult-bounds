"""Exact 16-role Shannon dual and independently authenticated native chart coverage."""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
from itertools import combinations,permutations
import json
from pathlib import Path

G=(1,2,4,8,15);full=(1<<16)-1

def need(x,label):
    if not x:raise ValueError(label)

def apply(S,p):return sum(1<<p[j] for j in range(16) if S>>j&1)

def proof(q, missing=None):
    full=(1<<16)-1 if missing is None else ((1<<16)-1)^(1<<missing)
    nbs=[sum(1<<(i^s) for s in G) for i in range(16)];S0=(full&~(nbs[0]|1))|2;loss=Fraction(q['optimum']);need(q['S']==S0 and q['target']==0 and loss>0,'true deleted 0←1 directed marginal')
    pm=[]
    for s in permutations(G[1:]):
        t=(1,)+s;p=[]
        for x in range(16):
            v=0
            for j in range(4):
                if x>>j&1:v^=t[j]
            p.append(v)
        if missing is not None and p[missing]!=missing:continue
        need(len(set(p))==16 and p[0]==0 and p[1]==1 and apply(S0,p)==S0,'directed local automorphism');pm.append(p)
    order=len(pm);total=Counter();rhs=Fraction(0);pt=Counter()
    for weight,kind,*args in q['terms']:
        w=Fraction(weight);pt[kind]+=1
        if kind in ('diminish','mono','monofull','submod'):need(w>0,'positive Shannon multipliers')
        if kind=='unit':need(w==loss,'certified marginal coefficient');continue
        if kind=='empty':total[0]+=order*w;continue
        if kind=='monofull':
            need(0<=args[0] and not args[0]&~full,'real local subset');terms=[(full,1),(args[0],-1)]
        elif kind in ('decode','mono'):
            S,i=args;need(not S>>i&1 and 0<=S and not S&~full and 0<=i<16 and i!=missing,'one added owner');terms=[(S|1<<i,1),(S,-1)]
            if kind=='decode':need(not S&nbs[i],'valid native side-information decoder');rhs+=order*w
        elif kind=='diminish':
            U,S,i=args;need(not U&~S and not S>>i&1 and 0<=U and 0<=S and not S&~full and 0<=i<16 and i!=missing,'nested diminishing returns');terms=[(U|1<<i,1),(U,-1),(S|1<<i,-1),(S,1)]
        else:raise ValueError(kind)
        for p in pm:
            for t,c in terms:total[apply(t,p)]+=c*w
    v={k:z for k,z in total.items() if z};need(v=={full:order,S0:order*loss,S0|1:-order*loss} and rhs==6*order,'all 65536 raw subset coefficients exact')
    return {'rational_marginal_cost':str(1/loss),'native_arc_deletion_excess_over_b':str(loss),'positive_raw_predicates':dict(pt),'raw_subset_coordinates':1<<full.bit_count()}

def native(layout,c):
    raw=gzip.decompress(layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','actual 111-role source');v=json.loads(raw)['root_table'][:111]
    adj=[sum(1<<j for j,b in enumerate(v) if sum(s*t for s,t in zip(a,b))==0) for a in v];seen=set()
    for C,P in c['charts']:
        need(len(C)==3 and len(P)==16 and len(set(C+P))==19,'separate native 3+16 chart');allm=sum(1<<x for x in C+P)
        need(all(not adj[a]&allm for a in C),'uncontaminated three anchor banks')
        for a in range(16):
            for b in range(a):
                proper=((a^b) in G);need(bool(adj[P[a]]>>P[b]&1)==proper,'actual labelled Clebsch link')
                if proper:seen.add(tuple(sorted([P[a],P[b]])))
    allp={(i,j) for i in range(111) for j in range(i+1,111) if adj[i]>>j&1};missing=sorted(allp-seen)
    need(len(seen)==3231 and len(missing)==4,'all covered certified edges');return {'charts':len(c['charts']),'covered_undirected_edges':len(seen),'covered_directed_edges':2*len(seen),'missing_undirected_edges':missing}

def rectangles(layout, nine, covered):
    v=json.loads(gzip.decompress(layout.read_bytes()))['root_table'][:111]
    O=[[sum(x*y for x,y in zip(r,t))==0 for t in v] for r in v]
    missing={tuple(e) for e in covered['missing_undirected_edges']};pairs=missing|{(y,x) for x,y in missing};seen=set()
    for i,j,r,s,C in nine:
        need(len(set([i,j,r,s]+C))==12 and len(C)==8,'true exterior 8+4 rectangle roles')
        need(all(not O[x][y] for x in C for y in C),'eight true own pivots')
        for x,y in [(i,j),(r,j),(i,s),(r,s)]:
            need(O[x][y] and all(not (O[x][c] and O[c][y]) for c in C),'true path-free proper rectangle')
        need((i,j) in pairs and (r,j) not in pairs and (i,s) not in pairs,'both adjacent corners independently covered');seen.add((i,j))
    need(seen==pairs,'all remaining directed edges');return {'exceptional_rectangles':len(seen),'all_native_corank_per_excess':'19/5','regular_corank_per_excess':'7/5'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--charts',type=Path,required=True);p.add_argument('--dual',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--rectangles',type=Path);p.add_argument('--puncture',type=Path);p.add_argument('--puncture-dual',type=Path);a=p.parse_args()
    d=json.loads(a.dual.read_bytes());c=json.loads(gzip.decompress(a.charts.read_bytes()));data={'local_dual':proof(d),'native_coverage':native(a.layout,c),'certified_dual_sha256':sha256(a.dual.read_bytes()).hexdigest(),'native_charts_uncompressed_sha256':sha256(gzip.decompress(a.charts.read_bytes())).hexdigest()}
    if a.rectangles:data['remaining_arcs']=rectangles(a.layout,json.loads(a.rectangles.read_bytes()),data['native_coverage'])
    if a.puncture:
        q=json.loads(a.puncture_dual.read_bytes());data['punctured_dual']=proof(q,6)
        vs=json.loads(gzip.decompress(a.layout.read_bytes()))['root_table'][:111];missing={tuple(e) for e in data['native_coverage']['missing_undirected_edges']};target=missing|{(y,x) for x,y in missing};seen=set()
        for i,j,C,P in json.loads(a.puncture.read_bytes()):
            need(P[0]==i and P[1]==j and P[6] is None and len(C)==3 and len(set(C+[a for a in P if a is not None]))==18,'genuine directed punctured chart')
            foreign=lambda u,v:sum(a*b for a,b in zip(vs[u],vs[v]))==0
            need(all(not foreign(x,y) for x in C for y in C+[z for z in P if z is not None]),'pure punctured anchors')
            for x in range(16):
                for y in range(x):
                    if 6 not in (x,y):need(foreign(P[x],P[y])==((x^y) in G),'authentic 15-role link')
            seen.add((i,j))
        need(seen==target,'all eight directed punctures');data['punctured_dual_sha256']=sha256(a.puncture_dual.read_bytes()).hexdigest()
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CLEBSCH-RESULT.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(data)

if __name__=='__main__':main()
