#!/usr/bin/env python3
import argparse,json,hashlib,copy
from pathlib import Path
from collections import Counter
from field import invert,binary_matrix,restore_adds,mul
from choose_basis import choose_basis
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();root=Path(__file__).parent;raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];geo=json.loads((root/'GEOMETRY.json').read_text());targets=[3,76];assert geo['receivers']==targets;dot=lambda a,b:sum(x*y for x,y in zip(a,b));K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];basis=[0,1,2,4,8,9,14,30,59];M=[[1,1,1,1],[0,1,2,3]]
charts={'Hub':{'kind':'span','rows':[[int(i==j)for i in range(8)]for j in range(8)]},'zero':{'kind':'span','rows':[]},'CC':{'kind':'ann','rows':[R[3],R[76]]}}
for j,r in enumerate(R):charts[f'L{j}']={'kind':'span','rows':[r]};charts[f'F{j}']={'kind':'ann','rows':[r]}
common=[j for j in range(111)if dot(R[3],R[j])==dot(R[76],R[j])==0];assert common==geo['common_roles']and len(common)==36;private={};assigned={};restores={};members={};pivots={}
for d in geo['private_data']:
 i=d['receiver'];other=d['other'];roles=[j for j in range(111)if j!=i and dot(R[i],R[j])==0 and dot(R[other],R[j])!=0];assert roles==d['private_roles'];private[i]=roles
 for t,q in enumerate(d['normals']):charts[f'C{i}_{t}']={'kind':'ann','rows':[R[i],q]};members[i,t]=[]
 special=dict(zip(d['pivot_roles'],d['pivot_selected_pairs']))
 for j in roles:
  avail=[t for t,q in enumerate(d['normals'])if dot(R[j],q)==0];assert len(avail)>=2;ts=special[j]if j in special else avail[:2];assert set(ts)<=set(avail);assigned[j]=(i,ts);A=[[M[r][t]for t in ts]for r in range(2)];restores[j]=restore_adds(binary_matrix(invert(A,2,7),2,7))
  for slot,t in enumerate(ts):members[i,t].append((j,slot))
 for t in range(4):pivots[i,t]=next((j,s)for j,s in members[i,t]if j in special)
assert set(private[3]).isdisjoint(private[76]);assert len(private[3])==22 and len(private[76])==24
fieldrec=lambda j,s,k:f'X{j}_{2*s+k}';ops=[['INIT',f'A{k}','CC']for k in range(4)]
for j in range(111):
 if j in common:
  for k in range(4):ops += [['MOVE',f'X{j}_{k}','CC'],['ADD',f'X{j}_{k}',f'A{k}'],['MOVE',f'X{j}_{k}','Hub']]
 elif j in assigned:
  i,ts=assigned[j]
  for x,y in reversed(restores[j]):ops.append(['ADD',f'X{j}_{x}',f'X{j}_{y}'])
  for slot,t in enumerate(ts):ops += [['MOVE',fieldrec(j,slot,k),f'C{i}_{t}']for k in range(2)]
 else:ops += [['MOVE',f'X{j}_{k}','Hub']for k in range(4)]
for (i,t),items in members.items():
 pj,ps=pivots[i,t]
 for j,s in items:
  if(j,s)==(pj,ps):continue
  for k in range(2):ops += [['ADD',fieldrec(j,s,k),fieldrec(pj,ps,k)],['MOVE',fieldrec(j,s,k),'Hub']]
marks={'joint_source_aggregate_cut':len(ops)}
X=[f'X{j}_{k}'for j in range(111)for k in range(4)];val={n:1<<i for i,n in enumerate(X)};dual=val.copy();loc={n:f'L{i//4}'for i,n in enumerate(X)}
for o in ops:
 if o[0]=='MOVE'and o[1]in val:loc[o[1]]=o[2]
 elif o[0]=='ADD'and o[1]in val and o[2]in val:val[o[2]]^=val[o[1]];dual[o[1]]^=dual[o[2]]
