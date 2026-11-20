from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from algebra import *
p=argparse.ArgumentParser();p.add_argument('--h',type=int,default=64);p.add_argument('--size',type=int,default=6);ar=p.parse_args();h=ar.h;rng=np.random.default_rng(1868)
for I in itertools.combinations(range(6),ar.size):
 ellbase=kernel(np.hstack([nulls[i]for i in I]).T).T
 if len(ellbase)>=h:break
else:print('insufficient shared dual',len(ellbase),flush=True);sys.exit(1)
print('choice',I,'sensor-null',[u.shape[1]for u in nulls],'common dual',len(ellbase),'h',h,flush=True)
ell=mm(rng.integers(0,64,(h,len(ellbase)),dtype=np.uint8),ellbase);assert rank(ell)==h
transform=[];features=[]
for i in I:
 free=kernel(np.hstack([H[i].T,ell.T]));nz=free[-h:];assert rank(nz)==h
 cols=[];rank0=0
 for j in range(nz.shape[1]):
  test=rank(nz[:,cols+[j]])
  if test>rank0:cols.append(j);rank0=test
  if test==h:break
 ph=mm(free[:-h,cols],inverse(nz[:,cols])).T;assert np.array_equal(mm(ph,H[i]),ell)
 transform.append(ph);features.append(mm(ph,S[i]))
coeff=[];outside=set(ids)-set(I);zero=np.zeros((d,n),np.uint8)
for i in outside:
 g=K0[i*d:(i+1)*d];coeff.extend([np.hstack([g,zero]),np.hstack([zero,g])])
scales=rng.choice(np.arange(1,64),size=len(I),replace=False);print('scales',scales,flush=True)
for t,i in enumerate(I):
 g=K0[i*d:(i+1)*d];coeff.extend([np.hstack([TABLE[scales[t],g],g]),np.hstack([TABLE[scales[t],features[t]],features[t]])])
constraints=np.vstack(coeff);solutions=kernel(constraints);assert solutions.shape[1]>0;print('search space',solutions.shape,flush=True)
first=solutions[:n];second=solutions[n:];forms=[mm(x,first)for x in features];outputs=[mm(K0[i*d:(i+1)*d],first)for i in I];rr=[rank(x)for x in forms];print('feature ranks',rr,'output ranks',[rank(x) for x in outputs],flush=True)
if min(rr)<h:sys.exit(1)
np.savez_compressed(folder/f'DESIGN-{h}.npz',I=I,ell=ell,features=np.stack(features),first=first,second=second,scales=scales,forms=np.stack(forms),outputs=np.stack(outputs),**{f'phi{i}':v for i,v in zip(I,transform)})
