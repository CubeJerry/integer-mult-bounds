"""Exact small-half code minima and priced facet-arrival consequences."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
from itertools import combinations
import argparse,hashlib,json

NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PINS={'restored':'fbbae97bf0c71ca5d1f74bbe272e5507690f09d991600fe42f1636f0386c7433','low':'c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'}
def need(ok,why):
 if not ok:raise ValueError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return list(b.values())
def root(n):
 scale=10**36;target=n**199*scale**200;lo=0;hi=n*scale+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 return F(lo,scale),F(hi,scale)
def moment(profile):
 lo=hi=F(0)
 for n,c in profile.items():
  l,h=root(int(n));lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 return lo,hi
def record(x):return {'rational':list(map(str,x)),'decimal_approximation':list(map(float,x))}
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--restored-review',type=Path,required=True);p.add_argument('--low-review',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';need(sha(native)==NATIVE,'native pin')
 R=json.loads(native.read_text())['native_roots'];N=[sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)];K=[(1<<i)^N[i]for i in range(111)];C=basis(K);need(len(C)==9,'full canonical rank')
 words=[0]
 for c in C:words += [w^c for w in words]
 distance=[]
 for i in range(111):
  forbidden=((1<<111)-1)^(N[i]|(1<<i));projected=[w&forbidden for w in words]
  need(sum(w==0 for w in projected)==2,'canonical fitting kernel dimension one')
  d=min(w.bit_count()for w in projected if w);need(d>=18,'uniform puncture resistance');distance.append(d)
 groups=defaultdict(list)
 for i,r in enumerate(R):
  support=tuple(j for j,v in enumerate(r)if v)
  if len(support)==4:groups[support].append(i)
 halves=[];union=0
 for support,roles in sorted(groups.items()):
  x,y=support[:2]
  for sign in [1,-1]:
   ids=[i for i in roles if R[i][x]==sign*R[i][y]];h=sum(1<<i for i in ids)
   need(not(h&union),'disjoint half partition');union|=h
   need(len(ids)in[3,4],'actual half sizes')
   need(all((h^(1<<i))&~N[i] for i in ids),'own-containing half has a foreign forbidden coordinate')
   halves.append({'support':support,'sign':sign,'roles':ids,'mask':h,'beneficiaries':[i for i in range(111)if not(h&~N[i])]})
 need(len(halves)==28 and union==sum(1<<i for i in range(8,111)),'complete noncoordinate half partition')
 degree=[x.bit_count()for x in N];gain=[[len(h['roles'])if i in h['beneficiaries']else 0 for i in range(111)]for h in halves]
 def witness(selected):
  rows=K[:]
  for j in selected:
   for i in halves[j]['beneficiaries']:rows[i]^=halves[j]['mask']
  need(all((rows[i]>>i)&1 and not(rows[i]&~(N[i]|(1<<i)))for i in range(111)),'actual fitting witness')
  weights=[(rows[i]&N[i]).bit_count()for i in range(111)]
  return {'selected_halves':selected,'union_support':sum(len(halves[j]['roles'])for j in selected),'charge':sum((w>36)+(w>52)for w in weights),'code_rank':len(basis(K+[halves[j]['mask']for j in selected])),'witness_matrix_rank':len(basis(rows)),'rows_hex':list(map(hex,rows)),'foreign_support_histogram':dict(Counter(weights))}
 summaries=[]
 for k in range(5):
  best=223;chosen=None;hist=Counter()
  for selected in combinations(range(28),k):
   weights=[degree[i]-sum(gain[j][i]for j in selected)for i in range(111)]
   chi=sum((w>36)+(w>52)for w in weights);hist[chi]+=1
   if chi<best:best=chi;chosen=selected
  need(best==[222,219,207,197,189][k],'exact small-half minimum')
  example=witness(chosen);need(example['charge']==best,'minimum witness')
  summaries.append({'selected_count':k,'minimum_charge':best,'number_of_subsets':sum(hist.values()),'charge_histogram':dict(sorted(hist.items())),'witness':example})
 five=witness((8,9,14,15,21));need(five['union_support']<=17 and five['charge']==187,'five-half arithmetic escape witness')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 allowance=tuple(v/6 for v in moment(gate));prices=[]
 for label,path,hist_expected in [('restored',a.restored_review,{1:71,4:40}),('low',a.low_review,{1:71,2:16,3:16,4:8})]:
  receipt=json.loads(path.read_text());need(receipt['native_sha256']==NATIVE and receipt['word_sha256']==PINS[label],'independently audited cut pin')
  hist={int(k):v for k,v in receipt['original_X_rank_histogram'].items()};need(hist==hist_expected,'actual X cut ranks')
  profile={int(k):v for k,v in receipt['stats']['movement_profile'].items()};Q0=moment(profile);delta_profile={}
  for r,count in hist.items():
   for d,c in[(7-r,count),(1,count),(8-r,-count)]:delta_profile[d]=delta_profile.get(d,0)+c
  for r in range(1,7):
   d=moment({7-r:1,1:1,8-r:-1})if r!=6 else moment({1:2,2:-1})
   need(0<d[0]<=d[1]<1,'strict facet fragmentation price below one')
  delta=moment(delta_profile);room=(allowance[0]-Q0[1],allowance[1]-Q0[0]);bound=(111+room[0]-delta[1],111+room[1]-delta[0]);floors=[x.numerator//x.denominator for x in bound];need(floors==[187,187],'priced occurrence cap')
  lower_profile=profile.copy()
  for d,c in delta_profile.items():lower_profile[d]=lower_profile.get(d,0)+c
  lower_profile[1]=lower_profile.get(1,0)+78
  lower_profile={d:c for d,c in sorted(lower_profile.items())if c}
  need(all(c>0 and 1<=d<=7 for d,c in lower_profile.items()),'nonnegative necessary profile in ranks1..7')
  lower=moment(lower_profile);excess=(lower[0]-allowance[1],lower[1]-allowance[0]);need(excess[0]>0,'strict target excess')
  five_room=(2-excess[1],2-excess[0]);need(five_room[0]>0,'five-half witness survives this necessary price test only')
  prices.append({'variant':label,'word_sha256':PINS[label],'independent_review_sha256':sha(path),'rank_histogram':hist,'source_movement':record(Q0),'source_room':record(room),'sum_facet_prices':record(delta),'chi_strict_upper_interval':record(bound),'integer_chi_cap':187,'charge189_mandatory_profile':lower_profile,'charge189_excess':record(excess),'charge187_optimistic_room':record(five_room)})
 proof=a.repo/'research/moonshot-005-program/results/bit-all-route-rank-gap/author/PROOF.md'
 out={'status':'PASS_EXACT_SMALL_HALF_MINIMA_AND_PRICED_CUT_GATE','native_sha256':NATIVE,'arrival_proof_sha256':sha(proof),'distance_histogram':dict(Counter(distance)),'halves':[{k:v for k,v in h.items()if k!='mask'}for h in halves],'subset_results':summaries,'five_half_witness':five,'priced_cuts':prices,'controls':{'raw_identity_charge':sum(((1<<i)&N[i]).bit_count()>36 for i in range(111)),'four_half_claim188_rejected':summaries[4]['minimum_charge']>188,'five_half_outside_class_witness':len(five['selected_halves'])==5 and five['charge']==187,'unpriced_caps':[188,189]},'scope':'For every characteristic-two field/positive width, C plus at most4 selected literal members of the fixed28 disjoint half sums has minimum charge>=189. Both actual correction cuts with monotone public routes and arbitrary nested owned routes allow chi<=187 after facet prices. General coded combinations of28, changed cuts and nonmonotone public routes are outside. Five-half witness is algebraic only; its matrix rank is a witness rank, not a minrank theorem.','new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
 print(out['status']);print('Small-half minima',[r['minimum_charge']for r in summaries]);print('Priced caps',[r['integer_chi_cap']for r in prices]);print('Excesses',[r['charge189_excess']['decimal_approximation'][0]for r in prices])
if __name__=='__main__':main()
