#!/usr/bin/env python3
"""Regenerate all large assets from the original 111 native donors and fixed RNG seeds."""
import argparse,hashlib,importlib.util,json,os,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--cache',type=Path,help='retained working directory; skips already source-regenerated intermediate large matrices');a=p.parse_args()
home=Path(__file__).resolve().parent;repo=a.repo.resolve();base=repo/'research/moonshot-005-program/results';out=a.out.resolve();out.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(home));from verify import Ops,digest
sys.path.insert(0,str(home/'author'));from native import replay
manifest=json.loads((home/'author/sources/MANIFEST.json').read_bytes())
def emit(name,**kw):
    assert {k:digest(v)for k,v in kw.items()}==manifest[name],name
    np.savez_compressed(out/(name+'.npz'),**kw)
with tempfile.TemporaryDirectory(prefix='two-native-source-')as td:
    f=a.cache.resolve()if a.cache else Path(td);f.mkdir(parents=True,exist_ok=True);op=Ops(f,base)
    from transfer import Atlas
    k=base/'bit-gf64-actual-k-atlas/author/output';d=base/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz';at=Atlas(repo,k,d,f/'mul.so')
    if not (f/'S5.npz').is_file():
        rr={};eligible={t for ch in at.kr.values()for _,ins,outs in ch['stripes'] if len(ins)==36 for t in outs}
        for i in range(6):
            e,E,y,Y=at.facet(i);ii=[j for j,t in enumerate(e)if t in eligible];jj=[j for j,t in enumerate(y)if t in eligible];rr['e'+str(i)]=[e[j]for j in ii];rr['y'+str(i)]=[y[j]for j in jj];rr['fold'+str(i)]=np.hstack((E[96:,ii],Y[96:,jj]))
        replay(repo,base,f,at,rr,True);np.savez_compressed(f/'K.npz',K=rr['K'])
        for i in range(6):np.savez_compressed(f/f'S{i}.npz',**{t:rr[t+str(i)]for t in ('e','y','fold','sens')})
    K=np.load(f/'K.npz')['K']
    for i in range(8):emit(f'anchor-{i}',K=K[i*384:(i+1)*384])
    for i in range(6):
        z=np.load(f/f'S{i}.npz');emit(f'observer-{i}',**{k:z[k]for k in z.files})
    four=base/'bit-native-low-rank-facet-retuning'
    if not (four/'verify.py').is_file():four=home.parent/four.name
    py=[sys.executable,'-I','-B'];subprocess.run([*py,str(four/'verify.py'),'--repo',str(repo),'--out',str(f/'four'),'--emit-gauges'],check=True)
    w=np.load(f/'four/LARGE-GAUGES.npz')
    np.savez_compressed(f/'old.npz',actual=w['Winv'])
    for i in range(4):emit(f'old-gauge-{i}',W=w['W'][i],Winv=w['Winv'][i])
    env=dict(os.environ,FE_DIR=str(f),FE_REPO=str(repo))
    for name in ('solver','protect'):subprocess.run([*py,str(home/'author'/(name+'.py')),'--h','307'],env=env,check=True)
    q=np.load(f/'NEW-307.npz')
    for i in range(6):emit(f'changed-{i}',U=q['acts'][i],phi=q['phi'+str(i)])
(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('Verified all 24 regenerated asset hashes')
