"""Reproduce actual30 word, acquisition envelope and four-bit family proofs."""
from pathlib import Path
import argparse,concurrent.futures,json,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
R=a.repo/'research/moonshot-005-program/results';B=R/'bit-three-cell-retention';E=R/'bit-acquisition-bank-envelope';C=R/'complex-four-bit-family';base=R/'bit-six-channel-retention/twenty-seven/output/WORD.json';done=[]
def run(name,path,*args):
 cmd=[sys.executable,'-B',str(path)]+list(map(str,args));r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(a.out/(name+'.log')).write_text(r.stdout);done.append({'name':name,'command':cmd,'returncode':r.returncode})
 if r.returncode:raise RuntimeError(name+':'+r.stdout[-2000:])
fresh=a.out/'word30';run('build30',B/'author/build.py','--repo',a.repo,'--base',base,'--out',fresh);assert(fresh/'WORD.json').read_bytes()==(B/'author/output/WORD.json').read_bytes()
for n in ['classification','audit']:shutil.copytree(C/n,a.out/n,dirs_exist_ok=True)
tasks=[('author30',B/'author/check.py','--repo',a.repo,'--base',base,'--out',fresh),('root30',B/'root-review/check.py','--repo',a.repo,'--word',fresh/'WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--certificate',B/'author/output/RESULT.json','--out',a.out/'root30.json'),('bank-author',E/'author/check.py','--repo',a.repo,'--word',base,'--out',a.out/'bank-author'),('bank-root',E/'root-review/check.py','--repo',a.repo,'--word',base,'--engine',R/'bit-shared-meet-funnel/root-review','--certificate',E/'author/output/RESULT.json','--out',a.out/'bank-root.json'),('classification-author',a.out/'classification/check.py','--repo',a.repo),('classification-root',C/'root-classification/check.py','--engine',R/'complex-boolean-sign-family/root-review/check.py','--proof',C/'classification/PROOF.md','--out',a.out/'classification-root.json'),('audit-author',a.out/'audit/check.py','--repo',a.repo),('audit-root',C/'root-audit/check.py','--engine',R/'complex-boolean-sign-family/root-review/check.py','--audit',C/'audit/AUDIT.md','--out',a.out/'audit-root.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(lambda x:run(*x),tasks))
run('price30',B/'author/price.py','--out',fresh)
(a.out/'REPRODUCTION.json').write_text(json.dumps({'status':'PASS_CP8_REPRODUCTION','commands':done,'byte_identical_rebuilt_words':1,'new_complete_kappa':False},indent=2)+'\n');print('PASS_CP8_REPRODUCTION',len(done),'commands')
