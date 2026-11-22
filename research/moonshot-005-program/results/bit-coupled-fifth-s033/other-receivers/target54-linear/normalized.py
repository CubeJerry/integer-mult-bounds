"""Normalized independent receiver relaxation; common variable kernels need not be fixed."""
from solve import *
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);args=p.parse_args();repo=args.repo.resolve();b=repo/BASE
for q,h in read(HERE/'NORMALIZED-SOURCE-PINS.json').items():need(hashlib.sha256((repo/q).read_bytes()).hexdigest()==h,'source pin '+q)
here=HERE;z=read(b/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');old=np.array(read(b/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz')['matrix'],dtype=np.uint8);O={int(k):v for k,v in z['D_outputs'].items()};I={int(k):v for k,v in z['D_inputs'].items()};eq=read(here/'output/LINEAR-EQUATIONS.json.gz')['donors'];free=[(q,p)for q in range(8)for p in range(35)if p not in[4,5,7,8]];fi={qp:k for k,qp in enumerate(free)};answer=[]
for r in[9,48]:
 equations=[];rhs=[]
 for x in eq:
  if not x['separate_isolation_necessary']:continue
  j=x['donor'];y=next(y for y in x['blocks']if y['receiver']==r);A=np.array(y['ann_W'],dtype=np.uint8);V=np.array(y['old_input_kernel'],dtype=np.uint8);C=mm(mm(A,old[np.ix_(O[r],I[j])]),V);E=np.zeros((12,len(free)),dtype=np.uint8)
  for a in range(6):
   for k in range(2):
    for q in range(8):
     for p,col in enumerate(I[j]):
      if(q,col)in fi:E[2*a+k,fi[q,col]]^=P[A[a,q],V[p,k]]
  equations.append(E);rhs.append(C.reshape(-1))
 A=np.vstack(equations);bb=np.hstack(rhs)[:,None];rk=rank(A);ra=rank(np.hstack([A,bb]));print('RECEIVER',r,'rank',rk,ra,'free',len(free),flush=True);xp=solve(A,bb)[:,0];K=null(A);T0=old[O[r]].copy();rows,cols=np.array(free).T;T0[rows,cols]^=xp;V=np.zeros((K.shape[1],8,8),dtype=np.uint8);cmap={p:i for i,p in enumerate(I[0])}
 for t,(q,p)in enumerate(free):
  if p in cmap:V[:,q,cmap[p]]=K[t]
 N=null(np.vstack([T0[:,I[0]],V.reshape(-1,8)]));print('NULL',N.tolist(),flush=True);answer.append({'receiver':r,'free_entries':free,'equations':A.tolist(),'rhs':bb.tolist(),'rank':rk,'affine_dimension':len(free)-rk,'particular':xp.tolist(),'homogeneous_kernel':K.tolist(),'donor0_universal_kernel':N.tolist()})
args.out.mkdir(parents=True,exist_ok=True);save(args.out/'NORMALIZED-RELAXATION.json.gz',answer)
