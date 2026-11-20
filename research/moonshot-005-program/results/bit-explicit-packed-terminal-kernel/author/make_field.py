"""Choose a binary degree-24 field and its native GF64 coefficient basis."""
import json
from pathlib import Path


def mul(a,b,f):
    v=0
    while b:
        if b&1:v^=a
        a*=2
        if a>>24:a^=f
        b//=2
    return v


def power(x,n,f):
    z=1
    while n:
        if n&1:z=mul(z,x,f)
        x=mul(x,x,f);n//=2
    return z


def gcd(a,b):
    while b:
        while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
        a,b=b,a
    return a


def make():
    Q=1<<24;n=Q-1
    for low in range(3,256,2):
        f=Q+low
        if power(2,Q,f)!=2 or any(gcd(f,power(2,1<<(24//z),f)^2)!=1 for z in (2,3)):continue
        if any(power(2,n//r,f)==1 for r in (3,5,7,13,17,241)):continue
        break
    else:raise ValueError('no low-degree primitive modulus')
    root=power(2,n//63,f)
    z=next(a for k in range(1,64) if power((a:=power(root,k,f)),6,f)^a^1==0)
    basis=[mul(power(2,k,f),power(z,l,f),f) for k in range(4) for l in range(6)]
    rows={}
    for i,v in enumerate(basis):
        y=1<<i
        while v:
            c=v.bit_length()-1
            if c not in rows:
                rows[c]=v,y;break
            u,w=rows[c];v^=u;y^=w
        if not v:raise ValueError('not a 24-bit native basis')
    inverse=[]
    for i in range(24):
        v=1<<i;y=0
        while v:
            q,w=rows[v.bit_length()-1];v^=q;y^=w
        inverse.append(y)
    return {'binary_modulus':f,'native_Galois_generator':z,'native_basis':basis,'inverse_basis':inverse,'primitive':2}


if __name__=='__main__':print(json.dumps(make()))
