#!/usr/bin/env python3
"""Native availability and exhaustive width-two hyperplane fitting checks.

The universal proper-quotient theorem is proved separately. The finite search
is exactly all 15 hyperplanes in the declared four-dimensional binary tensor
quotient, with independent affine row choices and fixed identity diagonals.
"""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
import itertools
import json
from pathlib import Path

NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
S1=[2,9,12,30,38,42]
S2=[2,26,63,65,81,87]


def need(ok,why):
    if not ok:
        raise ValueError(why)


def echelon(rows):
    p={}
    for row in rows:
        while row:
            j=row.bit_length()-1
            if j in p:
                row ^= p[j]
            else:
                p[j]=row
                break
    return p


def rank(rows):
    return len(echelon(rows))


def reduce(row,p):
    for j in sorted(p,reverse=True):
        if row>>j&1:
            row ^= p[j]
    return row


def combos(rows):
    out=[0]
    for row in rows:
        out += [x^row for x in out]
    return out


def lift(row,channel):
    return sum(1<<(2*j+channel) for j in range(111) if row>>j&1)


def linear_combination(mask,rows):
    out=0
    for j,row in enumerate(rows):
        if mask>>j&1:
            out ^= row
    return out


def allowed_kernel(basis,forbidden):
    piv={}
    kernel=[]
    for full in basis:
        restricted=full&forbidden
        while restricted:
            j=restricted.bit_length()-1
            if j in piv:
                old_restricted,old_full=piv[j]
                restricted ^= old_restricted
                full ^= old_full
            else:
                piv[j]=(restricted,full)
                break
        if not restricted:
            kernel.append(full)
    need(rank(kernel)==len(kernel),'allowed kernel basis independent')
    need(all(not row&forbidden for row in kernel),'allowed kernel forbidden zeros')
    return kernel


def diagonal_affine(kernel,receiver):
    piv={}
    null=[]
    for full in kernel:
        diag=(full>>(2*receiver))&3
        while diag:
            j=diag.bit_length()-1
            if j in piv:
                old_diag,old_full=piv[j]
                diag ^= old_diag
                full ^= old_full
            else:
                piv[j]=(diag,full)
                break
        if not diag:
            null.append(full)
    need(len(piv)==2,'all diagonal value vectors available')
    particular=[]
    for target in [1,2]:
        full=0
        while target:
            j=target.bit_length()-1
            diag,word=piv[j]
            target ^= diag
            full ^= word
        particular.append(full)
    need(rank(null)==len(null),'diagonal-zero kernel independent')
    for r,p in enumerate(particular):
        need((p>>(2*receiver))&3==1<<r,'particular identity row')
    return particular,null


def support(row):
    return sum(1<<j for j in range(111) if (row>>(2*j))&3)


