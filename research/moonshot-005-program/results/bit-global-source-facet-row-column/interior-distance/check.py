#!/usr/bin/env python3
"""Restricted transfer capacities on actual native routes for a disjoint minor."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path

def consume(x,goal):
    current=0
    for i,w in enumerate(sorted(x,reverse=True),1):
        current+=w
        if current>=goal:return i,current-w,current
    raise ValueError('insufficient total')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();base=a.repo/'research/moonshot-005-program/results'
    def unpack(path,pin):
        raw=gzip.decompress((base/path).read_bytes())
        if sha256(raw).hexdigest()!=pin:raise ValueError(path)
        return raw
    layout=json.loads(unpack('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'))
    routes=unpack('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
    H=list(map(set,layout['A2']));D=list(map(set,layout['D4']));dual=layout['dual_D4']
    I=set(range(55));J=set(range(55,111))
    ins=[Counter() for _ in range(3)];outs=[Counter() for _ in range(3)]
    for line in routes.splitlines():
        phase,role,coord,h,d,k,j,i=json.loads(line)
        if h is not None:
            if j in J:ins[0][h]+=8
            if D[dual[d]] & I:outs[0][h]+=8
        if h is not None and H[h] & J:ins[1][d]+=8
        if k is not None and H[k] & I:outs[1][d]+=8
        if k is not None:
            if D[d] & J:ins[2][k]+=8
            if i in I:outs[2][k]+=8
    caps={}
    for k,name in enumerate(['H','D','K']):
        caps[name]=[min(ins[k][v],outs[k][v]) for v in sorted(ins[k].keys()|outs[k].keys())]
    review=base/'bit-global-source-facet-row-column/review/output/DISJOINT-RIM.json'
    data=json.loads(review.read_bytes())
    assert data['exact_disjoint_one_copy_rank']==26125
    assert data['disjoint_receivers']==sorted(I) and data['disjoint_donors']==sorted(J)
    rank=7*26125
    result={'rows':sorted(I),'cols':sorted(J),'disjoint_minor_rank':rank,
            'capacity_histograms':{k:dict(Counter(v)) for k,v in caps.items()},'tariffs':{}}
    caps['middle H/D/K']=sum(caps.values(),[])

    for target in (34560+49,34688):
        distance=rank-target
        result['tariffs'][target]={'necessary_total_changed_capacity':distance,
                                   'minimum_counts_if_only_family_changes':{k:consume(v,distance) for k,v in caps.items()}}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['tariffs'])
if __name__=='__main__':main()
