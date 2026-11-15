#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
from functools import lru_cache
import argparse,json,hashlib,copy
import sympy as sp
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b));K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)]
def rank(rows):
 B={}
 for v in rows:
  while v:
   q=v.bit_length()-1
   if q in B:v^=B[q]
   else:B[q]=v;break
 return len(B)
def replay(w,marks=True):
 charts={}
 for n,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);charts[n]=tuple(tuple(v)for v in(M.rowspace()if c['kind']=='span'else M.nullspace()))
 @lru_cache(None)
 def sub(x,y):return(sp.Matrix(charts[x]+charts[y]).rank()if charts[x]+charts[y]else 0)==len(charts[y])
 assert len(charts['I'])==5 and sub('I','C2')and sub('I','C3')
 for j,r in enumerate(R):assert charts[f'L{j}']==tuple(tuple(v)for v in sp.Matrix([r]).rowspace());assert charts[f'F{j}']==tuple(tuple(v)for v in sp.Matrix([r]).nullspace())
 X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];v={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{i//4}'for i,n in enumerate(X)}|{n:'zero'for n in Y};owners=set();born=set();counts=Counter();profile=Counter();dirty=0;events={};transport=[];allP=[];seedrows=[];fullC=[sum(1<<(4*j+k)for j in range(111)if K[i]>>j&1)for i in range(111)for k in range(4)]
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
   if label in ['cached_source_aggregate_cut','four_actual_proper_imports_at_I','actual_canonical36_at_ground_with_D4_retained_at_I']:
    assert held==['X1_2','X1_3','X2_2','X2_3'];assert rank(H)==440 and event['canonical_Hub_intersection']==32
    assert all(v[n]==1<<(444+i)and loc[n]=='zero'for i,n in enumerate(Y))
   if label=='four_actual_proper_imports_at_I':
    for z,src in enumerate(w['proper_import_originals']):assert loc[f'D{z}']=='I'and v[f'D{z}']==v[src]
   if label=='actual_canonical36_at_ground_with_D4_retained_at_I':
    for q,i in enumerate(w['canonical_basis_roles']):
     for k in range(4):assert loc[f'P{q}_{k}']=='zero'and v[f'P{q}_{k}']==sum(1<<(4*j+k)for j in range(111)if K[i]>>j&1)
    G=[v[f'P{q}_{k}']for q in range(9)for k in range(4)];D=[v[f'D{z}']for z in range(4)];assert rank(G)==36 and rank(G+D)==40;assert rank(seedrows)==36 and rank(transport)==40;event.update(ground_canonical_rank=36,completed_Hub_seed_rank=36,completed_seed_and_transport_rank=40,canonical_plus_retained_proper_D_rank=40,all_partial_Hub_seed_and_transport_history_rank=rank(allP))
   if label=='original_local_correction_completed_sources_not_yet_restored':
    for k in range(4):assert v[f'Y3_{k}']==(1<<(444+12+k))^(1<<(12+k))
    event['four_actual_Y3_targets_completed']=True
   events[label]=event
 assert not owners
 for j in range(111):
  for k in range(4):assert v[f'X{j}_{k}']==1<<(4*j+k)and loc[f'X{j}_{k}']=='Hub';assert v[f'Y{j}_{k}']==((1<<(444+4*j+k))^((1<<(4*j+k))if j==3 else 0))and loc[f'Y{j}_{k}']==f'F{j}'
 assert counts==Counter({'INIT':44,'ADD':4181,'MOVE':1204,'CLEAR':44})and dirty==44;assert dict(profile)=={1:16,2:228,3:36,5:268,6:4,7:652}
 return {'status':'PASS_CACHED_MDS_CANONICAL_EARLY_SOURCE','columns':888,'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'dirty_clears':dirty,'events':events,'completed_native_roles':[3],'physical_copies':4,'all_partial_Hub_seed_and_transport_history_rank':rank(allP),'completed_seed_and_transport_history_rank':rank(transport),'new_complete_kappa':False}
p=Path(__file__).parent;w=json.loads((p/'WORD.json').read_text());r=replay(w);tests=[('omit_anchor_capture',lambda o:o[0]=='ADD'and o[2]=='A0_0'),('omit_D_capture',lambda o:o==['ADD','X1_2','D0']),('omit_D_descent',lambda o:o==['MOVE','D0','I']),('omit_packet_patch',lambda o:o[0]=='ADD'and o[1]=='D0'and o[2].startswith('P')),('omit_ground_preload',lambda o:o==['ADD','P0_0','Y3_0']),('omit_anchor_read',lambda o:o==['ADD','A0_0','Y3_0']),('omit_inverse',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X')),('omit_D_retirement',lambda o:o==['CLEAR','D0'])];controls=[]
for name,pred in tests:
 bad=copy.deepcopy(w);ids=[i for i,o in enumerate(bad['operations'])if pred(o)];bad['operations'].pop(ids[-1]if name=='omit_inverse'else ids[0])
 try:replay(bad,marks=False)
 except(AssertionError,KeyError)as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
 else:raise AssertionError(name)
r['negative_controls']=controls;r['word_sha256']=hashlib.sha256((p/'WORD.json').read_bytes()).hexdigest();(p/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['counts'],r['movement_profile'],'transport',r['completed_seed_and_transport_history_rank'],'allprefix',r['all_partial_Hub_seed_and_transport_history_rank'],len(controls))
