#!/usr/bin/env python3
"""Independent exact source geometry for the nine-packet no-line gate.

Enumerates binary charts by unique reduced bases, independently of author
files. E6/A2 and D6/A1^2 planes are rebuilt from actual integer source roots.
The inherited root-system completeness theorem is a separate proof premise.
"""
import argparse
import collections
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

SOURCE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
FULL = 'd9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'


def need(test,message):
    if not test:raise ValueError(message)


def root(n):
    if n.bit_count()==3:return tuple(2 if n>>j&1 else -1 for j in range(9))
    need(n.bit_count()==7,'Source root normal')
    p,q=[j for j in range(9) if not n>>j&1]
    return tuple(3*((j==p)-(j==q)) for j in range(9))


def dot(a,b):return sum(x*y for x,y in zip(a,b))


def binary_rank(rows):
    basis={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p not in basis:basis[p]=row;break
            row^=basis[p]
    return len(basis)


def rational_rank(rows):
    pivots={}
    for raw in rows:
        row=[F(x) for x in raw]
        for p,old in sorted(pivots.items()):
            if row[p]:
                scale=row[p];row=[x-scale*y for x,y in zip(row,old)]
        p=next((i for i,x in enumerate(row) if x),None)
        if p is not None:
            scale=row[p];pivots[p]=[x/scale for x in row]
    return len(pivots)


def power(r,bits=128):
    den=1<<bits;target=r**199*den**200
    low,high=0,r*den+1
    while high-low>1:
        mid=(low+high)//2
        if mid**200<=target:low=mid
        else:high=mid
    need(low**200<=target<(low+1)**200,'Directed power enclosure')
    return F(low,den),F(low if low**200==target else low+1,den)


def moment(profile):
    low=high=F(0)
    for r,c in profile.items():
        a,b=power(r)
        low+=c*(a if c>=0 else b);high+=c*(b if c>=0 else a)
    return low,high


def normalize_pair(a,b):
    if a==b==0:return (0,0)
    d=math.gcd(a,b);a//=d;b//=d
    if a<0 or (a==0 and b<0):a,b=-a,-b
    return a,b


def main(args):
    raw=(args.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==SOURCE,'Source pin')
    source=json.loads(gzip.decompress(raw))
    hosted=sorted(source['live'][j] for j in source['hosted']['Dports'])
    normals={i:source['frames'][source['initial'][i]][0] for i in hosted}
    roots={n:root(n) for n in range(512) if n.bit_count() in (3,7)}
    need(len(hosted)==96 and len(roots)==120,'Source populations')
    masks={v:sum(1<<j for j,i in enumerate(hosted) if not ((v&normals[i]).bit_count()&1))
           for v in range(1,512)}
    chart_results={}
    for dim,expected in [(2,43435),(3,788035)]:
        counts=collections.Counter();witness=None;maximum=-1;total=0
        # Every binary subspace has a unique reduced basis with these leading
        # pivot bits. Nonpivot bits below each leading bit are exactly free.
        for pivots in itertools.combinations(range(9),dim):
            options=[]
            for pivot in pivots:
                free=[j for j in range(pivot) if j not in pivots]
                options.append([(1<<pivot)|sum((1<<j) for k,j in enumerate(free) if mask>>k&1)
                                for mask in range(1<<len(free))])
            for basis in itertools.product(*options):
                support=(1<<96)-1
                for b in basis:support&=masks[b]
                count=support.bit_count();counts[count]+=1;total+=1
                if count>maximum:
                    maximum=count;witness={'basis':list(basis),'hosted_ports':[i for j,i in enumerate(hosted) if support>>j&1]}
        need(total==expected,'Complete unique reduced-chart census')
        need(maximum==35 if dim==2 else maximum<=24,'Source chart support cap')
        chart_results[str(dim)]={'count':total,'maximum_hosted_sources':maximum,
                                 'support_count_histogram':dict(sorted(counts.items())), 'maximum_witness':witness}
        print(json.dumps({'chart_dimension':dim,'count':total,'maximum':maximum}),flush=True)

    seen=set();census=collections.Counter();candidates=[];flat_max={'E6':0,'D6':0}
    for n,m in itertools.combinations(roots,2):
        inner=dot(roots[n],roots[m])
        if inner not in (-9,0,9):continue
        kind='D6' if inner==0 else 'E6'
        if kind=='E6':
            third=tuple(x-(1 if inner==9 else -1)*y for x,y in zip(roots[n],roots[m]))
            z=next(k for k,v in roots.items() if v==third or v==tuple(-x for x in third))
            key=(kind,*sorted((n,m,z)))
        else:key=(kind,n,m)
        if key in seen:continue
        seen.add(key)
        zero=[];groups={}
        for i in hosted:
            pair=normalize_pair(dot(roots[normals[i]],roots[n]),dot(roots[normals[i]],roots[m]))
            if pair==(0,0):zero.append(i)
            else:groups.setdefault(pair,[]).append(i)
        flat_max[kind]=max(flat_max[kind],len(zero));census[(kind,len(groups))]+=1
        # Every pair-complement has the asserted full E6/D6 root population.
        allzero=[v for v in roots.values() if dot(v,roots[n])==dot(v,roots[m])==0]
        need(len(allzero)==(36 if kind=='E6' else 30),'Full complement population')
        if len(groups)<=3:
            need(kind=='E6' and rational_rank(allzero)==6,'Candidate zero-flat rank')
            group_records=[]
            for direction,ports in sorted(groups.items()):
                br=binary_rank([normals[i] for i in ports]);need(br==7,'Candidate physical group rank')
                group_records.append({'projective_direction':list(direction),'ports':ports,'size':len(ports),'binary_normal_rank':br})
            nonzero=96-len(zero)
            price={9:6,7:3,2:nonzero,6:nonzero,8:-nonzero}
            lo,hi=moment(price)
            candidates.append({'kind':kind,'normal_pair':[n,m],'plane_root_normals':list(key[1:]),
                               'zero_ports':zero,'groups':group_records,
                               'acquisition_refinement_profile':price,'price_bounds':[str(lo),str(hi)]})
    need(sum(v for (kind,_),v in census.items() if kind=='E6')==1120,'E6 complement census')
    need(sum(v for (kind,_),v in census.items() if kind=='D6')==3780,'D6 complement census')
    need(len(candidates)==6,'Exactly six low-direction candidates')
    print(json.dumps({'plane_census':{str(k):v for k,v in sorted(census.items())},'candidates':6}),flush=True)

    fullraw=(args.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes()
    need(hashlib.sha256(fullraw).hexdigest()==FULL,'Complete caller pin')
    full=json.loads(fullraw)
    t={int(k):v for k,v in full['invoice']['T'].items()};p={int(k):v for k,v in full['invoice']['P'].items()}
    n={int(k):v for k,v in full['native']['paid'].items()};h={int(k):v for k,v in full['native']['helpers'].items()}
    allowance={r:F(n.get(r,0)-h.get(r,0))+F(t.get(r,0)-p.get(r,0),18) for r in set(t)|set(p)|set(n)|set(h)}
    for r,c in {8:400,9:8,1:8}.items():allowance[r]=allowance.get(r,F(0))-c
    allowlo,allowhi=moment(allowance)
    gates={}
    for z,mass in [(6,18),(7,9)]:
        signed={9:F(z),7:F(mass,7)}
        for r,c in allowance.items():signed[r]=signed.get(r,F(0))-c
        lo,hi=moment(signed);need(lo>0,'Rank-mass infeasibility gate')
        gates[str(z)]={'forbidden_local_rank_mass_at_least':mass,'deficit_bounds':[str(lo),str(hi)]}
    lo,hi=moment({**{r:-c for r,c in allowance.items()},9:F(8)-allowance.get(9,F(0))})
    need(lo>0,'Eight zero-born packets already exceed remaining budget')
    caps={1:1,2:2,3:4,4:8,5:16,6:24,7:35}
    coverage={}
    for z,local,mass in [(6,3,17),(7,2,8)]:
        feasible=[x for x in itertools.product(range(1,8),repeat=local) if sum(x)<=mass]
        maximum=max(sum(caps[r] for r in x) for x in feasible)
        examples=[list(x) for x in feasible if sum(caps[r] for r in x)==maximum]
        coverage[str(z)]={'maximum_local_sources':maximum,'minimum_zero_only_sources':96-maximum,'maximizing_rank_tuples':examples}
    need(coverage['6']['maximum_local_sources']==74 and coverage['7']['maximum_local_sources']==36,'Exhaustive permissive rank-profile coverage')
    best=min(candidates,key=lambda c:F(c['price_bounds'][0]))
    # Build a separate nine-row positive witness, choosing the zero-flat basis
    # in reverse source order rather than importing the author's matrix.
    selected=[]
    for i in reversed(best['zero_ports']):
        if rational_rank([roots[normals[j]] for j in selected+[i]])>len(selected):selected.append(i)
        if len(selected)==6:break
    need(len(selected)==6,'Independent E6 basis for positive witness')
    witness=[[F(dot(roots[normals[i]],roots[normals[j]]),18) for j in hosted] for i in selected]
    aa,bb=best['normal_pair']
    for group in best['groups']:
        x,y=group['projective_direction'];ports=set(group['ports'])
        witness.append([F(dot(roots[normals[j]],roots[aa]),18*x) if j in ports and x
                        else F(dot(roots[normals[j]],roots[bb]),18*y) if j in ports else F(0)
                        for j in hosted])
    target=[[roots[normals[j]][k] for j in hosted] for k in range(9)]
    need(rational_rank(witness)==9 and rational_rank(witness+target)==9,'Independent positive nine-row acquisition witness')
    witness_control=witness[:6]+witness[7:]
    need(rational_rank(witness_control+target)>rational_rank(witness_control),'Delete one fiber loses target containment')
    result={'status':'PASS_ROOT_NINE_NO_LINE_SOURCE_PREMISES','native_sha256':SOURCE,'complete_caller_sha256':FULL,
            'chart_census':chart_results,'plane_direction_census':{str(k):v for k,v in sorted(census.items())},
            'source_complement_maxima':flat_max,'six_candidates':candidates,'best_candidate_pair':best['normal_pair'],
            'limiting_return_allowance_bounds':[str(allowlo),str(allowhi)],'rank_mass_gates':gates,
            'eight_zero_born_deficit_bounds':[str(lo),str(hi)],'source_coverage_gates':coverage,
            'independent_positive_witness':{'hosted_order':hosted,'E6_basis_roles':selected,
                                             'packet_rows':[[str(x) for x in row] for row in witness],
                                             'packet_rank':9,'rank_after_target_stacking':9,
                                             'deleted_fiber_packet_rank':rational_rank(witness_control),
                                             'deleted_fiber_with_target_rank':rational_rank(witness_control+target)},
            'negative_controls':{'generic_binary_caps_without_source_census':{6:32,7:64},
                                 'candidate_exact_but_over_budget':best['normal_pair']},
            'proof_dependencies':'General arbitrary-V quotient theorem, E8 rank<=5 root counts and rank6 >=22 classification/E8 complement lattice theorem are separately reviewed proof premises; this computation does not replace them.',
            'scope':'Nine fresh single-birth packets, unchanged raw paths, no useful Hub side information, no one-dimensional nonzero birth charts. No new kappa.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'best_candidate_pair':best['normal_pair'],
                      'best_price_approx':float(F(best['price_bounds'][0])),'allowance_approx':float(allowlo)}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args())
