#!/usr/bin/env python3
"""Literal replay, actual raw acquisition checks, and scoped affine controls."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys
from build import build,BASE
from price import invoice,moment,encode
WORD='7c5165a225e70e74181ac01c76dcde156c724aeb1e708309b146b7f174be723c'
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 raw=(a.out/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;old=json.loads(br)
 ep=Path(__file__).with_name('retained')/'source_history_engine.py';assert hashlib.sha256(ep.read_bytes()).hexdigest()=='c934d8ff2f80970fa7db3dbf98e2d5a96e728b00cf314aa4a8e5d79dce632f29';sp=importlib.util.spec_from_file_location('engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
 source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']]
 run=e.replay(w,R,S,15,False);prior=e.replay(old,R,S,15,False);C=run['C'];cut=run['cuts']['seed'];ocut=prior['cuts']['seed'];v,at=cut['values'],cut['charts']
 assert run['count']=={'INIT':104,'ADD':866,'MOVE':427,'CLEAR':104}and run['dirty_CLEAR']==104
 assert run['profile']=={1:100,2:67,3:56,4:13,5:71,6:23,7:96,8:1}
 assert w['targets']==old['targets']and w['seed_rows_hex']==old['seed_rows_hex']
 for j in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{j}']==[o for o in old['operations']if o[0]=='MOVE'and o[1]==f'X{j}']
 for s in w['affine_injections']:
  row=int(s['row_hex'],16);assert v[s['owner']]==row and at[s['owner']]==s['chart'];assert v[s['first_retention']]==ocut['values'][s['first_retention']]^row
  assert not any(o[0]=='MOVE'and o[1]==s['owner']for o in w['operations'])
  for i in s['old_receivers']:assert e.contained(C[s['chart']],C[f'F{i}'])
 changed={s['owner']for s in w['affine_injections']}|{s['first_retention']for s in w['affine_injections']}
 for n in ocut['values']:
  if n not in changed:assert v[n]==ocut['values'][n]and at[n]==ocut['charts'][n]
 # Independently track captures: the original has not yet been recoded.
 vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};capture=[]
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':vals[n]=0;loc[n]=q[0]
  elif op=='MOVE':loc[n]=q[0]
  elif op=='ADD':
   t=q[0]
   if t.startswith('AFF'):
    assert n.startswith('X')and vals[n]==1<<int(n[1:]);assert C[loc[n]]==C[loc[t]];capture.append({'step':step,'source':n,'owner':t,'chart':loc[t],'actual_raw_hex':hex(vals[n])})
   vals[t]^=vals[n]
  elif op=='CLEAR':del vals[n],loc[n]
 assert len(capture)==3
 # Finite adversarial boundary checks supplement the universal algebraic proof.
 allowed=[f['group']for f in old['forks']]+[old['h1_private_roles'][str(i)]for i in[4,74,78]];boundary=[]
 patterns=[('all_zero',[[]for _ in range(6)]),('all_39_parameters',allowed)]
 for z,g in enumerate(allowed):
  for j in g:
   p0=[[]for _ in range(6)];p0[z]=[j];patterns.append((f'isolated_{z}_{j}',p0))
 for label,params in patterns:
  ww=build(old,params);rr=e.replay(ww,R,S,15,False);h=sum(bool(params[z])for z in range(3));expected=prior['profile'].copy();expected[1]+=4*h;expected[2]-=2*h;assert rr['profile']==expected;boundary.append(label)
 rejected=[]
 tests=[]
 for s in w['affine_injections']:
  z=s['packet'];name=s['owner']
  for op in [['ADD',name,f'P{z}']]+[['ADD',name,f'Y{i}']for i in s['old_receivers']]+[['CLEAR',name]]:tests.append((str(op),op))
 for label,op in tests:
  ids=[i for i,o in enumerate(w['operations'])if o==op];assert len(ids)==1;mut=copy.deepcopy(w);mut['operations'].pop(ids[0]);mut['milestones']={k:-1 for k in w['milestones']};mut.pop('source_cut',None)
  try:e.replay(mut,R,S,15,False)
  except AssertionError:rejected.append(label)
  else:raise AssertionError('accepted semantic mutant '+label)
 capture_contract_controls=[]
 for s in w['affine_injections']:
  for j in s['roles']:
   mut=copy.deepcopy(w);ix=mut['operations'].index(['ADD',f'X{j}',s['owner']]);mut['operations'].pop(ix);mut['milestones']={k:v-(v>ix)for k,v in w['milestones'].items()};mut.pop('source_cut',None)
   rr=e.replay(mut,R,S,15,False);assert rr['cuts']['seed']['values'][s['owner']]!=int(s['row_hex'],16)
   capture_contract_controls.append({'removed_capture':j,'owner':s['owner'],'all_endpoints_remain_valid':True,'declared_acquired_row_rejected':True})
 result={'status':'PASS_ACTUAL_HIGHER_CHART_AFFINE_THIRTY','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'input_columns':222,'targets':w['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'affine_injections':w['affine_injections'],'actual_raw_captures':capture,'capture_contract_controls':capture_contract_controls,'original_X_routes_unchanged':True,'all_other_seed_cut_values_and_locations_unchanged':True,'boundary_parameter_words_checked':boundary,'semantic_negative_controls':rejected,'negative_controls_disable_invoice_source_cut_and_milestones':True,'exact_movement_increment':'4 - 2*2^(199/200)','scope':'Constructive source-preserving higher-chart family; no new endpoint or complete kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');price=invoice(run['profile']);price['increment_from_thirty']=encode(moment({1:4,2:-2}));(a.out/'PRICE.json').write_text(json.dumps(price,indent=2)+'\n');print(result['status'],run['count']);print('Q',price['moment']['lower'],'room',price['limiting_room']['lower'],'delta',price['increment_from_thirty']['lower']);print('boundaries',len(boundary),'controls',len(rejected))
if __name__=='__main__':main()
