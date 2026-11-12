#!/usr/bin/env python3
"""Exact source side-information graph and eight-packet decoder obstruction.
For @CubeJerry, with OpenAI assistance. No new kappa is claimed.
"""
import argparse
from collections import deque
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import random

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
REMOVED = {28141,28169,33554,33558,34467,34479,37597,37606,39217,39546,40094,40096,41756,41758}

def check(x, text):
    if not x: raise ValueError(text)

def read_json(path):
    raw=path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)

def write_json(path,value):
    raw=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(raw,mtime=0) if path.suffix=='.gz' else raw)

def space(frame):
    s = {0}
    for x in frame: s |= {y ^ x for y in tuple(s)}
    return tuple(sorted(s))

def axpy(a, b, c=F(1)):
    for k, v in tuple(b.items()):
        z = a.get(k, F(0)) + c * v
        if z: a[k] = z
        else: a.pop(k, None)

def neutral(w, canon):
    main = set(w['live']) | {x+112 for x in w['live']} | set(w['hosted']['X2']) | set(w['hosted']['Y2'])
    h = [{} for _ in range(w['public']+w['owned_fields'])]
    off = [j for j in range(w['public']) if canon[w['final'][j]] != 127]
    for j in off: h[j] = {j:F(1)}
    good, bad, owned, scalars = [], [], [], {}
    guard = w['public']
    def coef(s):
        if s not in scalars: scalars[s] = F(s)
        return scalars[s]
    for event in range(len(w['program'])-1,-1,-1):
        x = w['program'][event]; op,a,b = x[:3]
        if op == 'ADD':
            check(a != b,'self ADD'); axpy(h[b],h[a],coef(x[3]))
        elif op == 'SCALE': h[a] = {k:coef(b)*v for k,v in h[a].items() if coef(b)*v}
        elif op == 'COPY':
            axpy(h[b],h[a],coef(x[3])); h[a] = {guard:F(1)}; guard += 1
        elif op in ('INIT','CLEAR'): h[a] = {}
        elif op == 'MOVE':
            e = dict(event=event,role=a,source=canon[b],target=canon[x[3]],rank=abs(len(w['frames'][b])-len(w['frames'][x[3]])))
            if a >= w['public']: owned.append(e | {'kind':'clean-second-owned'})
            elif a not in main:
                if h[a]:
                    k=min(h[a]);bad.append(e | {'witness_output':k,'witness_coefficient':str(h[a][k])})
                else: good.append(e | {'kind':'neutral-public'})
        else: raise ValueError(op)
    return dict(public_neutral=sorted(good,key=lambda e:e['event']),public_nonzero=sorted(bad,key=lambda e:e['event']),all_owned=sorted(owned,key=lambda e:e['event']),offhub_public_count=len(off),copy_guards=guard-w['public'],distinct_scalars=len(scalars))

def root(v):
    if v.bit_count()==3:
        return [2*((v>>k)&1) for k in range(8)] if v&256 else [1 if v>>k&1 else -1 for k in range(8)]
    check(v.bit_count()==7,'port weight')
    z=[k for k in range(9) if not v>>k&1]
    return ([1 if k==z[0] else -1 for k in range(8)] if z[1]==8 else [2*((k==z[0])-(k==z[1])) for k in range(8)])

def coordinates(vectors,target):
    basis={}
    for label,vec in vectors:
        z=list(map(F,vec));expr={label:F(1)}
        for p in sorted(basis):
            if z[p]:
                c=z[p];b,e=basis[p];z=[a-c*t for a,t in zip(z,b)];axpy(expr,e,-c)
        if any(z):
            p=next(k for k,a in enumerate(z) if a);c=z[p]
            basis[p]=([a/c for a in z],{k:a/c for k,a in expr.items()})
    z=list(map(F,target));expr={}
    for p in sorted(basis):
        if z[p]:
            c=z[p];b,e=basis[p];z=[a-c*t for a,t in zip(z,b)];axpy(expr,e,c)
    return len(basis),expr if not any(z) else None

