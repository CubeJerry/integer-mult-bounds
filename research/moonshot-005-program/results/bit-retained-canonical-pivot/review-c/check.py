#!/usr/bin/env python3
"""Independent all-column replay, chronology and residual cut for the C5 word."""
import argparse,gzip,hashlib,json,copy
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

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

CYCLE=[92,36,54,38,55]
TARGETS=[0]
RESIDUAL=[4,8,9,14,30,73]
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PIVOTS='8c11ca368995bc6a77f8d0425ac259384a7edf6164bc4254dfc0c7d780e26e19'

def replay(word,native,E,closed=False):
 need(word['public']==222 and word['start']==native['start'][:222],'actual public inputs')
 bases={int(c):echelon(f['B']) for c,f in word['frames'].items()}
 dims={int(c):f['dim'] for c,f in word['frames'].items()}
 need(all(len(bases[c])==dims[c] for c in bases),'rational chart ranks')
 for c in set(word['start']):
  original=echelon(native['frames'][str(c)]['B'])
  need(subset(bases[c],original) and subset(original,bases[c]),'actual native initial geometry')
 loc=dict(enumerate(word['start']));rows={i:1<<i for i in range(222)}
 born=set(loc);peak=0;counts=Counter();pairs=set();trajectories={};erasures=[];history=[]
 for k,op in enumerate(word['program'],1):
  t,i=op[:2];counts[t]+=1
  if t=='INIT':
   need(i>=222 and i not in born,'fresh actual zero INIT');born.add(i);loc[i]=op[2];rows[i]=0
   peak=max(peak,len(loc)-222)
  elif t=='CLEAR':
   need(i>=222 and loc.get(i)==op[2],'owned erasure at actual chart')
   promised={333:E[0],336:E[1]^E[0],338:E[2]^E[0]}
   if i in promised:need(rows[i]==promised[i],'actual retained core before closure')
   erasures.append((k,i,op[2],rows[i]));del loc[i];del rows[i]
  elif t=='MOVE':
   _,i,u,v=op;need(loc.get(i)==u,'actual MOVE source');d=dims[v]-dims[u]
   need(abs(d)==1,'literal unit MOVE')
   if i<222:need(d>0,'all original physical paths ascend')
   if (u,v) not in pairs:
    lo,hi=(u,v) if d>0 else(v,u);need(subset(bases[lo],bases[hi]),'actual nested MOVE');pairs.add((u,v))
   trajectories.setdefault(i,[]).append((dims[u],dims[v],k));loc[i]=v
  elif t=='ADD':
   _,i,j,c=op;need(i!=j and i in loc and j in loc and loc[i]==loc[j]==c,'actual cochart ADD')
   rows[i]^=rows[j]
  else:raise ValueError('unknown operation '+t)
  for packet in (333,335,337):
   if packet in loc and dims[loc[packet]]<8:history.append(rows[packet]&((1<<111)-1))
 for i in range(111):
  expected=(1<<(111+i)) ^ ((1<<i) if i in TARGETS else E[i])
  need(rows[111+i]==expected,'exact arbitrary-Y endpoint '+str(i))
  if closed or i in TARGETS:need(subset(bases[loc[111+i]],echelon(native['frames'][str(native['final'][111+i])]['B'])) and dims[loc[111+i]]==7,'native Y endpoint')
  else:need(dims[loc[111+i]]==0,'uncompleted Y remains at ground')
  need(rows[i]==1<<i and dims[loc[i]]==8,'all original X restored at Hub')
 if closed:need(len(loc)==222,'all owned lifetimes closed')
 else:
  need(len(loc)==336,'114 retained caches')
  need(all(rows[222+i]==1<<i and loc[222+i]==native['start'][i] for i in range(111)),'111 actual stationary pure copies')
 return {'counts':dict(counts),'peak_owned':peak,'owned_live':len(loc)-222,'packet_X_history_rank':len(binary_basis(history)),
         'distinct_MOVE_pairs':len(pairs),'nonmonotone_owned':{str(i):p for i,p in trajectories.items() if i>=222 and len({b-a for a,b,k in p})>1},
         'erased_nonzero_values':sum(bool(r) for k,i,c,r in erasures)},loc,rows,bases,trajectories,erasures

def coalesced_profile(word):
 dims={int(c):f['dim'] for c,f in word['frames'].items()}
 pending={};profile=Counter()
 def flush(i):
  if i in pending:
   direction,distance=pending.pop(i);profile[distance]+=1
 for op in word['program']:
  kind,i=op[:2]
  if kind=='MOVE':
   delta=dims[op[3]]-dims[op[2]];direction=1 if delta>0 else-1
   if i in pending and pending[i][0]!=direction:flush(i)
   pending[i]=(direction,pending.get(i,(direction,0))[1]+abs(delta))
  elif kind=='ADD':flush(i);flush(op[2])
  else:flush(i)
 for i in list(pending):flush(i)
 return dict(sorted(profile.items()))

