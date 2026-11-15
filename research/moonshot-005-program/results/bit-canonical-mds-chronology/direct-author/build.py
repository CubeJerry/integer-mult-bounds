#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json,hashlib,argparse,copy
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--local',type=Path,default=Path(__file__).parent.parent/'shared-facet-coding/four-chart-word/WORD.json');a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];localraw=a.local.read_bytes();assert hashlib.sha256(localraw).hexdigest()=='831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa';w=json.loads(localraw);dot=lambda x,y:sum(a*b for a,b in zip(x,y));K=[sum(1<<j for j in range(111)if j==i or dot(R[i],R[j])==0)for i in range(111)];basis=[0,1,2,4,8,9,14,30,59];assert K[3]==K[0]^K[1]^K[2]
charts=copy.deepcopy(w['charts'])
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
held=[n for n in X if loc[n]!='Hub'];assert held==['X1_2','X1_3','X2_2','X2_3']
from choose_basis import choose_basis
canonical,proj,selection=choose_basis(K,basis,dual,X,held)
assert proj==[1,2,4,8]+[0]*32
seedmeta=[]
for q,row in enumerate(canonical):
 n=f'P{q}';coeff=[x for x in X if(row&dual[x]).bit_count()%2];hub=[x for x in coeff if loc[x]=='Hub'];missing=[held.index(x)for x in coeff if loc[x]!='Hub'];assert len(missing)<=1
 ops.append(['INIT',n,'Hub']);ops += [['ADD',x,n]for x in hub]
 if missing:
  src=held[missing[0]];ops += [['MOVE',n,loc[src]],['ADD',src,n],['MOVE',n,'zero']]
 else:ops.append(['MOVE',n,'zero'])
 seedmeta.append({'packet':n,'canonical_row_hex':hex(row),'Hub_reads':hub,'direct_held_original_reads':[held[t]for t in missing],'held_projection_hex':hex(proj[q])})
marks['actual_adapted_canonical36_at_ground']=len(ops)
B={}
for q,row in enumerate(canonical):
 v=row;c=1<<q
 while v:
  p=v.bit_length()-1
  if p in B:v^=B[p][0];c^=B[p][1]
  else:B[p]=(v,c);break
assert len(B)==36
preloads=[]
for k in range(4):
 v=sum(1<<(4*j+k)for j in range(111)if K[3]>>j&1);c=0
 while v:
  p=v.bit_length()-1;v^=B[p][0];c^=B[p][1]
 ns=[q for q in range(36)if c>>q&1];ops += [['ADD',f'P{q}',f'Y3_{k}']for q in ns];preloads.append({'copy':k,'principal_indices':ns})
ops += ypre+ymove
for t in range(2):
 for k in range(2):ops.append(['ADD',f'A{t}_{k}',f'Y3_{2*t+k}'])
marks['canonical_preload_and_anchor_reads_completed']=len(ops)
oldstart=len(ops);ops += w['operations'][cut:]
for label,pos in w['milestones'].items():
 if pos>cut:marks['original_'+label]=oldstart+pos-cut
owners=[f'A{t}_{k}'for t in range(2)for k in range(2)]+[f'P{q}'for q in range(36)];ops += [['CLEAR',n]for n in owners]
out={'schema':'direct-query-adapted-canonical-MDS-source-v1','native_sha256':hashlib.sha256(raw).hexdigest(),'local_word_sha256':hashlib.sha256(localraw).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'source_assignments':w['source_assignments'],'foreign_indices':w['foreign_indices'],'pivot_originals':w['pivot_originals'],'chart_normal_native_indices':w['chart_normal_native_indices'],'predecessor_canonical_basis_roles':basis,'canonical_seeds':seedmeta,'K3_preload_witnesses':preloads,'canonical_basis_selection':selection,'direct_query_originals':held,'physical_binary_copies':4,'actual_ground_information_rank':36,'completed_seed_and_transport_history_rank':40,'literal_principal_history_including_partial_Hub_formation_rank':444,'completed_native_roles':[3],'new_complete_kappa':False};p=Path(__file__).parent;(p/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print(dict(Counter(o[0]for o in ops)),len(ops),'seedADD',sum(len(x['Hub_reads'])+len(x['direct_held_original_reads'])for x in seedmeta))
