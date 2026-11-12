#!/usr/bin/env python3
"""Independent all-label bit propagation and exact source adjoint review.
No author imports; the supplied certificate provides only claimed evidence.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse,gzip,hashlib,json
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,s):
    if not x:raise ValueError(s)
def span(f):
    a={0}
    for b in f:a|={v^b for v in a}
    return tuple(sorted(a))
def addto(a,b,c):
    for k,x in b.items():
        v=a.get(k,Q(0))+c*x
        if v:a[k]=v
        else:a.pop(k,None)
def roots(v):
    if v.bit_count()==3:r=[Q(int(bool(v&(1<<k))))-Q(1,3) for k in range(9)]
    else:
        need(v.bit_count()==7,'weight');i,j=[k for k in range(9) if not(v&(1<<k))];r=[Q((k==i)-(k==j)) for k in range(9)]
    return [2*r[k]+r[8] for k in range(8)]
def main(a):
    raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));certbytes=a.certificate.read_bytes();certbytes=gzip.decompress(certbytes) if certbytes[:2]==b'\x1f\x8b' else certbytes;cert=json.loads(certbytes)
    fs=list(map(span,w['frames']));first={}
    for k,s in enumerate(fs):first.setdefault(s,k)
    C=[first[s] for s in fs];n=w['public'];P=w['program'];xs=w['live'];need(xs==sorted(xs),'ordered source roles')
    need(cert['source_sha256']==PIN and cert['column_order_donor_X']==xs and cert['row_order_receiver_for_X']==xs,'certificate binding')
    mainroles=set(xs)|{x+112 for x in xs}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);hub=C[w['final'][xs[0]]]
    off=[j for j,f in enumerate(w['final']) if C[f]!=hub];adj={j:{('endpoint',j):Q(1)} for j in off};neutral=[];nonzero=[];owned=[];guardonly=[]
    def row(j):return adj.setdefault(j,{})
    for t in range(len(P)-1,-1,-1):
        e=P[t];op,j=e[:2]
        if op=='ADD':need(j!=e[2],'self ADD');addto(row(e[2]),row(j),Q(e[3]))
        elif op=='SCALE':adj[j]={k:Q(e[2])*v for k,v in row(j).items() if Q(e[2])*v}
        elif op=='COPY':addto(row(e[2]),row(j),Q(e[3]));adj[j]={('guard',t):Q(1)}
        elif op=='CLEAR':adj[j]={}
        elif op=='INIT':adj.pop(j,None)
        elif op=='MOVE':
            if j>=n:owned.append(t)
            elif j not in mainroles:
                if row(j):
                    nonzero.append(t)
                    if all(k[0]=='guard' for k in row(j)):guardonly.append(t)
                else:neutral.append(t)
        else:raise ValueError(op)
    neutral.sort();nonzero.sort();owned.sort();E=cert['edge_certificate']
    need(neutral==[e['event'] for e in E['public_neutral']],'complete neutral event list')
    need(nonzero==[e['event'] for e in E['public_nonzero']],'complete nonneutral event list');need(owned==[e['event'] for e in E['all_owned']],'owned event list')
    # All claimed neutral edge metadata comes from the actual pinned occurrence.
    for key in ['public_neutral','public_nonzero','all_owned']:
        for edge in E[key]:
            t=edge['event'];e=P[t]
            need((edge['role'],edge['source'],edge['target'])==(e[1],C[e[2]],C[e[3]]),'edge occurrence')
    routes={j:{C[w['initial'][j]]} for j in xs+[x+112 for x in xs]}
    for e in P:
        if e[0]=='MOVE' and e[1] in routes:routes[e[1]].add(C[e[3]])
    A=[roots(v) for v in w['ports']];out={};allmat=[];path_count=0;witness_count=0;cycle_control=None
    for name,drop in [('S8_33',set(cert['removed_second_owned_events'])),('full47',set())]:
        events=sorted(neutral+[t for t in owned if t not in drop]);admitted=set(events);reach={}
        for j,x in enumerate(xs):
            for chart in routes[x]:reach[chart]=reach.get(chart,0)|(1<<j)
        for t in events:
            e=P[t];src,dst=C[e[2]],C[e[3]];reach[dst]=reach.get(dst,0)|reach.get(src,0)
        masks=[]
        for x in xs:
            mask=0
            for chart in routes[x+112]:mask|=reach.get(chart,0)
            masks.append(mask)
        S=[[int(bool(mask&(1<<j))) for j in range(104)] for mask in masks];need(S==cert['side_information'][name]['matrix'],'independent timed all-source propagation')
        need(not any(S[i][i] for i in range(104)),'no own-demand path');allmat.append(S)
        for i in range(104):
            for j in range(104):
                p=cert['side_information'][name]['witness_paths'][i][j]
                if not S[i][j]:need(p is None,'nonedge has no path');continue
                need(p['seed_chart'] in routes[xs[j]],'path seed');chart=p['seed_chart'];last=-1
                for t in p['events']:
                    need(t>last and t in admitted and C[P[t][2]]==chart,'chronological path edge');chart=C[P[t][3]];last=t
                need(chart==p['chart'] and chart in routes[xs[i]+112],'path terminal');path_count+=1
        screen=cert['eight_packet_screen']['variants'][name];order=screen['acyclic_topological_order_X'];need(len(order)==len(set(order)),'acyclic unique vertices');pos={x:k for k,x in enumerate(order)}
        edgesU=[(xs[i],xs[j]) for i in range(104) for j in range(104) if xs[i] in pos and xs[j] in pos and S[i][j]]
        need(all(pos[x]<pos[y] for x,y in edgesU),'exact supplied acyclic order');need(len(order)==54,'54-vertex certificate')
        if edgesU:cycle_control={'existing_edge':edgesU[0],'reverse_edge_rejected':True};need(not pos[edgesU[0][1]]<pos[edgesU[0][0]],'reverse-edge negative control')
        ws=screen['indistinguishability_witnesses'];need(len(ws)==104,'104 receiver witnesses');seen=set()
        for witness in ws:
            x=witness['receiver_X'];i=xs.index(x);need(x not in seen,'unique receiver witness');seen.add(x);z={xs.index(j):Q(c) for j,c in witness['indistinguishable_difference']};need(z.get(i)==1,'target displacement1')
            need(all(not z.get(j) for j in range(104) if S[i][j]),'known coordinate unchanged')
            need(all(sum(c*A[j][k] for j,c in z.items())==0 for k in range(8)),'all eight packets unchanged');witness_count+=1
        # Universal coefficient mutation at target breaks the exhibited kernel.
        mut=ws[0];mi=xs.index(mut['receiver_X']);mz={xs.index(j):Q(c) for j,c in mut['indistinguishable_difference']};mz[mi]+=1
        need(any(sum(c*A[j][k] for j,c in mz.items()) for k in range(8)),'doubling target coefficient rejects kernel mutant')
        out[name]={'neutral_arcs':len(neutral),'owned_arcs':len(owned)-len(drop),'side_information_edges':sum(map(sum,S)),'acyclic_vertices':len(order),'induced_edges':len(edgesU),'indistinguishability_witnesses':len(ws),'known_odd_pairs':sum(S[i][j] and (w['ports'][i]&w['ports'][j]).bit_count()%2 for i in range(104) for j in range(104))}
    need(allmat[0]==allmat[1],'33/47 side-information equality')
    R={'status':'PASS_INDEPENDENT_TIMED_SIDE_INFORMATION_REVIEW','source_sha256':PIN,'author_certificate_sha256':hashlib.sha256(certbytes).hexdigest(),'offhub_endpoints':len(off),'neutral_public_arcs':len(neutral),'nonneutral_public_arcs':len(nonzero),'all_owned_arcs':len(owned),'guard_only_nonneutral_moves':guardonly,'checked_paths':path_count,'checked_receiver_witnesses':witness_count,'variants':out,'negative_controls':{'relabel_nonneutral_event_as_neutral_rejected':nonzero[0],'reversed_acyclic_edge':cycle_control,'target_kernel_coefficient_doubled':'nonzero eight-packet response'},'scope':'Fixed-calendar pure-information routing graph with hoisted donor caches, no consumed-main-route reuse, and no additional usable common-response observations. Not a lower bound for arbitrary common-mode network codes.','new_complete_kappa':None}
    a.output.write_text(json.dumps(R,indent=2)+'\n');print(json.dumps(R,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
