#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from price import invoice,moment,encode
WORD='8580350db073049f01268989d6acdb4bf770699a079760163a394d2867323c36';BASE='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
def dual(e,rows,i):
 eq=rows+[1<<i];cols=[sum(((r>>j)&1)<<k for k,r in enumerate(eq))for j in range(111)];v=e.solve(cols,1<<len(rows));assert v is not None and v>>i&1 and all((v&r).bit_count()%2==0 for r in rows);return v

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=(a.out/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;old=json.loads(br)
 ep=Path(__file__).with_name('retained')/'source_history_engine.py';assert hashlib.sha256(ep.read_bytes()).hexdigest()=='c934d8ff2f80970fa7db3dbf98e2d5a96e728b00cf314aa4a8e5d79dce632f29';sp=importlib.util.spec_from_file_location('engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];run=e.replay(w,R,S,15,False);prev=e.replay(old,R,S,15,False);C=run['C'];v,at=run['cuts']['seed']['values'],run['cuts']['seed']['charts'];ov,oa=prev['cuts']['seed']['values'],prev['cuts']['seed']['charts'];rank=lambda rows:len(e.basis(rows))
 assert run['count']=={'INIT':114,'ADD':902,'MOVE':436,'CLEAR':114}and run['dirty_CLEAR']==114
 assert run['profile']=={1:110,2:65,3:56,4:14,5:73,6:24,7:94}and w['targets']==old['targets']and w['seed_rows_hex']==old['seed_rows_hex']
 for j in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{j}']==[o for o in old['operations']if o[0]=='MOVE'and o[1]==f'X{j}']
 assert v==ov
 for n in at:assert at[n]==('L29'if n in ['ZRAW0','ZKEEP2']else oa[n])
 assert v['ZRAW0']==1 and v['ZKEEP2']==int(w['m1_retention'][0]['h_hex'],16)
 assert e.contained(C['L29'],C['M1'])and e.contained(C['L29'],C['Jnew2'])and e.contained(C['Jnew2'],C['F2'])and C['C2']==C['M1']
 assert len(C['M1'])-len(C['L29'])==4
 # Actual acquisition occurs immediately after raw X0's first chart arrival.
 cap=[i for i,o in enumerate(w['operations'])if o==['ADD','X0','ZRAW0']];assert len(cap)==1;ix=cap[0];assert w['operations'][ix-1]==['MOVE','X0','C2']and w['operations'][ix+1]==['MOVE','ZRAW0','L29']
 vv={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)}
 for i,o in enumerate(w['operations']):
  op,n,*q=o
  if op=='INIT':vv[n]=0
  elif op=='ADD':
   if i==ix:assert vv['X0']==1 and vv['ZRAW0']==0
   vv[q[0]]^=vv[n]
  elif op=='CLEAR':del vv[n]
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
 # The new placement fixes the old three envelope failures but loses receiver46.
 hh=w['singular_h'];ex=w['history_extra_query_roles'];h0=[1<<j for j in range(111)if hh[j]==0];h1=[1<<j for j in range(111)if hh[j]==1 and j not in ex];g0=int(w['extra_source_delivery']['first_retention_hex'],16);g1=int(w['higher_source_delivery']['first_retention_hex'],16);bank=[([7,11,12],h0),([29,28,44],h1),([19],[1<<j for j in ex]+[g0]),([27],h0+[g1])];gr=[1<<j for j in w['targets']];cr=[]
 for i in range(111):
  rr=gr+[1<<j for j in range(111)if dot(i,j)==0]
  for pp,bb in bank:
   if any(dot(i,d)==0 for d in pp):rr+=bb
  cr.append(rr)
 ck=set(w['targets'])
 while True:
  ns={i for i,rr in enumerate(cr)if e.solve(rr+[1<<j for j in ck],1<<i)is not None};assert ck<=ns
  if ns==ck:break
  ck=ns
 assert sorted(set(range(111))-ck)==[46];cd=dual(e,cr[46]+[1<<j for j in ck],46)
 tests=[['ADD','X0','ZRAW0'],['MOVE','ZRAW0','L29'],['ADD','ZRAW0','P3'],['ADD','P3','ZKEEP2'],['ADD','ZKEEP2','Y2'],['ADD','ZCORR2','Y2'],['CLEAR','ZRAW0']];rejected=[]
 for op in tests:
  assert op in w['operations'],op
  mut=copy.deepcopy(w);mut['operations'].remove(op);mut['milestones']={k:-1 for k in w['milestones']};mut.pop('source_cut',None)
  try:e.replay(mut,R,S,15,False)
  except AssertionError:rejected.append(op)
  else:raise AssertionError('accepted semantic mutant '+str(op))
 for n in ['ZRAW0','ZKEEP2']:
  mut=copy.deepcopy(w);o=next(o for o in mut['operations']if o[0]=='INIT'and o[1]==n);o[2]='L0';mut['milestones']={k:-1 for k in w['milestones']};mut.pop('source_cut',None)
  try:e.replay(mut,R,S,15,False)
  except AssertionError:rejected.append(['wrong_birth',n,'L0'])
  else:raise AssertionError('accepted wrong birth '+n)
 out={'status':'PASS_ACTUAL_PORT29_REPAIR_SAME_THIRTYFOUR','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':w['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':114,'all_seed_cut_values_unchanged':True,'only_seed_cut_location_changes':['ZRAW0','ZKEEP2'],'all_original_X_routes_unchanged':True,'actual_raw_capture_step':ix+1,'fully_paid_helper_MOVE_rank':4,'port_repair':w['port_repair'],'principal_snapshot_count':len(obs),'principal_history_rank':rank(obs),'ground_rank':rank(ground),'complete_normalized_rank':rank(norm),'normalized_rank_with_all_Y_nuisance':rank(norm)+111,'proper_nonlocal_inventory':[{'field':n,'chart':at[n],'row_hex':hex(v[n])}for n in nn],'actual_stock_history_fitting':actual,'raw_local_fitting':rawfits,'strong_stock_history_raw_fitting':strong,'free_point_feedback_closure':sorted(known),'feedback_waves':waves,'feedback_closure_duals':duals,'new_coarse_bank_closure':sorted(ck),'new_coarse_bank_outsider':46,'new_coarse_bank_dual_hex':hex(cd),'semantic_negative_controls':rejected,'negative_controls_disable_invoice_source_cut_and_milestones':True,'scope':'Actualportrepair preserves34; fullbankrelaxation110 stillfails46. No complete supplier or newkappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');pr=invoice(run['profile']);pr['increment_from_previous_thirtyfour']=encode(moment({4:1}));(a.out/'PRICE.json').write_text(json.dumps(pr,indent=2)+'\n');print(out['status'],run['count'],'Q',pr['moment']['lower'],'room',pr['limiting_room']['lower']);print('actual',actual,'strong',strong,'closure',sorted(known),'coarse110dual',hex(cd),'normal',rank(norm),'proper',len(nn))
if __name__=='__main__':main()
