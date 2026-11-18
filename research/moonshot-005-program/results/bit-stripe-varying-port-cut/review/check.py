#!/usr/bin/env python3
"""Independent exact color-domain review of varying-stripe capacity caps."""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations,product
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR_HASH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'

def need(ok,why):
    if not ok:raise ValueError(why)

def members(mask):
    while mask:
        b=mask&-mask;mask^=b;yield b.bit_length()-1

def verify_coloring(edges,n,k,colors):
    if colors is None:return False
    if len(colors)!=n or set(colors)!=set(range(k)):return False
    return all(any(v in E and len({colors[u]for u in E})==1 for E in edges)for v in range(n))

def has_packing(masks,k):
    if k==1:return bool(masks)
    for i,a in enumerate(masks):
        for j in range(i+1,len(masks)):
            b=masks[j]
            if a&b:continue
            if k==2:return True
            if any(not(c&(a|b))for c in masks[j+1:]):return True
    return False

def solve(masks,n,k):
    """Finite-domain support consistency, then MRV vertex branching.

    The author branches bitsets of color classes. This implementation instead
    maintains each vertex's allowed-color domain and propagates hyperedge
    support masks; it never imports author search or previously derived caps.
    """
    masks=tuple(sorted(set(masks)));edges=tuple(tuple(members(E))for E in masks)
    if n<k or not has_packing(masks,k):return {'sat':False,'nodes':0,'reason':'no disjoint port anchors'}
    incident=tuple(tuple(t for t,E in enumerate(edges)if v in E)for v in range(n))
    if any(not x for x in incident):return {'sat':False,'nodes':0,'reason':'uncovered vertex'}
    allcolors=(1<<k)-1;nodes=0
    @lru_cache(None)
    def search(state):
        nonlocal nodes
        nodes+=1;domains=list(state)
        while True:
            changed=False;support=[0]*n;edgecolors=[]
            for E in edges:
                c=allcolors
                for v in E:c&=domains[v]
                edgecolors.append(c)
                if c:
                    for v in E:support[v]|=c
            for v in range(n):
                d=domains[v]&support[v]
                if not d:return None
                if d!=domains[v]:domains[v]=d;changed=True
            if changed:continue
            for v in range(n):
                d=domains[v]
                if d&(d-1):continue
                candidates=[t for t in incident[v]if edgecolors[t]&d]
                if len(candidates)==1:
                    for u in edges[candidates[0]]:
                        if domains[u]!=d:domains[u]=d;changed=True
            if changed:continue
            used=0
            for d in domains:
                if not(d&(d-1)):used|=d
            free=[v for v,d in enumerate(domains)if d&(d-1)]
            missing=allcolors^used
            if len(free)<missing.bit_count():return None
            for c in members(missing):
                possible=[v for v in free if domains[v]>>c&1]
                if not possible:return None
                if len(possible)==1:domains[possible[0]]=1<<c;changed=True
            if changed:continue
            if len(free)==missing.bit_count() and missing:
                for v in free:
                    d=domains[v]&missing
                    if not d:return None
                    if d!=domains[v]:domains[v]=d;changed=True
            if not changed:break
        if not free:
            colors=tuple(d.bit_length()-1 for d in domains)
            return colors if verify_coloring(edges,n,k,colors)else None
        v=min(free,key=lambda v:(domains[v].bit_count(),-sum(len(edges[t])for t in incident[v]),v))
        allowed=domains[v]&used
        unused=domains[v]&~used
        if unused:allowed|=unused&-unused
        for c in members(allowed):
            nxt=domains[:];nxt[v]=1<<c;answer=search(tuple(nxt))
            if answer is not None:return answer
        return None
    start=[allcolors]*n;start[0]=1;answer=search(tuple(start))
    if answer is not None:need(verify_coloring(edges,n,k,answer),'constructed partition checks independently')
    return {'sat':answer is not None,'nodes':nodes,'colors':answer,'reason':'exhaustive finite domain search'}

def brute(masks,n,k):
    E=[tuple(members(m))for m in masks]
    return any(verify_coloring(E,n,k,c)for c in product(range(k),repeat=n))

def span(rows):
    s={0}
    for r in rows:s|={x^r for x in list(s)}
    return frozenset(s)

