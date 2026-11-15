#!/usr/bin/env python3
"""Four proper-chart local correction with four separately paid binary copies."""
import json,argparse,hashlib
from pathlib import Path
from collections import Counter
from field import mul,invert,binary_matrix,restore_adds
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'four-chart-word');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);nb=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(nb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(nb)['native_roots'];i=3;qs=[76,81,91,96];d=2;mod=7;b=2;n=4;copies=4;D=[[1,1,1,1],[0,1,2,3]];dot=lambda x,y:sum(a*b for a,b in zip(x,y));foreign=[j for j in range(111)if j!=i and dot(R[i],R[j])==0];assert len(foreign)==58
assigned={};restore={};members={t:[]for t in range(4)}
for j in foreign:
 avail=[t for t,q in enumerate(qs)if dot(R[j],R[q])==0];assert len(avail)>=2;chosen=avail[:2];assigned[j]=chosen;E=[[D[r][t]for t in chosen]for r in range(2)];restore[j]=restore_adds(binary_matrix(invert(E,d,mod),d,mod))
 for slot,t in enumerate(chosen):members[t].append((j,slot))
assert all(members.values());pivots={t:members[t][0]for t in members};DA=[[D[r][t]for t in range(2)]for r in range(2)];y_restore=restore_adds(binary_matrix(invert(DA,d,mod),d,mod))
charts={'Hub':{'kind':'span','rows':[[int(k==l)for l in range(8)]for k in range(8)]},'zero':{'kind':'span','rows':[]}}
for j,r in enumerate(R):charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
for t,q in enumerate(qs):charts[f'C{t}']={'kind':'ann','rows':[R[i],R[q]]}
ops=[];milestones={};fieldrecord=lambda j,s,k:f'X{j}_{2*s+k}'
for j in range(111):
 if j not in assigned:
  ops += [['MOVE',f'X{j}_{k}','Hub']for k in range(4)];continue
 for x,y in reversed(restore[j]):ops.append(['ADD',f'X{j}_{x}',f'X{j}_{y}'])
 for slot,t in enumerate(assigned[j]):ops += [['MOVE',fieldrecord(j,slot,k),f'C{t}']for k in range(2)]
for t,items in members.items():
 pj,ps=pivots[t]
 for j,s in items[1:]:
  for k in range(2):ops.append(['ADD',fieldrecord(j,s,k),fieldrecord(pj,ps,k)])
 for j,s in items[1:]:ops += [['MOVE',fieldrecord(j,s,k),'Hub']for k in range(2)]
milestones['all_chart_aggregates_formed']=len(ops)
for x,y in reversed(y_restore):ops.append(['ADD',f'Y{i}_{x}',f'Y{i}_{y}'])
for t in range(2):
 pj,ps=pivots[t]
 for k in range(2):
  y=f'Y{i}_{2*t+k}';ops += [['MOVE',y,f'C{t}'],['ADD',fieldrecord(pj,ps,k),y],['MOVE',y,f'F{i}'],['MOVE',fieldrecord(pj,ps,k),'Hub']]
for x,y in y_restore:ops.append(['ADD',f'Y{i}_{x}',f'Y{i}_{y}'])
for t in range(2,4):
 pj,ps=pivots[t]
 for k in range(2):ops.append(['MOVE',fieldrecord(pj,ps,k),f'F{i}'])
 for row in range(2):
  for src in range(2):
   v=mul(D[row][t],1<<src,d,mod)
   for dst in range(2):
    if v>>dst&1:ops.append(['ADD',fieldrecord(pj,ps,src),f'Y{i}_{2*row+dst}'])
 for k in range(2):ops.append(['MOVE',fieldrecord(pj,ps,k),'Hub'])
milestones['local_correction_completed_sources_not_yet_restored']=len(ops)
for t,items in members.items():
 pj,ps=pivots[t]
 for j,s in items[1:]:
  for k in range(2):ops.append(['ADD',fieldrecord(j,s,k),fieldrecord(pj,ps,k)])
for j in foreign:
 for x,y in restore[j]:ops.append(['ADD',f'X{j}_{x}',f'X{j}_{y}'])
milestones['all_original_sources_restored']=len(ops)
for j in range(111):
 if j!=i:ops += [['MOVE',f'Y{j}_{k}',f'F{j}']for k in range(4)]
w={'schema':'shared-facet-four-chart-correction-v1','native_sha256':hashlib.sha256(nb).hexdigest(),'physical_binary_copies':4,'algebraic_field':'GF4=F2[t]/(t^2+t+1)','algebraic_output_banks':2,'algebraic_chart_channels':4,'receiver':i,'chart_normal_native_indices':qs,'charts':charts,'foreign_indices':foreign,'decoder_matrix':D,'source_assignments':assigned,'pivot_originals':pivots,'milestones':milestones,'operations':ops,'expected_local_map':'Y3_k -> Y3_k + sum(Xj_k for j orthogonal to r3), all original X restored and other Y unchanged','canonical_preload_or_multiplication_admission':False,'new_complete_kappa':False}
(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(dict(Counter(o[0]for o in ops)),len(ops),len(foreign),pivots)
