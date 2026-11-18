#!/usr/bin/env python3
"""Independent clean-receiver census and exhaustive small weighted-Rado controls."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations,product
from pathlib import Path
import gzip,json


def need(ok,why):
    if not ok:
        raise ValueError(why)


def span(vectors):
    out={0}
    for v in vectors:
        out |= {x^v for x in list(out)}
    return frozenset(out)


def dim(space):
    need(len(space)&(len(space)-1)==0,'binary subspace cardinality')
    return len(space).bit_length()-1


def controls():
    spaces=sorted({span(v) for n in range(4) for v in combinations(range(1,8),n)},key=lambda s:(len(s),sorted(s)))
    need(len(spaces)==16,'all subspaces of F2^3')
    weighted=0
    for U,V in product(spaces,repeat=2):
        hall=dim(U)>=2 and dim(V)>=1 and dim(span(U|V))>=3
        actual=any(len(span([a,b,c]))==8 for a,b in combinations(U-{0},2) for c in V-{0})
        need(hall==actual,'weights 2+1 exact source basis')
        weighted+=1
    unit=0
    for U,V,W in product(spaces,repeat=3):
        S=[U,V,W]
        hall=all(dim(span(set().union(*(S[i] for i in I))))>=len(I)
                 for n in range(1,4) for I in combinations(range(3),n))
        actual=any(len(span([a,b,c]))==8 for a,b,c in product(U-{0},V-{0},W-{0}))
        need(hall==actual,'three unit slots exact source basis')
        unit+=1
    U=span([1,2]); V=U
    need(dim(U)>=2 and dim(V)>=1 and dim(span(U|V))<3,'singleton ranks do not replace joint ranks')
    return {'weighted_2_plus_1_cases':weighted,'unit_1_plus_1_plus_1_cases':unit,
            'joint_rank_counterexample':[sorted(U),sorted(V)]}


def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True)
    p.add_argument('--author-result',type=Path,required=True);p.add_argument('--proof',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    w=json.loads(raw);R=w['root_table'];H=[set(h) for h in w['A2']]
    O=[{j for j,s in enumerate(R) if sum(x*y for x,y in zip(r,s))==0} for r in R[:111]]
    pencil=[[h for h,P in enumerate(H) if j in P] for j in range(111)]
    visible=[[i for i in range(111) if P<=O[i]] for P in H]
    singleton={j:next((h for h in pencil[j] if len(H[h]&set(range(111)))==1),None) for j in range(111)}
    tight=lambda j,i:singleton[j] is None or i not in visible[singleton[j]]
    ordinary=[(j,h) for j in range(111) for h in pencil[j] if h!=singleton[j]]
    need(len(ordinary)==3097 and sum(v is not None for v in singleton.values())==11,'all ordinary flags and singleton donors')
    witnesses={}
    for j,h in ordinary:
        good=[]
        for i in visible[h]:
            if not tight(j,i):
                continue
            others=[p for p in pencil[j] if p!=h and i in visible[p]]
            need(len(others)==15,'fifteen comparison planes')
            if all(any(k!=j and k<111 and tight(k,i) for k in H[p]) for p in others):
                good.append(i)
        witnesses[j,h]=good
    hist=Counter(len(x) for x in witnesses.values());need(min(hist)==13,'all flags have clean tight companions')
    author=json.loads(a.author_result.read_bytes())
    need(len(author['witnesses'])==3097,'one published witness per flag')
    got=set()
    for item in author['witnesses']:
        j,h,i=item['donor'],item['plane'],item['receiver'];need((j,h) not in got,'distinct published flags');got.add((j,h))
        need(i in witnesses[j,h] and item['available_receivers']==len(witnesses[j,h]),'independently recomputed witness receiver')
        expected={p for p in pencil[j] if p!=h and i in visible[p]}
        need({p for p,k in item['companions']}==expected and len(item['companions'])==15,'all comparison planes once')
        need(all(k in H[p] and k!=j and k<111 and tight(k,i) for p,k in item['companions']),'every actual companion is tight')
    need(got==set(ordinary),'complete ordinary flag coverage')
    need({str(k):v for k,v in sorted(hist.items())}==author['clean_witness_histogram'],'full independent histogram')
    receipt={'status':'PASS_INDEPENDENT_BALANCED_QUOTIENT_SOURCE_REVIEW',
             'author_proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),
             'author_result_sha256':sha256(a.author_result.read_bytes()).hexdigest(),
             'layout_uncompressed_sha256':sha256(raw).hexdigest(),'ordinary_flags':3097,
             'minimum_clean_receivers':min(hist),'clean_receiver_histogram':dict(sorted(hist.items())),
             'weighted_source_controls':controls(),'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(receipt['status'])


if __name__=='__main__':
    main()
