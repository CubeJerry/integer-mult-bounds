#!/usr/bin/env python3
"""Independent raw-DAG pullback, boundary and integer-power price review."""
from argparse import ArgumentParser
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip,json

def need(ok,message):
    if not ok:raise ValueError(message)

ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
b=args.repo/'research/moonshot-005-program/results';pkg=Path(__file__).resolve().parents[1]
for name,digest in json.loads((pkg/'SOURCE-PINS.json').read_text())['files'].items():need(sha256((args.repo/name).read_bytes()).hexdigest()==digest,'source pin '+name)
raw=gzip.decompress((b/'complex-native-funded-donor-cuts/inputs/DOUBLE-CANDIDATE.json.gz').read_bytes())
need(sha256(raw).hexdigest()=='7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48','literal source')
w=json.loads(raw);forms={e:[(i,Q(c))for i,c in rows]for e,rows in w['forms']};original={e:(u,v)for e,u,v in w['moves']}
routes=dict(original);del routes[95914];routes.update({94019:(3,278),90369:(3,304),88:(278,127)})
observer=max(w['schedule'])+1;with_observer={**routes,observer:(3,282)}
spaces=[]
for frame in w['frames']:
    S={0}
    for x in frame:S.update(y^x for y in tuple(S))
    need(len(S)==1<<len(frame),'independent chart frame');spaces.append(tuple(sorted(S)))
names={space:i for i,space in reversed(list(enumerate(spaces)))};canonical=[names[S]for S in spaces]
need(len(set(canonical))==1102,'canonical subspace vertices')
def closure(seeds,blocked=()):
    blocked=set(blocked);edges={c:set()for c in set(canonical)}
    for e,(u,v)in with_observer.items():
        if e not in blocked:edges[canonical[u]].add(canonical[v])
    seen={canonical[c]for c in seeds};todo=list(seen)
    while todo:
        fresh=edges[todo.pop()]-seen;seen.update(fresh);todo.extend(fresh)
    return seen

@lru_cache(None)
def reverse_row(terminal):
    weights={terminal:Q(1)}
    for e in reversed(w['schedule']):
        factor=weights.pop(e,0)
        if factor:
            for i,c in forms[e]:
                value=weights.get(i,0)+factor*c
                if value:weights[i]=value
                else:weights.pop(i,None)
    need(all(i<0 for i in weights),'complete reverse functional')
    return {~i:v for i,v in weights.items()}

cuts=[];mandatory=set()
for cert in json.loads((pkg/'CUTS.json').read_text())['cuts']:
    axes=cert['source_axes'];terminals=cert['terminal_slots'];blocked=set(cert['blocked_occurrences']);r=len(axes)
    inside=closure([w['initial'][j]for j in axes],blocked)
    boundary={e for e,(u,v)in with_observer.items()if canonical[u]in inside and canonical[v]not in inside}
    need(boundary==blocked and len(boundary)==r,'exact saturated boundary')
    need(canonical[3]not in inside,'arbitrary observer count does not add outgoing capacity')
    need(all(canonical[w['final'][e-w['first_output']]]not in inside for e in terminals),'target outside cut')
    matrix=[[reverse_row(e).get(j,Q(0))for j in axes]for e in terminals]
    diagonal=[Q(v)for v in cert['minor_diagonal']]
    need(matrix==[[diagonal[a]if a==c else Q(0)for c in range(r)]for a in range(r)],'independent exact diagonal minor')
    determinant=Q(1)
    for x in diagonal:determinant*=x
    need(determinant!=0,'full demand rank')
    mandatory|=boundary;cuts.append({'id':cert['id'],'rank':r,'determinant':str(determinant),'boundary':sorted(boundary),'canonical_cut_size':len(inside)})
    for e in boundary:
        need(len(boundary-{e})==r-1,'every single deletion loses one complete field')

graph={c:set()for c in set(canonical)}
for u,v in routes.values():graph[canonical[u]].add(canonical[v])
@lru_cache(None)
def reachable(v):
    seen={v};todo=[v]
    while todo:
        new=graph[todo.pop()]-seen;seen.update(new);todo.extend(new)
    return seen
grade=lambda route:abs(len(w['frames'][route[0]])-len(w['frames'][route[1]]))
wide={e for e,route in routes.items()if grade(route)>=3};cycles={e for e in wide if canonical[routes[e][0]]in reachable(canonical[routes[e][1]])}
need(len(wide)==1076 and len(cycles)==11,'inherited exact high-grade roster')
possible=cycles-mandatory;need(possible=={86,97232,97241,97323,99064},'five remaining candidates')
need(Counter(grade(routes[e])for e in possible)=={3:1,4:4},'optimistic deletion profile')

application=json.loads(gzip.decompress((b/'complex-native-contested-restoration/rail/sources/DOUBLE-APPLICATION.json.gz').read_bytes()))
native={int(k):Q(v)for k,v in application['native']['paid_native_ranks'].items()};helpers={int(k):Q(v)for k,v in application['native']['positive_helper_ranks'].items()};cc=application['caller_census'];need(cc['calls']==48,'all48 calls charged')
required=Counter(native)
for factor,profile in [(-1,helpers),(Q(1,48),cc['fixed_caller_paid']),(-Q(1,48),cc['fixed_root_targets'])]:
    for rank,count in profile.items():required[int(rank)]+=factor*Q(count)

@lru_cache(None)
def power_interval(rank,exponent):
    # Decimal only proposes endpoints. Integer inequalities certify both bounds.
    scale=1<<96;p,q=exponent.numerator,exponent.denominator
    with localcontext()as context:
        context.prec=100;centre=int((Decimal(rank)**(Decimal(p)/Decimal(q)))*scale)
    lo,hi=centre-2,centre+2;target=pow(rank,p)*pow(scale,q)
    need(pow(lo,q)<=target<=pow(hi,q),'exact outward integer-power enclosure')
    return Q(lo,scale),Q(hi,scale)
def moment(profile,t):
    lo=hi=Q(0)
    for rank,count in profile.items():
        if not count:continue
        a,c=power_interval(rank,t)
        if count<0:a,c=c,a
        lo+=count*a;hi+=count*c
    return lo,hi
prices={}
for kappa in (Q(43,10000),Q(1,200)):
    t=1-kappa;save=moment({3:1,4:4,5:1,7:-1},t);req=moment(required,t);margin=(save[0]-req[1],save[1]-req[0])
    need((margin[1]<0)if kappa==Q(1,200)else(margin[0]>0),'correct price sign')
    prices[str(kappa)]={'margin_bounds':[str(x)for x in margin],'approx':[float(x)for x in margin]}
result={'status':'PASS_ROOT_COMPLEX_SATURATED_CUT_REVIEW','cuts':cuts,'newly_mandatory_high_grade':sorted(cycles&mandatory),'remaining_high_grade':sorted(possible),'price_method':'96-bit rational endpoints certified by exact integer powers; Decimal is only a proposal','prices':prices,'new_complete_kappa':False}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
