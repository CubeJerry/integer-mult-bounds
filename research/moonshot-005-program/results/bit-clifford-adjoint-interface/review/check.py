#!/usr/bin/env python3
"""Separate trace-pairing and native Clifford review over F2 and F4."""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip,json,random

def need(ok,label):
    if not ok:raise ValueError(label)
def xor(values):
    z=0
    for x in values:z^=x
    return z
def matmul(A,B):
    return [xor(B[k]for k in range(len(B))if row>>k&1)for row in A]
def add(A,B):return [a^b for a,b in zip(A,B)]
def eye(n):return [1<<k for k in range(n)]
def dagger(A):
    n=len(A)
    return [sum(((A[n-1-j]>>(n-1-i))&1)<<j for j in range(n))for i in range(n)]
def native(layout,basis):
    cols=basis['lattice_basis_columns'];rows=[[Fraction(cols[j][i])for j in range(8)]+[Fraction(i==j)for j in range(8)]for i in range(8)]
    for c in range(8):
        p=next(i for i in range(c,8)if rows[i][c]);rows[c],rows[p]=rows[p],rows[c]
        x=rows[c][c];rows[c]=[v/x for v in rows[c]]
        for i in range(8):
            if i!=c:
                x=rows[i][c];rows[i]=[v-x*w for v,w in zip(rows[i],rows[c])]
    lookup={xor(basis['hyperbolic_basis_masks'][k]for k in range(8)if v>>k&1):v for v in range(256)}
    primitive=[]
    for axis in range(4):
        for creation in [True,False]:
            matrix=[0]*16
            for column in range(16):
                if bool(column>>axis&1)!=creation:matrix[column^(1<<axis)]|=1<<column
            primitive.append(matrix)
    answer=[]
    for root in layout['root_table']:
        cs=[sum(a*b for a,b in zip(row[8:],root))for row in rows]
        need(all(x.denominator==1 for x in cs),'exact native lattice coordinates')
        v=lookup[sum((int(x)&1)<<k for k,x in enumerate(cs))]
        gamma=[xor(primitive[k][i]for k in range(8)if v>>k&1)for i in range(16)]
        need(matmul(gamma,gamma)==eye(16),'native root square');answer.append(gamma)
    return answer

def fmul(a,b):
    out=0
    for bit in range(2):
        if b>>bit&1:out^=a<<bit
    if out&4:out^=7
    return out
