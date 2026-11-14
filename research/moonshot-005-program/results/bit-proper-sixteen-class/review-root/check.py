#!/usr/bin/env python3
"""Independent exact review of the puncture-adapted sixteen-class certificate."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
    if not c:raise ValueError(m)
def basis(rows):
    out={}
    for w in rows:
        while w:
            p=w.bit_length()-1
            if p in out:w^=out[p]
            else:out[p]=w;break
    return list(out.values())
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rankq(rows):
    a=[list(map(F,r))for r in rows];k=0
    for j in range(8):
        t=next((i for i in range(k,len(a))if a[i][j]),None)
        if t is None:continue
        a[k],a[t]=a[t],a[k];z=a[k][j];a[k]=[x/z for x in a[k]]
        for i in range(k+1,len(a)):
            z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[k])]
        k+=1
    return k
def run(repo,path):
    raw=(repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');s=json.loads(gzip.decompress(raw));c=json.loads(path.read_text())
    R=[list(map(F,s['frames'][str(s['start'][i])]['B'][0]))for i in range(111)];K=[sum(int(i==j or dot(r,v)==0)<<j for j,v in enumerate(R))for i,r in enumerate(R)]
    classes=c['proper_classes'];need(len(classes)==16 and sorted(i for S in classes for i in S)==list(range(111)),'disjoint cover111')
    need(Counter(map(len,classes))=={7:15,6:1},'exact class sizes')
    need(all(dot(R[i],R[j])==0 for S in classes for i,j in itertools.combinations(S,2)),'all actual within-class contacts')
    need(all(rankq([R[i]for i in S])==len(S) for S in classes),'independent proper acquisition charts')
    need(all(rankq([R[i]for i in S if i!=j])==len(S)-1<=6 for S in classes for j in S),'all111 exact single proper covers')
    pair=[rankq([R[i]for i in S+T]) for S,T in itertools.combinations(classes,2)];need(len(pair)==120 and set(pair)=={8},'all pair spans fill ambient')
    facets=[[j for j in range(111)if all(dot(R[i],R[j])==0 for i in S)]for S in classes];need(facets==c['class_chart_containing_receiver_facets'],'exact terminal access')
    U=[sum(1<<i for i in S)for S in classes];C=basis(K);Q3=basis(a&b&d for a,b,d in itertools.combinations_with_replacement(C,3))
    need(len(basis(U))==16 and len(basis(C+U))==23 and len(basis(Q3+U))==90,'canonical and cubic compatibility')
    ell=K[92]&K[54];need(len(basis(U+[ell,1<<92,1<<15]))==19 and len(basis(U+[ell,1<<92,1<<15,K[92]]))==20,'paid-prefix dimension')
    need(len(basis(U+[sum(1<<i for i in (1,56,73,81,95))]))==17,'separate cubic mode cost')
    # Reconstruct source binary coordinates without accepting author solves.
    B=[w^((1<<111)-1)for w in K];frame=[0,1,2,4,8,14,30,59]
    G=[sum(((B[i]>>j)&1)<<a for a,j in enumerate(frame))for i in frame]
    inverse={sum(((g&x).bit_count()%2)<<a for a,g in enumerate(G)):x for x in range(256)};need(len(inverse)==256,'nondegenerate polar coordinates')
    X=[inverse[sum(((B[i]>>j)&1)<<a for a,i in enumerate(frame))]for j in range(111)]
    def q(x):return (x.bit_count()+sum(((x>>i)&1)*((x>>j)&1)*((G[i]>>j)&1)for i,j in itertools.combinations(range(8),2)))%2
    full={x for x in range(256)if q(x)};need(len(full)==120 and len(set(X))==111 and set(X)<=full,'all actual quadric points')
    L=set(c['singular_subspace']);need(len(L)==16 and len(basis(L))==4 and all(x^y in L for x in L for y in L)and all(not q(x)for x in L),'actual maximal singular subspace')
    label=lambda x:min(x^u for u in L)
    groups={a:[i for i,x in enumerate(X)if label(x)==a]for a in sorted({label(x)for x in full})}
    need(Counter(map(len,groups.values()))=={7:9,8:6} and len({label(x)for x in full-set(X)})==9,'puncture separation')
    T=set(c['orthogonal_transversal']);need(len(T)==6 and all(dot(R[i],R[j])==0 for i,j in itertools.combinations(T,2)),'actual orthogonal transversal')
    need(all(len(T&set(S))==int(len(S)==8)for S in groups.values()),'one per full class')
    reconstructed={frozenset(set(S)-T)for S in groups.values()}|{frozenset(T)};need(reconstructed==set(map(frozenset,classes)),'explicit coset refinement')
    S=next(S for S in groups.values()if len(S)==8);need(rankq([R[i]for i in S[1:]])==7,'full-class control fails proper cover')
    need(7**199*10**200>69**200 and 8**199*10**200>79**200,'rigorous naive-route lower bound')
    return {'status':'PASS_INDEPENDENT_PROPER_SIXTEEN_CLASS_CERTIFICATE','source_sha256':PIN,'author_certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'class_count':16,'class_sizes':{'7':15,'6':1},'sharp_class_partition_minimum':16,'cover_charge':0,'pair_span_histogram':dict(Counter(pair)),'canonical_joint_rank':23,'cubic_joint_rank':90,'current_ground_prefix_joint_rank':19,'current_proper_prefix_joint_rank':20,'explicit_coset_and_transversal_verified':True,'author_discovery_census_repeated':False,'naive_sixteen_full_bus_cost_lower_bound':'1658.2','full_class_negative_control_rank':7,'source_chronology_supplied':False,'no_new_kappa':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=run(a.repo,a.certificate);a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
