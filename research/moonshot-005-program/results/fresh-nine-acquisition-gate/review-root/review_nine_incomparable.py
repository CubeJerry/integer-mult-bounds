#!/usr/bin/env python3
"""Independent robust quadratic-span and exact-nine profile audit."""
import argparse,gzip,hashlib,itertools,json
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
P=1009
def need(ok,why):
 if not ok:raise ValueError(why)
def root(n):
 ones=[j for j in range(9) if n>>j&1]
 if len(ones)==3:return [2 if j in ones else -1 for j in range(9)]
 need(len(ones)==7,'E8 root type');u,v=[j for j in range(9) if j not in ones];return [3*(int(j==u)-int(j==v)) for j in range(9)]
def det(a):
 a=[[x%P for x in row] for row in a];ans=1
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]),None)
  if k is None:return 0
  if k!=j:a[j],a[k]=a[k],a[j];ans=-ans
  v=a[j][j];ans=ans*v%P;iv=pow(v,-1,P)
  for k in range(j+1,len(a)):
   c=a[k][j]*iv%P;a[k]=[(x-c*y)%P for x,y in zip(a[k],a[j])]
 return ans%P
def main(a):
 raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'Native pin');s=json.loads(gzip.decompress(raw));H={s['live'][i] for i in s['hosted']['Dports']};R={h:root(s['frames'][s['initial'][h]][0])[:8] for h in H};projector={h:[R[h][i]*R[h][j] for i in range(8) for j in range(i,8)] for h in H}
 cert=json.loads(a.certificate.read_text());bases=cert['two_disjoint_projector_bases'];need(len(bases)==2,'Two bases');used=set();minors=[]
 for b in bases:
  need(len(b)==len(set(b))==36 and set(b)<=H and not used&set(b),'Disjoint actual36-projector bases');used.update(b);d=det([projector[h] for h in b]);need(d,'Independent integer minor modulo1009');minors.append(d)
 mutant=[projector[h] for h in bases[0]];mutant[0]=mutant[1];need(det(mutant)==0,'Repeated projector negative control')
 cap={1:1,2:2,3:4,4:8,5:16,6:24,7:35,8:96};profiles=[]
 for ranks in itertools.combinations_with_replacement(range(1,9),3):
  if sum(ranks)>17 or ranks==(1,8,8):continue
  best=min(cap[r]+cap[t] for r,t in itertools.combinations(ranks,2));need(best<42,'Every nonexceptional profile violates distance42');profiles.append({'ranks':ranks,'smallest_pair_cap':best})
 need(len(profiles)==96 and max(x['smallest_pair_cap'] for x in profiles)==40,'Exact profile census')
 z7=max(cap[r]+cap[t] for r in range(1,9) for t in range(1,9) if r+t<=8);need(z7==36,'z7 pair bound')
 out={'status':'PASS_INDEPENDENT_EXACT_NINE_INCOMPARABLE_REVIEW','native_sha256':PIN,'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'coordinate_model':'First8 coordinates of integer sum-zero Q9 roots, prime1009; distinct from author B8/65537 minor computation.','two36_minor_residues_mod1009':minors,'two_bases_disjoint':True,'every_single_projector_deletion_retains_full_quadratic_span':True,'profiles':profiles,'z7_pair_cap':z7,'negative_control_repeated_projector':True,'scope':'Finite source premises; separately reviewed all-volume pair-capacity and quadratic contradiction. Exactly9 lower bound; at-most9 optimum only at t199/200 with fresh8 predecessor.'}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','two36_minor_residues_mod1009','every_single_projector_deletion_retains_full_quadratic_span','z7_pair_cap']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
