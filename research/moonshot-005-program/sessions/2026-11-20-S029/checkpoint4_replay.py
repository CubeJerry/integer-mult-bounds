#!/usr/bin/env python3
"""Run S029 checkpoint four proofs and check the scientific payloads in a fresh directory."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--jobs',type=int,default=1);p.add_argument('--only')
    a=p.parse_args();repo=a.repo.resolve();dst=a.out.resolve();dst.mkdir(parents=True,exist_ok=True)
    R=repo/'research/moonshot-005-program/results'
    K=R/'bit-gf64-actual-k-atlas/author/output';D=R/'bit-minimum-cache-d-atlas/author/output'
    RA=R/'bit-spread-rs-physical-word/author';H=RA/'output'
    F=R/'bit-minimum-terminal-storage/author/output';multi=R/'bit-spread-two-centre-packing'
    packed=R/'bit-spread-packed-source-owner-compiler/author';source=R/'bit-spread-h263-source/author/output/COEFFICIENTS.json.gz'
    scm=R/'bit-spread-source-owner-compiler/author/compile_source.py'
    mid=R/'bit-spread-isolated-middle-cut';nl=R/'bit-nonlinear-middle-gauge-obstruction/author'
    part=R/'bit-partial-covariant-star-word';star=R/'bit-full-covariant-star-word'
    ov=R/'bit-covariant-canonical-center';rig=R/'bit-native-rank-nine-rigidity';term=R/'bit-physical-terminal-quotient'
    plans=[]
    def add(name,script,ref,files=('RESULT.json',),args=(),use_repo=True):
        plans.append((name,script,ref,files,args,use_repo))
    add('two-centre',multi/'author/check.py',multi/'author/output')
    add('two-centre-review',multi/'review/check.py',multi/'review/output')
    flags=['--parameters',multi/'author/output/PARAMETERS.json','--background',RA/'source-output/PER-DONOR-COSTS.json']
    add('30-price',packed/'compile_pack.py',packed/'output-30',args=flags)
    add('31-price',packed/'compile_pack.py',packed/'output-31',args=flags+['--singleton-coefficients',multi/'author/output/SINGLETONS.json.gz'])
    add('D120',mid/'author/check.py',mid/'author/output',args=['--h-author',RA,'--d-charts',D/'CHARTS.json.gz','--k-words',K,'--source',source,'--source-compiler',scm])
    add('D120-review',mid/'review/check.py',mid/'review/output',args=['--words',mid/'author/output/WORDS.json.gz'])
    add('nonlinear',nl/'check.py',nl/'output',args=['--native-review',mid/'review/output/RESULT.json'],use_repo=False)
    for label,pack in [('partial',part),('full',star)]:
        auth=pack/'author'
        cert=auth/'output'
        files=['RESULT.json']+[x.name for x in sorted(cert.glob('*word.json.gz'))]
        add(label+'-construct',auth/'construct.py',cert,files=files)
        add(label+'-replay',auth/'check_word.py',cert,files=['REPLAY.json'],args=['--certs',cert])
        add(label+'-review',pack/'review/check.py',pack/'review/output',args=['--words',cert])
    add('center-construct',ov/'author/augment.py',ov/'author/output',files=['RESULT.json','row-word.json.gz','column-word.json.gz'],args=['--base',star/'author/output'])
    add('center-replay',ov/'author/check.py',ov/'author/output',files=['REPLAY.json'],args=['--word',ov/'author/output','--replayer',star/'author/check_word.py'])
    add('center-review',ov/'review/check.py',ov/'review/output',args=['--words',ov/'author/output','--full-review',star/'review/check.py'])
    add('rigid',rig/'author/check.py',rig/'author/output')
    add('rigid-review',rig/'review/check.py',rig/'review/output')
    add('free-F-cut',term/'author/check.py',term/'author/output',args=['--h-words',H,'--d-words',D,'--k-words',K,'--f-words',F])
    # The second proof produces arrays and then independently reduces them.
    add('free-F-direct',term/'review/transfer.py',term/'review/output',files=['COMPOSITION.json'],args=['--d-words',D,'--k-words',K,'--arrays-out',dst/'native-arrays'])
    def run(item):
        n,script,ref,files,flags,use_repo=item
        out=dst/n;out.mkdir(exist_ok=True)
        with (dst/(n+'.log')).open('w') as log:
            subprocess.run([sys.executable,'-B',script,*(['--repo',repo] if use_repo else []),'--out',out,*flags],check=True,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
        answer={}
        for f in files:
            def read(x):
                raw=x.read_bytes()
                return gzip.decompress(raw) if x.suffix=='.gz' else raw
            actual=read(out/f)
            if actual!=read(ref/f):raise ValueError(n+' '+f)
            answer[f]=sha256(actual).hexdigest()
        print(n,flush=True)
        return n,answer
    todo=[j for j in plans if not a.only or j[0]==a.only]
    if a.only and not todo and a.only!='free-F-direct-rank':raise ValueError('unknown job')
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:results=dict(ex.map(run,todo))
    if not a.only or a.only=='free-F-direct-rank':
        job=('free-F-direct-rank',term/'review/check.py',term/'review/output',['RANK.json'],['--arrays',dst/'native-arrays','--author-result',term/'author/output/RESULT.json'],True)
        key,value=run(job);results[key]=value
    (dst/'VALIDATION.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
