#!/usr/bin/env python3
"""Independent exact native reconstruction for Gram-plus-one proper-local gate."""
import argparse,gzip,hashlib,json,itertools
from pathlib import Path
from collections import Counter

def need(q,s):
    if not q:raise ValueError(s)

def basis(xs):
    b={}
    for x in xs:
        while x:
            p=(x&-x).bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b

def root(n):
    if n.bit_count()==3:return [3*((n>>i)&1)-1 for i in range(9)]
    missing=[i for i in range(9)if not(n>>i&1)];need(len(missing)==2,'native root weights');a,b=missing
    return [3*((i==a)-(i==b))for i in range(9)]

def main():
    p=argparse.ArgumentParser()
    for s in ['package','output']:p.add_argument('--'+s,type=Path,required=True)
    a=p.parse_args();raw=(a.package/'dependencies/native.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin')
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='6b34df2903ab09247d9e443dc9a85a2e631b4970425421443e026f595b07bd11','proof pin')
    w=json.loads(gzip.decompress(raw));proof=json.load(gzip.open(a.package/'output/GEOMETRY.json.gz','rt'));ports=w['live'];need(len(set(ports))==104,'native104');norm={h:w['frames'][w['initial'][h]][0]for h in ports};r={h:root(norm[h])for h in ports}
    need({int(h):v for h,v in proof['normal_by_port'].items()}==norm,'certificate actual normals')
    need(all(len(w['frames'][w['initial'][h]])==1 and sum(r[h])==0 and sum(x*x for x in r[h])==18 for h in ports),'actual root realization')
    G={}
    for h in ports:
        for j in ports:
            d=sum(x*y for x,y in zip(r[h],r[j]));need(d%9==0,'twice Gram integral');G[h,j]=d//9
            need((h==j and G[h,j]==2)or(h!=j and G[h,j]in[-1,0,1]),'Gram entries')
            if h!=j:need(bool(G[h,j])==((norm[h]&norm[j]).bit_count()%2==0),'source incidence')
    for h in ports:
        f=w['frames'][w['final'][h+112]];need(len(f)==8 and len(basis(f))==8 and all((norm[h]&x).bit_count()%2==0 for x in f),'actual receiver facet')
        neigh=[j for j in ports if j!=h and G[h,j]];need(len(neigh)==48 and len(basis(norm[j]for j in neigh))==8,'full local facet span')
    pos={h:i for i,h in enumerate(ports)};adj=[sum(1<<pos[j]for j in ports if j!=h and G[h,j]==0)for h in ports];frames=[]
    def walk(chosen,remaining):
        if len(chosen)==8:frames.append(tuple(ports[i]for i in chosen));return
        while remaining:
            if remaining.bit_count()<8-len(chosen):return
            bit=remaining&-remaining;i=bit.bit_length()-1;remaining^=bit;walk(chosen+[i],remaining&adj[i])
    walk([], (1<<104)-1)
    claimed=[tuple(x)for x in proof['frames']];need(len(frames)==759 and set(frames)==set(claimed),'all authentic eightframes independently enumerated')
    pairs={(b,c)for b,c in itertools.combinations(ports,2)if G[b,c]==0};need(len(pairs)==2860,'orthogonal pair count');seen=set();hist=Counter();negative={}
    for z in proof['orthogonal_pairs']:
        b,c=z['pair'];need((b,c)in pairs and (b,c)not in seen,'exact pair coverage');seen.add((b,c));B=claimed[z['frame_index']];need(b in B and c in B,'authentic containing frame')
        for rec in z['directions']:
            h,k=rec['receiver'],rec['other'];need({h,k}=={b,c},'directed pair');S=[j for j in ports if j!=h and G[h,j]and not G[k,j]];hist[len(S)]+=1
            need(len(S)==rec['exclusive_count']and len(basis(norm[j]for j in S))==7,'exclusive span dimension7')
            need(all((norm[h]&norm[j]).bit_count()%2==0 and ((norm[k]^511)&norm[j]).bit_count()%2==0 for j in S),'exclusive inclusion')
            v=rec['basis'];need(len(set(v))==7 and set(v)<=set(S)and len(basis(norm[j]for j in v))==7,'exact exclusive witness')
        common=[j for j in ports if j not in[b,c]and G[b,j]and G[c,j]];need(len(common)==z['common_count'],'common count')
        u,v=z['common_same_sign'],z['common_opposite_sign'];need(u in common and v in common and G[b,u]*G[c,u]==1 and G[b,v]*G[c,v]==-1,'both forced scalar signs')
    need(seen==pairs and hist==Counter({24:56,26:1344,28:3840,30:480}),'all pair premises')
    B=claimed[0]
    need(all(2*G[h,j]==sum(G[h,b]*G[b,j]for b in B)for h in ports for j in ports),'exact frame factorization')
    need(all(sum(G[h,k]*G[k,j]for k in ports)==26*G[h,j]for h in ports for j in ports),'credited G squared identity')
    clique=proof['nonorthogonal_eight_clique'];need(len(set(clique))==8 and all(G[h,j]for h,j in itertools.combinations(clique,2)),'nonorthogonal eight control')
    need(len(basis(sum(1<<j for j in range(9)if j!=i)for i in range(9)))==8,'JplusI9 binary rank8')
    ex=proof['orthogonal_pairs'][0];v=ex['directions'][0]['basis'];negative['missing_exclusive_basis']=len(basis(norm[j]for j in v[:-1]))==6
    bad=list(B);bad[1]=bad[0];negative['duplicate_frame']=len(set(bad))<8
    b,c=ex['pair'];j=ex['common_same_sign'];negative['wrong_opposite_sign']=G[b,j]*G[c,j]!=-1
    need(all(negative.values()),'meaningful negative controls')
    out=dict(status='PASS_INDEPENDENT_GLOBAL_PREFIX_GEOMETRY',proof_sha256=hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest(),ports=104,independently_enumerated_frames=len(frames),orthogonal_pairs=len(pairs),directed_exclusive_spans=2*len(pairs),exclusive_count_histogram=dict(hist),frame_factorization_checks=104*104,actual_facet_checks=104,negative_controls=negative,scope='Separate native reconstruction and exact witnesses; operator proof directly reviewed. No supplier or new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(frames),len(pairs))
if __name__=='__main__':main()
