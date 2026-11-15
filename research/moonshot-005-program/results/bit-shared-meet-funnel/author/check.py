#!/usr/bin/env python3
"""Exact literal replay, rational geometry and semantic mutation controls."""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import argparse,json,hashlib,copy
import sympy as sp

def rank(rows):
 B={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;break
 return len(B)

def replay(word,R,marks=True):
 chart={}
 for name,c in word['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);basis=M.rowspace()if c['kind']=='span'else M.nullspace();chart[name]=tuple(tuple(v)for v in basis)
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(chart[a]+chart[b]).rank()if chart[a]+chart[b]else 0)==len(chart[b])
 @lru_cache(None)
 def same(a,b):return sub(a,b)and sub(b,a)
 assert len(chart['Hub'])==8 and len(chart['zero'])==0 and len(chart['Meet'])==5
 dot=lambda a,b:sum(x*y for x,y in zip(a,b));T=word['targets'];fullC=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];assert rank(fullC)==9
 for j in range(111):
  assert chart[f'L{j}']==tuple(tuple(v)for v in sp.Matrix([R[j]]).rowspace());assert chart[f'F{j}']==tuple(tuple(v)for v in sp.Matrix([R[j]]).nullspace())
 assert all(sub('Meet',f'F{i}')for i in T)
 X=[f'X{j}'for j in range(111)];Y=[f'Y{j}'for j in range(111)];val={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{j}'for j,n in enumerate(X)}|{n:'zero'for n in Y};live=set();born=set();profile=Counter();counts=Counter();dirty=0;events={};history=[];peak=0
 for step,o in enumerate(word['operations']):
  op,n,*q=o;counts[op]+=1
  if op=='INIT':
   assert n not in val and n not in born,('duplicate_birth',step,n);live.add(n);born.add(n);val[n]=0;loc[n]=q[0];peak=max(peak,len(live))
  elif op=='ADD':
   m=q[0];assert n!=m and n in val and m in val and same(loc[n],loc[m]),('bad_ADD',step,o,loc.get(n),loc.get(m));val[m]^=val[n]
   if m in live:history.append(val[m])
  elif op=='MOVE':
   dst=q[0];assert n in val
   assert sub(dst,loc[n])if n in live else sub(loc[n],dst),('direction',step,o,loc.get(n))
   d=abs(len(chart[dst])-len(chart[loc[n]]));assert d>0,('zero_MOVE',step,o);profile[d]+=1;loc[n]=dst
  elif op=='CLEAR':
   assert n in live,('unowned_CLEAR',step,o);live.remove(n);dirty+=bool(val[n]);del val[n],loc[n]
  else:raise AssertionError(('unknown',op))
  if marks and step+1 in word['milestones'].values():
   name=next(k for k,v in word['milestones'].items()if v==step+1);event={}
   if name in ['source_cut','canonical9_before_Y']:
    assert all(val[y]==1<<(111+j)and loc[y]=='zero'for j,y in enumerate(Y)),('premature_Y',name)
    held=[j for j in range(111)if loc[f'X{j}']!='Hub'];assert held==word['held_originals'];assert rank([val[x]for x in X])==111
    for c in word['cache_metadata']:
     assert same(loc[c['name']],'Meet');assert val[c['name']]==sum(1<<j for j in c['roles']),('wrong_cache',c['name'])
    event.update(held_originals=held,Hub_original_rank=rank([val[x]for x in X if loc[x]=='Hub']))
   if name=='canonical9_before_Y':
    P=[val[f'P{q}']for q in range(9)];assert rank(P)==rank(P+fullC)==9
    for q,s in enumerate(word['canonical_seeds']):assert loc[f'P{q}']=='zero'and val[f'P{q}']==int(s['canonical_row_hex'],16)
    event.update(ground_canonical_rank=9,first_acquisition_history_rank=rank(history))
   if name.startswith('completed_'):
    i=int(name.split('_')[1]);assert i in T and val[f'Y{i}']==(1<<(111+i))^(1<<i)and loc[f'Y{i}']==f'F{i}',('endpoint',name);event['actual_endpoint']=True
   if name=='all_X_restored':assert all(val[f'X{j}']==1<<j and loc[f'X{j}']=='Hub'for j in range(111))
   events[name]=event
 assert not live,('owned_lifetime',live)
 for j in range(111):
  assert val[f'X{j}']==1<<j and loc[f'X{j}']=='Hub',('X_restore',j)
  assert val[f'Y{j}']==(1<<(111+j))^((1<<j)if j in T else 0)and loc[f'Y{j}']==f'F{j}',('Y_endpoint',j)
 return {'status':'PASS_ACTUAL_MEET_FUNNEL_SOURCE','targets':T,'columns':222,'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'peak_owners':peak,'dirty_clears':dirty,'events':events,'new_complete_kappa':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads((a.out/'WORD.json').read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];ans=replay(w,R)
 tests=[]
 def delete_one(name,pred,last=False):
  ids=[j for j,o in enumerate(w['operations'])if pred(o)]
  if not ids:return
  bad=copy.deepcopy(w);bad['operations'].pop(ids[-1]if last else ids[0]);tests.append((name,bad))
 delete_one('omit_actual_cache_capture',lambda o:o[0]=='ADD'and o[2]=='A0')
 delete_one('omit_cache_descent',lambda o:o[0]=='MOVE'and o[1].startswith('A')and o[2]=='Meet')
 delete_one('omit_true_Hub_seed',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2]=='P0')
 q=next(o for o in w['operations']if o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('P')and int(o[1][1:])in w['held_originals'])
 delete_one('omit_actual_held_query',lambda o:o==q)
 delete_one('omit_query_chart_visit',lambda o:o[0]=='MOVE'and o[1]==q[2]and o[2].startswith('F'))
 for i in w['targets']:
  delete_one(f'omit_funnel_read_{i}',lambda o,i=i:o[0]=='ADD'and o[1].startswith('A')and o[2]==f'Y{i}')
 delete_one('omit_singleton_delivery',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('Y'))
 delete_one('omit_pivot_restoration',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'),last=True)
 delete_one('omit_owner_retirement',lambda o:o==['CLEAR','P0'])
 delete_one('omit_early_point_capture',lambda o:o[0]=='ADD'and o[2]=='E0')
 delete_one('omit_early_ground_correction',lambda o:o[0]=='ADD'and o[1]=='E0'and o[2].startswith('P'))
 if w['early_point_helper_originals']:
  bad=copy.deepcopy(w);idx=next(i for i,o in enumerate(bad['operations'])if o[0]=='INIT'and o[1]=='E0');bad['operations'][idx][2]='Hub';tests.append(('false_free_point_source',bad))
 # Every test checks semantics without exact invoice or author milestones.
 controls=[]
 for label,bad in tests:
  try:replay(bad,R,marks=False)
  except(AssertionError,KeyError,ValueError)as e:controls.append({'name':label,'rejected':True,'reason':str(e)})
  else:raise AssertionError(('surviving_mutant',label))
 ans['semantic_negative_controls']=controls;ans['word_sha256']=hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest();(a.out/'RESULT.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps({k:v for k,v in ans.items()if k not in ['events','semantic_negative_controls']}));print('negative_controls',len(controls))
if __name__=='__main__':main()
