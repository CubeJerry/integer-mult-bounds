#!/usr/bin/env python3
"""Exact finite-source and group-algebra controls for the spectator theorem."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path

import sympy
from sympy import I, QQ_I
from sympy.polys.matrices import DomainMatrix

PINNED = {
    "results/complex-sameplus-routed-column/author/PROOF.md": "904a4a1b2d859661a3d3a832e476977f78e64907bce4aafb02e8a63d7fe6ea1a",
    "results/complex-sameplus-fixed-output-gate/author/PROOF.md": "5d34d4e386aab40e82722a8b118ec67b5deda56cf38eb46d93f6caa7985080a5",
    "results/complex-mixed-all-profile-gate/author/output/RESULT.json": "93112c2d95d05de06eb197d601ed25e1f45ad0badd5969cae9d5f8b279c98ddb",
}
IDENTITY = (0, tuple(range(4)))
SAB = (0, (1, 0, 2, 3))
HBD = (0, (0, 3, 2, 1))
PREFIX_SAB = (1, SAB[1])
ONE = {IDENTITY: Fraction(1)}
ZERO = {}


def group_product(left, right):
    # A permutation p writes output coordinate i from input coordinate p[i].
    return left[0] ^ right[0], tuple(right[1][j] for j in left[1])


def plus(*args):
    ans = Counter()
    for value in args:
        ans.update(value)
    return {g: v for g, v in ans.items() if v}


def times(c, value):
    return {g: c * v for g, v in value.items() if c * v}


def conv(*args):
    ans = ONE
    for arg in args:
        dest = Counter()
        for g, c in ans.items():
            for h, d in arg.items():
                dest[group_product(g, h)] += c * d
        ans = {g: v for g, v in dest.items() if v}
    return ans


def primitive_shear(target, src, value):
    word = []
    for (z, perm), coeff in sorted(value.items()):
        assert coeff.denominator & (coeff.denominator - 1) == 0
        for power in range(abs(coeff.numerator).bit_length()):
            if not (abs(coeff.numerator) >> power) & 1:
                continue
            c = Fraction((1 if coeff > 0 else -1) * (1 << power), coeff.denominator)
            element = (z, perm)
            inv = (z, tuple(perm.index(i) for i in range(4)))
            if element != IDENTITY:
                word.append(("MONO", src, element))
            if c != 1:
                word.append(("SCALE", src, c))
            word.append(("ADD", target, src))
            if c != 1:
                word.append(("SCALE", src, 1 / c))
            if element != IDENTITY:
                word.append(("MONO", src, inv))
    return word


def reverse_word(word):
    result = []
    for op, n, arg in reversed(word):
        if op == "MONO":
            z, p = arg
            result.append((op, n, (z, tuple(p.index(i) for i in range(4)))))
        elif op == "SCALE":
            result.append((op, n, 1 / arg))
        else:
            result.extend(primitive_shear(n, arg, times(-1, ONE)))
    return result


def replay_word(word, omit=None):
    matrix = [[ONE if j == k else ZERO for k in range(3)] for j in range(3)]
    bounds = [Fraction(1)] * 3
    peak = Fraction(1)
    for i, (op, j, arg) in enumerate(word):
        if i == omit:
            continue
        if op == "ADD":
            matrix[j] = [plus(a, b) for a, b in zip(matrix[j], matrix[arg])]
            bounds[j] += bounds[arg]
        elif op == "MONO":
            matrix[j] = [conv({arg: Fraction(1)}, a) for a in matrix[j]]
        else:
            matrix[j] = [times(arg, a) for a in matrix[j]]
            bounds[j] *= abs(arg)
        peak = max(peak, *bounds)
    return matrix, peak


def benchmark_word():
    p = times(Fraction(1, 2), plus(ONE, {PREFIX_SAB: Fraction(1)}))
    n = plus(ONE, times(-1, p))
    h = {HBD: Fraction(1)}
    v = plus(p, conv(n, h))
    j = conv(n, h, n)
    t = plus(times(5, j), times(-4, conv(j, j, j)))
    assert conv(t, j) == conv(j, t) == n
    inverse = plus(p, conv(t, plus(n, times(-1, conv(n, h, p)))))
    assert conv(v, inverse) == conv(inverse, v) == ONE
    minus = times(-1, ONE)
    # Chronological ordering: balanced diagonal, swap(0,2), then E02(I).
    word = (primitive_shear(1, 2, minus) + primitive_shear(2, 1, ONE)
            + primitive_shear(1, 2, minus) + primitive_shear(1, 2, v)
            + primitive_shear(2, 1, times(-1, inverse)) + primitive_shear(1, 2, v)
            + [("SCALE", 0, Fraction(-1))] + primitive_shear(0, 2, ONE)
            + primitive_shear(2, 0, minus) + primitive_shear(0, 2, ONE)
            + primitive_shear(0, 2, ONE))
    inverse_word = reverse_word(word)
    expected = [[ONE, ZERO, inverse], [ZERO, v, ZERO], [ONE, ZERO, ZERO]]
    expected_inverse = [[ZERO, ZERO, ONE], [ZERO, inverse, ZERO], [v, ZERO, times(-1, v)]]
    receipts = {}
    for label, current, wanted in [("forward", word, expected), ("inverse", inverse_word, expected_inverse)]:
        actual, peak = replay_word(current)
        assert actual == wanted
        add_indices = [i for i, op in enumerate(current) if op[0] == "ADD"]
        assert all(replay_word(current, omit=i)[0] != wanted for i in add_indices)
        receipts[label] = {"counts": dict(Counter(op[0] for op in current)),
                           "uniform_triangle_norm_bound": str(peak), "rejected_ADD_omissions": len(add_indices)}
    return v, inverse, receipts


def dm(x):
    return DomainMatrix.from_Matrix(x).convert_to(QQ_I).to_sparse()


def lin(*rows):
    return rows[0][0].hstack(*rows[0][1:]).vstack(*[r[0].hstack(*r[1:]) for r in rows[1:]])


def table(address, phase=lambda *bits: 0):
    entries = {}
    for j in range(16):
        bits = tuple((j >> k) & 1 for k in range(4))
        out = address(*bits)
        entries[sum(b << k for k, b in enumerate(out)), j] = I ** (phase(*bits) % 4)
    return dm(sympy.SparseMatrix(16, 16, entries))


def gp(p):
    return table(lambda *bits: tuple(bits[k] for k in p))


def adj(v):
    return dm(v.to_Matrix().H)


def rank_type(v):
    # Exact disjoint, flat Walsh blocks, checked by dephasing over QQ(i).
    m = v.to_Matrix()
    supports = [tuple(i for i in range(16) if m[i, j] != 0) for j in range(16)]
    size = len(supports[0])
    assert size in (1, 2, 4, 8, 16)
    assert all(len(x) == size for x in supports)
    assert len(set(supports)) * size == 16
    for rows in set(supports):
        cols = [j for j, support in enumerate(supports) if support == rows]
        assert len(cols) == size
        vals = set()
        for r in rows:
            row = []
            for c in cols:
                w = m[r, c]
                assert sympy.expand(w * w.conjugate()) == sympy.Rational(1, size)
                row.append(sympy.cancel(w * m[rows[0], cols[0]] / (m[r, cols[0]] * m[rows[0], c])))
            assert set(row) <= {-1, 1}
            vals.add(tuple(row))
        assert len(vals) == size and all(tuple(x*y for x, y in zip(l, h)) in vals for l in vals for h in vals)
    return size.bit_length() - 1


def ring_value(word, sign, identity):
    out = identity * QQ_I.zero
    for (z, p), coeff in word.items():
        out += gp(p) * QQ_I.from_sympy(sympy.Rational(coeff.numerator, coeff.denominator) * sign ** z)
    return out


def source_controls(v_word, vinv_word):
    ident = dm(sympy.eye(16))
    zero = dm(sympy.zeros(16))
    half = QQ_I.from_sympy(sympy.Rational(1, 2))
    x = table(lambda a,b,c,d:(a,b^1,c,d))
    rot = table(lambda a,b,c,d:(b,c,d,a), lambda a,b,c,d:2*a*b*d)
    a = (ident*QQ_I(1,1) + x*QQ_I(1,-1)) * half * rot
    ai = adj(a)
    assert ai*a == a*ai == ident
    s = gp((0,1,3,2))
    s1 = gp((3,1,2,0))
    s2 = gp(SAB[1])
    h2 = gp(HBD[1])
    hreturn = gp((0,2,1,3))
    assert ai*s*a==s1 and ai**2*s*a**2==s2
    witness = a*s*ai
    assert witness*witness == ident
    assert 0 < (ident+witness).rank() < 16
    words = {"A":a, "A2":a**2, "A3":a**3, "A4":a**4, "AsA":a*s*a,
             "A3s2A":a**3*s2*a, "A2hA":a**2*h2*a, "A2s2hA":a**2*s2*h2*a,
             "AsA_inverse":witness}
    ranks={name:rank_type(mat) for name,mat in words.items()}
    assert list(ranks.values()) == [1,2,3,4,2,2,1,1,2]
    # A commuting chart supplies a control in which the crucial nonmonomial property fails.
    assert rank_type(a*s1*ai)==0
    l=lin([a,zero,zero],[ident,a,zero],[zero,zero,ident])
    u=lin([a,-a**2,zero],[zero,a,zero],[zero,zero,ident])
    l_inv=lin([ai,zero,zero],[-ai**2,ai,zero],[zero,zero,ident])
    u_inv=lin([ai,ident,zero],[zero,ai,zero],[zero,zero,ident])
    oinv=lin([ident,zero,zero],[-ident,ident,zero],[-ident,ident,ident])
    o=lin([ident,zero,zero],[ident,ident,zero],[zero,-ident,ident])
    eye3=lin([ident,zero,zero],[zero,ident,zero],[zero,zero,ident])
    assert l_inv*l==u_inv*u==o*oinv==eye3
    samples=[]
    parabolic_samples=[]
    benchmark=[]
    for sign in (1,-1):
        S=s*sign; p=(ident+S)*half; n=ident-p
        p1=(ident+s1*sign)*half; p2=(ident+s2*sign)*half; n2=ident-p2
        c=lin([p,zero,-n],[p,ident,-n],[n,zero,p])
        ci=lin([p,zero,n],[-ident,ident,zero],[-n,zero,p])
        assert c*ci==ci*c==eye3
        for label,d,d1,e,g,h,k in [
                ("identity",ident,ident,zero,zero,zero,ident),
                ("transported_noncommuting",s,s1,h2,rot,x+ident,x),
                ("nonintertwining",ident,hreturn,h2,rot,x+ident,x)]:
            k_inv=adj(k); di=adj(d); d1i=adj(d1)
            kfull=lin([d,e,g],[zero,d1,h],[zero,zero,k])
            kinv=lin([di,-di*e*d1i,di*(e*d1i*h-g)*k_inv],
                      [zero,d1i,-d1i*h*k_inv],[zero,zero,k_inv])
            assert kinv*kfull==kfull*kinv==eye3
            m=oinv*l*c*kfull*u
            mi=u_inv*kinv*ci*l_inv*o
            assert mi*m==m*mi==eye3
            eq1=lin([d*a,-d*a**2+e*a+a*d1*a,g+a*h+S*k])
            eq2=lin([-k_inv*n*ai,-k_inv*p,k_inv*p])
            assert m.extract(list(range(32,48)),list(range(48)))==eq1
            assert mi.extract(list(range(32,48)),list(range(48)))==eq2
            if label=="nonintertwining":
                assert a*d1!=d*a and rank_type(a*d1*a)==0
                # Cubic contribution cannot be dropped when d1 is changed.
                assert -d*a**3+a*d1*a**2 != zero
            else:
                assert a*d1==d*a
            samples.append([sign,label])
        active_lower=lin([ident,zero,zero],[rot+x,ident,zero],[zero,zero,ident])
        lower_inverse=lin([ident,zero,zero],[-rot-x,ident,zero],[zero,zero,ident])
        shear=lin([ident,h2,x+ident],[zero,ident,rot],[zero,zero,x])
        shear_inverse=lin([ident,-h2,(h2*rot-x-ident)*x],
                          [zero,ident,-rot*x],[zero,zero,x])
        pk=active_lower*shear
        pki=shear_inverse*lower_inverse
        assert pk*pki==pki*pk==eye3
        actual=l*c*pk*u
        actual_inv=u_inv*pki*ci*l_inv
        assert actual*actual_inv==actual_inv*actual==eye3
        assert lin([zero,zero,p])*actual==lin([zero,zero,p*x])
        assert lin([zero,zero,ident])*actual_inv==lin([-x*n*ai,zero,x*p])
        # Moving the spectator into the active input is the genuine boundary of the claim.
        active_to_spectator=lin([ident,zero,zero],[zero,ident,zero],[zero,ident,ident])
        assert lin([zero,zero,p])*l*c*active_to_spectator*u != lin([zero,zero,p])
        parabolic_samples.append({"prefix_sign":sign, "active_lower_left_nonzero":True,
                                   "physical_low_row":True,"physical_inverse_spectator_row":True,
                                   "spectator_row_mutation_rejected":True})
        v=ring_value(v_word,sign,ident);vi=ring_value(vinv_word,sign,ident)
        assert vi*v==v*vi==ident and v==p2+n2*h2
        q=lin([ident,zero,vi],[zero,v,zero],[ident,zero,zero])
        qi=lin([zero,zero,ident],[zero,vi,zero],[v,zero,-v])
        assert q*qi==qi*q==eye3
        E=oinv*l*c*u*q*l
        nominal=lin([-a*n*a,-a**3*p2*a,a**2*p1*vi],
                    [a**2*p2-n*a+a**2*n2*h2,a**2*n2*h2*a,a*p1*vi],
                    [a**2+S*a,zero,a*vi])
        assert E==nominal
        high=lin([zero,-a**4*half,zero],[zero,zero,zero],[zero,zero,zero])
        Ei=l_inv*qi*u_inv*ci*l_inv*o
        assert Ei*E==eye3
        right=Ei*high
        # A separated component may be non-idempotent despite being a full quartic corner.
        defect=right**2-right
        benchmark.append({"prefix_sign":sign,"checked_input_columns":48,
                          "quartic_corner_rank":high.rank(),"idempotence_defect_rank":defect.rank(),
                          "projector_pulled_back_is_ordinary_idempotent":defect.is_zero_matrix})
    assert any(x["idempotence_defect_rank"]>0 for x in benchmark)
    return {"one_letter_verified_classes":ranks,"nonmonomial_physical_plus_rank":(ident+witness).rank(),
            "forward_and_inverse_third_row_samples":samples,"full_parabolic_controls":parabolic_samples,"benchmark":benchmark}


def price():
    scale=10**40
    def bound(n):
        rhs=n**199 * scale**200
        lo, hi=0,n*scale+1
        while lo+1 < hi:
            mid=(lo+hi)//2
            if mid**200 <= rhs:lo=mid
            else:hi=mid
        assert lo**200<=rhs<(lo+1)**200
        return Fraction(lo,scale),Fraction(lo+1,scale)
    a,b,f,c,d=(bound(x) for x in (7,8,22,23,24))
    def subtract_profiles(pos,neg):
        return [sum(n*iv[0] for n,iv in pos)-sum(n*iv[1] for n,iv in neg),
                sum(n*iv[1] for n,iv in pos)-sum(n*iv[0] for n,iv in neg)]
    invoice=[(3,(1,1)),(6,a),(3,b)]
    first=subtract_profiles(invoice,[(1,d),(1,c),(1,f)])
    second=subtract_profiles(invoice,[(2,c),(1,f)])
    assert 0<first[0]<first[1]<second[0]
    return {"parabolic_deficit_at_199_over_200":list(map(str,first)),
            "transported_subfamily_deficit_at_199_over_200":list(map(str,second))}



def main():
    parser=ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    directory=args.repo/"research"/"moonshot-005-program"
    for path,digest in PINNED.items():
        assert sha256((directory/path).read_bytes()).hexdigest()==digest
    word,inverse,receipts=benchmark_word()
    exact=source_controls(word,inverse)
    result={"status":"PASS_SAMEPLUS_SPECTATOR_PULLBACK_AND_ALL_INPUT_BENCHMARK",
            "baseline":"e31d437b489a416446fdd7e294bc2238829c5925","pins":PINNED,
            **exact,**price(),"all_input_Q_paid_receipts":receipts,
            "transported_triangular_maximum_head":2,"arbitrary_parabolic_profile_cap":[3,2,1],
            "transported_triangular_profile_cap":[2,2,1],"independent_421_endpoint":False,
            "new_complete_kappa":False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(result["status"])


if __name__=="__main__":
    main()
