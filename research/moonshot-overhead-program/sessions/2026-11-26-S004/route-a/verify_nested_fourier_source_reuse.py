#!/usr/bin/env python3
"""Exact controls for a shared source-transform tree; no tape simulation."""
from itertools import product
from math import comb
from pathlib import Path
from random import Random
import json


def basis(vectors):
    pivots={}
    for x in vectors:
        while x:
            p=x.bit_length()-1
            if p in pivots: x^=pivots[p]
            else:
                pivots[p]=x
                break
    return tuple(pivots[p] for p in sorted(pivots,reverse=True))


def dot(x,y): return (x&y).bit_count()&1


def walsh(values,axes=None,inverse=False):
    out=list(values)
    if axes is None: axes=range(len(out).bit_length()-1)
    for axis in axes:
        bit=1<<axis
        for i in range(len(out)):
            if i&bit: continue
            x,y=out[i],out[i|bit]
            if inverse:
                assert (x+y)%2==0 and (x-y)%2==0
                out[i],out[i|bit]=(x+y)//2,(x-y)//2
            else: out[i],out[i|bit]=x+y,x-y
    return out


def states(L,t):
    return tuple(sorted((s for s in product(range(t),repeat=L) if 0 in s),key=lambda s:(sum(s),s)))


def parent(s):
    ell=min(x for x in s if x)
    i=s.index(ell)
    p=list(s);p[i]-=1
    return tuple(p),i,ell


def invoice(L,t):
    q=1<<t
    lam=sum(comb(L,k)*t**k for k in range(1,L+1,2))
    deriv=sum(k*comb(L,k)*t**(k-1) for k in range(1,L+1,2))
    A=(q-1-t)*deriv
    S=sum((1<<(ell-1))*((t-ell+1)**L-2*(t-ell)**L+(t-ell-1)**L) for ell in range(1,t))
    D=2+L*(q-2)
    previous=2*(D-1)+2*lam+4*A
    new=2*(D-1)+2*S+2*lam+2*A
    assert 0<=S<=A and previous<=2*new and new<=previous
    return dict(L=L,t=t,q=q,D=D,incidence=lam,old_source_axes=A,shared_source_axes=S,
                original_free_axes=2*D*lam,preconditioned_free_axes=previous,nested_free_axes=new)


def combinatorics():
    cases=state_count=incidences=0
    for L in (2,4,6):
        for t in range(1,5):
            Q=states(L,t);actual=set();A=0;count=0
            for choices in product(range(-1,t),repeat=L):
                if sum(c>=0 for c in choices)%2!=1: continue
                s=tuple(max(c,0) for c in choices)
                actual.add(s);A+=sum((1<<c)-1 for c in s);count+=1
            row=invoice(L,t)
            assert actual==set(Q)
            assert len(Q)==t**L-(t-1)**L
            assert A==row['old_source_axes'] and count==row['incidence']
            S=0
            for s in Q:
                if not any(s): continue
                p,i,ell=parent(s)
                assert p in actual and sum(p)<sum(s)
                S+=1<<(ell-1)
            assert S==row['shared_source_axes']
            cases+=1;state_count+=len(Q);incidences+=count
    profiles=[invoice(L,t) for L in range(2,22,2) for t in range(1,31)]
    examples=[invoice(4,t) for t in (2,3,4,8,16)]
    assert examples[0]['nested_free_axes']==230
    assert examples[1]['nested_free_axes']==1342
    return dict(exhaustive_incidence_families=cases,distinct_states=state_count,
                original_incidences=incidences,integer_invoice_profiles=len(profiles),examples=examples)


