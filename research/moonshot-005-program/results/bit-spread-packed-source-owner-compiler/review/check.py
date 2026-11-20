#!/usr/bin/env python3
"""Audit each packed GF64 primitive and all of the actual source owner prices."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path
import numpy as np

def mul(a,b):
    p=0
    for j in range(6):
        if b&(1<<j):p^=a<<j
    for j in range(10,5,-1):
        if p&(1<<j):p^=67<<(j-6)
    return p

def scale_cost(z):
    basis=[sum(((mul(z,1<<j)>>i)&1)<<j for j in range(6)) for i in range(6)]
    rows=basis[:]
    word=[]
    def add(i,j):
        rows[i]^=rows[j]
        word.append((i,j))
    for j in range(6):
        i=next(i for i in range(j,6) if (rows[i]>>j)&1)
        if i!=j:
            add(i,j);add(j,i);add(i,j)
        for i in range(6):
            if i!=j and (rows[i]>>j)&1:add(i,j)
    if rows!=[1<<i for i in range(6)]:raise ValueError("scale")
    for i,j in reversed(word):rows[i]^=rows[j]
    if rows!=basis:raise ValueError("inverse scale")
    return len(word)

ADD=np.array([sum(mul(z,1<<j).bit_count() for j in range(6)) for z in range(64)])
SCALE=np.array([0]+[scale_cost(z) for z in range(1,64)])

def field_word(folder,holder,k,donor,allocated,late,Y,seen):
    typ=np.dtype([('t','u1'),('a','<u2'),('b','<u2'),('z','u1')])
    word=np.frombuffer(gzip.decompress((folder/holder['reduce_file']).read_bytes()),dtype=typ)
    t,d,s,q=(word[f] for f in ('t','a','b','z'))
    if np.any(t>2) or np.any(d>=32*k) or np.any(s>=32*k) or np.any(q>63):raise ValueError('primitive')
    if np.any((t!=1)&(d==s)) or np.any((t!=2)&(q==0)):raise ValueError('singular')
    places=holder['original_field_placements']
    if len(places)!=8 or any(len(x)!=32*k for x in places):raise ValueError('copies')
    flat=[i for v in places for i in v]
    if len(set(flat))!=len(flat) or allocated.intersection(flat):raise ValueError('collision')
    allocated.update(flat)
    price=8*int(ADD[q[t==0]].sum()+SCALE[q[t==1]].sum()+18*(t==2).sum())
    writes=0
    for job in holder['before_departure_late_parities']:
        cof=job['coefficients']
        for dst,start in job['dest_and_first_X']:
            if Y[dst]!=(donor,job['h']) or dst in late or dst in seen:raise ValueError('Y write')
            if any((start+16*i)//3840!=donor for i,z in enumerate(cof) if z):raise ValueError('X read')
            late.add(dst)
            writes+=int(ADD[cof].sum())
    return price,writes,Counter({int(op):int(np.sum(t==op)) for op in (0,1,2)})
def main():
    p=argparse.ArgumentParser()
    for n in ('repo','words','out'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args()
    wd=a.words
    invoice=json.loads((wd/'RESULT.json').read_bytes())
    root=a.repo/'research/moonshot-005-program/results'
    route=gzip.decompress((root/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
    if sha256(route).hexdigest()!='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036':raise ValueError('source pin')
    X,Y={},{}
    for line in route.splitlines():
        phase,role,local,h,d,k,j,i=json.loads(line)
        if h is not None and j is not None:
            dest=X if phase=='X' else Y
            for e in range(8):dest[3840*role+8*local+e+(0 if phase=='X' else 426240)]=(j,h)
    totals=Counter()
    seen=set()
    hist=Counter()
    for donor in sorted(map(int,invoice['special_donor_costs'])):
        holders=json.loads(gzip.decompress((wd/('HOLDERS-%d.json.gz'%donor)).read_bytes()))
        home=set(range(3840*donor,3840*(donor+1)))
        allocated,late=set(),set()
        basis=write=0
        for k in (3,12):
            b,w,h=field_word(wd,holders[f'{donor}-{k}'],k,donor,allocated,late,Y,seen)
            basis+=b
            write+=w
            hist.update(h)
        if allocated!=home or any(X[t][0]!=donor for t in home):raise ValueError('owner coverage')
        swaps=holders[f'{donor}-swaps']
        if any(i==j or i not in home or j not in home for i,j in swaps):raise ValueError('owner swap')
        seen.update(late)
        perm=18*len(swaps)
        tm=6*len(late)
        bill={'basis_ADD':basis,'permutation_ADD':perm,'write_ADD':write,'read_ADD':tm,'INIT':tm,'dirty_CLEAR':tm,
              'forward_ADD':basis+perm+write+tm,'inverse_ADD':basis+perm,'total_ADD':2*(basis+perm)+write+tm}
        if bill!=invoice['special_donor_costs'][str(donor)]:raise ValueError('per-stage invoice')
        totals.update(bill)
    background=json.loads((root/'bit-spread-rs-physical-word/author/source-output/PER-DONOR-COSTS.json').read_bytes())
    bg=Counter()
    for j,b in background.items():
        if j not in invoice['special_donor_costs']:bg.update(b)
    if bg!=invoice['background']:raise ValueError('background')
    inv=bg['early_basis_ADD']+bg['source_owner_permutation_ADD']
    cache=bg['snapshot_copy_ADD_INIT_dirty_CLEAR']
    price=totals['total_ADD']+2*inv+bg['late_evaluation_ADD']+cache
    init=totals['INIT']+cache
    if price!=invoice['combined']['source_forward_and_inverse_ADD'] or init!=invoice['combined']['source_INIT']:raise ValueError('combined')
    out={'charts':invoice['native_chart_count'],'special_donors':len(invoice['special_donor_costs']),'unreplicated_primitives_by_opcode':dict(hist),'true_distinct_late_holders':len(seen),'exact_ADD':price,'exact_INIT_and_dirty_CLEAR_each':init,'additional_MOVE':0}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out)
if __name__=='__main__':main()
