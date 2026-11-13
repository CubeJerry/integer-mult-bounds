"""Exact finite premises for the nine-packet comparable-birth price gate."""
import argparse,collections,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CP='9ec15dbf981c3a238b0c4687a717d5a3f32dc730099b29eb47b66b430f27983c'
B=[5,56,69,100,65,77,96,103]
def root(n):
 t=[i for i in range(9) if n>>i&1]
 if len(t)==3:return [2 if i in t else -1 for i in range(9)]
 assert len(t)==7;z=[i for i in range(9) if i not in t]
 return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 e={}
 for rr in rows:
  x=list(map(F,rr))
  for j in range(len(x)):
   if not x[j]:continue
   if j in e:
    c=x[j];x=[v-c*w for v,w in zip(x,e[j])]
   else:
    c=x[j];e[j]=[v/c for v in x];break
 return len(e)
def det(rows):
 x=[list(map(F,r)) for r in rows];d=F(1)
 for j in range(len(x)):
  k=next((k for k in range(j,len(x)) if x[k][j]),None)
  if k is None:return F(0)
  if k!=j:x[j],x[k]=x[k],x[j];d=-d
  v=x[j][j];d*=v;x[j]=[w/v for w in x[j]]
  for k in range(j+1,len(x)):
   v=x[k][j];x[k]=[a-v*b for a,b in zip(x[k],x[j])]
 return d
def main(a):
 raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 cr=a.cap_certificate.read_bytes();assert hashlib.sha256(cr).hexdigest()==CP;cap=json.loads(cr);assert cap['source_pin']==SP
 caps={int(r):v for r,v in cap['rank_caps'].items()};assert caps=={1:1,2:2,3:4,4:8,5:16,6:24,7:35}
 s=json.loads(gzip.decompress(raw));H=[s['live'][i] for i in s['hosted']['Dports']];ns={h:s['frames'][s['initial'][h]][0] for h in H};R={h:root(ns[h]) for h in H}
 assert len(H)==len(set(H))==96 and all(dot(R[i],R[j])==18*int(i==j) for i in B for j in B)
 G={h:[F(dot(R[h],R[b]),9) for b in B] for h in H};assert rank(list(G.values()))==8
 assert rank([[v[p]*v[q] for p in range(8) for q in range(p,8)] for v in G.values()])==36
 I={c:{h for h in H if not((ns[h]&c).bit_count()%2)} for c in range(1,512)};hist=collections.Counter();eligible=[]
 for c in range(1,512):
  rr=rank([G[h] for h in H if h not in I[c]]);hist[rr]+=1
  if rr==7:
   eligible.append(c);rc=root(c);assert all((dot(rc,R[h])!=0)==(h in I[c]) for h in H)
 assert dict(hist)=={8:487,7:24}
 bases=[]
 for c in eligible:
  chosen=set();two=[]
  for _ in range(2):
   b=[]
   for h in sorted(I[c]-chosen):
    if rank([G[j] for j in b+[h]])>len(b):b.append(h)
    if len(b)==8:break
   assert len(b)==8;dd=det([G[h] for h in b]);assert dd;chosen.update(b);two.append({'roles':b,'det_twice_unit_coordinates':str(dd)})
  assert set(two[0]['roles']).isdisjoint(two[1]['roles']);bases.append({'binary_line':c,'population':len(I[c]),'two_disjoint_root_bases':two})
 assert min(len(I[c]) for c in eligible)==43 and max(len(I[c]) for c in eligible)==52
 pairs=[{'c':c,'d':d,'intersection':len(I[c]&I[d])} for c,d in itertools.combinations(eligible,2)]
 assert len(pairs)==276 and min(p['intersection'] for p in pairs)==15 and max(p['intersection'] for p in pairs)==28
 cheap=[(caps[r]+caps[t],r,t) for r in range(1,8) for t in range(1,8) if r+t<=9];assert max(x[0] for x in cheap)==37
 shared5=[(min(caps[r],28)+caps[t],r,t) for r in range(5,8) for t in range(1,8) if r+t<=10]
 shared4=[(min(caps[r],28)+caps[t],r,t) for r in range(5,8) for t in range(1,8) if r+t<=11]
 assert max(x[0] for x in shared5)==32 and max(x[0] for x in shared4)==40
 bad=[G[h] for h in bases[0]['two_disjoint_root_bases'][0]['roles']];bad[0]=bad[1];assert det(bad)==0
 out={'status':'PASS_NINE_COMPARABLE_BIRTH_SOURCE_PREMISES','source_sha256':SP,'cap_dependency_sha256':CP,'source_projector_rank':36,'line_outside_root_rank_histogram':dict(hist),'eligible_lines':eligible,'eligible_population_min':43,'eligible_population_max':52,'two_disjoint_bases_every_eligible_line':bases,'eligible_pair_count':276,'eligible_pair_intersection_min':15,'eligible_pair_intersection_max':28,'eligible_pair_intersection_histogram':dict(sorted(collections.Counter(x['intersection'] for x in pairs).items())),'minimum_intersection_witnesses':[p for p in pairs if p['intersection']==15],'maximum_intersection_witnesses':[p for p in pairs if p['intersection']==28],'cheap_pair_support_max_rank_sum9':max(cheap),'shared_center_z5_support_max':max(shared5),'shared_center_z4_support_max':max(shared4),'same_line_pair_z6_source_coverage_bound':89,'negative_controls':{'repeated_basis_row_has_zero_determinant':True},'scope':'Exact finite premises; all-V comparable-birth theorem and mixed capacity lemma in PROOF.md. Pairwise incomparable line births remain open.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','source_projector_rank','eligible_population_min','eligible_population_max','eligible_pair_intersection_min','eligible_pair_intersection_max','cheap_pair_support_max_rank_sum9','shared_center_z5_support_max','shared_center_z4_support_max']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--cap-certificate',type=Path,default=Path(__file__).with_name('CAP-CERTIFICATE.json'));main(p.parse_args())
