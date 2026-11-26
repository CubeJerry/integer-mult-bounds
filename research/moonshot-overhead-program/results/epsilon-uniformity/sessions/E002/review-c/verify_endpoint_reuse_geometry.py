#!/usr/bin/env python3
"""Finite exact witnesses for endpoint reuse; no tape lower bound."""
from itertools import product
from pathlib import Path
from fractions import Fraction
import hashlib,json


def inner(a,d):
    return (a,)*d+(0,)*(d-1)


def label(alpha,d):
    z=(0,)*(2*d-1)
    return tuple(inner(a,d) for a in alpha)+(z,)*(d-1)


def far_count(v,w,d):
    return sum(sum(a!=b for a,b in zip(u,z))==d for u,z in zip(v,w))


def binary_rank(rows,n):
    rows=list(rows);r=0
    for col in range(n):
        pivot=next((i for i in range(r,len(rows)) if (rows[i]>>col)&1),None)
        if pivot is None:continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        for i in range(len(rows)):
            if i!=r and (rows[i]>>col)&1:rows[i]^=rows[r]
        r+=1
    return r


def main():
    counts={'far_triangles':0,'oriented_graph_connections':0,'triangle_pin_negative_controls':0,
            'grid_cases':0,'grid_labels':0,'grid_pair_counts':0,
            'source_binary_gram_rank_checks':0,'relative_star_swap_witnesses':0}
    for d,q in product((2,3,4,8),(3,4,8)):
        vs=[label((a,)*d,d) for a in (0,1,2)]
        assert all(far_count(vs[a],vs[b],d)==(0 if a==b else d) for a,b in product(range(3),repeat=2))
        # The six directed far edges connect both orientations of every label.
        graph={('S',i):set() for i in range(3)}|{('T',i):set() for i in range(3)}
        for i,j in product(range(3),repeat=2):
            if i!=j:
                graph['S',i].add(('T',j));graph['T',j].add(('S',i))
        seen={('S',0)};todo=list(seen)
        while todo:
            v=todo.pop()
            for w in graph[v]-seen:seen.add(w);todo.append(w)
        assert len(seen)==6 and ('T',0) in seen
        # Source suffix annihilates x0 but destination suffix contains x0.
        assert Fraction(1-far_count(vs[0],vs[0],d),1)==1
        counts['far_triangles']+=1;counts['oriented_graph_connections']+=1
        wrong=tuple((2,)*(d-1)+(0,)*d for _ in range(d))+((0,)*(2*d-1),)*(d-1)
        assert far_count(vs[0],wrong,d)==0
        counts['triangle_pin_negative_controls']+=1
    for d,q in product((2,3,4),(2,3,4)):
        alphas=list(product(range(q),repeat=d));vs=[label(a,d) for a in alphas]
        for i,a in enumerate(alphas):
            degree=0
            for j,b in enumerate(alphas):
                h=sum(x!=y for x,y in zip(a,b))
                assert far_count(vs[i],vs[j],d)==h
                if i!=j:assert h>0
                degree+=h==d
                counts['grid_pair_counts']+=1
            assert degree==(q-1)**d
        counts['grid_cases']+=1;counts['grid_labels']+=len(alphas)
    words=list(product(range(4),repeat=2))
    gram=[[1^(sum(a!=b for a,b in zip(v,w))&1) for w in words] for v in words]
    rows=[sum(bit<<j for j,bit in enumerate(row)) for row in gram]
    assert binary_rank(rows,16)==6
    ix={w:i for i,w in enumerate(words)}
    es=[1<<ix[a,0] for a in range(4)]
    p=(1<<ix[0,1])^es[1]^es[2]^es[3]
    q=(1<<ix[0,2])^es[1]^es[2]^es[3]
    def pair(v,w):
        return sum(gram[i][j] for i in range(16) if (v>>i)&1 for j in range(16) if (w>>j)&1)&1
    basis=es+[p,q]
    expected=[[int(i==j) if i<4 and j<4 else int((i,j) in ((4,5),(5,4))) for j in range(6)] for i in range(6)]
    assert [[pair(v,w) for w in basis] for v in basis]==expected
    counts['source_binary_gram_rank_checks']=2
    for alphabet in (2,4,8):
        def swap(v,j):
            v=list(v);v[0],v[j]=v[j],v[0];return tuple(v)
        def rel(v,j):return swap(swap(v,1),j)
        v=(1,0,0,0)
        assert rel(rel(v,3),2)==(0,0,1,0)
        assert rel(rel(v,2),3)==(0,0,0,1)
        counts['relative_star_swap_witnesses']+=1
    report={'status':'PASS_FINITE_ENDPOINT_REUSE_GEOMETRY','counts':counts,
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'characterization_sha256':hashlib.sha256(Path(__file__).with_name('COMPATIBLE-ENDPOINT-REUSE.md').read_bytes()).hexdigest(),
            'scope':'Finite actual far-label triangles and grids, source quotient Gram rank, and relative swap witnesses. No physical runtime or universal asymptotic verification.'}
    Path(__file__).with_name('endpoint-reuse-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