held=[n for n in X if loc[n]!='Hub'];assert len(held)==16 and {int(n.split('_')[0][1:])for n in held}=={1,4,60,64}
canonical,proj,selection=choose_basis(K,basis,dual,X,held);assert proj==[1<<j for j in range(16)]+[0]*20
seedmeta=[]
for q,row in enumerate(canonical):
 n=f'P{q}';coeff=[x for x in X if(row&dual[x]).bit_count()%2];hub=[x for x in coeff if loc[x]=='Hub'];missing=[held.index(x)for x in coeff if loc[x]!='Hub'];assert len(missing)<=1;ops.append(['INIT',n,'Hub']);ops += [['ADD',x,n]for x in hub]
 if missing:
  src=held[missing[0]];ops += [['MOVE',n,loc[src]],['ADD',src,n],['MOVE',n,'zero']]
 else:ops.append(['MOVE',n,'zero'])
 seedmeta.append({'packet':n,'canonical_row_hex':hex(row),'Hub_reads':hub,'direct_original_reads':[held[t]for t in missing],'held_projection_hex':hex(proj[q])})
marks['canonical36_at_ground_before_all_Y_moves']=len(ops)
B={}
for q,row in enumerate(canonical):
 v=row;c=1<<q
 while v:
  p=v.bit_length()-1
  if p in B:v^=B[p][0];c^=B[p][1]
  else:B[p]=(v,c);break
assert len(B)==36;preloads=[]
for i in targets:
 for k in range(4):
  v=sum(1<<(4*j+k)for j in range(111)if K[i]>>j&1);c=0
  while v:
   p=v.bit_length()-1;v^=B[p][0];c^=B[p][1]
  ns=[q for q in range(36)if c>>q&1];ops += [['ADD',f'P{q}',f'Y{i}_{k}']for q in ns];preloads.append({'receiver':i,'copy':k,'principal_indices':ns})
 for k in range(4):ops += [['MOVE',f'Y{i}_{k}','CC'],['ADD',f'A{k}',f'Y{i}_{k}'],['MOVE',f'Y{i}_{k}',f'F{i}']]
 for t in range(4):
  pj,ps=pivots[i,t];ops += [['MOVE',fieldrec(pj,ps,k),f'F{i}']for k in range(2)]
  for row in range(2):
   for src in range(2):
    z=mul(M[row][t],1<<src,2,7)
    for dst in range(2):
     if z>>dst&1:ops.append(['ADD',fieldrec(pj,ps,src),f'Y{i}_{2*row+dst}'])
  ops += [['MOVE',fieldrec(pj,ps,k),'Hub']for k in range(2)]
 marks[f'actual_receiver_{i}_completed']=len(ops)
for (i,t),items in members.items():
 pj,ps=pivots[i,t]
 for j,s in items:
  if(j,s)==(pj,ps):continue
  for k in range(2):ops.append(['ADD',fieldrec(j,s,k),fieldrec(pj,ps,k)])
for j,restore in restores.items():
 for x,y in restore:ops.append(['ADD',f'X{j}_{x}',f'X{j}_{y}'])
marks['all_X_restored']=len(ops)
ops += [['MOVE',f'Y{i}_{k}',f'F{i}']for i in range(111)if i not in targets for k in range(4)];ops += [['CLEAR',n]for n in [f'A{k}'for k in range(4)]+[f'P{q}'for q in range(36)]]
out={'schema':'joint-two-receiver-shared-facet-MDS-v1','native_sha256':hashlib.sha256(raw).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'completed_native_roles':targets,'physical_binary_copies':4,'common_roles':common,'private_roles':private,'private_assignments':assigned,'private_pivots':{f'{i}:{t}':list(z)for(i,t),z in pivots.items()},'canonical_seeds':seedmeta,'canonical_basis_selection':selection,'canonical_preload_witnesses':preloads,'direct_query_originals':held,'geometry_sha256':hashlib.sha256((root/'GEOMETRY.json').read_bytes()).hexdigest(),'actual_ground_information_rank':36,'new_complete_kappa':False};(root/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(Counter(o[0]for o in ops)),selection,'Ypreloads',sum(len(r['principal_indices'])for r in preloads))
