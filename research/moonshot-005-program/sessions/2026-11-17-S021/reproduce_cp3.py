#!/usr/bin/env python3
"""Portable focused replay of seven S021 checkpoint3 admissions."""
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4]);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);results=repo/'research/moonshot-005-program/results'
 names={'rigidity':'bit-induced95-equality-rigidity','coupling':'bit-proper-decoder-dual-coupling','tradeoff':'bit-proper-block-sum-tradeoff','formation':'bit-low-exterior-formation-gate','caches':'bit-deferred-terminal-caches','column':'complex-sameplus-routed-column','gate':'complex-sameplus-fixed-output-gate'}
 pk={k:results/v for k,v in names.items()};support=pk['rigidity']/'author/FULL-SUPPORT-CERTIFICATE.json';view=out/'portable-worker-view'
 copies={
  'C/induced95-rigidity/FULL-SUPPORT-CERTIFICATE.json':support,
  'A/two-copy-f4/output/WORD.json':results/'bit-two-copy-field-compiler/author/output/WORD.json',
  'A/three-copy-f8/output/WORD.json':results/'bit-three-copy-field-compiler/author/output/WORD.json',
  'C/pair-source-audit/output/SINGLE-CUT.json':results/'bit-separated-private-transcript/author/output/SINGLE-CUT.json',
  'C/pair-source-audit/output/TRIPLE-CUT.json':results/'bit-separated-private-transcript/author/output/TRIPLE-CUT.json',
  'C/two-copy-source-cut/output/INDEPENDENT-CUT.json':results/'bit-two-copy-field-compiler/physical-review/output/INDEPENDENT-CUT.json',
  'R/proper-basis-coupling/PROOF.md':pk['coupling']/'author/PROOF.md',
  'R/proper-basis-tradeoff/PROOF.md':pk['tradeoff']/'author/PROOF.md'}
 for relative,source in copies.items():
  target=view/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 # Each tuple contains its frozen package and all scientific output files.
 jobs=[
  ('rigidity-author',pk['rigidity']/'author','check.py',['--repo',repo],['CERTIFICATE.json']),
  ('rigidity-review',pk['rigidity']/'review','check.py',['--repo',repo,'--author',pk['rigidity']/'author'],['CERTIFICATE.json']),
  ('coupling-review',pk['coupling']/'review','check.py',['--support',support,'--author',pk['coupling']/'author'],['RESULT.json','TRIPLE-CERTIFICATE.json']),
  ('tradeoff-author',pk['tradeoff']/'author','check.py',['--support',support],['CERTIFICATE.json']),
  ('tradeoff-review',pk['tradeoff']/'review','check.py',['--support',support,'--author',pk['tradeoff']/'author'],['RESULT.json']),
  ('formation-author',pk['formation']/'author','check.py',['--repo',repo,'--workers',view],['RESULT.json','ALL-FIELD-LOCALITY.json']),
  ('formation-review',pk['formation']/'review','check.py',['--repo',repo,'--workers',view],['CERTIFICATE.json']),
  ('caches-author',pk['caches']/'author','build.py',['--repo',repo],['WORD.json','RESULT.json','CACHE-LIFETIMES.json']),
  ('caches-review',pk['caches']/'review','check.py',['--repo',repo,'--author',pk['caches']/'author'],['RESULT.json','INDEPENDENT-CACHE-LIFETIMES.json','ALL888-FINAL-ROWS.json']),
  ('column-author',pk['column']/'author','check.py',['--repo',repo],['RESULT.json','WORDS.json','MANIFEST.json']),
  ('column-review',pk['column']/'review','check.py',['--author',pk['column']/'author'],['RESULT.json','SOURCE-IDENTITIES.json']),
  ('gate-author',pk['gate']/'author','check.py',['--repo',repo,'--positive',pk['column']/'author'],['RESULT.json','NONORDINARY-WITNESS.json','MANIFEST.json']),
  ('gate-review',pk['gate']/'review','check.py',['--author',pk['gate']/'author'],['RESULT.json','FREE-SOURCE-EQUATION.json'])]
 receipt={'status':'PASS','python':platform.python_version(),'commands':[],'outputs':[],'portable_input_view_from_frozen_repository':True}
 for label,package,script,arguments,files in jobs:
  command=[sys.executable,'-B',str(package/script)]+list(map(str,arguments))+['--out',str(out/label)]
  run=subprocess.run(command,cwd=repo,capture_output=True,text=True);(out/(label+'.log')).write_text(run.stdout+run.stderr)
  if run.returncode:raise RuntimeError(label+' failed: '+run.stderr[-3000:])
  receipt['commands'].append({'label':label,'exit_code':0,'checker_sha256':hashlib.sha256((package/script).read_bytes()).hexdigest()})
  for filename in files:
   frozen=package/'output'/filename;generated=out/label/filename;old=frozen.read_bytes();new=generated.read_bytes()
   if json.loads(old)!=json.loads(new):raise ValueError('Scientific output differs: '+str(frozen))
   canonical=json.dumps(json.loads(new),sort_keys=True,separators=(',',':')).encode()
   receipt['outputs'].append({'path':str(frozen.relative_to(repo)),'frozen_sha256':hashlib.sha256(old).hexdigest(),'generated_sha256':hashlib.sha256(new).hexdigest(),'canonical_json_sha256':hashlib.sha256(canonical).hexdigest(),'all_scientific_fields_equal':True,'byte_equal':old==new})
  print(label+' PASS',flush=True)
 script=pk['coupling']/'proof-pin-review/check.py';run=subprocess.run([sys.executable,'-B',str(script),'--workers',str(view)],cwd=repo,capture_output=True,text=True)
 (out/'author-proof-pins.log').write_text(run.stdout+run.stderr)
 assert run.returncode==0,run.stderr
 receipt['commands'].append({'label':'author-proof-pins','exit_code':0,'checker_sha256':hashlib.sha256(script.read_bytes()).hexdigest()})
 (out/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'status':'PASS_S021_CP3','checks':len(receipt['commands']),'complete_scientific_outputs':len(receipt['outputs'])}))
if __name__=='__main__':main()
