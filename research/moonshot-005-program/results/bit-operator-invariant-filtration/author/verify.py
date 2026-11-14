#!/usr/bin/env python3
"""Exact controls for the invariant-layer canonical quotient theorem.

Universal statements are proved separately in PROOF.md. This checker supplies
explicit native fitting and operator-algebra controls, not a search theorem.
Prepared for @CubeJerry with OpenAI assistance; Apache-2.0.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
import json
from pathlib import Path
import random

NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
DENSITY_PROOF='3f9b100c03dd998c371a4590ac4c23670eed41d9fe688008de6b4c74c5c23c66'
POINT_PROOF='f001063e2df55ed4b8df3c2f7231b0138da6e276ee046639f88ac4b17d310c72'
S1=[2,9,12,30,38,42]
S2=[2,26,63,65,81,87]


def require(ok,why):
    if not ok:
        raise ValueError(why)


def rank(rows):
    p={}
    for row in rows:
        while row:
            i=row.bit_length()-1
            if i in p:
                row ^= p[i]
            else:
                p[i]=row
                break
    return len(p)


def row_product(row,B):
    out=0
    while row:
        i=(row&-row).bit_length()-1
        out ^= B[i]
        row &= row-1
    return out


def product(A,B):
    return tuple(row_product(row,B) for row in A)


def xor(A,B):
    return tuple(a^b for a,b in zip(A,B))


def identity(v):
    return tuple(1<<a for a in range(v))


def unit(v,i,j):
    return tuple(1<<j if a==i else 0 for a in range(v))


def blocks(F,v):
    I=identity(v)
    Z=(0,)*v
    return [[I if F[i]>>j&1 else Z for j in range(111)] for i in range(111)]


def flatten(A,v):
    return [sum(A[i][j][a]<<(j*v) for j in range(111)) for i in range(111) for a in range(v)]


def inspect(A,K,v):
    I=identity(v)
    foreign=[]
    for i in range(111):
        require(A[i][i]==I,'identity diagonal')
        require(all(not any(A[i][j]) for j in range(111) if not K[i]>>j&1),'prescribed zero mask')
        foreign.append(sum(any(A[i][j]) for j in range(111) if j!=i))
    ell=sum(int(x>36)+int(x>52) for x in foreign)
    b=sum(x<=36 for x in foreign)
    rows=flatten(A,v)
    canonical=flatten(blocks(K,v),v)
    require(rank(canonical)==9*v,'canonical tensor dimension')
    d=rank(rows+canonical)-9*v
    if ell<=194:
        c=17-min(b,9)
        require(d>=v+(v+c-1)//c,'inherited density bound')
    return dict(V=v,rank=rank(rows),canonical_quotient=d,ell=ell,double_saving_rows=b,
                foreign_support_histogram=dict(sorted(Counter(foreign).items())))


def diagonal_layer(A,start,width):
    mask=(1<<width)-1
    return [[tuple((A[i][j][start+a]>>start)&mask for a in range(width))
             for j in range(111)] for i in range(111)]


def flag_check(A,K,parts):
    v=sum(parts)
    boundaries=[]
    n=0
    for w in parts[:-1]:
        n+=w
        boundaries.append(n)
    for row in A:
        for block in row:
            for cut in boundaries:
                require(all(not (block[a]&((1<<cut)-1)) for a in range(cut,v)),'common invariant flag')
    full=inspect(A,K,v)
    layers=[]
    at=0
    for w in parts:
        layers.append(inspect(diagonal_layer(A,at,w),K,w))
        at+=w
    require(all(layer['ell']<=full['ell'] for layer in layers),'support passes to every diagonal layer')
    require(full['canonical_quotient']>=sum(layer['canonical_quotient'] for layer in layers),'stacked rectangular rank inequality')
    c=17-min(full['double_saving_rows'],9)
    theoretical=v+sum((w+c-1)//c for w in parts)
    require(full['canonical_quotient']>=theoretical,'additive filtration bound')
    return dict(full=full,parts=parts,layers=layers,proved_lower_bound=theoretical)


def commutes(mats):
    return all(product(a,b)==product(b,a) for a in mats for b in mats)


def gf4_product(a,b):
    r=0
    while b:
        if b&1:
            r ^= a
        b >>= 1
        a <<= 1
        if a&4:
            a ^= 7
    return r


def gf4_matrix(A,B):
    return [[gf4_product(A[i][0],B[0][j])^gf4_product(A[i][1],B[1][j]) for j in range(2)] for i in range(2)]


def rectangular_controls():
    rng=random.Random(830114)
    records=[]
    for row_sizes,col_sizes in [([2,3],[3,1]),([1,2,3],[2,1,2]),([3,1,2],[1,3,2]),([2,2,2],[2,2,2])]:
        row_layer=[i for i,n in enumerate(row_sizes) for _ in range(n)]
        col_layer=[i for i,n in enumerate(col_sizes) for _ in range(n)]
        for case in range(16):
            M=[sum((rng.randrange(2) if row_layer[i]<=col_layer[j] else 0)<<j for j in range(len(col_layer)))
               for i in range(len(row_layer))]
            diagonal=[]
            for layer in range(len(row_sizes)):
                rid=[i for i,a in enumerate(row_layer) if a==layer]
                cid=[j for j,a in enumerate(col_layer) if a==layer]
                sub=[sum(((M[i]>>j)&1)<<b for b,j in enumerate(cid)) for i in rid]
                diagonal.append(rank(sub))
            require(rank(M)>=sum(diagonal),'rectangular upper-triangular rank lemma')
            records.append(dict(row_sizes=row_sizes,col_sizes=col_sizes,case=case,rank=rank(M),diagonal_ranks=diagonal))
    require(rank([3,3])==1<2,'nonzero below-diagonal control invalidates the sum bound')
    return records


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--density-proof',type=Path,required=True)
    p.add_argument('--point-proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    require(sha256(args.density_proof.read_bytes()).hexdigest()==DENSITY_PROOF,'density proof pin')
    require(sha256(args.point_proof.read_bytes()).hexdigest()==POINT_PROOF,'point handoff proof pin')
    raw=args.native.read_bytes()
    require(sha256(raw).hexdigest()==NATIVE,'native pin')
    source=json.loads(gzip.decompress(raw))
    roots=[list(map(Fraction,source['frames'][str(source['start'][i])]['B'][0])) for i in range(111)]
    ortho=[[sum(a*b for a,b in zip(x,y))==0 for y in roots] for x in roots]
    K=[sum(int(i==j or ortho[i][j])<<j for j in range(111)) for i in range(111)]
    require(rank(K)==9,'canonical rank')
    deg=[w.bit_count()-1 for w in K]
    I1=[i for i in range(111) if all(ortho[i][j] for j in S1) and deg[i]<=58]
    I2=[i for i in range(111) if all(ortho[i][j] for j in S2) and deg[i]<=58]
    require(len(I1)==len(I2)==17 and len(set(I1)&set(I2))==5,'two native seventeen-savings supports')
    h1=sum(1<<j for j in S1)
    h2=sum(1<<j for j in S2)
    F=[row^h1 if i in I1 else row^h2 if i in I2 else row for i,row in enumerate(K)]
    scalar=inspect(blocks(F,1),K,1)
    require(scalar['ell']==193 and scalar['rank']==11 and scalar['canonical_quotient']==2,'sharp commuting scalar fitting')
    require(len(set(S1)|set(S2))==11<=20,'point-retained handoff obstruction still applies')
    minor_rows=[]
    selected=[]
    for i,row in enumerate(F):
        if rank(selected+[row])>len(selected):
            selected.append(row)
            minor_rows.append(i)
    pivots={}
    for row in selected:
        while row:
            j=row.bit_length()-1
            if j in pivots:
                row ^= pivots[j]
            else:
                pivots[j]=row
                break
    minor_columns=sorted(pivots)
    restricted=[sum(((F[i]>>j)&1)<<a for a,j in enumerate(minor_columns)) for i in minor_rows]
    require(len(minor_rows)==len(minor_columns)==rank(restricted)==11,'explicit nonsingular eleven-by-eleven minor')
    scalar_artifact=dict(schema='native-binary-fitting-v1',native_sha256=NATIVE,
                         bit_order='least-significant bit is source port0',
                         canonical_rows_hex=[hex(row) for row in K],fitting_rows_hex=[hex(row) for row in F],
                         S1=S1,S2=S2,I1=I1,I2=I2,
                         selected_patch=[1 if i in I1 else 2 if i in I2 else 0 for i in range(111)],
                         nonsingular_minor=dict(receiver_rows=minor_rows,source_columns=minor_columns,rank=11),
                         code_dimension=11,canonical_quotient_dimension=2,ell=193,
                         physical_word_or_decoder=False)
    lifts=[]
    for v in [1,2,3,4,7]:
        r=flag_check(blocks(F,v),K,[1]*v)
        require(r['full']['canonical_quotient']==2*v and r['full']['rank']==11*v,'sharp tensor lift')
        lifts.append(r)
    contacts=[(i,j) for i in range(111) for j in range(111) if i!=j and F[i]>>j&1]
    p1,p2,p3=contacts[:3]

    # Commuting but not diagonalizable: a nonzero nilpotent part survives.
    I=identity(2)
    N=unit(2,0,1)
    require(any(N) and not any(product(N,N)),'genuine nilpotent')
    Jordan=xor(I,N)
    jordan=blocks(F,2)
    jordan[p1[0]][p1[1]]=Jordan
    require(commutes([I,Jordan,(0,0)]),'commuting Jordan family')
    jordan_result=flag_check(jordan,K,[1,1])

    # Commuting nonsplit F2 algebra, diagonalized over GF4 exactly.
    J=(2,3)
    require(xor(xor(product(J,J),J),I)==(0,0),'irreducible quadratic relation')
    def mv(M,x):
        return sum(((row&x).bit_count()%2)<<a for a,row in enumerate(M))
    require(all(mv(J,x)!=x for x in [1,2,3]),'no invariant F2 line')
    nonsplit=blocks(F,2)
    nonsplit[p1[0]][p1[1]]=J
    require(commutes([I,J,product(J,J),(0,0)]),'commuting extension-field family')
    nonsplit_result=inspect(nonsplit,K,2)
    require(nonsplit_result['canonical_quotient']>=4,'commuting bound without base-field splitting')
    P=[[1,1],[2,3]]
    Pinv=[[3,1],[2,1]]
    require(gf4_matrix(Pinv,P)==[[1,0],[0,1]],'GF4 eigenbasis inverse')
    require(gf4_matrix(gf4_matrix(Pinv,[[0,1],[1,1]]),P)==[[2,0],[0,3]],'exact GF4 splitting')

    # Noncommuting does not avoid the theorem when a complete flag remains.
    U=xor(identity(3),unit(3,0,1))
    W=xor(identity(3),unit(3,1,2))
    require(product(U,W)!=product(W,U),'noncommuting upper-triangular family')
    upper=blocks(F,3)
    upper[p1[0]][p1[1]]=U
    upper[p2[0]][p2[1]]=W
    upper_result=flag_check(upper,K,[1,1,1])

    # A genuine two-plus-three common flag, with lower entries inside layers.
    mixed=blocks(F,5)
    mixed[p1[0]][p1[1]]=xor(xor(identity(5),unit(5,0,1)),unit(5,2,3))
    mixed[p2[0]][p2[1]]=xor(xor(identity(5),unit(5,1,0)),unit(5,3,2))
    mixed[p3[0]][p3[1]]=xor(identity(5),unit(5,0,2))
    mixed_result=flag_check(mixed,K,[2,3])

    # Opposite nilpotents have no common eigenvector over any field:
    # their only eigenvalue is0 and their kernels are distinct lines.
    E12,E21=unit(2,0,1),unit(2,1,0)
    require(product(E12,E21)!=product(E21,E12),'irreducible pair noncommutes')
    require(rank(list(E12)+list(E21))==2,'their kernels intersect trivially')
    require(not any(product(E12,E12)) and not any(product(E21,E21)),'both nilpotent')
    nontriangular=blocks(F,2)
    nontriangular[p1[0]][p1[1]]=xor(I,E12)
    nontriangular[p2[0]][p2[1]]=xor(I,E21)
    nontriangular_result=inspect(nontriangular,K,2)
    # This example tests the scope boundary; it is not a cheap quotient code.

    rectangular=rectangular_controls()
    rounding=[]
    for v in [1,2,3,16,17,18,34,35,51,128]:
        for maximum in [1,2,3,5,17,18,32]:
            parts=[maximum]*(v//maximum)+([v%maximum] if v%maximum else [])
            additive=v+sum((w+16)//17 for w in parts)
            lower=v+(v+min(maximum,17)-1)//min(maximum,17)
            require(additive>=lower,'maximum layer-size consequence')
            rounding.append(dict(V=v,max_layer=maximum,parts=parts,additive=additive,coarse=lower))
    result=dict(status='PASS_OPERATOR_INVARIANT_FILTRATION_CONTROLS',
                native_sha256=NATIVE,density_proof_sha256=DENSITY_PROOF,point_proof_sha256=POINT_PROOF,
                explicit_scalar_fitting=dict(S1=S1,S2=S2,I1=I1,I2=I2,intersection=sorted(set(I1)&set(I2)),result=scalar),
                sharp_tensor_lifts=lifts,commuting_nondiagonalizable=jordan_result,
                commuting_nonsplit=nonsplit_result,GF4_diagonalization=dict(P=P,Pinv=Pinv,diagonal=[2,3]),
                noncommuting_triangular=upper_result,invariant_two_plus_three=mixed_result,
                nontriangularizable_scope_control=nontriangular_result,
                rectangular_rank_controls=rectangular,layer_rounding_controls=rounding,
                negative_controls=dict(commuting_does_not_require_diagonalizable=True,
                                       commuting_does_not_require_base_field_split=True,
                                       noncommuting_does_not_imply_no_flag=True,
                                       arbitrary_families_not_triangularizable=True,
                                       lower_block_zero_premise_essential=True),
                physical_realization_claimed=False,new_kappa=False,
                classification='Author all-field invariant-filtration proof plus exact finite controls; independent review pending.')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.output/'SCALAR-FITTING.json').write_text(json.dumps(scalar_artifact,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],scalar_ell=scalar['ell'],scalar_quotient=scalar['canonical_quotient'],
                         tensor_quotients=[r['full']['canonical_quotient'] for r in lifts],
                         Jordan_quotient=jordan_result['full']['canonical_quotient'],
                         nonsplit_quotient=nonsplit_result['canonical_quotient'],
                         triangular_noncommuting_quotient=upper_result['full']['canonical_quotient'],
                         mixed_flag_quotient=mixed_result['full']['canonical_quotient'])))


if __name__=='__main__':
    main()
