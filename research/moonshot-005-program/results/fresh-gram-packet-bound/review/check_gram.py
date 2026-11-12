#!/usr/bin/env python3
"""Independent E8-moment, source-locality, integer-capacity and price review.
No author verifier or helper is imported.
"""
import argparse,gzip,hashlib,itertools,json,math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
F1=[7,25,42,52,76,82,97,127]
F2=[67,104,137,162,266,289,448,491]
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def root9(v):
 S=[i for i in range(9) if v>>i&1]
 if len(S)==3:return tuple(2 if i in S else -1 for i in range(9))
 need(len(S)==7,'root weight');i,j=[k for k in range(9) if k not in S]
 return tuple(3*(int(k==i)-int(k==j)) for k in range(9))
def root8(v):
 r=root9(v);need(all((2*r[k]+r[8])%3==0 for k in range(8)),'integral isometry image')
 return tuple((2*r[k]+r[8])//3 for k in range(8))
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def rank(A):
 rows=[list(map(F,r)) for r in A];p=0
 if not rows:return 0
 for j in range(len(rows[0])):
  k=next((k for k in range(p,len(rows)) if rows[k][j]),None)
  if k is None:continue
  rows[p],rows[k]=rows[k],rows[p];c=rows[p][j];rows[p]=[v/c for v in rows[p]]
  for k in range(p+1,len(rows)):
   if rows[k][j]:c=rows[k][j];rows[k]=[a-c*b for a,b in zip(rows[k],rows[p])]
  p+=1
  if p==len(rows):break
 return p
def multiply(P,Q):
 out={}
 for e,c in P.items():
  for f,d in Q.items():
   key=tuple(x+y for x,y in zip(e,f));out[key]=out.get(key,0)+c*d
 return {e:c for e,c in out.items() if c}
def moments(roots):
 zero=(0,)*8;actual={2:{},4:{},6:{}}
 for a in roots:
  L={tuple(int(k==i) for k in range(8)):c for i,c in enumerate(a) if c};P={zero:1}
  for degree in range(1,7):
   P=multiply(P,L)
   if degree in actual:
    for e,c in P.items():actual[degree][e]=actual[degree].get(e,0)+c
 Q={tuple(2*int(k==i) for k in range(8)):1 for i in range(8)};P={zero:1};checks={}
 for k,constant in enumerate((120,288,960),1):
  P=multiply(P,Q);expected={e:constant*c for e,c in P.items()};observed={e:c for e,c in actual[2*k].items() if c}
  need(observed==expected,'independent complete moment polynomial '+str(2*k));checks[2*k]={'nonzero_monomials':len(expected),'all_homogeneous_monomials':math.comb(2*k+7,7)}
 return checks
def span(vs):
 S={0}
 for v in vs:S|={x^v for x in tuple(S)}
 return S
def cap(r):return min(1<<(r-1),96)
def integer_search():
 hist=Counter();largest=0;witness=None
 def walk(parts,left,least):
  nonlocal largest,witness
  m=len(parts)
  if m>=8:
   cover=sum(cap(r) for r in parts);dist=sum(cap(r) for r in parts[:m-7]);hist['all']+=1;hist['cover']+=int(cover>=96);hist['distance']+=int(dist>=37);hist['both']+=int(cover>=96 and dist>=37)
   if dist>=37 and cover>largest:largest=cover;witness=parts
  for r in range(least,min(left,9)+1):walk(parts+(r,),left-r,r)
 walk((),47,1);need(hist['both']==0,'all partitions of rank budget47 excluded');return dict(hist),largest,witness
def power(r,precision=110):
 den=1<<precision;target=r**199*den**200;lo=0;hi=r*den+1
 while hi-lo>1:
  k=(lo+hi)//2
  if k**200<=target:lo=k
  else:hi=k
 need(lo**200<=target<(lo+1)**200,'exact dyadic root');return F(lo,den),F(lo if lo**200==target else lo+1,den)
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes();need(sha(sb)==SPIN and sha(ib)==IPIN,'exact source/invoice')
 s=json.loads(gzip.decompress(sb));invoice=json.loads(ib);H=[s['live'][k] for k in s['hosted']['Dports']];normal={h:s['frames'][s['initial'][h]][0] for h in H};allv=[v for v in range(512) if v.bit_count() in(3,7)];omitted=set(allv)-set(normal.values());need(len(H)==96 and len(set(normal.values()))==96 and len(omitted)==24,'hosted subset cardinalities')
 roots={v:root8(v) for v in allv};double={r for a in roots.values() for r in(a,tuple(-x for x in a))};standard=set()
 for i,j in itertools.combinations(range(8),2):
  for si,sj in itertools.product((-2,2),repeat=2):standard.add(tuple(si*int(k==i)+sj*int(k==j) for k in range(8)))
 standard|={r for r in itertools.product((-1,1),repeat=8) if math.prod(r)==-1}
 need(len(double)==len(standard)==240 and double==standard,'exact doubled E8 sign-system identity')
 checks=moments(list(roots.values()))
 for frame in(F1,F2):need(len(set(frame))==8 and set(frame)<=omitted and all(dot(root9(v),root9(w))==18*(i==j) for i,v in enumerate(frame) for j,w in enumerate(frame)),'independent omitted Q9 orthogonal frame')
 need(not(set(F1)&set(F2)),'two omitted frames disjoint')
 # Exact one-variable polynomial products, avoiding sampled inequalities.
 poly=lambda x:[F(v) for v in x]
 def pmul(A,B):
  C=[F(0)]*(len(A)+len(B)-1)
  for i,x in enumerate(A):
   for j,y in enumerate(B):C[i+j]+=x*y
  return C
 need(pmul(poly([8,-1]),pmul(poly([-2,1]),poly([-2,1])))==poly([32,-36,12,-1]),'1-p positive factor')
 need(pmul(poly([10,-1]),pmul(poly([-1,1]),poly([-1,1])))==poly([10,-21,12,-1]),'frame tangent positive factor')
 need(F(9,8)*120-F(3,8)*288+F(1,32)*960==57,'full p-sum')
 lower=F(57)-2*F(25,4)-8;need(lower==F(73,2) and math.ceil(lower)==37,'37-source support floor')
 vlist=list(normal.values());need(rank([root9(v) for v in vlist])==8,'hosted root rank8')
 local=[];ranks=Counter()
 for z in range(1,512):
  excluded=[v for v in vlist if (v&z).bit_count()%2];r=rank([root9(v) for v in excluded]);ranks[r]+=1
  if z in omitted:need(r==7 and all(dot(root9(z),root9(v))==0 for v in excluded),'exceptional line annihilator')
  else:need(r==8,'all other line cuts full rank')
  local.append({'direction':z,'excluded_count':len(excluded),'rank':r})
 need(dict(ranks)=={8:487,7:24},'complete511-line census');need(all(abs(dot(root9(v),root9(w)))<18 for v,w in itertools.combinations(sorted(omitted),2)),'distinct exceptional annihilator lines')
 for h,y in zip(H,s['hosted']['Y2']):need(span(s['frames'][s['final'][y]])=={z for z in range(512) if (z&normal[h]).bit_count()%2==0} and s['frames'][s['initial'][y]]==[],'actual rawY2 input/endpoints')
 census,largest,witness=integer_search();need(census=={'all':244755,'cover':197339,'distance':14,'both':0} and largest==51,'independent integer relaxation census')
 need(sum(cap(4) for _ in range(12))>=96 and 5*cap(4)>=37,'rank48 numerical relaxation witness')
 weak=(1,)+(5,)*9;need(sum(weak)==46 and sum(map(cap,weak))>=96 and sum(map(cap,weak[:3]))==33,'support33 negative control');need(44>=37 and 44<96,'coverage-premise negative control')
 wrong=[normal[H[0]]]+F1[1:];need(not set(wrong)<=omitted,'actual included-root mutation rejected')
 roles=set(s['live'])|{x+112 for x in s['live']}|set(s['hosted']['X2'])|set(s['hosted']['Y2']);need(len(roles)==400,'raw400')
 for r in roles:need(len(s['frames'][s['final'][r]])-len(s['frames'][s['initial'][r]])==8 and span(s['frames'][s['initial'][r]])<=span(s['frames'][s['final'][r]]),'legitimate favorable direct ascent')
 old=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in roles);need(dict(old)=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'source raw tariff')
 T={int(r):n for r,n in invoice['T4'].items()};P={int(r):n for r,n in invoice['P4'].items()}
 for r,n in old.items():P[r]-=18*n
 P[8]=P.get(8,0)+18*400;P[9]=P.get(9,0)+18*8;need(min(P.values())>=0,'complete favorable invoice nonnegative')
 lo=hi=F(0)
 for r in T.keys()|P.keys():
  c=T.get(r,0)-P.get(r,0);l,h=power(r);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 lo/=18;hi/=18;l9,h9=power(9);costlo=F(16,3)*l9;costhi=F(16,3)*h9;need(costlo>hi,'strict fresh-packet budget obstruction')
 result={'status':'PASS_INDEPENDENT_FRESH_GRAM_PACKET_OBSTRUCTION','source_sha256':SPIN,'invoice_sha256':IPIN,'moment_polynomials':checks,'doubled_root_system_size':240,'hosted_rank':8,'omitted_normals':sorted(omitted),'omitted_frames':[F1,F2],'support_lower_p_sum':str(lower),'support_floor':37,'locality_rank_counts':dict(ranks),'integer_partition_census':census,'largest_coverage_with_distance37':largest,'max_coverage_partition':witness,'rank_floor':48,'headroom_lower':str(lo),'headroom_upper':str(hi),'packet_price_lower':str(costlo),'packet_price_upper':str(costhi),'strict_deficit_lower':str(costlo-hi),'all_volume_proof_review':'Passed separately in REVIEW.md; finite tests corroborate source/polynomial/integer claims.','scope':'Fresh local packets from unchanged hosted raw values and no Y-dependent hub side information or funded informative moves; no new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'GRAM-REVIEW.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.output/'LINE-REVIEW.json').write_text(json.dumps(local,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','support_floor','rank_floor','integer_partition_census','strict_deficit_lower']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
