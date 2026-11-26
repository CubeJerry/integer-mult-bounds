#!/usr/bin/env python3
"""Exact sibling-space, shear, and adjoint-tree controls."""
from itertools import product
from random import Random
from pathlib import Path
import json
from verify_nested_fourier_source_reuse import basis,dot,walsh,states,invoice


def shear(values,alpha):
    assert not alpha&1
    return [values[z^alpha if z&1 else z] for z in range(len(values))]


def leaf(values,axes,alpha):
    mask=sum(1<<i for i in axes)
    out=shear(walsh(values,[0]),alpha&~mask)
    return [-x if (z&1 and dot(z,alpha&mask)) else x for z,x in enumerate(out)]


def all_shears():
    entries=negative=cases=0;rng=Random(26112026)
    for d in range(1,7):
        n=1<<d
        for W in range(1<<(d-1)):
            axes=[i+1 for i in range(d-1) if W>>i&1]
            for alpha0 in range(1<<(d-1)):
                alpha=alpha0<<1
                vectors=([int(i==j) for i in range(n)] for j in range(n)) if d<=4 else (
                    [rng.randrange(-3,4) for _ in range(n)] for _ in range(2))
                for values in vectors:
                    direct=shear(walsh(walsh(values,[0]),axes),alpha)
                    actual=walsh(leaf(values,axes,alpha),axes)
                    assert actual==direct
                    bad=walsh(shear(walsh(values,[0]),alpha&~sum(1<<i for i in axes)),axes)
                    negative+=sum(x!=y for x,y in zip(bad,direct))
                    entries+=n;cases+=1
    assert negative
    return dict(exact_shear_cases=cases,exact_shear_entries=entries,
                omitted_conjugation_phase_negative_entries=negative)


def coordinates(B):
    pivots={}
    for i,vector in enumerate(B):
        tag=1<<i;x=vector
        while x:
            p=x.bit_length()-1
            if p in pivots:
                row,old=pivots[p];x^=row;tag^=old
            else:
                pivots[p]=x,tag
                break
        assert x
    def encode(x):
        tag=0
        while x:
            p=x.bit_length()-1
            assert p in pivots
            row,old=pivots[p];x^=row;tag^=old
        return tag
    return encode


