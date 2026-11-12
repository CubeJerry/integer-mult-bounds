#!/usr/bin/env python3
"""Reproduce lost historical receipts without editing recovered source files.

The frozen review used historical absolute paths. This adapter changes only
its path globals and supplies its exact existing helper, leaving both frozen
implementations and all mathematical tests byte-authenticated.
"""
import argparse,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(p,msg):
 if not p:raise ValueError(msg)

def main(a):
 repo=a.repo.resolve();out=a.output_directory.resolve();out.mkdir(parents=True,exist_ok=True)
 recovered=repo/'research/moonshot-005-program/sessions/2026-11-12-S007/recovery'
 paths={
  'author_checker':(recovered/'budget/odd8-saturated-cut/check.py','65563ae9e89bccff0760eb2879170ca48655e3ba865284c8df0e53fcbf2dc6a4'),
  'author_proof':(recovered/'budget/odd8-saturated-cut/PROOF.md','2aae4529ce79f6918386ef0da0c13cb0fcdef4673f228397de27563e66b02fa4'),
  'historical_reviewer':(recovered/'review/odd8-saturated-cut/check_cut.py','7161aea481dd45d9e712b9ab753c9f7669c3287a2884d6f182283e0c893afc28'),
  'historical_review_proof':(recovered/'review/odd8-saturated-cut/REVIEW.md','55e48fb2ce45ccdefcc0162b3ae33eef5dfad936e716ae9138d1193db7323b1f'),
  'historical_reviewer_helper':(repo/'research/moonshot-005-program/results/observation-preserving-route-fusion/review/check_fusion.py','cd0a90cc2773d144a1c106245d14c5a6f6ee9fad76dca64383a5dc2d7fa04763')}
 for name,(p,pin) in paths.items():require(sha(p)==pin,'byte-authenticated '+name)
 author=out/'author';review=out/'review';helper=out/'worker-review/route-fusion';author.mkdir(exist_ok=True);review.mkdir(exist_ok=True);helper.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(paths['author_proof'][0],author/'PROOF.md');shutil.copyfile(paths['historical_reviewer_helper'][0],helper/'check_fusion.py')
 if a.reuse_author_result is not None:shutil.copyfile(a.reuse_author_result,author/'RESULT.json')
 else:
  run=subprocess.run([sys.executable,str(paths['author_checker'][0]),'--repo',str(repo),'--out',str(author/'RESULT.json')],check=True,capture_output=True,text=True)
  (out/'author-execution.log').write_text(run.stdout+run.stderr)
 require(sha(author/'RESULT.json')=='7c2e7f7d1c4db2c82ec020048432f7d5ef5a9244bc7fae3485aa711585994a51','exact frozen author receipt reproduced')
 spec=importlib.util.spec_from_file_location('historical_odd8_reviewer',paths['historical_reviewer'][0]);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 mod.BASE=out;mod.REPO=repo;mod.HERE=review;mod.PACK=author;mod.main()
 require(sha(review/'REVIEW-RESULT.json')=='4f219989485230154dc914fff5556efcc0bc180b11ef7db2070491ab4096f8e7','exact frozen independent review receipt reproduced')
 result=dict(status='PASS_EXACT_FROZEN_ODD8_RECEIPTS_REPRODUCED',historical_sources={name:pin for name,(p,pin) in paths.items()},
  restored_author_result_sha256=sha(author/'RESULT.json'),restored_review_result_sha256=sha(review/'REVIEW-RESULT.json'),adapter_sha256=sha(Path(__file__)),
  scope='Execution restoration of the historically independent author and reviewer implementations. Only absolute-path globals are rebound. This is not itself a new independent mathematical review; the separately written e8_saturated_cut.py supplies a fresh review and E8 application.')
 (out/'RECOVERY-REPRODUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output-directory',type=Path,required=True);p.add_argument('--reuse-author-result',type=Path);main(p.parse_args())
