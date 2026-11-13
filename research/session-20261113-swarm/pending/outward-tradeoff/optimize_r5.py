"""Exact finite threshold search; all bounds are rational square-root enclosures."""
from fractions import Fraction as Q
from itertools import product
from math import isqrt
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from search_q2 import H, matching, need, norm2


def all_candidates(x):
    z = tuple(sum(a*b for a,b in zip(r,x)) for r in H)
    # Independent complete coordinate boxes, then exact Euclidean error filter.
    choices = [range((a-2+1)//2, (a+2)//2+1) for a in z]
    return [y for y in product(*choices) if sum((2*a-b)**2 for a,b in zip(y,z))<=4]


def rational_allowed(a,b,c):
    if a<=b:
        return True
    d=Q(a-b)-c*c
    return d<=0 or d*d<=4*c*c*b


def main():
    radius=5
    xs=[x for x in product(range(-5,6),repeat=4) if norm2(x)<=25]
    all_edges={x:all_candidates(x) for x in xs}
    pairs={(norm2(y),norm2(x)) for x in xs for y in all_edges[x] if norm2(y)>norm2(x)}
    scale=1<<128
    groups=[]
    raw=[]
    for a,b in pairs:
        la,lb=isqrt(a*scale*scale),isqrt(b*scale*scale)
        ua,ub=la+int(la*la!=a*scale*scale),lb+int(lb*lb!=b*scale*scale)
        raw.append((la-ub,ua-lb,a,b))
    for lo,hi,a,b in sorted(raw):
        if groups and lo<=groups[-1]['hi']:
            need(lo==hi==groups[-1]['lo']==groups[-1]['hi'], 'distinct radical intervals must separate')
            groups[-1]['pairs'].append((a,b))
        else:
            groups.append({'lo':lo,'hi':hi,'pairs':[(a,b)]})
    probes=[]
    cache={}
    def run(i):
        if i not in cache:
            top=groups[i+1]['lo'] if i+1<len(groups) else groups[i]['hi']+2
            c=Q(groups[i]['hi']+top,2*scale)
            edges={x:[y for y in all_edges[x] if rational_allowed(norm2(y),norm2(x),c)] for x in xs}
            chosen,hall=matching(xs,edges)
            cache[i]=(c,edges,chosen,hall)
            probes.append({'index':i,'threshold_pair':groups[i]['pairs'][0],'complete':hall is None,'matched':len(chosen)})
        return cache[i]
    lo,hi=-1,len(groups)-1
    need(run(hi)[3] is None,'top finite candidate bound')
    while hi-lo>1:
        mid=(lo+hi)//2
        if run(mid)[3] is None:
            hi=mid
        else:
            lo=mid
    good=run(hi);bad=run(lo) if lo>=0 else None
    need(bad is not None and bad[3] is not None,'nonzero optimum with explicit Hall witness')
    a,b=groups[hi]['pairs'][0]
    out={'scope':'exact complete radius-five finite input ball only; global necessity, not global sufficiency',
         'matrix_numerator':H,'denominator':2,'error_bound_squared':1,'radius':5,'inputs':len(xs),
         'threshold_pair':[a,b], 'threshold_expression':f'sqrt({a})-sqrt({b})',
         'threshold_interval_bits':128,'threshold_scaled_interval':[groups[hi]['lo'],groups[hi]['hi']],
         'distinct_positive_thresholds':len(groups),'search_probes':probes,
         'matching':[[list(x),list(y)] for x,y in good[2].items()],
         'strict_lower_graph_rational_threshold':str(bad[0]),'hall':bad[3],
         'lower_hall_sizes':[len(bad[3]['input_set']),len(bad[3]['output_neighbors'])]}
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
