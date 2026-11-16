#!/usr/bin/env python3
"""Independent paid59 locality, clique, suffix and directed descent floor."""
import argparse,copy,hashlib,itertools,json,sys
from fractions import Fraction
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','word','proof','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from review_leaf_capacity import chart_basis,echelon
from price import invoice
raw=a.word.read_bytes();pin=hashlib.sha256(raw).hexdigest();assert pin=='dd60233b57be5fdef83b86a2d2b816e665e3d939850da94b680838d1d6d178ce';w=json.loads(raw);native=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(native).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
R=json.loads(native)['native_roots'];C={n:chart_basis(c)for n,c in w['charts'].items()}
for i,r in enumerate(R):
 assert len(C[f'L{i}'])==1 and len(echelon(C[f'L{i}']+[r])[0])==1
 assert len(C[f'F{i}'])==7 and all(sum(x*y for x,y in zip(v,r))==0 for v in C[f'F{i}'])
stats=independent_replay(w);cut=w['carrier_interface_before_operation'];assert cut==1380;v,at=trace(w)[0][cut];U=sorted(set(range(111))-set(w['targets']));assert len(U)==52;xm=(1<<111)-1
originals={f'{p}{i}'for p in 'XY'for i in range(111)};owners=set(v)-originals;assert len(owners)==185 and all(v[n]>>111==0 for n in owners)
checks=0;violations=[]
for n,row in v.items():
 for j in U:
  if row>>j&1:
   checks+=1
   if len(echelon(C[at[n]]+[R[j]])[0])!=len(C[at[n]]):violations.append([n,j,at[n]])
assert not violations
for i in range(111):assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
for i in range(111):assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in w['targets']else 0)and at[f'Y{i}']==(f'F{i}'if i in w['targets']else'zero')
J=[5,35,93,96,97,109,110];assert set(J)<=set(U)
dots=[[sum(x*y for x,y in zip(R[i],R[j]))for j in J]for i in J];assert all(z!=0 for row in dots for z in row)
suffix=w['operations'][cut:];assert len(suffix)==237 and sum(o[0]=='MOVE'for o in suffix)==52 and sum(o[0]=='CLEAR'for o in suffix)==185
assert sorted(o for o in suffix if o[0]=='MOVE')==sorted([['MOVE',f'Y{i}',f'F{i}']for i in U])
price=invoice(stats['movement_profile']);profile={int(k):v for k,v in stats['movement_profile'].items()};floor=dict(profile);floor[1]=floor.get(1,0)+len(J);lower=invoice(floor)
assert Fraction(lower['moment']['lower_fraction'])>Fraction(lower['limiting_allowance']['upper_fraction'])
assert Fraction(price['limiting_room']['upper_fraction'])<3
# A real earlier owned descent creates a nonlocal source and changes the
# premise; it is not inserted for free into the admitted paid59 prefix.
control=copy.deepcopy(w);name='CONTROL_GLOBAL_X5';ops=[['INIT',name,'Hub'],['ADD','X5',name],['MOVE',name,'zero']];control['operations'][cut:cut]=ops;control['operations'].append(['CLEAR',name]);control['schema']='material-cut-locality-hypothesis-control-v1';control['carrier_interface_before_operation']=cut+3
control_stats=independent_replay(control);cv,ca=trace(control)[0][cut+3];assert cv[name]==1<<5 and ca[name]=='zero'and len(C[ca[name]])==0
a.out.mkdir(parents=True,exist_ok=True);data=(json.dumps(control,indent=2)+'\n').encode();(a.out/'NONLOCAL-SOURCE-CONTROL-WORD.json').write_bytes(data)
report={'status':'PASS_ROOT_PAID59_SEVEN_FUTURE_DESCENT_FLOOR','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'word_sha256':pin,'native_source_sha256':w['source_sha256'],'cut':cut,'completed_Y':59,'unfinished_Y':52,'all_X_raw_Hub':True,'live_pure_X_owners':185,'unknown_locality_nonzero_coefficients_checked':checks,'locality_violations':violations,'nonorthogonal_clique':J,'clique_dot_matrix':dots,'frozen_suffix':{'direct_rank7_Y_MOVEs':52,'CLEAR':185,'other_operations':0},'full_word_stats':stats,'partial_price':price,'minimum_future_owned_descents':7,'optimistic_completed_profile_floor':floor,'completed_price_floor':lower,'necessary_extra_initial_global_directions_if_future_descents_at_most2':5,'material_hypothesis_control':{'word_sha256':hashlib.sha256(data).hexdigest(),'all222_endpoints_pass':True,'actual_new_unknown_x5_at_ground':True,'extra_owned_descent_rank':7,'source_locality_premise_fails':True,'stats':control_stats},'scope':'Universal fixed-schedule transcript argument reviewed separately. This exact cut cannot be completed within the retained limiting movement budget. Earlier history/source edits and different architectures remain open; all five global foundations retained. No kappa.'}
(a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
