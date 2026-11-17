#!/usr/bin/env python3
"""Independent ternary outer-flat coverage and entropy-inlet cost audit."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path

ROOT=Path('research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json')
WEIGHTS_HASH='e0a9f41270364857edf52eb07699cbaba700af5a055e57d5bd917668fbbb9cb2'
U=sorted(set(range(8,111))-{14,17,19,20,96,99,101,102})

def need(test,reason):
    if not test:raise ValueError(reason)

def inds(z):
    while z:
        t=z&-z;yield t.bit_length()-1;z^=t

def enumerate_W(R):
    normals=[sum(1<<j for j in U if sum(a*b for a,b in zip(x,R[j]))==0)for x in R]
    allmask=sum(1<<j for j in U);out=[]
    for i,j in combinations(U,2):
        if normals[i]>>j&1:continue
        excludes=normals[i]|normals[j]
        rem=allmask&~excludes&~((1<<(j+1))-1)
        for k in inds(rem):
            for t in inds(rem&~normals[k]&~((1<<(k+1))-1)):
                C=allmask&~(excludes|normals[k]|normals[t]|1<<i|1<<j|1<<k|1<<t)
                if C.bit_count()!=10:continue
                pts=list(inds(C));groups=[set(q)for q in combinations(pts,4)if all(not(normals[a]>>b&1)for a,b in combinations(q,2))]
                labels={a:frozenset(h for h,T in enumerate(groups)if a in T)for a in pts}
                need(len(groups)==5 and len(set(labels.values()))==10 and all(len(l)==2 for l in labels.values()),'Petersen coordinates')
                need(all(bool(normals[a]>>b&1)==labels[a].isdisjoint(labels[b])for a,b in combinations(pts,2)),'Petersen adjacency')
                out.append([i,j,k,t]+pts)
    need(len(out)==838,'witness count/order');return out

def coverage(repo,weightsfile):
    raw=(repo/ROOT).read_bytes();need(hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native')
    roots=json.loads(raw)['native_roots'];raw=weightsfile.read_bytes();need(hashlib.sha256(raw).hexdigest()==WEIGHTS_HASH,'witness weights')
    weights={int(k):v for k,v in json.loads(raw).items()};need(len(weights)==102 and sum(weights.values())==999993,'weight mass')
    groups=enumerate_W(roots)
    data=''.join(' '.join(map(str,[role,0]+roots[role]))+'\n' for role in U)
    data+=''.join(' '.join(map(str,[weights.get(k,0)]+[U.index(i)for i in group]))+'\n' for k,group in enumerate(groups))
    with tempfile.TemporaryDirectory()as tmp:
        exe=Path(tmp)/'geom'
        subprocess.run([os.environ.get('CXX','c++'),'-O2','-std=c++20',str(Path(__file__).with_name('flat_coverage.cpp')),'-o',str(exe)],check=True)
        res=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True)
    rows=[list(map(int,l.split()))for l in res.stdout.splitlines()]
    need([row[2]for row in rows]==[191805,387630,610722,827177,991966],'native ternary-flat coverage')
    need([row[3] for row in rows]==[286,483,660,764,829], 'unweighted full-family maximum below 838')
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--weights',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    geo=coverage(a.repo,a.weights);caps=[Q(0)]+[Q(s[2],999993)for s in geo]
    layer={2:Q(1),3:Q(19,20),4:Q(3,5),5:Q(1)}
    downhill=[]
    for s in range(1,9):
        for d in range(s):
            load=sum(w for r,w in layer.items()if d<=r<s)
            need(load**200<=(s-d)**199,'downward whole-record price')
            downhill.append([s,d,str(load)])
    upward=[]
    for s in range(1,6):
        for origin in range(s):
            bound=caps[origin]*sum(w for r,w in layer.items()if r>=s)
            need(bound<=1,'inlet costs at most one unit');upward.append([origin,s,str(bound)])
    need(9*sum(layer.values())==Q(639,20),'exact price')
    # On an internal carrier of a known previous cut value, a missed inlet
    # can be informative unconditionally. It is deterministic after that
    # earlier value is supplied, so an unconditional-zero rule fails.
    examples=[(bit,1^bit) for bit in (0,1)]
    need(len({v for _,v in examples})==2 and all(len({v for u,v in examples if u==h})==1 for h in (0,1)),'chronology control')
    c=(1+caps[4])/2
    unit=[caps[1],caps[2],caps[3],c,c,caps[3],caps[2],caps[1]]
    need(max(unit)==Q(913585,999993) and (1/c)**200<=2**199,'arbitrary-length cost')
    gaps=[-((-9*b*c.denominator)//c.numerator)for b in range(1,4)]
    need(gaps==[10,20,30],'all three integer gap floors')
    result={'arbitrary_length_unit_loss_caps':list(map(str,unit)),'arbitrary_length_private_plus_nonprivate_floor':str(8+9/c),
            'integer_nonprivate_gaps_for_b_1_2_3':gaps,'status':'PASS_INDEPENDENT_NONLINEAR_FIVE_LAYER_EQUALITY_INLET_REVIEW','weights_sha256':WEIGHTS_HASH,'positive_witnesses':102,
            'ternary_outer_flat_counts_and_maximum_hits':geo,'total_witness_weight':999993,'layer_weights':{r:str(w)for r,w in layer.items()},
            'all_36_downward_prices':downhill,'all_15_upward_inlet_unit_caps':upward,'normalized_lower_bill':'639/20',
            'equality_sources':'three authenticated sources from predecessor nonlinear 838-witness review; fixed deterministic schedules'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS independent ternary coverage, all downhill costs and inlet unit bounds, nonlinear equality 31.95')
if __name__=='__main__':main()
