#!/usr/bin/env python3
"""Independent exact E6 geometry and source-factorization controls."""
import argparse,hashlib,itertools,json,random
from collections import Counter
from pathlib import Path
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def canon(v):return tuple(v if next(x for x in v if x)>0 else[-x for x in v])
def rank(rows):
 p={}
 for x in rows:
  while x:
   j=(x&-x).bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def xor(xs):
 x=0
 for y in xs:x^=y
 return x
def multiply(A,B):return[xor(B[j]for j in range(len(B))if row>>j&1)for row in A]
def geometry(repo):
 p=repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';pin=hashlib.sha256(p.read_bytes()).hexdigest();assert pin=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
 original=[canon(r)for r in json.loads(p.read_text())['native_roots']];assert len(set(original))==111;roots=set(original)
 while True:
  more=set(roots)
  for p,q in itertools.product(roots,repeat=2):
   d=dot(p,q);assert d%2==0;v=canon([x-(d//2)*y for x,y in zip(p,q)]);assert dot(v,v)==4;more.add(v)
  assert len(more)<=120
  if more==roots:break
  roots=more
 full=original+sorted(roots-set(original));assert len(full)==120;ids={r:i for i,r in enumerate(full)};D=[[dot(p,q)for q in full]for p in full];planes=set()
 for i,j in itertools.combinations(range(120),2):
  if abs(D[i][j])==2:
   r=canon([x-(1 if D[i][j]>0 else-1)*y for x,y in zip(full[i],full[j])]);planes.add(tuple(sorted([i,j,ids[r]])))
 planes=sorted(planes);assert len(planes)==1120;hist=Counter();records=[];atlas=[[]for _ in range(111)]
 for number,plane in enumerate(planes):
  i,j=plane[:2];p,q=full[i],full[j];d=D[i][j];inside=[]
  for k,r in enumerate(full):
   ca=4*D[i][k]-d*D[j][k];cb=4*D[j][k]-d*D[i][k]
   if all(12*z==ca*x+cb*y for z,x,y in zip(r,p,q)):inside.append(k)
  assert tuple(inside)==plane;native=[k for k in plane if k<111];assert len(native)<=3;common=[k for k in range(120)if D[i][k]==D[j][k]==0];assert len(common)==36;hist[len(native)]+=1
  for k in native:atlas[k].append(number)
  records.append({'normal_roots':list(plane),'native_facets':native,'full_foreign_roots':common})
 for i,row in enumerate(atlas):
  assert len(row)==28
  for j in range(111):
   if D[i][j]==0:assert sum(j in records[k]['full_foreign_roots']for k in row)==16
  assert all(i not in records[k]['full_foreign_roots']for k in row)
 assert rank([(1<<i)^sum(1<<j for j in range(111)if D[i][j]==0)for i in range(111)])==9
 return {'native_sha256':pin,'reflection_closure_roots':[list(x)for x in full],'normal_planes':records,'native_atlas':atlas,'full_A2_planes':1120,'native_facets_per_chart_histogram':dict(sorted(hist.items())),'charts_per_native_facet':28,'coverage_per_native_foreign_root':16,'maximum_native_facets_per_chart':3,'canonical_rank':9}
def controls():
 rng=random.Random(11051628);cases=[]
 for c,b,V in itertools.product((4,5),(1,2,3),(1,2)):
  n=c*b;N=n*V
  for trial in range(8):
   P=[0]*N;U=[0]*N;supports=[]
   for cohort in range(c):
    for row in range(cohort*b*V,(cohort+1)*b*V):
     P[row]=sum(rng.randrange(2)<<col for col in range(cohort*b*V,(cohort+1)*b*V))
   for alpha in range(n):
    source=alpha//b;targets=rng.sample([i for i in range(c)if i!=source],rng.randrange(4));actual=[]
    for target in targets:
     hit=False
     for row in range(target*b*V,(target+1)*b*V):
      entry=rng.randrange(1<<V);U[row]^=entry<<(alpha*V);hit|=bool(entry)
     if hit:actual.append(target)
    supports.append(actual)
   best=0
   for order in itertools.permutations(range(c)):
    position={x:i for i,x in enumerate(order)}
    good=sum(all(position[alpha//b]<position[j]for j in targets)for alpha,targets in enumerate(supports));best=max(best,good)
   G=[row^(1<<i)for i,row in enumerate(multiply(U,P))];r=rank(G)
   assert r>=V*best>=V*((n+3)//4)
   cases.append({'cohorts':c,'banks':b,'width':V,'trial':trial,'rank':r,'max_good':best})
 sharp=[]
 for b in (1,2,3):
  n=4*b;U=[sum(1<<(j*b+a)for j in range(4)if j!=i)for i in range(4)for a in range(b)]
  r=rank([row^(1<<i)for i,row in enumerate(U)]);assert r==b;sharp.append({'banks':b,'rank':r})
 n=5;identity=[1<<i for i in range(n)];cycle=[1<<((i+1)%n)for i in range(n)];inverse=[1<<((i-1)%n)for i in range(n)]
 own=rank([a^b for a,b in zip(identity,multiply(identity,identity))]);cross=rank([a^b for a,b in zip(identity,multiply(cycle,inverse))]);four=rank([(1<<n)-1]*n)
 assert own==cross==0 and four==1<(n+3)//4
 return {'matrix_cases':cases,'sharp_general_algebra_cases':sharp,'negative_controls':{'own_cohort_allowed_rank':own,'cross_root_preencoder_allowed_rank':cross,'four_foreign_cohorts_allowed_rank':four},'universal_claim_from_written_proof':True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();g=geometry(args.repo);c=controls();args.out.mkdir(parents=True,exist_ok=True)
 (args.out/'GEOMETRY.json').write_text(json.dumps(g,indent=2)+'\n');(args.out/'MATRIX-CONTROLS.json').write_text(json.dumps(c,indent=2)+'\n')
 result={'status':'PASS_EXACT_E6_ONE_HOP_APPLICATION','native_sha256':g['native_sha256'],'full_A2_planes':g['full_A2_planes'],'native_facets_per_chart_histogram':g['native_facets_per_chart_histogram'],'matrix_control_count':len(c['matrix_cases']),'global_rank_lower_bound':'V*ceil(111*b/4)','canonical_rank':'9*b*V','minimum_support_incidence':'1258*b','maximum_one_hop_incidence':'333*b','negative_controls':c['negative_controls'],'new_kappa':False}
 (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
