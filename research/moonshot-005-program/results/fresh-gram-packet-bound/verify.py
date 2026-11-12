#!/usr/bin/env python3
"""Exact source, polynomial, all-volume packet-gate and tariff verification."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip, hashlib, itertools, json, math
from pathlib import Path

SOURCE_PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
INVOICE_PIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
FRAME1=[7,25,42,52,76,82,97,127]
FRAME2=[67,104,137,162,266,289,448,491]
DEN=10**24

def need(ok,message):
    if not ok: raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def root(v):
    present=[i for i in range(9) if v>>i&1]
    if len(present)==3:
        return [2*int(i in present) for i in range(8)] if 8 in present else [1 if i in present else -1 for i in range(8)]
    need(len(present)==7,'root normal weight')
    i,j=[i for i in range(9) if not v>>i&1]
    return [1 if k==i else -1 for k in range(8)] if j==8 else [2*((k==i)-(k==j)) for k in range(8)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def span(frame):
    out={0}
    for x in frame:out|={x^y for y in tuple(out)}
    return out

def row_basis(rows):
    echelon={};indices=[]
    for k,row in enumerate(rows):
        r=list(map(F,row))
        for j in sorted(echelon):
            if r[j]:
                q=r[j];r=[a-q*b for a,b in zip(r,echelon[j])]
        pivot=next((j for j,a in enumerate(r) if a),None)
        if pivot is not None:
            q=r[pivot];echelon[pivot]=[a/q for a in r];indices.append(k)
        if len(indices)==len(row):break
    return indices,sorted(echelon)

def determinant(A):
    A=[list(map(F,row)) for row in A];n=len(A);out=F(1)
    need(all(len(row)==n for row in A),'square determinant')
    for j in range(n):
        p=next((i for i in range(j,n) if A[i][j]),None)
        if p is None:return F(0)
        if p!=j:A[j],A[p]=A[p],A[j];out=-out
        t=A[j][j];out*=t;A[j]=[x/t for x in A[j]]
        for i in range(j+1,n):
            t=A[i][j]
            if t:A[i]=[a-t*b for a,b in zip(A[i],A[j])]
    return out

def compositions(total,length):
    if length==1:
        yield (total,);return
    for i in range(total+1):
        for rest in compositions(total-i,length-1):yield (i,)+rest

def multinomial(n,e):
    out=math.factorial(n)
    for k in e:out//=math.factorial(k)
    return out

def polynomial_moments(all_roots):
    checks=0
    for degree,constant in [(2,120),(4,288),(6,960)]:
        for exponents in compositions(degree,8):
            coefficient=multinomial(degree,exponents)*sum(math.prod(x**e for x,e in zip(a,exponents)) for a in all_roots)
            expected=constant*multinomial(degree//2,[e//2 for e in exponents]) if all(e%2==0 for e in exponents) else 0
            need(coefficient==expected,'exact moment polynomial coefficient')
            checks+=1
    return checks

def cap(r):return min(2**(r-1),96)
def relaxed_checks(ranks,distance=37,cover=True):
    if len(ranks)<8:return False
    capacities=[cap(r) for r in sorted(ranks)]
    return (not cover or sum(capacities)>=96) and sum(capacities[:len(ranks)-7])>=distance

def enumerate_histograms(budget):
    counts={'histograms_at_least8':0,'cover_pass':0,'distance_pass':0,'both_pass':0}
    best_distance_coverage=0;best_hist=None
    def visit(left,r,ranks):
        nonlocal best_distance_coverage,best_hist
        if r==10:
            if len(ranks)<8:return
            counts['histograms_at_least8']+=1
            capacities=[cap(v) for v in ranks]
            cover=sum(capacities)>=96;distance=sum(capacities[:len(ranks)-7])>=37
            counts['cover_pass']+=int(cover);counts['distance_pass']+=int(distance);counts['both_pass']+=int(cover and distance)
            if distance and sum(capacities)>best_distance_coverage:
                best_distance_coverage=sum(capacities);best_hist=dict(sorted(Counter(ranks).items()))
            return
        for k in range(left//r+1):visit(left-k*r,r+1,ranks+[r]*k)
    visit(budget,1,[])
    return {'rank_budget':budget,**counts,'max_coverage_if_distance_passes':best_distance_coverage,'max_coverage_histogram':best_hist}

def root_power_bounds(r):
    target=r**199*DEN**200
    lo,hi=0,r*DEN+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    need(lo**200<=target<(lo+1)**200,'directed integer power bracket')
    return F(lo,DEN),F(lo+1,DEN)

def interval(coefficients,powers):
    lo=hi=F(0)
    for r,c in coefficients.items():
        l,h=powers[r]
        lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
    return lo,hi

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes()
    need(sha(sb)==SOURCE_PIN and sha(ib)==INVOICE_PIN,'source and complete invoice pins')
    s=json.loads(gzip.decompress(sb));invoice=json.loads(ib)
    hosted=[s['live'][i] for i in s['hosted']['Dports']]
    normals={x:s['frames'][s['initial'][x]][0] for x in hosted};roots={x:root(normals[x]) for x in hosted}
    need(len(hosted)==96 and len(set(normals.values()))==96,'96 distinct hosted normal vectors')
    all_normals=[v for v in range(512) if v.bit_count() in (3,7)]
    all_roots=[root(v) for v in all_normals]
    omitted=set(all_normals)-set(normals.values())
    need(len(all_normals)==120 and len(omitted)==24,'full and omitted root sets')
    for frame in (FRAME1,FRAME2):
        need(set(frame)<=omitted and len(set(frame))==8,'eight omitted source roots')
        need([[dot(root(x),root(y)) for y in frame] for x in frame]==[[8*int(i==j) for j in range(8)] for i in range(8)],'orthogonal omitted frame')
    need(set(FRAME1).isdisjoint(FRAME2),'disjoint omitted frames')
    moment_checks=polynomial_moments(all_roots)
    need(moment_checks==2082,'all moment coefficients checked')
    # Polynomial coefficient identities, in ascending coefficient order.
    p=[F(0),F(9,8),F(-3,8),F(1,32)]
    need([F(1)-p[0],-p[1],-p[2],-p[3]]==[F(1),F(-9,8),F(3,8),F(-1,32)],'1-p factor coefficients')
    need([F(10,32)-p[0],F(15,32)-p[1],-p[2],-p[3]]==[F(10,32),F(-21,32),F(12,32),F(-1,32)],'tangent factor coefficients')
    full_p=F(9,8)*120-F(3,8)*288+F(1,32)*960
    hosted_p=full_p-2*F(25,4)-8
    need(full_p==57 and hosted_p==F(73,2) and math.ceil(hosted_p)==37,'universal support bound')
    witnesses=[];rank_hist=Counter()
    for z in range(1,512):
        excluded=[x for x in hosted if (normals[x]&z).bit_count()%2]
        rows=[roots[x] for x in excluded];pivots,columns=row_basis(rows);r=len(pivots)
        minor=[[rows[i][j] for j in columns] for i in pivots]
        det=determinant(minor);need(det!=0,'source locality nonzero minor')
        rank_hist[r]+=1
        record={'direction':z,'excluded_count':len(excluded),'rank':r,'basis_ports':[excluded[i] for i in pivots],'minor_columns':columns,'minor_determinant':str(det)}
        if z in omitted:
            need(r==7 and all(dot(root(z),row)==0 for row in rows),'exact exceptional annihilator')
            record['annihilator']=root(z)
        else:need(r==8,'all other directions exclude full root rank')
        witnesses.append(record)
    need(rank_hist=={8:487,7:24},'complete 511-direction classification')
    need(all(abs(dot(root(x),root(y)))<8 for x in omitted for y in omitted if x!=y),'distinct exceptional annihilator lines')
    for x,y in zip(hosted,s['hosted']['Y2']):
        frame=s['frames'][s['final'][y]]
        need(len(frame)==8 and all((normals[x]&v).bit_count()%2==0 for v in frame),'actual Y2 orthogonal final facet')
    exhaustive=enumerate_histograms(47)
    need(exhaustive['both_pass']==0 and exhaustive['max_coverage_if_distance_passes']==51,'integer rank48 floor corroboration')
    need(relaxed_checks([4]*12) and sum([4]*12)==48,'numerical relaxation attainment only')
    # Essential-premise controls.
    weakened=[1]+[5]*9
    need(relaxed_checks(weakened,distance=33) and not relaxed_checks(weakened),'support37 changes bounded feasibility')
    need(relaxed_checks([1]*44,cover=False) and not relaxed_checks([1]*44),'source coverage is essential')
    need(not set([normals[hosted[0]]]+FRAME1[1:])<=omitted or len(set([normals[hosted[0]]]+FRAME1[1:]))!=8 or [[dot(root(x),root(y)) for y in [normals[hosted[0]]]+FRAME1[1:]] for x in [normals[hosted[0]]]+FRAME1[1:]]!=[[8*int(i==j) for j in range(8)] for i in range(8)],'changed frame negative control')
    raw_roles=set(s['live'])|{x+112 for x in s['live']}|set(s['hosted']['X2'])|set(s['hosted']['Y2'])
    need(len(raw_roles)==400,'all 400 raw roles')
    for role in raw_roles:
        first=s['frames'][s['initial'][role]];last=s['frames'][s['final'][role]]
        need(len(last)-len(first)==8 and span(first)<=span(last),'legitimate optimistic direct raw ascent')
    old=Counter(abs(len(s['frames'][op[3]])-len(s['frames'][op[2]])) for op in s['program'] if op[0]=='MOVE' and op[1] in raw_roles)
    need(dict(sorted(old.items()))=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'actual source raw histogram')
    need(sum(old.values())==1710 and sum(r*n for r,n in old.items())==3200,'raw count and rank mass')
    T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
    for r,n in old.items():P[r]-=18*n
    P[8]+=18*400;P[9]+=18*8
    need(all(n>=0 for n in P.values()),'optimistic complete paid invoice remains nonnegative')
    powers={r:root_power_bounds(r) for r in set(T)|set(P)|{9}}
    lower,upper=interval({r:T[r]-P[r] for r in set(T)|set(P)},powers);lower/=18;upper/=18
    cost_lower=F(16,3)*powers[9][0];cost_upper=F(16,3)*powers[9][1]
    need(cost_lower>upper,'strict complete target obstruction')
    result={'status':'PASS_SOURCE_GRAM_RETURN_PACKET_OBSTRUCTION','source_sha256':SOURCE_PIN,'invoice_sha256':INVOICE_PIN,'all_field_volumes':True,'arbitrary_linear_coordinate_mixing':True,'complete_new_kappa':None,'hosted_source_count':96,'packet_demand_dimensions_per_field':8,'full_projective_root_count':120,'omitted_root_count':24,'omitted_frames':[FRAME1,FRAME2],'polynomial_coefficients_checked':moment_checks,'full_p_sum':'57','hosted_p_sum_lower':str(hosted_p),'minimum_source_block_support':37,'locality_rank_histogram':dict(sorted(rank_hist.items())),'exhaustive_rank_histogram_check':exhaustive,'rank_mass_floor':48,'numerical_relaxation_attainer':{'4':12},'scope':'Fresh single-cochart raw-source packets, no useful Y-dependent hub side information or funded transport. The rank48 relaxation attainer is not a constructed packet code. No new kappa.','negative_controls':['weakened support33 admits rank46 histogram','dropping total96 coverage admits44 rank1 packets','altered omitted frame rejected','all nonexceptional source directions have exact rank8 witnesses'],'optimistic_complete_caller':{'T4':dict(sorted(T.items())),'P_best':dict(sorted(P.items())),'raw_histogram':{'8':400},'retained_forward_packets':{'9':8},'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in set(T)|set(P)),'headroom_lower':str(lower),'headroom_upper':str(upper),'packet_cost_lower':str(cost_lower),'packet_cost_upper':str(cost_upper),'deficit_per_native_lower':str(cost_lower-upper),'deficit_per_native_upper':str(cost_upper-lower),'deficit_18_native_lower':str(18*(cost_lower-upper))},'power_denominator':DEN}
    locality={'source_sha256':SOURCE_PIN,'hosted_ports':hosted,'normal_vectors':normals,'root_rows':roots,'omitted_vectors':sorted(omitted),'witnesses':witnesses}
    a.output.mkdir(parents=True,exist_ok=True)
    for name,obj in [('RESULT.json',result),('LOCALITY.json',locality)]: (a.output/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'support_floor':37,'rank_floor':48,'histograms_checked':exhaustive['histograms_at_least8'],'headroom_interval':[str(lower),str(upper)],'packet_cost_interval':[str(cost_lower),str(cost_upper)],'deficit_per_native_lower':str(cost_lower-upper)},indent=2))
if __name__=='__main__':main()
