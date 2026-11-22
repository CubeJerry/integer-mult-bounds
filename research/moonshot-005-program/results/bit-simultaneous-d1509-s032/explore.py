"""S032 exact simultaneous D1509 inverse-fibre exploration (not an admission)."""
from pathlib import Path
import importlib.util, gzip, json, itertools, argparse
import numpy as np

def read(p): return json.loads(gzip.decompress(p.read_bytes()))

def load(repo):
 base=repo/'research/moonshot-005-program/results'; old=base/'bit-shared-h-s031-construction/native-d1509-all-native/output'
 spec=importlib.util.spec_from_file_location('s032_geometry',base/'bit-coupled-native-geometric-h-source/component/construction.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 f,a,p=g.context(repo)
 src=read(old/'SOURCES.json.gz');ph=read(old/'H-PHYSICAL.json.gz');dw=read(old/'D-WORD.json.gz')
 return g,a,src,ph,dw

def compute(repo,out):
 g,a,src,ph,dw=load(repo); D=1509
 marked=set(read(repo/'research/moonshot-005-program/results/bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D'])
 prot=list(range(48))+list(range(240,288)); frames={tuple(map(int,k.split('/'))):np.array(v,dtype=np.uint8)for k,v in src['frames'].items()}
 maps={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in vv.items()}for j,vv in src['paired_maps'].items()}
 T=np.array(dw['matrix'],dtype=np.uint8);downers=dw['owners'];rs=[i for i in range(120)if a.charts[D]<=a.adj[i]]
 print('receivers',rs,flush=True)
 result={};proper={};readouts={}
 for j,mmaps in maps.items():
  rows=[]
  for h,F in mmaps.items():
   Q=frames[j,h];z=ph[str(h)];xs=z['X_owners'];ys=z['Y_owners'];E=np.array(z['early'],dtype=np.uint8);B=np.array(z['late'],dtype=np.uint8);G=np.array(z['cross'],dtype=np.uint8).reshape(len(ys),len(xs))
   XE=np.zeros((len(xs),30),dtype=np.uint8);YL=np.zeros((len(ys),30),dtype=np.uint8)
   xx=[q for q,x in enumerate(xs)if x[1]==j];yy=[q for q,x in enumerate(ys)if x[6]==j];assert len(xx)+len(yy)==30
   XE[xx]=Q[:len(xx)];YL[yy]=Q[len(xx):]
   RX=a.mm(a.mm(E,XE),F[:,prot]);RY=a.mm(a.mm(G,XE)^a.mm(B,YL),F[:,prot]) if len(ys) else np.zeros((0,96),dtype=np.uint8)
   for owners,R in [(xs,RX),(ys,RY)]:
    for x,v in zip(owners,R):
     if x[4] in marked:rows.append((h,x,v))
  result[j]={};proper[j]={};readouts[j]={}
  inn=[q for q,x in enumerate(downers)if x[3]is not None and j in a.planes[x[3]]]
  assert len(inn)==8
  for i in rs:
   visible=[(x,v)for h,x,v in rows if a.planes[h]<=a.adj[i] and a.charts[x[4]]<=a.adj[i]]
   A=np.array([v for x,v in visible],dtype=np.uint8);assert A.shape==(96,96) and a.rank(A)==96,(j,i,A.shape,a.rank(A))
   labels=[(x[0],x[1],x[2])for x,v in visible]
   oo=[q for q,x in enumerate(downers)if x[5]is not None and i in a.planes[x[5]]];assert len(oo)==8
   C=T[np.ix_(oo,inn)];Ci=g.inverse(C,a);target=np.zeros((96,8),dtype=np.uint8)
   for q,p in enumerate(inn):
    x=downers[p];target[labels.index((x[0],x[1],x[2]))]=Ci[q]
   U=a.mm(g.inverse(A,a),target);assert a.rank(U)==8 and np.array_equal(a.mm(A,U),target)
   result[j][i]=U.tolist();proper[j][i]={'labels':labels,'matrix':A.tolist(),'target':target.tolist()};readouts[j][i]={'D_inputs':inn,'D_outputs':oo,'section':C.tolist()}
  print('FRAMES',j,len(rs),flush=True)
 out.mkdir(parents=True,exist_ok=True)
 for name,obj in [('FRAMES',result),('PROPER',proper),('READOUTS',readouts)]:
  (out/(name+'.json.gz')).write_bytes(gzip.compress((json.dumps(obj,separators=(',',':'),sort_keys=True)+'\n').encode(),mtime=0))
 print('FRAME_DONE',flush=True)

def census(repo,out):
 g,a,_,_,_=load(repo);frames=read(out/'FRAMES.json.gz');ff={int(j):{int(i):np.array(U,dtype=np.uint8)for i,U in rr.items()}for j,rr in frames.items()};rs=sorted(ff[0]);js=sorted(ff)
 old=[0,45,61,62,100];new=[j for j in js if j not in old]
 records=[]
 for i in rs:
  fixed_equal=all(np.array_equal(ff[0][i],ff[j][i])for j in old)
  span=[a.rank(np.hstack([ff[0][i],ff[j][i]]))for j in old]
  records.append({'receiver':i,'old_five_oriented_equal':fixed_equal,'joins_with0':dict(zip(old,span))})
 print('FIXED_OLD',json.dumps(records),flush=True)
 joint=[]
 for n in range(1,5):
  feasible=[];rank_profiles={}
  for R in itertools.combinations(rs,n):
   V=[np.hstack([ff[j][i]for i in R])for j in js];r=[a.rank(A)for A in V];kernel_equal=all(a.rank(np.vstack([V[0],A]))==r[0]for A in V)and len(set(r))==1
   if kernel_equal: feasible.append(list(R))
   key=','.join(map(str,r));rank_profiles[key]=rank_profiles.get(key,0)+1
  joint.append({'size':n,'joint_kernel_equal_sets':feasible,'joint_kernel_equal_count':len(feasible),'rank_profiles':rank_profiles})
  print('SIZE',n,'FEASIBLE',len(feasible),'RANK_PROFILES',len(rank_profiles),flush=True)
 (out/'CENSUS.json').write_text(json.dumps({'receivers':rs,'donors':js,'fixed_old':records,'joint':joint},indent=2)+'\n')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);p.add_argument('--census',action='store_true');q=p.parse_args();(census if q.census else compute)(q.repo.resolve(),q.out.resolve())