POWER_CACHE={}
def price_interval(profile):
 scale=1<<176;lower=F(0);upper=F(0)
 for rank,count in profile.items():
  if rank not in POWER_CACHE:
   target=(rank**199)*scale**200;lo=0;hi=rank*scale+1
   while hi-lo>1:
    mid=(lo+hi)//2
    if mid**200<=target:lo=mid
    else:hi=mid
   exact=lo**200==target
   POWER_CACHE[rank]=(F(lo,scale),F(lo if exact else hi,scale))
  a,b=POWER_CACHE[rank]
  lower+=count*(a if count>=0 else b);upper+=count*(b if count>=0 else a)
 return lower,upper

def residual_cut(loc,rows,bases,roots):
 inside={c:any(all(sum(x*y for x,y in zip(v,roots[i]))==0 for v in b.values())
               for i in RESIDUAL) for c,b in bases.items()}
 selected=[i for i,c in loc.items() if inside[c]]
 observation=[rows[i] for i in selected]
 targets=[(1<<i)^(1<<(111+i)) for i in RESIDUAL]
 r0=len(binary_basis(observation));r1=len(binary_basis(observation+targets))
 return {'receivers':RESIDUAL,'inside_fields':len(selected),'observation_rank':r0,
         'augmented_rank':r1,'deficit':r1-r0,
         'completed_Y_inside':sum(111+i in selected for i in TARGETS)}

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True)
 p.add_argument('--package',type=Path,required=True);p.add_argument('--caller',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 nr=a.native.read_bytes();need(hashlib.sha256(nr).hexdigest()==NATIVE,'native pin')
 native=json.loads(gzip.decompress(nr))
 roots=[list(map(F,native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
 K=[sum(int(i==j or sum(x*y for x,y in zip(u,v))==0)<<j for j,v in enumerate(roots)) for i,u in enumerate(roots)]
 B=[];indices=[]
 for i,row in enumerate(K):
  if len(binary_basis(B+[row]))>len(B):B.append(row);indices.append(i)
 need(indices==[0,1,2,4,8,9,14,30,59],'native independent canonical basis')
 H=[row ^ (K[0] if row&1 else 0) for row in B[1:]]
 L=K[0]^1;newbasis=[L]+H;lookup={0:0}
 for k,row in enumerate(newbasis):lookup.update({v^row:coeff^(1<<k) for v,coeff in list(lookup.items())})
 residual=[row^(row&1) for row in K]
 need(len(lookup)==512 and len(binary_basis(residual[1:]))==9,'rank-preserving coordinate projection')
 preloads=[];coefficients=[]
 for row in residual:
  coeff=lookup[row]&7;value=0
  for k,b in enumerate(newbasis[:3]):
   if coeff>>k&1:value^=b
  preloads.append(value);coefficients.append(coeff)
 code=json.loads((a.package/'CODE.json').read_text())
 for name,values in [('column_zero_complement_hex',H),('core_basis_hex',newbasis[:3]),
                     ('residual_fitting_rows_hex',residual),('receiver_preloads_hex',preloads),
                     ('six_remaining_modes_hex',H[2:])]:
  need(values==[int(x,16) for x in code[name]],'independent '+name)
 need(coefficients==code['receiver_core_coefficients'],'independent preload coefficients')
 need(L.bit_count()==56 and len(binary_basis(B+[L]))==10,'actual local form and full prescribed history dimension')
 for i,row in enumerate(residual[1:],1):
  need(row>>i&1 and not row & (((1<<111)-1)^K[i]),'remaining fitting mask')
 full=[1]+residual[1:]
 ell=sum(int((row^(1<<i)).bit_count()>36)+int((row^(1<<i)).bit_count()>52) for i,row in enumerate(full))
 need(ell==220,'support gate remains binding')
 prefix=json.loads(gzip.decompress((a.package/'PREFIX.json.gz').read_bytes()))
 closed=json.loads(gzip.decompress((a.package/'CLOSED-PARTIAL.json.gz').read_bytes()))
 author=json.loads((a.package/'RESULT.json').read_text());md=author['metadata']
 rp,loc,rows,bases,trajectories,erasures=replay(prefix,native,preloads)
 rc,*_=replay(closed,native,preloads,True)
 need(rp['counts']=={'INIT':117,'ADD':575,'MOVE':808,'CLEAR':3} and rp['peak_owned']==115,'prefix invoice')
 need(rc['counts']=={'INIT':117,'ADD':575,'MOVE':1578,'CLEAR':117} and rc['peak_owned']==115,'closed partial invoice')
 need(not rp['nonmonotone_owned'] and rp['packet_X_history_rank']==4,'actual descending histories have rank4')
 need([rows[i] for i in (333,336,338)]==newbasis[:3] and all(loc[i]==0 for i in (333,336,338)),'three pure retained cores at ground')
 need(334 not in loc and 333 in loc,'original-y cache retired; original pivot packet retained')
 cut=residual_cut(loc,rows,bases,roots)
 need((cut['observation_rank'],cut['augmented_rank'],cut['deficit'])==(215,221,6),'full222-column actual cut')
 need(cut['completed_Y_inside']==0,'completed pivot outside cut')
 profile=coalesced_profile(closed)
 need(profile=={1:57,6:56,7:167,8:2},'actual coalesced closed profile')
 budget=json.loads((a.package/'BUDGET.json').read_text());price_checks={}
 for extra in (0,6):
  augmented=dict(profile);augmented[8]+=extra;lo,hi=price_interval(augmented)
  claim=budget['actual_partial_moment'] if extra==0 else budget['conditional_future_Hub_modes']['6']['moment']
  need(F(claim['lower_rational'])<=lo<=hi<=F(claim['upper_rational']),'fresh exact moment interval')
  price_checks[str(extra)]={'lower_rational':str(lo),'upper_rational':str(hi)}
 caller_raw=a.caller.read_bytes();caller_pin=hashlib.sha256(caller_raw).hexdigest()
 need(caller_pin=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','retained caller receipt pin')
 caller=json.loads(caller_raw)
 N={int(k):F(v) for k,v in caller['native_paid'].items()};Hcost={int(k):F(v) for k,v in caller['helper_target'].items()}
 paid={int(k):F(v) for k,v in caller['paired_paid'].items()};target={int(k):F(v) for k,v in caller['paired_target'].items()}
 signed={k:(target.get(k,0)-paid.get(k,0))/36 for k in target.keys()|paid.keys()}
 limiting={k:N.get(k,0)-Hcost.get(k,0)+signed.get(k,0) for k in N.keys()|Hcost.keys()|signed.keys()}
 margins={}
 for extra in (6,7):
  augmented=dict(profile);augmented[8]+=extra;claim=budget['conditional_future_Hub_modes'][str(extra)]
  margins[str(extra)]={}
  for m,interval in claim['fixed_m_margins'].items():
   m=int(m);cost={k:limiting.get(k,0)+signed.get(k,0)/(m-1)-augmented.get(k,0) for k in limiting.keys()|signed.keys()|augmented.keys()}
   lo,hi=price_interval(cost)
   need(F(interval['lower_rational'])<=lo<=hi<=F(interval['upper_rational']),'fresh full-caller fixed-m margin')
   margins[str(extra)][str(m)]={'lower_rational':str(lo),'upper_rational':str(hi)}
 controls=[]
 omitted={'original_y_cache':md['original_y_cache'],'early_Y_precode':md['precode'][0],
          'actual_X_read':md['local_reads'][0],'K0_encoder_read':md['encoder'][0],
          'completed_Y_feedback':md['completed_Y_feedback'],'dirty_history_deposit':md['dirty_deposits'][0],
          'actual_y_purification':md['purification']}
 for k,item in enumerate(md['other_core']):
  omitted[f'H{k}_actual_encoder']=item['encoder'][0]
  omitted[f'H{k}_pure_cache']=item['copy']
  omitted[f'H{k}_receiver_deposit']=item['deposits'][0]
 for name,event in omitted.items():
  mutant=copy.deepcopy(closed);del mutant['program'][event]
  try:replay(mutant,native,preloads,True)
  except (ValueError,KeyError) as error:controls.append({'name':name,'rejected':True,'reason':str(error)})
  else:raise ValueError('mutant accepted '+name)
 mutant=copy.deepcopy(closed);at=md['pivot_completion']
 mutant['program'][at],mutant['program'][at+1]=mutant['program'][at+1],mutant['program'][at]
 try:replay(mutant,native,preloads,True)
 except (ValueError,KeyError) as error:controls.append({'name':'reversed_completion_exchange','rejected':True,'reason':str(error)})
 else:raise ValueError('reversed exchange accepted')
 # Closing after an early erasure would conceal loss of the promised live core.
 mutant=copy.deepcopy(prefix);mutant['program'].append(['CLEAR',333,0])
 try:replay(mutant,native,preloads)
 except (ValueError,KeyError) as error:controls.append({'name':'retire_useful_pivot_mode','rejected':True,'reason':str(error)})
 else:raise ValueError('lost useful mode accepted')
 pins={name:hashlib.sha256((a.package/name).read_bytes()).hexdigest() for name in
       ('PROOF.md','build.py','PREFIX.json.gz','CLOSED-PARTIAL.json.gz','CODE.json','RESULT.json','BUDGET.json')}
 out={'status':'PASS_INDEPENDENT_CANONICAL_PIVOT_SOURCE','author_code_imported_or_run':False,
      'native_sha256':NATIVE,'input_columns':222,'reviewed_pins':pins,'prefix':rp,'closed':rc,
      'static_remaining_rank':9,'prescribed_full_history_rank':10,'natural_full_fitting_ell':ell,
      'coalesced_profile':profile,'moment_intervals_t_199_over_200':price_checks,'actual_receiver_cut':cut,
      'retained_caller_sha256':caller_pin,'independent_fixed_m_margins':margins,
      'negative_controls':controls,'scope':'One target complete, same useful three-mode core retained; six-mode static complement only. Entire C+e0 history cannot meet support gate; no full supplier or kappa.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'controls':len(controls),'actual_history_rank':rp['packet_X_history_rank']}))

if __name__=='__main__':main()

