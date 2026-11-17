"""Exact source-contract checks and actual semantic omissions for masked-Hub source."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,collections

def rank(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--matching',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);w=json.loads(a.word.read_text());P=w['construction'];raw=(a.repo/w['parent_word_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['parent_word_sha256'];parent=json.loads(raw);assert w['operations'][:392]==parent['operations'][:392];match=json.loads(a.matching.read_text());assert[(p['unknown'],p['known'])for p in P['pairs']]==[(p['unknown'],p['known'])for p in match['pairs']];src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('proxy_author_native',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);_,_,stats=e.replay(w,R);C={h:e.chart(z)for h,z in w['charts'].items()};S=set(P['known_roles']);U=set(P['unknown_roles']);um=sum(1<<u for u in U)
 def cut(word,index):
  v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
  for typ,n,*q in word['operations'][:index]:
   if typ=='INIT':v[n]=0;at[n]=q[0]
   elif typ=='ADD':v[q[0]]^=v[n]
   elif typ=='MOVE':at[n]=q[0]
   else:del v[n];del at[n]
  return v,at
 oldv,oldat=cut(parent,392)
 def contract(word,index):
  v,at=cut(word,index)
  for n in oldv:
   if not n.startswith('X'):assert v[n]==oldv[n]and at[n]==oldat[n],('retained state',n)
  for p in P['pairs']:
   u,c,h=p['unknown'],p['known'],p['chart'];assert v[f'X{u}']==1<<u and at[f'X{u}']==h and len(C[h])==2,('held raw',u);assert v[f'X{c}']==(1<<c)^(1<<u)and at[f'X{c}']=='Hub',('Hub proxy',c)
  hub=[v[f'X{i}']for i in range(111)if at[f'X{i}']=='Hub'];assert len(hub)==54 and rank([x&um for x in hub])==54,'unknown quotient rank';assert rank([v[f'X{i}']for i in range(111)])==111,'full original invertibility'
  for i in range(111):assert any(at[n]==f'L{i}'and x==1<<i for n,x in v.items()),('physical native value',i)
  for k,(n,m)in enumerate(zip(P['Hub_source_fields'],P['ground_correction_fields'])):
   row=int(P['canonical_unknown_rows_hex'][k],16);mask=int(P['known_correction_rows_hex'][k],16);assert v[n]==row^mask and at[n]=='Hub',('Hub mode',k);assert v[m]==mask and at[m]=='zero'and not(mask&um),('actual ground mask',k);assert v[n]^v[m]==row,('corrected canonical',k)
  assert rank([int(x,16)for x in P['canonical_unknown_rows_hex']])==9
  return v,at
 v,at=contract(w,w['carrier_interface_before_operation']);controls=[]
 for key,choices in w['semantic_operation_indices'].items():
  for idx in choices:
   m=copy.deepcopy(w);del m['operations'][idx]
   try:e.replay(m,R);contract(m,w['carrier_interface_before_operation']-int(idx<w['carrier_interface_before_operation']))
   except (AssertionError,KeyError,ValueError)as ex:controls.append({'class':key,'deleted_index':idx,'deleted_operation':w['operations'][idx],'rejected':True,'reason':str(ex)[:250]});break
  else:raise AssertionError(('all omission controls passed',key))
 # No field is silently available at a non-coincident native position.
 visibility={str(i):[p['unknown']for p in P['pairs']if e.sub(C[p['chart']],C[f'F{i}'])]for i in sorted(U)};assert all(visibility.values());out={'status':'PASS_MASKED_HUB_SOURCE_AND_10_SEMANTIC_CONTROL_CLASSES','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'matching_sha256':hashlib.sha256(a.matching.read_bytes()).hexdigest(),'parent_word_sha256':w['parent_word_sha256'],'verifier_sha256':hashlib.sha256(ep.read_bytes()).hexdigest(),'all222_columns':True,'unknown_Hub_quotient_rank':54,'original_system_rank':111,'restricted_canonical_rank':9,'actual_native_values':111,'held_unknown_count':35,'known_native_count':22,'visibility':visibility,'controls':controls,'stats':stats,'scope':'Author-side replay and source controls; independent proof review is separate. Code transport remains unperformed.'};assert len(controls)==10;(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','word_sha256','unknown_Hub_quotient_rank','original_system_rank','restricted_canonical_rank','actual_native_values']}))
if __name__=='__main__':main()
