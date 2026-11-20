"""Verify the native 14-owner witness and a 1024-coordinate exact Shannon identity."""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

LAYOUT_SHA='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'


def need(value,message):
    if not value:
        raise ValueError(message)


def validate(roots,w):
    native=w['native'];C=native['anchors'];vertices=native['pair_to_native'];labels=list(combinations(range(5),2));P=[set(e) for e in labels]
    need(native['pair_order']==[list(e) for e in labels] and len(C)==4 and len(vertices)==10 and len(set(C+vertices))==14,'distinct authentic owners')
    def foreign(i,j):return sum(a*b for a,b in zip(roots[i],roots[j]))==0
    for i in C:
        for j in C+vertices:need(not foreign(i,j),'native independent anchor and no cross link')
    for i,r in enumerate(vertices):
        for j,s in enumerate(vertices):need(foreign(r,s)==(not P[i]&P[j]),'actual native Petersen proper support')
    c=w['petersen_certificate'];matching=c['matching_upper_bound']
    need(len(matching)==5 and sorted(j for e in matching for j in e)==list(range(10)) and all(not P[x]&P[y] for x,y in matching),'genuine five-edge upper bound')
    pos={v:i for i,v in enumerate(labels)};total=Counter();rhs=0;kinds=Counter();id_rhs=0
    for weight,kind,*args in c['weighted_raw_terms']:
        kinds[kind]+=1
        if kind in ('mono','submod'):
            need(weight>0,'nonnegative Shannon inequality multiplier')
        if kind=='empty':
            total[0]+=120*weight
            continue
        S,i,*extra=args;need(0<=S<1024 and 0<=i<10 and not(S>>i&1),'new singleton variable')
        if kind=='decode':
            need(all(P[i]&P[j] for j in range(10) if (S>>j)&1),'decoding equality includes no side-information donor')
        if kind=='submod':
            j,=extra;need(0<=j<10 and j!=i and not(S>>j&1),'two distinct increments')
        for perm in permutations(range(5)):
            pm=[pos[tuple(sorted((perm[x],perm[y])))] for x,y in labels]
            s=sum(1<<pm[b] for b in range(10) if (S>>b)&1);e=1<<pm[i]
            if kind in ('mono','decode'):
                total[s|e]+=weight;total[s]-=weight
                if kind=='decode':rhs+=weight
            elif kind=='submod':
                f=1<<pm[j];total[s|e]+=weight;total[s|f]+=weight;total[s]-=weight;total[s|e|f]-=weight
            else:raise ValueError('unknown Shannon predicate')
    nonzero={k:v for k,v in total.items() if v};scale=120*c['scale']
    need(nonzero=={0:-scale,1023:scale} and rhs==5*scale,'exact 1024-variable integer certificate')
    return {'native_anchors':C,'native_petersen_pair_order':vertices,'native_proper_edges_undirected':15,'raw_predicates_by_kind':dict(kinds),'distinct_template_orbits':len(c['orbit_representatives']),'permutation_images':120,'global_integer_coefficients':nonzero,'global_integer_rhs':rhs,'petersen_rank_or_entropy_lower_over_b':5,'native_rank_or_entropy_lower_over_b':9,'native_rank_lower_at_b_3840':34560}


def main():
    p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--witness',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_SHA,'published native layout');v=json.loads(raw)['root_table'][:111];w=json.loads(a.witness.read_bytes());result=validate(v,w);faults={}
    for name,mutate in [('anchor_overlap',lambda x:x['native']['anchors'].__setitem__(0,x['native']['pair_to_native'][0])),('native_owner_swap',lambda x:x['native']['pair_to_native'].__setitem__(0,x['native']['anchors'][0])),('changed_dual_weight',lambda x:x['petersen_certificate']['weighted_raw_terms'][0].__setitem__(0,99)),('illegal_decoding',lambda x:next(z for z in x['petersen_certificate']['weighted_raw_terms'] if z[1]=='decode').__setitem__(2,1<<7))]:
        bad=deepcopy(w);mutate(bad)
        try:validate(v,bad)
        except ValueError as ex:faults[name]=str(ex)
    need(len(faults)==4,'effective faults');result['faults']=faults;result['witness_sha256']=sha256(a.witness.read_bytes()).hexdigest();result['native_layout_uncompressed_sha256']=LAYOUT_SHA
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result)


if __name__=='__main__':main()
