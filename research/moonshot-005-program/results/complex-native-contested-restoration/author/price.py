"""Directed dyadic moment estimates and constructive single-grade funding."""
from collections import Counter
from fractions import Fraction as Q
from functools import cache
from math import isqrt
from graph import ROOT,require
import json

GRID=1<<288
BITS=112
TARGET=Q(1,200)
TRIAL=Q('0.0050005')
POWER=1<<30


def multiply(a,b):
    return a[0]*b[0]//GRID,-(-a[1]*b[1]//GRID)


@cache
def real_power(x,s):
    x,s=Q(x),Q(s)
    require(x>=1 and 0<=s<=1,'power domain')
    r=((x*GRID).__floor__(),(x*GRID).__ceil__())
    if s==1:
        return r
    z=(GRID,GRID)
    for _ in range(BITS):
        if not s:
            break
        lo,hi=isqrt(r[0]*GRID),isqrt(r[1]*GRID)
        r=(lo,hi+(hi*hi!=r[1]*GRID))
        bit,s=divmod(2*s,1)
        if bit:
            z=multiply(z,r)
    if s:
        z=(z[0],multiply(z,r)[1])
    return z


def moment(hist,s):
    lo=hi=0
    for k,n in hist.items():
        l,h=real_power(k,s)
        if n<0:
            l,h=h,l
        lo+=n*l
        hi+=n*h
    return Q(lo,GRID),Q(hi,GRID)


def difference(a,b):
    return a[0]-b[1],a[1]-b[0]


def add_profiles(*pairs):
    out=Counter()
    for scale,d in pairs:
        for k,v in d.items():
            out[k]+=scale*v
    return {k:v for k,v in out.items()if v}


def pretty(r):
    scale=10**12
    def fmt(n):
        sign='-' if n<0 else ''
        a,b=divmod(abs(n),scale)
        return f'{sign}{a}.{b:012d}'
    return [fmt((r[0]*scale).__floor__()),fmt((r[1]*scale).__ceil__())]


def chart_paths(g,relations):
    successor=dict(relations)
    predecessor={e:f for f,e in relations}
    require(len(successor)==len(predecessor)==len(relations),'paid vertex reused on a path')
    visited=set()
    hist=Counter()
    edge_lengths=Counter()
    for start in g.moves.keys()-predecessor.keys():
        total=0
        terms=0
        e=start
        while True:
            require(e not in visited,'cycle or double-spend')
            visited.add(e)
            total+=g.rank[e]
            terms+=1
            if e not in successor:
                break
            e=successor[e]
        require(total==abs(g.dimension[g.moves[start][0]]-g.dimension[g.moves[e][1]]),'summed nested charge')
        hist[total]+=1
        edge_lengths[terms]+=1
    require(visited==g.moves.keys(),'all paid events accounted')
    return hist,edge_lengths


def price(g):
    readers=Counter(e for row in g.forms.values()for e in row)
    arcs={(e,f) for f,(a,b) in g.moves.items() for e in g.forms[f]
          if e in g.moves and g.moves[e][1]==a and g.sign[e]==g.sign[f]}
    private={(e,f) for e,f in arcs if readers[e]==1 or len(g.forms[f])==1}
    extra={tuple(v)for v in json.loads((ROOT/'sources'/'contested-witness.json').read_text())}
    require(extra<=arcs-private and len(extra)==152,'contested word incidence')
    short,lengths=chart_paths(g,private)
    witness,_=chart_paths(g,private|extra)
    original,_=chart_paths(g,set())
    require(original==g.native and len(arcs)==11511 and len(private)==1727,'path family census')
    m=g.calls
    targets=add_profiles((1,g.fixed_root),(m,g.helpers))
    def completed(h):
        return add_profiles((1,g.fixed_paid),(m,h))
    def gap(h,price):
        return moment(add_profiles((1,targets),(-1,completed(h))),1-price)
    native_gap=gap(original,TARGET)
    need=(-native_gap[1]/m,-native_gap[0]/m)
    best=moment(add_profiles((1,original),(-1,short)),1-TARGET)
    residual=difference(need,best)
    join=moment({4:1,5:1,9:-1},1-TARGET)
    require(126*join[1]<residual[0] and 127*join[0]>residual[1],'contested join lower bound')
    left,right=Q('.00500109954083'),Q('.00500109954084')
    require(gap(witness,left)[0]>0>gap(witness,right)[1],'altered crossing bracket')
    require(gap(short,TARGET)[1]<0<gap(witness,TARGET)[0],'two pathway tariffs')
    # Even arbitrarily many private joins, or the 151-entry truncated witness, fail.
    truncated=json.loads((ROOT/'sources'/'contested-witness.json').read_text())[:-1]
    truncated_hist,_=chart_paths(g,private|set(map(tuple,truncated)))
    require(gap(truncated_hist,TARGET)[1]<0,'remove final contested move')
    counts={'original':dict(sorted(original.items())),'all_private_coarsened':dict(sorted(short.items())),
            'private_plus_152_contested':dict(sorted(witness.items()))}
    record={'graph_incidences':len(arcs),'private_joins':len(private),'maximal_path_lengths':dict(lengths),
            'source_histograms':counts,'original_gap':pretty(native_gap),'gain_needed_per_native':pretty(need),
            'maximum_private_native_gain':pretty(best),'remaining_per_native':pretty(residual),
            'maximum_one_contested_join_gain':pretty(join),'necessary_contested_per_identical_copy':127,
            'witness_contested_joins':len(extra),'witness_caller_gap_at_target':pretty(gap(witness,TARGET)),
            'witness_raw_crossing':[str(left),str(right)],'truncated_caller_gap':pretty(gap(truncated_hist,TARGET))}
    return record,completed(witness),targets


