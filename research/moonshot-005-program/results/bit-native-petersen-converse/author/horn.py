"""Integer proof of local Petersen leakage and every native directed-arc implication."""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

N = 111
LAYOUT_SHA = '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
PAIRS = list(combinations(range(5), 2))
PAIR_INDEX = {p:i for i,p in enumerate(PAIRS)}


def need(val, msg):
    if not val:
        raise ValueError(msg)


def pair_permutations():
    for perm in permutations(range(5)):
        yield [PAIR_INDEX[tuple(sorted((perm[a],perm[b])))] for a,b in PAIRS]


def perm_mask(S, perm):
    return sum(1 << perm[i] for i in range(10) if S >> i & 1)


def local_dual(q):
    source, target = q['premise_mask'], q['consequent']
    need((source,target) == (59,9), 'prescribed five-variable template')
    group = [p for p in pair_permutations() if perm_mask(source,p)==source and p[target]==target]
    need(len(group)==2, 'exact template stabilizer')
    total=Counter(); rhs=0; counts=Counter()
    for w,kind,*args in q['terms']:
        counts[kind]+=1
        if kind in ('mono','submod'):
            need(w>0, 'nonnegative dual inequalities')
        if kind=='empty':
            total[0]+=len(group)*w
            continue
        S,i,*extra=args
        need(0<=S<1024 and i in range(10) and not (S>>i)&1, 'native local entropy increment')
        if kind=='decode':
            need(all(set(PAIRS[j])&set(PAIRS[i]) for j in range(10) if S>>j&1), 'only true decoding equalities')
        if kind=='submod':
            j,=extra;need(j in range(10) and i!=j and not(S>>j)&1, 'valid submodular increment')
        for p in group:
            t=perm_mask(S,p);a=1<<p[i]
            if kind in ('mono','decode'):
                total[t|a]+=w;total[t]-=w
                if kind=='decode':rhs+=w
            elif kind=='submod':
                b=1<<p[j];total[t|a]+=w;total[t|b]+=w;total[t]-=w;total[t|a|b]-=w
            else:raise ValueError('known exact dual predicate')
    nonzero={k:v for k,v in total.items() if v}
    need(nonzero=={1023:8,source:4,source|1<<target:-4} and rhs==40,'raw local half-leakage integer identity')
    return {'group_size':len(group),'predicate_counts':dict(counts),'raw_nonzero_coefficients':nonzero,'raw_rhs_over_B':rhs,'marginal_per_excess':2}


def graph(roots):
    return [sum(1<<j for j,b in enumerate(roots) if sum(x*y for x,y in zip(a,b))==0) for a in roots]


def verify_horn(g,cert):
    raw=[]
    for p in pair_permutations():
        raw.append((tuple(sorted(p[k] for k in range(10) if 59>>k&1)),p[9]))
    templates=sorted(set(raw));num=len(templates);need(num==60,'all labelled five-premise predicates')
    for C,P in cert['charts']:
        need(len(C)==4 and len(P)==10 and len(set(C+P))==14 and all(0<=q<N for q in C+P),'distinct native owner chart')
        c=sum(1<<a for a in C);b=sum(1<<a for a in P)
        for v in C:need(not g[v]&(c|b),'four isolated true diagonals')
        for i,v in enumerate(P):
            expected=sum(1<<P[j] for j in range(10) if not set(PAIRS[i]) & set(PAIRS[j]))
            need(g[v]&b==expected,'induced genuine Petersen support')
    seen=set();used=set();steps=Counter();global_mask=(1<<N)-1
    for recipient,donor,sequence in cert['arcs']:
        need((recipient,donor) not in seen and g[recipient]>>donor&1,'genuine unique directed proper arc')
        seen.add((recipient,donor));need(len(sequence)==3,'two intermediate steps and a final implication')
        first=(global_mask & ~(g[recipient]|1<<recipient))|1<<donor;known=first
        for k,packed in enumerate(sequence):
            ch,t=divmod(packed,num);need(0<=ch<len(cert['charts']),'existing physical chart')
            used.add(ch);P=cert['charts'][ch][1];sources,result=templates[t];v=P[result]
            premise=sum(1<<P[u] for u in sources)
            need(not premise & ~(first if k<2 else known),'actual five previously available native columns')
            need(not known>>v&1,'new native marginal')
            if k==2:need(v==recipient,'conclusion at the true receiver')
            known|=1<<v
        steps[len(sequence)]+=1
    need(seen=={(i,j) for i in range(N) for j in range(N) if g[i]>>j&1} and len(seen)==6470,'every native direction')
    need(len(used)==len(cert['charts']),'only used physical charts')
    return {'charts':len(used),'native_directed_edges':len(seen),'template_orbit':num,'edge_path_length_histogram':dict(steps),'distinct_rule_applications':sum(n*v for n,v in steps.items()),'marginal_per_global_excess':6}


def main():
    p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--horn',type=Path,required=True);p.add_argument('--dual',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_SHA,'published native set');g=graph(json.loads(raw)['root_table'][:N]);hz=gzip.decompress(a.horn.read_bytes());c=json.loads(hz);d=json.loads(a.dual.read_bytes());e=local_dual(d);f=verify_horn(g,c);fault={}
    bad=deepcopy(d);bad['terms'][0][0]+=1
    try:local_dual(bad)
    except ValueError as exc:fault['dual_weight']=str(exc)
    for name,change in [('bad_owner',lambda x:x['charts'][0][1].__setitem__(0,x['charts'][0][0][0])),('bad_order',lambda x:x['arcs'][0][2].reverse()),('wrong_recipient',lambda x:x['arcs'][0].__setitem__(0,x['arcs'][0][1])),('missing_arc',lambda x:x['arcs'].pop())]:
        bad=deepcopy(c);change(bad)
        try:verify_horn(g,bad)
        except ValueError as exc:fault[name]=str(exc)
    need(len(fault)==5,'effective negative controls')
    data={'local_dual':e,'all_native_arcs':f,'native_layout_uncompressed_sha256':LAYOUT_SHA,'horn_uncompressed_sha256':sha256(hz).hexdigest(),'local_dual_sha256':sha256(a.dual.read_bytes()).hexdigest(),'negative_controls':fault,'native_floor_at_b3840':34560,'deleted_arc_floor_at_b3840':35200,'proper_minimum_rank_at_h128':3072}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'HORN-RESULT.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(data)


if __name__=='__main__':main()
