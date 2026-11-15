#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];B={};selected=[]
for i,row in enumerate(K):
 v=row
 while v:
  q=v.bit_length()-1
  if q in B:v^=B[q]
  else:B[q]=v;selected.append(i);break
assert len(selected)==9 and selected==[0,1,2,4,8,9,14,30,59];assert all((v&15).bit_count()%2==(v&240).bit_count()%2==0 for v in K)
charts={'Hub':{'kind':'span','rows':[[int(i==j)for i in range(8)]for j in range(8)]},'zero':{'kind':'span','rows':[]},'S0':{'kind':'span','rows':R[:4]},'T0':{'kind':'span','rows':R[1:4]},'S4':{'kind':'span','rows':R[4:8]},'T4':{'kind':'span','rows':R[5:8]},'C04':{'kind':'ann','rows':[R[0],R[4]]}}
for i,r in enumerate(R):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
ops=[['INIT',n,c]for n,c in [('A0','T0'),('A4','T4'),('G0','S0'),('G4','S4'),('Z','C04'),('B0','F0'),('B4','F4')]]
for base in [0,4]:
 for j in range(base+1,base+4):ops += [['MOVE',f'X{j}',f'T{base}'],['ADD',f'X{j}',f'A{base}'],['MOVE',f'X{j}',f'S{base}'],['ADD',f'X{j}',f'G{base}']]
 ops += [['MOVE',f'X{base}',f'S{base}'],['ADD',f'X{base}',f'G{base}']]
 for j in range(base+1,base+4):ops += [['ADD',f'X{base}',f'X{j}'],['MOVE',f'X{j}','Hub']]
classes=Counter()
for j in range(8,111):
 z0=dot(R[j],R[0])==0;z4=dot(R[j],R[4])==0;classes[str((z0,z4))]+=1
 if z0 and z4:c,n='C04','Z'
 elif z0:c,n='F0','B0'
 elif z4:c,n='F4','B4'
 else:ops.append(['MOVE',f'X{j}','Hub']);continue
 ops += [['MOVE',f'X{j}',c],['ADD',f'X{j}',n],['MOVE',f'X{j}','Hub']]
marks={'early_Hub_canonical_cut':len(ops)}
for n in ['G0','G4']:ops.append(['MOVE',n,'zero'])
for q,i in enumerate(selected):
 n=f'P{q}';ops.append(['INIT',n,'Hub']);ops += [['ADD',f'X{j}',n]for j in range(111)if j not in[0,4]and K[i]>>j&1];ops.append(['MOVE',n,'zero'])
marks['canonical_nine_and_two_paid_partial_fields_delivered']=len(ops)
for base,q,other in [(0,0,4),(4,3,0)]:ops += [['ADD',f'P{q}',f'Y{base}'],['ADD',f'G{other}',f'Y{base}'],['MOVE',f'Y{base}',f'T{base}'],['ADD',f'A{base}',f'Y{base}'],['MOVE',f'Y{base}','C04'],['ADD','Z',f'Y{base}'],['MOVE',f'Y{base}',f'F{base}'],['ADD',f'B{base}',f'Y{base}']]
marks['Y0_Y4_completed_with_two_X_held']=len(ops)
for base in [0,4]:ops += [['MOVE',f'X{base}','Hub']]+[['ADD',f'X{base}',f'X{j}']for j in range(base+1,base+4)]
marks['all_X_restored']=len(ops)
ops += [['MOVE',f'Y{j}',f'F{j}']for j in range(111)if j not in[0,4]]
ops += [['CLEAR',n]for n in ['A0','A4','G0','G4','Z','B0','B4']+[f'P{q}'for q in range(9)]]
w={'schema':'two-cohort-cached-early-Hub-source-v1','native_sha256':hashlib.sha256(raw).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'canonical_basis_roles':selected,'held_inverse_columns_hex':['0xf','0xf0'],'completed_targets':[0,4],'actual_ground_information_dimension':11,'partial_rank_four_fields':['G0','G4'],'nonaxis_classes':dict(classes),'new_complete_kappa':False};p=Path(__file__).parent;(p/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(dict(Counter(o[0]for o in ops)),classes)
