#!/usr/bin/env python3
"""Portable adapter for the unchanged independent quotient checker."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked_copy(src,dst,pin):
 if sha(src)!=pin:raise RuntimeError('Pin mismatch: '+str(src))
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
def main(a):
 here=Path(__file__).resolve().parent;results=here.parent
 with tempfile.TemporaryDirectory(prefix='moonshot-class-history-') as tmp:
  workspace=Path(tmp);src=here/'author'
  pin='7d5aa1911bc7a76e36167906d548435372afbd895cffcc5778e84a80b9d584d4'
  checked_copy(src/'MANIFEST.json',workspace/'worker-a/next/class-historical-closure/MANIFEST.json',pin)
  for row in json.loads((src/'MANIFEST.json').read_text())['files']:
   checked_copy(src/row['path'],workspace/'worker-a/next/class-historical-closure'/row['path'],row['sha256'])
  checked_copy(results/'bit-y-feedback-normalization/author/MANIFEST.json',workspace/'root-work/y-feedback-normalization/MANIFEST.json','d427cabd4770bdd787f8bf85e77640a16a0848264a6d9b74d4881f28e2a3cd56')
  checked_copy(results/'bit-fifteen-class-target/author/RESULT.json',workspace/'root-work/orthogonal-class-fitting/RESULT.json','7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117')
  checker=here/'review/check.py'
  if sha(checker)!='5aa4afbbc4fc1929e479e9ea3c1dcb08f19b4213cef8c91a71b33ecbc43eec39':raise RuntimeError('Reviewer checker pin')
  subprocess.run([sys.executable,'-I','-B',str(checker),'--repo',str(a.repo.resolve()),'--workspace',str(workspace),'--output',str(a.output.resolve())],check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
