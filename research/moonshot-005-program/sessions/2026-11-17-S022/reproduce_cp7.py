#!/usr/bin/env python3
"""Rebuild the real balanced trajectories, causal gates, field checks and native controlled outputs."""
import argparse
import concurrent.futures
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args();repo=args.repo.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    pg=repo/'research/moonshot-005-program';r=pg/'results'
    a=r/'bit-all111-balanced-causal-atlas';b=r/'bit-simultaneous-native-coordinates'
    A=a/'author';ao=A/'output';layout=r/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';factor=ao/'BALANCED-FACTOR.json'
    native=pg/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    jobs=[]
    def job(name,script,argv,outputs):
        dest=out/name;dest.mkdir(exist_ok=True)
        jobs.append((name,script,[str(dest) if x=='OUT' else str(dest/x[4:]) if isinstance(x,str)and x.startswith('OUT/') else str(x) for x in argv],[(src,dest/d if d else None)for src,d in outputs]))
    job('factor',A/'balance.py',['--layout',layout,'--factor',factor,'--out','OUT'],[(ao/f,f)for f in ('BALANCED-FACTOR.json','BALANCED-RESULT.json')])
    job('routes',A/'routes_balanced.py',['--layout',layout,'--factor',factor,'--out','OUT/r.json'],[(ao/'BALANCED-ROUTES.json','r.json')])
    job('budget',A/'budget.py',['--out','OUT/r.json'],[(ao/'BUDGET.json','r.json')])
    job('slack',A/'slack.py',['--layout',layout,'--out','OUT'],[(ao/f,f)for f in ('SLACK-PATCH.json.gz','SLACK-RESULT.json')])
    for tag in ['BASE','SLACK']:
        farg=['--patch',ao/'SLACK-PATCH.json.gz'] if tag=='SLACK' else []
        job('flow-'+tag,A/'flow.py',['--layout',layout,*farg,'--out','OUT'],[(ao/f,f)for f in ('FLOW-'+tag+'.json','PAIRS-'+tag+'.json.gz')])
    job('gf64',a/'review/check.py',['--native',native,'--layout',layout,'--factor',factor,'--out','OUT'],[(a/'review/output/RESULT.json','RESULT.json')])
    job('mixed',b/'mixed/mixed_demands.py',['--layout',layout,'--factor',factor,'--k','69','--workers','3','--out','OUT'],[(b/'mixed/output'/f,f)for f in ('MIXED-69.json','MIXED-69.json.gz')])
    for tag in ['sync-partial','sync-cache']:
        job(tag,b/tag/'check.py',['--layout',layout,'--factor',factor,'--out','OUT/r.json'],[(b/tag/'RESULT.json','r.json')])
    job('independent-dinic',b/'review/check.py',[layout,factor,'--cache'],[(b/'review/CERTIFICATE.json',None)])
    def run(cfg):
        name,script,argv,outputs=cfg
        env=dict(os.environ,PYTHONPATH=str(A),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
        proc=subprocess.run([sys.executable,'-B',str(script),*argv],cwd=repo,capture_output=True,env=env)
        if proc.returncode:raise RuntimeError(name+' failed: '+proc.stderr.decode())
        records=[]
        for src,actual in outputs:
            f=actual.read_bytes() if actual else proc.stdout
            frozen=src.read_bytes()
            if src.suffix=='.gz':f,frozen=gzip.decompress(f),gzip.decompress(frozen)
            if f!=frozen:raise ValueError(name+' differing output '+str(src))
            records.append({'relative_path':str(src.relative_to(pg)),'sha256_uncompressed':hashlib.sha256(f).hexdigest()})
        print(name,'PASS',flush=True);return {'check':name,'files':records}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)as tp:results=list(tp.map(run,jobs))
    (out/'VALIDATION.json').write_text(json.dumps({'status':'PASS','checks':results},indent=2)+'\n')
if __name__=='__main__':
    main()
