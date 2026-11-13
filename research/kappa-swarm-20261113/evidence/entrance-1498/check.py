#!/usr/bin/env python3
"""Finite entrance-only frame gate; no altered producer history."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from collections import defaultdict
import gzip,json,importlib.util,sys,argparse
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
def need(ok,label):
    if not ok:raise ValueError(label)
def run(output):
    raw=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(raw).hexdigest()=='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9','source pin')
    rr=(ROOT/'worker-b/shared-constraint-earlier/BEST-RELATION.json').read_bytes();need(sha256(rr).hexdigest()=='3dc05c86cc34d744144c2e125f6537e3272284d38b738f086e35b5c7cd886b90','relation pin')
    w=json.loads(gzip.decompress(raw));rel=json.loads(rr);u={int(h):Q(v) for h,v in rel['normalized_constraint'].items()};groups=defaultdict(list);cases=[]
    for h in sorted(u):
        f=w['initial'][h];groups[f].append(h);req={j:-a/u[h] for j,a in u.items() if j!=h}
        missing={j:a for j,a in req.items() if w['initial'][j]!=f};need(missing,'noncoframed requirement')
        j=min(missing);travel=abs(len(w['frames'][f])-len(w['frames'][w['initial'][j]]));need(travel==5,'dimension0/5 witness')
        cases.append(dict(demoted=h,entry=f,exit=w['final'][h],lost_target_rank=len(w['frames'][w['final'][h]])-len(w['frames'][f]),
            annihilating_coordinate=j,required_coefficient=str(missing[j]),foreign_donors=sorted(missing),minimum_rank_travel=travel))
    need(set(groups)=={3,1031} and len(groups[3])==42 and groups[1031]==[1498],'two actual entrance classes')
    need(w['frames'][3]==[] and len(w['frames'][1031])==5 and all(w['final'][h]==127 for h in u),'exact source frames')
    local={j:a for j,a in u.items() if j!=1498};h0=min(local)
    need(all(w['initial'][j]==3 for j in local if j!=h0),'remove foreign outlier control is fully coframed')
    path=ROOT/'budget_price.py';spec=importlib.util.spec_from_file_location('entryP',path);P=importlib.util.module_from_spec(spec);sys.modules[spec.name]=P;spec.loader.exec_module(P)
    prices=[]
    for k in [Q(19,5000),Q(1,250)]:
        after=P.moment({1:1,3:1,4:-1,5:-1},k);need(after[1]<0,'preparation wipes gain')
        prices.append(dict(kappa=str(k),before=P.display(P.moment({1:1,3:1,4:-1},k)),preparation=P.display(P.price(5,k)),after=P.display(after)))
    out=dict(status='EXACT_ENTRANCE_ONLY_GATE_BLOCKED',source_sha256=sha256(raw).hexdigest(),relation_sha256=sha256(rr).hexdigest(),
        normalized_constraint=rel['normalized_constraint'],provider_identity=rel['identity'],providers=rel['providers'],
        groups={str(f):hs for f,hs in groups.items()},orientations=cases,zero_paid_orientations=[],minimum_paid_preparation={'5':1},
        cheapest_helper=1498,cheapest_target_rank=4,other_target_rank=9,prices=prices,
        controls=dict(foreign_coordinate_nonzero=True,coframed_outlier_removed_control=True),
        scope='Only entrance scalar-coframed prep from original independent inputs plus owned zeros; fixed native entrance charts and subsequent producer history. Zero initialization at any frame and dirty erasure free. No universal construction exclusion.')
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['normalized_constraint','providers','groups','orientations']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();run(a.output)
