"""Explicit t=1 source collisions and mutation rejection controls."""
from pathlib import Path
import argparse,importlib.util,json,gzip,numpy as np

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def run(repo,out):
 here=Path(__file__).parent;b=mod(here/'check.py','bridgecontrol');g,a,s,e,src,c,changed=b.load(repo);w=[]
 for j,r in [(0,111),(32,6),(35,12),(35,108)]:
  hs=[h for h in sorted(src[j])if a.planes[h]<=a.adj[r]];A=np.vstack([src[j][h][np.ix_(b.PROWS,b.PROT)]for h in hs]);RR,piv=g.rref(A,a);free=[q for q in range(96)if q not in piv];need(len(free)==1,'rank95 source witness');v=np.zeros((96,1),dtype=np.uint8);v[free[0]]=1
  for q,p in enumerate(piv):v[p]=RR[q,free[0]]
  vv=np.zeros((480,1),dtype=np.uint8);vv[b.PROT]=v;need(not np.any(a.mm(A,v))and all(not np.any(a.mm(src[j][h],vv))for h in hs),'full480 source collision');w.append({'donor':j,'receiver':r,'source_planes':hs,'protected_rank':95,'protected_collision':v[:,0].tolist(),'full_source_rank':479})
 base=repo/'research/moonshot-005-program/results';z=b.read(base/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');X=np.array(z['systems']['0/263']['input_generators'],dtype=np.uint8);entry=np.argwhere(X!=0)[0];d=np.zeros((6,96),dtype=np.uint8);d[0,entry[0]]=1;need(np.any(a.mm(d,X)),'corrupted interpolation image rejected')
 out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_EXPLICIT_T1_SOURCE_COLLISIONS_AND_CONTROLS','t1_full_rank_failures':w,'corrupted_local_image_rejected':True,'new_complete_kappa':False};(out/'CONTROLS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],len(w),flush=True)

def need(v,msg):
 if not v:raise ValueError(msg)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);q=p.parse_args();run(q.repo.resolve(),q.out.resolve())
