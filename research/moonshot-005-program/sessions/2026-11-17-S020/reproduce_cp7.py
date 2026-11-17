#!/usr/bin/env python3
"""Focused S020 checkpoint7 reproduction; Python3.11+ and SymPy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);p=repo/'research/moonshot-005-program';s=p/'sessions/2026-11-17-S020';e=s/'checkpoint7-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP7.json'
    for pin in json.loads(pins.read_text())['files']:assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    geo=s/'checkpoint2-evidence/C/four-plane-review/check.py';sr=s/'checkpoint3-evidence/C/proper-query-export-review/check.py';entropy=s/'checkpoint1-evidence/C/entropy54-review/check.py'
    native=p/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';parent=s/'checkpoint6-evidence/A/parity-receiver-relays/WORD.json';service=A/'proper-half-service/WORD.json'
    olddual=s/'checkpoint4-evidence/R/fresh-transcript-nine/output/MAPPED-DUAL.json';mapped=C/'shared-half-fresh-transcript/output/MAPPED-DUAL.json';rootgeo=s/'checkpoint4-evidence/R/fresh-eight-facet-cut/check.py';rootentropy=s/'checkpoint1-evidence/R/entropy54/check.py'
    normalizer=s/'checkpoint5-evidence/B/distinguished-prefix-native-normalizer';source_review=s/'checkpoint6-evidence/R/endpoint-column-review/check.py'
    commands=[];comparisons=[]
    def add(name,script,options,folder,files):
        commands.append((name,script,options));comparisons.extend((name+'/'+f,folder+'/'+f) for f in files)
    trio=['WORD.json','RESULT.json','CUT-INVENTORY.json'];common=['--native',native,'--source-review',sr,'--arithmetic',geo]
    add('half-service',A/'build_proper_half_service.py',['--repo',repo,'--parent',parent],'A/proper-half-service',trio)
    add('independent-service',C/'proper-half-service-review/check.py',common+['--parent',parent,'--word',service],'C/proper-half-service-review/output',['CERTIFICATE.json','INDEPENDENT-CUT.json'])
    add('fresh-service-transcript',C/'shared-half-fresh-transcript/check.py',common+['--word',service,'--old-dual',olddual,'--entropy-review',entropy],'C/shared-half-fresh-transcript/output',['CERTIFICATE.json','MAPPED-DUAL.json'])
    add('independent-service-transcript',R/'shared-half-transcript-review/check.py',['--repo',repo,'--geometry',rootgeo,'--entropy',rootentropy,'--word',service,'--mapped',mapped,'--old-dual',olddual],'R/shared-half-transcript-review/output',['RESULT.json'])
    add('anticommuting-interface',B/'prefix-anticommuting-first-interface/check.py',['--repo',repo,'--normalizer',normalizer],'B/prefix-anticommuting-first-interface',['RESULT.json','WORDS.json'])
    add('independent-interface',R/'anticommuting-interface-review/check.py',['--repo',repo,'--source-review',source_review,'--normalizer',normalizer,'--author',B/'prefix-anticommuting-first-interface'],'R/anticommuting-interface-review/output',['RESULT.json'])
    selected=set(a.only or [r[0] for r in commands]);assert selected<={r[0] for r in commands}
    def run(row):
        name,script,options=row
        done=subprocess.run([sys.executable,'-B',str(script),*map(str,options),'--out',str(out/name)],cwd=repo,capture_output=True,text=True)
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
    result={'status':'PASS_S020_CHECKPOINT7_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'A shared-half word is independently reconstructed by C. Root independently audits C conditioned actual-cut geometry and dual, and B changed-interface source kernels, literal unit primitives and184 omitted ADDs. Reexecution is not independent proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(records),'checks',len(matched),'byte-identical outputs')
if __name__=='__main__':main()
