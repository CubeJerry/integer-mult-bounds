#!/usr/bin/env python3
"""Independent actual-cut replay, locality audit and sharp transcript controls."""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
from release_projection import N,chart,replay,require,rref
from price_projection import moment,record
PIN='dd60233b57be5fdef83b86a2d2b816e665e3d939850da94b680838d1d6d178ce'
PROOF='c72dadaad343844658a3e1f35365d7ed216a5521832f335b59537157f063e2e0'
J=[5,35,93,96,97,109,110]
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();raw=(a.work/'A/lower-history59-paid/WORD.json').read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'paid59 word pin');w=json.loads(raw)
 proof=(a.work/'R/local-cut-descents/PROOF.md').read_bytes();require(hashlib.sha256(proof).hexdigest()==PROOF,'reviewed proof pin')
 sr=(a.repo/w['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==w['source_sha256'],'native source pin');R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
 for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'all native charts')
 stats,tr,_=replay(w,collect=True);cut=w['carrier_interface_before_operation'];require(cut==1380,'actual fixed cut');v,at=tr[cut]
 unfinished=sorted(set(range(N))-set(w['targets']));originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};owned=set(v)-originals
 require(len(unfinished)==52 and len(owned)==185 and all(v[n]>>N==0 for n in owned),'actual cut owner/receiver contract')
 for i in range(N):
  require(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub','all originals rawHub')
  require(v[f'Y{i}']==(1<<(N+i))^((1<<i)if i in w['targets']else 0)and at[f'Y{i}']==(f'F{i}'if i in w['targets']else'zero'),'actual output cut')
 contain={}
 def local(n,j,loc):
  key=(loc,j)
  if key not in contain:contain[key]=len(rref(C[loc]+C[f'L{j}'])[0])==len(C[loc])
  return contain[key]
 def violations(values,locations,grant=0):
  checks=0;bad=[]
  for n,row in values.items():
   for j in unfinished:
    if row>>j&1 and not(grant>>j&1):
     checks+=1
     if not local(n,j,locations[n]):bad.append([n,j,locations[n]])
  return checks,bad
 checked,bad=violations(v,at);require(not bad,'all unfinished coefficients genuinely local')
 dots=[[sum(x*y for x,y in zip(R[i],R[j]))for j in J]for i in J]
 require(set(J)<=set(unfinished)and all(z!=0 for row in dots for z in row),'actual unfinished nonorthogonal clique including self')
 suffix=w['operations'][cut:];require(len(suffix)==237,'frozen closure size')
 require(sorted(o for o in suffix if o[0]=='MOVE')==sorted([['MOVE',f'Y{i}',f'F{i}']for i in unfinished]),'exact52 original direct closures')
 require(sum(o[0]=='CLEAR'for o in suffix)==185 and all(o[0]in{'MOVE','CLEAR'}for o in suffix),'no hidden future source work')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);allow=(gl/6,gh/6);q=moment(stats['movement_profile']);fp=stats['movement_profile'].copy();fp[1]=fp.get(1,0)+7;floor=moment(fp)
 require(floor[0]>allow[1]and allow[1]-q[0]<3,'directed quantitative fixed-cut rejection')
 # A physically paid earlier nonlocal field invalidates the zero-grant premise.
 nonlocal_word=copy.deepcopy(w);name='C_REVIEW_NONLOCAL_X5';ops=[['INIT',name,'Hub'],['ADD','X5',name],['MOVE',name,'zero']]
 nonlocal_word['operations'][cut:cut]=ops;nonlocal_word['operations'].append(['CLEAR',name]);nonlocal_word['carrier_interface_before_operation']=cut+3
 ns,nt,_=replay(nonlocal_word,collect=True);nv,na=nt[cut+3];_,nb=violations(nv,na)
 require(nb==[[name,5,'zero']],'actual added global source violates exactly its column');require(not violations(nv,na,1<<5)[1],'one actual global direction explains the violation')
 # Seven actual rank1 descents complete the selected clique: the count is sharp
 # for these seven outputs, although this does not complete the other45.
 saturation=copy.deepcopy(w);body=[];newowners=[]
 for j in J:
  n=f'C_REVIEW_DELIVER_{j}';newowners.append(n);body.extend([['INIT',n,'Hub'],['ADD',f'X{j}',n],['MOVE',n,f'F{j}'],['MOVE',f'Y{j}',f'F{j}'],['ADD',n,f'Y{j}']])
 oldtail=[o for o in suffix if not(o[0]=='MOVE'and o[1]in{f'Y{j}'for j in J})]
 saturation['operations']=w['operations'][:cut]+body+oldtail+[['CLEAR',n]for n in newowners];saturation['targets']=sorted(set(w['targets'])|set(J));sat,_,_=replay(saturation)
 require(sat['movement_profile']==fp,'seven actual rank1 descents exactly saturate the selected-clique floor')
 # Orthogonal-pair control: one whole-record descent can serve two outputs
 # when the nonorthogonality premise is absent.
 pair=[3,4];require(sum(x*y for x,y in zip(R[3],R[4]))==0,'orthogonal control inputs')
 pw={k:copy.deepcopy(w[k])for k in ['source_path','source_sha256','charts']};pw.update(schema='C-orthogonal-pair-one-descent-control-v1',targets=pair,operations=[])
 pw['charts']['C_REVIEW_PAIR_SPAN']={'kind':'span','rows':[R[i]for i in pair]};pops=pw['operations']
 for i in pair:pops.extend([['INIT',f'C_REVIEW_RAW_{i}',f'L{i}'],['ADD',f'X{i}',f'C_REVIEW_RAW_{i}'],['MOVE',f'X{i}','C_REVIEW_PAIR_SPAN']])
 pops.extend([['INIT','C_REVIEW_PAIR_CODE','C_REVIEW_PAIR_SPAN']]+[['ADD',f'X{i}','C_REVIEW_PAIR_CODE']for i in pair]+[['MOVE','C_REVIEW_PAIR_CODE','zero']])
 for i,j in [(3,4),(4,3)]:pops.extend([['ADD','C_REVIEW_PAIR_CODE',f'Y{i}'],['MOVE',f'Y{i}',f'L{j}'],['ADD',f'C_REVIEW_RAW_{j}',f'Y{i}'],['MOVE',f'Y{i}',f'F{i}']])
 for i in range(N):
  pops.append(['MOVE',f'X{i}','Hub'])
  if i not in pair:pops.append(['MOVE',f'Y{i}',f'F{i}'])
 pops.extend([['CLEAR','C_REVIEW_PAIR_CODE']]+[['CLEAR',f'C_REVIEW_RAW_{i}']for i in pair]);ps,_,_=replay(pw)
 born={o[1]for o in pops if o[0]=='INIT'};descents=[o for o in pops if o[0]=='MOVE'and o[1]in born]
 require(descents==[['MOVE','C_REVIEW_PAIR_CODE','zero']],'one actual owned descent serves both orthogonal receivers')
 a.out.mkdir(parents=True,exist_ok=True);pins={}
 for name,ww in [('NONLOCAL-CUT-CONTROL',nonlocal_word),('SEVEN-DESCENT-CONTROL',saturation),('ORTHOGONAL-PAIR-CONTROL',pw)]:
  data=(json.dumps(ww,indent=2)+'\n').encode();(a.out/(name+'.json')).write_bytes(data);pins[name]=hashlib.sha256(data).hexdigest()
 result={'status':'PASS_INDEPENDENT_FIXED_CUT_SEVEN_DESCENT_THEOREM','proof_sha256':PROOF,'word_sha256':PIN,'native_source_sha256':w['source_sha256'],
  'stats':stats,'cut':cut,'live_records':len(v),'live_pure_X_owners':185,'unfinished_columns':unfinished,
  'actual_nonzero_locality_coefficients_checked':checked,'unknown_locality_violations':bad,'nonorthogonal_clique':J,'dot_matrix':dots,
  'frozen_suffix':{'direct_rank7_Y_MOVEs':52,'CLEAR':185},'whole_moment':record(q),'necessary_allowance':record(allow),
  'remaining_room':record((allow[0]-q[1],allow[1]-q[0])),'minimum_future_owned_descents':7,
  'optimistic_completed_profile_floor':fp,'optimistic_completed_moment_floor':record(floor),
  'floor_excess_over_allowance':record((floor[0]-allow[1],floor[1]-allow[0])),
  'physical_controls':{'pins':pins,'nonlocal_source':{'stats':ns,'violations':nb,'one_direction_grant_restores_locality':True},
   'seven_descent_saturation':{'stats':sat,'completed_targets':66,'only_selected_clique_floor_saturated':True},
   'orthogonal_pair':{'stats':ps,'owned_descents':1,'outputs':2,'nonorthogonality_premise_essential':True}},
  'scope':'Universal finite-alphabet, fixed-width, fixed-schedule transcript proof reviewed in writing. Exact paid59 cut only; earlier source/history changes remain open. All five global foundations remain open, no kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','actual_nonzero_locality_coefficients_checked','remaining_room','optimistic_completed_moment_floor','floor_excess_over_allowance']},indent=2))
if __name__=='__main__':main()
