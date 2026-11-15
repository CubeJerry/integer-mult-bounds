#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json,hashlib,argparse,copy
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--local',type=Path,default=Path(__file__).parent.parent/'shared-facet-coding/four-chart-word/WORD.json');a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];localraw=a.local.read_bytes();assert hashlib.sha256(localraw).hexdigest()=='831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa';w=json.loads(localraw);dot=lambda x,y:sum(a*b for a,b in zip(x,y));K=[sum(1<<j for j in range(111)if j==i or dot(R[i],R[j])==0)for i in range(111)];basis=[0,1,2,4,8,9,14,30,59];assert K[3]==K[0]^K[1]^K[2]
charts=copy.deepcopy(w['charts']);charts['I']={'kind':'ann','rows':[R[3],R[91],R[96]]}
ops=[['INIT',f'A{t}_{k}',f'C{t}']for t in range(2)for k in range(2)];ypre=[];ymove=[];cut=w['milestones']['all_chart_aggregates_formed']
for o in w['operations'][:cut]:
 if o[0]=='ADD'and o[1].startswith('Y')and o[2].startswith('Y'):ypre.append(o)
 elif o[0]=='MOVE'and o[1].startswith('Y'):ymove.append(o)
 elif o[0]=='ADD'and o[2].startswith('Y'):
  k=int(o[2].split('_')[1]);ops.append(['ADD',o[1],f'A{k//2}_{k%2}'])
 else:ops.append(o)
marks={'cached_source_aggregate_cut':len(ops)}
X=[f'X{j}_{k}'for j in range(111)for k in range(4)];val={n:1<<i for i,n in enumerate(X)};dual=val.copy();loc={n:f'L{i//4}'for i,n in enumerate(X)}
for o in ops:
 if o[0]=='MOVE'and o[1]in val:loc[o[1]]=o[2]
 elif o[0]=='ADD'and o[1]in val and o[2]in val:val[o[2]]^=val[o[1]];dual[o[1]]^=dual[o[2]]
held=[n for n in X if loc[n]!='Hub'];assert held==['X1_2','X1_3','X2_2','X2_3'];Dnames=[]
for z,n in enumerate(held):
 dn=f'D{z}';Dnames.append(dn);ops += [['INIT',dn,loc[n]],['ADD',n,dn],['MOVE',dn,'I']]
marks['four_actual_proper_imports_at_I']=len(ops)
seedmeta=[]
for q,i in enumerate(basis):
 for k in range(4):
  row=sum(1<<(4*j+k)for j in range(111)if K[i]>>j&1);n=f'P{q}_{k}';coeff=[x for x in X if(row&dual[x]).bit_count()%2];hub=[x for x in coeff if loc[x]=='Hub'];missing=[held.index(x)for x in coeff if loc[x]!='Hub'];ops.append(['INIT',n,'Hub']);ops += [['ADD',x,n]for x in hub];ops.append(['MOVE',n,'I']);ops += [['ADD',f'D{z}',n]for z in missing];ops.append(['MOVE',n,'zero']);seedmeta.append({'packet':n,'canonical_role':i,'copy':k,'Hub_reads':hub,'proper_import_reads':missing,'canonical_row_hex':hex(row)})
marks['actual_canonical36_at_ground_with_D4_retained_at_I']=len(ops)
for k in range(4):ops += [['ADD',f'P{q}_{k}',f'Y3_{k}']for q in range(3)]
ops += ypre+ymove
for t in range(2):
 for k in range(2):ops.append(['ADD',f'A{t}_{k}',f'Y3_{2*t+k}'])
marks['canonical_preload_and_anchor_reads_completed']=len(ops)
oldstart=len(ops);ops += w['operations'][cut:]
for label,pos in w['milestones'].items():
 if pos>cut:marks['original_'+label]=oldstart+pos-cut
owners=[f'A{t}_{k}'for t in range(2)for k in range(2)]+Dnames+[f'P{q}_{k}'for q in range(9)for k in range(4)];ops += [['CLEAR',n]for n in owners]
out={'schema':'cached-MDS-canonical-source-v1-proper-patch','native_sha256':hashlib.sha256(raw).hexdigest(),'local_word_sha256':hashlib.sha256(localraw).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'source_assignments':w['source_assignments'],'foreign_indices':w['foreign_indices'],'pivot_originals':w['pivot_originals'],'chart_normal_native_indices':w['chart_normal_native_indices'],'canonical_basis_roles':basis,'canonical_seeds':seedmeta,'proper_import_originals':held,'physical_binary_copies':4,'actual_ground_information_rank':36,'completed_seed_and_transport_history_rank':40,'literal_principal_history_including_partial_Hub_formation_rank':444,'completed_native_roles':[3],'new_complete_kappa':False};p=Path(__file__).parent;(p/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(Counter(o[0]for o in ops)),len(ops),'seedADD',sum(len(x['Hub_reads'])+len(x['proper_import_reads'])for x in seedmeta))
