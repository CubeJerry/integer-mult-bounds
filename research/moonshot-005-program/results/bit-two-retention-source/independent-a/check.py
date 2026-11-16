#!/usr/bin/env python3
"""Independent all-column literal replay of the actual donor forks."""
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
def replay(w,R,marks=True):
 dot=lambda a,b:sum(x*y for x,y in zip(a,b));h=[int((i!=72 and dot(R[72],r)!=0)^(dot([0,0,1,1,0,0,1,-1],r)!=0))for i,r in enumerate(R)];assert h==w['singular_h'];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];S=[int(v,16)for v in w['seed_rows_hex']];K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];G=[int(v,16)for v in w['canonical_innovations_hex']];S0=[A[i]for i in [3,76,80,4,74,78]]+G;assert rank(A)==15 and rank(K)==9 and rank(K+G)==9 and rank(S)==rank(S0)==8 and rank(S0+K)==12 and rank(S0+A)==16
 chart={}
 for name,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);b=M.rowspace()if c['kind']=='span'else M.nullspace();chart[name]=tuple(tuple(v)for v in b)
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(chart[a]+chart[b]).rank()if chart[a]+chart[b]else 0)==len(chart[b])
 @lru_cache(None)
 def same(a,b):return sub(a,b)and sub(b,a)
 assert len(chart['Hub'])==8 and len(chart['zero'])==0 and len(chart['M0'])==5 and len(chart['M1'])==5
 for j in range(111):assert chart[f'L{j}']==tuple(tuple(v)for v in sp.Matrix([R[j]]).rowspace())and chart[f'F{j}']==tuple(tuple(v)for v in sp.Matrix([R[j]]).nullspace())
 for f in w['forks']:
  i,q,d,p,G,D=[f[k]for k in ['old_receiver','new_receiver','donor','carrier','group','chart']];assert A[i]==A[q];actual=[j for j in range(111)if h[j]==0 and[k for k in [3,76,80]if dot(R[k],R[j])==0]==[i]and j!=q];assert actual==G and d in G and p in G and d!=p;assert len(chart[D])==6 and sub(D,f'F{i}')and sub(D,f'F{q}');assert sub('M0',D)
 for c in w['cache_metadata']:
  act=[3,76,80]if c['family']==0 else[4,74,78];assert c['roles']==[j for j in range(111)if h[j]==c['family']and[i for i in act if dot(R[i],R[j])==0]==c['receivers']]
 X=[f'X{j}'for j in range(111)];Y=[f'Y{j}'for j in range(111)];val={n:1<<i for i,n in enumerate(X+Y)};loc={n:f'L{j}'for j,n in enumerate(X)}|{n:'zero'for n in Y};live=set();born=set();profile=Counter();counts=Counter();dirty=0;peak=0;events={};history=[]
 def inventory(step):
  nn=[n for n in val if n in live or(n.startswith('X')and loc[n]!='Hub')];vv=[val[n]for n in nn];inter=15+rank(vv)-rank(A+vv);return {'step':step,'fields':{n:{'chart':loc[n],'row_hex':hex(val[n])}for n in nn},'inventory_rank':rank(vv),'W15_intersection_dimension':inter,'W15_quotient_deficiency':15-inter,'including_original_Y_W15_intersection':15+rank(vv+[val[y]for y in Y])-rank(A+vv+[val[y]for y in Y]),'Hub_original_rows':{x:hex(val[x])for x in X if loc[x]=='Hub'}}
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o;counts[op]+=1
  if op=='INIT':assert n not in val and n not in born;live.add(n);born.add(n);val[n]=0;loc[n]=q[0];peak=max(peak,len(live));history.append({'step':step,'op':o,'row_hex':'0x0'})
  elif op=='ADD':
   m=q[0];assert n!=m and n in val and m in val and same(loc[n],loc[m]),('bad_ADD',step,o,loc.get(n),loc.get(m));val[m]^=val[n]
   if m in live or m.startswith('X'):history.append({'step':step,'op':o,'chart':loc[m],'source_row_hex':hex(val[n]),'result_row_hex':hex(val[m])})
  elif op=='MOVE':
   dst=q[0];assert n in val;assert sub(dst,loc[n])if n in live else sub(loc[n],dst),('direction',step,o,loc.get(n));d=abs(len(chart[dst])-len(chart[loc[n]]));assert d>0;profile[d]+=1;history.append({'step':step,'op':o,'from':loc[n],'row_hex':hex(val[n])});loc[n]=dst
  elif op=='CLEAR':
   assert n in live
   if n.startswith('P'):assert val[n]==S[int(n[1:])]and same(loc[n],'zero'),('seed_contract',n)
   if n.startswith('E')and n[1:].isdigit():assert val[n]==1<<int(n[1:]),('point_contract',n)
   if n.startswith('H'):assert val[n]==int(next(c for c in w['history_cache_metadata']if c['name']==n)['row_hex'],16),('filtered_cache_contract',n)
   if n.startswith('Q'):assert val[n]==sum(1<<j for j in next(c for c in w['cache_metadata']if c['name']==n)['roles']),('cache_contract',n)
   live.remove(n);dirty+=bool(val[n]);history.append({'step':step,'op':o,'chart':loc[n],'row_hex':hex(val[n])});del val[n],loc[n]
  else:raise AssertionError(('unknown',op))
  if marks and step in w['milestones'].values():
   name=next(k for k,v in w['milestones'].items()if v==step);event={}
   if name in ['source_cut','seed8_before_Y']:
    assert all(val[y]==1<<(111+j)and loc[y]=='zero'for j,y in enumerate(Y));assert rank([val[x]for x in X])==111
    for f in w['forks']:
     i,q,d,p,G=[f[k]for k in ['old_receiver','new_receiver','donor','carrier','group']];g=sum(1<<j for j in G);assert loc[f'X{p}']=='Hub'and val[f'X{p}']==g;assert loc[f'X{q}']==f'F{i}'and val[f'X{q}']==g^(1<<q);assert loc[f'X{d}']==f'F{q}'and val[f'X{d}']==g^(1<<d)^(1<<i)
    for n,v in w['source_cut'].items():
     if name=='source_cut'or not n.startswith('KEEP'):assert val[n]==int(v['row_hex'],16)and loc[n]==v['chart'],('source_cut',name,n)
    event=inventory(step);HH=[val[x]for x in X if loc[x]=='Hub'];EE=[val[f'E{j}']for j in w['point_targets']];QQ=[val[f"X{f['new_receiver']}"]for f in w['forks']];assert rank(HH)==102 and rank(HH+EE)==108 and rank(HH+EE+QQ)==111;event.update(Hub_rank=102,Hub_plus_point_rank=108,Hub_plus_point_plus_query_rank=111)
   if name=='seed8_before_Y':
    for z,s in enumerate(S):assert val[f'P{z}']==s and loc[f'P{z}']=='zero'
    event['actual_ground_seed_rank']=8
   if name.startswith('completed_'):
    i=int(name.split('_')[1]);assert val[f'Y{i}']==(1<<(111+i))^(1<<i)and loc[f'Y{i}']==f'F{i}',('endpoint',i);event=inventory(step);event['actual_endpoint']=i
   if name=='all_X_restored':assert all(val[x]==1<<j and loc[x]=='Hub'for j,x in enumerate(X));event=inventory(step)
   if 'W15_intersection_dimension'in event:assert event['including_original_Y_W15_intersection']==event['W15_intersection_dimension']
   events[name]=event
 assert not live
 for j in range(111):assert val[f'X{j}']==1<<j and loc[f'X{j}']=='Hub',('X_restoration',j);assert val[f'Y{j}']==(1<<(111+j))^((1<<j)if j in w['targets']else 0)and loc[f'Y{j}']==f'F{j}',('Y_endpoint',j)
 return {'status':'PASS_INDEPENDENT_TWO_RETENTION_SEVENTEEN','columns':222,'targets':w['targets'],'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'peak_owners':peak,'dirty_clears':dirty,'events':events,'acquisition_history':history,'new_complete_kappa':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads((a.out/'WORD.json').read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];ans=replay(w,R);tests=[]
 def omit(label,pred,last=False):
  ids=[k for k,o in enumerate(w['operations'])if pred(o)];assert ids,label;b=copy.deepcopy(w);b['operations'].pop(ids[-1]if last else ids[0]);tests.append((label,b))
 omit('omit_first_retention_capture',lambda o:o==['ADD','P0','KEEP_C0'])
 omit('omit_first_reset',lambda o:o==['ADD','KEEP_C0','P0'])
 omit('omit_second_retention_capture',lambda o:o==['ADD','P0','KEEP_L7'])
 omit('omit_second_reset',lambda o:o==['ADD','KEEP_L7','P0'])
 omit('omit_actual_early_raw_query',lambda o:o==['ADD','EARLY7','P0'])
 omit('omit_nonlocal_delivery',lambda o:o==['ADD','KEEP_L7','Y16'])
 omit('omit_new_correction_capture',lambda o:o[0]=='ADD'and o[2]=='CORR16')
 omit('omit_new_X8_raw_capture',lambda o:o[0]=='ADD'and o[1]=='X8'and o[2].startswith('Hnew'))
 omit('omit_new_displaced_filter_query',lambda o:o[0]=='ADD'and o[1].startswith('Hnew')and o[2].startswith('P'))
 omit('omit_filtered_raw_capture',lambda o:o[0]=='ADD'and o[2]=='H0_0')
 omit('omit_filtered_actual_query',lambda o:o[0]=='ADD'and o[1]=='H0_0'and o[2].startswith('P'))
 omit('omit_filtered_retirement',lambda o:o==['CLEAR','H0_0'])
 omit('omit_early_donor_copy',lambda o:o==['ADD','X1','E1'])
 omit('omit_early_donor_ground_arrival',lambda o:o==['MOVE','E1','zero'])
 omit('omit_actual_common_capture',lambda o:o[0]=='ADD'and o[2]=='Q0')
 omit('omit_h1_pair_descent',lambda o:o[0]=='MOVE'and o[1].startswith('Q'))
 for f in w['forks']:
  i,q,d,p=[f[k]for k in ['old_receiver','new_receiver','donor','carrier']];omit(f'omit_fork_donor_{d}',lambda o,p=p,d=d:o==['ADD',f'X{p}',f'X{d}']);omit(f'omit_old_endpoint_aggregate_{q}',lambda o,p=p,q=q:o==['ADD',f'X{p}',f'X{q}']);omit(f'omit_actual_cross_facet_source_{i}',lambda o,i=i,d=d:o==['ADD',f'X{i}',f'X{d}']);omit(f'omit_donor_mask_{q}',lambda o,d=d,q=q:o==['ADD',f'E{d}',f'Y{q}']);omit(f'omit_new_delivery_{q}',lambda o,d=d,q=q:o==['ADD',f'X{d}',f'Y{q}'])
 for z,q in enumerate([21,64,65]):omit(f'omit_actual_held_query_{q}',lambda o,z=z,q=q:o==['ADD',f'X{q}',f'P{z}'])
 omit('omit_compensated_Hub_seed',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2]=='P0')
 omit('omit_point_seed_correction',lambda o:o[0]=='ADD'and o[1].startswith('E')and o[2].startswith('P'))
 omit('omit_donor_restoration',lambda o:o==['ADD','X3','X1'],last=True)
 omit('omit_carrier_restoration',lambda o:o[0]=='ADD'and o[2]=='X10',last=True)
 omit('omit_owner_retirement',lambda o:o==['CLEAR','P0'])
 b=copy.deepcopy(w);idx=b['operations'].index(['INIT','E1','L1']);b['operations'][idx][2]='Hub';tests.append(('false_early_point_Hub_birth',b))
 b=copy.deepcopy(w);b['charts']['M0']={'kind':'ann','rows':[R[i]for i in [3,76,80]]};b['charts']['C0']=b['charts']['M0'];tests.append(('false_rank6_common_chart_for_new_receivers',b))
 controls=[]
 for label,b in tests:
  try:replay(b,R,marks=False)
  except(AssertionError,KeyError,ValueError)as e:controls.append({'name':label,'rejected':True,'reason':str(e)})
  else:raise AssertionError(('surviving_mutant',label))
 ans['semantic_negative_controls']=controls;ans['word_sha256']=hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest();(a.out/'RESULT.json').write_text(json.dumps({k:v for k,v in ans.items()if k not in ['events','acquisition_history']},indent=2)+'\n');(a.out/'INVENTORY.json').write_text(json.dumps(ans['events'],indent=2)+'\n');(a.out/'ACQUISITION-HISTORY.json').write_text(json.dumps(ans['acquisition_history'],indent=2)+'\n');print(json.dumps({k:v for k,v in ans.items()if k not in ['events','acquisition_history','semantic_negative_controls']}));print('negative controls',len(controls));print('cuts',{k:(v.get('inventory_rank'),v.get('W15_intersection_dimension'))for k,v in ans['events'].items()})
if __name__=='__main__':main()
