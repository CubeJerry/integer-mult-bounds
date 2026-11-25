#!/usr/bin/env python3
"""Independent exact replay of E002 HS run-sort/short-row transpose."""
from math import gcd
from pathlib import Path
import json

DUMMY=object()

def move_bit(data,prefix,columns,suffix,inverse=False):
    size=2*columns*suffix
    assert len(data)==prefix*size
    out=[]
    for p in range(prefix):
        block=data[p*size:(p+1)*size]
        if inverse:
            for bit in range(2):
                for column in range(columns):
                    start=(2*column+bit)*suffix
                    out.extend(block[start:start+suffix])
        else:
            for column in range(columns):
                for bit in range(2):
                    start=(bit*columns+column)*suffix
                    out.extend(block[start:start+suffix])
    return out

def stable_binary_sort(records,width):
    for bit in range(width):
        records=[r for r in records if not (r[0]>>bit)&1]+[r for r in records if (r[0]>>bit)&1]
    return records

def forward(data,Q,B,c):
    a=c%Q
    if a==1: return list(data)
    q,s=divmod(Q,a); h=(a-1).bit_length(); A=1<<h
    assert A*(q+1)<4*Q
    records=[]
    for r in range(a):
        start=(r*Q+a-1)//a; end=((r+1)*Q+a-1)//a; t=(-r*Q)%a
        assert end-start==q+(t<s)
        payload=list(data[start*B:end*B])
        if end-start==q: payload.extend([DUMMY]*B)
        records.append((t,payload))
    records=stable_binary_sort(records,h)
    assert [t for t,payload in records]==list(range(a))
    rows=[x for t,payload in records for x in payload]+[DUMMY]*((A-a)*(q+1)*B)
    for i in range(h):
        rows=move_bit(rows,1<<(h-i-1),q+1,(1<<i)*B)
    output=[]
    for k in range(q+1):
        for t in range(a if k<q else s):
            start=(k*A+t)*B; output.extend(rows[start:start+B])
    assert DUMMY not in output
    return output

def backward(data,Q,B,c):
    a=c%Q
    if a==1: return list(data)
    q,s=divmod(Q,a); h=(a-1).bit_length(); A=1<<h
    rows=[]
    for k in range(q+1):
        for t in range(A):
            real=t<a and (k<q or t<s)
            rows.extend(data[(a*k+t)*B:(a*k+t+1)*B] if real else [DUMMY]*B)
    for i in reversed(range(h)):
        rows=move_bit(rows,1<<(h-i-1),q+1,(1<<i)*B,inverse=True)
    records=[]; inv=pow(s,-1,a)
    for t in range(a):
        records.append(((-t*inv)%a,t,rows[t*(q+1)*B:(t+1)*(q+1)*B]))
    records=stable_binary_sort(records,h)
    output=[]
    for r,t,payload in records:
        output.extend(payload if t<s else payload[:-B])
    assert DUMMY not in output
    return output

cases=positions=nontrivial=0
for Q in range(2,65):
    for c in range(1,130):
        if gcd(c,Q)!=1: continue
        for B in (1,3):
            data=[(y,t,0 if (y+t)%3==0 else 1) for y in range(Q) for t in range(B)]
            output=forward(data,Q,B,c)
            expected=[None]*(Q*B)
            for y in range(Q):
                expected[(c*y%Q)*B:(c*y%Q+1)*B]=data[y*B:(y+1)*B]
            assert output==expected
            assert backward(output,Q,B,c)==data
            cases+=1; positions+=Q*B; nontrivial+=int(c%Q!=1)

result={'status':'passed','coprime_forward_inverse_cases':cases,
        'exact_record_positions':positions,'nontrivial_run_transposes':nontrivial,
        'scope':'Finite literal run sort, binary digit moves, padding removal and inverse. Complexity and visited-space reviewed separately; no multiplier claim.'}
Path(__file__).with_name('height-priced-scaling-replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
