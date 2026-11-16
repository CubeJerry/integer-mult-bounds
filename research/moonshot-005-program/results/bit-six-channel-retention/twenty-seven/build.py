#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,copy
BASE='1253ce71d23750d912ca9b43837c9b0193c61ecebf967fe44287d2bdc195522d'
SPEC=[(3,0,2,29,['H6_0','Q2'],[0,28],'E6',4),(4,28,43,46,['H6_1','H6_3','Q2'],[28,44],'E75',74),(5,44,48,45,['H6_2','H6_3','Q2'],[0,44],'E79',78)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);R=json.loads((a.repo/old['source_path']).read_text())['native_roots'];w=copy.deepcopy(old);fields={c['name']:int(c['row_hex'],16)for c in old['history_cache_metadata']}|{c['name']:sum(1<<j for j in c['roles'])for c in old['cache_metadata']};defs=[];ops=[];source={};owners=[]
 for z,d,b,u,recipe,donors,early,oldi in SPEC:
  h=0
  for n in recipe:h^=fields[n]
  assert h==sum(1<<j for j in donors+[b,u]);pre=int(old['seed_rows_hex'][z],16)^(1<<int(early[1:]));w['charts'][f'Jnew{b}']={'kind':'span','rows':[R[d],R[u]]};owners +=[f'ZRAW{d}',f'ZCORR{b}',f'ZFIRST{z}',f'ZKEEP{b}'];ops +=[['INIT',f'ZRAW{d}',f'L{d}'],['ADD',f'X{d}',f'ZRAW{d}'],['INIT',f'ZCORR{b}',f'Jnew{b}'],['INIT',f'ZFIRST{z}','M1'],['INIT',f'ZKEEP{b}',f'L{d}']]
  source.update({f'ZRAW{d}':{'chart':f'L{d}','row_hex':hex(1<<d)},f'ZCORR{b}':{'chart':f'Jnew{b}','row_hex':hex(1<<u)},f'ZFIRST{z}':{'chart':'M1','row_hex':'0x0'},f'ZKEEP{b}':{'chart':f'L{d}','row_hex':'0x0'}});defs.append({'packet':z,'d':d,'b':b,'u':u,'h_hex':hex(h),'h_recipe':recipe,'donor_preloads':donors,'early':early,'old_receiver':oldi,'first_retention_hex':hex(pre)});w['seed_rows_hex'][z]=hex((1<<d)^(1<<int(early[1:])))
 marks={};replaced=[];retired=False;visited=[]
 for step,o in enumerate(old['operations'],1):
  q=next((q for q in defs if o==['MOVE',f"P{q['packet']}",'zero']),None)
  cap=next((q for q in defs if o==['MOVE',f"X{q['u']}",'C2']),None)
  oldpre=next((q for q in defs if o==['ADD',f"P{q['packet']}",f"Y{q['old_receiver']}"]),None)
  oldarr=next((q for q in defs if o==['MOVE',f"Y{q['old_receiver']}",'M1']),None)
  new=next((q for q in defs if o==['MOVE',f"Y{q['b']}",f"F{q['b']}"]),None)
  if q:
   z,d,b=[q[k]for k in ['packet','d','b']];ops +=[['ADD',f'P{z}',f'ZFIRST{z}'],['ADD',f'ZFIRST{z}',f'P{z}']]+[['ADD',n,f'P{z}']for n in q['h_recipe']]+[['MOVE',f'P{z}',f'L{d}'],['ADD',f'P{z}',f'ZKEEP{b}'],['ADD',f'ZKEEP{b}',f'P{z}'],['ADD',f'ZRAW{d}',f'P{z}'],o];replaced.append(z)
  elif cap:ops +=[['MOVE',o[1],f"Jnew{cap['b']}"],['ADD',o[1],f"ZCORR{cap['b']}"],o];visited.append(cap['u'])
  elif oldpre:ops.append(['ADD',oldpre['early'],o[2]])
  elif oldarr:ops +=[o,['ADD',f"ZFIRST{oldarr['packet']}",o[1]]]
  elif new:
   b,d=[new[k]for k in ['b','d']];ops +=[['MOVE',f'Y{b}',f'L{d}'],['ADD',f'ZKEEP{b}',f'Y{b}'],['MOVE',f'Y{b}',f'Jnew{b}'],['ADD',f'ZCORR{b}',f'Y{b}'],o];marks[f'completed_{b}']=len(ops)
  else:
   if o[0]=='CLEAR'and not retired:ops +=[['CLEAR',n]for n in owners];retired=True
   ops.append(o)
   for q in defs:
    if o==['MOVE',f"Y{q['d']}",f"F{q['d']}"]:marks[f"completed_{q['d']}"]=len(ops)
  for k,v in old['milestones'].items():
   if v==step:marks[k]=len(ops)
  if step==old['milestones']['seed8_before_Y']:
   for q in defs:
    d,b,z=[q[k]for k in ['d','b','packet']];ops +=[['ADD',f'P{z}',f'Y{d}'],['ADD',q['early'],f'Y{d}']]
    for donor in q['donor_preloads']:
     m=next(t for t in defs if t['d']==donor);ops +=[['ADD',f"P{m['packet']}",f'Y{b}'],['ADD',m['early'],f'Y{b}']]
 assert replaced==[3,4,5]and sorted(visited)==[29,45,46]
 w.update({'schema':'actual-six-double-retentions-twentyseven-v1','base_word_sha256':BASE,'operations':ops,'milestones':marks,'targets':sorted(old['targets']+[q[k]for q in defs for k in ['d','b']]),'m1_retention':defs,'ground_code':'Six masked raw point terminals plus two canonical terminals; allsix old active rows retained atactualM0/M1 andsixproperkernels retained atactualnative lines.'});w['source_cut'].update(source);a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print('WORD',hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),'ops',len(ops))
if __name__=='__main__':main()
