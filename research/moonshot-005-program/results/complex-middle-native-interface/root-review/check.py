#!/usr/bin/env python3
"""Independent exact actual-source controls for the middle-native lemma.

Imports no author engine. Gaussian-rational width-one controls do not prove
tensor separation: that argument is audited separately in the written review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix


def dm(m):
    return DomainMatrix.from_Matrix(m.applyfunc(s.expand)).convert_to(QQ_I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--proof', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    n = 16
    one,zero = s.eye(n),s.zeros(n)
    rot,phase,flip = s.zeros(n),s.zeros(n),s.zeros(n)
    for j in range(n):
        rot[(j >> 1) | ((j & 1) << 3), j] = 1
        phase[j, j] = -1 if (j & 13) == 13 else 1
        flip[j ^ 2, j] = 1
    a = ((1+s.I)*one+(1-s.I)*flip)/2 * phase * rot
    ai = a.conjugate().T
    assert dm(a)*dm(ai) == dm(one)
    assert {sum(x != 0 for x in a.row(j)) for j in range(n)} == {2}
    aa,a4 = s.simplify(a*a),s.simplify(a**4)
    assert {sum(x != 0 for x in aa.row(j)) for j in range(n)} == {4}
    assert {sum(x != 0 for x in a4.row(j)) for j in range(n)} == {16}

    def block(rows):
        return dm(s.BlockMatrix(rows).as_explicit())
    def unit(i,j,m):
        rows = [[zero for _ in range(3)] for _ in range(3)]
        rows[i][j] = m
        return block(rows)
    ident = block([[one,zero,zero],[zero,one,zero],[zero,zero,one]])
    nil = ident-ident
    native_l = block([[a,zero,zero],[one,a,zero],[zero,zero,one]])
    native_li = block([[ai,zero,zero],[-ai*ai,ai,zero],[zero,zero,one]])
    native_u = block([[a,-aa,zero],[zero,a,zero],[zero,zero,one]])
    da = block([[a,zero,zero],[zero,a,zero],[zero,zero,one]])
    dai = block([[ai,zero,zero],[zero,ai,zero],[zero,zero,one]])
    p0,t0 = unit(2,2,one),unit(0,1,-a)
    u0,u1,u2 = p0,block([[a,zero,zero],[zero,a,zero],[zero,zero,zero]]),unit(0,1,-aa)
    assert native_l*native_li == native_li*native_l == ident
    assert da*(ident+t0) == u0+u1+u2 == native_u

    h,jmap = s.zeros(n),s.zeros(n)
    for k in range(n):
        h[k ^ (1 if k & 4 else 0),k] = s.I**((k >> 1) & 3)
        jmap[(k+1)%n,k] = s.I**(k%4)
    assert dm(h)*dm(jmap) != dm(jmap)*dm(h)
    assert dm(h)*dm(a) != dm(a)*dm(h)
    c_steps = [unit(2,0,h),unit(0,1,jmap),unit(1,2,h.conjugate().T)]
    q_steps = [unit(0,2,jmap),unit(2,1,h),unit(1,0,jmap.conjugate().T)]
    def product(xs):
        r = ident
        for x in xs:
            r = r*x
        return r
    c = product([ident+x for x in c_steps])
    ci = product([ident-x for x in reversed(c_steps)])
    q = product([ident+x for x in q_steps])
    qi = product([ident-x for x in reversed(q_steps)])
    assert c*ci == ci*c == q*qi == qi*q == ident
    b0,b1,b2 = [c*u*q for u in (u0,u1,u2)]
    assert [b.rank() for b in (b0,b1,b2)] == [n,2*n,n]
    f = b0+b1
    fi = qi*dai*ci
    assert f*fi == fi*f == ident
    p,t = fi*b0,fi*b2
    assert p == qi*p0*q and t == qi*t0*q
    assert p*p == p and t*t == p*t == t*p == nil
    assert p.rank() == t.rank() == n
    assert f*qi*dai == c
    assert c*native_u*q == f*(ident+t) == b0+b1+b2
    assert native_li*(native_l*c*native_u*q*native_l)*native_li == c*native_u*q

    concentrated = block([[zero,-a4,zero],[aa,zero,zero],[zero,zero,one]])
    assert native_l*native_u*native_l == concentrated
    nonordinary_idle = block([[zero,-a4,zero],[aa,zero,zero],[zero,zero,ai]])
    assert native_li*nonordinary_idle*native_li == native_u-u0+unit(2,2,ai)
    diagonal = block([[a4,zero,zero],[zero,aa,zero],[zero,zero,a]])
    peeled_diagonal = block([[aa,zero,zero],[-a-ai,one,zero],[zero,zero,a]])
    assert native_li*diagonal*native_li == peeled_diagonal
    diagonal_flat = block([[zero,zero,zero],[-a-ai,one,zero],[zero,zero,a]])
    assert diagonal_flat.rank() == 2*n
    star2 = unit(0,0,aa/2)
    tstar = dai*star2
    assert (da+star2).rank() == 3*n
    assert tstar.rank() == n and tstar*tstar == unit(0,0,aa/4) != nil
    bad_li = block([[ai,zero,zero],[-ai,ai,zero],[zero,zero,one]])
    assert bad_li*native_l != ident
    assert native_u-u0 != native_u
    assert native_li*nonordinary_idle*native_li != native_u
    sources = ['complex-four-bit-cubic-source/author/PROOF.md','complex-four-bit-concentration/author/PROOF.md','complex-inverse-native-coset/two-native/PROOF.md']
    prefix = Path('research/moonshot-005-program/results')
    result = {
        'status':'PASS_ROOT_INDEPENDENT_MIDDLE_NATIVE_ACTUAL_SOURCE_CONTROLS',
        'method':'Independent SymPy DomainMatrix arithmetic over QQ(i); no author code imported.',
        'proof_sha256':hashlib.sha256(args.proof.read_bytes()).hexdigest(),
        'source_sha256':{str(prefix/p):hashlib.sha256((args.repo/prefix/p).read_bytes()).hexdigest() for p in sources},
        'source_dimension':n,'native_matrix_dimension':3*n,'matrix_columns_checked':'all',
        'ordinary_shears_per_interstage':3,'noncommuting_coefficients':True,
        'component_ranks':[n,2*n,n],'relative_projector_rank':n,'relative_nilpotent_rank':n,
        'both_native_inverse_equations':True,'noncommuting_conjugacy_and_reconstruction':True,
        'literal_diagonal_flat_rank':2*n,'rank_only_false_positive_invertible':True,
        'negative_controls':['wrong inverse power','dropped idle component','unpaid nonordinary idle substitution','correct component ranks but nonnilpotent relative component'],
        'universal_claim_basis':'Written audit proves block equations and faithful finite tensor-catalogue projection scope. Finite controls do not establish universal tensor separation.',
        'new_complete_kappa':False,
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__ == '__main__':
    main()
