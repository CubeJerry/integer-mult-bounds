#!/usr/bin/env python3
"""Diagnostic overgrants: retime clean-owned and optionally reuse main routes."""
import argparse,gzip,hashlib,json
from collections import defaultdict,deque
from pathlib import Path
from verify import PIN,check,graph,neutral,read_json,space,screen,write_json

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,required=True)
parser.add_argument('--base','--receipt',dest='receipt',type=Path,default=HERE/'RESULT.json.gz')
parser.add_argument('--output',type=Path,default=HERE/'EXPANDED.json.gz')
args=parser.parse_args()
raw=args.source.read_bytes()
check(hashlib.sha256(raw).hexdigest()==PIN,'native source SHA256')
w=json.loads(gzip.decompress(raw))
R=read_json(args.receipt)
first={};canon=[]
for i,f in enumerate(w['frames']):
    s=space(f);first.setdefault(s,i);canon.append(first[s])
E=neutral(w,canon)
check(E==R['edge_certificate'],'base exact adjoint certificate')
xs,native_routes,native_variants=graph(w,canon,E)
check(xs==R['row_order_receiver_for_X'] and xs==R['column_order_donor_X'],'base role order')
check(native_variants==R['side_information'],'base timed graph certificate')
routes={int(k):v for k,v in R['raw_itineraries'].items()}
check(all(routes[j]==native_routes[j] for j in xs+[x+112 for x in xs]),'base raw itineraries')
M=set(xs)|{x+112 for x in xs}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
main=[]
for event,x in enumerate(w['program']):
    if x[0]=='MOVE' and x[1] in M:
        main.append(dict(event=event,role=x[1],source=canon[x[2]],target=canon[x[3]],kind='reused-main'))
V={}
for name,reuse,drop in [('retimed33',False,set(R['removed_second_owned_events'])),('retimed47',False,set()),('main_reuse_retimed33',True,set(R['removed_second_owned_events'])),('main_reuse_retimed47',True,set())]:
    free=[e for e in R['edge_certificate']['all_owned'] if e['event'] not in drop]+(main if reuse else [])
    adj=defaultdict(list)
    for e in free:adj[e['source']].append(e)
    S=[[0]*104 for _ in xs];paths=[[None]*104 for _ in xs]
    for j,d in enumerate(xs):
        reach={c:dict(chart=c,after_event=-1,steps=[],seed_chart=c) for c in routes[d]}
        def close(seeds,time):
            queue=deque(seeds)
            while queue:
                c=queue.popleft()
                for e in adj[c]:
                    if e['target'] not in reach:
                        p=reach[c];reach[e['target']]=dict(chart=e['target'],after_event=time,steps=p['steps']+[dict(original_event=e['event'],kind=e['kind'],at_time=time)],seed_chart=p['seed_chart']);queue.append(e['target'])
        close(list(reach),-1)
        for e in R['edge_certificate']['public_neutral']:
            if e['source'] in reach and e['target'] not in reach:
                p=reach[e['source']];reach[e['target']]=dict(chart=e['target'],after_event=e['event'],steps=p['steps']+[dict(original_event=e['event'],kind=e['kind'],at_time=e['event'])],seed_chart=p['seed_chart']);close([e['target']],e['event'])
        for i,r in enumerate(xs):
            candidates=[reach[c] for c in routes[r+112] if c in reach]
            if candidates:
                S[i][j]=1;paths[i][j]=min(candidates,key=lambda p:(p['after_event'],len(p['steps']),p['chart']))
    V[name]=dict(second_owned_arcs=len(free)-(len(main) if reuse else 0),reused_main_arcs=len(main) if reuse else 0,matrix=S,witness_paths=paths,row_degree=list(map(sum,S)),column_degree=[sum(r[j] for r in S) for j in range(104)],side_information_edges=sum(map(sum,S)),self_delivery_count=sum(S[i][i] for i in range(104)))
C=screen(w,xs,V)
out=dict(schema='diagnostic-expanded-side-information-v1',source_sha256=R['source_sha256'],scope='Per-message unlimited-capacity overgrant. Clean second-owned arcs retimed arbitrarily; main_reuse variants additionally permit already-consumed main raw reservations to be reused at arbitrary times. This supplies no physical construction.',row_order_receiver_for_X=xs,column_order_donor_X=xs,variants=V,eight_packet_screen=C)
write_json(args.output,out)
print(json.dumps({k:dict(side_info=v['side_information_edges'],self_delivery=v['self_delivery_count'],e8_decodable=len(C['variants'][k]['decodable_receivers']),acyclic_bound=C['variants'][k]['broadcast_packet_lower_bound']) for k,v in V.items()},sort_keys=True))
