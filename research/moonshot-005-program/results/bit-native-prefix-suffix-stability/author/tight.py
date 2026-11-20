#!/usr/bin/env python3
"""Revalue the exact counting weights at the stricter outer-port excesses."""
import argparse,gzip,json
from collections import Counter
from pathlib import Path
from count import minimum_truncated_mass
def run(a):
    w=json.loads(gzip.decompress(a.charts.read_bytes()));charts={(z['side'],z['plane']):z for z in w}
    pairs=json.loads(gzip.decompress(a.pairs.read_bytes()));cert=json.loads(a.certificate.read_text());out={}
    for h in (45,49,56,128):
        table={}
        for side,record in sorted(cert.items()):
            credit=0;load=Counter();M=record['common_denominator']
            for s,p,cap,k in record['weighted_cuts']:
                z=charts[s,p];m={int(d):v for d,v in z['chart_multiplicities'].items()}
                need=max(0,(8*sum(x[2]-min(x[:2])for x in z['sector_ranks'])-h*z['cost']+63)//64)
                credit+=k*minimum_truncated_mass(m.values(),need,cap)
                load.update({d:k*min(v,cap)for d,v in m.items()})
            excess=sum(max(0,x-M)for x in load.values());net=credit-excess;bound=(net+M-1)//M
            table[side]={'fractional_dual_numerator':net,'denominator':M,'min_changed_physical_D':bound}
        for s in ('L','R'):
            ns=[]
            for z in pairs:
                if z['side']!=s:continue
                t=max(0,(8*sum(x[2]-min(x[:2])for x in z['sector_ranks'])-h*z['cost']+63)//64);m=sorted(z['chart_multiplicities'].values(),reverse=True)
                ns.append(next(k for k in range(len(m)+1)if sum(m[:k])>=t))
            table[s]['max_changed_D_requiring_103_changed_stars_on_this_side']=min(ns)-1
        out[h]=table;print(h,{s:r['min_changed_physical_D']for s,r in table.items()},{s:table[s]['max_changed_D_requiring_103_changed_stars_on_this_side']for s in ('L','R')},flush=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('charts','pairs','certificate','out'):p.add_argument('--'+n,type=Path,required=True)
 run(p.parse_args())
