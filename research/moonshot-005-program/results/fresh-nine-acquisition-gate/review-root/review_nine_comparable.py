#!/usr/bin/env python3
"""Independent modular certificates for characteristic-zero source premises."""
import argparse,collections,gzip,hashlib,itertools,json
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CAP='9ec15dbf981c3a238b0c4687a717d5a3f32dc730099b29eb47b66b430f27983c'
PRIME=1009
def need(ok,why):
 if not ok:raise ValueError(why)
def root(n):
 a=[j for j in range(9) if n>>j&1]
 if len(a)==3:return tuple(2 if j in a else -1 for j in range(9))
 need(len(a)==7,'Source root type');p,q=[j for j in range(9) if j not in a];return tuple(3*(int(j==p)-int(j==q)) for j in range(9))
def rank(rows):
 b={}
 for row in rows:
  v=[x%PRIME for x in row]
  for j in range(len(v)):
   if not v[j]:continue
   if j in b:
    q=v[j];v=[(x-q*y)%PRIME for x,y in zip(v,b[j])]
   else:
    q=pow(v[j],-1,PRIME);b[j]=[x*q%PRIME for x in v];break
 return len(b)
def determinant(rows):
 a=[[x%PRIME for x in row] for row in rows];ans=1
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]),None)
  if k is None:return 0
  if k!=j:a[k],a[j]=a[j],a[k];ans=-ans
  v=a[j][j];ans=ans*v%PRIME;inv=pow(v,-1,PRIME)
  for k in range(j+1,len(a)):
   t=a[k][j]*inv%PRIME;a[k]=[(x-t*y)%PRIME for x,y in zip(a[k],a[j])]
 return ans%PRIME
def main(a):
 raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'Native pin');s=json.loads(gzip.decompress(raw));H=[s['live'][i] for i in s['hosted']['Dports']];ns={h:s['frames'][s['initial'][h]][0] for h in H};R={h:root(ns[h]) for h in H};q={h:R[h][:8] for h in H}
 need(all(sum(v)==0 for v in R.values()) and rank(q.values())==8,'Faithful rational coordinates')
 P={h:[q[h][i]*q[h][j] for i in range(8) for j in range(i,8)] for h in H};need(rank(P.values())==36,'Source projector span')
 groups={c:{h for h in H if (ns[h]&c).bit_count()%2==0} for c in range(1,512)};eligible=[];hist=collections.Counter();dot=lambda x,y:sum(u*v for u,v in zip(x,y))
 for c in range(1,512):
  outside=[h for h in H if h not in groups[c]];r=rank([q[h] for h in outside]);hist[r]+=1
  if r==7:
   v=root(c);need(all(dot(v,R[h])==0 for h in outside),'Exact rank7 upper witness');need(all(dot(v,R[h])!=0 for h in groups[c]),'Exact shortening support');eligible.append(c)
  else:need(r==8,'Exact full-rank lower witness')
 need(dict(hist)=={8:487,7:24},'Line census');cert=json.loads(a.certificate.read_text());need(eligible==cert['eligible_lines'],'Certificate exact eligible set');minors=[]
 for row in cert['two_disjoint_bases_every_eligible_line']:
  c=row['binary_line'];seen=set()
  for basis in row['two_disjoint_root_bases']:
   roles=basis['roles'];need(len(roles)==len(set(roles))==8 and set(roles)<=groups[c],'Actual line support basis');need(not seen&set(roles),'Disjoint bases');seen.update(roles);d=determinant([q[h] for h in roles]);need(d!=0,'Independent modular nonzero8-minor');minors.append({'line':c,'roles':roles,'minor_mod1009':d})
 need(len(minors)==48,'Every line has two bases');intersections=[len(groups[c]&groups[d]) for c,d in itertools.combinations(eligible,2)];need((min(intersections),max(intersections))==(15,28),'Independent overlap range')
 capraw=a.cap_certificate.read_bytes();need(hashlib.sha256(capraw).hexdigest()==CAP,'Admitted chart-cap dependency');caps={int(k):v for k,v in json.loads(capraw)['rank_caps'].items()};need(caps=={1:1,2:2,3:4,4:8,5:16,6:24,7:35},'Rank caps')
 bounds={'two_low_ranks_sum9':max(caps[r]+caps[t] for r in range(1,8) for t in range(1,8) if r+t<=9),'shared_center_plus_single_sum10':max(min(caps[r],28)+caps[t] for r in range(5,8) for t in range(1,8) if r+t<=10),'shared_center_plus_other_sum11':max(min(caps[r],28)+caps[t] for r in range(5,8) for t in range(1,8) if r+t<=11),'best_small_pair_in_three_low_ranks_sum17':max(min(caps[x]+caps[y] for x,y in itertools.combinations(rs,2)) for rs in itertools.product(range(1,8),repeat=3) if sum(rs)<=17)}
 need(bounds=={'two_low_ranks_sum9':37,'shared_center_plus_single_sum10':32,'shared_center_plus_other_sum11':40,'best_small_pair_in_three_low_ranks_sum17':40},'Finite integer case bounds')
 M=[0,1,3,6,12,20,36];small={z:max(M[z]+pairs*M[z+2]+(9-z-2*pairs)*M[z+1] for pairs in range((9-z)//2+1)) for z in range(4)};need(small=={0:13,1:25,2:45,3:78},'Mixed small-z coverage')
 mutant=[q[h] for h in minors[0]['roles']];mutant[0]=mutant[1];need(determinant(mutant)==0,'Repeated basis-row mutant')
 out={'status':'PASS_INDEPENDENT_COMPARABLE_NINE_SOURCE_REVIEW','native_sha256':PIN,'source_coordinate_model':'Integer Q9 sum-zero roots, drop final coordinate; prime1009 nonzero minors certify Q lower ranks.','projector_rank':36,'line_rank_histogram':dict(hist),'eligible_lines':eligible,'disjoint_basis_minors':minors,'intersection_range':[min(intersections),max(intersections)],'integer_support_bounds':bounds,'small_z_coverage_bounds':small,'negative_control_repeated_basis_row':True,'inherited_caps_sha256':CAP,'scope':'Finite source premises and separately reviewed all-volume star/quotient argument; new incomparable theorem needs its two36-basis certificate.'}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','projector_rank','line_rank_histogram','intersection_range','integer_support_bounds','small_z_coverage_bounds']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--cap-certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
