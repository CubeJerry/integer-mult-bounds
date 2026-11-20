"""Exact min-sum elimination on the true P104 fixed-incidence subspace constraints."""
from collections import Counter, defaultdict
from functools import cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse,gzip,json

WORD='7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48'
ZERO=1
FULL=(1<<512)-1
BITS=144
UNIT=1<<BITS
PROFILE={r:1<<((r-1)*16)for r in range(1,10)}|{0:0}

def need(q,msg):
    if not q:raise ValueError(msg)

def dim(H):return H.bit_count().bit_length()-1

def extend(H,x):
    old=H;coset=0
    while old:
        p=old&-old;old-=p;coset|=1<<((p.bit_length()-1)^x)
    return H|coset

@cache
def hull(U,V):
    if U&V in (U,V):return U|V
    H=U;added=V&~U
    while added:
        H=extend(H,(added&-added).bit_length()-1);added=V&~H
    return H

@cache
def domains(lo,hi):
    seen={lo};pending=[lo]
    while pending:
        H=pending.pop();rest=hi&~H
        while rest:
            x=(rest&-rest).bit_length()-1;K=extend(H,x)
            if K not in seen:seen.add(K);pending.append(K)
            rest&=~K
    return tuple(sorted(seen))

def power(r):
    a=r**199*UNIT**200;y=1<<((a.bit_length()+199)//200)
    while True:
        z=(199*y+a//y**199)//200
        if z>=y:break
        y=z
    need(y**200<=a<(y+1)**200,'integer-root enclosure');return y,y+(y**200<a)

PRICE={r:power(r)for r in range(1,10)}

@cache
def bounds(profile):
    lo=hi=0
    for r,(l,h)in PRICE.items():
        c=(profile>>((r-1)*16))&65535;lo+=l*c;hi+=h*c
    return lo,hi

def cheaper(a,b):
    if b is None:return True
    if a==b:return False
    al,ah=bounds(a);bl,bh=bounds(b)
    if ah<bl:return True
    if bh<al:return False
    raise ValueError('distinct histograms not separated at the certified precision')

def decode(H):return {r:(H>>((r-1)*16))&65535 for r in range(1,10)if (H>>((r-1)*16))&65535}

class Model:
    def __init__(self,word):
        moves={e:(a,b)for e,a,b in word['moves']};first=word['first_output'];self.frames=[]
        for F in word['frames']:
            H=ZERO
            for x in F:H=extend(H,x)
            need(dim(H)==len(F),'independent atlas basis');self.frames.append(H)
        parent={}
        def root(x):
            if x not in parent:parent[x]=x
            while parent[x]!=x:
                parent[x]=parent[parent[x]];x=parent[x]
            return x
        for f,row in word['forms']:
            for e,q in row:parent[root((1,f))]=root((0,e))
        groups=defaultdict(list)
        for token in parent:groups[root(token)].append(token)
        lookup={k:i for i,k in enumerate(sorted(groups))};self.site={};self.pinned=set()
        for key,tokens in groups.items():
            v=lookup[key];sites=set()
            for role,e in tokens:
                if role==0 and e<0:sites.add(word['initial'][~e]);self.pinned.add(v)
                elif role==1 and e not in moves:sites.add(word['final'][e-first]);self.pinned.add(v)
                else:sites.add(moves[e][1-role])
            need(len(sites)==1,'old chart equality');self.site[v]=self.frames[sites.pop()]
        self.edges={e:(lookup[root((1,e))],lookup[root((0,e))])for e in moves};self.preds={v:set()for v in self.site};self.succs={v:set()for v in self.site};self.multiplicity=Counter();self.cost=0
        for u,v in self.edges.values():
            if dim(self.site[u])>dim(self.site[v]):u,v=v,u
            need(self.site[u]&self.site[v]==self.site[u] and self.site[u]!=self.site[v],'positive initial inclusion')
            self.preds[v].add(u);self.succs[u].add(v);self.multiplicity[u,v]+=1;self.cost+=PROFILE[dim(self.site[v])-dim(self.site[u])]
        self.order=sorted(self.site,key=lambda v:dim(self.site[v]))

    def intervals(self,pred,succ,order):
        low={v:self.site[v]if v in self.pinned else ZERO for v in self.site}
        high={v:self.site[v]if v in self.pinned else FULL for v in self.site}
        for v in order:
            for u in pred[v]:low[v]=hull(low[v],low[u])
        for v in reversed(order):
            for w in succ[v]:high[v]&=high[w]
        return low,high

    def reversals(self):
        low,high=self.intervals(self.preds,self.succs,self.order);desc={v:1<<v for v in self.site};kept=[];stats=Counter()
        for u in reversed(self.order):
            for v in self.succs[u]:desc[u]|=desc[v]
        for u,v in self.multiplicity:
            if any(desc[w]&(1<<v)for w in self.succs[u]-{v}):stats['alternate_path']+=1;continue
            lo=self.site[v]if v in self.pinned else ZERO
            for w in self.preds[v]-{u}:lo=hull(lo,low[w])
            hi=self.site[u]if u in self.pinned else FULL
            for w in self.succs[u]-{v}:hi&=high[w]
            if lo&hi!=lo or lo==hi:stats['fixed_bounds_prevent_strict_reversal']+=1;continue
            kept.append((u,v));stats['potential_strict']+=1
        return sorted(kept),stats

    def solve(self,reversal=None):
        pred={v:p.copy()for v,p in self.preds.items()};succ={v:s.copy()for v,s in self.succs.items()};pairs=self.multiplicity.copy()
        changes=() if reversal is None else (reversal,) if isinstance(reversal[0],int) else reversal
        for u,v in changes:
            pred[v].remove(u);succ[u].remove(v);pred[u].add(v);succ[v].add(u);pairs[v,u]=pairs.pop((u,v))
        deg={v:len(ps)for v,ps in pred.items()};ready=[v for v,k in deg.items()if not k];order=[]
        while ready:
            u=ready.pop();order.append(u)
            for v in succ[u]:
                deg[v]-=1
                if not deg[v]:ready.append(v)
        if len(order)!=len(self.site):return None
        low,high=self.intervals(pred,succ,order)
        if any(low[v]&high[v]!=low[v]for v in order):return None
        dom={v:domains(low[v],high[v])for v in order};free={v for v in order if len(dom[v])>1};graph={v:set()for v in free};unary={v:[0]*len(dom[v])for v in free};factors=[];cost=0
        for (u,v),multiplicity in pairs.items():
            if u in free and v in free:
                graph[u].add(v);graph[v].add(u)
                factors.append(((u,v),{(i,j):multiplicity*PROFILE[dim(y)-dim(x)]for i,x in enumerate(dom[u])for j,y in enumerate(dom[v])if x&y==x}));continue
            if u not in free and v not in free:cost+=multiplicity*PROFILE[dim(dom[v][0])-dim(dom[u][0])];continue
            active=u if u in free else v
            for i,z in enumerate(dom[active]):
                x=z if active==u else dom[u][0];y=z if active==v else dom[v][0];need(x&y==x,'fixed neighbor bound');unary[active][i]+=multiplicity*PROFILE[dim(y)-dim(x)]
        for v,values in unary.items():factors.append(((v,),{(i,):x for i,x in enumerate(values)}))
        back=[];width=table=0
        while graph:
            v=min(graph,key=lambda x:(sum(len(graph[x]-graph[y]-{y})for y in graph[x]),len(graph[x]),x));nb=graph.pop(v);width=max(width,len(nb));scope=tuple(sorted(nb));ind={x:i for i,x in enumerate((v,)+scope)}
            for x in nb:graph[x]|=nb-{x};graph[x].remove(v)
            selected=[];remaining=[]
            for old,F in factors:
                if v in old:selected.append((tuple(ind[x]for x in old),F))
                else:remaining.append((old,F))
            factors=remaining;out={};choice={}
            for q in product(*(range(len(dom[x]))for x in scope)):
                best=None
                for i in range(len(dom[v])):
                    key=(i,)+q;total=0
                    for ids,F in selected:
                        part=F.get(tuple(key[j]for j in ids))
                        if part is None:break
                        total+=part
                    else:
                        if cheaper(total,best):best=total;choice[q]=i
                if best is not None:out[q]=best
            if not out:return None
            back.append((v,scope,choice));table=max(table,len(out))
            if scope:factors.append((scope,out))
            else:cost+=out[()]
        chosen={}
        for v,scope,C in reversed(back):chosen[v]=C[tuple(chosen[t]for t in scope)]
        labels={v:dom[v][chosen.get(v,0)]for v in order};recheck=0
        for (u,v),mult in pairs.items():
            x,y=labels[u],labels[v];need(x&y==x,'decoded solution inclusion');recheck+=mult*PROFILE[dim(y)-dim(x)]
        need(recheck==cost,'decoded cost')
        return cost,labels,width,table,Counter(len(d)for d in dom.values())

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();raw=gzip.decompress(args.source.read_bytes());need(sha256(raw).hexdigest()==WORD,'upstream word');data=json.loads(raw);model=Model(data);flips,stats=model.reversals();old=model.cost;rows=[];maxw=maxt=0
    for edge in [None,*flips]:
        r=model.solve(edge)
        if r is None:rows.append({'reversed':edge,'feasible':False});continue
        value,labels,w,tab,ds=r;need(not cheaper(value,old),'a cheaper fixed-incidence source');maxw=max(maxw,w);maxt=max(maxt,tab)
        rows.append({'reversed':edge,'feasible':True,'same_optimal_histogram':old==value,'histogram':decode(value),'tree_width':w,'table_size':tab})
        if edge is None:
            need(value==old and sum(len(D)for D in model.succs.values())==len(model.multiplicity),'incumbent and relation count');alternative={v:hex(z)for v,z in labels.items()if model.site[v]!=z};base_domains=dict(ds)
    result={'status':'PASS_ALL_ORIGINAL_ORIENTATIONS_AND_ONE_DISTINCT_REVERSAL','source_sha256':WORD,'paid_events':len(model.edges),'component_pairs':len(model.multiplicity),'chart_components':len(model.site),'externally_pinned':len(model.pinned),'original_price_histogram':decode(old),'direction_filter':dict(stats),'base_domain_cardinalities':base_domains,'maximum_elimination_width':maxw,'maximum_message_table_size':maxt,'alternate_equal_histogram_component_changes':alternative,'orientations':rows}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],len(model.site),dict(stats),base_domains,len(alternative),maxw,maxt)

if __name__=='__main__':main()
