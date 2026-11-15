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
assert len(selected)==9;assert all((v&15).bit_count()%2==0 for v in K);assert selected[0]==0
charts={'Hub':{'kind':'span','rows':[[int(i==j)for i in range(8)]for j in range(8)]},'zero':{'kind':'span','rows':[]},'S':{'kind':'span','rows':R[:4]},'T':{'kind':'span','rows':R[1:4]}}
for i,r in enumerate(R):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
ops=[['INIT','A','T'],['INIT','B','F0']]
for j in [1,2,3]:ops += [['MOVE',f'X{j}','T'],['ADD',f'X{j}','A'],['MOVE',f'X{j}','S']]
ops += [['MOVE','X0','S']]
for j in [1,2,3]:ops += [['ADD','X0',f'X{j}'],['MOVE',f'X{j}','Hub']]
foreign=[j for j in range(111)if j!=0 and dot(R[0],R[j])==0]
for j in range(4,111):
 if j in foreign:ops += [['MOVE',f'X{j}','F0'],['ADD',f'X{j}','B'],['MOVE',f'X{j}','Hub']]
 else:ops += [['MOVE',f'X{j}','Hub']]
marks={'early_Hub_canonical_cut':len(ops)}
for q,i in enumerate(selected):
 n=f'P{q}';ops.append(['INIT',n,'Hub']);ops += [['ADD',f'X{j}',n]for j in range(1,111)if K[i]>>j&1];ops.append(['MOVE',n,'zero'])
marks['canonical_nine_fields_delivered_with_X0_held']=len(ops)
ops += [['ADD','P0','Y0'],['MOVE','Y0','T'],['ADD','A','Y0'],['MOVE','Y0','F0'],['ADD','B','Y0']]
marks['Y0_completed_with_X0_held']=len(ops)
ops += [['MOVE','X0','Hub']]+[['ADD','X0',f'X{j}']for j in [1,2,3]]
marks['all_X_restored']=len(ops)
for j in range(1,111):ops.append(['MOVE',f'Y{j}',f'F{j}'])
ops += [['CLEAR',n]for n in ['A','B']+[f'P{q}'for q in range(9)]]
w={'schema':'cached-early-Hub-canonical-source-v1','native_sha256':hashlib.sha256(raw).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'canonical_basis_roles':selected,'early_kernel_input_hex':hex(15),'source_side_rows':{'A':hex(14),'B':hex(sum(1<<j for j in foreign if j not in[1,2,3]))},'completed_targets':[0],'source_interface':'All9 canonical fields become actually available at ground while X0 remains at S; the proper T cache then completes Y0 before X0 returns. All X originals subsequently restore. Other Y values remain unchanged.','new_complete_kappa':False}
p=Path(__file__).parent;(p/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(selected,'foreign',len(foreign),'counts',dict(Counter(o[0]for o in ops)))
