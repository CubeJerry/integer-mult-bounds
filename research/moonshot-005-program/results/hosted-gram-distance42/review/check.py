#!/usr/bin/env python3
"""Independent distance42/root chamber and changed-tariff review.

Does not import the author's verifier, coefficient tables or reflection census.
"""
import argparse,gzip,hashlib,itertools,json,math
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'

def require(q,msg):
    if not q:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def scalar(x,y):return sum(a*b for a,b in zip(x,y))
def inverse(A):
    n=len(A);M=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        p=next(i for i in range(j,n) if M[i][j]);M[j],M[p]=M[p],M[j];c=M[j][j];M[j]=[x/c for x in M[j]]
        for i in range(n):
            if i!=j:
                c=M[i][j]
                if c:M[i]=[x-c*y for x,y in zip(M[i],M[j])]
    return [r[n:] for r in M]
def native_root(v):
    ones={i for i in range(9) if (v>>i)&1}
    if len(ones)==3:
        if 8 in ones:return tuple(2*int(i in ones) for i in range(8))
        return tuple(1 if i in ones else -1 for i in range(8))
    require(len(ones)==7,'source weight3 or7');i,j=sorted(set(range(9))-ones)
    if j==8:return tuple(1 if k==i else -1 for k in range(8))
    return tuple(2*int(k==i)-2*int(k==j) for k in range(8))
def binary_span(vectors):
    points={0}
    for v in vectors:points|={v^w for w in tuple(points)}
    return points

