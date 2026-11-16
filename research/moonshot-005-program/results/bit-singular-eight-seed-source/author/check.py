#!/usr/bin/env python3
"""Exact 222-column replay and actual chronological inventory of the two funnels."""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import argparse,json,hashlib,copy
import sympy as sp

def basis(rows):
 B={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;break
 return list(B.values())
def rank(rows):return len(basis(rows))
def intersection_dimension(A,B):return rank(A)+rank(B)-rank(A+B)
def replay(w,R,marks=True):
 dot=lambda a,b:sum(x*y for x,y in zip(a,b));h=[int((i!=72 and dot(R[72],r)!=0)^(dot([0,0,1,1,0,0,1,-1],r)!=0))for i,r in enumerate(R)];assert h==w['singular_h'];K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];A=[row&sum(1<<j for j in range(111)if h[i]==h[j])for i,row in enumerate(K)];assert rank(K)==9 and rank(A)==15;S=[A[i]for i in w['seed_basis_native_rows']];assert rank(S)==8 and S==[int(v,16)for v in w['seed_rows_hex']]
 chart={}
 for name,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);b=M.rowspace()if c['kind']=='span'else M.nullspace();chart[name]=tuple(tuple(v)for v in b)
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(chart[a]+chart[b]).rank()if chart[a]+chart[b]else 0)==len(chart[b])
 @lru_cache(None)
 def same(a,b):return sub(a,b)and sub(b,a)
 assert len(chart['Hub'])==8 and len(chart['zero'])==0 and len(chart['M0'])==6 and len(chart['M1'])==5
 for j in range(111):
  assert chart[f'L{j}']==tuple(tuple(v)for v in sp.Matrix([R[j]]).rowspace());assert chart[f'F{j}']==tuple(tuple(v)for v in sp.Matrix([R[j]]).nullspace())
 T=w['targets'];pivots={int(i):j for i,j in w['singleton_pivots'].items()};points=w['point_targets'];active={int(b):v for b,v in w['active_targets'].items()};private={int(i):v for i,v in w['private_roles'].items()};assert sorted(pivots.values())==points
 assert set(points).isdisjoint(pivots)and set(points)|set(pivots)==set(T)
 for b,ii in active.items():assert all(h[i]==b and sub(f'M{b}',f'F{i}')for i in ii)
 for c in w['cohorts']:
  actual=[j for j in range(111)if h[j]==c['h']and[i for i in active[c['h']]if dot(R[i],R[j])==0]==c['receivers']];assert actual==c['roles']
 X=[f'X{j}'for j in range(111)];Y=[f'Y{j}'for j in range(111)];val={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{j}'for j,n in enumerate(X)}|{n:'zero'for n in Y};live=set();born=set();profile=Counter();counts=Counter();dirty=0;events={};acquisition={};last_write={n:0 for n in val};peak=0
 def inventory(step):
  names=sorted([n for n in val if(n in live or(n.startswith('X')and loc[n]!='Hub'))]);groups={'ground':[n for n in names if same(loc[n],'zero')],'cache':[c['name']for c in w['cache_metadata']if c['name']in val],'held_X':[n for n in names if n.startswith('X')]};vv=[val[n]for n in names];out={'step':step,'fields':{n:{'chart':loc[n],'chart_dimension':len(chart[loc[n]]),'row_hex':hex(val[n]),'last_write_step':last_write[n]}for n in names},'groups':groups,'inventory_rank':rank(vv),'W15_intersection_dimension':intersection_dimension(A,vv),'W15_quotient_deficiency':15-intersection_dimension(A,vv),'Hub_raw_original_count':sum(loc[x]=='Hub'and val[x]==1<<j for j,x in enumerate(X)),'Y_nuisance_columns_retained':111}
  for g,nn in groups.items():out[g+'_rank']=rank([val[n]for n in nn]);out[g+'_W15_intersection']=intersection_dimension(A,[val[n]for n in nn])
  out['including_all_original_Y_rank']=rank(vv+[val[y]for y in Y]);out['including_all_original_Y_W15_intersection']=intersection_dimension(A,vv+[val[y]for y in Y]);assert out['including_all_original_Y_rank']==rank(vv)+111 and out['including_all_original_Y_W15_intersection']==out['W15_intersection_dimension']
  out['excluded_Hub_originals']=[j for j,x in enumerate(X)if loc[x]=='Hub'];out['nonraw_Hub_originals']={x:hex(val[x])for j,x in enumerate(X)if loc[x]=='Hub'and val[x]!=1<<j}
  return out
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o;counts[op]+=1
  if op=='INIT':
   assert n not in val and n not in born,('duplicate_birth',step,n);live.add(n);born.add(n);val[n]=0;loc[n]=q[0];peak=max(peak,len(live));last_write[n]=step;acquisition[n]={'birth_step':step,'birth_chart':q[0],'writes':[],'moves':[]}
  elif op=='ADD':
   m=q[0];assert n!=m and n in val and m in val and same(loc[n],loc[m]),('bad_ADD',step,o,loc.get(n),loc.get(m));val[m]^=val[n];last_write[m]=step
   if m in live:acquisition[m]['writes'].append({'step':step,'source':n,'source_row_hex':hex(val[n]),'result_row_hex':hex(val[m]),'chart':loc[m]})
  elif op=='MOVE':
   dst=q[0];assert n in val;assert sub(dst,loc[n])if n in live else sub(loc[n],dst),('direction',step,o,loc.get(n));d=abs(len(chart[dst])-len(chart[loc[n]]));assert d>0,('zero_MOVE',step,o);profile[d]+=1
   if n in live:acquisition[n]['moves'].append({'step':step,'from':loc[n],'to':dst,'rank':d,'row_hex':hex(val[n])})
   loc[n]=dst
  elif op=='CLEAR':
   assert n in live,('unowned_CLEAR',step,o)
   if n.startswith('P'):assert val[n]==S[int(n[1:])]and same(loc[n],'zero'),('seed_contract_at_retirement',n)
   if n.startswith('E'):assert val[n]==1<<int(n[1:]),('point_contract_at_retirement',n)
   if n.startswith('Q'):
    c=next(c for c in w['cache_metadata']if c['name']==n);assert val[n]==sum(1<<j for j in c['roles']),('cache_contract_at_retirement',n)
   acquisition[n]['clear_step']=step;acquisition[n]['clear_chart']=loc[n];acquisition[n]['clear_row_hex']=hex(val[n]);live.remove(n);dirty+=bool(val[n]);del val[n],loc[n]
  else:raise AssertionError(('unknown',op))
  if marks and step in w['milestones'].values():
   name=next(k for k,v in w['milestones'].items()if v==step);event={}
   if name in ['source_cut','seed8_before_Y']:
    assert all(val[y]==1<<(111+j)and loc[y]=='zero'for j,y in enumerate(Y)),('premature_Y',name);assert rank([val[x]for x in X])==111
    for j in range(111):
     if j in points:
      i=next(i for i,p in pivots.items()if p==j);assert loc[f'X{j}']==f'F{i}'and val[f'X{j}']==sum(1<<k for k in private[i]),('held_aggregate',j)
     else:assert loc[f'X{j}']=='Hub'and val[f'X{j}']==1<<j,('nonpivot_Hub',j)
    for c in w['cache_metadata']:assert same(loc[c['name']],f"M{c['family']}")and val[c['name']]==sum(1<<j for j in c['roles']),('cache_at_cut',c['name'])
    event=inventory(step)
   if name=='seed8_before_Y':
    for q,row in enumerate(S):assert loc[f'P{q}']=='zero'and val[f'P{q}']==row,('seed8_cut',q)
    event['ground_seed_rank']=8
   if name.startswith('completed_'):
    i=int(name.split('_')[1]);assert i in T and val[f'Y{i}']==(1<<(111+i))^(1<<i)and loc[f'Y{i}']==f'F{i}',('endpoint',name);event=inventory(step);event['actual_endpoint']=i
   if name=='all_X_restored':
    assert all(val[f'X{j}']==1<<j and loc[f'X{j}']=='Hub'for j in range(111));event=inventory(step)
   events[name]=event
 assert not live,('owned_lifetime',live)
 for j in range(111):
  assert val[f'X{j}']==1<<j and loc[f'X{j}']=='Hub',('X_restore',j);assert val[f'Y{j}']==(1<<(111+j))^((1<<j)if j in T else 0)and loc[f'Y{j}']==f'F{j}',('Y_endpoint',j)
 return {'status':'PASS_ACTUAL_SINGULAR_TWO_FUNNEL_SOURCE','targets':T,'columns':222,'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'peak_owners':peak,'dirty_clears':dirty,'events':events,'acquisition_history':acquisition,'new_complete_kappa':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads((a.out/'WORD.json').read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];ans=replay(w,R);tests=[]
 def delete_one(name,pred,last=False):
  ids=[j for j,o in enumerate(w['operations'])if pred(o)];assert ids,('missing_control',name);bad=copy.deepcopy(w);bad['operations'].pop(ids[-1]if last else ids[0]);tests.append((name,bad))
 delete_one('omit_early_point_capture',lambda o:o==['ADD','X1','E1'])
 delete_one('omit_early_point_arrival',lambda o:o==['MOVE','E1','zero'])
 delete_one('omit_actual_cache_capture',lambda o:o[0]=='ADD'and o[2]=='Q0')
 delete_one('omit_cache_descent',lambda o:o[0]=='MOVE'and o[1].startswith('Q'))
 delete_one('omit_true_Hub_seed',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2]=='P0')
 delete_one('omit_point_grant_seed_correction',lambda o:o[0]=='ADD'and o[1].startswith('E')and o[2].startswith('P'))
 delete_one('omit_principal_ground_arrival',lambda o:o==['MOVE','P0','zero'])
 for i in w['point_targets']:delete_one(f'omit_point_output_{i}',lambda o,i=i:o==['ADD',f'E{i}',f'Y{i}'])
 for i in [j for ii in w['active_targets'].values()for j in ii]:delete_one(f'omit_actual_funnel_read_{i}',lambda o,i=i:o[0]=='ADD'and o[1].startswith('Q')and o[2]==f'Y{i}')
 delete_one('omit_private_aggregate_delivery',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('Y'))
 delete_one('omit_private_aggregate_restoration',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'),last=True)
 delete_one('omit_owner_retirement',lambda o:o==['CLEAR','P0'])
 bad=copy.deepcopy(w);idx=next(i for i,o in enumerate(bad['operations'])if o==['INIT','E1','L1']);bad['operations'][idx][2]='Hub';tests.append(('false_Hub_point_birth',bad))
 bad=copy.deepcopy(w);idx=next(i for i,o in enumerate(bad['operations'])if o[0]=='ADD'and o[1].startswith('E')and o[2].startswith('P'));bad['operations'][idx][1]='X'+bad['operations'][idx][1][1:];tests.append(('false_Hub_availability_of_held_pivot',bad))
 controls=[]
 for label,bad in tests:
  try:replay(bad,R,marks=False)
  except(AssertionError,KeyError,ValueError)as e:controls.append({'name':label,'rejected':True,'reason':str(e)})
  else:raise AssertionError(('surviving_mutant',label))
 ans['semantic_negative_controls']=controls;ans['word_sha256']=hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest();(a.out/'RESULT.json').write_text(json.dumps({k:v for k,v in ans.items()if k not in ['events','acquisition_history']},indent=2)+'\n');(a.out/'INVENTORY.json').write_text(json.dumps(ans['events'],indent=2)+'\n');(a.out/'ACQUISITION-HISTORY.json').write_text(json.dumps(ans['acquisition_history'],indent=2)+'\n');print(json.dumps({k:v for k,v in ans.items()if k not in ['events','acquisition_history','semantic_negative_controls']}));print('negative_controls',len(controls));print('cuts',{k:(v.get('inventory_rank'),v.get('W15_intersection_dimension'),v.get('W15_quotient_deficiency'))for k,v in ans['events'].items()})
if __name__=='__main__':main()
