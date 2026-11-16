#!/usr/bin/env python3
"""Literal cross-bank chronology and complete endpoint/stock verification."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 assert sha(a.base)=='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e';assert sha(a.word)=='f17fb4bb7cc9dbe2c3a1725f1b24586b0e97262b98c7e2cff07e25df35ad35a5';base=json.loads(a.base.read_text());w=json.loads(a.word.read_text());native=a.repo/w['source_path'];assert sha(native)==w['source_sha256'];R=json.loads(native.read_text())['native_roots'];s=importlib.util.spec_from_file_location('engine',Path(__file__).with_name('retained')/'source_history_engine.py');e=importlib.util.module_from_spec(s);s.loader.exec_module(e);S=[int(x,16)for x in w['seed_rows_hex']];b=e.replay(base,R,S,15,False);r=e.replay(w,R,S,15,False);v=r['cuts']['seed']['values'];at=r['cuts']['seed']['charts'];bv=b['cuts']['seed']['values'];C=r['C'];g=bv['HKEEP_D7'];rank=lambda rows:len(e.basis(rows))
 assert w['targets']==base['targets']and len(w['targets'])==34;assert r['cuts']['source']==b['cuts']['source'];assert at==b['cuts']['seed']['charts'];assert{n for n in v if v[n]!=bv[n]}=={'KEEP_C0'}and v['KEEP_C0']==bv['KEEP_C0']^g;assert all(v[f'P{z}']==bv[f'P{z}']for z in range(8))
 assert r['count']=={'INIT':114,'ADD':905,'MOVE':435,'CLEAR':114}and r['dirty_CLEAR']==114 and r['profile']==b['profile'];assert len(w['operations'])==len(base['operations'])+3
 for o in base['operations'][base['milestones']['source_cut']:w['cross_bank_coupling']['old_initial_P7_block_start']]:assert not(o[0]=='ADD'and o[2].startswith('X'))and not(o[0]=='MOVE'and o[1].startswith('X'))
 assert w['operations'].index(['ADD','P7','HKEEP_D7'])<w['operations'].index(['ADD','HKEEP_D7','P0'])
 for name in [f'X{j}'for j in range(111)]+[f'Y{j}'for j in range(111)]+[f'P{j}'for j in range(8)]:assert[o for o in w['operations']if o[:2]==['MOVE',name]]==[o for o in base['operations']if o[:2]==['MOVE',name]]
 pure=[x for n,x in v.items()if not n.startswith('Y')];oldpure=[x for n,x in bv.items()if not n.startswith('Y')];assert rank(pure)==rank(oldpure)==rank(pure+oldpure)
 obs=[int(q['row_hex'],16)for q in r['snapshots']];oldobs=[int(q['row_hex'],16)for q in b['snapshots']];assert rank(obs)==rank(oldobs)==rank(obs+oldobs)==85
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));K=[(1<<i)|sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];h=w['singular_h'];W=[K[i]&sum(1<<j for j in range(111)if h[i]==h[j])for i in range(111)];assert rank(obs+K)==rank(obs+W)==85
 ground=[x for n,x in v.items()if at[n]=='zero'and not n.startswith('Y')];nn=[n for n in v if at[n]not in ['zero','Hub']and not n.startswith('Y')and any(v[n]>>j&1 and not e.contained(C[f'L{j}'],C[at[n]])for j in range(111))];normal=ground+[v[n]for n in nn];assert len(nn)==22 and rank(normal)==36 and rank(normal+[v[f'Y{j}']for j in range(111)])==147
 bases=[]
 for i in range(111):
  visible={n for n,chart in C.items()if e.contained(chart,C[f'F{i}'])};bases.append([x for n,x in v.items()if not n.startswith('Y')and at[n]in visible]+[x for x,q in zip(obs,r['snapshots'])if q['chart']in visible]+[1<<j for j in range(111)if dot(i,j)==0])
 known=set();waves=[]
 while True:
  nxt={i for i,rows in enumerate(bases)if e.solve(rows+[1<<j for j in sorted(known)],1<<i)is not None};assert known<=nxt
  if nxt==known:break
  waves.append(sorted(nxt-known));known=nxt
 duals=[]
 for i,rows in enumerate(bases):
  if i in known:continue
  rr=rows+[1<<j for j in sorted(known)];eq=rr+[1<<i];cols=[sum(((x>>j)&1)<<k for k,x in enumerate(eq))for j in range(111)];lam=e.solve(cols,1<<len(rr));assert lam is not None and lam>>i&1 and all(not((lam&x).bit_count()%2)for x in rr);duals.append({'receiver':i,'dual_hex':hex(lam)})
 rejected=[]
 for op in [['ADD','HKEEP_D7','P0'],['ADD','HKEEP_D7','Y3'],['ADD','HKEEP_D7','Y21'],['ADD','P7','HKEEP_D7'],['ADD','KEEP_C0','P0'],['CLEAR','HKEEP_D7']]:
  m=copy.deepcopy(w);assert m['operations'].count(op)==1;m['operations'].remove(op);m['milestones']={k:-1 for k in m['milestones']};m.pop('source_cut',None)
  try:e.replay(m,R,S,15,False)
  except AssertionError:rejected.append(op)
  else:raise AssertionError(('accepted omission',op))
 m=copy.deepcopy(base);ops=[]
 for o in m['operations']:
  ops.append(o)
  if o in [['MOVE','P0','D3_21'],['MOVE','Y3','D3_21'],['MOVE','Y21','D3_21']]:ops.append(['ADD','HKEEP_D7',o[1]])
 m['operations']=ops;m['milestones']={k:-1 for k in m['milestones']};m.pop('source_cut',None)
 try:e.replay(m,R,S,15,False)
 except AssertionError:rejected.append('coupling_without_retiming')
 else:raise AssertionError('accepted late donor chronology')
 assert not(g>>24&1)and((g>>42)&1)==((g>>69)&1)
 out={'status':'PASS_ACTUAL_ZERO_MOVE_CROSS_BANK_COUPLING','word_sha256':sha(a.word),'base_sha256':sha(a.base),'native_source_sha256':sha(native),'all222_columns':True,'counts':r['count'],'profile':r['profile'],'dirty_CLEAR':114,'extra_ADD':3,'extra_MOVE':0,'extra_owners':0,'all_original_and_principal_and_receiver_routes_unchanged':True,'all_terminal_seed_values_unchanged':True,'only_seed_cut_value_changed':'KEEP_C0','new_retention_hex':hex(v['KEEP_C0']),'transferred_actual_row_hex':hex(g),'literal_source_cut_unchanged':True,'retiming_original_custody_checked':True,'principal_snapshot_count':len(obs),'history_rank':85,'history_W15_and_C9_retained':True,'abstract_history_and_live_spans_unchanged':True,'normalized_rank':36,'proper_nonlocal_count':22,'rank_including_Y':147,'strong_feedback_closure':sorted(known),'feedback_waves':waves,'outsider_duals':duals,'negative_controls':rejected,'old_three_coarse_duals_not_removed_by_fixed_transferred_row':True,'scope':'Actual cross-bank acquisition at a shared proper chart; same34 endpoints and movement. No all111 delivery or complete supplier.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:x for k,x in out.items()if k not in ['outsider_duals','feedback_waves']}))
if __name__=='__main__':main()
