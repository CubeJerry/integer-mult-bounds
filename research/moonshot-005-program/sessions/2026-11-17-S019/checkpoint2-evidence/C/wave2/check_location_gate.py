#!/usr/bin/env python3
"""Exact source-chart coverage obstruction for departures containing M1.

Own native interpreter dependency is the separately reviewed portable audit.
No previous source/port census or optimization result is trusted.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def demand(p,message):
    if not p:raise ValueError(message)


def row_basis(rows):
    rows=[list(map(Fraction,r))for r in rows];k=0
    for column in range(5):
        pivot=next((i for i in range(k,len(rows))if rows[i][column]),None)
        if pivot is None:continue
        rows[k],rows[pivot]=rows[pivot],rows[k];v=rows[k][column];rows[k]=[x/v for x in rows[k]]
        for i in range(len(rows)):
            if i!=k and rows[i][column]:
                v=rows[i][column];rows[i]=[x-v*y for x,y in zip(rows[i],rows[k])]
        k+=1
    return tuple(tuple(r)for r in rows[:k])


def census(points,r):
    # Every maximal intersection with an r-dimensional subspace is dominated by
    # one spanned by r actual points, because the full point set spans dimension5.
    found={}
    for inds in combinations(range(len(points)),r):
        B=row_basis([points[i]for i in inds])
        if len(B)!=r or B in found:continue
        found[B]=tuple(j for j,p in enumerate(points)if len(row_basis(list(B)+[p]))==r)
    return found


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=p.parse_args()
    spec=importlib.util.spec_from_file_location('independent_cp6_audit',a.audit_module);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    path=a.evidence/'A/local-canonical9-source/WORD.json';raw=path.read_bytes();demand(hashlib.sha256(raw).hexdigest()=='3643c6db33ce5ed1ea61724b126a8a3cad28be0c728376193b1f11fbf0457565','exact source word');w=json.loads(raw);src=a.repo/w['source_path'];source=json.loads(src.read_text());demand(m.sha(src)==w['source_sha256'],'published recovered native source pin')
    cut=w['carrier_interface_before_operation'];stats,snaps,C,events=m.replay(w,source,[cut]);v,loc=snaps[cut];U=sorted(set(range(111))-set(w['targets']));M=C['M1'];R=source['native_roots'];demand(len(M)==5 and len(U)==63,'source dimensions')
    own=[]
    for i in U:
        visible=[n for n,z in v.items()if i in z and m.subset(C[loc[n]],C[f'F{i}'])]
        demand(not visible,('no initial own-coordinate information',i));own.append(i)
    groups=defaultdict(list)
    for i in U:
        restricted=tuple(sum(x*y for x,y in zip(R[i],b))for b in M)
        B=row_basis([restricted]);demand(len(B)==1,'no unknown facet contains M1');groups[B[0]].append(i)
    points=sorted(groups);demand(len(points)==20 and len(row_basis(points))==5,'exact20 spanning projective directions')
    allflats={};maxima={};hist={}
    for r in range(1,5):
        f=census(points,r);allflats[r]=f;maxima[r]=max(map(len,f.values()));hist[r]=dict(sorted(Counter(map(len,f.values())).items()))
    demand(maxima=={1:1,2:3,3:7,4:12},'exact small-flat capacities')
    # Exact rational comparison, not floating optimization.
    q=m.moment(stats['movement_profile']);bound=m.moment({1:8,4:1});p3=m.power_interval(3);p2=m.power_interval(2)
    a3=((p3[0]-1)/6,(p3[1]-1)/6)
    demand(p2[0]-1>=2*a3[1],'rank2 price slope lower bound')
    demand(0<a3[0] and a3[1]<1,'positive slope below1')
    all_small=(9+11*a3[0],9+11*a3[1]);demand(all_small[0]>bound[1],'all rank<=3 departures cost strictly more')
    # A genuine coverage-only witness: one rank4 descent plus eight unit ones.
    B,hits=next((B,h)for B,h in allflats[4].items()if len(h)==12)
    omitted=[i for i in range(20)if i not in hits]
    demand(len(omitted)==8,'coverage-only nine-port witness')
    cover=set(hits)|set(omitted);demand(cover==set(range(20)),'complete projective coverage')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    allow=tuple(x/6 for x in m.moment(gate));excess=(q[0]+bound[0]-allow[1],q[1]+bound[1]-allow[0]);demand(excess[0]>0,'source plus location floor exceeds necessary allowance')
    controls=[]
    # Concrete counterexample to omitting the departure-chart hypothesis:
    # descend actual raw5 from its native line to ground, which is below all
    #63 facets and therefore all20 classes. Origin L5 does not contain M1.
    demand(not m.subset(M,C['L5'])and all(m.subset(C['zero'],C[f'F{i}'])for i in U),'outside-scope native-cache descent control')
    controls.append({'kind':'native_unit_descent_outside_hypothesis','source':'L5','destination':'zero','geometric_classes_reached':20,'M1_contained_in_departure':False,'payload_does_not_complete_all_targets':True})
    # A lower departure can span multiple classes at unit price; it genuinely
    #violates the hypothesis, not the proof.
    B2,hit2=next((B,h)for B,h in allflats[2].items()if len(h)==3)
    controls.append({'kind':'rank4_to_rank3_relay_outside_hypothesis','three_possible_final_classes':list(hit2),'required_fresh_information_not_supplied':True})
    result={'status':'PASS_SOURCE_LOCATION_TWENTY_CLASSES_AND_DIRECT_DEPARTURE_COST_GATE','word_sha256':m.sha(path),'native_source_sha256':m.sha(src),'cut':cut,'all63_initial_own_access_absent':own,'source_chart':'M1','source_dimension':5,'projective_classes':[{'index':i,'normal':[str(x)for x in point],'receivers':groups[point]}for i,point in enumerate(points)],'flat_counts':{r:len(f)for r,f in allflats.items()},'flat_capacity_histograms':hist,'max_classes_by_rank_drop':maxima,'all_unit_departure_floor':20,'nonlinear_transcript_message_lower_bound_dependency':'S019 exact Petersen+four-isolates entropy certificate','movement_floor':{'formula':'8 + 4^(199/200)','interval':m.interval_json(bound)},'all_rank_at_most_three_relaxation_floor':{'formula':'9 + 11*(3^(199/200)-1)/6','interval':m.interval_json(all_small)},'source_plus_floor_excess':m.interval_json(excess),'coverage_only_witness':{'rank4_normal_space_basis':[[str(x)for x in r]for r in B],'rank4_port_covered_classes':list(hits),'eight_rank1_port_classes':omitted,'physical_decoding_claimed':False},'negative_scope_controls':controls,'scope':'Every future downward transfer must depart a real chart containing initial M1; arbitrary fixed-schedule nonlinear co-chart computation and original-Y feedback allowed. This includes Hub departures but excludes lower-chart/native departures. Every whole-record transfer and any enlarged alphabet must be charged. The invoice bound is a necessary movement bound only; abstract coverage feasibility is not decoding.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'LOCATION-GATE-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    flatout={r:[{'basis':[[str(x)for x in row]for row in B],'classes':list(hits)}for B,hits in f.items()]for r,f in allflats.items()};(a.out/'EXACT-FLAT-CENSUS.json').write_text(json.dumps(flatout,indent=2)+'\n')
    print(result['status']);print('20 classes; capacities1,3,7,12; location movement floor',result['movement_floor']['interval']['decimal']);print('excess',result['source_plus_floor_excess']['decimal'])
if __name__=='__main__':main()
