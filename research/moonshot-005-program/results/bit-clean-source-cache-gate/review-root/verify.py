#!/usr/bin/env python3
"""Independent source replay and dominated-union dynamic program for cache paths."""
import argparse,collections,gzip,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
 if not c:raise ValueError(m)
def integer_rows(rows):
 out=[]
 for row in rows:
  r=list(map(F,row));d=math.lcm(*(x.denominator for x in r));out.append(tuple(int(x*d) for x in r))
 return out
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank_mod(rows,p=1009):
 a=[[x%p for x in row] for row in rows];rank=0
 for c in range(8):
  k=next((i for i in range(rank,len(a)) if a[i][c]),None)
  if k is None:continue
  a[rank],a[k]=a[k],a[rank];z=pow(a[rank][c],-1,p);a[rank]=[x*z%p for x in a[rank]]
  for i in range(rank+1,len(a)):
   z=a[i][c]
   if z:a[i]=[(x-z*y)%p for x,y in zip(a[i],a[rank])]
  rank+=1
 return rank
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'Source identity')
 s=json.loads(gzip.decompress(raw));frames={int(c):f for c,f in s['frames'].items()};B={c:integer_rows(f['B']) for c,f in frames.items()};A={c:integer_rows(f['A']) for c,f in frames.items()}
 for c,f in frames.items():
  need(rank_mod(B[c])==f['dim'] and rank_mod(A[c])==8-f['dim'],'Independent complementary frame ranks')
  need(all(dot(x,y)==0 for x in B[c] for y in A[c]),'Exact frame orthogonality')
 def nested(c,d):return all(dot(x,y)==0 for x in B[c] for y in A[d])
 roots=[B[c][0] for c in s['start'][:111]];rows=[1<<i for i in range(111)];at=s['start'][:111];hist=collections.defaultdict(set);paid=collections.Counter();adds=0
 def save(i):hist[at[i]].add(rows[i])
 for i in range(111):save(i)
 for e in s['program']:
  op,i=e[:2]
  if i>=111:continue
  if op in ('ADD','SWAP'):
   j=e[2]
   if j>=111:continue
   adds+=1
   if op=='ADD':need(at[i]==at[j]==e[3],'Clean source cochart');rows[i]^=rows[j]
   else:rows[i],rows[j]=rows[j],rows[i];at[i],at[j]=at[j],at[i];save(j)
   save(i)
  elif op=='MOVE':
   c,d=e[2:];need(at[i]==c and frames[c]['dim']<frames[d]['dim'] and nested(c,d),'Actual upward MOVE')
   paid[frames[d]['dim']-frames[c]['dim']]+=1;at[i]=d;save(i)
  else:raise ValueError(op)
 need(rows==[1<<i for i in range(111)] and at==s['final'][:111],'Clean X endpoint')
 need(adds==628 and dict(paid)=={1:289,2:244} and sum(map(len,hist.values()))==1027,'Source counts')
 support={}
 for c,rr in hist.items():
  mask=0
  for row in rr:mask|=row
  need(all(all(dot(roots[j],v)==0 for v in A[c]) for j in range(111) if mask>>j&1),'Every history support lies in its chart')
  support[c]=mask
 charts=sorted(hist,key=lambda c:(frames[c]['dim'],c));pred={c:[d for d in charts if frames[d]['dim']<frames[c]['dim'] and nested(d,c)] for c in charts}
 need(all(not (frames[c]['dim']==frames[d]['dim'] and nested(c,d)) for c in charts for d in charts if c<d),'Distinct history chart geometries')
 # Every chain ending at C is a singleton or extends one ending at a smaller D.
 # Discarding a support union contained in another is safe for every later extension.
 states={};weighted={};peak=0
 for c in charts:
  possible={support[c]}
  for d in pred[c]:possible.update(u|support[c] for u in states[d])
  maximal=[]
  for u in sorted(possible,key=int.bit_count,reverse=True):
   if not any(u&~v==0 for v in maximal):maximal.append(u)
  states[c]=maximal;peak=max(peak,len(maximal))
  weighted[c]=support[c].bit_count()+max([weighted[d] for d in pred[c]]+[0])
 contacts=[];maxima=[];paths=[];weighted_bounds=[];receiver_unions=[]
 for i in range(111):
  facet=s['final'][111+i];need(frames[facet]['dim']==7 and all(dot(roots[i],v)==0 for v in B[facet]),'Actual receiver facet')
  target=sum(int(i!=j and dot(roots[i],roots[j])==0)<<j for j in range(111));contacts.append(target)
  need(rank_mod([roots[j] for j in range(111) if target>>j&1])==7,'Contact support spans actual facet')
  eligible=[c for c in charts if nested(c,facet)]
  receiver_unions.append({u for c in eligible for u in states[c]})
  maximum=max(u.bit_count() for c in eligible for u in states[c]);maxima.append(maximum);weighted_bounds.append(max(weighted[c] for c in eligible))
  need(maximum<target.bit_count(),'Any single chain misses a source coordinate')
  need(all(u&~target==0 for c in eligible for u in states[c]),'Chain support is entirely actual contact support')
  pooled=0
  for c in eligible:pooled|=support[c]
  need(pooled==target,'Pooled incomparable-chart support control')
 private=[]
 for i,target in enumerate(contacts):
  pair=min(((target&~contacts[h]).bit_count(),h) for h in range(111) if h!=i)
  private.append({'receiver':i,'minimum_private_coordinates':pair[0],'closest_other_receiver':pair[1],
   'max_single_chain_support':maxima[i],'gap':pair[0]-maxima[i]})
  best=min(((target&~contacts[h]&~u).bit_count(),h,u) for h in range(111) if h!=i for u in receiver_unions[i])
  private[-1].update({'minimum_private_ports_outside_any_one_suffix_chain':best[0],
   'best_partner_for_exception_bound':best[1],'best_suffix_support_mask':best[2]})
 need(min(x['minimum_private_coordinates'] for x in private)==21 and max(maxima)==18 and min(x['gap'] for x in private)==4,'Exact last-interaction gaps')
 author=json.loads((a.author/'RESULT.json').read_text())
 result={'status':'PASS_INDEPENDENT_SOURCE_AND_DOMINATED_UNION_PATH_REVIEW','native_sha256':PIN,
  'replayed_source':{'X_arithmetic':adds,'X_moves':dict(sorted(paid.items())),'distinct_history_rows':sum(map(len,hist.values())),'charts':len(charts)},
  'independent_algorithm':'Maximal support-union dynamic program on the exact chart poset, not author terminal-chain enumeration.',
  'largest_antichain_state_count':peak,'total_retained_union_states':sum(map(len,states.values())),
  'max_chain_contact_coordinates':max(maxima),'minimum_single_chain_missing_coordinates':min(x.bit_count()-m for x,m in zip(contacts,maxima)),
  'minimum_private_support':21,'minimum_last_interaction_gap':4,'per_receiver':private,
  'minimum_exception_ports_needed_even_for_one_output':min(x['minimum_private_ports_outside_any_one_suffix_chain'] for x in private),
  'maximum_receiver_exception_requirement':max(x['minimum_private_ports_outside_any_one_suffix_chain'] for x in private),
  'maximum_source_history_support_by_chart_dimension':{d:max(support[c].bit_count() for c in charts if frames[c]['dim']==d) for d in sorted({frames[c]['dim'] for c in charts})},
  'weighted_path_control_minimum_missing':min(x.bit_count()-m for x,m in zip(contacts,weighted_bounds)),
  'negative_controls':['Incomparable-chart pooled support recovers each complete contact support','Distinct chart geometries checked before strict-chain enumeration'],
  'reviewed_author_manifest_sha256':hashlib.sha256((a.author/'MANIFEST.json').read_bytes()).hexdigest(),
  'scope':'Fixed canonical initial y+Kx, clean independently executed X-only histories, stationary pure-X caches, monotone public-Y paths and no Y-bearing or informative moving owned copies. Universal support argument extends the stated tensor source to every characteristic-two field and V; no complete native or kappa.'}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','largest_antichain_state_count','total_retained_union_states','max_chain_contact_coordinates','minimum_single_chain_missing_coordinates','minimum_last_interaction_gap']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
