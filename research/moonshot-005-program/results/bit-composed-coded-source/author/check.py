#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,importlib.util
from cross_builder import build as cross
from port_builder import build as port
from price import invoice
BASE='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e';PORT='204e38b8c56f17cc3e88a475d4c75e5613ed4215e29c6ede33e55a3e614a82b1';CROSS='f17fb4bb7cc9dbe2c3a1725f1b24586b0e97262b98c7e2cff07e25df35ad35a5'
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--port',type=Path,required=True);p.add_argument('--cross',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();br=a.base.read_bytes();pr=a.port.read_bytes();cr=a.cross.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE and hashlib.sha256(pr).hexdigest()==PORT and hashlib.sha256(cr).hexdigest()==CROSS;w0=json.loads(br);wp=json.loads(pr);wc=json.loads(cr)
 assert port(w0)['operations']==wp['operations']and cross(w0)['operations']==wc['operations'];w=cross(wp);reverse=port(wc);assert w['operations']==reverse['operations']and w['milestones']==reverse['milestones'];w['base_word_sha256']=PORT;w['composition_sources']={'common_base':BASE,'port41':PORT,'cross_bank':CROSS};w['affine_scope']='Exactcompositionofprotectedcodedport41andzeroMOVEcross-bankcoupling. All34preserved; no fullsupplierornewkappa.'
 ep=Path(__file__).with_name('retained')/'source_history_engine.py';spec=importlib.util.spec_from_file_location('engine',ep);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];run=e.replay(w,R,S,15,False);prior=e.replay(wp,R,S,15,False);v,at=run['cuts']['seed']['values'],run['cuts']['seed']['charts'];pv,pa=prior['cuts']['seed']['values'],prior['cuts']['seed']['charts'];g=int(w['cross_bank_coupling']['transported_row_hex'],16)
 assert run['count']=={'INIT':115,'ADD':908,'MOVE':436,'CLEAR':115}and run['profile']==prior['profile']and run['dirty_CLEAR']==115
 assert at==pa
 for n in pv:assert v[n]==pv[n]^(g if n=='KEEP_C0'else 0)
 assert w['targets']==wp['targets']==wc['targets']and w['seed_rows_hex']==wp['seed_rows_hex']==wc['seed_rows_hex']
 def inventory(ww):
  vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};C=run['C']
  for o in ww['operations']:
   op,n,*q=o
   if op=='INIT':vals[n]=0;loc[n]=q[0]
   elif op=='MOVE':loc[n]=q[0]
   elif op=='ADD':
    if o==['ADD','BACK2','P3']:return {n:hex(r)for n,r in vals.items()if n!='P3'and r.bit_length()<=111 and C[loc[n]]==C['M1']}
    vals[q[0]]^=vals[n]
   elif op=='CLEAR':del vals[n],loc[n]
  raise AssertionError('no reset')
 available=inventory(w);assert available==inventory(wp);assert available['Q1']==hex(v['Q1'])
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw);out={'status':'PASS_COMPOSED_CODED_SOURCE','word_sha256':hashlib.sha256(raw).hexdigest(),'composition_sources':w['composition_sources'],'input_columns':222,'targets':w['targets'],'counts':run['count'],'movement_profile':run['profile'],'dirty_CLEAR':115,'transforms_commute_as_exact_operation_words':True,'milestones_equal_in_both_orders':True,'seed_cut_change_from_port41_only_KEEP_C0':hex(g),'all_terminal_rows_unchanged':True,'actual_M1_recipe_inventory_unchanged':available,'actual_M1_recipe_rank':len(e.basis(int(x,16)for x in available.values())),'scope':'Exactcompositionofreviewedsourcewords;all34remain,complete111decoderandnewkappaopen.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'PRICE.json').write_text(json.dumps(invoice(run['profile']),indent=2)+'\n');print(out['word_sha256'],out['status'],run['count'])
if __name__=='__main__':main()