def optimize_code(K,canonical,extra):
    basis=canonical+extra
    need(rank(basis)==len(basis),'fixed code basis independent')
    full=(1<<111)-1
    fitting=[]
    minima=[]
    counts=[]
    nullities=[]
    for i in range(111):
        forbidden_scalar=full^K[i]
        forbidden=lift(forbidden_scalar,0)|lift(forbidden_scalar,1)
        kernel=allowed_kernel(basis,forbidden)
        particular,null=diagonal_affine(kernel,i)
        variations=combos(null)
        row0=[(x^particular[0],support(x^particular[0])) for x in variations]
        row1=[(x^particular[1],support(x^particular[1])) for x in variations]
        best=None
        for (r0,s0),(r1,s1) in itertools.product(row0,row1):
            foreign=(s0|s1).bit_count()-1
            key=(foreign,r0,r1)
            if best is None or key<best:
                best=key
        foreign,r0,r1=best
        need((r0>>(2*i))&3==1 and (r1>>(2*i))&3==2,'winner identity diagonal')
        need(not (r0|r1)&forbidden,'winner forbidden zeros')
        fitting.extend([r0,r1])
        minima.append(foreign)
        counts.append(len(row0)*len(row1))
        nullities.append(len(null))
    ell=sum(int(x>36)+int(x>52) for x in minima)
    qdim=rank(canonical+fitting)-18
    return dict(minimum_ell=ell,savings=222-ell,canonical_quotient_dimension=qdim,
                fitting_rank=rank(fitting),row_minimum_foreign_support=minima,
                row_affine_nullities=nullities,row_pairs_examined=counts,
                total_row_pairs_examined=sum(counts),fitting_rows_hex=[hex(x) for x in fitting])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--native',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    blob=args.native.read_bytes()
    need(sha256(blob).hexdigest()==NATIVE,'native pin')
    native=json.loads(gzip.decompress(blob))
    roots=[list(map(Fraction,native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
    ortho=[[sum(a*b for a,b in zip(x,y))==0 for y in roots] for x in roots]
    K=[sum(int(i==j or ortho[i][j])<<j for j in range(111)) for i in range(111)]
    basis=[]
    for row in K:
        if rank(basis+[row])>len(basis):
            basis.append(row)
    need(len(basis)==9,'canonical basis')
    h1=sum(1<<j for j in S1)
    h2=sum(1<<j for j in S2)
    need(rank(basis+[h1,h2])==11,'independent two-patch quotient')
    full=(1<<111)-1
    records=[]
    categories={():[],(1,):[],(2,):[],(3,):[],(1,2,3):[]}
    for i in range(111):
        forbidden=full^K[i]
        p=echelon([w&forbidden for w in basis])
        need(len(p)==8,'local canonical kernel')
        residuals=[reduce(h1&forbidden,p),reduce(h2&forbidden,p)]
        available=tuple(j for j in [1,2,3] if not linear_combination(j,residuals))
        need(available in categories,'binary two-direction availability subspace')
        categories[available].append(i)
        records.append(dict(receiver=i,available_nonzero_directions=list(available),
                            restriction_quotient_rank=rank(residuals),
                            canonical_foreign_degree=K[i].bit_count()-1))
    expected_both=[33,57,68,79,102,106]
    need(categories[(1,2,3)]==expected_both,'six doubly available receivers')
    need([len(categories[x]) for x in [(),(1,),(2,),(3,),(1,2,3)]]==[77,14,14,0,6],'availability census')
    U1=sorted(categories[(1,)]+categories[(1,2,3)])
    U2=sorted(categories[(2,)]+categories[(1,2,3)])
    need(U1==[i for i in range(111) if all(ortho[i][j] for j in S1)],'availability h1 is actual common perpendicular')
    need(U2==[i for i in range(111) if all(ortho[i][j] for j in S2)],'availability h2 is actual common perpendicular')
    need(all(i not in set(S1)|set(S2) for i in expected_both),'both-available receivers outside innovation support')
    need(len(set(S1)|set(S2))==11,'union support size')
    need(min(K[i].bit_count()-1 for i in range(111))==55,'no two-unit savings from at most11 deletions')
    eligible1=[i for i in U1 if K[i].bit_count()-1<=58]
    eligible2=[i for i in U2 if K[i].bit_count()-1<=58]
    need(len(eligible1)==len(eligible2)==17,'single-patch degree count')
    need([K[i].bit_count()-1 for i in expected_both]==[60,58,58,58,58,58],'double-availability degrees')
    canonical=[lift(w,a) for w in basis for a in range(2)]
    tensor_extra=[lift(h1,0),lift(h1,1),lift(h2,0),lift(h2,1)]
    runs=[]
    for normal in range(1,16):
        coeffs=[]
        for c in range(1,16):
            if not (normal&c).bit_count()%2 and rank(coeffs+[c])>len(coeffs):
                coeffs.append(c)
        need(len(coeffs)==3,'hyperplane basis')
        extra=[linear_combination(c,tensor_extra) for c in coeffs]
        result=optimize_code(K,canonical,extra)
        need(result['canonical_quotient_dimension']<=3,'fitting inside fixed hyperplane')
        need(result['minimum_ell']>=205,'universal proper-quotient theorem')
        result.update(normal=normal,hyperplane_basis_coefficients=coeffs,
                      contains_full_h1_tensor=(normal&3)==0,
                      contains_full_h2_tensor=(normal>>2)==0,
                      contains_full_hsum_tensor=(normal&3)==(normal>>2))
        predicted=205 if result['contains_full_h1_tensor'] or result['contains_full_h2_tensor'] else 216 if result['contains_full_hsum_tensor'] else 222
        need(result['minimum_ell']==predicted,'exact all-width classification at this binary hyperplane')
        runs.append(result)
    census=dict(sorted(Counter(x['minimum_ell'] for x in runs).items()))
    need(census=={205:6,216:3,222:6},'exact width-two optimum census')
    unrestricted=optimize_code(K,canonical,tensor_extra)
    need(unrestricted['canonical_quotient_dimension']==4 and unrestricted['minimum_ell']<=194,'full tensor quotient escapes proper-space gate')
    # The one-patch tensor realizes the universal lower bound205 at d=V.
    one_patch=optimize_code(K,canonical,tensor_extra[:2])
    need(one_patch['minimum_ell']==205 and one_patch['canonical_quotient_dimension']==2,'sharp proper-quotient control')
    F=[]
    for i,row in enumerate(K):
        if i in expected_both:
            row ^= h1^h2
        elif i in eligible1:
            row ^= h1
        elif i in eligible2:
            row ^= h2
        F.append(row)
    scalar_ell=sum(int(row.bit_count()-1>36)+int(row.bit_count()-1>52) for row in F)
    need(scalar_ell==192 and rank(F)==11 and rank(F+basis)==11,'explicit full scalar control')
    need(all(row>>i&1 and not row&(full^K[i]) for i,row in enumerate(F)),'full scalar fitting mask')
    # Allowing a zero output diagonal would make the zero fitting admissible;
    # our affine normalization has explicitly enforced both output units.
    need(all(any(int(x,16) for x in r['fitting_rows_hex']) for r in runs),'nonzero normalized outputs')
    out=dict(status='PASS_TWO_PATCH_PROPER_QUOTIENT_NATIVE_AND_EXACT_HYPERPLANES',
             native_sha256=NATIVE,S1=S1,S2=S2,availability_records=records,
             availability_categories={str(list(k)):v for k,v in categories.items()},
             eligible_h1=eligible1,eligible_h2=eligible2,
             universal_bound=dict(proper_quotient_ell_at_least=205,
                                  neither_full_coordinate_tensor_ell_at_least=216,
                                  fields='Every characteristic-two field',widths='Every positive V',
                                  proof_separate_from_finite_search=True),
             width_two_hyperplane_count=15,width_two_minimum_ell_histogram=census,
             hyperplane_results=runs,full_tensor_control=unrestricted,
             one_patch_sharp_control=one_patch,
             explicit_full_scalar_control=dict(canonical_rows_hex=[hex(x) for x in K],
                                               fitting_rows_hex=[hex(x) for x in F],ell=192,rank=11,canonical_quotient_dimension=2),
             finite_scope='All15 F2 hyperplanes of span{h1,h2} tensor F2^2. Every diagonal-normalized row pair enumerated in each allowed local kernel; row choices independent.',
             physical_decoder_supplied=False,new_kappa=False,
             classification='Author universal source-specific theorem and exhaustive fixed-code finite minima; independent review pending.')
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=out['status'],availability_census={str(list(k)):len(v) for k,v in categories.items()},
                         minimum_ell_histogram=census,full_tensor_ell=unrestricted['minimum_ell'],
                         one_patch_ell=one_patch['minimum_ell'])))


if __name__=='__main__':
    main()
