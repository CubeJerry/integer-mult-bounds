#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from price import invoice,moment,encode
WORD='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e';BASE='73a6c4adb00498a0c33956a3aa1a0525eb143fa0179a4abaeb238b150774da45'
def dual(e,rows,i):
 eq=rows+[1<<i];cols=[sum(((r>>j)&1)<<k for k,r in enumerate(eq))for j in range(111)];v=e.solve(cols,1<<len(rows));assert v is not None and v>>i&1 and all((v&r).bit_count()%2==0 for r in rows);return v

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=(a.out/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;old=json.loads(br)
 ep=Path(__file__).with_name('retained')/'source_history_engine.py';assert hashlib.sha256(ep.read_bytes()).hexdigest()=='c934d8ff2f80970fa7db3dbf98e2d5a96e728b00cf314aa4a8e5d79dce632f29';sp=importlib.util.spec_from_file_location('engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];run=e.replay(w,R,S,15,False);prev=e.replay(old,R,[int(x,16)for x in old['seed_rows_hex']],15,False);C=run['C'];v,at=run['cuts']['seed']['values'],run['cuts']['seed']['charts'];ov,oa=prev['cuts']['seed']['values'],prev['cuts']['seed']['charts'];meta=w['extra_source_delivery'];rank=lambda rows:len(e.basis(rows))
 assert run['count']=={'INIT':114,'ADD':902,'MOVE':435,'CLEAR':114}and run['dirty_CLEAR']==114
 assert run['profile']=={1:110,2:65,3:56,4:13,5:73,6:24,7:94}
 assert sorted(set(w['targets'])-set(old['targets']))==[19,20]and set(old['targets'])<set(w['targets'])
 for j in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{j}']==[o for o in old['operations']if o[0]=='MOVE'and o[1]==f'X{j}']
 assert e.contained(C['L19'],C['Extra6'])and e.contained(C['L19'],C['F20'])and len(C['Extra6'])==6
 assert v['EXTRA_AFF']==v['HKEEP_L19']==1<<20 and at['EXTRA_AFF']=='Extra6'and at['HKEEP_L19']=='L19'
 assert v['HRAW19']==1<<19 and at['HRAW19']=='L19'
 assert v['HKEEP_E6']==int(meta['first_retention_hex'],16)and at['HKEEP_E6']=='Extra6'
 for n in ov:
  if n!='P6':assert v[n]==ov[n]and at[n]==oa[n]
 assert v['P6']==int(meta['changed_ground_row_hex'],16)and at['P6']=='zero'
 assert [o for o in old['operations']if o[0]=='ADD'and o[1]=='P6'and o[2].startswith('Y')]==[]
 assert w['operations'][:2]==[['INIT','HRAW19','L19'],['ADD','X19','HRAW19']]
 for n in ['HRAW19','HKEEP_E6','HKEEP_L19']:assert not any(o[0]=='MOVE'and o[1]==n for o in w['operations'])
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
 tests=[['ADD','X19','HRAW19'],['ADD','P6','HKEEP_E6'],['ADD','HKEEP_E6','P6'],['ADD','EXTRA_AFF','P6'],['ADD','P6','HKEEP_L19'],['ADD','HKEEP_L19','P6'],['ADD','HRAW19','P6'],['ADD','HKEEP_L19','Y20'],['ADD','P6','Y19'],['ADD','E75','Y19'],['MOVE','P6','L19'],['CLEAR','HKEEP_E6']];rejected=[]
 for op in tests:
  mut=copy.deepcopy(w);ix=max(k for k,o in enumerate(mut['operations'])if o==op);mut['operations'].pop(ix);mut['milestones']={k:-1 for k in w['milestones']};mut.pop('source_cut',None)
  try:e.replay(mut,R,S,15,False)
  except AssertionError:rejected.append(op)
  else:raise AssertionError('accepted semantic mutant '+str(op))
 out={'status':'PASS_ACTUAL_EXTRA_SOURCE_THIRTYFOUR','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':w['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':114,'original_X_routes_unchanged':True,'seed_cut_only_old_row_change':'P6','extra_source_delivery':meta,'principal_snapshot_count':len(obs),'principal_history_rank':rank(obs),'history_W15_intersection':rank(obs)+15-rank(obs+W),'history_C9_intersection':rank(obs)+9-rank(obs+K),'ground_rank':rank(ground),'complete_normalized_rank':rank(norm),'normalized_rank_with_all_Y_nuisance':rank(norm)+111,'proper_nonlocal_inventory':[{'field':n,'chart':at[n],'row_hex':hex(v[n])}for n in nn],'actual_stock_history_fitting':actual,'raw_local_fitting':rawfits,'strong_stock_history_raw_fitting':strong,'free_point_feedback_closure':sorted(known),'feedback_waves':waves,'feedback_closure_duals':duals,'semantic_negative_controls':rejected,'negative_controls_disable_invoice_source_cut_and_milestones':True,'scope':'Actual34 native partial endpoints, including20 outside even the old global-common plus all-private-bank83 envelope. Not fullsupplier or newkappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HISTORY-SNAPSHOTS.json').write_text(json.dumps(run['snapshots'],indent=2)+'\n');price=invoice(run['profile']);price['increment_from_higher_thirtytwo']=encode(moment({1:2,5:1,7:-1}));(a.out/'PRICE.json').write_text(json.dumps(price,indent=2)+'\n');print(out['status'],run['count'],'Q',price['moment']['lower'],'room',price['limiting_room']['lower']);print('fits',actual,'raw',rawfits,'strong',strong,'closure',sorted(known));print('history',len(obs),rank(obs),'normal',rank(norm),'nonlocal',len(nn))
if __name__=='__main__':main()
