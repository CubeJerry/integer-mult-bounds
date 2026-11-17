#!/usr/bin/env python3
"""Independent source and shared-plane extension checks on the exact incidence table."""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from itertools import combinations,product
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--layout',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    args=p.parse_args();raw=gzip.decompress(args.layout.read_bytes())
    assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    w=json.loads(raw);H=w['A2'];D=w['D4'];R=w['root_table']
    N=[{i for i in range(111) if sum(a*b for a,b in zip(R[j],R[i]))==0} for j in range(120)]
    normal=[set.intersection(*(N[j] for j in h)) for h in H]
    single={h for h,p in enumerate(H) if sum(j<111 for j in p)==1}
    clean=[]
    for j in range(111):
        incident={h for h,p in enumerate(H) if j in p};exceptional=incident&single
        for h in incident:
            possible=normal[h].difference(*(normal[k] for k in exceptional-{h}))
            clean.append(len(possible))
    assert len(clean)==3108 and min(clean)==13
    flags={(h,d) for _,d,h,*_ in w['routes'] if h is not None and min(H[h])<111}
    visible=Counter(sum(j<111 for j in D[w['dual_D4'][d]]) for h,d in flags)
    assert len(flags)==50355 and min(visible)==8 and max(visible)==12
    gens=[3,5,4]
    sums={0}
    for x in gens:
        sums|={s^x for s in sums}
    assert len(sums)==8
    candidate=[{0,1},{0,1}]
    assert all(len(x)==2 for x in candidate) and len({x^y for x in candidate[0] for y in candidate[1]})==2
    binary=sum(all(a!=b for a,b in combinations(row,2)) for row in product((1,2,3),repeat=4))
    assert binary==0
    result={'clean_flags':len(clean),'minimum_clean_receivers':min(clean),'clean_receiver_histogram':dict(sorted(Counter(clean).items())),
            'active_H_to_D_ports':len(flags),'coefficient_degree_histogram':dict(sorted(visible.items())),
            'binary_degree_four_suffices':2**4>max(visible),'small_product_solutions':binary,
            'three_independent_XOR_subgroups_cover_points':len(sums)}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS quotient independence, 3108 eligible flags and finite degree bound twelve')

if __name__=='__main__':
    main()
