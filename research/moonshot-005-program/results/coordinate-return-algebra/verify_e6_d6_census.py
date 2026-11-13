#!/usr/bin/env python3
"""Exact finite pair-orthogonal E6/D6 census; no optimality classification."""
import argparse,gzip,hashlib,itertools,json
from pathlib import Path
if not __debug__:raise SystemExit('Exact assertion checks require Python without -O')
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();R=args.repo;OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';WP='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'
def load(p,pin):
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==pin;return json.loads(gzip.decompress(b))
s=load(R/'research/shared-wire-split-composition/data/final.json.gz',SP);w=load(R/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz',WP)
def root(n):
 o=[j for j in range(9) if n>>j&1]
 if len(o)==3:return [2 if j in o else 0 for j in range(8)] if 8 in o else [1 if j in o else -1 for j in range(8)]
 z=[j for j in range(9) if j not in o];x,y=z
 return [1 if j==x else -1 for j in range(8)] if y==8 else [2*(int(j==x)-int(j==y)) for j in range(8)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank_mod(A):
 E={};chosen=[]
 for ix,row in enumerate(A):
  v=[x%65537 for x in row]
  for j in range(8):
   if not v[j]:continue
   if j in E:
    c=v[j];v=[(x-c*y)%65537 for x,y in zip(v,E[j])]
   else:
    c=pow(v[j],-1,65537);E[j]=[x*c%65537 for x in v];chosen.append(ix);break
 return len(E),chosen
N=[n for n in range(512) if n.bit_count() in (3,7)];A=[root(n) for n in N];assert len(N)==120 and all(dot(a,a)==8 for a in A)
H=[s['live'][i] for i in s['hosted']['Dports']];K=[h for g in w['cyclic_dual']['source_groups'] for f in ['B','S','T'] for h in g[f]];B=[h for g in w['cyclic_dual']['source_groups'] for h in g['B']];O=[h for h in H if h not in K];base=O+B;normal={h:s['frames'][s['initial'][h]][0] for h in H};ix={n:i for i,n in enumerate(N)}
assert len(base)==82 and len(O)==74 and all(dot(root(normal[b]),root(normal[c]))==8*int(b==c) for b in B for c in B)
flats={'E6':{},'D6':{}}
for i,j in itertools.combinations(range(120),2):
 cross=dot(A[i],A[j]);assert cross in (-4,0,4)
 f=tuple(k for k,a in enumerate(A) if dot(a,A[i])==dot(a,A[j])==0);kind='E6' if cross else 'D6'
 assert len(f)==(36 if cross else 30)
 if f not in flats[kind]:
  r,chosen=rank_mod([A[k] for k in f]);assert r==6
  flats[kind][f]={'normal_pair':[N[i],N[j]],'full_root_normals':[N[k] for k in f],'rank6_witness_normals':[N[f[k]] for k in chosen],'outside_ports':[h for h in O if ix[normal[h]] in f],'base_ports':[h for h in base if ix[normal[h]] in f]}
assert {k:len(v) for k,v in flats.items()}=={'E6':1120,'D6':3780}
summary={}
for kind,fs in flats.items():
 vals=list(fs.values());summary[kind]={'flats':len(vals),'full_root_lines':len(vals[0]['full_root_normals']),'outside_max':max(len(x['outside_ports']) for x in vals),'base_max':max(len(x['base_ports']) for x in vals),'outside_histogram':{str(q):sum(len(x['outside_ports'])==q for x in vals) for q in sorted(set(len(x['outside_ports']) for x in vals))},'base_histogram':{str(q):sum(len(x['base_ports'])==q for x in vals) for q in sorted(set(len(x['base_ports']) for x in vals))},'base_max_witness':max(vals,key=lambda x:len(x['base_ports']))}
assert summary['E6']['outside_max']==26 and summary['E6']['base_max']==29 and summary['D6']['outside_max']==24 and summary['D6']['base_max']==27
out={'status':'PASS_EXACT_FINITE_PAIR_FLAT_CENSUS','native_sha256':SP,'cyclic_sha256':WP,'source_normals':{str(h):normal[h] for h in H},'B':B,'K':K,'outside':O,'base82':base,'summary':summary,'negative_controls':{'self_pair_has_63_perpendicular_lines':sum(dot(A[0],a)==0 for a in A)==63,'self_pair_forbidden_from_rank6_pair_domain':True,'corrupted_source_rejected':hashlib.sha256((R/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()+b'x').hexdigest()!=SP},'scope':'Exhausts pair-perpendicular finite E6/D6 families only. Universal rank6 optimality needs an independent root-subsystem or matroid completeness theorem.'}
(OUT/'E6-D6-CENSUS.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'status':out['status'],'summary':{k:{a:v for a,v in d.items() if a not in ('base_max_witness','outside_histogram','base_histogram')} for k,d in summary.items()}},indent=2))
