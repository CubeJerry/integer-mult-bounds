#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,copy
BASE='1da8ac07063da93aaf002fa6feeb6de4ec1aa327a7740f3f61747abd559d14d0'
PAIRS=[(0,7,16,['H1_0','Q0']),(1,11,23,['H1_1','Q0']),(2,12,22,['H1_0','H1_1','Q0'])]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);R=json.loads((a.repo/old['source_path']).read_text())['native_roots'];w=copy.deepcopy(old);fields={c['name']:int(c['row_hex'],16)for c in old['history_cache_metadata']}|{c['name']:sum(1<<j for j in c['roles'])for c in old['cache_metadata']};w['charts']['SH2']={'kind':'span','rows':[R[5],R[15]]};defs=[];inits=[['INIT','SHARED','SH2']];newowners=['SHARED'];source={'SHARED':{'row_hex':hex((1<<5)^(1<<15)),'chart':'SH2'}}
 for z,d,b,recipe in PAIRS:
  h=0
  for n in recipe:h^=fields[n]
  correction=h^(1<<b);unique=correction^((1<<5)^(1<<15));roles=[j for j in range(111)if correction>>j&1];ur=[j for j in range(111)if unique>>j&1];early=old['seed_metadata'][z]['early_point_reads'];emask=sum(1<<int(n[1:])for n in early);pre=int(old['seed_rows_hex'][z],16)^emask;w['charts'][f'J{b}']={'kind':'span','rows':[R[j]for j in roles]};w['charts'][f'M{b}']={'kind':'span','rows':[R[5],R[15],R[d]]};newowners +=[f'RAW{d}',f'PRIVATE{b}',f'KEEP_C{z}',f'KEEP_M{b}']
  inits +=[['INIT',f'RAW{d}',f'L{d}'],['ADD',f'X{d}',f'RAW{d}'],['INIT',f'PRIVATE{b}',f'J{b}'],['INIT',f'KEEP_C{z}','C0'],['INIT',f'KEEP_M{b}',f'L{d}']]
  source.update({f'RAW{d}':{'row_hex':hex(1<<d),'chart':f'L{d}'},f'PRIVATE{b}':{'row_hex':hex(unique),'chart':f'J{b}'},f'KEEP_C{z}':{'row_hex':'0x0','chart':'C0'},f'KEEP_M{b}':{'row_hex':'0x0','chart':f'L{d}'}})
  oldrec=[3,76,80][z];newrec=next(f['new_receiver']for f in old['forks']if f['old_receiver']==oldrec);defs.append({'packet':z,'d':d,'b':b,'h_hex':hex(h),'h_recipe':recipe,'unique_roles':ur,'unique_hex':hex(unique),'correction_roles':roles,'early_corrections':early,'ground_mask_hex':hex(emask),'first_retention_hex':hex(pre),'old_receivers':[oldrec,newrec]});w['seed_rows_hex'][z]=hex((1<<d)^emask)
 w['operations']=ops=inits;marks={};visited=[];replaced=[];retired=False
 for step,o in enumerate(old['operations'],1):
  pp=next((q for q in defs if o==['MOVE',f"P{q['packet']}",'zero']),None)
  yy=next((q for q in defs if o[0]=='ADD'and o[1]==f"P{q['packet']}"and o[2]in[f'Y{i}'for i in q['old_receivers']]),None)
  arrival=next((q for q in defs if o[0]=='MOVE'and o[1]in[f'Y{i}'for i in q['old_receivers']]and o[2]=='M0'),None)
  b=next((q for q in defs if o==['MOVE',f"Y{q['b']}",f"F{q['b']}"]),None)
  if pp:
   z,d,t=[pp[k]for k in ['packet','d','b']];ops +=[['ADD',f'P{z}',f'KEEP_C{z}'],['ADD',f'KEEP_C{z}',f'P{z}']]+[['ADD',n,f'P{z}']for n in pp['h_recipe']]+[['MOVE',f'P{z}',f'M{t}'],['ADD',f'P{z}',f'Y{t}'],['MOVE',f'Y{t}',f'J{t}'],['ADD',f'PRIVATE{t}',f'Y{t}'],['MOVE',f'Y{t}',f'F{t}']];marks[f'completed_{t}']=len(ops);ops +=[['MOVE',f'P{z}',f'L{d}'],['ADD',f'P{z}',f'KEEP_M{t}'],['ADD',f'KEEP_M{t}',f'P{z}'],['ADD',f'RAW{d}',f'P{z}'],o];replaced.append(z)
  elif o[0]=='MOVE'and o[1].startswith('X')and o[2]=='C0':
   j=int(o[1][1:]);q=next((q for q in defs if j in q['unique_roles']),None)
   if j in[5,15]:ops +=[['MOVE',o[1],'SH2'],['ADD',o[1],'SHARED']]
   elif q:ops +=[['MOVE',o[1],f"J{q['b']}"],['ADD',o[1],f"PRIVATE{q['b']}"]];visited.append(j)
   ops.append(o)
  elif yy:ops +=[['ADD',n,o[2]]for n in yy['early_corrections']]
  elif arrival:ops +=[o,['ADD',f"KEEP_C{arrival['packet']}",o[1]]]
  elif b:pass
  else:
   if o[0]=='CLEAR'and not retired:ops +=[['CLEAR',n]for n in newowners];retired=True
   ops.append(o)
   for q in defs:
    if o==['MOVE',f"Y{q['d']}",f"F{q['d']}"]:marks[f"completed_{q['d']}"]=len(ops)
  for k,v in old['milestones'].items():
   if v==step:marks[k]=len(ops)
  if step==old['milestones']['source_cut']:
   for q in defs:ops +=[['MOVE',f"Y{q['b']}",'SH2'],['ADD','SHARED',f"Y{q['b']}"],['MOVE',f"Y{q['b']}",f"M{q['b']}"]]
  if step==old['milestones']['seed8_before_Y']:
   for q in defs:ops +=[['ADD',f"P{q['packet']}",f"Y{q['d']}"]]+[['ADD',n,f"Y{q['d']}"]for n in q['early_corrections']]
 assert replaced==[0,1,2]and len(visited)==len(set(visited))==15
 w.update({'schema':'actual-three-double-retentions-twentyone-v1','base_word_sha256':BASE,'targets':sorted(old['targets']+[q[k]for q in defs for k in ['d','b']]),'milestones':marks,'ground_code':'Actual U8 principal terminals with three first h0 values replaced by masked raw7,11,12; six E points unchanged','multi_retention':defs,'early_completed_targets':[q['b']for q in defs],'extra_source_cut':source});w['source_cut'].update(source);w.pop('seed_metadata',None);w.pop('principal_query_reads',None);w['history_claim']='All actual predecessor W15 and C9 history values survive before three resets; three actual nonlocal native-line retentions and interleaved rank3 deliveries complete new receivers with shared rank2 and private rank4 source caches.';a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print('WORD',hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),'operations',len(ops))
if __name__=='__main__':main()
