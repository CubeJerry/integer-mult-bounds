#!/usr/bin/env python3
"""Independent literal-prefix replay and full-input placement-cut ranks."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PREFIX='afa3e7d08904fcfad2e55babcdff14e6961b3e19ee4aa1df0e42e2f509191d0a'
S8=[0,14,15,30,38,39,59,60]
S12=[108,107,20,21,28,24,36,37,38,39,49,55]

def need(ok,msg):
 if not ok:raise ValueError(msg)

def echelon(rows):
 b={}
 for row in rows:
  v=list(map(F,row))
  for p,u in sorted(b.items()):
   c=v[p]
   if c:v=[x-c*y for x,y in zip(v,u)]
  p=next((i for i,x in enumerate(v) if x),None)
  if p is not None:
   c=v[p];b[p]=tuple(x/c for x in v)
 return b

def subset(a,b):
 for u in a.values():
  v=list(u)
  for p,r in sorted(b.items()):
   c=v[p]
   if c:v=[x-c*y for x,y in zip(v,r)]
  if any(v):return False
 return True

def binary_basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return b

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 nr=a.native.read_bytes();wr=a.prefix.read_bytes();need(hashlib.sha256(nr).hexdigest()==NATIVE,'native pin');need(hashlib.sha256(wr).hexdigest()==PREFIX,'literal prefix pin')
 n=json.loads(gzip.decompress(nr));w=json.loads(gzip.decompress(wr));need(w['public']==222 and w['start']==n['start'][:222],'native public input interface')
 bases={int(c):echelon(f['B']) for c,f in w['frames'].items()};dims={int(c):f['dim'] for c,f in w['frames'].items()}
 need(all(len(bases[c])==dims[c] for c in bases),'chart ranks')
 roots=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 loc=dict(enumerate(w['start']));rows={i:1<<i for i in range(222)};born=set(loc);counts=Counter();peak=0;pairs=set();moves={}
 for o in w['program']:
  t,i=o[:2];counts[t]+=1
  if t=='INIT':
   need(i>=222 and i not in born,'fresh zero birth');born.add(i);loc[i]=o[2];rows[i]=0;peak=max(peak,len(loc)-222)
  elif t=='CLEAR':
   need(i>=222 and loc.get(i)==o[2],'actual owned erasure');del loc[i];del rows[i]
  elif t=='MOVE':
   _,i,u,v=o;need(loc.get(i)==u,'actual MOVE source');d=dims[v]-dims[u];need(abs(d)==1,'literal unit MOVE')
   if i<222:need(d>0,'public ascents')
   moves.setdefault(i,set()).add(1 if d>0 else-1)
   if (u,v) not in pairs:
    low,high=(u,v) if d>0 else(v,u);need(subset(bases[low],bases[high]),'nested actual MOVE');pairs.add((u,v))
   loc[i]=v
  elif t=='ADD':
   _,i,j,c=o;need(i!=j and i in loc and j in loc and loc[i]==loc[j]==c,'actual cochart ADD');rows[i]^=rows[j]
  else:raise ValueError(t)
 need(all(len(v)==1 for v in moves.values()),'no route reversals')
 need(counts=={'INIT':80,'ADD':459,'MOVE':680,'CLEAR':3} and peak==78,'prefix invoice')
 need(len(loc)==222+77 and sum(loc[i]==1 for i in range(111))==83,'literal handoff roles')
 need(all(loc[111+i]==0 and rows[111+i]>>(111)==1<<i for i in range(111)),'all arbitrary original Y retained')
 need(all(rows[i]==1<<i for i in range(111) if loc[i]==1),'83 Hub originals unchanged')
 rank=lambda rr:len(binary_basis(rr));mask=(1<<111)-1
 outside_hub=[rows[i] for i,c in loc.items() if c!=1]
 pure_all=[x for x in outside_hub if x>>111==0]
 need(rank(pure_all)==105,'actual pure retained rank105')
 def cut(S,extra=()):
  inside={c:any(all(sum(x*y for x,y in zip(v,roots[i]))==0 for v in b.values()) for i in S) for c,b in bases.items()}
  fields=[i for i,c in loc.items() if inside[c]]
  observation=[rows[i] for i in fields]+list(extra)
  targets=[(1<<i)^(1<<(111+i)) for i in S]
  pure=[x for x in observation if x>>111==0]
  return {'targets':S,'inside_original_X':sum(i<111 for i in fields),'inside_original_Y':sum(111<=i<222 for i in fields),
          'inside_owned':sum(i>=222 for i in fields),'pure_X_rank':rank(pure),'full_input_observation_rank':rank(observation),
          'rank_with_targets':rank(observation+targets),'future_capacity_required':rank(observation+targets)-rank(observation),
          'all_pure_rows_zero_on_targets':all(not(x>>i&1) for x in pure for i in S)}
 first=cut(S8);second=cut(S12);drop=[1<<j for j in [8,9,16]]
 need((first['pure_X_rank'],first['full_input_observation_rank'],first['rank_with_targets'])==(86,197,205),'S8 exact cut')
 need((second['pure_X_rank'],second['full_input_observation_rank'],second['rank_with_targets'])==(92,203,215),'S12 exact cut')
 need(second['all_pure_rows_zero_on_targets'],'S12 coordinate separation')
 repairs={'S8_with_hypothetical_three_donor_observations':cut(S8,drop),
          'S12_with_hypothetical_three_donor_observations':cut(S12,drop)}
 need(repairs['S8_with_hypothetical_three_donor_observations']['future_capacity_required']==6,'donors repair only the S8 screen')
 need(repairs['S12_with_hypothetical_three_donor_observations']['future_capacity_required']==12,'donors do not repair S12')
 controls=[]
 for label,claim in [('global rank105 grants every cut six-message completion',first['future_capacity_required']<=6),
                     ('three donor observations repair every placement cut',repairs['S12_with_hypothetical_three_donor_observations']['future_capacity_required']<=6),
                     ('inside pure state carries selected pivot information',not second['all_pure_rows_zero_on_targets'])]:
  try:need(claim,label)
  except ValueError:controls.append(label)
  else:raise ValueError('negative control accepted')
 out={'status':'PASS_INDEPENDENT_LITERAL_RETAINED_DOWNSET_CUTS','native_sha256':NATIVE,'prefix_sha256':PREFIX,
      'author_code_imported':False,'input_columns':222,'prefix_receipt':{'counts':dict(counts),'peak_owned':peak,'actual_pure_retained_rank':105,'distinct_nested_MOVE_pairs':len(pairs)},
      'S8':first,'S12':second,'hypothetical_information_relaxations_not_emitted_words':repairs,
      'negative_controls':controls,'classification':'proved scoped dynamic cut; exact finite literal prefix; no completed decoder','new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'future_deficits':[first['future_capacity_required'],second['future_capacity_required']],'controls':len(controls)}))

if __name__=='__main__':main()
