#!/usr/bin/env python3
"""Independently reconstruct physical chart components and three weighted 9-flag cuts."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from collections import Counter,defaultdict
from decimal import Decimal,localcontext
from functools import cache
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow,connected_components

def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def require(x,m):
    if not x:raise ValueError(m)
def span(b):
    a={0}
    for i in b:a|={v^i for v in a}
    return a

def exact_components(w):
    # Connected components by independent undirected graph. Tokens I[e] and O[f]
    # distinguish one arrival from one form. A second pass supplies only the
    # historical serialized indices used by the delivered array of capacities.
    ids={};tok=[];phys=[]
    def item(q):
        if q not in ids:ids[q]=len(tok);tok.append(q)
        return ids[q]
    for f,terms in w['forms']:
        for e,amount in terms:
            require(F(amount)!=0,'nonzero scalar incidence');phys.append((item((1,f)),item((0,e))))
    n=len(ids);a,b=zip(*phys);M=csr_matrix((np.ones(len(a),np.int8),(a,b)),shape=(n,n))
    count,cl=connected_components(M,directed=False);count=int(count)
    parent=list(range(n))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,j in phys:parent[root(i)]=root(j)
    byclass=defaultdict(set)
    for i in range(n):byclass[cl[i]].add(tok[root(i)])
    require(len(byclass)==count and all(len(s)==1 for s in byclass.values()),'delivered index matches independent components')
    hist={r:k for k,r in enumerate(sorted(next(iter(s))for s in byclass.values()))}
    site={node:hist[next(iter(byclass[cl[i]]))]for node,i in ids.items()}
    chart=defaultdict(set);pins=set();moves={e:(a,b) for e,a,b in w['moves']}
    for (side,e),v in site.items():
        if not side and e<0:pins.add(v);c=w['initial'][~e]
        elif side and e not in moves:pins.add(v);c=w['final'][e-w['first_output']]
        else:c=moves[e][1-side]
        chart[v].add(c)
    require(all(len(c)==1 for c in chart.values()),'physical cochart components')
    frame={v:span(w['frames'][next(iter(c))])for v,c in chart.items()}
    mu=Counter(tuple(sorted((site[1,e],site[0,e])))for e in moves)
    return count,pins,frame,mu

def bitsets(basis,frame):
    F0={0};prior={k:1 for k in frame};bits=[]
    for z in basis:
        n=len(F0);F0|={i^z for i in F0};require(len(F0)==2*n,'independent flag')
        cur={i:len(t&F0)for i,t in frame.items()};require(all(cur[i] in (prior[i],2*prior[i])for i in frame),'flag threshold')
        bits.append({i:cur[i]>prior[i]for i in frame});prior=cur
    return bits

def cuts(n,pinned,bits,weighted):
    vals=[];inc=[]
    for j,labels in enumerate(bits):
        # Contract the two prescribed terminal sides before max-flow, avoiding
        # artificial super-arc weights and preserving exact integral capacities.
        edges=Counter();ones=n;zeros=n+1;inc.append(sum(c[j]for (u,v),c in weighted.items()if labels[u]!=labels[v]))
        def q(i):return (ones if labels[i]else zeros)if i in pinned else i
        for (u,v),c in weighted.items():
            x,y=q(u),q(v)
            if x!=y:
                edges[x,y]+=c[j];edges[y,x]+=c[j]
        pairs=list(edges);vals0=list(edges.values())
        require(max(vals0)<2**31,'independent native max-flow integer capacity')
        mat=csr_matrix((np.array(vals0,np.int64),([i for i,jj in pairs],[jj for i,jj in pairs])),shape=(n+2,n+2))
        res=maximum_flow(mat,ones,zeros,method='dinic');v=int(res.flow_value)
        residual=(mat-res.flow).tocsr()
        seen={ones};stack=[ones]
        while stack:
            node=stack.pop()
            for qpos in range(residual.indptr[node],residual.indptr[node+1]):
                dest=int(residual.indices[qpos])
                if residual.data[qpos]>0 and dest not in seen:seen.add(dest);stack.append(dest)
        require(zeros not in seen and v==sum(c for (x,y),c in edges.items()if x in seen and y not in seen),'explicit independent min cut')
        vals.append(v)
    return vals,inc

def intervals(app,s):
    # Decimal ln and exp are correctly rounded; outward radius dominates all
    # errors by >20 decimal orders on the finite domain checked below.
    def price(k):
        k=int(k)
        if k==1:return Decimal(1),Decimal(1)
        p=(Decimal(k).ln()*s).exp();err=Decimal('1e-65')
        return p-err,p+err
    def moment(h):
        p=[(int(v),price(k))for k,v in h.items()];return (sum(n*a for n,(a,b)in p),sum(n*b for n,(a,b)in p))
    c=app['caller_census'];T=moment(c['fixed_root_targets']);P=moment(c['fixed_caller_paid']);H=moment(app['native']['positive_helper_ranks'])
    return price,H[1]+(T[1]-P[0])/c['calls']

def main():
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--capacities',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    wf=a.sources/'DOUBLE-CANDIDATE.json.gz';af=a.sources/'DOUBLE-APPLICATION.json.gz'
    require(hashlib.sha256(gzip.decompress(wf.read_bytes())).hexdigest()=='7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48','paid word')
    require(hashlib.sha256(gzip.decompress(af.read_bytes())).hexdigest()=='1b2d87e93ae023f5ffd464546af53281b6cb4963dfd76ae4742e0a5540b752fa','caller')
    n,pins,f,edges=exact_components(read(wf));app=read(af);result={'chart_components':n,'pinned':len(pins),'native_paid_events':sum(edges.values()),'component_pairs':len(edges),'tables':{}}
    for name,expected in [('capacities',959119819),('capacities-optimized',959536391),('capacities-best',959881296)]:
        d=read(a.capacities/(name+'.json.gz'));scale=d['scale'];wt={tuple(sorted((u,v))):c for u,v,c in d['edges']}
        require(set(wt)==set(edges)and len(wt)==len(d['edges']),'every actual pair once')
        for pair,fees in wt.items():
            require(len(fees)==9 and min(fees)>=0,'capacity domain');total=0;mult=edges[pair]
            for k,m in enumerate(sorted(fees,reverse=True),1):
                total+=m;require(total**200<=(scale*mult)**200*k**199,'integer-power majorization')
        b=bitsets(d['basis'],f);flow,inc=cuts(n,pins,b,wt);require(sum(flow)==expected,'actual price bound')
        unit,bill=cuts(n,pins,b,{e:[m]*9 for e,m in edges.items()});require(unit==bill and sum(unit)==9646,'linear native volume')
        result['tables'][name]={'basis':d['basis'],'flow':flow,'scale':scale,'native_moment':str(F(sum(flow),scale)),'unit_flows':unit}
    with localcontext()as ctx:
        ctx.prec=96
        s0=Decimal(199)/200;p0,allow=intervals(app,s0)
        result['native_allowance_at_one_over_200_upper']=str(allow);require(Decimal('9591.19819')>allow,'strict target')
        for e,M,s,lam in [('optimized','9595.36391','0.99544','0.087559'),('best','9598.81296','0.995608','0.121014')]:
            pp,limit=intervals(app,Decimal(s));x=Decimal(lam)
            for j in range(1,10):
                require(pp(j)[0]>=(1-x)*p0(j)[1]+x*j,'per-grade two-exponent interpolation')
            lower=(1-x)*Decimal(M)+x*9646;require(lower>limit,'full caller interpolated')
            result[e+'_trial']={'exponent':s,'native_lower':str(lower),'caller_upper':str(limit),'strict_gap_lower':str(lower-limit)}
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
if __name__=='__main__':main()
