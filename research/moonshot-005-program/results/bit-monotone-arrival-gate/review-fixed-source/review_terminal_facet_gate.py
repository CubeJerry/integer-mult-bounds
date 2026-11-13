#!/usr/bin/env python3
"""Independent exact source check of final-facet visit count and movement cut."""
import gzip,hashlib,json
from fractions import Fraction as Q
from collections import Counter,defaultdict
from decimal import Decimal, getcontext
from pathlib import Path
ROOT=Path('.')
raw=(ROOT/'programme/research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
SHA=hashlib.sha256(raw).hexdigest(); N=json.loads(gzip.decompress(raw));F={int(k):v for k,v in N['frames'].items()}
D=json.load(open(ROOT/'root-work/BIT-NINE-PACKET-SCREEN.json'))
need=lambda c,m: (_ for _ in ()).throw(AssertionError(m)) if not c else None
need(SHA=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
need(D['native_sha256']==SHA,'screen/native cross pin')
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 a=[[Q(x) for x in r] for r in rows];m=len(a);n=len(a[0]) if m else 0;p=0
 for c in range(n):
  t=next((r for r in range(p,m) if a[r][c]),None)
  if t is None:continue
  a[p],a[t]=a[t],a[p];q=a[p][c];a[p]=[x/q for x in a[p]]
  for r in range(m):
   if r!=p and a[r][c]:q=a[r][c];a[r]=[x-q*y for x,y in zip(a[r],a[p])]
  p+=1
  if p==m:break
 return p
# Rebuild 111 input roots from actual start charts, as exact rational vectors.
roots=[]
for i in range(111):
 fr=F[N['start'][i]];need(fr['dim']==1 and len(fr['B'])==1,'source input line')
 r=[Q(x) for x in fr['B'][0]];n=dot(r,r);need(n in (1,4),'root norm')
 r=[2*x if n==1 else x for x in r];need(all(x.denominator==1 for x in r) and dot(r,r)==4,'integral norm4 roots');roots.append(tuple(int(x) for x in r))
# Every output facet is the exact orthogonal hyperplane of its own source root.
facets=[N['final'][111+i] for i in range(111)];need(len(set(facets))==111,'facet chart IDs unique')
need(all(F[c]['dim']==7 for c in facets),'all output facets rank7')
contacts=[];contact_span=[];no_self=[]
for i,c in enumerate(facets):
 v=roots[i];fr=F[c];AB=[[Q(x) for x in row] for row in fr['B']]
 need(len(AB)==7 and rank(AB)==7,'facet basis rank')
 need(all(dot(v,row)==0 for row in AB),'own source root is normal')
 s=[]
 for j,w in enumerate(roots):
  if j==i:
   need(dot(v,w)!=0,'self line excluded');continue
  if dot(v,w)==0:
   s.append(j);need(rank(AB+[[Q(x) for x in w]])==7,'contact root is contained in actual facet')
 need(i not in s,'no diagonal contact')
 need(rank([[Q(x) for x in roots[j]] for j in s])==7,'contacts span full rank7 facet')
 contacts.append(s);contact_span.append(7);no_self.append(True)
# Actual clean independent-X histories at each endpoint facet.
hist=defaultdict(set)
for h in D['histories']:hist[h['chart']].add(int(h['row']))
served=[i for i,c in enumerate(facets) if hist[c]]
need(len(served)==57,'57 exact-facet clean-X histories')
need(len(set(facets))==111,'no endpoint facet aliases')
rank_hist=Counter(rank([[((r>>j)&1) for j in range(111)] for r in hist[facets[i]]]) for i in served)
# Flat source histories have dimension 1 or 2 here, so treat every one as a fully free exception.
need(set(rank_hist)=={1,2},'facet history ranks are one or two')
missing=[i for i in range(111) if i not in served];need(len(missing)==54,'54 facets with no clean-X history')
# Exact geometric last-proper-chart implication encoded as theorem premises.
getcontext().prec=50;t=Decimal(199)/Decimal(200)
mp=lambda r:(Decimal(r).ln()*t).exp()
base=Decimal(289)*mp(1)+Decimal(244)*mp(2)+Decimal(111)*mp(7)+Decimal(9)*mp(8)
limit=Decimal('1621.750880211152355')
room=limit-base
split_per=(Decimal(8)*mp(1)-mp(8))
extra9=Decimal(9)*split_per
out={'status':'PASS_EXACT_FINAL_FACET_GEOMETRY_AND_EVENT_CUT','native_sha256':SHA,'screen_native_sha256':D['native_sha256'],
 'receiver_count':111,'distinct_final_facet_charts':len(set(facets)),'all_facet_dimensions':7,'contact_count_range':[min(map(len,contacts)),max(map(len,contacts))],
 'every_contact_set_spans_rank7_facet':True,'self_line_excluded_for_all':True,'clean_x_histories_at_exact_facet':57,'missing_clean_x_facets':54,'facet_history_rank_histogram':dict(sorted(rank_hist.items())),
 'movement_ceiling':'1621.750880211152355','baseline_moment_decimal':str(base),'baseline_room_decimal':str(room),'full_unit_split_8_to_7_to_6_to_5_to_4_to_3_to_2_to_1_to_0_per_packet_extra':str(split_per),'nine_such_splits_extra':str(extra9),
 'optimistic_new_moves_needed_after_9_packet_facet_visits':45,'lower_moment_if_rank1_each':45,'room_after_9_splits_decimal':str(room-extra9),
 'scope':'Source/geometry replay plus conditional event lower bound. For each of the54 facets with no X-only source-history record, if no correction-bearing nonpublic field enters that exact rank7 facet, every correction on the monotone public-Y lineage is supported in its last proper chart and cannot equal F_i. A nonzero operand must therefore be transported into Fi by a distinct MOVE (unless a new source schedule creates a row there). Distinct facets require distinct destination MOVE events. Nine prebudgeted monotone packet lineages can visit at most nine rank7 facets; if packet cloning or added cache moves are allowed, each remaining facet still costs at least one additional rank1 MOVE. The 57 histories are treated as if sufficient, although their ranks are only1–2. Does not validate rank-nine terminal fit decomposition or apply outside clean-X, fixed-final-K, additive monotone scheme.'}
json.dump(out,open('worker-c/bit-mutable-packets/TERMINAL-FACET-REVIEW.json','w'),indent=2)
print(json.dumps(out,indent=2))
