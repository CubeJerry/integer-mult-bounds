#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,shutil,subprocess,sys,tempfile

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 here=Path(__file__).resolve().parent;src=here.parent/'bit-fifteen-class-target/author/RESULT.json';checker=here/'review/check.py'
 if sha(src)!='7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117':raise RuntimeError('Class source pin')
 if sha(checker)!='5e8ba4b24c05be7f2a47580f53c8457c89711405312c1e3fb8f52e98b6a681df':raise RuntimeError('Reviewer pin')
 a.output.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='moonshot-coset-review-') as tmp:
  w=Path(tmp);dst=w/'root-work/orthogonal-class-fitting/RESULT.json';dst.parent.mkdir(parents=True);shutil.copy2(src,dst)
  subprocess.run([sys.executable,'-I','-B',str(checker),'--repo',str(a.repo.resolve()),'--workspace',str(w),'--output',str(a.output.resolve())],check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
