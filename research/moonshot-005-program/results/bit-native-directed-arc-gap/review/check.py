"""Check each directed information inequality in the stabilizer quotient by integer arithmetic."""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import lcm
import json
from pathlib import Path

GEN=(1,2,4,8,15)

def verify(source, puncture):
    dual=json.loads(source.read_bytes())
    weights=[Fraction(t[0]) for t in dual['terms']]
    scale=lcm(*(q.denominator for q in weights))
    field=range(16)
    universe=frozenset(field)-(set() if puncture is None else {puncture})
    neighbors={i:{i^g for g in GEN}&universe for i in universe}
    group=[]
    for late in permutations(GEN[1:]):
        order=(1,)+late
        p=[0]
        for u in order[:4]:
            p.extend([j^u for j in p])
        if puncture is None or p[puncture]==puncture:
            assert len(set(p))==16 and p[0]==0 and p[1]==1
            assert all({p[j] for j in neighbors[i]}==neighbors[p[i]] for i in universe)
            group.append(p)
    @lru_cache(None)
    def key(mask):
        bits=[i for i in field if mask & (1<<i)]
        assert set(bits)<=universe
        return min(sum(1<<p[i] for i in bits) for p in group)
    full=sum(1<<i for i in universe)
    decode_received=full-sum(1<<i for i in {0}|neighbors[0])+2
    assert dual['S']==decode_received
    coef=Counter();value=0
    def add(mask,w):coef[key(mask)]+=w
    def gain(mask,i,w):
        assert i in universe and mask&(1<<i)==0
        add(mask|1<<i,w);add(mask,-w)
    for (weight,kind,*a),q in zip(dual['terms'],weights):
        w=int(q*scale)
        if kind=='unit':
            assert q==Fraction(dual['optimum'])
        elif kind=='empty':add(0,w)
        elif kind=='decode':
            mask,i=a
            assert all(mask&(1<<j)==0 for j in neighbors[i])
            gain(mask,i,w);value+=w
        elif kind=='mono':assert w>0;gain(*a,w)
        elif kind=='monofull':assert w>0;add(full,w);add(a[0],-w)
        elif kind=='diminish':
            u,s,i=a;assert w>0 and not (u & ~s)
            gain(u,i,w);gain(s,i,-w)
        else:raise ValueError(kind)
    z=Fraction(dual['optimum']);assert value==6*scale
    assert {k:x for k,x in coef.items() if x}=={key(full):scale,key(decode_received):int(z*scale),key(decode_received|1):-int(z*scale)}
    return {'terms':len(weights),'group_order':len(group),'cleared_denominator':str(scale),'local_floor':6,'arc_deletion_excess':str(z)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--dual-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result={p.name:verify(p,None if p.name.startswith('CLEBSCH') else 6) for p in sorted(a.dual_dir.glob('*.json')) if ('DUAL' in p.name or 'STRONGER' in p.name)}
    assert 'CLEBSCH-DUAL.json' in result and len(result)>=2
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'REVIEW.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
