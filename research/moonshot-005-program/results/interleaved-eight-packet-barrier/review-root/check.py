#!/usr/bin/env python3
"""Independent exact source/accounting review: no author-code imports."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
SPECTRUM={0:1,20:3,22:48,24:28,26:96,28:28,30:48,32:3,52:1}
def need(ok,msg):
 if not ok:raise AssertionError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parity(a,b):return (a&b).bit_count()&1
def space(g):
 s={0}
 for x in g:s.update(y^x for y in tuple(s))
 return frozenset(s)
def root(z):
 bits=[bool(z&(1<<i)) for i in range(9)]
 if sum(bits)==3:return tuple(2*int(bits[i]) if bits[8] else 2*int(bits[i])-1 for i in range(8))
 need(sum(bits)==7,'root source domain');m=[i for i in range(9) if not bits[i]]
 if m[1]==8:return tuple(1 if i==m[0] else -1 for i in range(8))
 return tuple(2*((i==m[0])-(i==m[1])) for i in range(8))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 piv={}
 for r in rows:
  v=list(map(F,r))
  for k,u in sorted(piv.items()):
   q=v[k]
   if q:v=[x-q*y for x,y in zip(v,u)]
  if any(v):
   k=next(i for i,x in enumerate(v) if x);q=v[k];piv[k]=[x/q for x in v]
 return len(piv)
def power(r):
 if not r:return F(0),F(0)
 den=10**80;value=r**199*den**200;lower,upper=0,r*den+1
 while lower+1<upper:
  mid=(lower+upper)//2
  if mid**200<=value:lower=mid
  else:upper=mid
 need(lower**200<=value<upper**200,'directed integer power')
 return F(lower,den),F(upper,den)
def interval(hist):
 lo=hi=F(0)
 for r,c in hist.items():
  a,b=POWER[r];lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--minimal',type=Path,required=True);ap.add_argument('--interleaved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
source=args.repo/'research/shared-wire-split-composition/data/final.json.gz';invoice=args.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json'
need(digest(source)==SPIN and digest(invoice)==IPIN,'source/invoice pins')
s=json.loads(gzip.decompress(source.read_bytes()));iv=json.loads(invoice.read_text());roles=s['live'];normals={i:s['frames'][s['initial'][i]][0] for i in roles};roots={i:root(z) for i,z in normals.items()}
need(len(roles)==104 and len(set(normals.values()))==104,'inventory');need(all(z.bit_count()%2 for z in normals.values()),'odd source normals');need(rank(roots.values())==8 and all(dot(a,a)==8 for a in roots.values()),'real source rank/norm')
facets={i:space(s['frames'][s['final'][i+112]]) for i in roles}
for i in roles:
 need(space(s['frames'][s['initial'][i+112]])=={0},'empty receiver start');need(facets[i]=={z for z in range(512) if not parity(z,normals[i])},'actual endpoint facet')
need(len(set(facets.values()))==104,'distinct facets')
missing=sorted(z for z in range(1,512) if z.bit_count() in(3,7) and z not in normals.values());need(len(missing)==16,'omitted roots')
locality={z:rank(roots[i] for i in roles if parity(normals[i],z)) for z in range(1,512)}
need(Counter(locality.values())=={8:495,7:16},'511 rational ranks');need(sorted(z for z,r in locality.items() if r==7)==missing,'rank7 exactly omitted')
for z in missing:need(all(not dot(root(z),roots[i]) for i in roles if parity(normals[i],z)),'root annihilator')
support={};codes={};patterns=Counter();triples=Counter();pair_sizes=Counter();witnesses=[]
for z in missing:
 support[z]=[i for i in roles if dot(root(z),roots[i])];need(len(support[z])==52,'support52');need(set(support[z])=={i for i in roles if not parity(z,normals[i])},'real/binary incidence');need(frozenset.intersection(*(facets[i] for i in support[z]))=={0,z},'intersection exactly root')
 codes[z]={v:sum(parity(v,normals[i])<<j for j,i in enumerate(support[z])) for v in range(512)};words=set(codes[z].values());p=(1<<52)-1
 need(len(words)==256 and Counter(w.bit_count() for w in words)==SPECTRUM,'full code spectrum');need(codes[z][511]==p and [v for v,w in codes[z].items() if not w]==[0,z],'kernel/parity')
 disjoint=[(u,v) for u in words if u for v in words if v and not(u&v)];need(len(disjoint)==254 and all(u^v==p for u,v in disjoint),'only complement disjoint pairs')
 for a,b in itertools.combinations([v for v in missing if v!=z],2):
  counts=Counter((parity(a,normals[i]),parity(b,normals[i])) for i in support[z]);need(len(counts)==4 and min(counts.values())>=7,'prior-pair patterns');patterns[tuple(counts[k] for k in((0,0),(0,1),(1,0),(1,1)))]+=1;need(511 not in space([z,a,b]),'triple excludes parity')
for triple in itertools.combinations(missing,3):
 common=[i for i in roles if all(not parity(z,normals[i]) for z in triple)];need(len(common)>=7,'triple common receiver');triples[len(common)]+=1
for quad in itertools.combinations(missing,4):
 for pair in itertools.combinations(quad,2):
  actual=[i for i in roles if set(z for z in quad if not parity(z,normals[i]))==set(pair)];need(len(actual)>=2,'exact pair classes');pair_sizes[len(actual)]+=1;witnesses.append([list(quad),list(pair),actual[0]])
need(sum(pair_sizes.values())==10920,'full quadruple/pair domain')
z,a=missing[:2];u=codes[z][a];p=(1<<52)-1;need(len(space([z,511,a]))==8 and u and(p^u) and not(u&(p^u)),'parity fork exception')
# Explicit abstract retained-copy schedule invalidates unqualified temporal-order assumptions.
ABC=(97,42,82);U=space(ABC);pairplane={ABC[j]:space([ABC[j],ABC[(j+1)%3]]) for j in range(3)};route_counts=Counter();deliveries=0
for i in roles:
 wanted=[z for z in ABC if not parity(z,normals[i])];route=[frozenset({0})]
 if len(wanted)==3:route.append(U);deliveries+=3
 elif len(wanted)==2:
  late=next(z for z in wanted if pairplane[z]==space(wanted));early=next(z for z in wanted if z!=late);route.extend([space([early]),space(wanted)]);deliveries+=2
 elif len(wanted)==1:route.append(space(wanted));deliveries+=1
 route.append(facets[i]);need(all(a<=b for a,b in zip(route,route[1:])),'nested three-chain receivers');route_counts[len(wanted)]+=1
need(route_counts=={0:8,1:44,2:44,3:8} and deliveries==156,'three cheap full deliveries')
raw=set(roles)|{i+112 for i in roles}|set(s['hosted']['X2'])|set(s['hosted']['Y2']);need(len(raw)==400,'raw400')
for i in raw:
 initial=space(s['frames'][s['initial'][i]]);final=space(s['frames'][s['final'][i]]);need(initial<=final and len(final)==256*len(initial),'raw rank8 endpoints')
old=Counter(abs(len(s['frames'][e[2]])-len(s['frames'][e[3]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw);T=Counter({int(r):c for r,c in iv['T4'].items()});P=Counter({int(r):c for r,c in iv['P4'].items()});POWER={r:power(r) for r in set(T)|set(P)|set(range(10))};base=Counter(T)
for r,c in P.items():base[r]-=c
for r,c in old.items():base[r]+=18*c
base[8]-=18*400;ordered=base.copy()
for r,c in {9:6,8:1,7:1,1:1}.items():ordered[r]-=18*c
interleaved=base.copy()
for r,c in {9:5,8:3,1:51,7:51}.items():interleaved[r]-=18*c
interleaved[8]+=18*51;flo,fhi=interval({5:10});records={}
for name,hist in [('globally_ordered',ordered),('arbitrarily_interleaved',interleaved)]:
 lo,hi=interval(hist);lo/=18;hi/=18;need(flo>hi,'strict fresh-return deficit');records[name]={'headroom_lower':str(lo),'headroom_upper':str(hi),'deficit_lower':str(flo-hi),'deficit_upper':str(fhi-lo),'headroom_decimal':float(hi),'deficit_decimal':float(flo-hi)}
no_cheap=interval({9:3,8:48,7:-51,1:-51});need(no_cheap[0]>0,'zero cheap case');f=interval({1:1,7:1,8:-1});need(f[0]>0,'proper raw split fee');need(POWER[9][0]>POWER[7][1]+1 and POWER[9][0]>POWER[8][1],'ordered comparisons');need(POWER[9][0]>POWER[6][1]+2,'retained chains cheap')
args.output.mkdir(parents=True,exist_ok=True)
result={'status':'PASS_INDEPENDENT_SOURCE_AND_ACCOUNTING_REVIEW','source_sha256':SPIN,'invoice_sha256':IPIN,'proof_pins':{name:digest(folder/'PROOF.md') for name,folder in [('minimal_eight',args.minimal),('interleaved_eight',args.interleaved)]},'exact_rational_locality_domain':511,'rank_counts':dict(Counter(locality.values())),'spectra_roots':16,'preceding_pair_cases':sum(patterns.values()),'triple_common_counts':dict(triples),'quadruple_pair_counts':dict(pair_sizes),'quadruple_pair_cases':len(witnesses),'retained_three_pattern_counts':dict(route_counts),'retained_three_deliveries':deliveries,'original_raw_histogram':dict(old),'raw_split_fee_lower':str(f[0]),'zero_cheap_comparison_lower':str(no_cheap[0]),'whole_caller':records,'negative_controls':['Rank2 all-ones subcode is disconnected.','Three cheap retained-copy packets defeat an unqualified global-order bound.','Zero cheap case checked separately.'],'scope':'Independent exact finite source and inequality review. Universal proof review separately recorded in REVIEW.md. No new kappa.'}
(args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(args.output/'PAIR-WITNESSES.json').write_text(json.dumps(witnesses,separators=(',',':'))+'\n');print(result['status']);print(json.dumps(records,indent=2))
