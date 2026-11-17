#!/usr/bin/env python3
"""Exact near-full signature antichain and private-terminal capacity premises."""
from argparse import ArgumentParser
from collections import Counter
from functools import reduce
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json

PIN='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'

def run(path):
 raw=path.read_bytes();assert sha256(raw).hexdigest()==PIN;R=json.loads(raw)['native_roots'];N=[frozenset(j for j,s in enumerate(R) if sum(x*y for x,y in zip(r,s))==0) for r in R]
 order=Counter(len(a-b) for j,a in enumerate(N) for k,b in enumerate(N) if j!=k);overlap=Counter(len(a&b) for a,b in combinations(N,2))
 i,j=next((i,j) for i,a in enumerate(N) for j,b in enumerate(N) if i!=j and len(a-b)==min(order));deleted=N[i]-N[j];assert len(deleted)==21 and N[i]-deleted<=N[j]-deleted
 x,y=next((i,j) for i,a in enumerate(N) for j,b in enumerate(N) if i<j and len(a&b)==min(overlap));t=sorted(N[x]&N[y]);assert len(t)==23 and len((N[x]-set(t[:-2]))&(N[y]-set(t[:-2])))==2
 return {'status':'PASS_NEAR_FULL_EXACT_SIGNATURE_GATE','native_sha256':PIN,'N':len(R),'foreign_incidences':sum(map(len,N)),
          'degree_histogram':dict(sorted(Counter(map(len,N)).items())), 'ordered_difference_histogram':dict(sorted(order.items())),
          'unordered_intersection_histogram':dict(sorted(overlap.items())),
          'first_comparability_deletion_control':{'pair':[i,j],'deleted':sorted(deleted)},
          'first_two_private-exceptions_intersection_control':{'pair':[x,y],'deleted':t[:-2],'left':t[-2:]},
          'applicability':'At most 20 arbitrary receiver roles omitted; direct final terminals and own exact-signature anchors only. Cross-group multistage taps and other relay networks are outside the result.'}
if __name__=='__main__':
 p=ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.native);a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
