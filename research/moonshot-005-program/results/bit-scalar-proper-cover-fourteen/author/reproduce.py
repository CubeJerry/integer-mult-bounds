#!/usr/bin/env python3
"""Rebuild every finite premise, preserving the frozen author's source method."""
import argparse,gzip,json,subprocess,sys,hashlib
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent;repo=a.repo.resolve();work=a.work.resolve()
    if work.exists():raise ValueError('work directory must be new')
    work.mkdir(parents=True);native=repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';census=work/'census';census.mkdir();commands=[]
    def run(args):
        cmd=[sys.executable,'-I','-B',*map(str,args)];q=subprocess.run(cmd,capture_output=True,text=True);commands.append(dict(command=cmd,exit_code=q.returncode))
        if q.returncode:raise RuntimeError(q.stdout+q.stderr)
    run([here/'census_rank3.py','--repo',repo,'--output',census])
    run([here/'census_cliques.py','--native',native,'--output',census/'CLIQUE-CASES.json'])
    run([here/'certify.py','--native',native,'--rank3',census/'RANK3-CASES.json','--cliques',census/'CLIQUE-CASES.json','--output',work/'output'])
    for name in ['CASES.json.gz','MINORS.json.gz']:
        if gzip.decompress((work/'output'/name).read_bytes())!=gzip.decompress((here/'output'/name).read_bytes()):raise ValueError('canonical payload mismatch '+name)
    expected=json.load(open(here/'output/RESULT.json'));actual=json.load(open(work/'output/RESULT.json'))
    for key in ['cases_sha256','minors_sha256']:expected.pop(key);actual.pop(key)
    if expected!=actual:raise ValueError('scientific summary mismatch')
    out=dict(status='PASS_ISOLATED_SHARP_FOURTEEN_AUTHOR_REPRODUCTION',commands=commands,exact_minors=actual['exact_integer_minors'],canonical_payloads_identical=True,scope='Author reproduction, not independent review; gzip containers may vary by runtime.')
    (work/'REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
