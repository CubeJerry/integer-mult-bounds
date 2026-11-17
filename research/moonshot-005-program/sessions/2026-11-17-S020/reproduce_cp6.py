#!/usr/bin/env python3
"""Focused S020 checkpoint6 reproduction; Python3.11+ and SymPy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);p=repo/'research/moonshot-005-program';s=p/'sessions/2026-11-17-S020';e=s/'checkpoint6-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP6.json'
    for pin in json.loads(pins.read_text())['files']:assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    geo=s/'checkpoint2-evidence/C/four-plane-review/check.py';sr=s/'checkpoint3-evidence/C/proper-query-export-review/check.py';entropy=s/'checkpoint1-evidence/C/entropy54-review/check.py'
    native=p/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';parent=s/'checkpoint5-evidence/A/full-half-reservoir/WORD.json';parity=A/'parity-receiver-relays/WORD.json';sixteen=C/'parity-sixteen-diagonals/output/WORD.json'
    olddual=s/'checkpoint4-evidence/R/fresh-transcript-nine/output/MAPPED-DUAL.json';mapped=C/'sixteen-fresh-transcript/output/MAPPED-DUAL.json';rootgeo=s/'checkpoint4-evidence/R/fresh-eight-facet-cut/check.py';rootentropy=s/'checkpoint1-evidence/R/entropy54/check.py'
    commands=[];comparisons=[]
    def add(name,script,options,folder,files):
        commands.append((name,script,options));comparisons.extend((name+'/'+f,folder+'/'+f) for f in files)
    trio=['WORD.json','RESULT.json','CUT-INVENTORY.json'];common=['--native',native,'--source-review',sr,'--arithmetic',geo]
    add('parity-relay',A/'build_parity_receiver_relays.py',['--repo',repo,'--parent',parent],'A/parity-receiver-relays',trio)
    add('independent-parity',C/'parity-relay-review/check.py',common+['--parent',parent,'--word',parity],'C/parity-relay-review/output',['CERTIFICATE.json','INDEPENDENT-CUT.json'])
    add('sixteen-values',C/'parity-sixteen-diagonals/build.py',common+['--parent',parity],'C/parity-sixteen-diagonals/output',trio)
    add('independent-sixteen',A/'review_sixteen_diagonals.py',['--repo',repo,'--word',sixteen,'--parent',parity,'--author-result',sixteen.with_name('RESULT.json'),'--author-inventory',sixteen.with_name('CUT-INVENTORY.json')],'A/sixteen-diagonals-review',['RESULT.json'])
    add('fresh-transcript',C/'sixteen-fresh-transcript/check.py',common+['--word',sixteen,'--old-dual',olddual,'--entropy-review',entropy],'C/sixteen-fresh-transcript/output',['CERTIFICATE.json','MAPPED-DUAL.json'])
    add('independent-transcript',R/'sixteen-transcript-review/check.py',['--repo',repo,'--geometry',rootgeo,'--entropy',rootentropy,'--word',sixteen,'--mapped',mapped,'--old-dual',olddual],'R/sixteen-transcript-review/output',['RESULT.json'])
    add('endpoint-column',B/'prefix-three-bank-endpoint-column/check.py',['--repo',repo],'B/prefix-three-bank-endpoint-column',['RESULT.json','WORDS.json'])
    add('independent-column',R/'endpoint-column-review/check.py',['--repo',repo,'--author',B/'prefix-three-bank-endpoint-column'],'R/endpoint-column-review/output',['RESULT.json'])
    add('column-gate',B/'prefix-endpoint-column-gate/check.py',['--repo',repo,'--positive',B/'prefix-three-bank-endpoint-column'],'B/prefix-endpoint-column-gate',['RESULT.json'])
    add('independent-column-gate',R/'endpoint-column-gate-review/check.py',['--repo',repo,'--source-review',R/'endpoint-column-review/check.py','--author',B/'prefix-endpoint-column-gate'],'R/endpoint-column-gate-review/output',['RESULT.json'])
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
    result={'status':'PASS_S020_CHECKPOINT6_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'A relay is independently reconstructed by C; C16-value source by A. Root independently reconstructs C postcut geometry and dual, B column primitives and source identities, and B endpoint-dimension gate. Reexecution is not independent proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(records),'checks',len(matched),'byte-identical outputs')
if __name__=='__main__':main()
