#!/usr/bin/env python3
"""Independent halfclass algebra, complete eight-frame census and prefix gate."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def basis(rows):
 b={};chosen=[]
 for index,x in enumerate(rows):
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;chosen.append(index);break
 return b,chosen

def census(neighbors):
 frames=[];nodes=0
 def visit(chosen,possible):
  nonlocal nodes
  nodes+=1
  if len(chosen)==8:frames.append(chosen);return
  required=8-len(chosen)
  while possible.bit_count()>=required:
   bit=possible&-possible;possible^=bit;i=bit.bit_length()-1
   visit(chosen+[i],possible&neighbors[i])
 visit([], (1<<111)-1)
 return frames,nodes

def gauge(k,groups,pivots,frames):
 need(len(groups)==len(pivots)==36,'all halfclass/coordinate pivots')
 need(all(p in group for p,group in zip(pivots,groups)),'pivot belongs to its own group')
 d=[sum(1<<j for j in group) for group in groups]
 rows=[]
 for i,row in enumerate(k):
  for mask,p in zip(d,pivots):
   if row>>p&1:row^=mask
  need(not(row>>i&1),'gauged own coefficient zero')
  need(all(not(row>>p&1) for p in pivots),'gauged pivot columns zero')
  rows.append(row)
 b,chosen=basis(rows);need(len(b)==3,'three global quotient modes')
 hist=Counter();witness={}
 for frame in frames:
  mask=sum(1<<j for j in frame);rank=len(basis([row&mask for row in b.values()])[0])
  hist[rank]+=1;witness.setdefault(rank,frame)
 return {'pivots':pivots,'quotient_basis_original_receiver_indices':chosen,
         'quotient_basis_rows':[hex(rows[i]) for i in chosen],
         'rank_counts':dict(sorted(hist.items())),'rank_witnesses':dict(sorted(witness.items())),
         'minimum_restricted_rank':min(hist),'total_packet_lower_bound_after_three_unchanged_broadcasts':11-min(hist)}

def retention(k,groups,pivots):
 """Full (X,Y)-row quotient, including arbitrary independent original Y."""
 rank=lambda rows:len(basis(rows)[0])
 masks=[sum(1<<j for j in group) for group in groups]
 rows=[]
 for row in k:
  for mask,p in zip(masks,pivots):
   if row>>p&1:row^=mask
  rows.append(row)
 core=[rows[i] for i in basis(rows)[1]]
 donors=[i for i in range(8,111) if i not in pivots]
 columns=[sum(((b>>j)&1)<<t for t,b in enumerate(core)) for j in donors]
 omitted=[donors[i] for i in basis(columns)[1]]
 need(omitted==[8,9,16],'independent donor minor')
 retained=[i for i in donors if i not in omitted]+[0,1]
 banks=masks[8:];pure=banks+[1<<i for i in retained]
 target=[(1<<i)^rows[i] for i in range(111)]
 cases={}
 for label,p in [('bare_banks',banks),('individual_copies_without_core',pure),
                 ('individual_copies_with_core',pure+core)]:
  # Check the simplified formula against the full222-column observation map.
  observation=p+[rows[i]^(1<<(111+i)) for i in range(111)]
  endpoints=[(1<<i)^(1<<(111+i)) for i in range(111)]
  deficit=rank(p+target)-rank(p)
  need(deficit==rank(observation+endpoints)-rank(observation),'full unknown-Y quotient')
  cases[label]={'pure_X_rank':rank(p),'X_projection_rank_including_masked_Y':rank(p+rows),
                'additional_packet_information_required':deficit,
                'total_packet_lower_bound_after_three_broadcasts':3+deficit}
 need(rank(pure)==102 and rank(pure+core)==105,'retained pure information')
 need(cases['individual_copies_without_core']['additional_packet_information_required']==9,
      'unknown Y cannot stand in for actual core observations')
 need(cases['individual_copies_with_core']['additional_packet_information_required']==6,
      'six-message abstract information repair')
 return {'omitted_donor_minor_columns':omitted,'retained_individual_indices':retained,
         'core_basis_rows':[hex(x) for x in core],'rank_I_plus_R':rank(target),'cases':cases}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True)
 ap.add_argument('--repair',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source')
 s=json.loads(gzip.decompress(raw));rr=[list(map(F,s['frames'][str(s['start'][i])]['B'][0])) for i in range(111)]
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 k=[sum(int(i==j or dot(v,w)==0)<<j for j,w in enumerate(rr)) for i,v in enumerate(rr)]
 groups={}
 for i,r in enumerate(rr):
  support=tuple(j for j,x in enumerate(r) if x);sgn=1 if r[support[0]]>0 else-1
  key=(support,sum(x*sgn<0 for x in r)%2);groups.setdefault(key,[]).append(i)
 groups=list(groups.values());need(len(groups)==36 and all(g==[i] for i,g in enumerate(groups[:8])),'36 local groups')
 need(all(dot(rr[i],rr[j])==0 for g in groups for i in g for j in g if i!=j),'orthogonal halfclass groups')
 d=[sum(1<<j for j in g) for g in groups]
 need(len(basis(d)[0])==36 and len(basis(k)[0])==9 and len(basis(k+d)[0])==39,'exact code dimensions')
 nmask=(1<<111)-1
 neighbors=[nmask^row for row in k] # K diagonal1; complement has no loops.
 frames,nodes=census(neighbors)
 need(len(frames)==4373,'complete native eight-frame census')
 minimum=gauge(k,groups,[min(g) for g in groups],frames)
 need(minimum['rank_counts']=={0:31,1:124,2:782,3:3436},'minimum-index gauge independent census')
 repair_raw=a.repair.read_bytes();r=json.loads(repair_raw);repaired=gauge(k,groups,list(range(8))+r['pivots'],frames)
 need(repaired['rank_counts']=={2:440,3:3933},'repaired gauge independent census')
 retained=retention(k,groups,list(range(8))+r['pivots'])
 sizes=Counter(map(len,groups[8:]));need(sizes=={2:2,3:5,4:21},'actual halfclass sizes')
 capture=Counter({7:8})
 for group in groups[8:]:
  size=len(group);capture[size-1]+=size;capture[8-size]+=size
 need(capture=={1:4,2:15,3:84,4:84,5:15,6:4,7:8},'support-span capture profile')
 controls=[]
 for label,condition in [('q8 completion after repaired unchanged broadcasts',repaired['minimum_restricted_rank']>=3),
                         ('masked R supplies pure cache information',retained['cases']['individual_copies_without_core']['additional_packet_information_required']<=6),
                         ('source byte alteration',hashlib.sha256(raw+b'x').hexdigest()==PIN)]:
  try:need(condition,label)
  except ValueError:controls.append(label)
  else:raise ValueError('control accepted: '+label)
 out={'status':'PASS_INDEPENDENT_HALFCLASS_FRAME_GATES','native_sha256':PIN,
      'repair_source_sha256':hashlib.sha256(repair_raw).hexdigest(),'author_checker_imported':False,
      'D_dimension':36,'C_dimension':9,'C_plus_D_dimension':39,'intersection_dimension':6,
      'complete_eight_frame_census':{'count':len(frames),'recursive_nodes':nodes},
      'halfclass_size_histogram':dict(sorted(sizes.items())),
      'support_span_X_capture_profile':dict(sorted(capture.items())),
      'minimum_index_gauge':minimum,'repaired_gauge':repaired,
      'full_input_retention_audit':retained,
      'negative_controls':controls,
      'classification':'exact finite algebra and necessary prefix packet gate; no complete source or supplier',
      'new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'frames':len(frames),'census_nodes':nodes,
                   'minimum_gauge_packet_floor':minimum['total_packet_lower_bound_after_three_unchanged_broadcasts'],
                   'repaired_gauge_packet_floor':repaired['total_packet_lower_bound_after_three_unchanged_broadcasts']}))
if __name__=='__main__':main()