def binary_rank(rows):
    pivots={}
    for value in rows:
        while value:
            p=value.bit_length()-1
            if p not in pivots:pivots[p]=value;break
            value^=pivots[p]
    return len(pivots)

def controls():
    cases=0
    for n in range(1,4):
        possibilities=list(range(1,1<<n))
        for family in range(1<<len(possibilities)):
            E=[p for j,p in enumerate(possibilities)if family>>j&1]
            for k in range(1,min(n,3)+1):
                need(solve(E,n,k)['sat']==brute(E,n,k),'exhaustive small hypergraph coloring')
                cases+=1
    edges=[(1<<a)|(1<<b)for a,b in combinations(range(4),2)]
    for family in range(64):
        E=[p for j,p in enumerate(edges)if family>>j&1]
        for k in[2,3]:
            need(solve(E,4,k)['sat']==brute(E,4,k),'four-vertex graph coloring control');cases+=1
    spaces=sorted({span([a,b])for a,b in combinations(range(1,16),2)},key=lambda s:sorted(s))
    need(len(spaces)==35,'all two-dimensional quotient spaces')
    common_cases=0
    for U,V in product(spaces,repeat=2):
        parent=list(range(16))
        def root(a):
            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
            return a
        for S in[U,V]:
            rows=sorted(S-{0})[:2];fibres={}
            for x in range(16):
                val=tuple((x&r).bit_count()%2 for r in rows)
                if val in fibres:parent[root(x)]=root(fibres[val])
                else:fibres[val]=x
        need(len({root(x)for x in range(16)})==len(U&V),'arbitrary common functions factor through row intersection')
        common_cases+=1
    stripe_cases=0
    for a,b,c,d in product(range(1,4),repeat=4):
        U=span([a,b<<2]);V=span([c,d<<2]);expected=span(([a]if a==c else[])+([b<<2]if b==d else[]))
        need(U&V==expected,'aligned stripe intersection');stripe_cases+=1
    return {'exhaustive_hypergraph_and_graph_cases':cases,'nonlinear_common_function_quotient_pairs':common_cases,'aligned_stripe_intersections':stripe_cases}

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--factor',type=Path,required=True);p.add_argument('--author-result',type=Path);p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_HASH,'layout pin');w=json.loads(raw)
    roots=w['root_table'];H=[set(x)for x in w['A2']];D=[set(x)for x in w['D4']];native=set(range(111))
    perpendicular=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots[:111]]
    I=[[i for i in range(111)if h<=perpendicular[i]]for h in H]
    DV=[{i for i in range(111)if d<=perpendicular[i]}for d in D]
    factor_raw=a.factor.read_bytes();need(sha256(factor_raw).hexdigest()==FACTOR_HASH,'factor pin');factor=dict(json.loads(factor_raw)['factors'])
    x={h:12//len(P&native)+factor.get(h,0)for h,P in enumerate(H)if P&native}
    need(all(45*sum(x[h]for h,P in enumerate(H)if j in P)==5760 for j in native),'all original early source-bank counts')
    need(all(max(8,x[h])==8 for h,P in enumerate(H)if len(P&native)>=2),'ordinary source cuts have360 symbols')
    need(all(max(8,x[h])==12 for h,P in enumerate(H)if len(P&native)==1),'singleton source cuts have540 symbols')
    K=[(1<<i)^sum(1<<j for j in perpendicular[i]&native)for i in range(111)]
    need(binary_rank(K)==9,'canonical rank nine')
    for i in range(111):
        complement=((1<<111)-1)^sum(1<<j for j in perpendicular[i]&native)
        need(binary_rank([v&complement for v in K])==9,'outside canonical neutrality')
    singletons={next(iter(h&native)):z for z,h in enumerate(H)if len(h&native)==1}
    need(len(singletons)==11,'eleven singleton source flags')
    def tight(j,i):return j not in singletons or i not in I[singletons[j]]
    pair_hist=Counter(tight(j,i)for i in range(111)for j in perpendicular[i]&native)
    need(pair_hist=={True:6110,False:360},'actual tight and slack source cuts')
    records=[];hist=Counter();total_uncovered=0;capacity=11*540;solves=0;nodes=0
    for h,P in enumerate(H):
        J=sorted(P&native)
        if len(J)<2:continue
        targets=[i for i in I[h]if all(tight(j,i)for j in J)];index={i:v for v,i in enumerate(targets)}
        mids=[d for d,Q in enumerate(D)if P<=Q];need(len(mids)==45,'actual forty-five plane ports')
        need(all(sum(i in DV[d]for d in mids)==15 for i in targets),'every joint-tight receiver sees fifteen ports')
        allmasks=[sum(1<<index[i]for i in DV[d]&set(targets))for d in mids]
        uncovered=allmasks.count(0);total_uncovered+=uncovered
        masks=sorted(set(allmasks)-{0});n=len(targets);k2=solve(masks,n,2);k3=None
        solves+=int(k2['nodes']>0);nodes+=k2['nodes']
        if not k2['sat']:cap=1
        elif len(J)==2:cap=2
        else:
            k3=solve(masks,n,3);solves+=int(k3['nodes']>0);nodes+=k3['nodes'];cap=3 if k3['sat']else 2
        hist[len(J),cap]+=1;capacity+=360*cap+24*uncovered
        records.append({'plane':h,'native_donors':J,'joint_tight_receivers':targets,'port_neighborhoods':masks,'uncovered_ports':uncovered,'rank_cap':cap,'k2':k2,'k3':k3})
    need(len(records)==1108 and total_uncovered==1436,'all ordinary planes and exact uncovered count')
    need(hist=={(3,1):630,(3,2):249,(3,3):2,(2,1):204,(2,2):23},'independently obtained rank cap distribution')
    need(capacity==538644 and 102*5760-capacity==48876,'strict global cut deficit')
    author_pin=None
    if a.author_result:
        author_raw=a.author_result.read_bytes();author_pin=sha256(author_raw).hexdigest();z=json.loads(gzip.decompress(author_raw)if author_raw[:2]==b'\x1f\x8b'else author_raw)
        entries=z.get('records',z.get('planes'));need(entries is not None,'author plane records')
        theirs={q.get('h',q.get('plane')):q.get('cap',q.get('rank_cap'))for q in entries}
        need(theirs=={q['plane']:q['rank_cap']for q in records},'all author plane caps agree')
        ours={q['plane']:q for q in records}
        for q in entries:
            mine=ours[q.get('h',q.get('plane'))]
            if 'donors'in q:need(q['donors']==mine['native_donors'],'all donor sets agree')
            if 'receivers'in q:need(q['receivers']==mine['joint_tight_receivers'],'all joint-tight receiver sets agree')
            if 'uncovered_ports'in q:need(q['uncovered_ports']==mine['uncovered_ports'],'all uncovered counts agree')
            for k,key in[(2,'two_colors'),(3,'three_colors')]:
                decision=q.get(key)
                if decision and decision['status']=='SAT':
                    colors=[-1]*len(mine['joint_tight_receivers'])
                    for c,mask in enumerate(decision['colors']):
                        for v in members(mask):need(colors[v]==-1,'disjoint author color classes');colors[v]=c
                    need(verify_coloring([tuple(members(E))for E in mine['port_neighborhoods']],len(colors),k,colors),'every author SAT witness checked')
    output={'status':'PASS_INDEPENDENT_VARYING_STRIPE_ARRAY_GATE','layout_uncompressed_sha256':LAYOUT_HASH,'factor_sha256':FACTOR_HASH,'author_proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),'author_result_sha256':author_pin,'rank_cap_histogram':[[list(k),v]for k,v in sorted(hist.items())],'ordinary_planes':len(records),'uncovered_ports':total_uncovered,'covered_capacity':sum(360*q['rank_cap']for q in records),'uncovered_capacity':24*total_uncovered,'singleton_capacity':11*540,'total_capacity':capacity,'required_kernel_capacity':102*5760,'deficit':102*5760-capacity,'finite_domain_searches':solves,'finite_domain_nodes':nodes,'controls':controls(),'records':records,'author_search_imported':False,'timeouts_or_float_solvers_used':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(output,indent=2)+'\n');print(output['status'],capacity,'deficit',output['deficit'],'searches',solves,'nodes',nodes,dict(hist),flush=True)

if __name__=='__main__':main()