def fm(A,B):return [[xor(fmul(x,y)for x,y in zip(row,col))for col in zip(*B)]for row in A]
def fa(A,B):return [[x^y for x,y in zip(a,b)]for a,b in zip(A,B)]
def fs(a,A):return [[fmul(a,x)for x in row]for row in A]
def fi(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def fd(A):return [[A[len(A)-1-j][len(A)-1-i]for j in range(len(A))]for i in range(len(A))]
def trace(A):return xor(A[i][i]for i in range(len(A)))
def fr(A):
    A=[row[:]for row in A];r=0
    for c in range(len(A[0])):
        p=next((i for i in range(r,len(A))if A[i][c]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];iv=next(x for x in range(1,4)if fmul(x,A[r][c])==1)
        A[r]=[fmul(iv,x)for x in A[r]]
        for i in range(r+1,len(A)):
            if A[i][c]:
                a=A[i][c];A[i]=[x^fmul(a,y)for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve();author=args.author.resolve();base=repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    raw=gzip.decompress(lp.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native layout pin')
    layout=json.loads(raw);gammas=native(layout,json.loads(bp.read_bytes()))
    need(len(gammas)==120 and all(dagger(G)==G for G in gammas),'all native roots self-adjoint')
    i,j=layout['A2'][370][:2];G,H=gammas[i],gammas[j];I=eye(16);basis=[I,G,H,matmul(G,H)]
    need(add(matmul(G,H),matmul(H,G))==I,'native anisotropic plane')
    need(dagger(matmul(G,H))==matmul(H,G)!=matmul(G,H),'adjoint reverses noncommuting product')
    one=both=0
    for coeff in product(range(2),repeat=4):
        C=[xor(c*B[k]for c,B in zip(coeff,basis))for k in range(16)]
        c1=matmul(C,G)==matmul(G,C);c2=matmul(C,H)==matmul(H,C)
        one+=c1;both+=c1 and c2
    need(one==4 and both==2,'native centralizer dimensions2 and1')
    identities=0;ordinary_faults=0
    for B in basis:
        for t in range(16):
            # Compute the pairing on each input matrix unit and output basis.
            adj=[[0]*16 for _ in range(256)]
            for r in range(16):
                for c in range(16):
                    for y in range(16):
                        left=((B[15-y]>>r)&1)if c==t else 0
                        target_row=16*(15-r)+(15-c)
                        adj[target_row][y]=left
            formula=[[0]*16 for _ in range(256)]
            Bd=dagger(B)
            for r in range(16):
                for y in range(16):formula[16*r+15-t][y]=(Bd[r]>>y)&1
            need(adj==formula,'complete native trace-adjoint basis formula')
            ordinary=[[((B[y]>>r)&1)if c==t else 0 for y in range(16)]for r in range(16)for c in range(16)]
            ordinary_faults+=ordinary!=adj;identities+=1
    need(identities==64 and ordinary_faults==64,'all64 paired maps and transpose controls')

    # A separate four-dimensional spinor model over F4.
    prim=[]
    for axis in range(2):
        for create in [True,False]:
            A=[[0]*4 for _ in range(4)]
            for c in range(4):
                if bool(c>>axis&1)!=create:A[c^(1<<axis)][c]=1
            prim.append(A)
    g=fa(prim[0],prim[1]);h=fa(prim[0],fa(prim[2],prim[3]));E=fi(4);zero=[[0]*4 for _ in range(4)]
    need(fm(g,g)==fm(h,h)==E and fa(fm(g,h),fm(h,g))==E,'separate F4 Clifford pair')
    one4=both4=rank_checks=endpoint_checks=0
    for coeff in product(range(4),repeat=4):
        C=zero
        for a,B in zip(coeff,[E,g,h,fm(g,h)]):C=fa(C,fs(a,B))
        c1=fm(C,g)==fm(g,C);c2=fm(C,h)==fm(h,C)
        one4+=c1;both4+=c1 and c2
        need((fm(fd(C),h)==fm(h,fd(C)))==c2,'mirrored receiver condition equals original donor condition')
        need(fr(fa(E,C))==fr(fa(E,fd(C))),'return rank is unchanged by paired adjoint')
        endpoint_checks+=1;rank_checks+=1
    need(one4==16 and both4==4,'F4 dimensions2 and1 without binary extrapolation')
    need(fm(g,g)==fm(g,g)and fm(fd(g),h)!=fm(h,fd(g)),'receiver-only covariance does not imply mirror')
    rng=random.Random(2801);trace_checks=0
    for trial in range(32):
        A=zero
        for a,B in zip([rng.randrange(4)for _ in range(4)],[E,g,h,fm(g,h)]):A=fa(A,fs(a,B))
        u=[rng.randrange(4)for _ in range(4)];y=[rng.randrange(4)for _ in range(4)]
        Ay=[row[0]for row in fm(fd(A),[[v]for v in y])]
        claimed=[[fmul(Ay[r],u[3-c])for c in range(4)]for r in range(4)]
        for r in range(4):
            for c in range(4):
                X=[[0]*4 for _ in range(4)];X[r][c]=1
                FX=[row[0]for row in fm(fm(A,X),[[v]for v in u])]
                left=xor(fmul(FX[k],y[3-k])for k in range(4))
                right=trace(fm(fd(X),claimed));need(left==right,'mixed F4 rank-one adjoint with correct order');trace_checks+=1
    result={'status':'PASS_INDEPENDENT_CLIFFORD_DUAL_INTERFACE_REVIEW','native_self_adjoint_roots':120,
            'native_full_adjoint_basis_maps':identities,'ordinary_transpose_failures':ordinary_faults,
            'native_one_root_centralizer_dimension':2,'native_two_root_centralizer_dimension':1,
            'source_parameter_dimensions':[64,32,16],
            'F4_centralizer_counts':[one4,both4],'F4_endpoint_criterion_checks':endpoint_checks,
            'F4_rank_invariance_checks':rank_checks,'F4_mixed_trace_pairing_checks':trace_checks,
            'scope':'paired adjoint and exact two-sided endpoint criterion; no physical reversal or decoder admission',
            'source_pins':[{'path':str(p.relative_to(repo)),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [lp,bp]],
            'author_pins':[{'path':str(p.relative_to(author)),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [author/'PROOF.md',author/'check.py',author/'algebra.py']],
            'no_new_kappa':True}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({'native_maps':identities,'F4_trace_checks':trace_checks,'parameters':[64,32,16]}))

if __name__=='__main__':main()
