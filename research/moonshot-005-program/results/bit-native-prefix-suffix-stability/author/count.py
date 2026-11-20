#!/usr/bin/env python3
"""Check the integer lower-bound certificates without packages or a numerical optimizer."""
import argparse,gzip,json
from collections import Counter
from pathlib import Path

def minimum_truncated_mass(m,target,cap):
    optimum=[100000]*(target+1);optimum[0]=0
    for weight in m:
        for k in range(target,-1,-1):
            next_k=min(target,k+weight)
            optimum[next_k]=min(optimum[next_k],optimum[k]+min(weight,cap))
    return optimum[target]
def verify(charts,k):
    for sides,w in k.items():
        M=w['common_denominator'];charges=Counter();credit=0;seen=set()
        for s,h,cap,g in w['weighted_cuts']:
            assert s in sides and (s,h,cap)not in seen and g>=0;seen.add((s,h,cap))
            z=charts[s,h];m={int(d):a for d,a in z['chart_multiplicities'].items()}
            numer=8*sum(c[2]-min(c[:2])for c in z['sector_ranks'])-128*z['cost']
            need=max(0,-(-numer//64));credit+=g*minimum_truncated_mass(m.values(),need,cap)
            charges.update({d:g*min(v,cap)for d,v in m.items()})
        penalty=sum(max(0,x-M)for x in charges.values());numer=credit-penalty
        assert numer==w['integer_numerator'] and penalty==w['rounding_penalty'] and max(charges.values())==w['max_charge']
        assert -(-numer//M)==w['minimum_D_nodes'];print(sides,-(-numer//M))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('charts',type=Path);p.add_argument('certificate',type=Path);a=p.parse_args()
    w=json.loads(gzip.decompress(a.charts.read_bytes()));cs={(z['side'],z['plane']):z for z in w};assert len(cs)==len(w)
    v=json.loads(a.certificate.read_text());verify(cs,v)