def integer_partition_review():
    capacity={r:min(1<<(r-1),96) for r in range(1,10)}
    count49=passes49=0;passed50=[]
    def traverse(r,remaining,counts):
        nonlocal count49,passes49
        if r==10:
            mass=sum(i*c for i,c in counts.items());m=sum(counts.values())
            if m<8:return
            if mass<=49:count49+=1
            ranks=[i for i,c in counts.items() for _ in range(c)];ranks.sort()
            yes=sum(capacity[i] for i in ranks)>=96 and sum(capacity[i] for i in ranks[:m-7])>=42
            if mass<=49:passes49+=int(yes)
            elif yes:passed50.append(counts.copy())
            return
        for c in range(remaining//r+1):
            if c:counts[r]=c
            else:counts.pop(r,None)
            traverse(r+1,remaining-c*r,counts)
        counts.pop(r,None)
    traverse(1,50,{})
    require(count49==321728 and passes49==0,'independent count-vector rank49 enumeration')
    require(len(passed50)==3 and all(x in passed50 for x in ({5:10},{2:1,4:12},{1:2,4:12})),'only three exact mass50 histograms')
    # Independent unbounded-knapsack bounds for the small-rank side of the proof.
    dp=[]
    for largest in range(2,7):
        budget=49-7*largest;table=[0]*(budget+1)
        for b in range(1,budget+1):table[b]=max([table[b-1]]+[table[b-r]+capacity[r] for r in range(1,min(largest,b)+1)])
        require(table[budget]<42,'analytic h-case independently corroborated')
        dp.append({'largest_small_rank':largest,'small_rank_budget':budget,'maximum_capacity':table[budget]})
    return {'histograms_rank_at_most49':count49,'passing_at_most49':passes49,'passing_at_exact50':passed50,'independent_knapsack_bounds':dp}

def power(rank):
    denominator=1<<120;target=pow(rank,199)*pow(denominator,200);lower=0;upper=rank*denominator+1
    while lower+1<upper:
        center=(lower+upper)//2
        if pow(center,200)<=target:lower=center
        else:upper=center
    require(pow(lower,200)<=target<pow(lower+1,200),'independent dyadic power bounds')
    return Q(lower,denominator),Q(lower+1,denominator)
def signed_sum(coefficients,powers):
    lower=upper=Q(0)
    for r,c in coefficients.items():
        lo,hi=powers[r];lower+=c*(lo if c>=0 else hi);upper+=c*(hi if c>=0 else lo)
    return lower,upper

def main(a):
    sourcebytes=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    invoicebytes=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes()
    require(digest(sourcebytes)==SPIN and digest(invoicebytes)==IPIN,'immutable actual source and invoice')
    source=json.loads(gzip.decompress(sourcebytes));invoice=json.loads(invoicebytes)
    # Generate the standard signed240 roots independently of source normal labels.
    phi=set()
    for i in range(8):
        for j in range(i+1,8):
            for si in (-2,2):
                for sj in (-2,2):phi.add(tuple(si*int(k==i)+sj*int(k==j) for k in range(8)))
    for signs in itertools.product((-1,1),repeat=8):
        if signs.count(-1)%2:phi.add(signs)
    require(len(phi)==240 and all(scalar(r,r)==8 for r in phi),'independent240-root set')
    normals=[v for v in range(512) if v.bit_count() in(3,7)];projective={v:native_root(v) for v in normals}
    require({r for v in projective.values() for r in (v,tuple(-x for x in v))}==phi,'independent source root isometry')
    # Construct simple rows geometrically, and derive all duals by elimination.
    alpha=[(1,)+(-1,)*7,(2,2)+(0,)*6,(-2,2)+(0,)*6]
    for i in range(1,6):alpha.append(tuple(-2*int(k==i)+2*int(k==i+1) for k in range(8)))
    require(len(alpha)==8 and all(r in phi for r in alpha),'geometric simple basis')
    dual=[tuple(c) for c in zip(*inverse(alpha))]
    require([[scalar(x,y) for y in alpha] for x in dual]==[[int(i==j) for j in range(8)] for i in range(8)],'derived dual basis')
    coordinates={r:tuple(scalar(w,r) for w in dual) for r in phi}
    require(all(all(c.denominator==1 for c in row) and (all(c>=0 for c in row) or all(c<=0 for c in row)) for row in coordinates.values()),'all240 integral uniform-sign coordinates')
    require(all(tuple(sum(c*alpha[i][k] for i,c in enumerate(coordinates[r])) for k in range(8))==r for r in phi),'independent simple reconstruction')
    reflection_checks=0
    for simple in alpha:
        reflected={tuple(Q(r[k])-Q(scalar(r,simple),4)*simple[k] for k in range(8)) for r in phi}
        require(reflected==phi,'every simple reflection is a full root permutation');reflection_checks+=len(phi)
    deletions=[]
    for j in range(8):
        tw=sum(coordinates[r][j]==0 and sum(bool(x) for x in r)==2 for r in phi)//2
        sg=sum(coordinates[r][j]==0 and all(abs(x)==1 for x in r) for r in phi)//2
        deletions.append({'index':j+1,'two_coordinate_pairs':tw,'sign_pairs':sg,'total':tw+sg})
    require([x['total'] for x in deletions]==[42,28,22,14,16,23,37,63],'node-deletion census')
    require(tuple(4*x for x in dual[7]) in phi,'unique exceptional dual is a root direction')
    H=[source['live'][i] for i in source['hosted']['Dports']];vectors={h:source['frames'][source['initial'][h]][0] for h in H}
    require(len(H)==96 and len(set(vectors.values()))==96,'actual96 hosted source normals')
    census=[]
    for v,r in projective.items():
        support=[h for h in H if scalar(r,projective[vectors[h]])]
        census.append({'normal':v,'support':len(support),'hosted_roles':support})
    require(min(x['support'] for x in census)==42 and [x['normal'] for x in census if x['support']==42]==[38,191],'exact source distance witnesses')
    chamber=json.loads((a.author/'output/CHAMBER.json').read_text());author_result=json.loads((a.author/'output/RESULT.json').read_text())
    require(census==chamber['source_supports'],'all120 source support lists match independently')
    require([[str(x) for x in row] for row in dual]==[[str(Q(x,4)) for x in row] for row in chamber['dual_simple_normals_times4']],'independently derived duals agree')
    partitions=integer_partition_review()
    # Source-matched complete tariffs, using dyadic instead of author decimal bounds.
    raw=set(source['live'])|{x+112 for x in source['live']}|set(source['hosted']['X2'])|set(source['hosted']['Y2'])
    require(len(raw)==400,'raw field inventory')
    for x in raw:
        first=source['frames'][source['initial'][x]];last=source['frames'][source['final'][x]]
        require(len(last)-len(first)==8 and binary_span(first)<=binary_span(last),'each direct raw ascent is a valid optimistic grant')
    old=Counter(abs(len(source['frames'][e[3]])-len(source['frames'][e[2]])) for e in source['program'] if e[0]=='MOVE' and e[1] in raw)
    T=Counter({int(k):v for k,v in invoice['T4'].items()});Pdirect=Counter({int(k):v for k,v in invoice['P4'].items()})
    for r,c in old.items():Pdirect[r]-=18*c
    Pdirect[8]+=18*400
    powers={r:power(r) for r in set(T)|set(Pdirect)|{1,2,4,5,7,8,9}}
    price_low,price_high=10*powers[5][0],10*powers[5][1]
    require(price_high<12*powers[4][0]+powers[2][0] and price_high<12*powers[4][0]+2,'strict relaxed minimum10rank5')
    require(51**200*5>50**200*9,'all higher rank masses cost more')
    tariffs={}
    for name,packets in [('eight_rank9',{9:8}),('two_late_with_all_raw_refinements_free',{9:6,8:1,7:1,1:1})]:
        P=Pdirect.copy()
        for r,c in packets.items():P[r]+=18*c
        lo,hi=signed_sum({r:T[r]-P[r] for r in set(T)|set(P)},powers);lo/=18;hi/=18
        require(price_low>hi,'freshpacket theorem defeats complete favorable tariff '+name)
        tariffs[name]={'paid_positions':sum(P.values()),'targets':sum(T.values()),'headroom_lower':str(lo),'headroom_upper':str(hi),'packet_histogram':packets,'fresh_return_price_lower':str(price_low),'fresh_return_price_upper':str(price_high),'deficit_lower':str(price_low-hi),'deficit_upper':str(price_high-lo)}
    oldtariff=tariffs['eight_rank9'];require(Q(author_result['favorable_caller']['remaining_moment_lower'])<=Q(oldtariff['headroom_lower'])<=Q(oldtariff['headroom_upper'])<=Q(author_result['favorable_caller']['remaining_moment_upper']),'dyadic independent tariff refines author interval')
    require(Q(author_result['packet_moment_lower'])<=price_low<=price_high<=Q(author_result['packet_moment_upper']),'independent exact price refines author interval')
    # Three separate mathematical failure modes, no author's mutant implementation.
    wrong_dual=list(dual);wrong_dual[7]=tuple(-x for x in wrong_dual[7])
    require(any(not(all(scalar(w,r)>=0 for w in wrong_dual) or all(scalar(w,r)<=0 for w in wrong_dual)) for r in phi),'mixed-sign chamber mutation detected')
    require(sum(scalar(dual[7],r)==0 for r in phi)==126,'root exception really has63 zero pairs')
    c0=[1]+[4]*12;require(sum(c0)==49 and sum(min(2**(r-1),96) for r in c0[:-7])==41,'one weaker distance unit invalidates rank50 gate')
    files=['PROOF.md','verify.py','output/RESULT.json','output/CHAMBER.json']
    report={'status':'PASS_INDEPENDENT_DISTANCE42_CHAMBER_AND_CHANGED_TARIFF_REVIEW','reviewed_author_files':{f:digest((a.author/f).read_bytes()) for f in files},'source_sha256':SPIN,'invoice_sha256':IPIN,'method':'Fresh geometric signed-root construction, duals derived by exact elimination, separate reflection/node census, actual hosted support lists, count-vector integer enumeration, dyadic power arithmetic; no author verifier imported or executed. Universal chamber proof reviewed analytically.','simple_duals':[[str(x) for x in row] for row in dual],'root_reflection_identities':reflection_checks,'deletion_census':deletions,'minimum_distance':42,'attaining_normals':[38,191],'nonroot_real_normal_support_lower':54,'integer_packet_review':partitions,'exact_relaxed_moment_floor':'10*5^(199/200)','tariffs':tariffs,'negative_controls':['wrong simple orientation creates mixed signs','root exception has126 signed zeros','distance41 admits rank49 near-boundary histogram'],'scope':'Source/all-volume unchanged-raw freshpacket theorem accepted. Mixed current rows, funded routes, useful hub side information and changed packet interfaces remain outside the obstruction. No new kappa.'}
    a.output.mkdir(parents=True,exist_ok=True);(a.output/'REVIEW.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(report['status']);print(json.dumps({name:{'headroom':float(Q(r['headroom_lower'])),'deficit':float(Q(r['deficit_lower']))} for name,r in tariffs.items()},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
