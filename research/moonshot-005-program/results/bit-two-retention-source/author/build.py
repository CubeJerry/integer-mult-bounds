#!/usr/bin/env python3
"""Literal two-retention extension of the pinned changed-code source."""
import argparse,copy,hashlib,json
from pathlib import Path
BASE='1da8ac07063da93aaf002fa6feeb6de4ec1aa327a7740f3f61747abd559d14d0'
H=int('60000c00180a0',16)
D=7;TARGET=16;CORRECTION=H^(1<<TARGET);ROLES=[i for i in range(111)if CORRECTION>>i&1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];roots=json.loads(src)['native_roots'];w=copy.deepcopy(old)
 w['schema']='actual-two-retention-seventeen-v1';w['base_word_sha256']=BASE;w['targets']=sorted(old['targets']+[D,TARGET]);w['seed_rows_hex'][0]=hex(1<<D);w['charts']['J16']={'kind':'span','rows':[roots[i]for i in ROLES]};w['operations']=ops=[['INIT','EARLY7','L7'],['ADD','X7','EARLY7'],['INIT','CORR16','J16'],['INIT','KEEP_C0','C0'],['INIT','KEEP_L7','L7']];marks={};replaced=0;visited=[]
 for step,o in enumerate(old['operations'],1):
  if o==['MOVE','P0','zero']:
   ops +=[['ADD','P0','KEEP_C0'],['ADD','KEEP_C0','P0'],['ADD','H1_0','P0'],['ADD','Q0','P0'],['MOVE','P0','L7'],['ADD','P0','KEEP_L7'],['ADD','KEEP_L7','P0'],['ADD','EARLY7','P0'],['MOVE','P0','zero']];replaced+=1
  elif o[0]=='MOVE'and o[1].startswith('X')and int(o[1][1:])in ROLES and o[2]=='C0':
   ops +=[['MOVE',o[1],'J16'],['ADD',o[1],'CORR16'],o];visited.append(int(o[1][1:]))
  elif o in [['ADD','P0','Y3'],['ADD','P0','Y21']]:pass
  elif o==['MOVE','Y16','F16']:
   ops +=[['MOVE','Y16','L7'],['ADD','KEEP_L7','Y16'],['MOVE','Y16','J16'],['ADD','CORR16','Y16'],['MOVE','Y16','F16']];marks['completed_16']=len(ops)
  else:
   if o[0]=='CLEAR'and not any(v[0]=='CLEAR'for v in ops):ops +=[['CLEAR','EARLY7'],['CLEAR','CORR16'],['CLEAR','KEEP_C0'],['CLEAR','KEEP_L7']]
   ops.append(o)
   if o in [['MOVE','Y3','M0'],['MOVE','Y21','M0']]:ops.append(['ADD','KEEP_C0',o[1]])
   if o==['MOVE','Y7','F7']:marks['completed_7']=len(ops)
  for k,v in old['milestones'].items():
   if v==step:marks[k]=len(ops)
  if step==old['milestones']['seed8_before_Y']:ops.append(['ADD','P0','Y7'])
 assert replaced==1 and sorted(visited)==ROLES,(replaced,visited,ROLES)
 w['milestones']=marks;w['source_cut'].update({'EARLY7':{'row_hex':hex(1<<7),'chart':'L7'},'CORR16':{'row_hex':hex(CORRECTION),'chart':'J16'},'KEEP_C0':{'row_hex':'0x0','chart':'C0'},'KEEP_L7':{'row_hex':'0x0','chart':'L7'}})
 w.pop('seed_metadata',None);w.pop('principal_query_reads',None);w['principal_routes'][0]=['F3','D3_21','M0','L7','zero'];w['ground_code']='Previous U8 with A3 replaced by the actual raw x7 terminal; E6 unchanged';w['history_claim']='Actual old W15+C9 histories persist. New mixed proper kernels are A3 at C0 and h at L7; h is actually consumed by Y16.';w['double_retention']={'first_chart':'C0','first_owner':'KEEP_C0','first_value_hex':old['seed_rows_hex'][0],'second_chart':'L7','second_owner':'KEEP_L7','second_value_hex':hex(H),'second_source_names':['H1_0','Q0'],'terminal_hex':hex(1<<7),'early_raw_owner':'EARLY7','correction_owner':'CORR16','correction_chart':'J16','correction_roles':ROLES,'correction_hex':hex(CORRECTION),'new_targets':[7,16],'old_completed_targets':old['targets']};a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print('WORD',hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),'operations',len(ops))
if __name__=='__main__':main()
