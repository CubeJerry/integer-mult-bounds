"""Native semantic controls for the fifty-output source with five retained modes."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];s=importlib.util.spec_from_file_location('mode_controls',a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py');e=importlib.util.module_from_spec(s);s.loader.exec_module(e);_,_,baseline=e.replay(w,R);ops=w['operations'];cases=[]
 for k,o in enumerate(ops):
  if o[0]=='ADD'and o[2].startswith(('MODE_D4_RAW_','LOCAL_PAIR_RAW_','LOCAL_PAIR_SOURCE_','SHARED_PROPER_RAW_')):cases.append(('actual_native_capture',k))
  if o[0]=='ADD'and(o[1]=='MODE_INITIAL_Y74'or o[2]=='MODE_INITIAL_Y74'):cases.append(('actual_initial_y_snapshot',k))
  if o[0]=='ADD'and o[1].startswith('X')and o[2]=='Y74':cases.append(('primary_local_source',k))
  if o[0]=='ADD'and o[1].startswith('LOCAL_PAIR_SOURCE_')and o[2]in{'P1','P2'}:cases.append(('existing_descent_pair_load',k))
  if o==['MOVE','ZFIRST4',w['mode_preserving_d4']['common']]:cases.append(('one_shared_unit_descent',k))
  if o==['ADD','ZFIRST4','P4']:cases.append(('old_lower_tail_reset',k))
 sm=w['shared_proper_masks'];cases.extend(('retained_unknown_mode_source',k)for k in sm['source_add_indices']);cases.extend(('actual_shared_proper_correction',k)for k in sm['correction_add_indices']);cell=w['mode_preserving_d4']['feedback_cell'];k=cell['before_operation'];assert ops[k:k+2]==[['ADD','P4','Y74'],['ADD','Y74','P4']];cases.extend([('ordered_primary_feedback',k),('ordered_primary_feedback',k+1)]);rejected=[]
 for kind,k in cases:
  q=copy.deepcopy(w);del q['operations'][k]
  try:e.replay(q,R)
  except(AssertionError,KeyError)as ex:rejected.append({'kind':kind,'index':k,'operation':ops[k],'failure':str(ex)[:100]or'222-column endpoint identity'})
  else:raise AssertionError(('accepted active omission',kind,k))
 k=cell['before_operation'];q=copy.deepcopy(w);q['operations'][k:k+2]=q['operations'][k:k+2][::-1]
 try:e.replay(q,R)
 except(AssertionError,KeyError):rejected.append({'kind':'reversed_primary_feedback','index':k})
 else:raise AssertionError('accepted reversed feedback')
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps({'status':'PASS_MODE_PRESERVING_NATIVE_SEMANTIC_CONTROLS','word_sha256':hashlib.sha256(raw).hexdigest(),'baseline':baseline,'control_count':len(rejected),'rejected':rejected,'scope':'Author controls on the literal word; exact geometry/all222 columns, credited retained interpreter.'},indent=2)+'\n');print('PASS',len(rejected))
if __name__=='__main__':main()
