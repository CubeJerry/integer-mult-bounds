#!/usr/bin/env python3
"""Separate parity-equation solver and recovery of conjugated simplex families."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json


def need(x,m):
    if not x: raise ValueError(m)


def eye(n): return [1<<i for i in range(n)]


def product(A,B):
    out=[]
    for row in A:
        z=0
        for j in range(len(B)):
            if row>>j&1:z^=B[j]
        out.append(z)
    return out


def solve(equations,n):
    a=list(equations);p=[];r=0
    for j in range(n):
        z=next((z for z in range(r,len(a))if a[z]>>j&1),None)
        if z is None:continue
        a[r],a[z]=a[z],a[r]
        for k in range(len(a)):
            if k!=r and a[k]>>j&1:a[k]^=a[r]
        p.append(j);r+=1
    if any((row&((1<<n)-1))==0 and row>>n&1 for row in a):return None
    return sum(((a[k]>>n)&1)<<j for k,j in enumerate(p))


def inverse(A):
    n=len(A);a=[row|(1<<(n+i))for i,row in enumerate(A)]
    for j in range(n):
        z=next(z for z in range(j,n)if a[z]>>j&1);a[j],a[z]=a[z],a[j]
        for k in range(n):
            if k!=j and a[k]>>j&1:a[k]^=a[j]
    out=[x>>n for x in a];need(product(A,out)==eye(n),'inverse');return out


def factor(A,ncols):
    n=len(A);cols=[sum(((A[i]>>j)&1)<<i for i in range(n))for j in range(ncols)]
    basis={};chosen=[];coordinates=[]
    for col in cols:
        v=col;tag=0
        while v:
            lead=v.bit_length()-1
            if lead not in basis:
                index=len(chosen);chosen.append(col);tag^=1<<index;basis[lead]=(v,tag);v=0
            else:
                u,t=basis[lead];v^=u;tag^=t
        coordinates.append(tag)
    U=[sum(((col>>i)&1)<<j for j,col in enumerate(chosen))for i in range(n)]
    V=[sum(((tag>>i)&1)<<j for j,tag in enumerate(coordinates))for i in range(len(chosen))]
    need(product(U,V)==A,'full rank factorization');return U,V


def simplex(s):
    n=16*s;ones=(1<<16)-1;out=[]
    for h in range(17):
        u=1<<h if h<16 else ones;v=(1<<h)^ones if h<16 else ones
        rows=[v if u>>i&1 else 0 for i in range(16)]
        out.append([sum(1<<(j*s+t)for j in range(16)if row>>j&1)for row in rows for t in range(s)])
    return out


def recovery(s):
    n=16*s;original=simplex(s);T=eye(n)
    for k in range(3*n):
        i=(11*k+1)%n;j=(7*k+3)%n
        if i!=j:T[i]^=T[j]
    Ti=inverse(T);maps=[product(product(T,N),Ti)for N in original]
    Fs=[factor(N,n)for N in maps];need(all(len(V)==s for U,V in Fs),'full term ranks')
    U=[sum(Fs[h][0][i]<<(h*s)for h in range(17))for i in range(n)]
    V=[row for Uh,Vh in Fs for row in Vh]
    need(product(U,V)==eye(n),'factor UV identity')
    P=product(V,U);E=[row^(1<<i)for i,row in enumerate(P)];A,B=factor(E,17*s)
    need(len(B)==s,'rank-s complementary projection')
    Ablocks=[A[h*s:(h+1)*s]for h in range(17)]
    changed=[]
    for h,(Uh,Vh)in enumerate(Fs):
        Ah=Ablocks[h];inverse(Ah);changed.append(product(Uh,Ah))
    basis=[sum(changed[h][i]<<(h*s)for h in range(16))for i in range(n)]
    bi=inverse(basis)
    recovered=[product(product(bi,N),basis)for N in maps]
    need(recovered==original,'classification recovers canonical simplex from arbitrary factor bases')
    need(product(maps[0],maps[0])==[0]*n,'square-zero conjugate')
    return {'internal_width':s,'bank_dimension':n,'independent_column_factorizations':17,
            'complement_rank':s,'recovered_exact_standard_family':True}


def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True)
    ap.add_argument('--witnesses',type=Path,required=True);ap.add_argument('--proof',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    w=json.loads(raw);R=w['root_table'];H=[set(h)for h in w['A2']]
    O=[{j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0}for r in R[:111]]
    singles={next(j for j in h if j<111):h for h in H if sum(j<111 for j in h)==1}
    yes=[];no=[];sols={}
    for i in range(111):
        T=(O[i]&set(range(111)))-{j for j,h in singles.items()if h<=O[i]}
        rows=[sum(1<<j for j in h&T)for h in H if h<=O[i]]
        rows += [1<<j for j in range(111)if j not in T]
        rows += [sum(1<<j for j in T)|(1<<111)]
        solution=solve(rows,111)
        if solution is None:no.append(i)
        else:yes.append(i);sols[i]=solution
    wr=gzip.decompress(a.witnesses.read_bytes());author=json.loads(wr)
    need(len(yes)==87 and len(no)==24,'independent parity linear systems')
    need(set(yes)=={v['receiver']for v in author['witnesses']}and no==author['no_odd_witness_receivers'],'exact witness existence set')
    histogram=Counter()
    for v in author['witnesses']:
        i=v['receiver'];S=set(v['odd_donors']);T=set(v['tight_donors'])
        expected=(O[i]&set(range(111)))-{j for j,h in singles.items()if h<=O[i]}
        need(T==expected and S<=T and len(S)%2==1,'odd subset of exact tight donors')
        pairs=[]
        for h,P in enumerate(H):
            if P<=O[i]:
                need(len(P&S)in(0,2),'all plane intersections even')
                if len(P&S)==2:pairs.append([h,sorted(P&S)])
        need(pairs==v['paired_planes']and 2*len(pairs)==16*len(S),'every actual paired plane')
        histogram[len(S)]+=1
    result={'status':'PASS_INDEPENDENT_ODD_PLANE_ASYMMETRY_AND_SIMPLEX_CLASSIFICATION',
            'author_proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),
            'witnesses_uncompressed_sha256':sha256(wr).hexdigest(),'receivers_with_witness':len(yes),
            'receivers_with_no_odd_solution':no,'witness_size_histogram':dict(sorted(histogram.items())),
            'conjugacy_recovery_controls':[recovery(s)for s in(1,2)],'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])


if __name__=='__main__':main()
