#!/usr/bin/env python3
"""Independent endpoint, source and information audit of protected-point41."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
BASE='440bf0bb44f65180c066166e21691d15efcd19fb3e3bad7ea76038a4fa6834c8'
WORD='9053904c95084269c8d2df3f883a8c32dfadff763a2c0338a5ebf7c45d4d6267'
MARK=['ADD','CAP46','P3']
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ledger(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owners=set();captures=[];retired={};zeros=[]
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0];owners.add(n)
  elif op=='ADD':
   if q[0].startswith(('IMPORT_E','DIRECT_RAW')):captures.append({'step':step,'source':n,'destination':q[0],'source_chart':at[n],'destination_chart':at[q[0]],'source_row_hex':hex(v[n])})
   v[q[0]]^=v[n]
  elif op=='MOVE':
   if n in owners and v[n]==0:zeros.append({'step':step,'operation':o,'from':at[n]})
   at[n]=q[0]
  elif op=='CLEAR':retired[n]={'value_hex':hex(v[n]),'chart':at[n]};del v[n],at[n]
 return captures,retired,zeros
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','base','word','author-price','engine','price-engine','history-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();assert sha(a.base)==BASE and sha(a.word)==WORD;old=json.loads(a.base.read_text());w=json.loads(a.word.read_text());assert w['base_word_sha256']==BASE and w['targets']==old['targets']
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256']==old['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'e');price=load(a.price_engine,'p');hist=load(a.history_engine,'h')
 C0,H0,r0=e.replay(old,R);C,H,r=e.replay(w,R);assert r['counts']=={'INIT':122,'ADD':809,'MOVE':476,'CLEAR':122}and r['dirty_CLEAR']==122
 d={k:r['movement_profile'].get(k,0)-r0['movement_profile'].get(k,0)for k in set(r['movement_profile'])|set(r0['movement_profile'])};d={k:n for k,n in d.items()if n};assert d=={1:-4,2:1,5:-3,6:-2,7:3}
 own=lambda z:{o[1]for o in z['operations']if o[0]=='INIT'}
 assert own(old)-own(w)=={'AFF0','EXTRA_AFF','HKEEP_L19','HKEEP_L27'}and own(w)-own(old)=={'DIRECT_RAW10','DIRECT_RAW20'}
 assert ['INIT','P6','L19']in w['operations']and ['INIT','P7','L27']in w['operations']
 source0,ground0=hist.cut(old);source,ground=hist.cut(w);ss,sv,sa=source
 inv0={n:z for n,z in source0[1].items()if n!='P3'and not z>>111 and C0[source0[2][n]]==C0['M1']};inv={n:z for n,z in sv.items()if n!='P3'and not z>>111 and C[sa[n]]==C['M1']}
 assert inv==inv0 and sv['P3']==0 and sa['P3']=='M1'and len(e.bb(inv.values()))==11
 captures,retired,zeros=ledger(w);_,old_retired,_=ledger(old);assert zeros==[]
 for i in [8,9,36]:
  name=f'IMPORT_E{i}';assert inv[name]==1<<i and retired[name]==old_retired[name]=={'value_hex':hex(1<<i),'chart':'M1'}and w['protected_source_contracts'][name]==retired[name]
  cap=[z for z in captures if z['destination']==name];assert len(cap)==1 and cap[0]['source']==f'X{i}'and cap[0]['source_chart']==cap[0]['destination_chart']=='Extra6'and int(cap[0]['source_row_hex'],16)==1<<i
  probe=copy.deepcopy(w);ix=probe['operations'].index(MARK);probe['operations'][ix:ix]=[['ADD',name,'P3'],['ADD',name,'P3']];e.replay(probe,R)
 for i in [10,20]:
  name=f'DIRECT_RAW{i}';cap=[z for z in captures if z['destination']==name];assert len(cap)==1 and cap[0]['source']==f'X{i}'and cap[0]['source_chart']==cap[0]['destination_chart']==f'L{i}'and int(cap[0]['source_row_hex'],16)==1<<i
  assert retired[name]=={'value_hex':hex(1<<i),'chart':'zero'}and [o for o in w['operations']if f'Y{i}'in o]==[['ADD',name,f'Y{i}'],['MOVE',f'Y{i}',f'F{i}']]
 forward=hist.dominance(e,C0,H0,C,H);reverse=hist.dominance(e,C,H,C0,H0+[(-1,'FREE_RAW10','zero',1<<10),(-1,'FREE_RAW20','zero',1<<20)])
 common=lambda t:[z for n,z in t[1].items()if t[2][n]=='zero'and not z>>111]
 commonranks=(len(e.bb(common(ground0))),len(e.bb(common(ground))));assert commonranks==(18,20)
 controls=[]
 for i in [10,20]:
  for op in [['ADD',f'X{i}',f'DIRECT_RAW{i}'],['MOVE',f'DIRECT_RAW{i}','zero'],['ADD',f'DIRECT_RAW{i}',f'Y{i}'],['CLEAR',f'DIRECT_RAW{i}']]:
   bad=copy.deepcopy(w);bad['operations'].remove(op)
   try:e.replay(bad,R)
   except (AssertionError,KeyError)as ex:controls.append({'removed':op,'rejected':str(ex)})
   else:raise AssertionError(('essential omission accepted',op))
 source_controls=[]
 for i in [8,9,36]:
  for op in [['ADD',f'X{i}',f'IMPORT_E{i}'],['MOVE',f'IMPORT_E{i}','M1']]:
   bad=copy.deepcopy(w);bad['operations'].remove(op);e.replay(bad,R);bs,_=hist.cut(bad);assert bs[1][f'IMPORT_E{i}']!=1<<i or bs[2][f'IMPORT_E{i}']!='M1';source_controls.append({'removed':op,'endpoints_still_pass':True,'preload_import_contract_fails':True})
 Q=price.moment(r['movement_profile']);B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 allowance=tuple(z/6 for z in price.moment(B));room=(allowance[0]-Q[1],allowance[1]-Q[0]);author=json.loads(a.author_price.read_text())
 for k,z in [('moment',Q),('limiting_allowance',allowance),('limiting_room',room)]:assert z[0]<=Fraction(author[k]['lower_fraction'])<=Fraction(author[k]['upper_fraction'])<=z[1]
 known=set(w['targets']);obs=[];mask=(1<<111)-1
 for i in range(111):
  rows=[v&mask for _,_,c,v in H if e.sub(C[c],C[f'F{i}'])];rows += [1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0];obs.append(rows)
 waves=[]
 while True:
  nxt={i for i,rows in enumerate(obs)if e.fits(rows+[1<<j for j in known],1<<i)};assert known<=nxt
  if nxt==known:break
  waves.append(sorted(nxt-known));known=nxt
 duals=[{'receiver':i,'dual_hex':hex(price.outsider_dual(rows+[1<<j for j in known],i))}for i,rows in enumerate(obs)if i not in known]
 out={'status':'PASS_INDEPENDENT_PROTECTED_POINT41_AND_SOURCE_DOMINANCE','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'before':r0,'after':r,'exact_profile_difference':d,'price':{'moment':price.display(Q),'limiting_room':price.display(room),'increment':price.display(price.moment(d))},'source_cut_step':ss,'exact_M1_inventory_preserved':{n:hex(z)for n,z in inv.items()},'M1_rank_before_and_after':11,'common_rank_before_and_after':list(commonranks),'actual_raw_capture_events':captures,'three_import_contracts_before_clear':{f'IMPORT_E{i}':retired[f'IMPORT_E{i}']for i in [8,9,36]},'three_preload_read_unread_probes_pass':True,'remaining_owned_zero_MOVEs':zeros,'semantic_endpoint_controls':controls,'source_only_controls':source_controls,'old_full222_history_locally_dominated_by_new':True,'forward_history_recipes':forward,'new_full222_history_locally_dominated_by_old_plus_global_raw10_raw20':True,'reverse_history_recipes':reverse,'fresh_history_feedback_closure':sorted(known),'feedback_waves':waves,'fresh_outsider_duals':duals,'scope':'Exact41 endpoints and actual M1 custody; historical span dominance grants simultaneous observations. Other physical source banks are not inherited from it; no new kappa or complete supplier.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','after','common_rank_before_and_after','price','feedback_waves']}))
if __name__=='__main__':main()
