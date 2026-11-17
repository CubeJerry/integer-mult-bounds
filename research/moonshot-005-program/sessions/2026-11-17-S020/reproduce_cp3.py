#!/usr/bin/env python3
"""Focused S020 checkpoint3 reproduction; Python3.11+ with SymPy. Use fresh output."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);s=repo/'research/moonshot-005-program/sessions/2026-11-17-S020';e=s/'checkpoint3-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP3.json'
    for pin in json.loads(pins.read_text())['files']:
        assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    geo=s/'checkpoint2-evidence/C/four-plane-review/check.py';qi=s/'checkpoint2-evidence/C/klein-interface-review/check.py';capacity=s/'checkpoint1-evidence/C/ordinary-module-capacity'
    restored=A/'composed-four-plane-corrections/WORD.json';low=A/'low-retention-corrections/WORD.json';export=A/'proper-query-exports/WORD.json'
    commands=[
      ('author-restored',A/'build_composed_four_plane_corrections.py',['--repo',repo]),
      ('author-low',A/'build_low_retention_corrections.py',['--repo',repo,'--parent',restored]),
      ('author-export',A/'build_proper_query_exports.py',['--repo',repo,'--parent',low]),
      ('independent-restored',R/'composed-correction-review/check.py',['--repo',repo,'--word',restored,'--variant','restored']),
      ('independent-low',R/'composed-correction-review/check.py',['--repo',repo,'--word',low,'--variant','low']),
      ('independent-export',C/'proper-query-export-review/check.py',['--native',A/'SOURCE-RECOVERY.json','--word',export,'--parent',low,'--arithmetic',geo]),
      ('small-half-gate',R/'small-half-extensions/check.py',['--repo',repo,'--restored-review',R/'composed-correction-review/output/RESULT.json','--low-review',R/'composed-correction-review/low-output/RESULT.json']),
      ('independent-small-half',A/'review_small_half_extensions.py',['--inputs',A,'--author-certificate',R/'small-half-extensions/output/CERTIFICATE.json']),
      ('independent-priced-occurrence',C/'priced-occurrence-review/check.py',['--inputs',A,'--arithmetic',geo]),
      ('coupled-column',C/'klein-coupled-column/check.py',['--arithmetic',qi]),
      ('kernel-transfer',C/'klein-transferred-kernel/check.py',['--arithmetic',qi]),
      ('independent-kernel-transfer',B/'klein-transfer-independent-review/check.py',['--repo',repo,'--source',C/'klein-transferred-kernel']),
      ('rotation-capacity',B/'third-column-capacity-gate/check.py',['--repo',repo,'--capacity',capacity]),
      ('independent-complex-premises',R/'complex-endpoint-review/check.py',['--repo',repo,'--c4-package',B/'third-column-capacity-gate']),
    ]
    selected=set(a.only or [row[0]for row in commands]);assert selected<={row[0]for row in commands}
    records=[]
    for name,script,options in commands:
        if name not in selected:continue
        done=subprocess.run([sys.executable,'-B',str(script),*map(str,options),'--out',str(out/name)],cwd=repo,capture_output=True,text=True)
        (out/(name+'.log')).write_text(done.stdout+done.stderr)
        records.append({'name':name,'script':str(script.relative_to(repo)),'script_sha256':digest(script),'exit_code':done.returncode})
        print(name,'PASS'if done.returncode==0 else'FAIL',flush=True)
        if done.returncode:raise RuntimeError(done.stderr[-5000:])
    comparisons=[]
    for name,folder in [('restored','composed-four-plane-corrections'),('low','low-retention-corrections'),('export','proper-query-exports')]:
        for f in ['WORD.json','RESULT.json','CUT-INVENTORY.json']:comparisons.append((f'author-{name}/{f}',f'A/{folder}/{f}'))
    for name,folder in [('restored','R/composed-correction-review/output'),('low','R/composed-correction-review/low-output'),('export','C/proper-query-export-review/output')]:
        for f in ['RESULT.json','INDEPENDENT-CUT.json']:comparisons.append((f'independent-{name}/{f}',f'{folder}/{f}'))
    comparisons += [('small-half-gate/CERTIFICATE.json','R/small-half-extensions/output/CERTIFICATE.json'),('independent-small-half/RESULT.json','A/small-half-review/RESULT.json'),('independent-priced-occurrence/RESULT.json','C/priced-occurrence-review/output/RESULT.json')]
    for name,folder in [('coupled-column','C/klein-coupled-column/output'),('kernel-transfer','C/klein-transferred-kernel/output'),('rotation-capacity','B/third-column-capacity-gate')]:
        for f in ['RESULT.json','WORDS.json']:comparisons.append((f'{name}/{f}',f'{folder}/{f}'))
    comparisons += [('independent-kernel-transfer/RESULT.json','B/klein-transfer-independent-review/RESULT.json'),('independent-complex-premises/RESULT.json','R/complex-endpoint-review/output/RESULT.json')]
    matched=[]
    for fresh,frozen in comparisons:
        if fresh.split('/')[0]not in selected:continue
        actual=digest(out/fresh);assert actual==digest(e/frozen),'Exact reproduction mismatch: '+frozen
        matched.append({'path':frozen,'sha256':actual})
    result={'status':'PASS_S020_CHECKPOINT3_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'A actual words reviewed by root/C using separate geometry. Root literal-half code reviewed independently by A; price lemma by C. C actual transfer reviewed by B using separate arithmetic. Root independently reviews the coupled-column and endpoint proofs and checks literal premises/C4 words. Reexecution is not independent proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(matched),'byte-identical outputs')
if __name__=='__main__':main()
