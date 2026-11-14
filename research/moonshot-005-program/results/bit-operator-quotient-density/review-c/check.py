#!/usr/bin/env python3
"""Independent exact checks for the proportional canonical quotient proof.

No author verifier, companion verifier, or author-generated matrix is imported.
The universal proof is reviewed in REVIEW.md. These are finite source/control
checks, not an exhaustive all-field or all-width search. Apache-2.0.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
import itertools
import json
from pathlib import Path

NATIVE = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
GEOMETRY = '9ef3fb7f23605f8f7dd053dfb3a42b1ea1f71ab0f6945e365481262e72e771a8'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def echelon(rows):
    piv = {}
    for r in rows:
        while r:
            n = r.bit_length()-1
            if n in piv:
                r ^= piv[n]
            else:
                piv[n] = r
                break
    return piv


def residue(x, piv):
    for n in sorted(piv,reverse=True):
        if x >> n & 1:
            x ^= piv[n]
    return x


def binary_rank(rows):
    return len(echelon(rows))


def all_combinations(rows):
    xs = [0]
    for r in rows:
        xs += [x ^ r for x in xs]
    return set(xs)


def tensor_scalar_fitting(F, width):
    return [[sum(1 << (j*width+a) for j in range(111) if F[i]>>j&1)
             for a in range(width)] for i in range(111)]


def fitting_incidence(A, K, width):
    canonical = echelon([r for block in tensor_scalar_fitting(K,width) for r in block])
    require(len(canonical)==9*width, 'canonical tensor dimension')
    quotients = [[residue(r,canonical) for r in block] for block in A]
    dim = binary_rank([r for block in quotients for r in block])
    weights = []
    point_weight = Counter()
    patterns = []
    for i,block in enumerate(A):
        mask = (1<<width)-1
        support = []
        for j in range(111):
            column_block = tuple((r>>(j*width))&mask for r in block)
            if i==j:
                require(column_block==tuple(1<<a for a in range(width)), 'diagonal identity')
            if not K[i]>>j&1:
                require(not any(column_block), 'forbidden block')
            if j!=i and any(column_block):
                support.append(j)
        ell = int(len(support)>36)+int(len(support)>52)
        weight = 2-ell
        weights.append(weight)
        if weight:
            require(binary_rank(quotients[i])==width, 'saving row injects full width')
            points = all_combinations(quotients[i])-{0}
            require(len(points)==(1<<width)-1, 'full image size')
            for p in points:
                point_weight[p] += weight
            patterns.append(dict(receiver=i,weight=weight,image_size=len(points)))
    total = sum(weights)
    maximum = max(point_weight.values(),default=0)
    require(maximum<=17, 'shared quotient vector weighted multiplicity')
    require(sum(point_weight.values())==total*((1<<width)-1), 'weighted incidence double count')
    require(total*((1<<width)-1)<=17*((1<<dim)-1), 'finite-field incidence bound')
    if total>17:
        require(dim>=width+(width+16)//17, 'proportional quotient gap')
    b = weights.count(2)
    if total>=28:
        denominator = 17-min(b,9)
        require(dim>=width+(width+denominator-1)//denominator, 'weighted refinement')
    return dict(V=width,canonical_quotient_dimension=dim,S=total,ell=222-total,
                double_saving_rows=b,maximum_weight_on_nonzero_vector=maximum,
                distinct_active_nonzero_vectors=len(point_weight),positive_row_images=patterns)


def multiply(a,b):
    out=0
    while b:
        if b&1:
            out ^= a
        b >>= 1
        a <<= 1
        if a&32:
            a ^= 0b100101
    return out


def power(a,n):
    out=1
    while n:
        if n&1:
            out=multiply(out,a)
        a=multiply(a,a)
        n >>= 1
    return out


def field_rank(rows):
    rows=[list(r) for r in rows]
    rank=0
    if not rows:
        return 0
    for j in range(len(rows[0])):
        p=next((i for i in range(rank,len(rows)) if rows[i][j]),None)
        if p is None:
            continue
        rows[rank],rows[p]=rows[p],rows[rank]
        inv=power(rows[rank][j],30)
        rows[rank]=[multiply(inv,x) for x in rows[rank]]
        for i in range(len(rows)):
            if i!=rank and rows[i][j]:
                c=rows[i][j]
                rows[i]=[x^multiply(c,y) for x,y in zip(rows[i],rows[rank])]
        rank += 1
    return rank


def polynomial(roots):
    p=[1]
    for a in roots:
        q=[0]*(len(p)+1)
        for j,c in enumerate(p):
            q[j] ^= multiply(a,c)
            q[j+1] ^= c
        p=q
    return p


def evaluate(poly,x):
    out=0
    for c in reversed(poly):
        out=multiply(out,x)^c
    return out


def review_field_arrangement():
    require({power(2,j) for j in range(31)}==set(range(1,32)), 'GF32 primitive element/all nonzero field values')
    for a in range(1,32):
        require(multiply(a,power(a,30))==1, 'every nonzero value invertible')
    # Field distributivity/associativity are additionally exhaustively checked.
    for a,b,c in itertools.product(range(32),repeat=3):
        require(multiply(a,b^c)==multiply(a,b)^multiply(a,c), 'field distributivity')
        require(multiply(multiply(a,b),c)==multiply(a,multiply(b,c)), 'field associativity')
    points=list(range(28))
    normals=[[power(a,j) for j in range(18)] for a in points]
    require(field_rank(normals)==18, 'ambient rank')
    tested=[]
    for start in range(28):
        ids=[(start+j)%28 for j in range(18)]
        require(field_rank([normals[i] for i in ids])==18, '18 distinct polynomial evaluations')
        require(field_rank([normals[i] for i in ids[:17]])==17, '17 independent evaluations')
        tested.append(ids)
    roots=points[:17]
    p=polynomial(roots)
    values=[evaluate(p,a) for a in points]
    require(len(p)==18 and p[-1]==1, 'degree exactly seventeen')
    require([a for a,v in zip(points,values) if v==0]==roots, 'exactly seventeen memberships')
    # Tensor lift: separate channel equations; 17/18 selected hyperplanes
    # have 34/36 independent scalar constraints on the 36-dimensional space.
    lifted=[]
    for normal in normals[:18]:
        for channel in range(2):
            lifted.append([normal[j] if b==channel else 0 for j in range(18) for b in range(2)])
    require(field_rank(lifted)==36 and field_rank(lifted[:34])==34, 'two-channel tensor lift')
    require(18 < 2*17, 'counterexample to abstract d>=2V')
    return dict(field_order=32,irreducible_polynomial_bits='100101',V=17,d=18,
                number_of_subspaces=28,weight_per_subspace=1,S=28,
                universal_argument='Degree-at-most-17 polynomial has at most 17 distinct roots over this field; not an exhaustive vector enumeration.',
                checked_18_subset_count=len(tested),seventeen_root_witness=p,
                witness_roots=roots,witness_values_on_28_points=values,
                sharp_pointwise_multiplicity=17,tensor_lift=dict(V=34,d=36,intersection_after17=2,intersection_after18=0))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--proof',type=Path,required=True)
    parser.add_argument('--native',type=Path,required=True)
    parser.add_argument('--programme',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    raw=args.native.read_bytes()
    require(sha256(raw).hexdigest()==NATIVE,'native source pin')
    geometric_path=args.programme/'results/bit-quotient-direction-savings/review/RESULT.json'
    require(sha256(geometric_path.read_bytes()).hexdigest()==GEOMETRY,'retained independent geometry pin')
    geo=json.loads(geometric_path.read_text())
    require(geo['max_rank3_eligible']==17 and geo['max_orthogonal4_eligible']==7,'retained exceptional geometry')
    source=json.loads(gzip.decompress(raw))
    roots=[tuple(map(Fraction,source['frames'][str(source['start'][i])]['B'][0])) for i in range(111)]
    K=[sum(int(i==j or sum(a*b for a,b in zip(x,y))==0)<<j for j,y in enumerate(roots)) for i,x in enumerate(roots)]
    mask=(1<<111)-1
    basis=list(echelon(K).values())
    require(len(basis)==9,'canonical dimension')
    for i in range(111):
        forbidden=mask^K[i]
        require(binary_rank([b&forbidden for b in basis])==8,'single local kernel')
        for j in range(i):
            require(binary_rank([b&forbidden&(mask^K[j]) for b in basis])==7,'pair local gluing rank')
    S=[0,2,38,41,42,45]
    U=[i for i in range(111) if i not in S and all(K[i]>>j&1 for j in S)]
    require(len(U)==20,'sharp source orthogonal set')
    h=sum(1<<j for j in S)
    sharpF=[r^h if i in U else r for i,r in enumerate(K)]
    largeS=[0,1,2,3,4,9,30,8]
    sm=sum(1<<j for j in largeS)
    sparseF=[1<<i if i in largeS else r&~sm for i,r in enumerate(K)]
    sharp=[fitting_incidence(tensor_scalar_fitting(sharpF,v),K,v) for v in [1,2,3]]
    sparse=[fitting_incidence(tensor_scalar_fitting(sparseF,v),K,v) for v in [1,2,3]]
    require(all(r['S']==17 and r['canonical_quotient_dimension']==r['V'] for r in sharp),'strict S>17 premise is necessary')
    require(all(r['S']==39 and r['ell']==183 for r in sparse),'actual larger-quotient source controls')

    # Abstract codimension arithmetic and its integer rounding, independent
    # of native source tests. Every row has an explicitly stated field rank.
    rounding=[]
    for v in [1,2,16,17,18,33,34,35,128]:
        for t in range(9,19):
            d=v+(v+t-2)//(t-1)
            require(v-(t-1)*(d-v)<=0,'dimension bound equality/above')
            require(v-(t-1)*(d-1-v)>0,'integer previous dimension cannot suffice')
            rounding.append([v,t,d])
    weighted=[]
    for b in range(15):
        single=max(0,28-2*b)
        if b>=9:
            chosen_double,chosen_single=9,0
        else:
            chosen_double,chosen_single=b,18-2*b
        require(chosen_double<=b and chosen_single<=single,'weighted selection exists')
        require(2*chosen_double+chosen_single>17,'selected weight exceeds17')
        require(chosen_double+chosen_single-1==17-min(b,9),'weighted denominator')
        weighted.append(dict(b=b,n1=single,t=chosen_double+chosen_single))
    # Three planes may intersect pairwise without a common nonzero vector.
    pair_planes=[0b001,0b010,0b100]
    require(all(3-binary_rank(list(pair))==1 for pair in itertools.combinations(pair_planes,2)),'pairwise nonzero intersections')
    require(3-binary_rank(pair_planes)==0,'common intersection zero')
    # Below the eighteen-subspace bound V=34,d=35, coordinate hyperplanes
    # retain a 17-dimensional common intersection. Equality uses codim2.
    below=[1<<j for j in range(18)]
    equal=[1<<j for j in range(36)]
    require(35-binary_rank(below)==17 and 36-binary_rank(equal)==0,'dimensional controls')

    field=review_field_arrangement()
    result=dict(status='PASS_INDEPENDENT_OPERATOR_QUOTIENT_DENSITY_REVIEW',
                author_proof_sha256=sha256(args.proof.read_bytes()).hexdigest(),
                native_sha256=NATIVE,retained_geometry_sha256=GEOMETRY,
                author_verifier_imported_or_run=False,companion_verifier_imported_or_run=False,
                source_restriction_counts=dict(single=111,pair=6105),
                sharp_native_fitting_controls=sharp,sparse_native_fitting_controls=sparse,
                weighted_selection_controls=weighted,integer_rounding_controls=rounding,
                abstract_GF32_sharpness=field,
                negative_controls=dict(S_at_least17_not_sufficient=True,
                                       abstract_d_at_least_2V_false=True,
                                       pairwise_intersection_not_common=True,
                                       rounding_down_rejected=True),
                limits='Finite native/field examples plus separately reviewed universal proof; prior exceptional root geometry authenticated and reused, not rerun.',
                classification='Independent proof review accepts the stated all-field/all-width quotient theorem and conditional target corollary. No physical source, supplier or new kappa.')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],native_sharp_S=[x['S'] for x in sharp],
                         native_sparse_S=[x['S'] for x in sparse],
                         abstract_sharp_V=17,abstract_sharp_d=18,abstract_total_savings=28)))


if __name__=='__main__':
    main()
