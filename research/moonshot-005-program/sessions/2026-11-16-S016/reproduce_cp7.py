"""Rebuild the two-retention word and reproduce separate exact source reviews."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
R=a.repo/'research/moonshot-005-program/results';B=R/'bit-two-retention-source';C=R/'complex-four-bit-cubic-source';done=[]
def run(name,path,*args):
 cmd=[sys.executable,'-B',str(path)]+list(map(str,args));r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(a.out/(name+'.log')).write_text(r.stdout);done.append({'name':name,'command':cmd,'returncode':r.returncode})
 if r.returncode:raise RuntimeError(name+':'+r.stdout[-2000:])
build=a.out/'rebuilt';run('build17',B/'author/build.py','--repo',a.repo,'--base',R/'bit-canonical-history-source/author/output/WORD.json','--out',build)
assert (build/'WORD.json').read_bytes()==(B/'author/output/WORD.json').read_bytes()
review=a.out/'independent-a';review.mkdir(exist_ok=True);shutil.copy2(build/'WORD.json',review/'WORD.json');cx=a.out/'complex-author';shutil.copytree(C/'author',cx,dirs_exist_ok=True)
tasks=[('author17',B/'author/check.py','--repo',a.repo,'--out',build),('independent-a17',B/'independent-a/check.py','--repo',a.repo,'--out',review),('root17',B/'root-review/check.py','--repo',a.repo,'--word',build/'WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--out',a.out/'root17.json'),('complex-author',cx/'check.py','--repo',a.repo),('complex-root',C/'root-review/check.py','--engine',R/'complex-boolean-sign-family/root-review/check.py','--price-engine',R/'bit-shared-meet-funnel/root-review/budget.py','--proof',C/'author/PROOF.md','--out',a.out/'complex-root.json')]
CC=R/'complex-four-bit-concentration';cc=a.out/'concentration-author';shutil.copytree(CC/'author',cc,dirs_exist_ok=True)
tasks += [('concentration-author',cc/'check.py','--repo',a.repo),('concentration-root',CC/'root-review/check.py','--proof',CC/'author/PROOF.md','--price-engine',R/'bit-shared-meet-funnel/root-review/budget.py','--out',a.out/'concentration-root.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda x:run(*x),tasks))
run('price17',B/'author/price.py','--out',build)
assert (cx/'RESULT.json').read_bytes()==(C/'author/RESULT.json').read_bytes()
assert (cc/'RESULT.json').read_bytes()==(CC/'author/RESULT.json').read_bytes()
D=R/'bit-six-channel-retention';fresh={}
for n,sub,baseword in [(21,'twenty-one',R/'bit-canonical-history-source/author/output/WORD.json'),(27,'twenty-seven',a.out/'word21/WORD.json')]:
 dest=a.out/f'word{n}';fresh[n]=dest
 run(f'build{n}',D/sub/'build.py','--repo',a.repo,'--base',baseword,'--out',dest)
 assert (dest/'WORD.json').read_bytes()==(D/sub/'output/WORD.json').read_bytes()
more=[]
for n,sub in [(21,'twenty-one'),(27,'twenty-seven')]:
 dest=fresh[n]
 more += [(f'author{n}',D/sub/'check.py','--repo',a.repo,'--out',dest),(f'history{n}',D/sub/'history.py','--repo',a.repo,'--out',dest),(f'independent-c{n}',D/'independent-c/check.py','--repo',a.repo,'--word',dest/'WORD.json','--out',a.out/'independent-c'/str(n)),(f'root{n}',D/'root-review/check.py','--repo',a.repo,'--word',dest/'WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--certificate',D/'independent-c/output'/str(n)/'RESULT.json','--out',a.out/f'root{n}.json')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(lambda x:run(*x),more))
for n,sub in [(21,'twenty-one'),(27,'twenty-seven')]:run(f'price{n}',D/sub/'price.py','--out',fresh[n])
run('independent-c-price',D/'independent-c/price.py','--out',a.out/'independent-c')
(a.out/'REPRODUCTION.json').write_text(json.dumps({'status':'PASS_CP7_REPRODUCTION','commands':done,'byte_identical_rebuilt_words':3,'byte_identical_complex_source_result':True,'new_complete_kappa':False},indent=2)+'\n');print('PASS_CP7_REPRODUCTION',len(done),'commands')
