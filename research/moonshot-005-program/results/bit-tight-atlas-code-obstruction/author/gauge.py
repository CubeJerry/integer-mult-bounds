#!/usr/bin/env python3
"""Exact fixed-node obstruction with independently variable full donor gauges."""
import argparse
import json
from pathlib import Path
from check import atlas, checked_source

class GF:
    def __init__(self,poly):
        size=1<<(poly.bit_length()-1)
        self.m=[]
        for a in range(size):
            row=[]
            for b in range(size):
                x=a
                out=0
                for k in range(size.bit_length()-1):
                    if (b>>k)&1:
                        out^=x
                    x=x<<1
                    if x&size:
                        x^=poly
                row.append(out)
            self.m.append(row)
        self.inv=[0]+[self.m[i].index(1) for i in range(1,size)]

    def forms(self,nodes):
        p=[1]
        for a in nodes:
            q=[0]*(len(p)+1)
            for j,t in enumerate(p):
                q[j]^=self.m[a][t]
                q[j+1]^=t
            p=q
        return p

    def rank(self,cols):
        piv={}
        for orig in cols:
            v=orig[:]
            for t,p in sorted(piv.items()):
                if v[t]:
                    u=v[t]
                    v=[a^self.m[u][b] for a,b in zip(v,p)]
            if any(v):
                t=next(j for j,x in enumerate(v) if x)
                piv[t]=[self.m[self.inv[v[t]]][x] for x in v]
        return len(piv)


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    args=a.parse_args()
    roots,planes,perp,N,star,active,census=atlas(checked_source(args.repo))
    H=planes.index((7,8,9))
    I=[0,5,49,18,106,17,6,80,79,51,34,91,109,107,108,110]
    assert set(I)<=perp[H] and len(I)==len(set(I))==16
    f=GF(67)
    tables={}
    for j in (7,8):
        coeffs=[f.forms([t for t,h in enumerate(star[j]) if i in perp[h] and h!=H]) for i in I]
        assert all(len(p)==16 and p[-1]==1 for p in coeffs)
        tables[j]={'rank':f.rank(coeffs),'monic_coefficient_vectors':coeffs}
    assert [v['rank'] for v in tables.values()]==[15,16]
    result={'modulus_polynomial_binary':67,'H':[7,8,9],'receivers':I,'donors':tables,'fifteen_stripe_sum_dimensions':[225,240]}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS exact GF64 ranks 15 and 16, arbitrary 240-coordinate gauges excluded')

if __name__=='__main__':
    main()
