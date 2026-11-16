"""All222 negative controls for actual shared proper mask acquisition."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];s=importlib.util.spec_from_file_location('shared_control_engine',a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py');e=importlib.util.module_from_spec(s);s.loader.exec_module(e);_,_,baseline=e.replay(w,R);cases=[('source_mask',k)for k in w['shared_proper_masks']['source_add_indices']]+[('actual_shared_correction',k)for k in w['shared_proper_masks']['correction_add_indices']]+[('native_raw_capture',k)for k,o in enumerate(w['operations'])if o[0]=='ADD'and o[2].startswith('SHARED_PROPER_RAW_')];rejected=[]
 for kind,k in cases:
  q=copy.deepcopy(w);del q['operations'][k]
  try:e.replay(q,R)
  except(AssertionError,KeyError)as ex:rejected.append({'kind':kind,'index':k,'operation':w['operations'][k],'reason':str(ex)[:120]or'222-column endpoint mismatch'})
  else:raise AssertionError(('accepted active-mask omission',kind,k))
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps({'status':'PASS_SHARED_PROPER_OMISSION_CONTROLS','word_sha256':hashlib.sha256(raw).hexdigest(),'baseline':baseline,'control_count':len(rejected),'rejected':rejected,'scope':'Author controls on the all-one actual word. The universal mask argument is algebraic; no scalar scan is presented as proof.'},indent=2)+'\n');print('PASS',len(rejected))
if __name__=='__main__':main()
