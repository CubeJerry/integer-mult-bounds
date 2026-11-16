"""Reproduce inverse/coset and archived-star applications without changing sources."""
import argparse,concurrent.futures,json,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
R=a.repo/'research/moonshot-005-program/results';B=R/'bit-actual-six-grant-puncture';C=R/'complex-inverse-native-coset';done=[]
def run(name,path,*args):
 cmd=[sys.executable,'-B',str(path)]+list(map(str,args));r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(a.out/(name+'.log')).write_text(r.stdout);done.append({'name':name,'command':cmd,'returncode':r.returncode})
 if r.returncode:raise RuntimeError(name+':'+r.stdout[-2000:])
tasks=[]
for sub in ['inverse','two-native','fixed-boundary']:
 dest=a.out/sub;shutil.copytree(C/sub,dest,dirs_exist_ok=True);tasks.append((sub,dest/'check.py','--repo',a.repo))
tasks += [('star-author',B/'author/check.py','--repo',a.repo,'--source',B/'author/SOURCE.json','--out',a.out/'star-author'),('star-root',B/'root-review/check.py','--repo',a.repo,'--source',B/'author/SOURCE.json','--out',a.out/'star-root.json'),('complex-root',C/'root-review/check.py','--engine',R/'complex-boolean-sign-family/root-review/check.py','--certificates',C/'fixed-boundary/CERTIFICATES.json','--out',a.out/'complex-root.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda x:run(*x),tasks))
for sub in ['inverse','two-native','fixed-boundary']:assert (a.out/sub/'RESULT.json').read_bytes()==(C/sub/'RESULT.json').read_bytes()
assert (a.out/'fixed-boundary/CERTIFICATES.json').read_bytes()==(C/'fixed-boundary/CERTIFICATES.json').read_bytes()
(a.out/'REPRODUCTION.json').write_text(json.dumps({'status':'PASS_CP6_REPRODUCTION','commands':done,'byte_identical_author_results':3,'byte_identical_coset_certificate':True},indent=2)+'\n');print('PASS_CP6_REPRODUCTION',len(done),'commands')