def topo(subset,S):
    subset=set(subset);ind={i:sum(S[j][i] for j in subset) for i in subset}
    ready=deque(sorted(i for i in subset if not ind[i]));out=[]
    while ready:
        i=ready.popleft();out.append(i)
        for j in sorted(subset):
            if S[i][j]:
                ind[j]-=1
                if not ind[j]:ready.append(j)
    return out if len(out)==len(subset) else None

def acyclic(S):
    n=len(S);rng=random.Random(20261112);deg=[sum(S[i])+sum(r[i] for r in S) for i in range(n)];best=[]
    for trial in range(100):
        order=sorted(range(n),key=lambda i:deg[i]+(rng.random()*20 if trial else 0));keep=[]
        for i in order:
            if topo(keep+[i],S) is not None:keep.append(i)
        if len(keep)>len(best):best=keep
    return topo(best,S)

def graph(w,canon,E):
    xs=sorted(w['live']);routes=[[canon[f]] for f in w['initial']]
    for x in w['program']:
        if x[0]=='MOVE' and x[1]<w['public']:routes[x[1]].append(canon[x[3]])
    result={}
    for name,drop in [('S8_33',REMOVED),('full47',set())]:
        second=[e for e in E['all_owned'] if e['event'] not in drop]
        edges=sorted(E['public_neutral']+second,key=lambda e:e['event'])
        S=[[0]*len(xs) for _ in xs];paths=[[None]*len(xs) for _ in xs];reaches=[]
        for j,d in enumerate(xs):
            reach={c:dict(chart=c,after_event=-1,events=[],seed_chart=c) for c in routes[d]}
            for e in edges:
                if e['source'] in reach and e['target'] not in reach:
                    p=reach[e['source']];reach[e['target']]=dict(chart=e['target'],after_event=e['event'],events=p['events']+[e['event']],seed_chart=p['seed_chart'])
            reaches.append(sorted(reach))
            for i,dest in enumerate(xs):
                candidates=[reach[c] for c in routes[dest+112] if c in reach]
                if candidates:
                    p=min(candidates,key=lambda a:(a['after_event'],len(a['events']),a['chart']));S[i][j]=1;paths[i][j]=p
        result[name]=dict(second_owned_arcs=len(second),matrix=S,witness_paths=paths,reachable_charts=reaches,row_degree=list(map(sum,S)),column_degree=[sum(r[j] for r in S) for j in range(len(xs))],side_information_edges=sum(map(sum,S)),self_delivery_count=sum(S[i][i] for i in range(len(xs))))
    return xs,routes,result

