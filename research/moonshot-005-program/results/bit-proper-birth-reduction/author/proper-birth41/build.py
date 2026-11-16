#!/usr/bin/env python3
"""Relocate the births of two still-zero owned packets to their first read charts."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
BASE='b18c138efaf2d771197c46ef3ae2a5fc312c322694ef020e41cace70d7662e11'
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def zero_moves(word):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owned=set();found=[]
 for step,o in enumerate(word['operations'],1):
  op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0];owned.add(n)
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='MOVE':
   if n in owned and v[n]==0:found.append({'step':step,'field':n,'from':at[n],'to':q[0]})
   at[n]=q[0]
  elif op=='CLEAR':del v[n],at[n];owned.remove(n)
 return found

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);e=load(a.engine,'e');price=load(a.price_engine,'price');src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots'];C,H,orep=e.replay(old,R)
 changes={'P6':('Extra6','EXTRA_AFF'),'P7':('D3_21','AFF0')};w=copy.deepcopy(old);ops=[];witnesses=[]
 for name,(chart,source)in changes.items():
  uses=[(k,o)for k,o in enumerate(old['operations'])if o[1]==name or(o[0]=='ADD'and o[2]==name)]
  assert [o for _,o in uses[:3]]==[['INIT',name,'Hub'],['MOVE',name,chart],['ADD',source,name]]
  assert len(C['Hub'])-len(C[chart])==2
  witnesses.append({'packet':name,'first_three_uses':uses[:3],'old_birth':'Hub','new_birth':chart,'removed_empty_descent_rank':2,'first_actual_read_source':source})
 for o in old['operations']:
  if o[0]=='INIT'and o[1]in changes:ops.append(['INIT',o[1],changes[o[1]][0]])
  elif o[0]=='MOVE'and o[1]in changes and o[2]==changes[o[1]][0]:pass
  else:ops.append(o)
 w['operations']=ops;w['base_word_sha256']=BASE;w['schema']='endpoint-local-birth-native-word-v1';w['zero_birth_relocations']=witnesses;w['scope']='Same41 endpoints after relocating only still-zero P6/P7 births. Prior source histories/stock are not inherited; no complete supplier or new kappa.'
 C,H,rep=e.replay(w,R);zb=zero_moves(old);za=zero_moves(w);assert len(zb)==2 and {r['field']for r in zb}=={'P6','P7'} and not za;expected=orep['movement_profile'].copy();expected[2]-=2;assert rep['movement_profile']==expected
 assert rep['counts']=={k:v-(2 if k=='MOVE'else 0)for k,v in orep['counts'].items()};assert rep['dirty_CLEAR']==118
 Q=price.moment(rep['movement_profile']);B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 limit=tuple(x/6 for x in price.moment(B));room=(limit[0]-Q[1],limit[1]-Q[0]);saving=price.moment({2:2})
 bads=[]
 for name in changes:
  bad=copy.deepcopy(w);i=bad['operations'].index(['INIT',name,changes[name][0]]);bad['operations'][i]=['INIT',name,'zero']
  try:e.replay(bad,R)
  except AssertionError as ex:bads.append({'wrong_birth':name,'chart':'zero','rejected':str(ex)})
  else:raise AssertionError('accepted inaccessible birth')
 a.out.mkdir(parents=True,exist_ok=True);encoded=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(encoded);out={'status':'PASS_ACTUAL_ZERO_BIRTH_LOCALIZED41','word_sha256':hashlib.sha256(encoded).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':old['source_sha256'],'before':orep,'after':rep,'birth_witnesses':witnesses,'exact_movement_saving':'2[2]','independent_price':{'moment':price.display(Q),'limiting_room':price.display(room),'saving':price.display(saving)},'negative_controls':bads,'all_owned_zero_moves_before':zb,'all_owned_zero_moves_after':za,'targets':w['targets'],'no_inherited_source_cut_metadata':True,'scope':'Endpoint-only formal source, still41 targets. All prior omitted histories and all global foundations remain unproved; no full supplier or new kappa.'};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','word_sha256','after','independent_price']}))
if __name__=='__main__':main()
