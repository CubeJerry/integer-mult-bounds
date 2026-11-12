#!/usr/bin/env python3
"""Exact finite candidate check; does not certify a completed supplier."""
import gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parents[2]
repo=P.parents[1]
source=repo/'research/shared-wire-split-composition/data/final.json.gz'
raw=source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883':raise ValueError('source pin')
w=json.loads(gzip.decompress(raw))
hpath=P/'results/joint-additive-history-obstruction/CERTIFICATE.json'
epath=P/'results/eight-packet-prefix/PREFIX.json.gz'
h=json.loads(hpath.read_text());e=json.loads(gzip.decompress(epath.read_bytes()))
def space(frame):
 s={0}
 for b in frame:s|={v^b for v in tuple(s)}
 return frozenset(s)
frames=list(map(space,w['frames']));null={frames[c] for c in h['stations']}
v={77:F(1),10:F(-1),16:F(-1),20:F(1),26:F(1)}
roots=dict(zip(e['donor_roles'],e['roots']))
packet=[sum(v[x]*F(roots[x][j]) for x in v) for j in range(8)]
if any(packet):raise ValueError('not a packet kernel vector')
routes={x:[w['initial'][x]]+[op[3] for op in w['program'] if op[:2]==['MOVE',x]] for x in v}
if any(frames[c] not in null for route in routes.values() for c in route):raise ValueError('outside original-route station')
print(json.dumps({'status':'PASS_FINITE_CANDIDATE_CHECK_ONLY','q':{str(x):str(y) for x,y in v.items()},'Cq':list(map(str,packet)),'original_routes':routes,'source_sha256':hashlib.sha256(raw).hexdigest(),'history_certificate_sha256':hashlib.sha256(hpath.read_bytes()).hexdigest(),'packet_word_sha256':hashlib.sha256(epath.read_bytes()).hexdigest(),'scope':'Conditional on inherited all-time null-response certificate and no additional private or common-dependent records. Original-route coordinate controls only; mixed encodings and new access need a new analysis.'},indent=2))
