"""Public-only fixed-time funded-donor exterior tests in the actual P104 word."""
import argparse,gzip,json,importlib.util
from collections import defaultdict,Counter
from pathlib import Path
from functools import lru_cache
import time
T=time.monotonic()
def solve(src,out,mode):
    f=src/'7833-construction.py';spec=importlib.util.spec_from_file_location('p104',f);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    w=S.load_word(src/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);V=S.all_public_rows(g);shadow,=g.routes.keys()-w.routes.keys();allids=[*g.inputs,*g.schedule];table={e:1<<i for i,e in enumerate(allids)};sources={e:g.source(e) for e in g.schedule};dests={e:b for e,(a,b) in g.routes.items()};start=defaultdict(int)
    for e,a in g.inputs.items():start[a]|=table[e]
    start[g.routes[shadow][1]]|=table[shadow]
    full=(1<<len(g.inputs))-1
    support={e:sum(1<<j for j in V[e][1]) for e in V}
    def ids(x):
        while x:
            b=x&-x;yield allids[b.bit_length()-1];x^=b
    first=w.clock[w.readers(S.OBSERVER)[0]];donors=[e for e in w.schedule if e in w.routes and w.routes[e][0]==3 and w.clock[e]<first and w.grade(w.routes[e])>=3 and e not in (S.RETARGET,S.OBSERVER)]
    @lru_cache(maxsize=32000)
    def mask_support(mask):
        u=0
        for e in ids(mask):u|=support[e]
        return u
    good=[];remain=[];earlier={}
    for index,d in enumerate(donors):
        stock=start.copy();reached=set();groups=defaultdict(list);old=w.routes[d][1]
        for e in g.schedule:
            if e==shadow:continue
            if e==d:reached.add(old);continue
            a=sources[e];dirty=a in reached;ext=stock.get(a,0) if dirty else table[e]
            if e in dests:
                b=dests[e];stock[b]=stock.get(b,0)|ext
                if dirty:reached.add(b)
            elif dirty:groups[ext].append(e)
        if mode=='rank':
            p=out/'support.json'
            if p.exists() and d in {x['donor'] for x in json.loads(p.read_text())['excluded']}:continue
        found=None
        for m,es in sorted(groups.items(),key=lambda q:q[0].bit_count()):
            missing=full^mask_support(m)
            for e in es:
                pos=support[e]&missing
                if pos:
                    axis=(pos&-pos).bit_length()-1;fixed=list(ids(m));S.require(all(axis not in V[k][1]for k in fixed)and axis in V[e][1],'unit witness')
                    found={'donor':d,'original_route':w.routes[d],'grade':w.grade(w.routes[d]),'terminal':e,'boundary_count':len(fixed),'unit_axis':axis,'value_numerator':V[e][1][axis],'value_denominator':V[e][0]};break
            if found:break
        if mode=='rank' and not found:
            impact=w.evaluate({},{d:S.Q(1)})
            groups={m:[e for e in es if impact[e]]for m,es in groups.items()};groups={m:es for m,es in groups.items() if es}
            for m,es in sorted(groups.items(),key=lambda q:q[0].bit_count()):
                fixed=list(ids(m));freq=Counter(axis for i in fixed for axis in V[i][1]);order=sorted(range(len(g.inputs)),key=lambda j:(freq[j],j));E=S.IntegerElimination({j:i for i,j in enumerate(order)})
                for e in sorted(fixed,key=lambda i:(len(V[i][1]),i)):E.add(V[e][1])
                n=len(E.rows)
                for e in es:
                    if E.add(V[e][1]):
                        found={'donor':d,'original_route':w.routes[d],'grade':w.grade(w.routes[d]),'terminal':e,'boundary_count':len(fixed),'boundary_rank':n,'with_terminal':n+1};break
                if found:break
        if found:good.append(found)
        else:remain.append(d)
        if index%10==0 or index==len(donors)-1:print(index,'excluded',len(good),'remain',len(remain),'sec',round(time.monotonic()-T),flush=True)
        d0={'status':'PASS_TESTED_DONOR_EXTERIORS','total_candidates':len(donors),'mode':mode,'excluded':good,'undecided':remain}
        (out/(mode+'.json')).write_text(json.dumps(d0,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--mode',choices=['support','rank'],required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);solve(a.sources,a.out,a.mode)
