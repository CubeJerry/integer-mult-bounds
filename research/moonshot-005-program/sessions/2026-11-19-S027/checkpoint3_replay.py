"""Portable serial replay of S027 checkpoint3; not a new independent review."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--group',choices=['core','words','all'],default='all');a=ap.parse_args()
 repo=a.repo.resolve();base=repo/'research/moonshot-005-program/results';a.out.mkdir(parents=True,exist_ok=True)
 names={'masks':'bit-fixed-transfer-source-masks','support':'bit-one-d-terminal-support-gate','correlated':'bit-correlated-middle-phase-completion','commuting':'bit-nonsemisimple-commuting-source-gate','covariant':'bit-receiver-covariant-target','return':'bit-return-aware-source-rank','pair':'bit-native-shared-receiver-pair','overlap':'bit-native-masked-overlap','frame':'bit-native-common-frame-k-stitch'}
 p={k:base/v for k,v in names.items()};jobs=[]
 def add(group,name,script,args,expected,output='RESULT.json',fileout=False):jobs.append((group,name,script,args,expected,output,fileout))
 for key in ['masks','correlated','return']:
  add('core',key+'-author',p[key]/'author/check.py',[],p[key]/'author/output/RESULT.json')
  arg=['--proof',p[key]/'author/PROOF.md'] if key=='return' else ['--author',p[key]/'author']
  add('core',key+'-review',p[key]/'review/check.py',arg,p[key]/'review/output/RESULT.json')
 for key in ['support','commuting','covariant']:
  add('core',key+'-author',p[key]/'author/check.py',['--repo',repo],p[key]/'author/output/RESULT.json')
  args=['--repo',repo,'--author',p[key]/'author']
  if key!='covariant':args+=['--kind',key]
  add('core',key+'-review',p[key]/'review/check.py',args,p[key]/'review/output/RESULT.json')
 pins={'pair':'2b5f5dd5cefc36523787191b359d04d00a38cfa3ef025044c78e32314d86f794','overlap':'6096382d0542028f812130d707dbd299de23bbc52a800283ef219f9f9ab45ae7','frame':'806dca8703c7ca75854b91d9946f81c5df72b77614aa3b62b5a2e2c53692411a'}
 ledger={'pair':'shared-pair','overlap':'overlap','frame':'k-frame'}
 for key in ['pair','overlap','frame']:
  author=p[key]/'author';word=author/'output/WORD.json.gz'
  add('words',key+'-author',author/'build.py',['--repo',repo],author/'output/RESULT.json')
  add('words',key+'-owner-review',p['frame']/'owner-review/check.py',['--repo',repo,'--word',word,'--word-pin',pins[key]],p['frame']/'owner-review'/ledger[key]/'RESULT.json')
  args=['--repo',repo,'--word',word]
  args+=['--matrices',author/'output/MATRICES.json.gz'] if key=='pair' else ['--certificate',author/'output/CERTIFICATE.json.gz']
  add('words',key+'-controls',author/'controls.py',args,author/'controls/RESULT.json')
 add('words','pair-cut-gates',p['pair']/'author/gates.py',['--repo',repo],p['pair']/'author/output/GATES.json','GATES.json')
 add('words','overlap-mask-comparison',p['overlap']/'author/compare_masks.py',['--preferred',p['overlap']/'author/output/WORD.json.gz','--control',p['overlap']/'author/late-mask-control/WORD.json.gz'],p['overlap']/'author/output/MASK-COMPARISON.json','MASK-COMPARISON.json')
 add('words','overlap-response-review',p['masks']/'author/native_check.py',['--author',p['overlap']/'author'],p['masks']/'author/output/NATIVE-RESULT.json','NATIVE-RESULT.json')
 add('words','frame-author-audit',p['frame']/'author/audit.py',['--word',p['frame']/'author/output/WORD.json.gz','--certificate',p['frame']/'author/output/CERTIFICATE.json.gz'],p['frame']/'author/output/AUDIT.json','AUDIT.json')
 add('words','frame-saturation-author',p['frame']/'author/screen.py',['--repo',repo],p['frame']/'author/output/SYSTEM-SCREEN.json','SYSTEM-SCREEN.json')
 for label in ['response-review','saturation-review']:
  add('words','frame-'+label,p['frame']/label/'check.py',['--repo',repo,'--author',p['frame']/'author'],p['frame']/label/'output/RESULT.json')
 add('words','frame-coordinate-nilpotence',p['frame']/'response-review/nilpotence.py',['--word',p['frame']/'author/output/WORD.json.gz'],p['frame']/'response-review/output/NILPOTENCE.json','NILPOTENCE.json',True)
 results=[]
 for group,name,script,args,expected,output,fileout in jobs:
  if a.group!='all' and group!=a.group:continue
  dest=a.out/name;target=dest/output;start=time.monotonic()
  cmd=[sys.executable,'-B',str(script),*map(str,args),'--out',str(target if fileout else dest)]
  proc=subprocess.run(cmd,cwd=repo,text=True,capture_output=True,timeout=900)
  if proc.returncode:raise RuntimeError(name+' failed\n'+proc.stdout[-2000:]+'\n'+proc.stderr[-4000:])
  if json.loads(target.read_text())!=json.loads(expected.read_text()):raise RuntimeError(name+' differs from frozen receipt')
  item={'name':name,'script':str(script.relative_to(repo)),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'matches_frozen_json':True,'seconds':round(time.monotonic()-start,3)}
  results.append(item);print(json.dumps(item),flush=True)
 result={'status':'PASS_S027_CHECKPOINT3_RELOCATED_REPLAY','group':a.group,'checks':results,'scope':'Reproduction of separately authored/reviewed evidence; not another independent review.','new_complete_kappa':False}
 (a.out/'VALIDATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
