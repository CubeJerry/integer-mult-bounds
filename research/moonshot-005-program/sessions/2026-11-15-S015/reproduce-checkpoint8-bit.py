#!/usr/bin/env python3
"""Portable CP8 BIT replays in disposable copies of the frozen packages.

Run from any cwd with --repo REPO --out OUTPUT [--only GROUP].  No committed
author/review tree is modified.  Word hashes and stable JSON receipts are
compared against the exact committed copies, with commands/logs preserved.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

GROUPS=('rectangular','memory','early','common','direct','parametric')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--only',choices=GROUPS)
    a=ap.parse_args()
    repo=a.repo.resolve();out=a.out.resolve()
    results=repo/'research/moonshot-005-program/results'
    assert results.is_dir(),results
    # A replay output must not be anywhere inside frozen result packages.
    assert results not in (out,*out.parents),'--out must be outside frozen results'
    out.mkdir(parents=True,exist_ok=True)

    def group(name):
        work=out/name;work.mkdir(parents=True,exist_ok=True)
        commands=[];comparisons=[];status='PASS';error=None
        def copy(src,dst):
            assert src.is_dir(),('missing source',str(src))
            shutil.copytree(src,dst,dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            return dst
        def run(label,script,*args):
            cmd=[sys.executable,'-B',str(script),*map(str,args)]
            started=time.monotonic()
            proc=subprocess.run(cmd,capture_output=True,text=True,cwd=work,timeout=240)
            log=work/(label+'.log');log.write_text(proc.stdout+proc.stderr)
            commands.append({'group':name,'label':label,'command':cmd,
                             'exit_code':proc.returncode,
                             'seconds':round(time.monotonic()-started,3),
                             'log':str(log.relative_to(out))})
            assert proc.returncode==0,(label,proc.stderr[-4000:])
        def compare(src,dst,word=False):
            x,y=src.read_bytes(),dst.read_bytes()
            if word:
                assert x==y,('word bytes changed',str(src),str(dst))
            else:
                assert json.loads(x)==json.loads(y),('receipt changed',str(src),str(dst))
            comparisons.append({'group':name,'committed':str(src.relative_to(repo)),
                                'reproduced':str(dst.relative_to(out)),
                                'comparison':'byte_identical' if x==y else 'json_equal',
                                'kind':'word' if word else 'stable_receipt',
                                'committed_sha256':hashlib.sha256(x).hexdigest(),
                                'reproduced_sha256':hashlib.sha256(y).hexdigest()})
        def predecessor():
            return copy(results/'bit-shared-facet-mds/author',work/'deps/shared-facet-coding')
        try:
            if name=='rectangular':
                p=results/'bit-clipped-rectangular-source'
                # The independently frozen checker intentionally pins its
                # original sibling path. Recreate it instead of editing code.
                q=copy(p/'author-root',work/'root/rectangular-chart-source-gate')
                r=copy(p/'independent-a',work/'worker-a/review-rectangular-filtration')
                run('author',q/'check.py','--out',q/'output')
                compare(p/'author-root/output/RESULT.json',q/'output/RESULT.json')
                run('independent-a',r/'check.py')
                compare(p/'independent-a/RESULT.json',r/'RESULT.json')
            elif name=='memory':
                p=results/'bit-early-hub-memory';prior=predecessor()
                q=copy(p/'author',work/'author')
                r=copy(p/'review-root',work/'review-root')
                c=copy(p/'independent-c',work/'independent-c')
                run('author',q/'check.py','--repo',repo,'--source',prior)
                compare(p/'author/RESULT.json',q/'RESULT.json')
                run('root-review',r/'check.py','--repo',repo,'--source',prior,'--out',r/'output')
                compare(p/'review-root/output/RESULT.json',r/'output/RESULT.json')
                run('independent-c',c/'check.py','--repo',repo,'--source',prior)
                compare(p/'independent-c/RESULT.json',c/'RESULT.json')
            elif name=='early':
                p=results/'bit-cached-early-hub'
                versions={v:copy(p/v,work/v) for v in ('one','two')}
                for v,q in versions.items():
                    run(v+'-build',q/'build.py','--repo',repo)
                    compare(p/v/'WORD.json',q/'WORD.json',word=True)
                    run(v+'-author',q/'check.py','--repo',repo)
                    compare(p/v/'RESULT.json',q/'RESULT.json')
                    run(v+'-price',q/'price.py')
                    compare(p/v/'PRICE.json',q/'PRICE.json')
                r=copy(p/'independent-b',work/'independent-b')
                run('independent-b',r/'check.py','--repo',repo,
                    '--one',versions['one'],'--two',versions['two'],'--out',r/'RESULT.json')
                compare(p/'independent-b/RESULT.json',r/'RESULT.json')
            elif name in ('common','direct'):
                p=results/'bit-canonical-mds-chronology';prior=predecessor()
                author_name=name+'-author';review_name=name+'-review'
                q=copy(p/author_name,work/author_name)
                r=copy(p/review_name,work/review_name)
                run('build',q/'build.py','--repo',repo,
                    '--local',prior/'four-chart-word/WORD.json')
                compare(p/author_name/'WORD.json',q/'WORD.json',word=True)
                run('author',q/'check.py','--repo',repo)
                compare(p/author_name/'RESULT.json',q/'RESULT.json')
                run('price',q/'price.py')
                compare(p/author_name/'PRICE.json',q/'PRICE.json')
                run('independent-word',r/'check.py','--repo',repo,'--source',q,'--out',r/'output')
                compare(p/review_name/'output/RESULT.json',r/'output/RESULT.json')
                if name=='direct':
                    run('independent-basis',r/'check_basis.py','--repo',repo,'--source',q,'--out',r/'output')
                    compare(p/review_name/'output/BASIS-RESULT.json',r/'output/BASIS-RESULT.json')
                run('independent-budget',r/'check_budget.py','--source',q,'--out',r/'output')
                compare(p/review_name/'output/BUDGET-RESULT.json',r/'output/BUDGET-RESULT.json')
            elif name=='parametric':
                p=results/'bit-canonical-mds-chronology'
                q=copy(p/'parametric-root',work/'parametric-root')
                r=copy(p/'parametric-review',work/'parametric-review')
                run('root-certificate-price',q/'check.py','--repo',repo,'--out',q/'output')
                for f in ('CERTIFICATE.json','BUDGET.json'):
                    compare(p/'parametric-root/output'/f,q/'output'/f)
                run('independent-a',r/'check.py','--repo',repo,'--proof',q/'PROOF.md','--out',r/'output')
                compare(p/'parametric-review/output/RESULT.json',r/'output/RESULT.json')
            else:
                raise AssertionError(name)
        except Exception as exc:
            status='FAIL';error=repr(exc)
        finally:
            (work/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
            (work/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n')
        return {'group':name,'status':status,'error':error,
                'commands':commands,'comparisons':comparisons}

    names=[a.only] if a.only else list(GROUPS)
    completed=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        completed=list(pool.map(group,names))
    commands=[c for g in completed for c in g['commands']]
    comparisons=[c for g in completed for c in g['comparisons']]
    (out/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    (out/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n')
    failures=[{'group':g['group'],'error':g['error']} for g in completed if g['status']!='PASS']
    summary={'status':'PASS_CP8_BIT_PORTABLE_REPLAY' if not failures else 'FAIL_CP8_BIT_PORTABLE_REPLAY',
             'groups':names,'commands':len(commands),'comparisons':len(comparisons),
             'byte_identical':sum(c['comparison']=='byte_identical' for c in comparisons),
             'word_comparisons':sum(c['kind']=='word' for c in comparisons),'failures':failures}
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))
    if failures:sys.exit(1)


if __name__=='__main__':main()
