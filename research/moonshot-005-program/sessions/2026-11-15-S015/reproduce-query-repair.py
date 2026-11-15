#!/usr/bin/env python3
import argparse,json,subprocess,hashlib,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);p=repo/'research/moonshot-005-program/results/bit-chartwise-query-repair';cs=[];ds=[]
for label,args in [('author',[str(p/'author-root/check.py'),'--out',str(out/'author')]),('independent',[str(p/'independent-a/check.py'),'--repo',str(repo),'--source',str(p/'author-root'),'--out',str(out/'independent')])]:
 cmd=[sys.executable,'-B',*args];r=subprocess.run(cmd,capture_output=True,text=True);(out/(label+'.log')).write_text(r.stdout+r.stderr);assert r.returncode==0,(label,r.stderr);cs.append({'label':label,'command':cmd,'exit_code':r.returncode});src=p/('author-root'if label=='author'else'independent-a')/'output/RESULT.json';got=out/label/'RESULT.json';x=src.read_bytes();y=got.read_bytes();assert x==y,label;ds.append({'committed':str(src.relative_to(repo)),'sha256':hashlib.sha256(x).hexdigest(),'comparison':'byte_identical'})
(out/'COMMANDS.json').write_text(json.dumps(cs,indent=2)+'\n');(out/'COMPARISONS.json').write_text(json.dumps(ds,indent=2)+'\n');print(json.dumps({'status':'PASS_QUERY_REPAIR_REPRODUCTION','commands':len(cs),'byte_identical':len(ds)}))
