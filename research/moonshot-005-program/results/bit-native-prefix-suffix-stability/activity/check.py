"""Verify a positive integer cover for all chart-rank losses on genuine native pairs."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();r=a.repo/'research/moonshot-005-program/results'
    raw=gzip.decompress((r/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    L=json.loads(raw);V=L['root_table'][:111]
    D=[set(v)&set(range(111)) for v in L['D4']]
    O=[{j for j,v in enumerate(V) if sum(x*y for x,y in zip(v,u))==0} for u in V]
    terms=json.loads((Path(__file__).resolve().parent/'output/WEIGHTS.json').read_bytes())
    units={tuple(k):w for k,w in terms['weights_by_port_type']}
    assert all(w>=0 for w in units.values())
    cover={};counts=Counter()
    for i,N in enumerate(O):
        for j in N:
            tag=(len(N),len(O[j]),sum(x!=0 for x in V[i]),sum(x!=0 for x in V[j]),sum(x*y!=0 for x,y in zip(V[i],V[j])))
            cover[i,j]=units.get(tag,0)
    prices=[]
    for d,A in enumerate(D):
        rows=D[L['dual_D4'][d]];prices.append(sum(cover[i,j] for i in rows for j in A))
        counts.update((i,j) for i in rows for j in A)
    assert set(counts)==set(cover) and len(counts)==6470 and set(counts.values())=={60}
    assert len(D)==3150 and min(prices)==terms['minimum_coverage']==10000032
    mass=sum(cover.values());h=128;cap=64;b=3840
    assert mass==571622576 and b==60*cap and 6*h==12*cap
    bound=(6*h*mass)//(cap*min(prices))
    assert bound==685 and (bound+1)*min(prices)>12*mass
    result={'proper_pairs':len(cover),'middle_charts':len(D),'pair_sections':60,'capacity_per_section':64,
            'field_excess':h,'minimum_integer_charge_per_chart':min(prices),'total_pair_weight':mass,
            'upper_bound_fully_disabled_charts':bound,'minimum_active_charts':len(D)-bound,
            'uniform_deficit_field_sum_bound':(6*h*mass)//min(prices)}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
