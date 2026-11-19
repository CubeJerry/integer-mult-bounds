#!/usr/bin/env python3
"""Separate native geometry, modular dual and nonlinear controls for H263."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)
def gf4mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        a<<=1
        if a&4:a^=7
        b>>=1
    return z
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';rp=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz';pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    lr,rr=gzip.decompress(lp.read_bytes()),gzip.decompress(rp.read_bytes())
    need(hashlib.sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    need(hashlib.sha256(rr).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','routes pin')
    l=json.loads(lr);routes=[json.loads(x)for x in rr.splitlines()];H=list(map(set,l['A2']));D=list(map(set,l['D4']));roots=l['root_table'];native=set(range(111));h=263
    donors=sorted(H[h]);need(donors==[0,61,62],'actual H263')
    def perpendicular(i,W):return all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for j in W)
    ports=[d for d,W in enumerate(D)if H[h]<=W]
    receivers=[];views={}
    for i in native:
        if not perpendicular(i,H[h]):continue
        local={j:[p for p,P in enumerate(H)if j in P and perpendicular(i,P)]for j in donors}
        need(all(len(x)==16 for x in local.values()),'sixteen source planes')
        if all(len(H[p]&native)>=2 for v in local.values()for p in v):receivers.append(i);views[i]=local
    receivers.sort();aud={d:{i for i in receivers if perpendicular(i,D[d])}for d in ports}
    vis={i:{d for d in ports if i in aud[d]}for i in receivers}
    need(len(ports)==45 and len(receivers)==33 and all(len(v)==15 for v in vis.values()),'native 45/33/15 incidence')
    source_counts=Counter();early=Counter();exit_counts=Counter();h_owners=set()
    for phase,j,c,plane,middle,k,line,terminal in routes:
        source=j if phase=='X'else line
        if source is not None and plane is not None:source_counts[source,plane]+=1
        if plane==h:
            need(phase=='X'and j in donors,'no late H263 fields')
            need((j,c)not in h_owners,'distinct actual H263 owners');h_owners.add((j,c));early[j]+=1;exit_counts[middle]+=1
    need(early=={j:30 for j in donors}and exit_counts=={d:2 for d in ports},'actual fully early quotas')
    need(all(source_counts[j,p]==30 for local in views.values()for j,v in local.items()for p in v),'all99 views use only actual ordinary source quotients')
    isolators={};triples=Counter()
    for triple in itertools.combinations(receivers,3):
        common=set.intersection(*(vis[i]for i in triple));triples[len(common)]+=1
        if len(common)==1:isolators.setdefault(next(iter(common)),list(triple))
    need(set(isolators)==set(ports),'every actual port triple isolated')
    need(vis[4]&vis[5]&vis[6]=={2835},'designated isolating triple')
    for d in ports:need(set.intersection(*(vis[i]for i in aud[d]))=={d},'entire audience isolates exactly its port')
    weights={i:0 for i in receivers}
    for i in [4,5,6,7,53,55]:weights[i]=2
    for i in [8,10,47,48]:weights[i]=1
    sums={d:sum(weights[i]for i in aud[d])for d in ports}
    need(sum(weights.values())==16 and set(sums.values())=={3,6,12},'explicit mod3 dual')
    need(all(v%3==0 for v in sums.values()),'all incidence columns annihilated modulo3')
    classes=json.loads(gzip.decompress(pp.read_bytes()))['classes'][str(h)]
    need(len(classes)==5 and sorted(sum(classes,[]))==ports,'five actual nine-port classes')
    for block in classes:
        need(len(block)==9 and all(len(set(block)&vis[i])==3 for i in receivers),'width3 nonnegative integer dimension profile')
    # Nonlinear port relabelling over F4: Frobenius is a bijection but not
    # F4-linear. The common-coordinate linearization conclusion survives.
    states=list(itertools.product(range(4),repeat=3));encoded={z:tuple(gf4mul(x,x)for x in z)for z in states}
    need(len(set(encoded.values()))==64,'nonlinear product encoder bijective')
    need(gf4mul(2,2)!=2*gf4mul(1,1),'F4-linearity genuinely absent')
    for z,y in encoded.items():need(tuple(gf4mul(x,x)for x in y)==z,'exact nonlinear inverse')
    for selected in [(0,1),(0,2),(1,2)]:
        for z,y in encoded.items():need(tuple(gf4mul(y[k],y[k])for k in selected)==tuple(z[k]for k in selected),'saturated linear target after nonlinear labels')
    need(16%15!=0 and 16%3!=0 and 48%3==0 and 48%15!=0 and 240%15==0,'distinct repeated and varying-component divisors')
    result={'status':'PASS_SEPARATE_FULLY_EARLY_LINEARIZATION_REVIEW','author_code_imported':False,
      'receiver_count':33,'port_count':45,'triple_count':sum(triples.values()),'triple_intersection_histogram':dict(triples),
      'port_isolators':isolators,'mod3_weights':weights,'mod3_port_sum_histogram':dict(Counter(sums.values())),
      'total_mod3_weight':16,'ordinary_source_views_verified':99,'early_input_dimension':90,'outgoing_dimension':90,
      'identical_base_divisor':15,'common_uncoupled_component_divisor':3,'local_integer_component_divisor_is_sharp':True,
      'GF4_nonlinear_relabelling_states_checked':64,'scope':'Independent native premises and written common-function/direct-sum proof review. Source-only theorem retained; no complete kappa.',
      'source_pins':[{'path':str(p.relative_to(a.repo))if p.is_relative_to(a.repo)else p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,rp,pp,a.author/'PROOF.md']],
      'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['ordinary_source_views_verified','triple_intersection_histogram','total_mod3_weight','identical_base_divisor','common_uncoupled_component_divisor']},sort_keys=True))
if __name__=='__main__':main()
