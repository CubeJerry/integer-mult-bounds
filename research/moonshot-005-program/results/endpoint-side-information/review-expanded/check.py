#!/usr/bin/env python3
"""Independent bitset fixed-point reconstruction of expanded source routing.
The neutral classification is pinned to a separately checked source certificate.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,collections,gzip,hashlib,json
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
BASE='58186c21ef28a9ae71e8c14dd82c12a01bf50f33db28e23eadc23755e905b139'
def need(x,s):
    if not x:raise ValueError(s)
def span(f):
    s={0}
    for x in f:s|={y^x for y in s}
    return tuple(sorted(s))
def root(v):
    if v.bit_count()==3:r=[Q(int(bool(v&(1<<k))))-Q(1,3) for k in range(9)]
    else:
        i,j=[k for k in range(9) if not(v&(1<<k))];r=[Q((k==i)-(k==j)) for k in range(9)]
    return [2*r[k]+r[8] for k in range(8)]
def main(a):
    raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));basebytes=a.base.read_bytes();basebytes=gzip.decompress(basebytes) if basebytes[:2]==b'\x1f\x8b' else basebytes;need(hashlib.sha256(basebytes).hexdigest()==BASE,'independently checked neutral certificate');b=json.loads(basebytes);expandedbytes=a.expanded.read_bytes();expandedbytes=gzip.decompress(expandedbytes) if expandedbytes[:2]==b'\x1f\x8b' else expandedbytes;c=json.loads(expandedbytes);P=w['program'];xs=w['live'];A=list(map(root,w['ports']));first={};C=[]
    for i,f in enumerate(w['frames']):s=span(f);first.setdefault(s,i);C.append(first[s])
    need(c['source_sha256']==PIN and c['row_order_receiver_for_X']==xs and c['column_order_donor_X']==xs,'expanded source order')
    routes={j:{C[w['initial'][j]]} for j in xs+[x+112 for x in xs]}
    for e in P:
        if e[0]=='MOVE' and e[1] in routes:routes[e[1]].add(C[e[3]])
    mainroles=set(xs)|{x+112 for x in xs}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);mainmoves=[t for t,e in enumerate(P) if e[0]=='MOVE' and e[1] in mainroles];owned=[t for t,e in enumerate(P) if e[0]=='MOVE' and e[1]>=w['public']];neutral=[e['event'] for e in b['edge_certificate']['public_neutral']];drops=set(b['removed_second_owned_events']);out={};totalpaths=0;totalwitness=0
    for name in ['retimed33','retimed47','main_reuse_retimed33','main_reuse_retimed47']:
        reuse=name.startswith('main_');drop=drops if name.endswith('33') else set();free=[t for t in owned if t not in drop]+(mainmoves if reuse else []);allowed=set(free);edges=collections.defaultdict(set)
        for t in free:edges[C[P[t][2]]].add(C[P[t][3]])
        mask=collections.defaultdict(int)
        for j,x in enumerate(xs):
            for chart in routes[x]:mask[chart]|=1<<j
        def closure(seeds):
            todo=collections.deque(seeds);pending=set(seeds)
            while todo:
                src=todo.popleft();pending.remove(src)
                for dst in edges[src]:
                    z=mask[dst]|mask[src]
                    if z!=mask[dst]:
                        mask[dst]=z
                        if dst not in pending:todo.append(dst);pending.add(dst)
        closure(list(mask))
        for t in neutral:
            e=P[t];src,dst=C[e[2]],C[e[3]];z=mask[dst]|mask[src]
            if z!=mask[dst]:mask[dst]=z;closure([dst])
        S=[]
        for x in xs:
            z=0
            for chart in routes[x+112]:z|=mask[chart]
            S.append([int(bool(z&(1<<j))) for j in range(104)])
        v=c['variants'][name];need(S==v['matrix'],'all-source fixed-point matrix '+name)
        for i in range(104):
            for j in range(104):
                p=v['witness_paths'][i][j]
                if not S[i][j]:need(p is None,'absent path');continue
                chart=p['seed_chart'];need(chart in routes[xs[j]],'path seed');clock=-1
                for step in p['steps']:
                    t=step['original_event'];time=step['at_time'];e=P[t];need(time>=clock and C[e[2]]==chart,'path causal station')
                    if step['kind']=='neutral-public':need(t in neutral and time==t,'timed neutral path')
                    else:need(t in allowed,'free retimed path')
                    chart=C[e[3]];clock=time
                need(chart==p['chart'] and chart in routes[xs[i]+112],'path destination');totalpaths+=1
        z=c['eight_packet_screen']['variants'][name];order=z['acyclic_topological_order_X'];pos={x:k for k,x in enumerate(order)};need(len(pos)==len(order),'unique DAG vertices');induced=[]
        for i in range(104):
            for j in range(104):
                if xs[i] in pos and xs[j] in pos and S[i][j]:need(pos[xs[i]]<pos[xs[j]],'DAG orientation');induced.append([xs[i],xs[j]])
        bad=z['indistinguishability_witnesses'];seen=set()
        for witness in bad:
            x=witness['receiver_X'];i=xs.index(x);need(x not in seen,'unique receiver');seen.add(x);d={xs.index(j):Q(v) for j,v in witness['indistinguishable_difference']};need(d.get(i)==1,'target varies');need(all(not d.get(j) for j in range(104) if S[i][j]),'side information fixed');need(all(sum(v*A[j][k] for j,v in d.items())==0 for k in range(8)),'broadcast fixed');totalwitness+=1
        good=z['decodable_receivers'];need(set(good)=={xs[i] for i in range(104) if S[i][i]},'claimed successful cases are own-data overgrants');need(len(good)+len(bad)==104,'complete receiver partition')
        out[name]={'side_information_edges':sum(map(sum,S)),'self_deliveries':sum(S[i][i] for i in range(104)),'free_owned':len(owned)-len(drop),'reused_main':len(mainmoves) if reuse else 0,'acyclic_vertices':len(order),'induced_edges':len(induced),'eight_packet_failures':len(bad),'eight_packet_successes':good}
    need(out['main_reuse_retimed47']['acyclic_vertices']==43,'43-packet source witness');need(9**199>8**200,'exact ninth-rank tariff exceeds8 at kappa1/200');need(8*8+35==99,'conservative fixed-eight cost')
    R={'status':'PASS_INDEPENDENT_EXPANDED_ROUTING_REVIEW','source_sha256':PIN,'base_certificate_sha256':BASE,'expanded_certificate_sha256':hashlib.sha256(expandedbytes).hexdigest(),'variants':out,'checked_paths':totalpaths,'checked_kernel_witnesses':totalwitness,'conditional_budget':{'total_linear_packets_at_least':43,'fixed_eight_packets':8,'additional_complete_field_packets_at_least':35,'strict_paid_lower_bound':99,'hypothesis':'Eight retained rank9 broadcasts at kappa1/200, further complete-field calls each rank>=1, unchanged other invoice; additive allowance must be<99.'},'scope':'Retimed/reused routing overgrant only; no conclusion for extra usable common-response observations or changed baseline invoices.','new_complete_kappa':None}
    a.output.write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--expanded',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
