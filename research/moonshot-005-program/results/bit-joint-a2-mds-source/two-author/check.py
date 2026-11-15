#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
from functools import lru_cache
import argparse,json,hashlib,copy
import sympy as sp
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();root=Path(__file__).parent
raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)]
def rank(rows):
 B={}
 for v in rows:
  while v:
   q=v.bit_length()-1
   if q in B:v^=B[q]
   else:B[q]=v;break
 return len(B)
def replay(w,marks=True,invoice=True):
 charts={}
 for n,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);charts[n]=tuple(tuple(v)for v in(M.rowspace()if c['kind']=='span'else M.nullspace()))
 @lru_cache(None)
 def sub(x,y):return(sp.Matrix(charts[x]+charts[y]).rank()if charts[x]+charts[y]else 0)==len(charts[y])
 for j,r in enumerate(R):assert charts[f'L{j}']==tuple(tuple(v)for v in sp.Matrix([r]).rowspace());assert charts[f'F{j}']==tuple(tuple(v)for v in sp.Matrix([r]).nullspace())
 assert len(charts['CC'])==6 and sub('CC','F3')and sub('CC','F76')
 for i in [3,76]:
  for t in range(4):assert len(charts[f'C{i}_{t}'])==6 and sub(f'C{i}_{t}',f'F{i}')
 X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];v={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{i//4}'for i,n in enumerate(X)}|{n:'zero'for n in Y};owners=set();born=set();counts=Counter();profile=Counter();dirty=0;events={};transport=[];allP=[];seedrows=[];fullC=[sum(1<<(4*j+k)for j in range(111)if K[i]>>j&1)for i in range(111)for k in range(4)]
 assert rank(fullC)==36
 common=[j for j in range(111)if dot(R[3],R[j])==dot(R[76],R[j])==0];assert len(common)==36 and common==w['common_roles'];assert dot(R[3],R[76])!=0
 for step,op in enumerate(w['operations']):
  t,n,*z=op;counts[t]+=1
  if t=='INIT':assert n not in v and n not in born;owners.add(n);born.add(n);v[n]=0;loc[n]=z[0]
  elif t=='ADD':
   m=z[0];assert n!=m and sub(loc[n],loc[m])and sub(loc[m],loc[n]);v[m]^=v[n]
   if m.startswith('P'):
    allP.append(v[m])
    if loc[m]!='Hub':transport.append(v[m])
  elif t=='MOVE':
   dest=z[0];assert sub(dest,loc[n])if n in owners else sub(loc[n],dest);r=abs(len(charts[dest])-len(charts[loc[n]]));assert r;profile[r]+=1
   if n.startswith('P'):
    transport.append(v[n]);allP.append(v[n])
    if loc[n]=='Hub':seedrows.append(v[n])
   loc[n]=dest
  elif t=='CLEAR':assert n in owners;dirty+=bool(v[n]);owners.remove(n);del v[n],loc[n]
  else:raise AssertionError(t)
  if marks and step+1 in w['milestones'].values():
   label=next(k for k,u in w['milestones'].items()if u==step+1);H=[v[n]for n in X if loc[n]=='Hub'];held=[n for n in X if loc[n]!='Hub'];event={'Hub_X_rank':rank(H),'held_original_X':held,'canonical_Hub_intersection':36+rank(H)-rank(H+fullC)}
   if label in ['joint_source_aggregate_cut','canonical36_at_ground_before_all_Y_moves']:
    assert held==[f'X{j}_{k}'for j in[1,4,60,64]for k in range(4)];assert rank(H)==428 and event['canonical_Hub_intersection']==20
    assert all(v[n]==1<<(444+i)and loc[n]=='zero'for i,n in enumerate(Y))
    for k in range(4):assert v[f'A{k}']==sum(1<<(4*j+k)for j in common)
   if label=='canonical36_at_ground_before_all_Y_moves':
    for q,entry in enumerate(w['canonical_seeds']):assert loc[f'P{q}']=='zero'and v[f'P{q}']==int(entry['canonical_row_hex'],16)
    G=[v[f'P{q}']for q in range(36)];D=[v[n]for n in w['direct_query_originals']];assert rank(G)==rank(G+fullC)==36 and rank(D)==16
    event.update(ground_canonical_rank=36,completed_Hub_seed_rank=rank(seedrows),completed_seed_and_transport_rank=rank(transport),canonical_plus_held_original_rank=rank(G+D),canonical_held_intersection=36+16-rank(G+D),all_partial_Hub_seed_and_transport_history_rank=rank(allP))
   if label.startswith('actual_receiver_'):
    i=int(label.split('_')[2]);assert i in[3,76]
    for k in range(4):assert v[f'Y{i}_{k}']==(1<<(444+4*i+k))^(1<<(4*i+k))
    event['four_actual_targets_completed']=True
   if label=='all_X_restored':assert all(v[n]==1<<j and loc[n]=='Hub'for j,n in enumerate(X))
   events[label]=event
 assert not owners
 for j in range(111):
  for k in range(4):assert v[f'X{j}_{k}']==1<<(4*j+k)and loc[f'X{j}_{k}']=='Hub';assert v[f'Y{j}_{k}']==((1<<(444+4*j+k))^((1<<(4*j+k))if j in[3,76]else 0))and loc[f'Y{j}_{k}']==f'F{j}'
 if invoice:assert counts['INIT']==counts['CLEAR']==dirty==40;assert dict(profile)=={1:40,2:328,5:328,6:24,7:552,8:20}
 return {'status':'PASS_JOINT_TWO_RECEIVER_CANONICAL_MDS_SOURCE','columns':888,'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'dirty_clears':dirty,'events':events,'completed_native_roles':[3,76],'physical_copies':4,'all_partial_Hub_seed_and_transport_history_rank':rank(allP),'completed_seed_and_transport_history_rank':rank(transport),'completed_Hub_seed_rank':rank(seedrows),'new_complete_kappa':False}
w=json.loads((root/'WORD.json').read_text());r=replay(w)
query=next(o for o in w['operations']if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('P')and o[1]in w['direct_query_originals']);querymove=next(o for o in w['operations']if o[0]=='MOVE'and o[1]==query[2]and o[2].startswith('C'))
tests=[('omit_common_capture',lambda o:o[0]=='ADD'and o[2]=='A0'),('omit_direct_original_query',lambda o:o==query),('omit_query_chart_visit',lambda o:o==querymove),('omit_new_ground_preload',lambda o:o[0]=='ADD'and o[1].startswith('P')and o[2]=='Y76_0'),('omit_common_read_first_receiver',lambda o:o==['ADD','A0','Y3_0']),('omit_common_read_second_receiver',lambda o:o==['ADD','A0','Y76_0']),('omit_private_MDS_contribution',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2]=='Y76_0'),('omit_source_inverse',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X')),('omit_owner_retirement',lambda o:o==['CLEAR','P0'])]
controls=[]
for name,pred in tests:
 bad=copy.deepcopy(w);ids=[i for i,o in enumerate(bad['operations'])if pred(o)];assert ids,name;bad['operations'].pop(ids[-1]if name=='omit_source_inverse'else ids[0])
 try:replay(bad,marks=False,invoice=False)
 except(AssertionError,KeyError)as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
 else:raise AssertionError(name)
r['negative_controls']=controls;r['word_sha256']=hashlib.sha256((root/'WORD.json').read_bytes()).hexdigest();(root/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
