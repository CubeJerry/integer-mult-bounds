#!/usr/bin/env python3
"""Independent exact source, SCC, target-support and directed-price review.

Imports only earlier independent readers/reviews, never the current author
checker or its graph/price implementations. SCCs replace the author's cycle
reachability census; every one of 2048 deletion graphs is traversed directly.
"""
import argparse,gzip,hashlib,importlib.util,json,sys
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def decimal(z,p=24):
    scale=10**p;ans=[]
    for x in [z[0].numerator*scale//z[0].denominator,-((-z[1].numerator*scale)//z[1].denominator)]:
        u,v=divmod(abs(x),scale);ans.append(('-'if x<0 else'')+str(u)+'.'+str(v).zfill(p))
    return ans
def reach(adj,s):
    seen={s};todo=[s]
    while todo:
        u=todo.pop()
        for v in adj[u]:
            if v not in seen:seen.add(v);todo.append(v)
    return seen
def adjacency(routes,removed=()):
    g=defaultdict(set)
    for e,(u,v)in routes.items():
        if e not in removed:g[u].add(v)
    return g
def scc(g,vertices):
    sys.setrecursionlimit(10000)
    clock=0;index={};low={};stack=[];active=set();component={};groups=[]
    def visit(v):
        nonlocal clock
        index[v]=low[v]=clock;clock+=1;stack.append(v);active.add(v)
        for w in g[v]:
            if w not in index:visit(w);low[v]=min(low[v],low[w])
            elif w in active:low[v]=min(low[v],index[w])
        if low[v]==index[v]:
            group=[]
            while True:
                w=stack.pop();active.remove(w);component[w]=len(groups);group.append(w)
                if w==v:break
            groups.append(sorted(group))
    for v in vertices:
        if v not in index:visit(v)
    return component,groups

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    base=args.repo/'research/moonshot-005-program/results';package=Path(__file__).resolve().parents[1]
    pins=json.loads((package/'root-review/PINS.json').read_text())
    for p,h in pins.items():need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest()==h,'review source pin '+p)
    R=module(base/'complex-native-source-cut/root-review/check.py','independent_source_cut')
    arith=module(args.repo/R.PRIOR,'independent_fraction_reader')
    price=module(base/'kappa-significant-gain-screen/root-review/check.py','independent_log_exp')
    source=args.repo/R.SOURCE
    data=json.loads(gzip.decompress((source/'DOUBLE-CANDIDATE.json.gz').read_bytes()))
    app=json.loads(gzip.decompress((source/'DOUBLE-APPLICATION.json.gz').read_bytes()))
    full=arith.source_transfer(data,app);need(arith.rank(full)==1289,'complete original target is invertible')
    spans=arith.subspaces(data['frames']);canon=arith.canonicalize(spans);vertices=sorted(set(canon));need(len(vertices)==1102,'canonical spaces')
    ff,four,fs,_=R.surgery(data,False);vf,five,vs,extra=R.surgery(data,True)
    need(R.evaluate(data,vf,five,vs,arith)==full,'genuine fifth export restores full1289 target')
    need(R.evaluate(data,ff,four,fs,arith)!=full,'four-channel negative control')
    original={e:(u,v)for e,u,v in data['moves']}
    canonical=lambda routes:{e:(canon[u],canon[v])for e,(u,v)in routes.items()}
    old,graph,paid=map(canonical,(original,four,five))
    need(paid[extra]==(3,282),'actual paid observer')
    grade=lambda e:abs(len(data['frames'][four[e][0]])-len(data['frames'][four[e][1]]))
    def balance(routes):
        z=Counter(canon[c]for c in data['initial']);z.subtract(canon[c]for c in data['final'])
        for u,v in routes.values():z[u]-=1;z[v]+=1
        return {c:v for c,v in z.items()if v}
    need(balance(old)=={}and balance(graph)=={278:1,282:-1}and balance(paid)=={3:-1,278:1},'exact original/surgery degree balance')
    g=adjacency(graph);components,groups=scc(g,vertices)
    cycles=sorted(e for e,(u,v)in graph.items()if components[u]==components[v])
    wide=sorted(e for e in graph if grade(e)>=3);candidates=sorted(set(wide)&set(cycles))
    author=json.loads((package/'author/output/RESULT.json').read_text())
    need(cycles==author['cycle_occurrences'],'independent SCC census matches every cycle occurrence')
    need(candidates==[r['slot']for r in author['wide_cycles']]and len(candidates)==11 and len(wide)==1076,'high-grade classification')
    rev=defaultdict(set)
    for u,v in graph.values():rev[v].add(u)
    from3=reach(g,3);regions={}
    for dst in [278,282]:
        region=from3&reach(rev,dst)
        slots=sorted(e for e,(u,v)in graph.items()if u in region and v in region)
        need(slots==author['path_regions'][str(dst)]['old_occurrences'],'every unused-path occurrence')
        need(all(grade(e)<=2 for e in slots),'high-grade deletions cannot occur on unused paths')
        regions[str(dst)]={'charts':sorted(region),'slots':slots}
    need(not rev[3]and 278 not in reach(g,282),'no observer-created cycle or extra278 path')
    dependencies=defaultdict(set)
    for i,row in enumerate(full):
        for j in row:dependencies[canon[data['initial'][j]]].add(canon[data['final'][i]])
    basegraph=adjacency(paid,set(candidates));relevant={}
    for src,dsts in dependencies.items():
        absent=dsts-reach(basegraph,src)
        if absent:relevant[src]=absent
    need(all(dsts<=reach(adjacency(paid),src)for src,dsts in dependencies.items()),'full paid graph has every target dependency')
    forbidden=[]
    for pair in combinations(candidates,2):
        A=adjacency(paid,set(pair))
        if any(not dsts<=reach(A,src)for src,dsts in relevant.items()):forbidden.append(list(pair))
    need(forbidden==[r['deleted']for r in author['forbidden_pairs']],'all55 pairs independently classified')
    for witness in author['forbidden_pairs']:
        deleted=set(witness['deleted']);i=witness['terminal_axis'];j=witness['input_axis']
        need(full[i].get(j)==F(witness['target_coefficient'])!=0,'literal nonzero target witness')
        closed={canon[x]for x in witness['closed_charts']}
        need(canon[data['initial'][j]]in closed and canon[data['final'][i]]not in closed,'input and required terminal separated')
        need(all(not(u in closed and v not in closed)for e,(u,v)in paid.items()if e not in deleted),'zero outgoing capacity independent of parallel multiplicity')
    feasible=[];profiles=set()
    for mask in range(1<<len(candidates)):
        deleted={e for k,e in enumerate(candidates)if mask>>k&1}
        A=defaultdict(set,{u:set(v)for u,v in basegraph.items()})
        for e in candidates:
            if e not in deleted:u,v=paid[e];A[u].add(v)
        good=all(dsts<=reach(A,src)for src,dsts in relevant.items())
        need(good==all(not set(pair)<=deleted for pair in forbidden),'all2048 direct graph traversals equal pair clauses')
        if good:
            hist=Counter(grade(e)for e in deleted);feasible.append((sorted(deleted),hist));profiles.add(tuple(sorted(hist.items())))
    need(len(feasible)==352,'exact support feasible subsets')
    best=max(sum(k*v for k,v in hist.items())for _,hist in feasible)
    maximizers=[D for D,h in feasible if sum(k*v for k,v in h.items())==best]
    need(best==28 and maximizers==author['maximizing_subsets'],'both maximizing deletion families')
    old_profile=Counter(abs(len(data['frames'][u])-len(data['frames'][v]))for u,v in original.values())
    four_profile=Counter(grade(e)for e in four)
    diff=price.hist((1,old_profile),(-1,four_profile));need({k:v for k,v in diff.items()if v}=={3:1,5:1,7:-1},'literal surgery tariff')
    caller=app['caller_census'];native=app['native'];calls=F(caller['calls'])
    required=price.hist((1,native['paid_native_ranks']),(-1,native['positive_helper_ranks']),(-1/calls,caller['fixed_root_targets']),(1/calls,caller['fixed_caller_paid']))
    best_profile={3:1,4:5,5:1};net=price.hist((1,best_profile),(1,{5:1,7:-1}));prices={}
    for k in [F(43,10000),F(1,200)]:
        maximum=price.moment(best_profile,k)
        for profile in profiles:
            need(dict(profile)==best_profile or price.moment(dict(profile),k)[1]<maximum[0],'strict maximum among all distinct feasible profiles')
        gain=price.moment(net,k);threshold=price.moment(required,k);margin=(gain[0]-threshold[1],gain[1]-threshold[0])
        prices[str(k)]={'deleted':decimal(maximum),'net':decimal(gain),'required':decimal(threshold),'margin':decimal(margin)}
        supplied=author['prices'][str(k)]
        for field,value in [('maximum_high_grade_deleted_moment',maximum),('maximum_net_saving_with_one_paid_observer',gain),('complete_caller_required_saving',threshold),('unallocated_margin_for_additional_costs',margin)]:
            bracket=supplied[field]
            if isinstance(bracket,dict):raise ValueError('unexpected author price representation')
            need(F(bracket[0])<=value[0]and value[1]<=F(bracket[1]),'independent prices within outward author bounds')
    receipt={'status':'PASS_INDEPENDENT_PAID_EXPORT_SIEVE','target_columns':1289,'target_digest':arith.digest(full),'canonical_charts':len(vertices),'cycle_occurrences':cycles,'mandatory_high_grade':len(wide)-len(candidates),'cycle_candidates':candidates,'regions':regions,'forbidden_pairs':forbidden,'directly_traversed_subsets':2048,'support_feasible_subsets':352,'maximizing_subsets':maximizers,'prices':prices,'scope':'Arbitrary linear recoding and retiming, fixed original inputs/outputs, deletion subsets, and k>=1 paid parallel3->282 exports; no sufficiency or new kappa.'}
    (args.out/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(receipt['status'],len(candidates),len(forbidden),352,flush=True)

if __name__=='__main__':main()
