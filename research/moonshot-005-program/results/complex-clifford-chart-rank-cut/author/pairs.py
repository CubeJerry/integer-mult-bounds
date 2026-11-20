"""Exhaust all unordered pairs of reversed endpoint inclusions via exact deletion filters."""
from pathlib import Path
import argparse,gzip,hashlib,json,time,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import Model,hull,ZERO,FULL,dim,need,cheaper,decode,WORD
from functools import cache
from collections import Counter

@cache
def exclusions(values,op,start):
    prefix=[start]
    for x in values:prefix.append(op(prefix[-1],x))
    suffix=start;out=[]
    for i in reversed(range(len(values))):out.append(op(prefix[i],suffix));suffix=op(suffix,values[i])
    return tuple(reversed(out))

def disjoint_filter(m):
    edges=sorted(m.multiplicity);idx={e:i for i,e in enumerate(edges)};n=len(m.site);nodes=range(n);order=m.order
    pinlo=[m.site[i]if i in m.pinned else ZERO for i in nodes];pinhi=[m.site[i]if i in m.pinned else FULL for i in nodes];selfbits=[1<<i for i in nodes]
    pred=[tuple(sorted(m.preds[i]))for i in nodes];succ=[tuple(sorted(m.succs[i]))for i in nodes];inpos=[{v:i for i,v in enumerate(q)}for q in pred];outpos=[{v:i for i,v in enumerate(q)}for q in succ];tags=[(u,v,inpos[v][u],outpos[u][v])for u,v in edges]
    candidates=[];start=time.monotonic()
    for k,(ban,bar)in enumerate(edges):
        low=pinlo.copy();high=pinhi.copy();desc=selfbits.copy();exlo=[None]*n;exhi=[None]*n;exde=[None]*n
        for v in order:
            vals=tuple(ZERO if j==ban and v==bar else low[j]for j in pred[v]);exlo[v]=exclusions(vals,hull,pinlo[v]);
            for x in vals:low[v]=hull(low[v],x)
        for u in reversed(order):
            vals=tuple(FULL if u==ban and j==bar else high[j]for j in succ[u]);ds=tuple(0 if u==ban and j==bar else desc[j]for j in succ[u]);exhi[u]=exclusions(vals,int.__and__,pinhi[u]);exde[u]=exclusions(ds,int.__or__,0)
            for x in vals:high[u]&=x
            for x in ds:desc[u]|=x
        ok=0
        for j,(u,v,i,w)in enumerate(tags):
            if j==k or exde[u][w]&selfbits[v]:continue
            lo=exlo[v][i];hi=exhi[u][w]
            if lo!=hi and lo&hi==lo:ok|=1<<j
        candidates.append(ok)
        if k and k%800==0:print('deleted orientations checked',k,'of',len(edges),round(time.monotonic()-start,1),flush=True)
    pairs=[]
    for i,row in enumerate(candidates):
        later=row & ~((1<<(i+1))-1)
        while later:
            bit=later&-later;later-=bit;j=bit.bit_length()-1
            if candidates[j]&(1<<i):pairs.append((edges[i],edges[j]))
    return edges,pairs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();raw=gzip.decompress(args.source.read_bytes());need(hashlib.sha256(raw).hexdigest()==WORD,'upstream source');m=Model(json.loads(raw));edges,pairs=disjoint_filter(m);print('candidate pairs',len(pairs),flush=True);rows=[];wins=[];start=time.monotonic();stats=Counter();maxw=maxt=0
    for i,es in enumerate(pairs):
        r=m.solve(es)
        if r is None:stats['infeasible_or_forced_equal_cycle']+=1;continue
        val,labels,w,t,_=r;maxw=max(w,maxw);maxt=max(t,maxt);state='cheaper'if cheaper(val,m.cost)else'same_histogram'if val==m.cost else'more_expensive';stats[state]+=1
        rows.append([es,decode(val)])
        if state=='cheaper':wins.append([es,decode(val),{v:hex(x)for v,x in labels.items()if m.site[v]!=x}]);print('actual cheaper',es,decode(val),flush=True)
        if i and i%500==0:print('exact pair dispatch',i,len(pairs),'elapsed',round(time.monotonic()-start),flush=True)
    args.out.mkdir(parents=True,exist_ok=True);summ={'source_sha256':WORD,'unordered_component_pairs':len(edges)*(len(edges)-1)//2,'pairs_satisfying_both_deleted_graph_strict_filters':len(pairs),'exact_solutions':dict(stats),'maximum_elimination_width':maxw,'maximum_exact_table':maxt,'lower_candidates':wins,'feasible_histograms_sha256':hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()};(args.out/'PAIR-RESULT.json').write_text(json.dumps(summ,indent=2,sort_keys=True)+'\n');print('complete',summ,flush=True)
if __name__=='__main__':main()
