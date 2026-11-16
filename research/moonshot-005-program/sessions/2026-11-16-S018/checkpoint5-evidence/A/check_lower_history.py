"""Negative controls for actual source acquisition, feedback and shared lower delivery."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','lower_controls');_,_,baseline=e.replay(w,R);ops=w['operations'];cases=[]
 for k,o in enumerate(ops):
  if o[0]=='ADD'and o[2].startswith('LOWER_RAW_'):cases.append(('cyclic_raw_acquisition',k))
  if o[0]=='ADD'and o[2].startswith('LOWER_INITIAL_Y'):cases.append(('initial_y_snapshot_acquisition',k))
  if o[0]=='ADD'and o[1].startswith('LOWER_INITIAL_Y'):cases.append(('actual_y_purification',k))
  if o[0]=='ADD'and o[1].startswith('X')and o[2]in{'Y21','Y64','Y65'}:cases.append(('primary_local_acquisition',k))
  if o[0]=='MOVE'and o[1]in{'TRIAD16','TRIAD23','TRIAD22'}and o[2].startswith('LOWER_COMMON_'):cases.append(('shared_unit_descent',k))
  if o[0]=='ADD'and o[1]in{'TRIAD16','TRIAD23','TRIAD22'}and o[2]in{'P0','P1','P2'}:cases.append(('lower_packet_reset',k))
  if o[0]=='ADD'and o[2].startswith(('LOCAL_PAIR_RAW_','LOCAL_PAIR_SOURCE_')):cases.append(('local_pair_acquisition',k))
  if o[0]=='ADD'and o[1].startswith('LOCAL_PAIR_SOURCE_')and o[2]in{'P1','P2'}:cases.append(('existing_descent_source_load',k))
 for cell in w['lower_history']['feedback_cells']:
  k=cell['before_operation'];assert ops[k]==['ADD',cell['packet'],f"Y{cell['primary']}"]
  cases.extend([('ordered_primary_cell',k),('ordered_primary_cell',k+1)])
 rejected=[]
 for kind,k in cases:
  bad=copy.deepcopy(w);del bad['operations'][k]
  try:e.replay(bad,R)
  except(AssertionError,KeyError)as ex:rejected.append({'kind':kind,'index':k,'operation':ops[k],'failure':str(ex)[:180]or'222-column endpoint identity'})
  else:raise AssertionError(('accepted semantic omission',kind,k))
 for cell in w['lower_history']['feedback_cells']:
  k=cell['before_operation'];bad=copy.deepcopy(w);bad['operations'][k:k+2]=bad['operations'][k:k+2][::-1]
  try:e.replay(bad,R)
  except(AssertionError,KeyError):rejected.append({'kind':'reversed_primary_cell','index':k})
  else:raise AssertionError(('accepted reversed primary cell',k))
 # A retention reset here would erase the code before its already-paid next descent.
 for p,f in zip(['P0','P1','P2'],['KEEP_C0','KEEP_C1','KEEP_C2']):
  k=ops.index(['ADD',p,f])+1;bad=copy.deepcopy(w);bad['operations'].insert(k,['ADD',f,p])
  try:e.replay(bad,R)
  except(AssertionError,KeyError):rejected.append({'kind':'obsolete_upper_reset_reinserted','index':k})
  else:raise AssertionError(('accepted obsolete reset',p))
 out={'status':'PASS_NATIVE_LOWER_HISTORY_SEMANTIC_CONTROLS','word_sha256':hashlib.sha256(raw).hexdigest(),'baseline':baseline,'control_count':len(rejected),'rejected':rejected,'scope':'Author controls, all222 columns and exact native chart inclusions. Credited retained interpreter; independent review remains separate.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['word_sha256'],len(rejected))
if __name__=='__main__':main()
