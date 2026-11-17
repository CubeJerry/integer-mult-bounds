#!/usr/bin/env python3
"""Reproduce reviewed S020 checkpoint4 evidence; Python3.11+ with SymPy."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',action='append');ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    if out.exists()and any(out.iterdir()):raise ValueError('Use an empty output directory')
    out.mkdir(parents=True,exist_ok=True);s=repo/'research/moonshot-005-program/sessions/2026-11-17-S020';e=s/'checkpoint4-evidence';A=e/'A';B=e/'B';C=e/'C';R=e/'R';pins=s/'SOURCE-PINS-CP4.json'
    for pin in json.loads(pins.read_text())['files']:assert digest(repo/pin['path'])==pin['sha256'],pin['path']
    geo=s/'checkpoint2-evidence/C/four-plane-review/check.py';sr=s/'checkpoint3-evidence/C/proper-query-export-review/check.py';er=s/'checkpoint1-evidence/C/entropy54-review/check.py';dual=s/'checkpoint1-evidence/R/entropy54/CERTIFICATE.json'
    native=A/'SOURCE-RECOVERY.json';low=A/'low-retention-corrections/WORD.json';mapped=R/'fresh-transcript-nine/output/MAPPED-DUAL.json';geometry=R/'fresh-eight-facet-cut/check.py';common=['--native',native,'--inputs',A,'--source-review',sr,'--arithmetic',geo]
    commands=[];comparisons=[]
    def add(name,script,options,folder,files):
        commands.append((name,script,options))
        comparisons.extend((name+'/'+f,folder+'/'+f)for f in files)
    trio=['WORD.json','RESULT.json','CUT-INVENTORY.json']
    for number,q in [(4,1),(12,3),(16,4)]:add('pair-'+str(number),A/'build_direct_pair_exports.py',['--repo',repo,'--parent',low,'--queries-per-gadget',str(q)],'A/direct-pair-exports-'+str(number),trio)
    for name,limit in [('1',1),('greedy',19)]:add('cross-'+name,A/'build_cross_quartet_exports.py',['--repo',repo,'--parent',low,'--limit',str(limit)],'A/cross-quartet-export-1'if name=='1'else'A/cross-quartet-exports-greedy',trio)
    add('early-axis',A/'build_early_axis_bootstrap.py',['--repo',repo,'--parent',low],'A/early-axis-known8',trio)
    add('raw-cache',A/'check_raw_cache_reactivation.py',['--repo',repo,'--inputs',A],'A/raw-cache-reactivation',['CERTIFICATE.json'])
    add('four-facets',A/'check_four_facet_fresh_cut.py',['--repo',repo,'--inputs',A],'A/four-facet-fresh-cut',['CERTIFICATE.json'])
    add('raw-forcing',C/'forced-raw-reactivation/check.py',common,'C/forced-raw-reactivation/output',['CERTIFICATE.json'])
    add('raw-fanout',C/'forced-raw-fanout/check.py',common+['--forced',C/'forced-raw-reactivation/output/CERTIFICATE.json'],'C/forced-raw-fanout/output',['CERTIFICATE.json'])
    add('independent-fanout',A/'review_forced_raw_fanout.py',['--inputs',A,'--author-certificate',C/'forced-raw-fanout/output/CERTIFICATE.json'],'A/forced-raw-fanout-review',['RESULT.json'])
    add('independent-pairs',C/'direct-pair-review/check.py',common+['--parent',low],'C/direct-pair-review/output',['RESULT.json','BANK-CERTIFICATE.json'])
    add('eight-facets',geometry,['--repo',repo,'--inputs',A],'R/fresh-eight-facet-cut/output',['CERTIFICATE.json'])
    add('nine-transfers',R/'fresh-transcript-nine/check.py',['--repo',repo,'--inputs',A,'--geometry',geometry],'R/fresh-transcript-nine/output',['CERTIFICATE.json','MAPPED-DUAL.json'])
    add('independent-transcript',C/'fresh-transcript-review/check.py',common+['--certificate',dual,'--mapped',mapped,'--entropy-review',er],'C/fresh-transcript-review/output',['RESULT.json','EXPANDED-MAPPED-DUAL.json'])
    add('independent-84-bound',R/'raw-fanout-review/check.py',['--repo',repo,'--inputs',A,'--fanout',C/'forced-raw-fanout/output/CERTIFICATE.json','--pair-certificate',C/'direct-pair-review/output/BANK-CERTIFICATE.json','--nine-certificate',R/'fresh-transcript-nine/output/CERTIFICATE.json','--geometry',geometry],'R/raw-fanout-review/output',['RESULT.json'])
    add('independent-cross',C/'cross-quartet-review/check.py',common+['--parent',low],'C/cross-quartet-review/output',['RESULT.json','BANK-CERTIFICATE.json'])
    add('independent-early-axis',C/'early-axis-review/check.py',['--native',native,'--word',A/'early-axis-known8/WORD.json','--parent',low,'--source-review',sr,'--arithmetic',geo,'--entropy-review',er,'--mapped',mapped],'C/early-axis-review/output',['RESULT.json','INDEPENDENT-CUT.json','CONTINUATION-CERTIFICATE.json'])
    add('all-source-bound',R/'all-source-fanout/check.py',['--repo',repo,'--word',A/'early-axis-known8/WORD.json','--geometry',geometry],'R/all-source-fanout/output',['CERTIFICATE.json'])
    add('independent-all-source',C/'all-source-exit-review/check.py',['--native',native,'--word',A/'early-axis-known8/WORD.json','--source-result',C/'early-axis-review/output/RESULT.json','--source-review',sr,'--arithmetic',geo],'C/all-source-exit-review/output',['CERTIFICATE.json'])
    for name,author,review,files in [('joint-endpoint','row-support-endpoint-capacity','joint-endpoint-review',['RESULT.json']),('distinguished-plus','distinguished-column-plus-control','distinguished-plus-review',['RESULT.json','WORDS.json']),('crot-coset','crot-source-coset-gate','crot-coset-review',['RESULT.json'])]:
        add(name,B/author/'check.py',['--repo',repo],'B/'+author,files)
        add('independent-'+name,R/review/'check.py',['--repo',repo,'--author',B/author],'R/'+review+'/output',['RESULT.json'])
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
    result={'status':'PASS_S020_CHECKPOINT4_FOCUSED_REPRODUCTION','checks':records,'exact_reproductions':matched,'source_pins_sha256':digest(pins),'independence':'New A source words separately reconstructed by C. C access/fanout certificates reviewed with separate A/root geometry. Root entropy transport reviewed by C with a different dual expansion. Root all-source gate independently reviewed by C. B complex proofs and literal words independently reviewed by root using C sparse exact arithmetic. Reexecution is not independent mathematical proof.','new_complete_kappa':False}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(records),'checks',len(matched),'byte-identical outputs')
if __name__=='__main__':main()
