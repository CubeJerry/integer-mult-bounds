"""Reproduce the fixed-port obstruction and actual paid placement variants."""
from pathlib import Path
import argparse,concurrent.futures,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
R=a.repo/'research/moonshot-005-program/results';D=R/'bit-decoder-placement';base=R/'bit-higher-source-delivery/thirty-four/output/WORD.json';done=[]
def run(name,path,*args):
 cmd=[sys.executable,'-B',str(path)]+list(map(str,args));v=subprocess.run(cmd,capture_output=True,text=True);(a.out/(name+'.log')).write_text(v.stdout+v.stderr);done.append({'name':name,'command':cmd,'returncode':v.returncode})
 if v.returncode:raise RuntimeError(name+':'+v.stderr[-2000:])
run('port29-build',D/'port29/build.py','--base',base,'--out',a.out/'port29');assert(a.out/'port29/WORD.json').read_bytes()==(D/'port29/output/WORD.json').read_bytes()
run('ports-envelope',D/'port-envelope/check.py','--repo',a.repo,'--word',base,'--out',a.out/'envelope')
tasks=[('port29-author',D/'port29/check.py','--repo',a.repo,'--base',base,'--out',a.out/'port29'),('port29-independent',D/'independent-port29/check.py','--repo',a.repo,'--base',base,'--word',a.out/'port29/WORD.json','--out',a.out/'port29-independent'),('port-screen',D/'port-envelope/ports.py','--repo',a.repo,'--word',base,'--envelope',a.out/'envelope/RESULT.json','--out',a.out/'envelope'),('interface-independent',D/'independent-interface/check.py','--repo',a.repo,'--word',base,'--envelope',R/'bit-private-bank-reduction/author/output/RESULT.json','--compression',R/'bit-bank-compression/author/output/RESULT.json','--ports',D/'port-envelope/output/RESULT.json','--out',a.out/'interface-independent')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(lambda x:run(*x),tasks))
run('port29-price',D/'port29/price.py','--out',a.out/'port29')
X=R/'bit-cross-bank-recoding'
run('port41-build',D/'port41/build.py','--base',base,'--out',a.out/'port41');assert(a.out/'port41/WORD.json').read_bytes()==(D/'port41/output/WORD.json').read_bytes()
run('coupling-build',X/'author/build.py','--base',base,'--out',a.out/'coupling');assert(a.out/'coupling/WORD.json').read_bytes()==(X/'author/output/WORD.json').read_bytes()
tasks2=[('port41-author',D/'port41/check.py','--repo',a.repo,'--base',base,'--out',a.out/'port41'),('port41-root',D/'root-port41/check.py','--repo',a.repo,'--word',a.out/'port41/WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--certificate',D/'port41/output/RESULT.json','--out',a.out/'port41-root.json'),('port41-family-root',D/'root-port41/family.py','--repo',a.repo,'--base',base,'--word',a.out/'port41/WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--out',a.out/'port41-family-root.json'),('coupling-author',X/'author/check.py','--repo',a.repo,'--base',base,'--word',a.out/'coupling/WORD.json','--out',a.out/'coupling'),('coupling-independent',X/'independent-b/check.py','--repo',a.repo,'--base',base,'--word',a.out/'coupling/WORD.json','--out',a.out/'coupling-independent'),('coupling-root',X/'root-review/check.py','--repo',a.repo,'--word',a.out/'coupling/WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--certificate',X/'author/output/RESULT.json','--out',a.out/'coupling-root.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:list(pool.map(lambda x:run(*x),tasks2))
run('port41-price',D/'port41/price.py','--out',a.out/'port41')

Y=R/'bit-composed-coded-source'
run('composition-author',Y/'author/check.py','--repo',a.repo,'--base',base,'--port',D/'port41/output/WORD.json','--cross',X/'author/output/WORD.json','--out',a.out/'composition')
assert(a.out/'composition/WORD.json').read_bytes()==(Y/'author/output/WORD.json').read_bytes()
run('composition-independent',Y/'independent-b/check.py','--base',D/'port41/output/WORD.json','--word',a.out/'composition/WORD.json','--out',a.out/'composition-independent')

(a.out/'REPRODUCTION.json').write_text(json.dumps({'status':'PASS_CP10_REPRODUCTION','commands':done,'byte_identical_rebuilt_words':4,'new_complete_kappa':False},indent=2)+'\n');print('PASS_CP10_REPRODUCTION',len(done),'commands')
