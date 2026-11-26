#!/usr/bin/env python3
"""Exact canonical leaf-line cosets in binary Gram quotients."""
from itertools import product
from pathlib import Path
from functools import reduce
from operator import xor
import json
from verify_nested_fourier_source_reuse import basis
from verify_shared_fourier_destination import coordinates

def check(q,L,w):
    t=q.bit_length()-1
    labels=tuple(product(range(q),repeat=L));ix={v:i for i,v in enumerate(labels)}
    rows=[sum((1-(sum(a!=b for a,b in zip(v,z))&1))<<j for j,z in enumerate(labels)) for v in labels]
    D=len(basis(rows))
    def z(i,a):
        v=list(w);v[i]=a
        return rows[ix[tuple(v)]]
    es=[reduce(xor,(z(i,a) for a in range(q) if a!=w[i]),0) for i in range(L)]
    assert len(set(es))==1;e=es[0]
    blocks=[[None]*t for _ in range(L)];U=[[[] for _ in range(t)] for _ in range(L)];B=[e]
    for i in range(L):
        for s in range(t):
            start=((w[i]>>s)^1)<<s;letters=tuple(range(start,start+(1<<s)));blocks[i][s]=letters
            for a in letters[1:]:U[i][s].append(len(B));B.append(z(i,a)^z(i,letters[0]))
    rslots={}
    for i in range(L):
        for s in range(1,t):rslots[i,s]=len(B);B.append(z(i,blocks[i][s][0])^e)
    assert len(B)==D-1 and len(basis(B))==D-1
    encode=coordinates(B)
    ui=[reduce(xor,(z(i,a) for s in range(1,t) for a in blocks[i][s]),0) for i in range(L)]
    assert all(z(i,blocks[i][0][0])==e^ui[i] for i in range(L))
    if q>=4:assert len(basis(ui))==L
    else:assert not any(ui)
    seen={};rectangles=points=dupes=labelchecks=missingzero=0
    for choices in product(range(-1,t),repeat=L):
        if sum(s>=0 for s in choices)%2!=1:continue
        selected=[a for i,s in enumerate(choices) if s>=0 for a in U[i][s]]
        mask=sum(1<<a for a in selected)
        base=reduce(xor,(z(i,blocks[i][s][0]) for i,s in enumerate(choices) if s>=0),0)
        code=encode(base);assert code&1 and not code&mask
        formula=1;omitted=1
        for i,s in enumerate(choices):
            if s>0:formula^=1<<rslots[i,s];omitted^=1<<rslots[i,s]
            if s==0:formula^=encode(ui[i])
        assert formula==code;missingzero+=omitted!=code
        coset={code}
        for a in selected:coset|={v^(1<<a) for v in tuple(coset)}
        for v in coset:
            if v in seen:dupes+=1;assert q==2
            seen[v]=choices;points+=1
        side=[(w[i],) if s<0 else blocks[i][s] for i,s in enumerate(choices)]
        for v in product(*side):assert encode(rows[ix[v]]) in coset;labelchecks+=1
        rectangles+=1
    if q==2:assert set(seen)=={1} and dupes==rectangles-1
    else:assert dupes==0
    return dict(q=q,L=L,destination=w,auxiliary_dimension=D-1,
                rectangle_line_cosets=rectangles,enumerated_coset_points=points,duplicated_points=dupes,
                actual_source_labels_in_cosets=labelchecks,omitted_level_zero_offset_negative_cases=missingzero,
                canonical_selected_internal_phase_cases=rectangles,binary_free_axis_bill=4 if q==2 else None)

def main():
    cases=[check(q,L,w) for q,L,w in [(2,2,(0,0)),(2,4,(1,0,1,1)),(2,6,(0,)*6),
           (4,2,(1,2)),(4,4,(0,)*4),(4,4,(1,2,3,1)),(8,2,(3,6)),(16,2,(7,12))]]
    assert sum(c['omitted_level_zero_offset_negative_cases'] for c in cases)>0
    receipt=dict(status='pass',scope='exact local geometry and canonical phase simplification; no global runtime claim',
                 cases=cases,total_cosets=sum(c['rectangle_line_cosets'] for c in cases),
                 total_points=sum(c['enumerated_coset_points'] for c in cases),
                 total_label_checks=sum(c['actual_source_labels_in_cosets'] for c in cases))
    Path(__file__).with_name('fourier-leaf-line-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