@cache
def log2_bounds(k):
    # Compare an integer 2048th power with consecutive exact powers of 2.
    k=Q(k)
    v=2048
    n,d=k.numerator**v,k.denominator**v
    h=n.bit_length()-d.bit_length()
    if n<d<<h:
        h-=1
    return Q(h,v),Q(h+1,v)


def modal(hist,v,t):
    W={k:moment({k:n},t)for k,n in hist.items()}
    mid={k:(l+h)/2 for k,(l,h)in W.items()}
    total=sum(mid.values())
    counts={k:(v*w/total).__floor__() for k,w in mid.items()}
    while sum(counts.values())<v:
        i=max(mid,key=lambda k:mid[k]/(counts[k]+1))
        counts[i]+=1
    require(min(W[k][0]/n for k,n in counts.items() if n)>max(W[k][1]/(n+1)for k,n in counts.items()),'exact modal exchange')
    return counts


def compiler(paid,targets):
    t=1-TRIAL
    pt,tt=moment(paid,t),moment(targets,t)
    p1=sum(k*n for k,n in paid.items())
    mT=sum(n*log2_bounds(k)[0]for k,n in targets.items())/sum(targets.values())
    mP=sum(k*n*log2_bounds(k)[1]for k,n in paid.items())/p1
    require(mT-mP>Q(1,8),'full paid chord')
    v=POWER
    n=modal(targets,v,t)
    klow=Q(239,10)
    grade_gap=sum(nk*log2_bounds(k)[0] for k,nk in n.items())-v*log2_bounds(klow)[1]
    require(grade_gap>0,'finite grade lower')
    cutoff=moment({70:1},TRIAL/2)[0]
    deficit=min(1-pt[1]/tt[0],1-p1/(tt[0]*cutoff))
    d=len(targets)
    require(v*deficit>d*31+3,'split batch funding')
    r=moment({klow:1},t)[0]
    upper_B=tt[1]/r
    require(upper_B*70**5<klow**10,'degree ten')
    cap=Q(49,2);s=Q(1,1000)
    dK=pt[0]*moment({cap:1},s)[0]-moment(targets,t+s)[1]
    dh=p1-tt[1]*moment({8:1},TRIAL)[1]
    db=pt[0]-moment({cap:1},t)[1]*Q(31,10)**9
    require(min(dK,dh,db)>0 and cap/8<Q(31,10),'degree nine obstruction')
    return {'trial_saving':str(TRIAL),'target_mean_log2_lower':str(mT),'paid_mean_log2_upper':str(mP),
            'positive_log2_chord_derivative_margin_lower':str(mT-mP),'positive_raw_gap_at_trial':pretty(difference(tt,pt)),
            'power':v,'mode':n,'grade_above':'(239/10)^v','scaled_funding_slack_lower':str((v*deficit).__floor__()),
            'scaled_overhead_upper':d*31+3,'split_cutoff':'70^(v/2)','width_degree':10,
            'strict_degree_nine_controls':{'paid_over_large_grade':pretty((dK,dK)),'linear_mass_over_cutoff':pretty((dh,dh)),
               'batch_over_3.1_to_nine':pretty((db,db))}}


if __name__=='__main__':
    from graph import Graph
    q,p,t=price(Graph())
    print(json.dumps(q,indent=2))
    print(json.dumps(compiler(p,t),indent=2))
