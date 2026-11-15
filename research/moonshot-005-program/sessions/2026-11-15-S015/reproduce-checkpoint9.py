#!/usr/bin/env python3
"""Portable frozen CP9 joint-source/interface replay; no evidence is overwritten."""
import argparse,concurrent.futures,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
GROUPS=('two','three','interface')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--only',choices=GROUPS);a=ap.parse_args();repo=a.repo.resolve();out=a.out.resolve();results=repo/'research/moonshot-005-program/results';assert results.is_dir();assert results not in(out,*out.parents),'--out must be outside frozen results';out.mkdir(parents=True,exist_ok=True)
 def group(name):
  work=out/name;work.mkdir(parents=True,exist_ok=True);commands=[];comparisons=[];status='PASS';error=None
  def copy(src,dst):
   assert src.is_dir(),('missing source',str(src));shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));return dst
  def run(label,script,*args):
   cmd=[sys.executable,'-B',str(script),*map(str,args)];started=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,cwd=work,timeout=240);log=work/(label+'.log');log.write_text(p.stdout+p.stderr);commands.append({'group':name,'label':label,'command':cmd,'exit_code':p.returncode,'seconds':round(time.monotonic()-started,3),'log':str(log.relative_to(out))});assert p.returncode==0,(label,p.stderr[-4000:])
  def compare(src,dst,kind='stable_receipt'):
   x,y=src.read_bytes(),dst.read_bytes()
   if kind in('word','frozen_geometry','corroborating_pin_only'):assert x==y,(kind,str(src),str(dst))
   else:assert json.loads(x)==json.loads(y),('receipt changed',str(src),str(dst))
   comparisons.append({'group':name,'committed':str(src.relative_to(repo)),'reproduced':str(dst.relative_to(out)),'kind':kind,'comparison':'byte_identical'if x==y else'json_equal','committed_sha256':hashlib.sha256(x).hexdigest(),'reproduced_sha256':hashlib.sha256(y).hexdigest()})
  try:
   if name in('two','three'):
    p=results/'bit-joint-a2-mds-source';author=name+'-author';q=copy(p/author,work/author)
    # Geometry is a pinned certificate input. Its discovery/search script is
    # not part of rebuilding the proved static word.
    compare(p/author/'GEOMETRY.json',q/'GEOMETRY.json','frozen_geometry')
    run('build',q/'build.py','--repo',repo);compare(p/author/'WORD.json',q/'WORD.json','word')
    run('author',q/'check.py','--repo',repo);compare(p/author/'RESULT.json',q/'RESULT.json')
    run('price',q/'price.py');compare(p/author/'PRICE.json',q/'PRICE.json')
    bname=name+'-review-b';b=copy(p/bname,work/bname);run('independent-b',b/'check.py','--repo',repo,'--source',q,'--out',b/'RESULT.json');compare(p/bname/'RESULT.json',b/'RESULT.json')
    if name=='three':
     r=copy(p/'three-review-a',work/'three-review-a')
     run('independent-a-word',r/'check.py','--repo',repo,'--source',q,'--out',r/'output');compare(p/'three-review-a/output/RESULT.json',r/'output/RESULT.json')
     run('independent-a-basis',r/'check_basis.py','--repo',repo,'--source',q,'--out',r/'output');compare(p/'three-review-a/output/BASIS-RESULT.json',r/'output/BASIS-RESULT.json')
     run('independent-a-price',r/'check_budget.py','--source',q,'--out',r/'output');compare(p/'three-review-a/output/BUDGET-RESULT.json',r/'output/BUDGET-RESULT.json')
   elif name=='interface':
    p=results/'bit-a2-source-interface';source=copy(results/'bit-joint-a2-mds-source/three-author',work/'source-three');q=copy(p/'author-root',work/'author-root');r=copy(p/'independent-c',work/'independent-c')
    run('root-source-interface',q/'check.py','--repo',repo,'--source',source,'--out',q/'output');compare(p/'author-root/output/RESULT.json',q/'output/RESULT.json')
    run('independent-c',r/'check.py','--repo',repo,'--word',source/'WORD.json','--certificate',q/'output/RESULT.json');compare(p/'independent-c/RESULT.json',r/'RESULT.json')
    # This corroboration restates the same one-chart criterion; preserve pins
    # without claiming a second new theorem or a fresh independent proof run.
    c=copy(p/'corroborating-c',work/'corroborating-c');manifest=json.loads((c/'MANIFEST.json').read_text())
    for rel,pin in manifest['files'].items():
     assert hashlib.sha256((c/rel).read_bytes()).hexdigest()==pin;compare(p/'corroborating-c'/rel,c/rel,'corroborating_pin_only')
   else:raise AssertionError(name)
  except Exception as exc:status='FAIL';error=repr(exc)
  finally:
   (work/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');(work/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n')
  return{'group':name,'status':status,'error':error,'commands':commands,'comparisons':comparisons}
 names=[a.only]if a.only else list(GROUPS)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:done=list(pool.map(group,names))
 commands=[v for g in done for v in g['commands']];comparisons=[v for g in done for v in g['comparisons']];failures=[{'group':g['group'],'error':g['error']}for g in done if g['status']!='PASS']
 (out/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');(out/'COMPARISONS.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 summary={'status':'PASS_CP9_PORTABLE_REPLAY'if not failures else'FAIL_CP9_PORTABLE_REPLAY','groups':names,'commands':len(commands),'comparisons':len(comparisons),'byte_identical':sum(c['comparison']=='byte_identical'for c in comparisons),'word_comparisons':sum(c['kind']=='word'for c in comparisons),'corroborating_pin_only_comparisons':sum(c['kind']=='corroborating_pin_only'for c in comparisons),'corroboration_status':'Pin preservation only; not a new theorem or independent proof replay.','failures':failures};(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
 if failures:sys.exit(1)
if __name__=='__main__':main()
