"""Check actual source validity of protected source/D interpolation changes.

S033, @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse,gzip,importlib.util,json,time
import numpy as np

PROT=list(range(48))+list(range(240,288))
PROWS=[0,1,2,15,16,17]

def read(p):
 return json.loads(gzip.decompress(p.read_bytes())) if p.suffix=='.gz' else json.loads(p.read_text())
def module(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def load(repo,candidate=None):
 base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032'
 ex=module(four/'explore.py','s033_geometry');g,a,*_=ex.load(repo)
 s=read(four/'output/SOURCES.json.gz');e=read(four/'output/EARLY.json.gz')
 cc=read(candidate or base/'bit-source-d-tangent-s032/CERTIFICATE.json.gz')
 if 'candidate'in cc:cc=cc['candidate']
 delta=cc['source_protected_delta'];src={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in mm.items()}for j,mm in s['paired_maps'].items()}
 changed=[]
 # Preserve the literal protected/complement direct-sum partition.
 other_rows=[q for q in range(30)if q not in PROWS];other_cols=[q for q in range(480)if q not in PROT]
 for mm in src.values():
  for F in mm.values():
   if np.any(F[np.ix_(PROWS,other_cols)]) or np.any(F[np.ix_(other_rows,PROT)]):
    raise ValueError('source protected/complement direct-sum partition')
 for key,D in delta.items():
  j,h=map(int,key.split('/'));D=np.array(D,dtype=np.uint8)
  if np.any(D):src[j][h][np.ix_(PROWS,PROT)]^=D;changed.append([j,h])
 return g,a,s,e,src,cc,changed

def run(repo,out,candidate=None,propagation=False):
 g,a,s,e,src,cc,changed=load(repo,candidate);out.mkdir(parents=True,exist_ok=True)
 changed_donors=sorted({j for j,h in changed});result={'changed_quotients':changed,'changed_donors':changed_donors,'source_views':{},'early':{},'propagation':{},'complete_supplier':False,'new_complete_kappa':False}
 views={};inverses={}
 for j in sorted(src):
  hs=sorted(src[j]);maps={h:M[np.ix_(PROWS,PROT)]for h,M in src[j].items()};views[j]={};inverses[j]={};rr=[]
  for r in sorted(a.adj[j]):
   vv=[h for h in hs if a.planes[h]<=a.adj[r]];assert len(vv)==16
   A=np.vstack([maps[h]for h in vv]);rk=a.rank(A);rr.append([int(r),rk]);views[j][r]=vv
   if rk==96:inverses[j][r]=g.inverse(A,a)
  result['source_views'][j]={'views':rr,'all_protected_rank96':all(x[1]==96 for x in rr),'native_views':sum(int(r in a.native)for r,_ in rr)}
  # Actual source early owner matrix: replace precisely the physical rows
  # of Q[j,H] F[j,H] prescribed by the inherited early owner itinerary.
  E=np.array(e[str(j)]['physical_matrix'],dtype=np.uint8)
  for q,(h,owner) in enumerate(e[str(j)]['row_owners']):
   Q=np.array(s['frames'][f'{j}/{h}'],dtype=np.uint8);within=sum(t[0]==h for t in e[str(j)]['row_owners'][:q]);E[owner]=a.mm(Q,src[j][h])[within]
  result['early'][j]={'full_rank':a.rank(E),'shape':list(E.shape)}
  print('SOURCE',j,'views',len(rr),'bad',[x for x in rr if x[1]!=96],'early',result['early'][j]['full_rank'],flush=True)
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 if propagation:
  for j in changed_donors:
   if not result['source_views'][j]['all_protected_rank96']:continue
   records=[];hist={};best=[]
   hs=sorted(src[j])
   for h in hs:
    for k in hs:
     if h==k:continue
     rr=[r for r,vv in views[j].items()if h in vv and k in vv]
     blocks=[inverses[j][r][:,6*views[j][r].index(h):6*views[j][r].index(h)+6]for r in rr]
     P=np.hstack(blocks);rk=a.rank(P);hist[rk]=hist.get(rk,0)+1;records.append([h,k,rk])
     if rk>=90 and len(best)<5:best.append({'source':h,'target':k,'receivers':rr,'rank':rk})
    if h%10==0:print('PROP',j,h,dict(sorted(hist.items())),flush=True)
   result['propagation'][j]={'protected_rank_histogram':hist,'maximum':max(hist),'records':records,'saturation_witnesses':best,'complement_bound':360 if j in [0,45,61,62,100] else 120}
   print('PROP_DONE',j,dict(sorted(hist.items())),flush=True)
   (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);p.add_argument('--candidate',type=Path);p.add_argument('--propagation',action='store_true');q=p.parse_args();run(q.repo.resolve(),q.out.resolve(),q.candidate,q.propagation)
