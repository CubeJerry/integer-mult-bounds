"""Exact fixed-extension source lift for T(t)=T+tE00; default t=26."""
from pathlib import Path
import argparse,importlib.util,json,gzip,numpy as np

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def build(repo,t,out):
 b=mod(Path(__file__).parent/'check.py','bridgecheck');base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032';ex=mod(four/'explore.py','bridgegeometry');g,a,*_=ex.load(repo);z=b.read(base/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');T=np.array(b.read(four/'output/D-WORD.json.gz')['matrix'],dtype=np.uint8);R=z['retained_receivers'];J=z['donors'];I={int(j):x for j,x in z['D_inputs'].items()};O={int(r):x for r,x in z['D_outputs'].items()};T[0,0]^=t;ci={(j,r):g.inverse(T[np.ix_(O[r],I[j])],a)for j in J for r in R};ds={}
 for key,S in z['systems'].items():
  j,h=map(int,key.split('/'));F=np.array(S['old_protected_map'],dtype=np.uint8);X=np.array(S['input_generators'],dtype=np.uint8);C=np.array(S['H_observation_core'],dtype=np.uint8);M=[np.array(M,dtype=np.uint8)for M in S['receiver_ingress_to_quotient_maps']];N=np.array(S['relation_kernel'],dtype=np.uint8);Y=np.hstack([a.mm(F,C)]+[a.mm(M0,ci[j,r])for M0,r in zip(M,R)]);need(not np.any(a.mm(Y,N)),'exact local compatibility');_,cols=g.rref(X,a);B=X[:,cols];_,rows=g.rref(B.T,a);delta=Y^a.mm(F,X);D=np.zeros((6,96),dtype=np.uint8);D[:,rows]=a.mm(delta[:,cols],g.inverse(B[rows],a));need(np.array_equal(a.mm(D,X),delta),'literal fixed extension');ds[key]=D.tolist()
 result={'t':t,'D_matrix':T.tolist(),'source_protected_delta':ds};out.parent.mkdir(parents=True,exist_ok=True);raw=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode();out.write_bytes(gzip.compress(raw,mtime=0)if out.suffix=='.gz'else raw);print('PASS_EXACT_FIXED_SOURCE_D_LIFT',t,len(ds),flush=True);return result

def need(v,msg):
 if not v:raise ValueError(msg)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--parameter',type=int,default=26);p.add_argument('--out',type=Path,required=True);q=p.parse_args();build(q.repo.resolve(),q.parameter,q.out.resolve())
