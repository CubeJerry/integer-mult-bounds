#!/usr/bin/env python3
"""Independent all-column paid-port repair, stock and invoice audit."""
import argparse,copy,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 assert sha(a.base)=='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e';assert sha(a.word)=='8580350db073049f01268989d6acdb4bf770699a079760163a394d2867323c36'
 base=json.loads(a.base.read_text());w=json.loads(a.word.read_text());rt=Path(__file__).with_name('retained');e=load(rt/'source_history_engine.py','review');t=load(rt/'interval_price.py','price');source=a.repo/w['source_path'];assert sha(source)==w['source_sha256'];R=json.loads(source.read_text())['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];b=e.replay(base,R,S,15,False);r=e.replay(w,R,S,15,False);C=r['C'];v=r['cuts']['seed']['values'];at=r['cuts']['seed']['charts'];old=b['cuts']['seed'];rank=lambda rows:len(e.basis(rows))
 assert w['targets']==base['targets']and len(w['targets'])==34 and v==old['values'];assert{name for name in at if at[name]!=old['charts'][name]}=={'ZRAW0','ZKEEP2'};assert at['ZRAW0']==at['ZKEEP2']=='L29';assert v['ZRAW0']==1 and v['ZKEEP2']==sum(1<<j for j in [0,2,28,29])
 assert C['C2']==C['M1']and len(C['M1'])==5 and len(C['L29'])==1 and e.contained(C['L29'],C['M1'])and e.contained(C['L29'],C['Jnew2'])and e.contained(C['Jnew2'],C['F2'])
 vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};captured=False
 for k,o in enumerate(w['operations']):
  if o==['ADD','X0','ZRAW0']:
   assert not captured and w['operations'][k-1]==['MOVE','X0','C2']and vals['X0']==1 and C[loc['X0']]==C[loc['ZRAW0']]==C['M1'];assert w['operations'][k+1]==['MOVE','ZRAW0','L29'];captured=True
  if o[0]=='INIT':vals[o[1]]=0;loc[o[1]]=o[2]
  elif o[0]=='ADD':vals[o[2]]^=vals[o[1]]
  elif o[0]=='MOVE':loc[o[1]]=o[2]
  else:del vals[o[1]];del loc[o[1]]
 assert captured
 for j in range(111):assert[o for o in w['operations']if o[:2]==['MOVE',f'X{j}']]==[o for o in base['operations']if o[:2]==['MOVE',f'X{j}']]
 assert r['count']=={'INIT':114,'ADD':902,'MOVE':436,'CLEAR':114}and r['dirty_CLEAR']==114
 delta=Counter(r['profile']);delta.subtract(b['profile']);assert{k:x for k,x in delta.items()if x}=={4:1}
 ground=[x for n,x in v.items()if at[n]=='zero'and not n.startswith('Y')];nn=[n for n in v if at[n]not in ['zero','Hub']and not n.startswith('Y')and any(v[n]>>j&1 and not e.contained(C[f'L{j}'],C[at[n]])for j in range(111))];assert len(nn)==23 and rank(ground+[v[n]for n in nn])==36;assert rank(ground+[v[n]for n in nn]+[v[f'Y{j}']for j in range(111)])==147
 obs=[int(q['row_hex'],16)for q in r['snapshots']];assert len(obs)==283 and rank(obs)==85
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));bases=[]
 for i in range(111):
  visible={name for name,chart in C.items()if e.contained(chart,C[f'F{i}'])};rr=[x for n,x in v.items()if not n.startswith('Y')and at[n]in visible]+[x for x,q in zip(obs,r['snapshots'])if q['chart']in visible]+[1<<j for j in range(111)if dot(i,j)==0];bases.append(rr)
 known=set();waves=[]
 while True:
  nxt={i for i,rr in enumerate(bases)if e.solve(rr+[1<<j for j in sorted(known)],1<<i)is not None};assert known<=nxt
  if nxt==known:break
  waves.append(sorted(nxt-known));known=nxt
 assert sorted(known)==w['targets']
 duals=[]
 for i,rr in enumerate(bases):
  if i in known:continue
  rows=rr+[1<<j for j in sorted(known)];eq=rows+[1<<i];cols=[sum(((x>>j)&1)<<k for k,x in enumerate(eq))for j in range(111)];lam=e.solve(cols,1<<len(rows));assert lam is not None and lam>>i&1 and all(not((lam&x).bit_count()%2)for x in rows);duals.append({'receiver':i,'dual_hex':hex(lam)})
 tests=[['ADD','X0','ZRAW0'],['MOVE','ZRAW0','L29'],['ADD','P3','ZKEEP2'],['ADD','ZKEEP2','P3'],['ADD','ZRAW0','P3'],['ADD','ZKEEP2','Y2'],['ADD','ZCORR2','Y2'],['CLEAR','ZRAW0']];rejected=[]
 for op in tests:
  m=copy.deepcopy(w);assert m['operations'].count(op)==1;m['operations'].remove(op);m['milestones']={k:-1 for k in m['milestones']};m.pop('source_cut',None)
  try:e.replay(m,R,S,15,False)
  except AssertionError:rejected.append(op)
  else:raise AssertionError(('accepted deletion',op))
 m=copy.deepcopy(w);k=m['operations'].index(['INIT','ZRAW0','M1']);m['operations'][k]=['INIT','ZRAW0','L0'];m['milestones']={k:-1 for k in m['milestones']};m.pop('source_cut',None)
 try:e.replay(m,R,S,15,False)
 except AssertionError:rejected.append(['wrong_native_helper_birth'])
 else:raise AssertionError('accepted wrong native birth')
 h=w['singular_h'];extra=w['history_extra_query_roles'];banks=[([7,11,12],[1<<j for j in range(111)if h[j]==0]),([29,28,44],[1<<j for j in range(111)if h[j]==1 and j not in extra]),([19],[1<<j for j in extra]+[v['HKEEP_E6']]),([27],[1<<j for j in range(111)if h[j]==0]+[v['HKEEP_D7']])];coarse=[]
 for i in range(111):coarse.append([1<<j for j in w['targets']]+[1<<j for j in range(111)if dot(i,j)==0]+[x for ports,bank in banks if any(dot(i,d)==0 for d in ports)for x in bank])
 ck=set(w['targets'])
 while True:
  nxt={i for i,rr in enumerate(coarse)if e.solve(rr+[1<<j for j in sorted(ck)],1<<i)is not None}
  if nxt==ck:break
  ck=nxt
 assert sorted(set(range(111))-ck)==[46];assert all(not(x>>46&1)for x in coarse[46]+[1<<j for j in ck])
 B=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
 for j in range(1,9):B[1+7*j]+=Fraction(74,6);B[7*j]-=Fraction(74,6)
 B.subtract(r['profile']);out={'status':'PASS_INDEPENDENT_PAID_PORT29','word_sha256':sha(a.word),'base_sha256':sha(a.base),'native_source_sha256':sha(source),'all222_columns':True,'all_seed_values_identical':True,'only_seed_locations_changed':['ZRAW0','ZKEEP2'],'actual_raw_capture_verified':True,'all_original_routes_unchanged':True,'counts':r['count'],'dirty_CLEAR':114,'profile':r['profile'],'exact_increment':'4^(199/200)','price':t.report(t.interval(r['profile'])),'room':t.report(t.interval(B)),'principal_snapshots':283,'history_rank':85,'proper_nonlocal_count':23,'normalized_rank':36,'rank_including_Y':147,'strong_feedback_closure':sorted(known),'exclusion_duals':duals,'coarse_closure_count':len(ck),'coarse_excluded':46,'coarse_dual_hex':hex(1<<46),'negative_controls':rejected,'scope':'Same34 endpoints; paid placement experiment, not cheaper source or complete supplier. Unlimited separated-bank closure110 is not physical delivery.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:x for k,x in out.items()if k not in ['exclusion_duals','strong_feedback_closure']}))
if __name__=='__main__':main()
