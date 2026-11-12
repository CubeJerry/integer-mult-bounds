#!/usr/bin/env python3
"""Finite access inventory for the next investigation; not a gain witness."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
def span(frame):
    s={0}
    for b in frame:s|={v^b for v in tuple(s)}
    return frozenset(s)
p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();P=a.repository/'research/moonshot-005-program'
source=a.repository/'research/shared-wire-split-composition/data/final.json.gz';raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883':raise ValueError('source pin')
w=json.loads(gzip.decompress(raw));hpath=P/'results/joint-additive-history-obstruction/CERTIFICATE.json';h=json.loads(hpath.read_text());epath=P/'results/eight-packet-prefix/PREFIX.json.gz';e=json.loads(gzip.decompress(epath.read_bytes()));C=list(map(span,w['frames']));null={C[c] for c in h['stations']};xs=e['donor_roles'];roots=e['roots'];i=xs.index(77);rows=[]
for j,x in enumerate(xs):
    coefficient=F(int(i==j))-F(sum(u*v for u,v in zip(roots[i],roots[j])),8)
    if not coefficient:continue
    route=[w['initial'][x]]+[op[3] for op in w['program'] if op[:2]==['MOVE',x]]
    outside=[c for c in route if C[c] not in null]
    rows.append({'donor':x,'needed_weighted_correction':str(coefficient),'original_route':route,'stations_outside_receiver189_null_set':outside,'outside_initial_station':C[w['initial'][x]] not in null})
r={'status':'COMPUTATIONALLY_CHECKED_FINITE_ACCESS_INVENTORY_ONLY','source_sha256':hashlib.sha256(raw).hexdigest(),'history_certificate_sha256':hashlib.sha256(hpath.read_bytes()).hexdigest(),'packet_word_sha256':hashlib.sha256(epath.read_bytes()).hexdigest(),'receiver':189,'target_donor':77,'nonzero_required_foreign_coordinates':len(rows),'with_an_original_station_outside_null_set':sum(bool(x['stations_outside_receiver189_null_set']) for x in rows),'coordinates':rows,'scope':'Outside the proved null station set is necessary for a new history-relation response in this access model, not sufficient. No timed pulse, joint NB, common repair, physical cache schedule, cost improvement or new kappa is established. This preparation has not received independent review.'}
a.output.write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='coordinates'})