def destination(q,L,w):
    t=q.bit_length()-1
    labels=tuple(product(range(q),repeat=L));ix={v:i for i,v in enumerate(labels)}
    rows=[sum((1-(sum(a!=b for a,b in zip(v,z))&1))<<j for j,z in enumerate(labels)) for v in labels]
    D=len(basis(rows));wi=ix[w];dw=rows[wi]
    def neighbor(i,a):
        v=list(w);v[i]=a
        return ix[tuple(v)]
    ev=neighbor(0,w[0]^1);e=rows[ev]
    B=[e];coeff=[1<<ev];blocks=[[None]*t for _ in range(L)];slots=[[[] for _ in range(t)] for _ in range(L)]
    independence=0
    for i in range(L):
        for s in range(t):
            start=((w[i]>>s)^1)<<s
            letters=tuple(range(start,start+(1<<s)));blocks[i][s]=letters
            base=neighbor(i,letters[0])
            for a in letters[1:]:
                j=neighbor(i,a);z=rows[j]^rows[base]
                assert not ((z>>wi)&1)
                assert len(basis(B+[z]))==len(B)+1
                slots[i][s].append(len(B));B.append(z);coeff.append((1<<j)^(1<<base));independence+=1
    assert independence==L*(q-1-t)
    for j,row in enumerate(rows):
        c=(1<<j)^(((row>>wi)&1)<<wi)
        z=row^(((row>>wi)&1)*dw)
        if c.bit_count()%2:z^=e;c^=1<<ev
        assert c.bit_count()%2==0
        if len(basis(B+[z]))>len(B):B.append(z);coeff.append(c)
        if len(B)==D-1:break
    assert len(B)==D-1
    assert all(c.bit_count()%2==0 for c in coeff[1:])
    encode=coordinates(B);d=len(B);n=1<<d;Q=states(L,t)
    cache={s:[0]*n for s in Q};direct_total=[0]*n
    rng=Random(261126+q+sum(w));rectangles=internal_alpha=spanchecks=0
    for choices in product(range(-1,t),repeat=L):
        if sum(s>=0 for s in choices)%2!=1:continue
        state=tuple(max(0,s) for s in choices)
        axes=[a for i,s in enumerate(choices) if s>=0 for a in slots[i][s]]
        base=0;side=[]
        for i,s in enumerate(choices):
            if s<0:side.append((w[i],))
            else:
                letters=blocks[i][s];side.append(letters)
                base^=rows[neighbor(i,letters[0])]
        code=encode(base);assert code&1
        alpha=code^1;mask=sum(1<<a for a in axes)
        if alpha&mask:internal_alpha+=1
        side_rows=[rows[ix[v]] for v in product(*side)]
        U=[B[a] for a in axes]
        assert len(basis(side_rows))==len(U)+1
        assert len(basis(side_rows+[base]+U))==len(U)+1
        spanchecks+=1
        values=[rng.randrange(-2,3) for _ in range(n)]
        z=leaf(values,axes,alpha)
        expected=shear(walsh(walsh(values,[0]),axes),alpha)
        assert walsh(z,axes)==expected
        cache[state]=[a+b for a,b in zip(cache[state],z)]
        direct_total=[a+b for a,b in zip(direct_total,expected)]
        rectangles+=1
    edge_cost=0
    for s in reversed(Q):
        if not any(s):continue
        ell=min(a for a in s if a);i=s.index(ell);p=list(s);p[i]=0;p=tuple(p)
        axes=slots[i][ell]
        assert len(axes)==(1<<ell)-1
        transformed=walsh(cache[s],axes)
        cache[p]=[a+b for a,b in zip(cache[p],transformed)]
        edge_cost+=len(axes)
    assert cache[(0,)*L]==direct_total
    row=invoice(L,t);Qsize=t**L-(t-1)**L
    assert edge_cost==2*row['shared_source_axes']-(Qsize-1)
    shared=2*(D-1)+2*rectangles+2*row['shared_source_axes']+2*edge_cost
    if (q,L)==(4,4):assert shared==154
    return dict(q=q,L=L,destination=w,auxiliary_dimension=d,
                independent_internal_directions=independence,exact_rectangle_span_checks=spanchecks,
                representatives_with_selected_internal_components=internal_alpha,
                rectangle_contributions=rectangles,complete_accumulation_output_entries=n,
                source_edge_axes=row['shared_source_axes'],destination_edge_axes=edge_cost,
                shared_free_axis_invoice=shared)


def profiles():
    checked=0;examples=[]
    for L in range(2,22,2):
        for t in range(1,31):
            r=invoice(L,t);Q=t**L-(t-1)**L;S=r['shared_source_axes'];T=2*S-(Q-1)
            exact=sum(((1<<ell)-1)*((t-ell+1)**L-2*(t-ell)**L+(t-ell-1)**L) for ell in range(1,t))
            assert exact==T and 0<=T<=r['old_source_axes']
            free=2*(r['D']-1)+2*r['incidence']+2*S+2*T
            assert free<=r['nested_free_axes']
            if L==4 and t in (2,3,4,8,16):examples.append(dict(L=L,t=t,S=S,T=T,states=Q,shared_free_axes=free))
            checked+=1
    return dict(exact_integer_profiles=checked,examples=examples)


def main():
    cases=[destination(q,L,w) for q,L,w in
           [(2,4,(0,0,0,0)),(4,2,(1,2)),(4,4,(0,0,0,0)),
            (4,4,(1,2,3,1)),(8,2,(3,6))]]
    assert sum(c['representatives_with_selected_internal_components'] for c in cases)>0
    receipt=dict(status='pass',scope='exact shear, actual Gram geometry and independent-input accumulation; no tape simulation',
                 shear_controls=all_shears(),destination_cases=cases,invoice_controls=profiles(),
                 total_span_checks=sum(c['exact_rectangle_span_checks'] for c in cases),
                 total_accumulation_entries=sum(c['complete_accumulation_output_entries'] for c in cases))
    Path(__file__).with_name('shared-fourier-destination-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
