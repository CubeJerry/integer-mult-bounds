"""Literal replay and destructive controls for the frozen D4 routing candidate."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads(a.word.read_text());src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];p=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';s=importlib.util.spec_from_file_location('d4_control_native',p);e=importlib.util.module_from_spec(s);s.loader.exec_module(e);_,_,stats=e.replay(w,R)
 def cutcheck(word,cut):
  v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
  for typ,n,*q in word['operations'][:cut]:
   if typ=='INIT':v[n]=0;at[n]=q[0]
   elif typ=='ADD':v[q[0]]^=v[n]
   elif typ=='MOVE':at[n]=q[0]
   else:del v[n];del at[n]
  for i in range(111):
   assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub',('raw X cut',i)
   assert v[f'NATIVE_RAW_{i}']==1<<i and at[f'NATIVE_RAW_{i}']==f'L{i}',('native cache cut',i)
   assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in word['targets']else 0),('Y cut',i)
  for g,G in enumerate(word['construction']['groups']):assert v[f'GROUP_SUM_{g}']==sum(1<<j for j in G['donors']),('group cut',g)
  for q in word['construction']['routes']:
   row=sum(1<<j for j in word['construction']['groups'][q['group']]['donors'])^((1<<q['carrier'])if q['masked']else 0)
   assert v[f'ROUTE_{q["route"]}_FACET']==row,('route facet cut',q['route'])
   if q['plane']is not None:assert v[f'ROUTE_{q["route"]}_PLANE']==row,('route plane cut',q['route'])
  return True
 assert cutcheck(w,w['carrier_interface_before_operation'])
 # Delete an actual semantic operation.  The cut moves back by one operation;
 # no omitted check is rejected merely because its numerical index changed.
 results=[]
 for key in ['native_captures','common_captures','mask_captures','group_captures','pivot_coding','cohort_descents','masked_injections','route_deposits','carrier_restorations','canonical_loads','canonical_descents','canonical_preloads','receiver_reads']:
  for idx in w['semantic_operation_indices'][key]:
   mutant=copy.deepcopy(w);del mutant['operations'][idx]
   try:
    e.replay(mutant,R)
    cutcheck(mutant,w['carrier_interface_before_operation']-int(idx<w['carrier_interface_before_operation']))
   except (AssertionError,KeyError,ValueError)as ex:results.append({'kind':key,'deleted_index':idx,'deleted_operation':w['operations'][idx],'rejected':True,'reason':str(ex)[:220]});break
  else:raise AssertionError(('all controls unexpectedly passed',key))
 assert len(results)==13 and all(z['rejected']for z in results)
 out={'status':'PASS_D4_ROUTING_AND_13_DESTRUCTIVE_CONTROL_CLASSES','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stats':stats,'controls':results,'scope':'Author-side exact replay and omissions; independent proof review remains separate.'};a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'controls':len(results),'word_sha256':out['word_sha256']}))
if __name__=='__main__':main()
