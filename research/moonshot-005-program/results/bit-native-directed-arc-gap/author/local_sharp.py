"""Literal small codes attaining the full Clebsch directed-arc lower bound."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import argparse,json
from pathlib import Path
G={1,2,4,8,15}

def rank(rows):
    piv={}
    for v in rows:
        while v:
            k=v.bit_length()-1
            if k in piv:v^=piv[k]
            else:piv[k]=v;break
    return len(piv)

def compile(puncture):
    owners=[i for i in range(16) if i!=puncture];coverage=Counter();q=0;groups=[];own=[]
    if puncture is None:
        b=7;canonical=[0]*3+[1]*3;cliques=[(0,j) for j in (2,4,8,15)]+[(1,j) for j in (3,5,9,14)]+[(6,7),(10,11),(12,13)]
    else:
        assert puncture==6;b=6;canonical=[0]*2+[1]*3;cliques=[(0,j) for j in (2,4,15)]+[(1,j) for j in (3,5,9,14)]+[(7,8),(10,11),(12,13)]
    for bad in canonical:
        keep=[i for i in owners if i!=bad];rows=[sum(1<<j for j in keep if i==j or i^j in G) for i in keep];assert rank(rows)==6;coverage.update(keep);q+=6
    for i,j in cliques:
        assert i in owners and j in owners and (i^j) in G and {i,j}!={0,1};coverage.update([i,j]);q+=1
    assert sorted(coverage)==owners and all(coverage[i]==b for i in owners);return {'active_owners':owners,'bank':b,'canonical_omissions':canonical,'proper_clique_pairs':cliques,'rank':q,'rank_per_bank':str(Fraction(q,b)),'both_directions_0_1_zero':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();d={'full':compile(None),'puncture_6':compile(6)};a.out.mkdir(parents=True,exist_ok=True);(a.out/'LOCAL-SHARPNESS.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print({k:(v['bank'],v['rank']) for k,v in d.items()})
