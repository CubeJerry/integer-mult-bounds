"""Rebuild higher-source words and reproduce independent symbolic/source reviews."""
from pathlib import Path
import argparse,concurrent.futures,json,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.repo=a.repo.resolve();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=True)
R=a.repo/'research/moonshot-005-program/results';H=R/'bit-higher-chart-source';D=R/'bit-higher-source-delivery';B=R/'bit-private-bank-reduction';base=R/'bit-three-cell-retention/author/output/WORD.json';old27=R/'bit-six-channel-retention/twenty-seven/output/WORD.json';done=[]
def run(name,path,*args):
 cmd=[sys.executable,'-B',str(path)]+list(map(str,args));r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(a.out/(name+'.log')).write_text(r.stdout);done.append({'name':name,'command':cmd,'returncode':r.returncode})
 if r.returncode:raise RuntimeError(name+':'+r.stdout[-2500:])
rows=[('private',H/'higher-chart-affine',base),('expanded',H/'higher-chart-expanded',base),('32',D/'thirty-two',a.out/'expanded/WORD.json'),('34',D/'thirty-four',a.out/'32/WORD.json')]
for n,src,old in rows:
 run('build'+n,src/'build.py','--base',old,'--out',a.out/n)
 assert(a.out/n/'WORD.json').read_bytes()==(src/'output/WORD.json').read_bytes()
tasks=[]
for n,src,old in rows:tasks.append(('author'+n,src/'check.py','--repo',a.repo,'--base',old,'--out',a.out/n))
for n,sub in [('private','independent-private'),('expanded','independent-expanded')]:tasks.append(('independent'+n,H/sub/'check.py','--repo',a.repo,'--base',base,'--word',a.out/n/'WORD.json','--out',a.out/('independent-'+n)))
for n in ['32','34']:tasks.append(('independent'+n,D/'independent-c/check.py','--repo',a.repo,'--base',a.out/'expanded/WORD.json','--word',a.out/n/'WORD.json','--out',a.out/('independent-'+n)))
tasks += [('private-bank-author',B/'author/check.py','--repo',a.repo,'--word',old27,'--out',a.out/'bank-author'),('private-bank-independent',B/'independent-b/check_independent.py','--repo',a.repo,'--base-word',old27,'--author-result',B/'author/output/RESULT.json','--thirty-word',base,'--affine-word',a.out/'private/WORD.json','--out',a.out/'bank-independent')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(lambda x:run(*x),tasks))
for n,src,old in rows:run('price'+n,src/'price.py','--out',a.out/n)
for n,sub in [('32','thirty-two'),('34','thirty-four')]:run('root'+n,D/'root-review/check.py','--repo',a.repo,'--word',a.out/n/'WORD.json','--engine',R/'bit-shared-meet-funnel/root-review','--certificate',D/sub/'output/RESULT.json','--out',a.out/('root'+n+'.json'))
BC=R/'bit-bank-compression'
run('compression-author',BC/'author/check.py','--repo',a.repo,'--word',old27,'--envelope-result',B/'author/output/RESULT.json','--out',a.out/'compression-author')
run('compression-root',BC/'root-review/check.py','--repo',a.repo,'--word',old27,'--envelope',B/'author/output/RESULT.json','--certificate',BC/'author/output/RESULT.json','--out',a.out/'compression-root.json')
(a.out/'REPRODUCTION.json').write_text(json.dumps({'status':'PASS_CP9_REPRODUCTION','commands':done,'byte_identical_rebuilt_words':4,'new_complete_kappa':False},indent=2)+'\n');print('PASS_CP9_REPRODUCTION',len(done),'commands')
