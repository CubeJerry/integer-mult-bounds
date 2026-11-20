#!/usr/bin/env python3
"""Replay the P104 price, exact native cuts, signed rail and chart-282 confirmation."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def require(ok,what):
    if not ok:raise ValueError(what)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run(path,args):
    subprocess.run([sys.executable,'-I','-B',str(path),*map(str,args)],cwd=path.parent,check=True)

def compare(actual,expected):
    require(json.loads(actual.read_text())==json.loads(expected.read_text()),'receipt mismatch '+expected.name)

def program_binding(repo):
    checked=[];prefix='research/moonshot-005-program/results/standalone-cyclic-rail/'
    for name in ('rail-base.json.gz','rail-repaired.json.gz'):
        local=HERE/'rail'/'sources'/name
        tracked=subprocess.run(['git','-C',str(repo),'cat-file','blob','d080d81f84f3a140a481bfa9582857f2f196d690:'+prefix+name],capture_output=True)
        if tracked.returncode==0:
            require(tracked.stdout==local.read_bytes(),'programme origin '+name);checked.append(name)
    return checked

def signed_receipts():
    directory=HERE/'rail';raw=gzip.decompress((directory/'output/SIGNED-RECIPES.json.gz').read_bytes())
    require(hashlib.sha256(raw).hexdigest()=='1dfd2ac79bdf461512615d3a23d1708c88d37b296f85014599a714b78a714ab4','bound recipe bytes')
    code=directory/'sources/native_verify.py';spec=importlib.util.spec_from_file_location('checked_native',code);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    frames=json.loads(gzip.decompress((directory/'sources/rail-base.json.gz').read_bytes()))['frames'];recs=json.loads(raw)
    for r in recs:
        a,b=r['from'],r['to'];m.equal(m.recipe(r['recipe']),m.adjoint(m.frame(tuple(frames[a]),9))+m.frame(tuple(frames[b]),9),'signed rank-one repair')
    return len(recs)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--full',action='store_true',help='also recompute modular bank ranks and all exact original-stock portfolio cuts');a=ap.parse_args();repo=a.repo.resolve();out=a.out.resolve();require(repo.is_dir(),'repository directory');require(not out.exists() or not any(out.iterdir()),'fresh --out directory');out.mkdir(parents=True,exist_ok=True)
    lock=json.loads((HERE/'MANIFEST.json').read_text());
    for name,digest in lock['sha256'].items():require(sha(HERE/name)==digest,'bundle hash '+name)
    program=program_binding(repo);review=HERE/'review';author=HERE/'author';rail=HERE/'rail';src=author/'sources/DOUBLE-CANDIDATE.json.gz';rout=out/'review';rout.mkdir()
    run(author/'check.py',['--out',out/'author']);compare(out/'author/RESULT.json',author/'output/RESULT.json')
    run(review/'check.py',['--canonical',repo,'--author',author,'--out',rout]);compare(rout/'RESULT.json',review/'output/RESULT.json')
    run(HERE/'chart282.py',['--out',rout]);compare(rout/'CHART282.json',review/'output/CHART282.json')
    run(rail/'check.py',['--out',out/'rail']+(['--rebuild-charts']if a.full else[]));compare(out/'rail/RESULT.json',rail/'output/RESULT.json');require((out/'rail/COMPLETE-WORD.json.gz').read_bytes()==(rail/'output/COMPLETE-WORD.json.gz').read_bytes(),'byte-identical emitted complete scalar word')
    run(HERE/'rail-review/check.py',['--author',rail,'--out',out/'rail-review']);compare(out/'rail-review/RESULT.json',HERE/'rail-review/output/RESULT.json')
    count=signed_receipts();require(count==192,'signed star maps')
    if a.full:
        # The independent stock program computes its own checkpoints when imported by pooled_cut.
        compiler=shutil.which('cc');require(compiler,'C11 compiler for full bank replay');lib=out/'banks.so';subprocess.run([compiler,'-std=c11','-O3','-fPIC','-shared',str(review/'banks.c'),'-o',str(lib)],check=True)
        run(review/'banks.py',['--source',src,'--lib',lib,'--out',rout]);compare(rout/'BANKS.json',review/'output/BANKS.json')
        run(review/'pooled_cut.py',['--source',src,'--out',rout]);compare(rout/'SIDE-STOCK.json',review/'output/SIDE-STOCK.json');compare(rout/'POOLED-CUT.json',review/'output/POOLED-CUT.json')
    status={'status':'PASS_P104_CONTESTED_RESTORATION_PACKAGE','full_portfolio_recomputed':a.full,'signed_star_maps':count,'compare_available_programme_objects':program,'complete_kappa_claimed':False}
    (out/'REPLAY.json').write_text(json.dumps(status,sort_keys=True,indent=2)+'\n');print(status['status'],flush=True)

if __name__=='__main__':main()
