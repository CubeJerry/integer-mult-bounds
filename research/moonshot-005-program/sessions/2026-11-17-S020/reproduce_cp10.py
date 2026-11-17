#!/usr/bin/env python3
"""Focused S020 checkpoint10 reproduction; Python3.11+ and SymPy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);p=repo/'research/moonshot-005-program';s=p/'sessions/2026-11-17-S020';e=s/'checkpoint10-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP10.json'
    for pin in json.loads(pins.read_text())['files']:assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    parent=s/'checkpoint5-evidence/A/full-half-reservoir';geometry=s/'checkpoint4-evidence/R/fresh-eight-facet-cut/check.py';arithmetic=s/'checkpoint9-evidence/C/gaussian-dyadic-prefix-compiler/check.py'
    commands=[];comparisons=[]
    def add(name,script,options,folder,files):
        commands.append((name,script,options));comparisons.extend((name+'/'+f,folder+'/'+f) for f in files)
    add('three-round-frame-gate',A/'complementary-frame-search/check.py',['--repo',repo,'--parent',parent],'A/complementary-frame-search/output',['RESULT.json'])
    add('independent-frame-gate',R/'three-round-frame-review/check.py',['--repo',repo,'--geometry',geometry,'--word',parent/'WORD.json'],'R/three-round-frame-review/output',['RESULT.json'])
    add('return-clock-interface',B/'return-clock-source-interface/check.py',['--repo',repo],'B/return-clock-source-interface',['RESULT.json','WORDS.json','MANIFEST.json'])
    add('independent-return-interface',C/'mixed-return-interface-review/check.py',['--arithmetic',arithmetic],'C/mixed-return-interface-review',['CERTIFICATE.json'])
    add('independent-block-proof',C/'complementary-frame-review/check.py',['--native',p/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json','--cut',s/'checkpoint5-evidence/C/full-half-reservoir-review/output/INDEPENDENT-CUT.json','--cases',A/'complementary-frame-search/output/RESULT.json'],'C/complementary-frame-review',['CERTIFICATE.json'])
    selected=set(a.only or [r[0] for r in commands]);assert selected<={r[0] for r in commands}
    def run(row):
        name,script,options=row
        done=subprocess.run([sys.executable,'-B',str(script),*map(str,options),'--out',str(out/name/'CERTIFICATE.json' if name in {'independent-return-interface','independent-block-proof'} else out/name)],cwd=repo,capture_output=True,text=True)
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
    result={'status':'PASS_S020_CHECKPOINT10_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'Root independently replays actual source fields and derives all legal seed cases by missing-incidence signatures; A separately enumerates every seed permutation. C independently reconstructs B return/clock gauges, paid unit, all-width D8 kernel and fixed-interface gate with separate Fraction arithmetic. Reexecution is not independent proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(records),'checks',len(matched),'byte-identical outputs')
if __name__=='__main__':main()
