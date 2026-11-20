#!/usr/bin/env python3
"""Exact native tangent space and determinant pivots on all original roles."""
import argparse
from collections import Counter,deque
import gzip
from hashlib import sha256
import json
from pathlib import Path

PIN='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
CLIQUE=(1,29,28,37,36,65,63,73)

def check(ok,why):
    if not ok:raise ValueError(why)

def vertices(mask):
    while mask:
        b=mask&-mask
        yield b.bit_length()-1
        mask-=b

class Echelon:
    def __init__(self):self.rows={}
    def push(self,value):
        while value:
            c=value.bit_length()-1
            old=self.rows.get(c)
            if old is None:
                self.rows[c]=value
                return True
            value^=old
        return False

def clique_census(K,n):
    graph=[((1<<n)-1)^r for r in K]
    largest=[]
    counts=Counter()
    def visit(body,P,X):
        if not (P or X):
            counts[len(body)]+=1
            if len(body)>=8:largest.append(body)
            return
        pivot=max(vertices(P|X),key=lambda i:(P&graph[i]).bit_count())
        for i in vertices(P&~graph[pivot]):
            visit((*body,i),P&graph[i],X&graph[i])
            P^=1<<i
            X|=1<<i
    visit((),(1<<n)-1,0)
    foreign=[r^(1<<i) for i,r in enumerate(K)]
    coverage=Counter()
    anchors=Counter()
    for C in largest:
        chosen=sum(1<<i for i in C)
        masks=[foreign[i]&chosen for i in range(n)]
        count=0
        for i in range(n):
            if chosen>>i&1:continue
            for j in vertices(foreign[i]&~chosen):
                if not masks[i]&masks[j]:
                    coverage[i,j]+=1
                    count+=1
        anchors[count]+=1
    check(len(coverage)==sum(r.bit_count() for r in foreign),'all foreign anchor directions')
    return {'maximal_nonforeign_cliques_by_size':dict(counts),'total_ninth_pivots':sum(coverage.values()),
            'eight_cliques_per_foreign_anchor':dict(Counter(coverage.values())),
            'ordered_foreign_anchors_per_eight_clique':dict(anchors)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--skip-clique-enumeration',action='store_true')
    a=p.parse_args()
    f=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(f.read_bytes())
    check(sha256(raw).hexdigest()==PIN,'geometry payload')
    roots=json.loads(raw)['root_table'][:111];n=len(roots)
    K=[sum(1<<j for j,y in enumerate(roots) if i==j or sum(a*b for a,b in zip(x,y))==0)
       for i,x in enumerate(roots)]
    B=[x^(1<<i) for i,x in enumerate(K)]
    seen={0};queue=deque(seen)
    while queue:
        i=queue.popleft()
        for j in vertices(B[i]):
            if j not in seen:seen.add(j);queue.append(j)
    check(len(seen)==n,'connected foreign graph')
    T=[]
    for row in K:
        m=sum(((row>>c)&1)<<i for i,c in enumerate(CLIQUE))
        T.append(m|((1^(m.bit_count()&1))<<8))
    check(all((K[i]>>j)&1==(T[i]&T[j]).bit_count()%2 for i in range(n) for j in range(n)),'Gram factorization')
    q=Echelon()
    for t in T:q.push(t)
    check(len(q.rows)==9,'rank-nine factor')
    cond=Echelon();drop=Echelon();all_cells=Echelon();selected=[];fixed=0
    for i in range(n):
        for j in range(n):
            r=(T[j]<<(9*i))|(T[i]<<(9*(n+j)))
            all_cells.push(r)
            if i==j or not ((K[i]>>j)&1):
                if cond.push(r):selected.append(n*i+j)
                fixed+=1
                if (i,j)!=(0,0):drop.push(r)
    tangent=len(all_cells.rows)-len(cond.rows)
    cutspace=Echelon()
    for i in range(n):
        mask=sum(1<<(i*n+j) for j in vertices(B[i]))
        mask|=sum(1<<(j*n+i) for j in vertices(B[i]))
        cutspace.push(mask)
    check((fixed,len(cond.rows),len(all_cells.rows),tangent,len(cutspace.rows))==(5851,1807,1917,110,110),'tangent and cut space')
    check(len(cond.rows)-len(drop.rows)==1,'released diagonal grows tangent')
    # A single proper directed edge creates one unit of rank excess.
    j=next(vertices(B[0]))
    def rank(rows):
        e=Echelon()
        for r in rows:e.push(r)
        return len(e.rows)
    both=K+[((K[i]<<n)^(1<<j) if i==0 else K[i]<<n) for i in range(n)]
    check(rank(both)==19,'directed single-edge square-zero fitting')
    spec={'source_geometry_sha256':PIN,'n':n,'native_foreign':sum(z.bit_count() for z in B),
          'fixed_cells':fixed,'factor_variables':18*n,'coefficient_rank_all_cells':len(all_cells.rows),
          'coefficient_rank_fixed_cells':len(cond.rows),'factor_kernel':18*n-len(cond.rows),
          'true_tangent_dimension':tangent,'gauge_cut_space':len(cutspace.rows),
          'one_released_diagonal_rank':len(drop.rows),'one_proper_edge':(0,j),
          'two_bank_rank_with_one_nilpotent_edge':19,'independent_fixed_equation_ids':selected,
          'binary_rank_nine_rows':T,'clique':CLIQUE}
    if not a.skip_clique_enumeration:spec.update(clique_census(K,n))
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(spec,indent=2,sort_keys=True)+'\n')
    print('factor tangent',tangent,'all native anchors',spec.get('total_ninth_pivots'))

if __name__=='__main__':main()
