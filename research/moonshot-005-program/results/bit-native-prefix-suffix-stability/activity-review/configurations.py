"""True D pairwise star families, with weights depending on both native D cardinalities."""
import argparse,collections,gzip,hashlib,json
from pathlib import Path
def families(D,opp,j,bad):
    exc={i for i,q in bad if q==j};ds=[d for d in range(3150)if j in D[d]];ty=[(len(D[d]),len(opp[d]))for d in ds]
    n=len(ds);mask=[sum(1<<i for i in opp[d]-exc)for d in ds];nb=[0]*n
    for u in range(n):
        for v in range(u+1,n):
            if not mask[u]&mask[v]:nb[u]|=1<<v
    types=set()
    def dfs(cand,had):
        if not cand:types.add(tuple(sorted(had)));return
        while cand:
            b=cand&-cand;u=b.bit_length()-1;cand^=b;dfs(cand&nb[u],had+[ty[u]])
    dfs((1<<n)-1,[]);return types
def main(a):
    raw=gzip.decompress((a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72';L=json.loads(raw)
    D=[set(x)&set(range(111))for x in L['D4']];opp=[D[d]for d in L['dual_D4']];bad={(7,80),(10,81),(80,96),(81,95)};bad|={(j,i)for i,j in bad}
    fam=[families(D,opp,j,bad)for j in range(111)]
    ix={(j,ss):q for q,(j,ss)in enumerate((j,ss) for j in range(111)for ss in sorted(set(x for f in fam[j]for x in f)))};N=len(ix);globalc=[]
    for d,dd in enumerate(D):
        ss=(len(dd),len(opp[d]));globalc.append([ix[j,ss]for j in dd]+[ix[i,ss[::-1]]for i in opp[d]])
    if a.verify:
        doc=json.loads(a.verify.read_text());names={(j,tuple(ss)):v for j,ss,v in doc['nonzero_integer_prices']};z=[names.get(t,0)for t in ix]
        assert all(type(y)is int and y>=0 for y in z)and set(names)<=ix.keys()
    else:
        import numpy as np
        from scipy.sparse import coo_matrix
        from scipy.optimize import linprog
        row=[];col=[];val=[];rhs=[]
        def equation(terms,hi):
            row.extend([len(rhs)]*len(terms));col.extend(terms);val.extend(terms.values());rhs.append(hi)
        for cs in globalc:equation({q:-1 for q in cs},-1)
        for j,fs in enumerate(fam):
            for f in fs:
                c=dict(collections.Counter(ix[j,t]for t in f));c[N+j]=-1;equation(c,0)
        mat=coo_matrix((val,(row,col)),shape=(len(rhs),N+111)).tocsr();c=np.concatenate([np.zeros(N),2*np.ones(111)])
        hit=linprog(c,A_ub=mat,b_ub=rhs,bounds=(0,None),method='highs');assert hit.success;print('floating',hit.fun,flush=True)
        z=list(map(int,np.rint(hit.x[:N]*1000000)))
    local=[max(sum(z[ix[j,t]]for t in f)for f in fs)for j,fs in enumerate(fam)];budget=2*sum(local);low=min(sum(z[t]for t in cs)for cs in globalc);bound=budget//low
    record={'minimum_D_weight':low,'total_allowed_weight':budget,'max_dead_D':bound,'minimum_active_D':3150-bound,'nonzero_integer_prices':[[j,list(t),z[i]]for(j,t),i in ix.items()if z[i]],'local_maximum_weight':local}
    if a.verify:assert record==doc
    a.out.write_text(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n');print('exact',budget,low,bound,3150-bound,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--verify',type=Path);main(p.parse_args())
