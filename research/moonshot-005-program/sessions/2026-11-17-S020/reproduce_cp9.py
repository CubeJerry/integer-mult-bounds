#!/usr/bin/env python3
"""Focused S020 checkpoint9 reproduction; Python3.11+ and SymPy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);p=repo/'research/moonshot-005-program';s=p/'sessions/2026-11-17-S020';e=s/'checkpoint9-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP9.json'
    for pin in json.loads(pins.read_text())['files']:assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    commands=[];comparisons=[]
    def add(name,script,options,folder,files):
        commands.append((name,script,options));comparisons.extend((name+'/'+f,folder+'/'+f) for f in files)
    add('fixed-column-gate',B/'anticommuting-column-envelope-gate/check.py',['--repo',repo],'B/anticommuting-column-envelope-gate',['RESULT.json','MANIFEST.json'])
    add('independent-column-gate',A/'anticommuting-gate-review/check.py',['--repo',repo,'--author',B/'anticommuting-column-envelope-gate'],'A/anticommuting-gate-review/output',['RESULT.json'])
    add('prefix-compiler',C/'gaussian-dyadic-prefix-compiler/check.py',[],'C/gaussian-dyadic-prefix-compiler',['CERTIFICATE.json'])
    add('independent-prefix-compiler',R/'prefix-compiler-review/check.py',[],'R/prefix-compiler-review/output',['RESULT.json'])
    selected=set(a.only or [r[0] for r in commands]);assert selected<={r[0] for r in commands}
    def run(row):
        name,script,options=row
        done=subprocess.run([sys.executable,'-B',str(script),*map(str,options),'--out',str(out/name/'CERTIFICATE.json' if name=='prefix-compiler' else out/name)],cwd=repo,capture_output=True,text=True)
        (out/(name+'.log')).write_text(done.stdout+done.stderr)
        record={'name':name,'script':str(script.relative_to(repo)),'script_sha256':digest(script),'exit_code':done.returncode}
        print(name,'PASS' if done.returncode==0 else 'FAIL',flush=True)
        if done.returncode:record['failure_tail']=done.stderr[-3000:]
        return record
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:records=list(pool.map(run,[r for r in commands if r[0] in selected]))
    failures=[r for r in records if r['exit_code']]
    if failures:raise RuntimeError(json.dumps(failures,indent=2))
    matched=[]
    for fresh,frozen in comparisons:
        if fresh.split('/')[0] not in selected:continue
        actual=digest(out/fresh);assert actual==digest(e/frozen),'Exact reproduction mismatch: '+frozen
        matched.append({'path':frozen,'sha256':actual})
    result={'status':'PASS_S020_CHECKPOINT9_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'A independently reconstructs the full source as exact tensor words and checks B fixed-column encoder obstruction. Root independently reviews the all-size prefix compiler proof and replays selector/commutator/paired-unit primitives with separate SymPy arithmetic. Reexecution is not independent proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(records),'checks',len(matched),'byte-identical outputs')
if __name__=='__main__':main()
