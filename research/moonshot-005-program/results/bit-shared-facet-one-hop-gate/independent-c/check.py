#!/usr/bin/env python3
"""Independent signed-support geometry and direct finite matrix controls."""
from pathlib import Path
from collections import Counter
import json,hashlib,itertools,random,argparse
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));patterns=sorted({tuple(i for i,v in enumerate(r)if v)for r in R if sum(bool(v)for v in r)==4});assert len(patterns)==14
full={tuple(2*int(i==j)for i in range(8))for j in range(8)}
for S in patterns:
 for signs in itertools.product([-1,1],repeat=3):
  v=[0]*8;v[S[0]]=1
  for k,s in zip(S[1:],signs):v[k]=s
  full.add(tuple(v))
full=sorted(full);assert len(full)==120 and set(map(tuple,R))<=set(full);charts={};rows=[]
for i,r in enumerate(R):
 local=set()
 for q in full:
  d=dot(r,q)
  if abs(d)!=2:continue
  def belongs(x):
   aa=dot(r,x);bb=dot(q,x);return (16-d*d)*dot(x,x)-4*(aa*aa+bb*bb)+2*d*aa*bb==0
  roots=tuple(t for t,x in enumerate(full)if belongs(x));assert len(roots)==3;local.add(roots)
  native=[j for j,x in enumerate(R)if belongs(x)];inside=[j for j,x in enumerate(R)if dot(r,x)==dot(q,x)==0];assert set(native).isdisjoint(inside);assert len(native)<=3
  charts[roots]={'normal_full_indices':list(roots),'native_facet_indices':native,'source_indices':inside}
 assert len(local)==28;rows.append({'receiver':i,'atlas_count':28})

def rank(A,p):
 A=[r[:]for r in A];t=0
 for c in range(len(A[0])):
  z=next((i for i in range(t,len(A))if A[i][c]%p),None)
  if z is None:continue
  A[t],A[z]=A[z],A[t];iv=pow(A[t][c],-1,p);A[t]=[x*iv%p for x in A[t]]
  for i in range(t+1,len(A)):
   v=A[i][c];A[i]=[(x-v*y)%p for x,y in zip(A[i],A[t])]
  t+=1
 return t
rng=random.Random(159);controls=[]
for prime in [2,3,5]:
 for b,V,m in [(1,1,7),(2,1,7),(2,2,7),(3,2,5)]:
  n=m*b;N=n*V
  for sample in range(20):
   P=[[0]*N for _ in range(N)];U=[[0]*N for _ in range(N)];supports=[]
   for c in range(m):
    for x in range(b*V):
     for y in range(b*V):P[c*b*V+x][c*b*V+y]=rng.randrange(prime)
   for alpha in range(n):
    own=alpha//b;S=rng.sample([i for i in range(m)if i!=own],rng.randrange(4));supports.append(S)
    for target in S:
     for x in range(b*V):
      for y in range(V):U[target*b*V+x][alpha*V+y]=rng.randrange(prime)
   A=[[int(i==j)-sum(U[i][k]*P[k][j]for k in range(N))for j in range(N)]for i in range(N)]
   rr=rank(A,prime);bound=((n+3)//4)*V;assert rr>=bound;controls.append({'field':prime,'b':b,'V':V,'cohorts':m,'rank':rr,'bound':bound})
# Removing the no-own-cohort condition permits U=P=I and zero residual.
# Removing cohort-diagonal P permits U a cyclic shift and P its inverse.
N=7;U=[[int(i==(j+1)%N)for j in range(N)]for i in range(N)];P=[[int(j==(i+1)%N)for j in range(N)]for i in range(N)];assert all(sum(U[i][k]*P[k][j]for k in range(N))==int(i==j)for i in range(N)for j in range(N))
r={'status':'PASS_INDEPENDENT_ONE_HOP_GEOMETRY_AND_MATRIX_CONTROLS','native_sha256':hashlib.sha256(raw).hexdigest(),'full_root_reconstruction':'Eight doubled axes plus all signed lines on14 actual four-supports, independent of author reflection code.','full_roots':120,'distinct_charts_incident_to_native_facets':len(charts),'native_facet_multiplicity_distribution':dict(Counter(len(c['native_facet_indices'])for c in charts.values())),'charts':list(charts.values()),'native_rows':rows,'matrix_cases':len(controls),'matrix_controls':controls,'negative_scope_controls':['Own-cohort identity U=P=I has residual rank0.','A cyclic cross-cohort P inverse to U gives residual0 despite one foreign target per U column.'],'universal_proof_is_not_inferred_from_controls':True};(Path(__file__).parent/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['distinct_charts_incident_to_native_facets'],r['native_facet_multiplicity_distribution'],len(controls))
