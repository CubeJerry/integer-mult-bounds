#!/usr/bin/env python3
"""Focused S020 checkpoint5 reproduction; Python3.11+ and SymPy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists()and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);s=repo/'research/moonshot-005-program/sessions/2026-11-17-S020';e=s/'checkpoint5-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP5.json'
    for pin in json.loads(pins.read_text())['files']:assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    c4=s/'checkpoint4-evidence';geo=s/'checkpoint2-evidence/C/four-plane-review/check.py';sr=s/'checkpoint3-evidence/C/proper-query-export-review/check.py';er=s/'checkpoint1-evidence/C/entropy54-review/check.py';native=A/'SOURCE-RECOVERY.json'
    algebra=c4/'C/all-source-exit-review/check.py';fanout=c4/'C/all-source-exit-review/output/CERTIFICATE.json';mapped=c4/'R/fresh-transcript-nine/output/MAPPED-DUAL.json';geometry=c4/'R/fresh-eight-facet-cut/check.py';early=c4/'A/early-axis-known8/WORD.json'
    ground=A/'ground-retention-known8/WORD.json';proper=A/'frame-derived-proper-export/WORD.json';meet=C/'meet-frame-export/output/WORD.json';quadratic=A/'quadratic-first-exit/CERTIFICATE.json'
    commands=[];comparisons=[]
    def add(name,script,options,folder,files):
        commands.append((name,script,options));comparisons.extend((name+'/'+f,folder+'/'+f)for f in files)
    trio=['WORD.json','RESULT.json','CUT-INVENTORY.json'];common=['--native',native,'--source-review',sr,'--arithmetic',geo]
    add('ground',A/'build_ground_retention_source.py',['--repo',repo,'--parent',early],'A/ground-retention-known8',trio)
    add('proper-frame',A/'build_frame_derived_proper_export.py',['--repo',repo,'--parent',ground],'A/frame-derived-proper-export',trio)
    add('meet-frame',C/'meet-frame-export/build.py',common+['--parent',ground,'--algebra',algebra],'C/meet-frame-export/output',trio)
    add('quadratic-ground',A/'check_quadratic_first_exit.py',['--repo',repo,'--word',ground],'A/quadratic-first-exit',['CERTIFICATE.json'])
    add('independent-ground',C/'ground-retention-review/check.py',common+['--word',ground,'--parent',early,'--fanout-review',algebra,'--fanout-certificate',fanout,'--entropy-review',er,'--mapped',mapped],'C/ground-retention-review/output',['RESULT.json','INDEPENDENT-CUT.json'])
    add('independent-meet',A/'review_meet_frame_export.py',['--repo',repo,'--word',meet,'--parent',ground,'--author-result',meet.with_name('RESULT.json'),'--author-inventory',meet.with_name('CUT-INVENTORY.json')],'A/meet-frame-export-review',['RESULT.json'])
    add('independent-frame-gates',R/'quadratic-frame-gates/check.py',['--repo',repo,'--geometry',geometry,'--ground',ground,'--proper',proper,'--meet',meet],'R/quadratic-frame-gates/output',['CERTIFICATE.json'])
    add('independent-quadratic-and-proper',C/'frame-quadratic-review/check.py',common+['--ground',ground,'--join',proper,'--meet',meet,'--algebra',algebra,'--quadratic-certificate',quadratic],'C/frame-quadratic-review/output',['CERTIFICATE.json'])
    add('reservoir',A/'build_full_half_reservoir.py',['--repo',repo],'A/full-half-reservoir',trio)
    add('independent-reservoir',C/'full-half-reservoir-review/check.py',common+['--word',A/'full-half-reservoir/WORD.json','--entropy-review',er,'--mapped',mapped],'C/full-half-reservoir-review/output',['CERTIFICATE.json','INDEPENDENT-CUT.json'])
    add('prefix-normalizer',B/'distinguished-prefix-native-normalizer/check.py',['--repo',repo],'B/distinguished-prefix-native-normalizer',['RESULT.json','WORDS.json'])
    add('independent-prefix',R/'prefix-normalizer-review/check.py',['--repo',repo,'--author',B/'distinguished-prefix-native-normalizer'],'R/prefix-normalizer-review/output',['RESULT.json'])
    selected=set(a.only or [row[0]for row in commands]);assert selected<={row[0]for row in commands}
    def run(row):
        name,script,options=row
        done=subprocess.run([sys.executable,'-B',str(script),*map(str,options),'--out',str(out/name)],cwd=repo,capture_output=True,text=True)
        (out/(name+'.log')).write_text(done.stdout+done.stderr)
        record={'name':name,'script':str(script.relative_to(repo)),'script_sha256':digest(script),'exit_code':done.returncode}
        print(name,'PASS'if done.returncode==0 else'FAIL',flush=True)
        if done.returncode:record['failure_tail']=done.stderr[-3000:]
        return record
    with ThreadPoolExecutor(max_workers=a.jobs)as pool:records=list(pool.map(run,[r for r in commands if r[0]in selected]))
    failures=[r for r in records if r['exit_code']]
    if failures:raise RuntimeError(json.dumps(failures,indent=2))
    matched=[]
    for fresh,frozen in comparisons:
        if fresh.split('/')[0]not in selected:continue
        actual=digest(out/fresh);assert actual==digest(e/frozen),'Exact reproduction mismatch: '+frozen
        matched.append({'path':frozen,'sha256':actual})
    result={'status':'PASS_S020_CHECKPOINT5_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'A sources independently reconstructed by C, and C meet source by A. Quadratic gates reconstructed by root Fraction and C exact-integer methods, with fresh source-specific duals. B paid prefix word independently replayed by root using C sparse Q(i). Reexecution is not independent proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(records),'checks',len(matched),'byte-identical outputs')
if __name__=='__main__':main()