def screen(w,xs,variants):
    ports=[w['frames'][w['initial'][j]][0] for j in xs];roots=list(map(root,ports));gram=[[sum(a*b for a,b in zip(x,y)) for y in roots] for x in roots]
    for i,v in enumerate(ports):
        check(gram[i][i]==8,'root norm')
        check(set(space(w['frames'][w['final'][xs[i]+112]]))=={u for u in range(512) if not (u&v).bit_count()%2},'receiver hyperplane')
        for j,z in enumerate(ports):
            if i!=j:check(gram[i][j] in ((0,) if (v&z).bit_count()%2 else (-4,4)),'Gram parity')
    check(coordinates(list(enumerate(roots)),[0]*8)[0]==8,'packet rank')
    odd_span_ranks=[]
    for i in range(len(xs)):
        odd=[(j,roots[j]) for j in range(len(xs)) if i!=j and not gram[i][j]]
        odd_rank=coordinates(odd,[0]*8)[0]
        check(odd_rank==7,'ideal odd unknown span must equal root orthogonal complement')
        odd_span_ranks.append(odd_rank)
        for j in range(len(xs)):
            value=F(gram[i][j],8)-(F(gram[i][j],8) if i!=j and gram[i][j] else 0)
            check(value==(1 if i==j else 0),'full-even decoder identity')
        missing=next(j for j in range(len(xs)) if i!=j and gram[i][j])
        lost_rank,lost_expression=coordinates(odd+[(missing,roots[missing])],roots[i])
        check(lost_rank==8 and lost_expression is not None,'deleting one even correction must fail')
    out={}
    for name,V in variants.items():
        S=V['matrix'];bad=[];good=[];needed=[];odd=[]
        for i in range(len(xs)):
            missing=[xs[j] for j in range(len(xs)) if i!=j and gram[i][j] and not S[i][j]]
            needed.append(dict(receiver_X=xs[i],required_even_modes=sum(bool(gram[i][j]) for j in range(len(xs)) if i!=j),missing_even_modes=missing))
            if S[i][i]:
                good.append(xs[i])
                continue
            rank,expr=coordinates([(j,roots[j]) for j in range(len(xs)) if j!=i and not S[i][j]],roots[i])
            if expr is None:good.append(xs[i])
            else:
                null={i:F(1)};null.update({j:-c for j,c in expr.items()})
                check(all(sum(roots[j][k]*c for j,c in null.items())==0 for k in range(8)),'null packet witness')
                check(all(not S[i][j] for j in null),'null side-info witness')
                bad.append(dict(receiver_X=xs[i],unknown_other_root_rank=rank,indistinguishable_difference=[[xs[j],str(c)] for j,c in sorted(null.items())]))
            odd.extend([[xs[i],xs[j]] for j in range(len(xs)) if S[i][j] and (ports[i]&ports[j]).bit_count()%2])
        order=acyclic(S);check(order is not None,'acyclic witness')
        out[name]=dict(decodable_receivers=good,indistinguishability_witnesses=bad,aggregate_requirements=needed,known_odd_pairs=odd,acyclic_topological_order_X=[xs[i] for i in order],broadcast_packet_lower_bound=len(order))
    return dict(ports=ports,roots=roots,gram=gram,rank=8,ideal_odd_unknown_span_ranks=odd_span_ranks,negative_control_full_even_side_information_decodes_all=True,negative_control_removing_one_even_coordinate_fails_all=True,variants=out)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    raw=args.source.read_bytes();check(hashlib.sha256(raw).hexdigest()==PIN,'source SHA256');w=json.loads(gzip.decompress(raw))
    keys=list(map(space,w['frames']));first={}
    for i,k in enumerate(keys):first.setdefault(k,i)
    canon=[first[k] for k in keys];E=neutral(w,canon);check(len(E['public_neutral'])==1472,'neutral count');check(len(E['all_owned'])==47,'owned count')
    xs,routes,V=graph(w,canon,E);C=screen(w,xs,V)
    R=dict(schema='moonshot-timed-side-information-v2',source_sha256=PIN,source_instruction_count=len(w['program']),source_public_inputs=w['public'],domain='All independent common u and private q inputs; graph grants all individually reachable q coordinates.',scope='Donor q_X cached on its own original raw itinerary before common execution. Neutral public helpers and selected clean second-owned arcs retain native event times. Consumed main routes are not reused. Shared capacity, common restoration, second-owned duties, storage and ordinary costs are not supplied.',row_order_receiver_for_X=xs,column_order_donor_X=xs,removed_second_owned_events=sorted(REMOVED),canonical_frame_count=len(first),edge_certificate=E,raw_itineraries={str(j):routes[j] for j in xs+[x+112 for x in xs]},side_information=V,eight_packet_screen=C,status='Exact scoped source obstruction; no new kappa.')
    write_json(args.output,R)
    print(json.dumps({name:dict(side_info=v['side_information_edges'],self_delivery=v['self_delivery_count'],eight_packet_decodable=len(C['variants'][name]['decodable_receivers']),acyclic_lower_bound=C['variants'][name]['broadcast_packet_lower_bound']) for name,v in V.items()},sort_keys=True))

if __name__=='__main__':main()
