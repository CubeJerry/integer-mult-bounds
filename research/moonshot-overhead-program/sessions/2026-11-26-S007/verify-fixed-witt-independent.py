#!/usr/bin/env python3
"""Realize several Witt lengths inside literal local quotient rings and check ghost/Hasse transport."""
from collections import Counter
from functools import cache
from math import comb
from pathlib import Path
from random import Random
import json
import runpy

fn=runpy.run_path(str(Path(__file__).with_name("verify-fibre-join.py")))
def brem(x,g):return fn["divmod_binary"](x,g)[1]
def pmul(x,y,W):
    guard=2*W+min(len(x),len(y)).bit_length()
    a=sum(u<<(guard*i) for i,u in enumerate(x))
    b=sum(u<<(guard*i) for i,u in enumerate(y))
    p=a*b
    return [(p>>(guard*i))&((1<<W)-1) for i in range(len(x)+len(y)-1)]


class Literal:
    def __init__(self,h,H):
        self.h,self.d,self.H=h,h.bit_length()-1,H
        self.mod=1<<H
        self.zero=(0,)*self.d
        self.one=(1,)+(0,)*(self.d-1)
        self.x=self.reduce([0,1])
        self.z=brem(2,h)
        self.xt=self.teich(self.z)
        self.delta=self.sub(self.x,self.xt)
        assert all(v%2==0 for v in self.delta)

    def reduce(self,values):
        a=list(values)
        a.extend([0]*max(0,self.d-len(a)))
        for i in reversed(range(self.d,len(a))):
            v=a[i]
            for j in range(self.d):
                if self.h>>j&1:
                    a[i-self.d+j]-=v
        return tuple(v%self.mod for v in a[:self.d])

    def add(self,x,y):return tuple((a+b)%self.mod for a,b in zip(x,y,strict=True))
    def sub(self,x,y):return tuple((a-b)%self.mod for a,b in zip(x,y,strict=True))
    def mul(self,x,y):return self.reduce(pmul(x,y,self.H))
    def power(self,x,n):
        v=self.one
        while n:
            if n&1:v=self.mul(v,x)
            x=self.mul(x,x)
            n//=2
        return v

    @cache
    def teich(self,value):
        v=tuple((value>>j)&1 for j in range(self.d))
        # Multiple of the residue Frobenius period, enough to kill the principal units.
        t=self.d*((self.H+self.d-1)//self.d)
        out=self.power(v,1<<t)
        assert self.power(out,1<<self.d)==out
        assert sum((x&1)<<j for j,x in enumerate(out))==value
        return out

    def from_witt(self, coordinates):
        out=self.zero
        for j,s in enumerate(coordinates):
            v=brem(s,self.h)
            root=fn["power"](v,1<<((-j)%self.d),self.h)
            unit=self.teich(root)
            out=self.add(out,tuple((a<<j)%self.mod for a in unit))
        return out

    def horner(self,coeff,x):
        acc=self.zero
        for v in reversed(coeff):
            acc=self.mul(acc,x)
            acc=((acc[0]+v)%self.mod,)+acc[1:]
        return acc

    def unit_inverse(self,word):
        residue=sum((v&1)<<i for i,v in enumerate(word))
        h0=fn["inverse_mod"](residue,self.h)
        current=tuple((h0>>i)&1 for i in range(self.d))
        for _ in range(self.H.bit_length()):
            err=self.sub(self.one,self.mul(word,current))
            current=self.add(current,self.mul(current,err))
        assert self.mul(word,current)==self.one
        return current


def fold(vec,q,W):
    row=[0]*q
    for i,v in enumerate(vec):
        j=0 if i==0 else 1+(i-1)%(q-1)
        row[j]=(row[j]+v)% (1<<W)
    return row


def ghosts(coeff,q,H):
    rows=[]
    for j in range(H):
        W=j+1
        mod=1<<W
        total=[0]*q
        for i,v in enumerate(coeff):
            k=0 if i==0 else 1+(i*(1<<j)-1)%(q-1)
            total[k]=(total[k]+v)%mod
        for k,old in enumerate(rows):
            v=old
            for _ in range(j-k):
                v=fold(pmul(v,v,W),q,W)
            total=[(x-(y<<k))%mod for x,y in zip(total,v,strict=True)]
        assert all(u%(1<<j)==0 for u in total)
        rows.append([u>>j for u in total])
    return [sum(v<<j for j,v in enumerate(row)) for row in rows]


def hasse(coeff,j,H):
    return [(comb(i,j)*coeff[i])% (1<<H) for i in range(j,len(coeff))]


def wort_taylor(r,rows,step):
    out=r.zero
    for powers in reversed(rows):
        out=r.add(r.mul(out,step),r.from_witt(powers))
    return out


def trial(b,H,rng):
    q=1<<b
    factors=fn["fs_order"](b)
    rings=[Literal(g,H) for g in factors]
    counts=Counter()
    for r in rings:
        g=[(r.h>>i)&1 for i in range(r.d+1)]
        gs=[ghosts(hasse(g,j,H),q,H) for j in range(H)]
        d=hasse(g,1,H)
        ds=[ghosts(hasse(d,j,H),q,H) for j in range(H)]
        shift=r.zero
        for _ in range((H-1).bit_length()):
            v=wort_taylor(r,gs,shift)
            inv=r.unit_inverse(wort_taylor(r,ds,shift))
            shift=r.sub(shift,r.mul(v,inv))
        assert r.add(r.xt,shift)==r.x
        counts["actual_literal_factor_Hensel_roots"]+=1
    tests=[[rng.randrange(1<<H) for _ in range(q)] for _ in range(6)]
    tests += [[0]*q,[1]+[0]*(q-2)+[1]]
    for a in tests:
        deriv=[hasse(a,j,H) for j in range(H)]
        rows=[ghosts(d,q,H) for d in deriv]
        for r in rings:
            for d,g in zip(deriv,rows,strict=True):
                assert r.from_witt(g)==r.horner(d,r.xt)
                counts["full_Witt_Teich_coordinate_evaluations"]+=1
            result=wort_taylor(r,rows,r.delta)
            assert result==r.reduce(a)==r.horner(a,r.x)
            counts["actual_monic_remainders"]+=1
            counts["proper_nonprime_remainders"]+=int(1<r.d<b)
            counts["nonzero_Teich_to_literal_Hasse_shifts"]+=int(result!=r.from_witt(rows[0]))
            counts["missing_highest_Hasse_term_detected"]+=int(result!=wort_taylor(r,rows[:-1],r.delta))
    return {"b":b,"H":H,"counts":dict(sorted(counts.items()))}


if __name__=="__main__":
    rng=Random(0x478161)
    cases=[trial(b,H,rng) for b,H in ((2,4),(3,4),(4,4),(4,5),(6,5),(6,6))]
    totals=Counter()
    for case in cases:totals.update(case["counts"])
    assert totals["missing_highest_Hasse_term_detected"] and totals["proper_nonprime_remainders"]
    print(json.dumps({"seed":"0x478161","cases":cases,"totals":dict(sorted(totals.items()))},indent=2))
