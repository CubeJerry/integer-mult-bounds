"""Regenerate and independently replay all19600 finite selector counterexamples."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
SHA='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,s):
    if not b:raise ValueError(s)
def execute(command):
    r=subprocess.run([str(x) for x in command],capture_output=True,text=True,timeout=420)
    need(r.returncode==0,'command failed: '+str(command)+'\n'+r.stderr)
    return r.stdout
def run(word):
    raw=word.read_bytes();need(hashlib.sha256(raw).hexdigest()==SHA,'source SHA256')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='74563a7867d9d762b6588f65362369668841bb3e','source blob')
    with tempfile.TemporaryDirectory(prefix='selector-review-') as tmp:
        d=Path(tmp)
        execute([sys.executable,'-I','-B',HERE/'source_prepare.py',word,d])
        for source,binary in [('source_screen.cpp','screen'),('independent_verify.cpp','independent')]:
            execute(['g++','-O3','-std=c++17','-Wall','-Wextra',HERE/source,'-o',d/binary])
        execute([d/'screen',d/'screen-input.txt',d/'source'])
        summary=json.loads((d/'source-summary.json').read_text())
        need(summary['complete'] and summary['checked']==19600 and summary['survivors']==0,'complete author domain')
        need((d/'source-survivors.tsv').read_bytes()==b'','no surviving source rows')
        prep=json.loads(execute([sys.executable,'-I','-B',HERE/'independent_prepare.py','--word',word,'--screen-input',d/'screen-input.txt','--witnesses',d/'source.tsv','--output',d/'independent-input.txt']))
        result=json.loads(execute([d/'independent',d/'independent-input.txt']))
        mutation=subprocess.run([str(d/'independent'),str(d/'independent-input.txt'),'--mutate-witness'],capture_output=True,text=True,timeout=30)
        need(mutation.returncode==3 and 'DETECTED_WITNESS_MISMATCH' in mutation.stderr,'mutated witness not rejected')
        return {'status':'PASS_INDEPENDENT_FINITE_SELECTOR_FAMILY','source_sha256':SHA,
          'source_preparation':prep,'independent_replay':result,'mutated_witness_exit':3,
          'generated_input_sha256':hashlib.sha256((d/'independent-input.txt').read_bytes()).hexdigest(),
          'implementation_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ['source_prepare.py','source_screen.cpp','independent_prepare.py','independent_verify.cpp']},
          'no_new_kappa':True,'scope':'Exactly14^2*5^2*2^2 named contact-pattern schemes; finite rational endpoint exclusion only, no tariff claim.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=HERE.parents[1]/'shared-wire-split-composition/data/final.json.gz');ap.add_argument('--write',action='store_true');a=ap.parse_args()
    result=run(a.source.resolve());receipt=HERE/'RESULT.json'
    if a.write:receipt.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(receipt.read_text())==result,'frozen result mismatch')
    print(json.dumps(result,indent=2))
