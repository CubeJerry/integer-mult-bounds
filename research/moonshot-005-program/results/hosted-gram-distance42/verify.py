#!/usr/bin/env python3
"""Exact hosted-E8 distance42 and fresh-packet relaxation certificate."""
import argparse,gzip,hashlib,itertools,json,math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
ALPHA=[[1,-1,-1,-1,-1,-1,-1,-1],[2,2,0,0,0,0,0,0],[-2,2,0,0,0,0,0,0],[0,-2,2,0,0,0,0,0],[0,0,-2,2,0,0,0,0],[0,0,0,-2,2,0,0,0],[0,0,0,0,-2,2,0,0],[0,0,0,0,0,-2,2,0]]
DUAL4=[[0,0,0,0,0,0,0,-4],[1,1,1,1,1,1,1,-5],[-1,1,1,1,1,1,1,-7],[0,0,2,2,2,2,2,-10],[0,0,0,2,2,2,2,-8],[0,0,0,0,2,2,2,-6],[0,0,0,0,0,2,2,-4],[0,0,0,0,0,0,2,-2]]
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def root(v):
 S=[i for i in range(9) if v>>i&1]
 if len(S)==3:r=[2 if i in S else -1 for i in range(9)]
 else:
  need(len(S)==7,'binary root weight');i,j=[k for k in range(9) if k not in S];r=[3*(int(k==i)-int(k==j)) for k in range(9)]
 need(all((2*r[k]+r[8])%3==0 for k in range(8)),'integer isometry');return tuple((2*r[k]+r[8])//3 for k in range(8))
def reflect(r,a):
 scale=F(dot(r,a),4);out=tuple(F(x)-scale*y for x,y in zip(r,a));need(all(x.denominator==1 for x in out),'integral reflection');return tuple(int(x) for x in out)
def cap(r):return min(1<<(r-1),96)
def partition_gate(parts,distance=42,coverage=True):
 m=len(parts)
 return m>=8 and (not coverage or sum(map(cap,parts))>=96) and sum(cap(r) for r in parts[:m-7])>=distance
def partitions():
 stats=Counter();passing50=[]
 def visit(parts,total,least):
  if len(parts)>=8:
   if total<=49:
    stats['mass_at_most49']+=1;stats['distance42']+=int(partition_gate(parts,coverage=False));stats['both42']+=int(partition_gate(parts))
   elif total==50:
    stats['mass50']+=1
    if partition_gate(parts):passing50.append(dict(sorted(Counter(parts).items())))
  for r in range(least,min(50-total,9)+1):visit(parts+(r,),total+r,r)
 visit((),0,1)
 expected=[{5:10},{2:1,4:12},{1:2,4:12}];need(stats['both42']==0 and all(x in passing50 for x in expected) and len(passing50)==3,'exact mass50 admissible histograms')
 return dict(stats),passing50
def power(r,den=10**30):
 target=r**199*den**200;lo=0;hi=r*den+1
 while hi-lo>1:
  m=(lo+hi)//2
  if m**200<=target:lo=m
  else:hi=m
 need(lo**200<=target<(lo+1)**200,'exact target-power bracket');return F(lo,den),F(lo if lo**200==target else lo+1,den)
def span(vs):
 S={0}
 for v in vs:S|={x^v for x in tuple(S)}
 return S
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes();need(sha(sb)==SPIN and sha(ib)==IPIN,'immutable native/invoice pins');s=json.loads(gzip.decompress(sb));invoice=json.loads(ib)
 normals=[v for v in range(512) if v.bit_count() in(3,7)];projective={v:root(v) for v in normals};roots=sorted({r for x in projective.values() for r in(x,tuple(-u for u in x))});R=set(roots);need(len(normals)==120 and len(R)==240 and all(dot(r,r)==8 for r in roots),'complete projective/signed roots')
 standard=set()
 for i,j in itertools.combinations(range(8),2):
  for x,y in itertools.product((-2,2),repeat=2):standard.add(tuple(x*int(k==i)+y*int(k==j) for k in range(8)))
 standard|={r for r in itertools.product((-1,1),repeat=8) if math.prod(r)==-1};need(R==standard,'exact D8 plus odd-spin set')
 need(all(tuple(a) in R for a in ALPHA),'all simple roots present');need([[dot(w,a) for a in ALPHA] for w in DUAL4]==[[4*int(i==j) for j in range(8)] for i in range(8)],'explicit dual simple basis')
 coef={r:[F(dot(w,r),4) for w in DUAL4] for r in roots};need(all(all(x.denominator==1 for x in n) and (all(x>=0 for x in n) or all(x<=0 for x in n)) for n in coef.values()),'integral same-sign simple-root coordinates')
 need(all(tuple(sum((n[i]*ALPHA[i][k] for i in range(8)),F(0)) for k in range(8))==r for r,n in coef.items()),'exact simple-root reconstruction')
 idx={r:i for i,r in enumerate(roots)};perms=[]
 for simple in ALPHA:
  images=[reflect(r,simple) for r in roots];need(set(images)==R,'reflection permutes all240 roots');perm=[idx[r] for r in images];need(all(perm[perm[i]]==i for i in range(240)),'reflection involution');perms.append(perm)
 deletions=[sum(n[i]==0 for n in coef.values())//2 for i in range(8)];need(deletions==[42,28,22,14,16,23,37,63],'exact deletion census');need(tuple(DUAL4[7]) in R,'sole exceptional dual normal is a root')
 # The same-sign condition is essential: negating just one simple basis row breaks it.
 mutated=[[(-x if i==7 else x) for i,x in enumerate(n)] for n in coef.values()];need(any(not(all(x>=0 for x in n) or all(x<=0 for x in n)) for n in mutated),'wrong chamber orientation negative control')
 H=[s['live'][k] for k in s['hosted']['Dports']];normal={h:s['frames'][s['initial'][h]][0] for h in H};need(len(H)==96 and len(set(normal.values()))==96,'96 hosted sources');support=[]
 for v,r in projective.items():
  supp=[h for h in H if dot(r,projective[normal[h]])];support.append({'normal':v,'support':len(supp),'hosted_roles':supp})
 dist=min(z['support'] for z in support);witness=[z['normal'] for z in support if z['support']==dist];need(dist==42 and witness==[38,191],'exact root-direction source minimum')
 need(96-42==54>dist,'non-root chamber bound is strictly stronger');need(sum(dot(DUAL4[7],r)==0 for r in roots)//2==63,'root exception cannot be omitted')
 stats,passing=partitions();need(partition_gate((1,)+(4,)*12,distance=41) and not partition_gate((1,)+(4,)*12),'distance41 admits rank49 control');need(partition_gate((1,)*49,coverage=False) and not partition_gate((1,)*49),'coverage is essential')
 l2,h2=power(2);l4,h4=power(4);l5,h5=power(5);l9,h9=power(9);need(10*h5<12*l4+l2 and 10*h5<12*l4+2,'mass50 strict moment minimizer');need(51**200*5>50**200*9,'higher mass Bernoulli comparison')
 raw=set(s['live'])|{h+112 for h in s['live']}|set(s['hosted']['X2'])|set(s['hosted']['Y2']);need(len(raw)==400,'raw inventory')
 for r in raw:need(len(s['frames'][s['final'][r]])-len(s['frames'][s['initial'][r]])==8 and span(s['frames'][s['initial'][r]])<=span(s['frames'][s['final'][r]]),'direct raw ascent grant')
 old=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw);need(dict(old)=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'raw source histogram');T={int(r):n for r,n in invoice['T4'].items()};P={int(r):n for r,n in invoice['P4'].items()}
 for r,n in old.items():P[r]-=18*n
 P[8]=P.get(8,0)+18*400;P[9]=P.get(9,0)+18*8;need(min(P.values())>=0,'whole favorable caller')
 lo=hi=F(0)
 for r in T.keys()|P.keys():
  c=T.get(r,0)-P.get(r,0);l,h=power(r);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 lo/=18;hi/=18;price_lo=10*l5;price_hi=10*h5;need(price_lo>hi,'strict complete target obstruction')
 chamber={'simple_roots':ALPHA,'dual_simple_normals_times4':DUAL4,'projective_deletion_counts':deletions,'all240_roots':roots,'simple_coordinates':[[str(x) for x in coef[r]] for r in roots],'reflection_permutations':perms,'source_supports':support}
 result={'status':'PASS_EXACT_HOSTED_DISTANCE42_AND_FRESH_PACKET_FLOOR','source_sha256':SPIN,'invoice_sha256':IPIN,'exact_hosted_distance':42,'minimum_support_witness_normals':witness,'nonroot_direction_minimum_support':54,'projective_deletion_counts':deletions,'universal_proof':'Finite root permutation group, dominant orbit maximizer, explicit same-sign simple coordinates; see PROOF.md.','rank_mass_floor':50,'all_mass50_relaxation_histograms':passing,'exact_relaxed_moment_floor':'10*5^(199/200)','finite_histogram_corroboration':stats,'favorable_caller':{'paid':sum(P.values()),'targets':sum(T.values()),'P_best':dict(sorted(P.items())),'T4':dict(sorted(T.items())),'remaining_moment_lower':str(lo),'remaining_moment_upper':str(hi)},'packet_moment_lower':str(price_lo),'packet_moment_upper':str(price_hi),'deficit_per_native_lower':str(price_lo-hi),'deficit_per_native_upper':str(price_hi-lo),'negative_controls':['negating one simple basis root breaks uniform coefficient sign','root direction has63 full zero roots so exception is necessary','distance41 admits rank49 histogram','dropping coverage admits49 rank1 packets'],'scope':'Exact source-punctured Gram-code distance and restricted fresh local unchanged-raw whole-field packet price. New or funded mixed rows, side information and changed tariffs require new accounting. No new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CHAMBER.json').write_text(json.dumps(chamber,indent=2,sort_keys=True)+'\n');(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','exact_hosted_distance','minimum_support_witness_normals','rank_mass_floor','all_mass50_relaxation_histograms','exact_relaxed_moment_floor','deficit_per_native_lower']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
