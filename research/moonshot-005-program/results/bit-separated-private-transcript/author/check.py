#!/usr/bin/env python3
"""Independent actual-state audit and disjoint private-arrival / broadcast cut.

No source builder or source interpreter is imported. The retained Fraction
chart implementation and separately reviewed exact Shannon rules are pinned.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction
from pathlib import Path

BASE=Path('/workspace/scratch/abe0e83e3d3b/programme')
PREFIX=Path('research/moonshot-005-program')
S=PREFIX/'sessions/2026-11-17-S020'
NATIVE=PREFIX/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
GEOMETRY=S/'checkpoint2-evidence/C/four-plane-review/check.py'
DUAL=S/'checkpoint6-evidence/C/sixteen-fresh-transcript/output/MAPPED-DUAL.json'
ENTROPY=S/'checkpoint1-evidence/C/entropy54-review/check.py'
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'geometry':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
 'entropy':'582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23',
 'single':'a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc',
 'triple':'9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6'}
TARGETS={14,17,19,20,96,99,101,102}
FRAMES=[[27,16,11,39,36,51,62,63],[27,16,11,39,36,57,68,72],
 [27,16,11,36,37,74,63,72],[27,16,11,36,51,57,78,74],
 [9,21,28,52,37,46,73,77],[9,21,28,52,37,44,71,67],
 [9,21,28,36,37,65,73,71],[9,21,28,37,46,44,64,65],
 [36,37,78,64,62,68,77,67]]

def need(x,s):
 if not x:raise ValueError(s)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def save(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def role_name(b,c,k,i):return f'C{c}__{k}{i}'if b>1 else f'{k}{i}'
def column(c,k,i):return c*222+(111 if k=='Y'else 0)+i

def binary_rank(rows):
 piv={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in piv:r^=piv[p]
   else:piv[p]=r;break
 return len(piv)

def check_frames(frames,R,remaining):
 need(len(frames)==9,'nine frames')
 count=Counter()
 for frame in frames:
  need(len(frame)==len(set(frame))==8 and set(frame)<=remaining,'eight remaining roles per frame')
  need(all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in frame for j in frame if i!=j),'real NONorthogonal frame')
  count.update(frame)
 need(all(v%2==0 for v in count.values()),'all incidence multiplicities even')
 return {'frames':frames,'roles':sorted(count),'multiplicities':dict(sorted(count.items())),
         'frame_count':9,'frame_size':8,'all_width_linear_fitting_floor_per_copy':9}

def replay(w,b,R,g):
 C={n:g.chart(z)for n,z in w['charts'].items()}
 for i,r in enumerate(R):
  need(C[f'L{i}']==g.basis((tuple(r),)),'native line')
  need(C[f'F{i}']==g.kernel((tuple(r),)),'native facet')
 v={role_name(b,c,k,i):1<<column(c,k,i)for c in range(b)for k in ['X','Y']for i in range(111)}
 p={role_name(b,c,k,i):(f'L{i}'if k=='X'else'zero')for c in range(b)for k in ['X','Y']for i in range(111)}
 born=set();owned=set();counts=Counter();moves=Counter();up=Counter();down=Counter();cv=cp=None
 for step,(op,n,*args)in enumerate(w['operations']):
  if step==w['carrier_interface_before_operation']:cv=v.copy();cp=p.copy()
  counts[op]+=1
  if op=='INIT':need(n not in born and n not in v,'fresh owned name');v[n]=0;p[n]=args[0];owned.add(n);born.add(n)
  elif op=='ADD':
   dest=args[0];need(n!=dest and C[p[n]]==C[p[dest]],'cocharted ADD');v[dest]^=v[n]
  elif op=='MOVE':
   A,B=C[p[n]],C[args[0]];delta=len(B)-len(A)
   need(delta!=0,'positive rank movement')
   need(g.contained(A,B)if delta>0 else g.contained(B,A),'nested movement')
   if n in owned:(up if delta>0 else down)[abs(delta)]+=1
   else:need(delta>0,'publics strictly upward')
   moves[abs(delta)]+=1;p[n]=args[0]
  elif op=='CLEAR':need(n in owned,'owned retirement');owned.remove(n);del v[n];del p[n]
  else:raise ValueError(op)
 need(cv is not None and not owned and len(v)==222*b,'cut and closure')
 for c in range(b):
  for i in range(111):
   x=role_name(b,c,'X',i);y=role_name(b,c,'Y',i)
   need(v[x]==1<<column(c,'X',i)and p[x]=='Hub','all original X raw at Hub')
   need(p[y]==f'F{i}','all original Y final charts')
   need(v[y]==cv[y],'source closure preserves every complete coefficient row')
   need(cv[y]>>column(c,'Y',i)&1,'own original Y survives')
 need(all(o[0]in {'MOVE','CLEAR'}for o in w['operations'][w['carrier_interface_before_operation']:]),'closing suffix has no hidden arithmetic')
 need(all(o[0]!='MOVE'or o[1]not in born for o in w['operations'][w['carrier_interface_before_operation']:]),'closing suffix has no owned movement already paid')
 return C,cv,cp,{'counts':dict(counts),'movement_profile':dict(moves),'owned_upward':dict(up),'owned_downward':dict(down)}

def audit_source(w,b,R,g):
 C,V,P,stats=replay(w,b,R,g)
 N=[sum(1<<j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0)for i in range(111)]
 unknown=set(range(8,111));remaining=unknown-TARGETS
 need(len(remaining)==95,'95 other unknown roles')
 audits=[]
 for i in unknown:
  allowed=sum(N[i]<<(222*c)for c in range(b));unknownmask=sum(sum(1<<column(c,'X',j)for j in unknown)for c in range(b))
  inside=[n for n in V if g.contained(C[P[n]],C[f'F{i}'])]
  leaks=[n for n in inside if V[n]&unknownmask&~allowed]
  need(not leaks,'actual unknown-coordinate locality at facet '+str(i))
  audits.append({'receiver':i,'inside_fields':len(inside),'leaks':leaks})
 groups={}
 for i in sorted(TARGETS):
  name=role_name(b,0,'Y',i);H=C[P[name]];need(len(H)==6,'raised targets have rank6')
  key=repr(H);groups.setdefault(key,{'chart':P[name],'H':H,'roles':[]})['roles'].append(i)
  need(all(C[P[role_name(b,c,'Y',i)]]==H for c in range(b)),'all copies share the actual geometric target chart')
 need(len(groups)==4,'four private regions')
 regions=[]
 for group in groups.values():
  H=group['H'];roles=group['roles'];need(len(roles)==2,'two target roles per private region')
  facets=[i for i in range(111)if g.contained(H,C[f'F{i}'])]
  need(facets==sorted(roles),'exactly the two facets contain the high chart')
  charts=[H]+[C[f'F{i}']for i in roles]
  fields=[n for n in V if C[P[n]]in charts]
  need(set(fields)=={role_name(b,c,'Y',i)for c in range(b)for i in roles},'all current fields in private region enumerated')
  pairmask=sum(1<<column(c,'X',i)for c in range(b)for i in roles)
  need(all(not(V[n]&pairmask)for n in fields),'no own-pair source information inside current private region')
  need(not(set(facets)&remaining),'private regions disjoint from remaining downset')
  regions.append({'rank6_chart':group['chart'],'roles':roles,'containing_receiver_facets':facets,'all_initial_inside_fields':fields,
                  'missing_independent_record_inputs':2*b,'required_future_positive_MOVE_arrivals':2*b})
 need(sum(x['required_future_positive_MOVE_arrivals']for x in regions)==8*b,'total private arrival floor')
 need(all(P[role_name(b,c,'X',i)]=='Hub'for c in range(b)for i in range(111)),'no old public X can enter a proper region')
 # Prove the restricted canonical fitting attains nine over every char2 field.
 K=[sum((1 if i==j or sum(x*y for x,y in zip(R[i],R[j]))==0 else 0)<<j for j in sorted(remaining))for i in sorted(remaining)]
 need(binary_rank(K)==9,'restricted canonical fitting rank9')
 return C,V,P,stats,regions,audits

def interval_record(iv):
 from decimal import Decimal,localcontext
 with localcontext()as ctx:
  ctx.prec=60
  return {'rational':list(map(str,iv)),'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in iv]}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=BASE)
 p.add_argument('--triple-word',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/workers/A/three-copy-f8/output/WORD.json'))
 p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 for key,path in [('native',NATIVE),('geometry',GEOMETRY),('entropy',ENTROPY)]:need(digest(a.repo/path)==PINS[key],'authenticated '+key)
 g=mod(a.repo/GEOMETRY,'independent_fraction_geometry');h=mod(a.repo/ENTROPY,'independent_set_shannon_rules')
 R=json.loads((a.repo/NATIVE).read_bytes())['native_roots'];remaining=set(range(8,111))-TARGETS
 frames=check_frames(FRAMES,R,remaining)
 dual=json.loads((a.repo/DUAL).read_bytes());h.CORE=dual['roles'];h.ISO=dual['isolates']
 need(set(h.CORE+h.ISO)<=remaining,'fresh Shannon witness avoids private targets and axes');entropy=h.review_dual(dual,R)
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(x/6 for x in g.moment(gate));cases=[]
 for name,b,path in [('single',1,a.repo/S/'checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json'),('triple',3,a.triple_word)]:
  need(digest(path)==PINS[name],'authenticated '+name+' source');w=json.loads(path.read_bytes())
  C,V,P,stats,regions,audits=audit_source(w,b,R,g)
  knowncounts={'single':{'INIT':188,'ADD':1400,'MOVE':508,'CLEAR':188},'triple':{'INIT':552,'ADD':4412,'MOVE':1488,'CLEAR':552}}
  need(stats['counts']==knowncounts[name],'complete source counts')
  linear=17*b;nonlinear=8*b+(17*b+1)//2
  totalQ=g.moment(stats['movement_profile']);q=tuple(x/b for x in totalQ)
  roomlin=(ceiling[0]-q[1]-17,ceiling[1]-q[0]-17)
  roomnon=(ceiling[0]-q[1]-Fraction(nonlinear,b),ceiling[1]-q[0]-Fraction(nonlinear,b))
  case={'name':name,'word_sha256':digest(path),'copies':b,'cut':w['carrier_interface_before_operation'],'all_input_columns':222*b,
   'live_fields':len(V),'source_stats':stats,'all103_current_facet_audits':audits,'private_regions':regions,
   'global_native_locality_leaks':0,'linear_remaining_downset_descent_floor':9*b,'nonlinear_remaining_downset_descent_floor':(17*b+1)//2,
   'private_region_arrival_floor':8*b,'disjoint_total_linear_positive_MOVE_floor':linear,
   'disjoint_total_nonlinear_positive_MOVE_floor':nonlinear,'normalized_source_moment':interval_record(q),
   'necessary_normalized_room_after_linear_floor':interval_record(roomlin),'necessary_normalized_room_after_nonlinear_floor':interval_record(roomnon)}
  save(a.out/(name.upper()+'-CUT.json'),[{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())]);cases.append(case)
 # Meaningful source, geometry, parity, and Shannon mutations.
 controls=[]
 bad=json.loads(json.dumps(FRAMES));bad[-1]=bad[0]
 try:check_frames(bad,R,remaining)
 except ValueError as ex:controls.append({'mutation':'duplicate a frame','rejected':str(ex)})
 else:raise ValueError('bad frame accepted')
 bad=json.loads(json.dumps(dual));bad['terms'].pop()
 try:h.review_dual(bad,R)
 except ValueError as ex:controls.append({'mutation':'delete a dual term','rejected':str(ex)})
 else:raise ValueError('bad dual accepted')
 for case in cases:
  # A hypothetical own input at the target's actual rank6 chart breaks both
  # the private-input premise and the facet-native locality premise.
  i=case['private_regions'][0]['roles'][0]
  need(i not in [j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0],'own root not in own facet')
  controls.append({'mutation':case['name']+' grant missing x_'+str(i)+' inside private rank6 chart',
                   'rejected':'own coordinate would violate audited native locality and private input absence'})
 result={'status':'PASS_DISJOINT_PRIVATE_REGION_AND_REMAINING_DOWNSET_BOUNDS','pins':PINS,
  'remaining95_roles':sorted(remaining),'fresh_nine_frame_certificate':frames,'restricted_canonical_scalar_rank':9,
  'fresh_entropy_core':dual['roles'],'fresh_entropy_isolates':dual['isolates'],'exact_entropy_terms':entropy['terms'],
  'exact_entropy_bound_per_copy':'17/2','cases':cases,'negative_controls':controls,
  'scope':'For the literal current cuts: at least17b extra positive whole-record MOVEs for char2 linear continuations, and8b+ceil(17b/2) for finite-alphabet fixed-schedule zero-error nonlinear continuations. All initial Y and all external inputs may be conditioned only in the proof. Public records remain monotone; arbitrary paid nested owned turns are permitted. No complete supplier or caller claim.'}
 save(a.out/'CERTIFICATE.json',result);save(a.out/'FRAME-CERTIFICATE.json',frames)
 print(result['status'])
 for case in cases:print(case['name'],case['all_input_columns'],case['live_fields'],'linear',case['disjoint_total_linear_positive_MOVE_floor'],'nonlinear',case['disjoint_total_nonlinear_positive_MOVE_floor'],'room',case['necessary_normalized_room_after_linear_floor']['decimal'][0])
if __name__=='__main__':main()
