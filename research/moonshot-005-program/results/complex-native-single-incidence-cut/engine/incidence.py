"""Remove each individual supplied cochart equality and price the remaining paid slots."""
import argparse,gzip,json,sys,hashlib
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

def need(q,m):
    if not q:raise ValueError(m)

def read(f):return json.loads(gzip.decompress(f.read_bytes()))

def structure(w,model):
    ids={};tokens=[];parent=[];adj=[];terms=[]
    def vertex(tok):
        if tok not in ids:
            ids[tok]=len(tokens);tokens.append(tok);parent.append(len(parent));adj.append([])
        return ids[tok]
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for f,form in w['forms']:
        u=vertex((1,f))
        for e,coef in form:
            need(str(coef)!='0','ordinary incidence');v=vertex((0,e));j=len(terms);terms.append((f,e));adj[v].append((u,j));adj[u].append((v,j));parent[root(u)]=root(v)
    keys=sorted({tokens[root(i)] for i in range(len(tokens))});idx={r:j for j,r in enumerate(keys)};comp=[idx[tokens[root(i)]]for i in range(len(tokens))]
    groups=defaultdict(set);pins=defaultdict(set);routes={e:(a,b)for e,a,b in w['moves']};edgeids=list(routes)
    endpoints=[[ids[1,e],ids[0,e]] for e in edgeids];paidtokens={q for ends in endpoints for q in ends}
    for i,(role,e)in enumerate(tokens):
        groups[comp[i]].add(i)
        if not role and e<0 or role and e not in routes:pins[comp[i]].add(i)
    need(all(tuple(comp[x]for x in ab)==model.edges[e] for e,ab in zip(edgeids,endpoints)),'historical component indexing')
    order=[];discover=[-1]*len(tokens);low=discover.copy();leave=discover.copy();bridges=[];sys.setrecursionlimit(50000)
    def dfs(v,previous):
        discover[v]=low[v]=len(order);order.append(v)
        for to,j in adj[v]:
            if j==previous:continue
            if discover[to]<0:
                dfs(to,j);low[v]=min(low[to],low[v])
                if low[to]>discover[v]:bridges.append((j,to))
            else:low[v]=min(low[v],discover[to])
        leave[v]=len(order)
    for i in range(len(tokens)):
        if discover[i]<0:dfs(i,-1)
    trivial=Counter();hard=[]
    for j,v in bridges:
        c=comp[v];one=set(order[discover[v]:leave[v]]);two=groups[c]-one
        k,l=bool(one&pins[c]),bool(two&pins[c])
        if k and l:trivial['both_sides_pinned']+=1;continue
        if k or (not l and len(two&paidtokens)<len(one&paidtokens)):one=two
        n=len(one&paidtokens)
        if n<=1:trivial['detached_paid_'+str(n)]+=1;continue
        need(not one&pins[c],'detached side free');hard.append((terms[j],c,one))
    return terms,bridges,trivial,hard,comp,endpoints

def capacity(src,name,m,bitsfn,endpoints,comp):
    d=read(src/'author'/(name+'.json.gz'));scale=d['scale'];weights={tuple(sorted((u,v))):c for u,v,c in d['edges']};mu=Counter(tuple(sorted((comp[x],comp[y]))) for x,y in endpoints);rows=[]
    for x,y in endpoints:
        e=tuple(sorted((comp[x],comp[y])));fees=tuple(c//mu[e] for c in weights[e]);rows.append(fees)
    for fees in set(rows):
        total=0
        for k,x in enumerate(sorted(fees,reverse=True),1):
            total+=x;need(total**200<=scale**200*k**199,'single-slot majorization')
    b=bitsfn(m,d['basis']);return scale,rows,np.array([[v[i]for i in range(len(m.site))]for v in b],dtype=bool)

def aftersplit(detached,comp,ends,model,fee,bits):
    n=len(model.site);end=np.array([[(n if x in detached else comp[x]) for x in e]for e in ends],dtype=np.int64);pin=np.array(sorted(model.pinned));rows=np.array(fee,dtype=np.int64);values=[]
    for col,bit in enumerate(bits):
        labels=np.arange(n+1);labels[pin]=np.where(bit[pin],n+1,n+2);xy=labels[end];u,v=xy.T;keep=u!=v;u=u[keep];v=v[keep];q=rows[keep,col]
        graph=csr_matrix((np.r_[q,q],(np.r_[u,v],np.r_[v,u])),shape=(n+3,n+3));need(max(graph.data,default=0)<2**31,'scipy exact capacities')
        values.append(int(maximum_flow(graph,n+1,n+2).flow_value))
    return values

def main():
    p=argparse.ArgumentParser();p.add_argument('--chart',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();src=a.chart.resolve();sys.path.insert(0,str(src/'author'));from check import Model,WORD;from flag import flag_bits
    file=src/'sources/DOUBLE-CANDIDATE.json.gz';need(hashlib.sha256(gzip.decompress(file.read_bytes())).hexdigest()==WORD,'actual scalar rows');w=read(file);m=Model(w)
    terms,bridges,trivial,hard,comp,endpoints=structure(w,m);print('ordinary',len(terms),'bridges',len(bridges),'simple',dict(trivial),'hard',len(hard),flush=True)
    datasets={name:capacity(src,name,m,flag_bits,endpoints,comp)for name in ['capacities-best','capacities-optimized']};scales={r[0]for r in datasets.values()};need(scales=={100000},'published integer scale')
    out=[];bound=958742450
    for num,(edge,c,sub)in enumerate(hard):
        tests={}
        for name,(scale,fee,bits) in datasets.items():
            q=aftersplit(sub,comp,endpoints,m,fee,bits);tests[name]={'nine_flows':q,'total':sum(q)}
            if sum(q)>bound:break
        out.append({'incidence':edge,'tables':tests})
        if num%50==0:print('tested',num,'minimum',min(max(v['total']for v in t['tables'].values())for t in out),flush=True)
    simple=959881296-9*100000;res={'status':'PASS_SINGLE_ORDINARY_INCIDENCE_CUT','physical_ordinary_incidences':len(terms),'zero_effect_nonbridges':len(terms)-len(bridges),'bridges':len(bridges),'structural':dict(trivial),'hard_replays':len(hard),'target_native_upper_numerator_rounded_up':bound,'scale':100000,'one_free_paid_endpoint_lipschitz_floor':simple,'minimum_certified_numerator':min([simple]+[max(v['total']for v in t['tables'].values())for t in out]),'rows':out}
    need(res['minimum_certified_numerator']>bound,'one incidence target remains unaffordable');a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');print(res['minimum_certified_numerator'],len(hard),flush=True)
if __name__=='__main__':main()
