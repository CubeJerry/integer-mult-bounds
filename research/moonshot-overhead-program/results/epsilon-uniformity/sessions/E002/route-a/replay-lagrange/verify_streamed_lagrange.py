#!/usr/bin/env python3
"""Exact checks for the new streamed coefficient identity, not tape execution."""
from itertools import combinations
from pathlib import Path
import json

MOD=0b10011

def mul(a,b):
    value=0
    while b:
        if b&1:value^=a
        b>>=1;a<<=1
        if a&16:a^=MOD
    return value

def power(a,e):
    value=1
    while e:
        if e&1:value=mul(value,a)
        a=mul(a,a);e>>=1
    return value

def inv(a):
    assert a
    return power(a,14)

def sumf(values):
    result=0
    for a in values:result^=a
    return result

def dense_coefficients(nodes,j):
    poly=[1];den=1
    for a in nodes:
        if a==j:continue
        nxt=[0]*(len(poly)+1)
        for i,c in enumerate(poly):
            nxt[i]^=mul(a,c);nxt[i+1]^=c
        poly=nxt;den=mul(den,j^a)
    return [mul(c,inv(den)) for c in poly]

def evaluate_product(nodes,j,t):
    result=1
    for a in nodes:
        if a!=j:result=mul(result,mul(t^a,inv(j^a)))
    return result

def stream_coefficient(nodes,j,i,wrong=False):
    exponent=15-i if not wrong else 15+i
    return sumf(mul(power(t,exponent),evaluate_product(nodes,j,t)) for t in range(1,16))

def main():
    assert all(mul(a,inv(a))==1 for a in range(1,16))
    omega=next(a for a in range(2,16) if power(a,2)^a^1==0)
    f4=(0,1,omega,power(omega,2))
    counts={'coefficient_cases':0,'basis_repairs':0,'occupied_extension_vectors':0,
            'zero_gap_containing_sets':0,'wrong_exponent_rejections':0,
            'degree_alias_negative_controls':0}
    for size in (3,5,8):
        nodes=list(range(size));s=min(4,size)
        for ell in range(s+1):
            for js in combinations(nodes,ell):
                lam={}
                for j in js:
                    dense=dense_coefficients(js,j)
                    for i in range(s):
                        want=dense[i] if i<len(dense) else 0
                        value=stream_coefficient(js,j,i)
                        assert value==want
                        lam[j,i]=value
                        counts['coefficient_cases']+=1
                        counts['wrong_exponent_rejections']+=stream_coefficient(js,j,i,True)!=want
                for phase,z in enumerate(f4[1:]):
                    p=[z]*size
                    for j in js:p[j]=f4[(j+phase)%4]
                    if any(p[j]==z for j in js):counts['zero_gap_containing_sets']+=1
                    vectors=[[int(i==col) for i in nodes] for col in nodes]
                    vectors.append([(3*i+5)%16 for i in nodes])
                    for number,vec in enumerate(vectors):
                        delta=[sumf(mul(power(a,i),mul(p[a]^z,vec[a])) for a in nodes) for i in range(s)]
                        y=[sumf(mul(lam[j,l],mul(power(p[j]^z,2),mul(lam[j,i],delta[i]))) for j in js for i in range(s)) for l in range(s)]
                        lift=[sumf(mul(power(a,l),y[l]) for l in range(s)) for a in nodes]
                        out=[mul(p[a],vec[a])^mul(p[a],lift[a])^mul(z,lift[a]) for a in nodes]
                        assert out==[mul(z,v) for v in vec]
                        if number<size:counts['basis_repairs']+=1
                        else:counts['occupied_extension_vectors']+=1
    # Omitting the strict degree bound aliases T^(q-1) into coefficient zero.
    false_constant=sumf(power(t,15) for t in range(1,16))
    assert false_constant==1
    counts['degree_alias_negative_controls']+=1
    assert counts['wrong_exponent_rejections']>0
    result={'status':'PASS_EXACT_STREAMED_LAGRANGE','counts':counts,'modulus':MOD,
            'scope':'Finite coefficient extraction, all-basis repair and occupied extension-field vectors, with alias/exponent adverse controls. No tape execution, asymptotic proof or formal verification.'}
    Path(__file__).with_name('streamed-lagrange-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
