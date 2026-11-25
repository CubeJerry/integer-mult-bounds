#!/usr/bin/env python3
"""Exact finite identities for HS, not a physical-machine or asymptotic proof."""
from math import gcd
from pathlib import Path
import json


def sort_rows(rows,h):
    out=list(rows)
    for b in range(h):
        parts=[[],[]]
        for key,payload in out:
            parts[(key>>b)&1].append((key,payload))
        out=parts[0]+parts[1]
    return out


def transpose(data,A,C,inverse=False):
    h=(A-1).bit_length()
    assert A==1<<h
    steps=range(h-1,-1,-1) if inverse else range(h)
    out=list(data)
    for k in steps:
        high=A>>(k+1); low=1<<k
        nxt=[None]*len(out)
        for p in range(high):
            for b in range(2):
                for c in range(C):
                    for lo in range(low):
                        src=(((p*2+b)*C+c)*low+lo)
                        dst=(((p*C+c)*2+b)*low+lo)
                        if inverse:src,dst=dst,src
                        nxt[dst]=out[src]
        out=nxt
    return out


def positive(blocks,c,inverse=False,wrong_sign=False):
    Q=len(blocks)
    if Q==1:return list(blocks)
    a=c%Q
    assert a and gcd(a,Q)==1
    if a==1:return list(blocks)
    q,s=divmod(Q,a); h=(a-1).bit_length(); A=1<<h
    if not inverse:
        runs=[]; pos=0; t=0; delta=Q%a
        for r in range(a):
            length=q+(t<s)
            payload=list(blocks[pos:pos+length]); pos+=length
            if length==q:payload.append(None)
            runs.append((t,payload))
            t=(t+delta if wrong_sign else t-delta)%a
        assert pos==Q
        rows=[row for _,row in sort_rows(runs,h)]
        rows.extend([[None]*(q+1) for _ in range(A-a)])
        flat=transpose([z for row in rows for z in row],A,q+1)
        out=[flat[k*A+t] for k in range(q+1) for t in range(a) if k<q or t<s]
        assert len(out)==Q and None not in out
        return out
    padded=[];pos=0
    for k in range(q+1):
        for t in range(A):
            if t<a and (k<q or t<s):
                padded.append(blocks[pos]);pos+=1
            else:padded.append(None)
    flat=transpose(padded,A,q+1,inverse=True)
    inv=pow(Q%a,-1,a)
    rows=[((-t*inv)%a,(t,flat[t*(q+1):(t+1)*(q+1)])) for t in range(a)]
    out=[]
    for _,(t,row) in sort_rows(rows,h):out.extend(row[:q+(t<s)])
    assert len(out)==Q and None not in out
    return out


def scale(blocks,c,inverse=False):
    out=positive(blocks,abs(c),inverse)
    return out if c>0 else out[:1]+out[:0:-1]


def oracle(blocks,c):
    out=[None]*len(blocks)
    for y,z in enumerate(blocks):out[(c*y)%len(blocks)]=z
    return out

def main():
    counts=dict(integer_forward=0,integer_inverse=0,signed=0,rational=0,
                transpose=0,run_identity=0,wrong_sign_rejected=0,ragged_padding_rejected=0)
    witnesses=[]
    for Q in range(1,97):
        blocks=[(2,y,tuple((2,y,z) for z in range(3))) for y in range(Q)]
        for c in range(1,3*Q+3):
            if gcd(c,Q)!=1:continue
            out=positive(blocks,c)
            assert out==oracle(blocks,c)
            counts['integer_forward']+=1
            assert positive(out,c,inverse=True)==blocks
            counts['integer_inverse']+=1
            assert scale(blocks,-c)==oracle(blocks,-c)
            counts['signed']+=1
            a=c%Q if Q>1 else 0
            if a>1:
                q,s=divmod(Q,a)
                for r in range(a):
                    first=(r*Q+a-1)//a;stop=((r+1)*Q+a-1)//a;t=(-r*Q)%a
                    assert stop-first==q+(t<s)
                    for k in range(stop-first):
                        assert (a*(first+k))%Q==a*k+t
                        counts['run_identity']+=1
                bad=positive(blocks,c,wrong_sign=True)
                if bad!=out:
                    counts['wrong_sign_rejected']+=1
                    if len(witnesses)<4:witnesses.append(dict(Q=Q,coefficient=c,error='wrong residue sign'))
                if s:
                    assert a*(q+1)>Q
                    counts['ragged_padding_rejected']+=1
    for Q in range(1,65):
        blocks=list(range(Q))
        for n in range(-9,10):
            for d in range(1,10):
                if not n or gcd(n*d,Q)!=1:continue
                out=scale(positive(blocks,d,inverse=True),n)
                residue=(n*pow(d,-1,Q))%Q if Q>1 else 0
                assert out==oracle(blocks,residue)
                counts['rational']+=1
    for h in range(8):
        A=1<<h
        for C in range(1,40):
            data=[(r,c) for r in range(A) for c in range(C)]
            out=transpose(data,A,C)
            assert out==[(r,c) for c in range(C) for r in range(A)]
            assert transpose(out,A,C,inverse=True)==data
            counts['transpose']+=1
    assert counts['wrong_sign_rejected'] and counts['ragged_padding_rejected']
    report=dict(status='PASS_EXACT_FINITE_HS_IDENTITIES',counts=counts,
                source_pin='3344da59991ed94f9ba711217b29c1d760badfa6',negative_witnesses=witnesses,
                scope='Finite exact arithmetic/permutation checks only, not physical tape execution or an asymptotic proof.')
    Path(__file__).with_name('height-streams-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
