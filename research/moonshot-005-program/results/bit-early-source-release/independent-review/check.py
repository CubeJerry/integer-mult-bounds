#!/usr/bin/env python3
"""Independent early-release chronology, actual-source and exact-price review."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,copy,hashlib,importlib.util,json
BASE='9053904c95084269c8d2df3f883a8c32dfadff763a2c0338a5ebf7c45d4d6267'
WORD='509fe171db1fb0f82d9452c52e53166cae41da6f0c1700b10d8ef5db00ad28f2'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scan(w,C,e):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 seen=set();snapshots={};reads=defaultdict(list);retired={};first_all_raw=None
 for st,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='ADD':
   reads[tuple(o)].append((v[n],v[q[0]],C[at[n]],C[at[q[0]]]))
   if q[0]in [f'P{i}'for i in range(6)]and at[q[0]]=='Hub'and q[0]not in seen:
    P=q[0];seen.add(P);names=[f'X{i}'for i in range(111)if at[f'X{i}']=='Hub'];rows=[v[n]for n in names];known=[i for i in range(111)if e.fits(rows,1<<i)]
    snapshots[P]={'before_operation_1_based':st,'Hub_original_rank':len(e.bb(rows)),'raw_columns_available':known,'missing_raw_columns':sorted(set(range(111))-set(known)),'actual_Hub_original_rows':{n:hex(v[n])for n in names},'principal_value_hex':hex(v[P])}
   v[q[0]]^=v[n]
  elif op=='MOVE':at[n]=q[0]
  elif op=='CLEAR':retired[n]={'row_hex':hex(v[n]),'chart':at[n]};del v[n],at[n]
  if first_all_raw is None and all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111)):first_all_raw=st
 return snapshots,reads,retired,first_all_raw
def field_histories(H,C):
 d=defaultdict(list)
 for _,n,c,v in H:d[n].append((C[c],v))
 return d
def insert_probes(w,snapshots,points):
 at={s['before_operation_1_based']:(P,points[P])for P,s in snapshots.items()};out=copy.deepcopy(w);ops=[]
 for k,o in enumerate(w['operations'],1):
  if k in at:
   P,added=at[k]
   for i in added:ops += [['ADD',f'X{i}',P],['ADD',f'X{i}',P]]
  ops.append(o)
 out['operations']=ops;return out

def main():
 p=argparse.ArgumentParser()
 for n in ['repo','base','word','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();assert sha(a.base)==BASE and sha(a.word)==WORD;old=json.loads(a.base.read_text());w=json.loads(a.word.read_text());assert w['base_word_sha256']==BASE and w['targets']==old['targets']and w['charts']==old['charts']
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256']==old['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'e');price=load(a.price_engine,'p')
 C0,H0,r0=e.replay(old,R);C,H,r=e.replay(w,R);assert r==r0
 assert Counter(map(tuple,w['operations']))==Counter(map(tuple,old['operations']))
 assert field_histories(H0,C0)==field_histories(H,C)
 s0,reads0,ret0,full0=scan(old,C0,e);s,reads,ret,full=scan(w,C,e);assert reads==reads0
 assert [z['Hub_original_rank']for z in s0.values()]==[102]*6
 assert [z['Hub_original_rank']for z in s.values()]==[102,104,106,108,109,110]
 assert [len(z['raw_columns_available'])for z in s0.values()]==[99]*6
 assert [len(z['raw_columns_available'])for z in s.values()]==[99,102,105,108,109,110]
 added={P:sorted(set(z['raw_columns_available'])-set(s0[P]['raw_columns_available']))for P,z in s.items()}
 for P,cols in added.items():
  assert s[P]['principal_value_hex']=='0x0'
  for i in cols:assert s[P]['actual_Hub_original_rows'][f'X{i}']==hex(1<<i)
 probe=insert_probes(w,s,added);_,_,pr=e.replay(probe,R);assert pr['counts']['ADD']==r['counts']['ADD']+2*sum(map(len,added.values()))
 access=copy.deepcopy(w);idx=access['operations'].index(['ADD','CAP46','P3']);extra=[]
 for i in [8,9,36]:
  name=f'IMPORT_E{i}';assert ret[name]==ret0[name]=={'row_hex':hex(1<<i),'chart':'M1'};extra += [['ADD',name,'P3'],['ADD',name,'P3']]
 access['operations'][idx:idx]=extra;e.replay(access,R)
 controls=[]
 for op in [['ADD','X21','Y3'],['ADD','X10','X21']]:
  bad=copy.deepcopy(w);ix=max(k for k,o in enumerate(bad['operations'])if o==op);bad['operations'].pop(ix)
  try:e.replay(bad,R)
  except (AssertionError,KeyError)as ex:controls.append({'omitted':op,'rejected':str(ex)})
  else:raise AssertionError(('essential omission accepted',op))
 bad=copy.deepcopy(w);move=['MOVE','X1','Hub'];bad['operations'].remove(move);ix=bad['operations'].index(['ADD','X1','Y21']);bad['operations'].insert(ix,move)
 try:e.replay(bad,R)
 except (AssertionError,KeyError)as ex:controls.append({'return_moved_before_dependent_receiver_read':move,'rejected':str(ex)})
 else:raise AssertionError('early nonlocal source return accepted')
 oldprobe=insert_probes(old,s0,{P:([10]if P=='P1'else[])for P in s0});e.replay(oldprobe,R)
 assert s0['P1']['actual_Hub_original_rows']['X10']!=hex(1<<10)and 10 not in s0['P1']['raw_columns_available']
 controls.append({'old_P1_read_unread_X10_endpoints_pass':True,'old_source_row_hex':s0['P1']['actual_Hub_original_rows']['X10'],'old_raw_X10_unavailable_in_entire_Hub_span':True,'new_raw_X10_available':True})
 Q=price.moment(r['movement_profile']);B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 allowance=tuple(z/6 for z in price.moment(B));room=(allowance[0]-Q[1],allowance[1]-Q[0])
 out={'status':'PASS_INDEPENDENT_EARLY_RELEASE41_ACTUAL_SOURCE_EXPANSION','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'before':r0,'after':r,'entire_operation_multiset_identical':True,'every_record_ordered_chart_and_full222_value_history_identical':True,'every_ADD_source_and_destination_prestate_identical_by_instruction_occurrence':True,'no_Hub_reconstruction_or_extra_operation_used':True,'Hub_sources_before_old_loads':s0,'Hub_sources_before_new_loads':s,'new_raw_column_access_probes_by_principal':added,'all_new_raw_column_probes_pass':True,'number_of_distinct_stage_column_probes':sum(map(len,added.values())),'first_all_originals_raw_at_Hub_old':full0,'first_all_originals_raw_at_Hub_new':full,'protected_imports_before_clear':{f'IMPORT_E{i}':ret[f'IMPORT_E{i}']for i in [8,9,36]},'three_real_late_M1_import_probes_pass':True,'negative_controls':controls,'price':{'moment':price.display(Q),'limiting_room':price.display(room)},'scope':'Same41 endpoints and unchanged per-record historical values, with strictly expanded actual original-Hub source spans at later load times. Frozen timeless observation envelopes do not encode this chronological improvement. No new complete supplier or kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'ranks':[z['Hub_original_rank']for z in s.values()],'raw_column_counts':[len(z['raw_columns_available'])for z in s.values()],'probes':out['number_of_distinct_stage_column_probes'],'price':out['price']}))
if __name__=='__main__':main()
