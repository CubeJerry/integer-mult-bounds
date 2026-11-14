#!/usr/bin/env python3
"""Finite controls for the all-field support-scalarization lemma.

These exact F2 constructions are controls, not the all-field/all-width proof.
No predecessor verifier is imported. @CubeJerry/OpenAI assistance; Apache-2.0.
"""
import argparse
from fractions import Fraction
import gzip
from hashlib import sha256
import json
from pathlib import Path

NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PINS={
    'results/bit-quotient-direction-savings/author/PROOF.md':'8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b',
    'results/bit-quotient-direction-savings/review/REVIEW.md':'60cf45eceae4f3cd3dcd658e59fcbce7a3c626decc7eaefcf4e65ea42f980612',
    'results/bit-all-route-rank-gap/ADMISSION.md':'871510f1d9eb76e66b4efe737274af719100e610c375343e78859ba08da062c7',
}


def need(ok,why):
    if not ok:
        raise ValueError(why)


def echelon(rows):
    p={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in p:
                x ^= p[j]
            else:
                p[j]=x
                break
    return p


def rank(rows):
    return len(echelon(rows))


def reduce(row,p):
    for j in sorted(p,reverse=True):
        if row>>j&1:
            row ^= p[j]
    return row


def combine(mask,rows):
    result=0
    for j,row in enumerate(rows):
        if mask>>j&1:
            result ^= row
    return result


def lift(row,v,channel,n):
    return sum(1<<(j*v+channel) for j in range(n) if row>>j&1)


def tensor_basis(B,v,n):
    return [lift(row,v,a,n) for row in B for a in range(v)]


def scalar_tensor(F,v,n):
    return [[lift(row,v,a,n) for a in range(v)] for row in F]


def whole_support(blockrow,v,n):
    union=0
    for row in blockrow:
        union |= row
    mask=(1<<v)-1
    return sum(1<<j for j in range(n) if (union>>(j*v))&mask)


def scalarize(A,B,v,n):
    bbase=echelon(tensor_basis(B,v,n))
    delta=rank([row for block in A for row in block]+list(bbase.values()))-len(bbase)
    need(delta<v,'strict subwidth premise')
    F=[]
    witnesses=[]
    mask=(1<<v)-1
    for i,block in enumerate(A):
        need(tuple((row>>(i*v))&mask for row in block)==tuple(1<<a for a in range(v)),'identity diagonal')
        residuals=[reduce(row,bbase) for row in block]
        piv={}
        u=None
        for a,res in enumerate(residuals):
            coeff=1<<a
            while res:
                j=res.bit_length()-1
                if j in piv:
                    old,oldcoeff=piv[j]
                    res ^= old
                    coeff ^= oldcoeff
                else:
                    piv[j]=(res,coeff)
                    break
            if not res:
                u=coeff
                break
        need(u is not None and u!=0,'nonzero rowwise quotient kernel')
        in_code=combine(u,block)
        need(not reduce(in_code,bbase),'selected row belongs to scalar tensor code')
        need((in_code>>(i*v))&mask==u,'own coefficient equals kernel vector')
        coordinate=(u&-u).bit_length()-1
        row=sum(((in_code>>(j*v+coordinate))&1)<<j for j in range(n))
        need(row>>i&1,'scalar diagonal one')
        need(rank(B+[row])==rank(B),'scalar row belongs to B')
        need(not row&~whole_support(block,v,n),'scalar support contained in block support')
        F.append(row)
        witnesses.append(dict(receiver=i,kernel_vector=u,functional_coordinate=coordinate,scalar_row=hex(row)))
    return dict(n=n,V=v,scalar_code_dimension=rank(B),extra_quotient_dimension=delta,
                scalar_rows_hex=[hex(x) for x in F],rowwise_witnesses=witnesses)


def product(A,B):
    return tuple(combine(row,B) for row in A)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--programme',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    for path,pin in PINS.items():
        need(sha256((args.programme/path).read_bytes()).hexdigest()==pin,'dependency pin: '+path)
    cases=[]
    # A common one-dimensional innovation, but different receiver kernel
    # vectors and noncommuting singular/shear foreign blocks.
    A=scalar_tensor([7,7,7],2,3)
    extra=1
    A[1][0] ^= extra
    A[2][1] ^= extra
    c=scalarize(A,[7],2,3)
    need(c['extra_quotient_dimension']==1 and len({x['kernel_vector'] for x in c['rowwise_witnesses']})>1,'different valid rowwise kernels')
    M=(0,2)
    N=(1,3)
    need(product(M,N)!=product(N,M),'noncommuting foreign block control')
    cases.append(c)
    # Non-repetition code and two extra dimensions below width three.
    B=[15,3]
    A=scalar_tensor([3,3,12,12],3,4)
    for i in range(4):
        if i!=0:
            A[i][i%3] ^= 1
        if i!=1:
            A[i][(i+1)%3] ^= 1<<(3+1)
    c=scalarize(A,B,3,4)
    need(c['extra_quotient_dimension']==2,'two-dimensional subwidth example')
    cases.append(c)

    boundary=[]
    for v in [1,2,3,5]:
        A=scalar_tensor([1,2],v,2)
        Bv=tensor_basis([3],v,2)
        delta=rank([r for block in A for r in block]+Bv)-rank(Bv)
        need(delta==v,'strict inequality boundary exact')
        row_images=[rank(Bv+block)-rank(Bv) for block in A]
        need(row_images==[v,v],'support improvement forces full-width row images')
        # B has only two binary words; its diagonal-one rows are [1,1].
        need(all(whole_support(A[i],v,2)==1<<i for i in range(2)),'identity block foreign support empty')
        rejected=False
        try:
            scalarize(A,[3],v,2)
        except ValueError as err:
            rejected=str(err)=='strict subwidth premise'
        need(rejected,'boundary not admitted by scalarizer')
        boundary.append(dict(V=v,delta=delta,row_quotient_dimensions=row_images,rejected=rejected))
    missing=False
    try:
        scalarize([[0,0]],[],2,1)
    except ValueError as err:
        missing=str(err)=='identity diagonal'
    need(missing,'zero matrix cannot replace identity diagonal')

    # A three-dimensional graph in D tensor F2^2 has no full scalar line.
    T=(4,5,2)
    graph=[]
    for j in range(3):
        image=sum(((T[a]>>j)&1)<<a for a in range(3))
        graph.append((1<<(2*j))|sum(((image>>a)&1)<<(2*a+1) for a in range(3)))
    gbase=echelon(graph)
    need(len(gbase)==3,'graph quotient dimension')
    line_containment=[]
    for h in range(1,8):
        x=sum(((h>>a)&1)<<(2*a) for a in range(3))
        y=x<<1
        contains=not reduce(x,gbase) and not reduce(y,gbase)
        line_containment.append(contains)
        need(not contains,'graph contains no full scalar line tensor')

    raw=args.native.read_bytes()
    need(sha256(raw).hexdigest()==NATIVE,'native pin')
    native=json.loads(gzip.decompress(raw))
    roots=[list(map(Fraction,native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
    ortho=[[sum(a*b for a,b in zip(x,y))==0 for y in roots] for x in roots]
    K=[sum(int(i==j or ortho[i][j])<<j for j in range(111)) for i in range(111)]
    S1=[2,9,12,30,38,42]
    S2=[2,26,63,65,81,87]
    h1=sum(1<<j for j in S1)
    h2=sum(1<<j for j in S2)
    U1={i for i in range(111) if all(ortho[i][j] for j in S1)}
    U2={i for i in range(111) if all(ortho[i][j] for j in S2)}
    F=[row^h1^h2 if i in U1&U2 else row^h1 if i in U1 and row.bit_count()-1<=58 else row^h2 if i in U2 and row.bit_count()-1<=58 else row for i,row in enumerate(K)]
    ell=sum(int(row.bit_count()-1>36)+int(row.bit_count()-1>52) for row in F)
    need(ell==192 and rank(F+K)==11 and rank(K)==9,'native strict double-width boundary')
    native_controls=[]
    for v in [1,2,3]:
        rows=[r for block in scalar_tensor(F,v,111) for r in block]
        Cv=tensor_basis(K,v,111)
        Bv=tensor_basis(K+[h1],v,111)
        d=rank(rows+Cv)-rank(Cv)
        delta=rank(rows+Bv)-rank(Bv)
        need(d==2*v and delta==v,'native boundary dimensions')
        native_controls.append(dict(V=v,d=d,extra_over_one_line=delta,ell=ell))
    result=dict(status='PASS_SUBWIDTH_SUPPORT_SCALARIZATION_CONTROLS',native_sha256=NATIVE,
                dependency_sha256=PINS,source_free_cases=cases,strict_width_controls=boundary,
                missing_identity_diagonal_rejected=missing,
                line_free_graph_control=dict(quotient_dimension=3,basis_coefficients=graph,
                                             all_seven_binary_full_lines_absent=not any(line_containment),
                                             physical_or_fitting_realization_claimed=False),
                native_double_width_boundary=native_controls,
                universal_scope='Support scalarization over every field and width; native corollary characteristic two. These finite checks use F2.',
                classification='Author theorem and exact controls; independent review pending; no new kappa.')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],source_free_extra_dimensions=[c['extra_quotient_dimension'] for c in cases],
                         boundary_widths=[x['V'] for x in boundary],native_boundary_ell=ell,
                         line_free_graph_dimension=3)))


if __name__=='__main__':
    main()
