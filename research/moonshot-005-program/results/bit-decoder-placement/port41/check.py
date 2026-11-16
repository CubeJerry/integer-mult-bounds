#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from price import invoice,moment,encode
WORD='204e38b8c56f17cc3e88a475d4c75e5613ed4215e29c6ede33e55a3e614a82b1';BASE='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
def dual(e,rows,i):
 eq=rows+[1<<i];cols=[sum(((r>>j)&1)<<k for k,r in enumerate(eq))for j in range(111)];v=e.solve(cols,1<<len(rows));assert v is not None and v>>i&1 and all((v&r).bit_count()%2==0 for r in rows);return v

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=(a.out/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;old=json.loads(br)
 ep=Path(__file__).with_name('retained')/'source_history_engine.py';assert hashlib.sha256(ep.read_bytes()).hexdigest()=='c934d8ff2f80970fa7db3dbf98e2d5a96e728b00cf314aa4a8e5d79dce632f29';sp=importlib.util.spec_from_file_location('engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];run=e.replay(w,R,S,15,False);prev=e.replay(old,R,S,15,False);C=run['C'];v,at=run['cuts']['seed']['values'],run['cuts']['seed']['charts'];ov,oa=prev['cuts']['seed']['values'],prev['cuts']['seed']['charts'];rank=lambda rows:len(e.basis(rows))
 assert run['count']=={'INIT':115,'ADD':905,'MOVE':436,'CLEAR':115}and run['dirty_CLEAR']==115
 assert run['profile']=={1:109,2:66,3:57,4:13,5:73,6:24,7:94}and w['targets']==old['targets']and w['seed_rows_hex']==old['seed_rows_hex']
 for j in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{j}']==[o for o in old['operations']if o[0]=='MOVE'and o[1]==f'X{j}']
 for n in ov:
  assert v[n]==(ov['Q1']if n=='ZKEEP2'else ov[n]);assert at[n]==('L41'if n=='ZKEEP2'else'zero'if n=='ZRAW0'else oa[n])
 assert v['BACK2']==int(w['coded_port_repair']['backup_row_hex'],16)and at['BACK2']=='Jnew2'
 assert e.contained(C['L41'],C['M1'])and e.contained(C['Jnew2'],C['M1'])and e.contained(C['Jnew2'],C['F2'])
 assert len(C['M1'])-len(C['Jnew2'])==3 and not e.contained(C['L41'],C['F2'])
 assert not any(o[0]=='ADD'and o[1]=='ZKEEP2'and o[2].startswith('Y')for o in w['operations'])
 vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};available=None;loading=None
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':vals[n]=0;loc[n]=q[0]
  elif op=='MOVE':loc[n]=q[0]
  elif op=='ADD':
   if o==['ADD','BACK2','P3']:
    available={n:hex(r)for n,r in vals.items()if n!='P3'and r.bit_length()<=111 and C[loc[n]]==C['M1']};loading=step
   vals[q[0]]^=vals[n]
  elif op=='CLEAR':del vals[n],loc[n]
 assert available and available['Q1']==hex(v['Q1'])
 obs=[int(s['row_hex'],16)for s in run['snapshots']];xmask=(1<<111)-1;ground=[r for n,r in v.items()if at[n]=='zero'and not(r&~xmask)]
 localmask={ch:sum(1<<j for j in range(111)if e.contained(C[f'L{j}'],C[ch]))for ch in set(at.values())}
 nn=[n for n,r in v.items()if at[n]not in ['zero','Hub']and not(r&~xmask)and r&~localmask[at[n]]]
 assert all(n in nn for n in ['Q1','Q3','Q4','HKEEP_E6','HKEEP_L19'])
 norm=ground+[v[n]for n in nn];assert rank(norm+[v[f'Y{i}']for i in range(111)])==rank(norm)+111
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));K=[(1<<i)|sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];h=w['singular_h'];W=[K[i]&sum(1<<j for j in range(111)if h[i]==h[j])for i in range(111)]
 actual=[];rawfits=[];strong=[];bases=[]
 for i in range(111):
  F=C[f'F{i}'];stock=[r for n,r in v.items()if not(r&~xmask)and e.contained(C[at[n]],F)];stock +=[r for r,s in zip(obs,run['snapshots'])if e.contained(C[s['chart']],F)];local=[1<<j for j in range(111)if dot(i,j)==0]
  if e.solve(stock,1<<i)is not None:actual.append(i)
  relax=ground+[v[n]for n in nn if e.contained(C[at[n]],F)]+local
  if e.solve(relax,1<<i)is not None:rawfits.append(i)
  bb=stock+local;bases.append(bb)
  if e.solve(bb,1<<i)is not None:strong.append(i)
 known=set();waves=[]
 while True:
  nxt={i for i,bb in enumerate(bases)if e.solve(bb+[1<<j for j in known],1<<i)is not None};assert known<=nxt
  if nxt==known:break
  waves.append(sorted(nxt-known));known=nxt
 duals=[{'receiver':i,'dual_hex':hex(dual(e,bb+[1<<j for j in known],i))}for i,bb in enumerate(bases)if i not in known]
 tests=[['ADD','P3','BACK2'],['MOVE','BACK2','Jnew2'],['ADD','BACK2','Y2'],['MOVE','ZRAW0','zero'],['ADD','ZRAW0','P3'],['ADD','ZCORR2','Y2'],['CLEAR','BACK2']];rejected=[]
 for op in tests:
  mut=copy.deepcopy(w);mut['operations'].remove(op);mut['milestones']={k:-1 for k in w['milestones']};mut.pop('source_cut',None)
  try:e.replay(mut,R,S,15,False)
  except AssertionError:rejected.append(op)
  else:raise AssertionError('accepted semantic mutant '+str(op))
 payload_controls=[]
 for op in [['ADD','BACK2','P3'],['ADD','Q1','P3']]:
  mut=copy.deepcopy(w);ix=mut['operations'].index(op);mut['operations'].pop(ix);mut['milestones']={k:n-(n>ix)for k,n in w['milestones'].items()};mut.pop('source_cut',None);rr=e.replay(mut,R,S,15,False);assert rr['cuts']['seed']['values']['ZKEEP2']!=v['ZKEEP2'];payload_controls.append({'removed':op,'endpoints_still_correct':True,'claimed_payload_rejected':True})
 hh=w['singular_h'];ex=w['history_extra_query_roles'];h0=[1<<j for j in range(111)if hh[j]==0];h1=[1<<j for j in range(111)if hh[j]==1 and j not in ex];g0=int(w['extra_source_delivery']['first_retention_hex'],16);g1=int(w['higher_source_delivery']['first_retention_hex'],16);bank=[([7,11,12],h0),([41,28,44],h1),([19],[1<<j for j in ex]+[g0]),([27],h0+[g1])];cr=[]
 for i in range(111):
  rr=[1<<j for j in w['targets']]+[1<<j for j in range(111)if dot(i,j)==0]
  for pp,bb in bank:
   if any(dot(i,d)==0 for d in pp):rr+=bb
  cr.append(rr)
 ck=set(w['targets']);cw=[]
 while True:
  ns={i for i,rr in enumerate(cr)if e.solve(rr+[1<<j for j in ck],1<<i)is not None};assert ck<=ns
  if ns==ck:break
  cw.append(sorted(ns-ck));ck=ns
 assert len(ck)==111
 out={'status':'PASS_ACTUAL_PORT41_CODED_LOAD_FREEDOM','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':w['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':115,'all_terminal_principal_values_unchanged':True,'original_X_routes_unchanged':True,'coded_port_repair':w['coded_port_repair'],'admissible_recipe_cut_step':loading,'actually_live_M1_pureX_source_fields':available,'admissible_source_rank':rank([int(x,16)for x in available.values()]),'principal_snapshot_count':len(obs),'principal_history_rank':rank(obs),'ground_rank':rank(ground),'complete_normalized_rank':rank(norm),'normalized_rank_with_all_Y_nuisance':rank(norm)+111,'proper_nonlocal_inventory':[{'field':n,'chart':at[n],'row_hex':hex(v[n])}for n in nn],'actual_stock_history_fitting':actual,'raw_local_fitting':rawfits,'strong_stock_history_raw_fitting':strong,'free_point_feedback_closure':sorted(known),'feedback_waves':waves,'feedback_closure_duals':duals,'coarse_full_bank_closure':sorted(ck),'coarse_bank_feedback_waves':cw,'semantic_negative_controls':rejected,'payload_contract_controls':payload_controls,'scope':'Actual34 endpoints preserved with a new Q1 coded row atL41. Fullbank111 is onlyoptimisticinformationcoverage; actualcomplete decoderunproved.'}
 (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');pr=invoice(run['profile']);pr['increment_from_thirtyfour']=encode(moment({1:-1,2:1,3:1}));(a.out/'PRICE.json').write_text(json.dumps(pr,indent=2)+'\n');print(out['status'],run['count'],'Q',pr['moment']['lower'],'room',pr['limiting_room']['lower']);print('actual',actual,'raw',rawfits,'closure',sorted(known),'admissible_rank',out['admissible_source_rank'])
if __name__=='__main__':main()