def geometry(q,L,v):
    t=q.bit_length()-1
    labels=tuple(product(range(q),repeat=L));index={w:i for i,w in enumerate(labels)}
    rows=[sum((1-(sum(a!=b for a,b in zip(w,z))&1))<<j for j,z in enumerate(labels)) for w in labels]
    D=len(basis(rows));assert D==2+L*(q-2)
    vi=index[v];dv=rows[vi];B=[];coeff=[];slots=[[[] for _ in range(t)] for _ in range(L)]
    wrong_projection=0
    for i in range(L):
        previous={v[i]}
        for level in range(1,t):
            start=(v[i]>>level)<<level
            current=set(range(start,start+(1<<level)))
            slots[i][level]=list(slots[i][level-1])
            for a in sorted(current-previous):
                w=list(v);w[i]=a;u=index[tuple(w)]
                assert not ((rows[u]>>vi)&1)
                assert ((rows[u]^dv)>>vi)&1
                wrong_projection+=1
                slots[i][level].append(len(B));B.append(rows[u]);coeff.append(1<<u)
            previous=current
    assert len(basis(B))==len(B)
    for u,row in enumerate(rows):
        projection=row^(((row>>vi)&1)*dv)
        if len(basis(B+[projection]))>len(B):
            B.append(projection);coeff.append((1<<u)^(((row>>vi)&1)<<vi))
        if len(B)==D-1:break
    assert len(B)==D-1
    G=[sum(dot(B[i],coeff[j])<<j for j in range(len(B))) for i in range(len(B))]
    assert len(basis(G))==len(B)
    rank_checks=degenerate=0
    for s in states(L,t):
        axes=[a for i,c in enumerate(s) for a in slots[i][c]]
        selected=[B[a] for a in axes]
        assert len(basis(selected))==sum((1<<c)-1 for c in s)
        side=[]
        for i,c in enumerate(s):
            start=(v[i]>>c)<<c
            side.append(range(start,start+(1<<c)))
        side_rows=[rows[index[w]] for w in product(*side)]
        assert len(basis(side_rows))==1+len(selected)
        assert len(basis([dv]+selected+side_rows))==1+len(selected)
        if axes:
            small=[sum(((G[a]>>b)&1)<<j for j,b in enumerate(axes)) for a in axes]
            if len(basis(small))<len(axes):degenerate+=1
        rank_checks+=1
    return G,slots,dict(exact_projected_side_rank_checks=rank_checks,
                        degenerate_requested_flag_spaces=degenerate,
                        wrong_affine_projection_controls=wrong_projection)


def execution(q,L,v):
    G,slots,counts=geometry(q,L,v);d=len(G);n=1<<d;t=q.bit_length()-1
    rng=Random(260112+q+L+sum(v));original=[rng.randrange(-4,5) for _ in range(n)]
    ordinary_dual=[sum(dot(row,z)<<i for i,row in enumerate(G)) for z in range(n)]
    assert len(set(ordinary_dual))==n
    reindexed=[0]*n
    for z,c in enumerate(ordinary_dual):reindexed[c]=original[z]
    full=walsh(reindexed)
    Q=states(L,t);root=(0,)*L;cache={root:full};axis_cost=0
    for s in Q:
        if s==root:continue
        p,i,ell=parent(s)
        added=slots[i][ell][len(slots[i][ell-1]):]
        assert len(added)==1<<(ell-1)
        cache[s]=walsh(cache[p],added,True);axis_cost+=len(added)
    assert axis_cost==invoice(L,t)['shared_source_axes']
    entries=wrong_dual=0
    outputs=range(n) if d<=9 else tuple(sorted(rng.sample(range(n),32)))
    incorrect_full=walsh(original)
    for s in Q:
        axes=[a for i,c in enumerate(s) for a in slots[i][c]]
        mask=sum(1<<a for a in axes)
        incorrect=walsh(incorrect_full,axes,True)
        for out in outputs:
            expected=sum((-value if dot(c&~mask,out) else value)
                         for value,c in zip(original,ordinary_dual) if c&mask==out&mask)
            assert cache[s][out]==expected
            entries+=1
            wrong_dual+=incorrect[out]!=expected
    wrong_copy=0
    if t>=2 and L>=2:
        first=walsh(full,slots[0][1],True)
        incorrectly_reused=walsh(first,slots[1][1],True)
        second=[0]*L;second[1]=1
        correct=cache[tuple(second)]
        wrong_copy=sum(x!=y for x,y in zip(incorrectly_reused,correct))
        assert wrong_copy
    counts.update(q=q,L=L,source_label=v,auxiliary_dimension=d,
                  exact_transform_output_entries=entries,wrong_dual_basis_controls=wrong_dual,
                  mutated_parent_copy_controls=wrong_copy,tree_axis_count=axis_cost)
    return counts


def main():
    cases=[execution(q,L,v) for q,L,v in
           [(2,4,(0,0,0,0)),(4,2,(0,0)),(4,4,(0,0,0,0)),
            (4,4,(1,2,3,1)),(8,2,(3,6))]]
    assert sum(c['wrong_dual_basis_controls'] for c in cases)>0
    assert sum(c['degenerate_requested_flag_spaces'] for c in cases)>0
    receipt=dict(status='pass',scope='exact finite source-reuse identities and call counts; no full tape simulation',
                 combinatorics=combinatorics(),geometry_and_execution=cases,
                 totals={key:sum(c[key] for c in cases) for key in
                         ('exact_projected_side_rank_checks','degenerate_requested_flag_spaces',
                          'wrong_affine_projection_controls','exact_transform_output_entries',
                          'wrong_dual_basis_controls','mutated_parent_copy_controls')})
    Path(__file__).with_name('nested-fourier-source-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
