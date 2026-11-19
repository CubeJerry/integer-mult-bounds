#!/usr/bin/env python3
"""Exact finite evidence for coupled-source feasibility and common-lift gate.
Author computation, S028 Worker B; separate review remains necessary.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import gzip,json
from pathlib import Path
import numpy as np
import algebra as a

def mm(A,B,T):
    out=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint16)
    for k in range(A.shape[1]):out^=T[A[:,k,None],B[k,None,:]]
    return out

def inverse(M,T,iv):
    n=len(M);A=np.concatenate([M,np.eye(n,dtype=np.uint16)],axis=1).astype(np.uint16)
    for c in range(n):
        ps=np.flatnonzero(A[c:,c]);a.require(len(ps)>0,'invertible finite matrix')
        p=c+int(ps[0]);A[[c,p]]=A[[p,c]]
        A[c,c:]=T[iv[A[c,c]],A[c,c:]]
        f=A[:,c].copy();f[c]=0;A[:,c:]^=T[f[:,None],A[c,c:][None,:]]
    a.require(np.array_equal(A[:,:n],np.eye(n,dtype=np.uint16)),'inverse identity')
    return A[:,n:]

def trace(A):return int(np.bitwise_xor.reduce(np.diag(A)))

def words(U,V,T):
    P=[np.eye(3,dtype=np.uint16),U,mm(U,U,T)]
    return np.column_stack([mm(mm(P[i],V,T),P[j],T).reshape(-1)for i in range(3)for j in range(3)])

def coupled_controls(T,iv):
    I=np.eye(3,dtype=np.uint16);P=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=np.uint16)
    C=np.zeros((3,3),dtype=np.uint16);C[0,0]=1
    L=I.copy();L[0,1]=1;R=I.copy();R[1,2]=1
    results=[]
    for lam in range(5):
        B=P^(I*lam);W=words(B,C,T)
        a.require(a.rank(W,T,iv)==9,'nine full matrix-algebra words')
        Ap=mm(L,R,T);Bp=mm(mm(L,B,T),R,T);Cp=mm(mm(L,C,T),R,T)
        Ai=inverse(Ap,T,iv);U=mm(Ai,Bp,T);V=mm(Ai,Cp,T)
        a.require(a.rank(words(U,V,T),T,iv)==9 and trace(U)==lam,'independent input/output gauge invariant')
        results.append({'lambda':lam,'word_rank':9,'relative_trace':trace(U)})
    bad_rank=a.rank(words(P,I,T),T,iv)
    a.require(bad_rank==3,'commuting generator negative control')
    a.require(len({x['relative_trace']for x in results})==5,'pairwise inequivalent triples')
    degree=296+54+1+8+2
    a.require(degree==361 and degree<512,'safe individual degree bound')
    return {'components':results,'commuting_word_rank':bad_rank,'duplicate_trace_factor':0,
            'covariant_parameters_per_incidence_per_component':576,'total_components':5,
            'individual_degree_bound':degree,'field_size':512}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();base=args.repo/a.PROGRAMME/'results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    rp=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    a.require(sha256(gzip.decompress(lp.read_bytes())).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    a.require(sha256(gzip.decompress(rp.read_bytes())).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','route pin')
    layout=a.unpack(lp);masks,gamma,adj=a.geometry(layout,a.unpack(bp));planes=list(map(set,layout['A2']))
    classes=a.unpack(pp)['classes']['263'];T,iv=a.field(529);coupling=coupled_controls(T,iv)
    counts=Counter();actual_ports=set()
    for line in gzip.decompress(rp.read_bytes()).splitlines():
        row=json.loads(line)
        if row[0]=='X':
            counts[row[1],row[3]]+=1
            if row[3]==263:actual_ports.add(row[4])
    quotas={key:n*8//15 for key,n in counts.items()};donors=sorted(planes[263]);a.require(donors==[0,61,62],'H263 donors')
    allports=[D for C in classes for D in C]
    a.require(len(classes)==5 and all(len(C)==9 for C in classes)and len(set(allports))==45 and set(allports)==actual_ports,'literal five-class port partition')
    views={j:{i:[h for h,H in enumerate(planes)if j in H and H<=adj[i]]for i in sorted(adj[j]&set(range(111)))}for j in donors}
    receivers=sorted(set.intersection(*(set(views[j])for j in donors)))
    tight=[i for i in receivers if all(all(quotas[j,h]<=16 for h in views[j][i])for j in donors)]
    a.require(len(tight)==33,'joint-tight native receivers')
    certificates=[];all_graphs=[]
    for class_index,C in enumerate(classes):
        V=np.zeros((9,9),dtype=np.uint16)
        for p in range(9):
            V[p,0]=1
            for t in range(1,9):V[p,t]=T[V[p,t-1],p+1]
        a.require(a.rank(V,T,iv)==9,'full nine-port Vandermonde')
        graphs={}
        for i in tight:
            rows=[k for k,D in enumerate(C)if set(layout['D4'][D])<=adj[i]]
            a.require(len(rows)==3,'three actual visible class ports')
            blocks=[V[np.ix_(rows,range(3*j,3*j+3))]for j in range(3)]
            G=np.vstack([inverse(M,T,iv)for M in blocks]);graphs[i]=G
            all_graphs.append({'class':class_index,'receiver':i,'visible_node_indices':rows,'T':G.tolist()})
        for j in donors:
            for h in sorted(H for J,H in quotas if J==j and H!=263):
                selected=[i for i in tight if h in views[j][i]]
                columns=[];names=[]
                for i in selected:
                    for col in range(3):
                        v=graphs[i][:,col]
                        candidate=np.column_stack(columns+[v])
                        if a.rank(candidate,T,iv)>len(columns):columns.append(v);names.append([i,col])
                        if len(columns)==9:break
                    if len(columns)==9:break
                a.require(len(columns)==9,'full common-lift annihilation span')
                a.require(a.rank(np.column_stack(columns),T,iv)==9,'exact nine-column span witness')
                certificates.append({'class':class_index,'donor':j,'other_plane':h,'witness_columns':names,'rank':9})
    a.require(len(certificates)==405 and len(all_graphs)==165,'complete common-lift coverage')
    # One receiver alone spans only3 scalar directions and cannot prove this gate.
    one=np.array(all_graphs[0]['T'],dtype=np.uint16)
    a.require(a.rank(one,T,iv)==3,'single-receiver scope control')
    pins=[]
    for p in [lp,bp,rp,pp]:
        raw=p.read_bytes();pins.append({'path':str(p.relative_to(args.repo)),'sha256':sha256(raw).hexdigest(),
           **({'decompressed_sha256':sha256(gzip.decompress(raw)).hexdigest()}if p.suffix=='.gz'else{})})
    result={'status':'PASS_COUPLED_SOURCE_AND_COMMON_LIFT_CERTIFICATES','source_pins':pins,
            'coupling':coupling,'joint_tight_receivers':tight,'common_lift_span_checks':405,
            'common_lift_rank_histogram':{'9':405},'single_receiver_scalar_rank_control':3,
            'common_lift_scope':'fixed GF512 V9 nodes1..9, one common J for all tight H263 receivers; arbitrary receiver-dependent kernel lifts remain open',
            'source_scope':'existence of five inequivalent coupled components; no selected complete coefficients or shared decoder',
            'complete_source_coefficients_emitted':False,'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'SPAN-WITNESSES.json').write_text(json.dumps(certificates,separators=(',',':'),sort_keys=True)+'\n')
    (args.out/'GRAPHS.json').write_text(json.dumps(all_graphs,separators=(',',':'),sort_keys=True)+'\n')
    print(result['status'], 'common-lift checks',len(certificates),'degree',coupling['individual_degree_bound'])

if __name__=='__main__':main()
