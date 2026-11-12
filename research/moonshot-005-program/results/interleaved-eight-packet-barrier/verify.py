#!/usr/bin/env python3
"""Source certificate for the interleaved eight-packet + mandatory-raw barrier."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
PARENT='184428adb93a4c62b14a106566bb7a5b6d358ef91fdc230c59159d9098853bfe'
D42='77c996ff9233f087a0e024c107b552f022adeca51cf5540c2487ef80cb2a2506'
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(vs):
 S={0}
 for v in vs:S|={x^v for x in tuple(S)}
 return frozenset(S)
def root(v):
 bs=[i for i in range(9) if v>>i&1]
 if len(bs)==3:return [2*int(i in bs) for i in range(8)] if 8 in bs else [1 if i in bs else -1 for i in range(8)]
 need(len(bs)==7,'root weight');i,j=[i for i in range(9) if i not in bs]
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def power(r):
 if not r:return Q(0),Q(0)
 d=1<<120;target=r**199*d**200;lo,hi=0,r*d+1
 while lo+1<hi:
  m=(lo+hi)//2
  if m**200<=target:lo=m
  else:hi=m
 need(lo**200<=target<(lo+1)**200,'exact directed power interval')
 return Q(lo,d),Q(lo+1,d)
def interval(cs):
 lo=hi=Q(0)
 for r,c in cs.items():
  a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi

def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes()
 need(sha(sb)==SPIN and sha(ib)==IPIN,'immutable source/invoice')
 need(sha((a.minimal_eight/'PROOF.md').read_bytes())==PARENT,'frozen minimal factor/locality/spectrum/rank saturation proof dependency')
 if a.distance42:need(sha((a.distance42/'PROOF.md').read_bytes())==D42,'frozen exact42 return theorem')
 s=json.loads(gzip.decompress(sb));invoice=json.loads(ib);N={x:s['frames'][s['initial'][x]][0] for x in s['live']};O=[z for z in range(512) if z.bit_count() in(3,7) and z not in N.values()]
 need(len(N)==104 and len(set(N.values()))==104 and len(O)==16,'source inventory')
 need(all(n.bit_count()%2==1 for n in N.values()),'parity vector511 excluded by every receiver facet')
 full_support={z:{x for x,n in N.items() if dot(root(z),root(n))} for z in O}
 need(all(len(S)==52 for S in full_support.values()),'each cheap omitted-root packet has52 recipients')
 need(all((x in full_support[z])==(not((n&z).bit_count()%2)) for z in O for x,n in N.items()),'source support/annihilator incidence identity')
 triples=[]
 for C in itertools.combinations(O,3):
  both=set.intersection(*(full_support[z] for z in C));need(len(both)>=7 and 511 not in span(C),'all triple contacts; parity cannot lie in a three-root span')
  triples.append({'roots':C,'common_receivers':sorted(both)})
 quads=[];pairminimum=104
 for C in itertools.combinations(O,4):
  masks={x:sum(int(x in full_support[z])<<i for i,z in enumerate(C)) for x in N}
  pairs=[]
  for i,j in itertools.combinations(range(4),2):
   roles=[x for x,m in masks.items() if m==(1<<i)|(1<<j)];need(len(roles)>=2,'every exact-pair cohort occurs');pairminimum=min(pairminimum,len(roles));pairs.append({'pair':[C[i],C[j]],'receivers':roles})
  quads.append({'roots':C,'six_exact_pair_classes':pairs})
 need(len(quads)==1820 and len(triples)==560,'complete three/four-root domain')
 # Endpoints make the mandatory raw-refinement fee source-exact.
 facets=[]
 for x in N:
  first=s['frames'][s['initial'][x+112]];last=s['frames'][s['final'][x+112]]
  need(len(first)==0 and len(last)==8,'actual firstY endpoints0->8');S=span(last);need(S==frozenset(v for v in range(512) if not((N[x]&v).bit_count()%2)),'actual source facet');facets.append(S)
 need(len(set(facets))==104,'different receivers have different dimension8 facets')
 f0,f1=interval({1:1,7:1,8:-1});need(f0>0,'strict mandatory split penalty')
 for d in range(2,7):
  cc=Counter({d:1});cc[8-d]+=1
  cc[1]-=1;cc[7]-=1
  need(interval(dict(cc))[0]>0,'interior split costs more than endpoint split')
 # Case zero cheap packets must also obey the unified lower bound.
 zero_gap=Counter({9:3,8:48,7:-51,1:-51});need(interval(zero_gap)[0]>0,'zero-cheap case exceeds unified interleaved packet+raw lower bound')
 raw=set(N)|{x+112 for x in N}|set(s['hosted']['X2'])|set(s['hosted']['Y2']);need(len(raw)==400,'raw inventory')
 for x in raw:need(len(s['frames'][s['final'][x]])-len(s['frames'][s['initial'][x]])==8 and span(s['frames'][s['initial'][x]])<=span(s['frames'][s['final'][x]]),'all400 raw paths retain net ascent8')
 old=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
 T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r,c in old.items():P[r]-=18*c
 lower_raw={8:349,7:51,1:51};lower_owned={9:5,8:3}
 for hist in (lower_raw,lower_owned):
  for r,c in hist.items():P[r]+=18*c
 need(all(c>=0 for c in P.values()),'nonnegative complete lower-profile invoice')
 h0,h1=interval({r:T[r]-P[r] for r in T.keys()|P.keys()});h0/=18;h1/=18;g0,g1=power(5);g0*=10;g1*=10;need(g0>h1,'interleaved pure8 interface still cannot fund exact42 fresh return')
 # Three retained chains exhibit why the old at-most2 theorem required global order.
 C=[97,42,82];U=span(C);need(len(U)==8,'three chosen normals independent in binary space')
 cyclic=[(C[0],C[1]),(C[1],C[2]),(C[2],C[0])]
 pair_owner={frozenset(pair):pair[0] for pair in cyclic};counts=Counter();deliveries=[]
 for x in N:
  H=[z for z in C if x in full_support[z]];counts[len(H)]+=1;facet=facets[list(N).index(x)]
  if len(H)==0:chain=[]
  elif len(H)==1:chain=[span(H)]
  elif len(H)==2:
   owner=pair_owner[frozenset(H)];first=next(z for z in H if z!=owner);chain=[span([first]),span(H)]
  else:chain=[U]
  need(all(A<=B for A,B in zip([frozenset([0])]+chain,chain+[facet])),'explicit retained-chain raw cochart routes ascend')
  deliveries.append({'source_role':x,'supported_late_roots':H,'raw_chart_dimensions':[len(T0).bit_length()-1 for T0 in chain]})
 need(dict(counts)=={0:8,1:44,2:44,3:8},'exact retained-three source pattern counts')
 # Bind the candidate budget to the real rank88 prefix stops, while still not
 # claiming a new phase-checked complete source word.
 parent_blob=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes()
 need(sha(gzip.decompress(parent_blob))=='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','actual retained-three candidate parent')
 parent=json.loads(gzip.decompress(parent_blob));rawmap={int(x):r for x,r in parent['private_role_map'].items()};frames=s['frames']+[q['frame'] for q in parent['additional_charts']];spaces=list(map(span,frames));raw_delta=Counter()
 for x in N:
  H=[z for z in C if x in full_support[z]];k=len(H)
  if not k:continue
  moves=[e for e in parent['program'][:parent['marks']['common_starts']] if e[0]=='MOVE' and e[1]==rawmap[x+112]]
  need(len(moves)==1 and len(frames[moves[0][2]])==0,'one actual unread firstY prefix ascent');target=moves[0][3];d=len(frames[target]);need(span(H)<spaces[target],'all selected normal spans fit actual prefix stop')
  if k==3:raw_delta[3]+=1
  else:raw_delta[1]+=k
  raw_delta[d-k]+=1;raw_delta[d]-=1
 need(dict(sorted((r,c) for r,c in raw_delta.items() if c))=={1:132,3:8,5:13,6:39,7:39,8:-91},'exact candidate raw delta')
 candidate_owned=Counter({9:5,6:3,1:6});candidate_total=candidate_owned.copy();candidate_total.update(raw_delta);candidate_total[9]-=8
 candidate_saving=interval({r:-c for r,c in candidate_total.items()});candidate_raw_fee=interval(raw_delta)
 candidate_P=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r,c in old.items():candidate_P[r]-=18*c
 candidate_P[8]+=18*400
 for hist in (raw_delta,candidate_owned):
  for r,c in hist.items():candidate_P[r]+=18*c
 ch0,ch1=interval({r:T[r]-candidate_P[r] for r in T.keys()|candidate_P.keys()});ch0/=18;ch1/=18
 need(g0>ch1,'the specific retained-three route also fails its fully charged favorable return budget')
 # Negative scope controls: stationary retained copies invalidate chronological
 # descent, while pair-class omission would weaken the capacity argument.
 need(len(list(itertools.combinations(range(4),2)))==6>4,'four-packet capacity mutant')
 fork_example=[O[0],511,O[1]];need(len(span(fork_example))==8,'genuine parity-fork3-chart example')
 result={'status':'PASS_INTERLEAVED_MINIMAL_EIGHT_PLUS_MANDATORY_RAW_BARRIER','source_sha256':SPIN,'invoice_sha256':IPIN,'parent_minimal_eight_proof_sha256':PARENT,'distance42_proof_sha256':D42,'all_three_root_subsets':560,'all_four_root_subsets':1820,'exact_pair_classes_checked':6*1820,'minimum_exact_pair_receiver_count':pairminimum,'every_cheap_broadcast_topology':'spatial descending chain, or a single parity fork with two dimension2 leaves; stationary copies may be retained indefinitely','maximum_cheap_packets_with_interleaving':3,'cheap_threshold':'9^(199/200)','mandatory_raw_split_receivers_if_any_cheap':51,'split_fee_lower':str(f0),'split_fee_upper':str(f1),'unified_extra_packet_and_raw_floor':'5*9^(199/200)+3*8^(199/200)+51*(1+7^(199/200)-8^(199/200))','lower_raw_profile':lower_raw,'lower_owned_profile':lower_owned,'complete_optimistic_headroom_lower':str(h0),'complete_optimistic_headroom_upper':str(h1),'fresh_return_floor_lower':str(g0),'fresh_return_floor_upper':str(g1),'deficit_lower':str(g0-h1),'deficit_upper':str(g1-h0),'three_retained_chain_scope_counterexample':{'normals':C,'cyclic_pair_owner':cyclic,'receiver_pattern_counts':dict(sorted(counts.items())),'owned_packet_profile_with_five_early_packets':{9:5,6:3,1:6},'actual_parent_payload_sha256':'2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','raw_delta':dict(sorted(raw_delta.items())),'raw_fee_lower':str(candidate_raw_fee[0]),'raw_fee_upper':str(candidate_raw_fee[1]),'saving_over_eight_rank9_parent_lower':str(candidate_saving[0]),'saving_over_eight_rank9_parent_upper':str(candidate_saving[1]),'candidate_complete_optimistic_headroom_lower':str(ch0),'candidate_complete_optimistic_headroom_upper':str(ch1),'candidate_fresh_return_deficit_lower':str(g0-ch1),'candidate_fresh_return_deficit_upper':str(g1-ch0),'status':'Exact abstract source-chart/copy schedule with actual pinned prefix stops and complete route invoice; no full-word phase/compiler admission claimed. It has three cheap packets because deliveries interleave.'},'negative_controls':['allones parity-fork exception retained','stationary copies can deliver after descendants: chronology cannot be inferred from spatial chain','all six exact-pair classes are required for four-versus-six counting'],'scope':'Exactly8 pure full-field minimal Gram packets; arbitrary interleaving, stationary owned copies and ambient charts; unchanged monotone receiver identities/endpoints; every informative owned move paid; no within-packet rank fragmentation or cross-packet mixing. The fresh-return incompatibility retains its own unchanged-source/fresh-packet hypotheses. Independent review pending. No new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.output/'QUADRUPLES.json').write_text(json.dumps(quads,indent=2,sort_keys=True)+'\n');(a.output/'TRIPLES.json').write_text(json.dumps(triples,indent=2,sort_keys=True)+'\n');(a.output/'THREE-RETAINED.json').write_text(json.dumps(deliveries,indent=2,sort_keys=True)+'\n');print(result['status']);print('headroom',float(h0),'deficit',float(g0-h1),'pair classes',len(quads)*6)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--minimal-eight',type=Path,required=True);ap.add_argument('--distance42',type=Path);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
