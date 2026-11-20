#!/usr/bin/env python3
"""Replay the global Clifford price cut."""
import argparse,gzip,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
HEAD='14c74c6a67108f675ac1196a5f2415ead0920e71'

def require(q,msg):
    if not q:raise ValueError(msg)

def run(path,args):subprocess.run([sys.executable,'-I','-B',str(path),*map(str,args)],cwd=path.parent,check=True,stdout=subprocess.DEVNULL)
def same(a,b):require(json.loads(a.read_text())==json.loads(b.read_text()),'relocated result '+a.name)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--full',action='store_true',help='also exhaust all two-inclusion reversals');a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();require(repo.is_dir(),'repository directory');require(not out.exists()or not any(out.iterdir()),'fresh output');out.mkdir(exist_ok=True,parents=True)
    lock=json.loads((HERE/'MANIFEST.json').read_text())['sha256']
    for name,d in lock.items():require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==d,'input '+name)
    src=HERE/'sources/DOUBLE-CANDIDATE.json.gz';app=HERE/'sources/DOUBLE-APPLICATION.json.gz';author=HERE/'author';supplied=subprocess.run(['git','-C',str(repo),'cat-file','-e',HEAD],capture_output=True).returncode==0
    if supplied:
        for file,raw in [('DOUBLE-CANDIDATE.json.gz',src.read_bytes()),('DOUBLE-APPLICATION.json',gzip.decompress(app.read_bytes()))]:require(subprocess.check_output(['git','-C',str(repo),'cat-file','blob',HEAD+':research/p104-chart306-chain/'+file])==raw,'upstream '+file)
    run(author/'check.py',['--source',src,'--out',out]);same(out/'RESULT.json',author/'output/RESULT.json')
    for sub,name in [('', 'capacities.json.gz'),('optimized','capacities-optimized.json.gz'),('best','capacities-best.json.gz')]:
        q=out/sub;r=author/'output'/sub;run(author/'flag.py',['--source',src,'--application',app,'--capacity',author/name,'--out',q]);same(q/'FLAG-RESULT.json',r/'FLAG-RESULT.json')
        if (r/'CEILING.json').exists():run(author/'ceiling.py',['--application',app,'--flag-result',q/'FLAG-RESULT.json','--out',q]);same(q/'CEILING.json',r/'CEILING.json')
    run(HERE/'review/check.py',['--sources',HERE/'sources','--capacities',author,'--out',out/'review']);same(out/'review/RESULT.json',HERE/'review/output/RESULT.json')
    run(HERE/'donor100187.py',['--out',out]);same(out/'DONOR100187.json',author/'output/DONOR100187.json')
    if a.full:run(author/'pairs.py',['--source',src,'--out',out]);same(out/'PAIR-RESULT.json',author/'output/PAIR-RESULT.json')
    summary={'status':'PASS_GLOBAL_CLIFFORD_FRAME_PRICE_CUT','nested_double_orientation_exhausted':a.full,'matched_available_upstream_commit':supplied,'weighted_native_floor':'9598.81296','sharp_volume':9646,'full_interval_ceiling':'0.004392'};(out/'REPLAY.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n');print(summary['status'])
if __name__=='__main__':main()
