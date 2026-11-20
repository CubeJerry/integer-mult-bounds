"""Find a disjoint signed-determinant two witness with a small certified rank-distance bill."""
import argparse,json,random
from pathlib import Path
import numpy as np
from check import source,closure,determinant


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--closure',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--trials',type=int,default=320);args=p.parse_args()
    geom=source(args.repo);weights,_=closure(geom,json.loads(args.closure.read_bytes()));g=np.array(geom,dtype=np.int64);w=np.zeros_like(g)
    for (r,c),v in weights.items():w[r,c]=v
    rng=random.Random(230491);best=1000;best_result=None
    for run in range(args.trials):
        while True:
            sample=rng.sample(range(111),20);R=sample[:10];C=sample[10:];d=round(np.linalg.det(g[np.ix_(R,C)]))
            if abs(d)==2:break
        for step in range(120):
            A=g[np.ix_(R,C)];d=round(np.linalg.det(A));cof=np.rint(np.linalg.inv(A).T*d).astype(np.int64)
            if not np.array_equal(A@cof.T,d*np.eye(10,dtype=np.int64)):raise ValueError('exact cofactors')
            cur=int(w[np.ix_(R,C)].sum());allowed=[u for u in range(111) if u not in R and u not in C];moves=[]
            for add in (True,False):
                if add:before=w[np.ix_(R,C)].sum(axis=1);after=w[np.ix_(allowed,C)].sum(axis=1);dets=g[np.ix_(allowed,C)]@cof.T
                else:before=w[np.ix_(R,C)].sum(axis=0);after=w[np.ix_(R,allowed)].sum(axis=0);dets=g[np.ix_(R,allowed)].T@cof
                permitted=np.abs(dets)==2;inc=after[:,None]-before[None,:];best_inc=np.min(inc[permitted],initial=10000)
                for x,pos in zip(*np.where(permitted&(inc==best_inc))):moves.append((int(best_inc),add,int(pos),allowed[int(x)]))
            if cur<best:
                best=cur;exact=determinant([[geom[x][y] for y in C] for x in R]);assert abs(exact)==2
                best_result={'rows':R.copy(),'columns':C.copy(),'determinant':exact,'sum_edge_error_weights':best,'odd_excess_lower_denominator':best+1,'search_run':run,'step':step,'known_nonzero':int(A.sum())}
                args.out.mkdir(parents=True,exist_ok=True);(args.out/'ODD.json').write_text(json.dumps(best_result,sort_keys=True,indent=2)+'\n');print(run,step,best,flush=True)
            mi=min(x[0] for x in moves)
            if mi>0 or (mi==0 and step>28 and rng.random()<0.2):break
            _,add,pos,u=rng.choice([m for m in moves if m[0]==mi]);(R if add else C)[pos]=u
    print(best_result,flush=True)


if __name__=='__main__':main()
