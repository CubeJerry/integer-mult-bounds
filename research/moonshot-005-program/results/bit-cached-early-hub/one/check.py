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
 for j,r in enumerate(R):assert charts[f'L{j}']==tuple(tuple(v)for v in sp.Matrix([r]).rowspace());assert charts[f'F{j}']==tuple(tuple(v)for v in sp.Matrix([r]).nullspace())
 v={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};owners=set();born=set();counts=Counter();profile=Counter();dirty=0;events={};D={f'X{j}':1<<j for j in range(111)}
 for step,op in enumerate(w['operations']):
  t,n,*z=op;counts[t]+=1
  if t=='INIT':assert n not in v and n not in born;owners.add(n);born.add(n);v[n]=0;loc[n]=z[0]
  elif t=='ADD':
   m=z[0];assert n!=m and sub(loc[n],loc[m])and sub(loc[m],loc[n]);v[m]^=v[n]
   if n.startswith('X')and m.startswith('X'):D[n]^=D[m]
  elif t=='MOVE':
   dest=z[0];assert sub(dest,loc[n])if n in owners else sub(loc[n],dest);r=abs(len(charts[dest])-len(charts[loc[n]]));assert r;profile[r]+=1;loc[n]=dest
  elif t=='CLEAR':assert n in owners;dirty+=bool(v[n]);owners.remove(n);del v[n],loc[n]
  else:raise AssertionError(t)
  if marks and step+1 in w['milestones'].values():
   label=next(k for k,u in w['milestones'].items()if u==step+1);H=[v[f'X{j}']for j in range(111)if loc[f'X{j}']=='Hub'];held=[j for j in range(111)if loc[f'X{j}']!='Hub'];event={'Hub_X_rank':rank(H),'held_original_X':held,'canonical_Hub_intersection':9+rank(H)-rank(H+K)}
   if label in ['early_Hub_canonical_cut','canonical_nine_fields_delivered_with_X0_held','Y0_completed_with_X0_held']:
    assert held==[0]and loc['X0']=='S';assert rank(H)==110 and rank(H+K)==110;assert D['X0']==15;assert v['A']==14;assert (v['A']&D['X0']).bit_count()%2==1;event['held_inverse_column_hex']=hex(D['X0']);event['actual_T_cache_restricted_rank']=1
   if label=='canonical_nine_fields_delivered_with_X0_held':
    for q,i in enumerate(w['canonical_basis_roles']):assert loc[f'P{q}']=='zero'and v[f'P{q}']==K[i]
    assert rank([v[f'P{q}']for q in range(9)])==9;event['nine_actual_canonical_ground_fields']=True
   if label=='Y0_completed_with_X0_held':assert v['Y0']==(1<<111)^1 and loc['Y0']=='F0';event['Y0_actual_target_completed']=True
   events[label]=event
 assert not owners
 for j in range(111):assert v[f'X{j}']==1<<j and loc[f'X{j}']=='Hub';assert v[f'Y{j}']==((1<<(111+j))^(1 if j==0 else 0))and loc[f'Y{j}']==f'F{j}'
 assert counts==Counter({'INIT':11,'ADD':594,'MOVE':292,'CLEAR':11})and dirty==11;assert dict(profile)=={2:3,1:56,3:2,4:5,6:53,7:164,8:9}
 return {'status':'PASS_LITERAL_CACHED_EARLY_HUB_SOURCE','columns':222,'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'dirty_clears':dirty,'events':events,'completed_targets':[0],'new_complete_kappa':False}
p=Path(__file__).parent;w=json.loads((p/'WORD.json').read_text());r=replay(w);tests=[('omit_axis_cache_capture',lambda o:o==['ADD','X1','A']),('omit_early_recoding',lambda o:o==['ADD','X0','X1']),('omit_canonical_seed_term',lambda o:o==['ADD','X1','P0']),('omit_proper_cache_read',lambda o:o==['ADD','A','Y0']),('omit_full_facet_cache_read',lambda o:o==['ADD','B','Y0']),('omit_restoration',lambda o:o==['ADD','X0','X1']),('omit_cache_retirement',lambda o:o==['CLEAR','A'])];controls=[]
for name,pred in tests:
 bad=copy.deepcopy(w);ids=[i for i,o in enumerate(bad['operations'])if pred(o)];idx=ids[-1]if name=='omit_restoration'else ids[0];bad['operations'].pop(idx)
 try:replay(bad,marks=False)
 except(AssertionError,KeyError)as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
 else:raise AssertionError(name)
r['negative_controls']=controls;r['word_sha256']=hashlib.sha256((p/'WORD.json').read_bytes()).hexdigest();(p/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['counts'],r['movement_profile'],'mutants',len(controls))
