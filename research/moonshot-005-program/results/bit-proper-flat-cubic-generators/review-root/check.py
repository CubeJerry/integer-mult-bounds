#!/usr/bin/env python3
"""Independent certificate review; no imports from the author implementation."""
import argparse, gzip, hashlib, itertools, json
from fractions import Fraction as F
from pathlib import Path
PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
    if not c: raise ValueError(m)
def rank2(rows):
    p={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in p: x^=p[j]
            else: p[j]=x; break
    return list(p.values())
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def rankq(rows):
    a=[list(map(F,r)) for r in rows]; k=0
    for j in range(8):
        t=next((t for t in range(k,len(a)) if a[t][j]),None)
        if t is None: continue
        a[k],a[t]=a[t],a[k]; v=a[k][j]; a[k]=[x/v for x in a[k]]
        for i in range(k+1,len(a)):
            v=a[i][j]; a[i]=[x-v*y for x,y in zip(a[i],a[k])]
        k+=1
    return k
def run(repo,certificate):
    raw=(repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'actual source pin')
    source=json.loads(gzip.decompress(raw)); roots=[]
    for j in range(111):
        r=list(map(F,source['frames'][str(source['start'][j])]['B'][0]))
        if sum(bool(x) for x in r)==1: r=[2*x for x in r]
        need(dot(r,r)==4 and all(x.denominator==1 for x in r),'normalized actual roots')
        roots.append(tuple(map(int,r)))
    c=json.loads(certificate.read_text()); full=list(map(tuple,c['full_roots']))
    # Reconstruct the completion using its 14 coordinate blocks, rather than accepting its table.
    blocks=sorted({tuple(i for i,x in enumerate(r) if x) for r in roots if sum(bool(x) for x in r)==4})
    actual=[tuple(2*int(i==j) for i in range(8)) for j in range(8)]
    for B in blocks:
        for s in itertools.product((-1,1),repeat=3):
            v=[0]*8;v[B[0]]=1
            for i,x in zip(B[1:],s):v[i]=x
            actual.append(tuple(v))
    need(len(blocks)==14 and full==actual and len(set(full))==120,'full real completion')
    index={r:i for i,r in enumerate(roots)}
    K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(roots)) for i,r in enumerate(roots)]
    C=rank2(K); Q2=rank2(a&b for a,b in itertools.combinations_with_replacement(C,2))
    Q3=rank2(a&b&d for a,b,d in itertools.combinations_with_replacement(C,3))
    need((len(C),len(Q2),len(Q3))==(9,36,84),'independent Schur ranks')
    words=[]
    def witness(w):
        A=set(w['full_frame0']);B=set(w['full_frame1']);common=A&B
        need(len(A)==len(B)==8 and len(common)==4,'two full frames')
        need(all(dot(full[i],full[j])==0 for S in (A,B) for i,j in itertools.combinations(S,2)),'actual full orthogonality')
        S=sorted(index[full[i]] for i in A^B if full[i] in index)
        need(S==w['native_difference'] and 5<=len(S)<=8,'actual punctured difference')
        need(rankq([roots[i] for i in S])==4,'rational rank four')
        need(all(dot(roots[i],full[j])==0 for i in S for j in common),'explicit proper-chart annihilator')
        m=sum(1<<i for i in S)
        need(len(rank2(Q3+[m]))==84,'cubic membership')
        return m
    for w in c['independent_generators']:words.append(witness(w))
    need(len(words)==len(rank2(words))==84,'84 independent proper-flat cubic generators')
    ell=witness(c['chosen_five_input_mode']); need(ell==sum(1<<i for i in (1,56,73,81,95)),'five actual inputs')
    half={}
    for i,r in enumerate(roots):
        key=(tuple(j for j,x in enumerate(r) if x),sum(x<0 for x in r)%2)
        half[key]=half.get(key,0)|(1<<i)
    CU=rank2(C+list(half.values()))
    need(len(half)==36 and len(CU)==39 and len(rank2(CU+[ell]))==40,'escape entire old halfclass reservoir')
    need(len(rank2(Q2+[ell]))==37,'escape entire quadratic reservoir')
    support=[i for i in range(111) if ell>>i&1]
    accessible=[j for j,r in enumerate(roots) if all(dot(r,roots[i])==0 for i in support)]
    need(accessible==[0,15,20,39,44,57,68,69,83,92,106,107],'exact facet availability')
    need(len(rank2(Q3+[ell^(1<<92)]))==85 and rankq([roots[i] for i in support+[92]])==5,'two advertised invalid mutations')
    need(len(rank2(words[:-1]))==83,'omit-basis-vector negative control')
    return {'status':'PASS_INDEPENDENT_PROPER_FLAT_CUBIC_BASIS','source_sha256':PIN,'author_certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'native_ports':111,'basis_size':84,'every_basis_real_rank':4,'candidate_support':support,'candidate_facets':accessible,'code_ranks':{'C':9,'Q2':36,'Q3':84,'C_plus_halfclass':39,'with_candidate':40},'negative_controls':['own coordinate leaves Q3','receiver root raises real rank to5','omit one basis vector gives rank83'],'author_census_independently_reenumerated':False,'literal_source_replay':False,'no_new_kappa':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=run(a.repo,a.certificate);a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
