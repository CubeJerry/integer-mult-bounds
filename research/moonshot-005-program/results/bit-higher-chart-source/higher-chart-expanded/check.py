#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from build import build,BASE
from price import invoice,moment,encode
WORD='6a1eef8ef1f620914b3f014c9ba129bbe389c6fd5a010872f3e5cca88f5cb52f'
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=(a.out/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);br=a.base.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE;old=json.loads(br)
 ep=Path(__file__).with_name('retained')/'source_history_engine.py';assert hashlib.sha256(ep.read_bytes()).hexdigest()=='c934d8ff2f80970fa7db3dbf98e2d5a96e728b00cf314aa4a8e5d79dce632f29';sp=importlib.util.spec_from_file_location('engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];os=[int(x,16)for x in old['seed_rows_hex']];run=e.replay(w,R,S,15,False);prev=e.replay(old,R,os,15,False);C=run['C'];v,at=run['cuts']['seed']['values'],run['cuts']['seed']['charts'];ov=prev['cuts']['seed']['values'];oa=prev['cuts']['seed']['charts'];spec=w['affine_injections']+w['higher_shared_injections'];diff={}
 assert run['count']=={'INIT':108,'ADD':877,'MOVE':430,'CLEAR':108}and run['profile']=={1:106,2:64,3:56,4:13,5:71,6:23,7:96,8:1}
 assert w['targets']==old['targets']
 for s in spec:
  r=int(s['row_hex'],16);assert v[s['owner']]==r and at[s['owner']]==s['chart'];n=s['first_retention']or'P6';diff[n]=diff.get(n,0)^r
  assert not any(o[0]=='MOVE'and o[1]==s['owner']for o in w['operations'])
 for n in ov:assert v[n]==ov[n]^diff.get(n,0)and at[n]==oa[n]
 for j in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{j}']==[o for o in old['operations']if o[0]=='MOVE'and o[1]==f'X{j}']
 rank=lambda rows:len(e.basis(rows));extra=[1<<j for j in old['history_extra_query_roles']];assert rank(os+extra)==14
 allowed=[f['group']for f in old['forks']]+[old['h1_private_roles'][str(i)]for i in[4,74,78]]+[next(d['roles']for d in old['cache_metadata']if d['chart']==ch)for ch in['C1','C4','C3']]+[old['history_extra_query_roles']]
 boundary=[];patterns=[('zero',[[]for _ in range(10)]),('all_72',allowed)]
 for z,roles in enumerate(allowed):
  for j in roles:p0=[[]for _ in range(10)];p0[z]=[j];patterns.append((f'isolated_{z}_{j}',p0))
 for name,params in patterns:
  ww=build(old,params);rr=e.replay(ww,R,[int(x,16)for x in ww['seed_rows_hex']],15,False);h=sum(bool(g)for g in params[:3]);c=sum(bool(g)for g in params[6:9]);expect=prev['profile'].copy();expect[1]+=4*h+2*c;expect[2]-=2*h+c;assert rr['profile']==expect;boundary.append(name)
 # A separate raw-column trace checks acquisition before mutation.
 vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};owners={s['owner']for s in spec};captures=[]
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':vals[n]=0
  elif op=='ADD':
   t=q[0]
   if t in owners:assert n.startswith('X')and vals[n]==1<<int(n[1:]);captures.append({'step':step,'source':n,'owner':t,'row_hex':hex(vals[n])})
   vals[t]^=vals[n]
  elif op=='CLEAR':del vals[n]
 rejected=[];contracts=[]
 for s in spec:
  name=s['owner'];z=s['packet'];tests=[['ADD',name,f'P{z}']]+[['ADD',name,f'Y{i}']for i in s['old_receivers']]+[['CLEAR',name]]
  for op in tests:
   mut=copy.deepcopy(w);ix=mut['operations'].index(op);mut['operations'].pop(ix);mut['milestones']={k:-1 for k in w['milestones']};mut.pop('source_cut',None)
   try:e.replay(mut,R,S,15,False)
   except AssertionError:rejected.append(op)
   else:
    assert s['packet']==6 and op==['ADD',name,'P6'];contracts.append({'removed':op,'endpoints_still_valid':True,'declared_P6_terminal_rejected':True})
 result={'status':'PASS_72_PARAMETER_EXPANDED_SOURCE_INSTANCE','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'targets':w['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'actual_raw_captures':captures,'seed_cut_changes':{n:hex(r)for n,r in diff.items()},'all_other_seed_cut_rows_and_locations_unchanged':True,'original_X_routes_unchanged':True,'base_terminal_code_intersection_Extra6':0,'boundary_parameter_words':boundary,'semantic_negative_controls':rejected,'changed_terminal_contract_controls':contracts,'scope':'Actualprivate/pair/Extra6 acquisition changes with30 endpoints retained. No fullsupplier or newkappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');pr=invoice(run['profile']);pr['increment_from_thirty']=encode(moment({1:10,2:-5}));(a.out/'PRICE.json').write_text(json.dumps(pr,indent=2)+'\n');print(result['status'],run['count'],'Q',pr['moment']['lower'],'room',pr['limiting_room']['lower'],'boundaries',len(boundary),'controls',len(rejected))
if __name__=='__main__':main()
