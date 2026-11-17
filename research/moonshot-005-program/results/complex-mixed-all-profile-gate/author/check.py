#!/usr/bin/env python3
"""Exact source coefficients and complete price for the fixed mixed-interface gate.

The universal claims are proved in PROOF.md; finite replay is not substituted
for the collective-word independence argument.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

PINS = {
    'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py':
        '1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91',
    'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint10-evidence/B/return-clock-source-interface/PROOF.md':
        '82c0dec112b3f9eaf0a06cbf9b75c8b1be49ec70cb68d69f25c1cb0e7b778270',
    'research/moonshot-005-program/sessions/2026-11-17-S020/logical-records-before-cp1/TARGET-005.md':
        '8c7001ff518eae3d9951ea6017cc47047a31fe0f4f599c4adfe541a382968238',
}


def run(repo, out):
    for name, expected in PINS.items():
        assert hashlib.sha256((repo/name).read_bytes()).hexdigest() == expected
    ep = repo/next(iter(PINS))
    spec = importlib.util.spec_from_file_location('fixed_mixed_gate_exact', ep)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    eye = m.eye(16)
    roots = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def sc(x, v):
        v = F(v)
        assert not v.denominator & (v.denominator-1)
        y = x.scale((v.numerator, 0))
        return m.M(y.a, y.k+v.denominator.bit_length()-1).norm()

    def tab(dest, phase):
        bits = [tuple((x >> j) & 1 for j in range(4)) for x in range(16)]
        return m.monomial([dest(*b) for b in bits], [phase(*b) % 4 for b in bits])

    R = tab(lambda a,b,c,d: b+2*c+4*d+8*a, lambda a,b,c,d: 2*a*b*d)
    Xb = m.monomial([x ^ 2 for x in range(16)], [0]*16)
    A = sc(eye.scale((1,1))+Xb.scale((1,-1)), F(1,2)) @ R
    s = tab(lambda a,b,c,d: a+2*c+4*b+8*d, lambda a,b,c,d: 0)
    h = tab(lambda a,b,c,d: a+2*c+4*b+8*d, lambda a,b,c,d: b-c)
    ret = A @ s @ A
    mw = A.star() @ h @ A.power(2)
    qw = A.star() @ h @ s @ h @ A
    assert s@s == h@h == qw@qw == eye
    assert ret.k == 0 and m.gaussian_rank(ret) == 0
    supports = lambda x: sorted({sum(z != (0,0) for z in row) for row in x.a})
    assert supports(mw) == [8] and supports(qw) == [4]
    assert qw.trace() == (8,0)
    assert sc(eye+qw,F(1,2)) @ sc(eye+qw,F(1,2)) == sc(eye+qw,F(1,2))
    assert sc(eye+qw,F(1,2)).trace() == (12,0)

    # This exact Walsh-block test is the inherited source recognition routine,
    # reimplemented locally to avoid importing an author result or certificate.
    def head_rank(x):
        counts = {sum(v != (0,0) for v in row) for row in x.a}
        assert len(counts) == 1
        n = counts.pop()
        assert n and not n & (n-1)
        assert all(n*(v[0]*v[0]+v[1]*v[1]) == 1 << (2*x.k)
                   for row in x.a for v in row if v != (0,0))
        groups = {}
        for row in x.a:
            groups.setdefault(tuple(j for j,v in enumerate(row) if v != (0,0)), []).append(row)
        assert len(groups) == 16//n
        for columns, rows in groups.items():
            assert len(rows) == n
            phases = {m.gm(rows[0][columns[0]], u): k for k,u in enumerate(roots)}
            assert all(row[j] in phases for row in rows for j in columns)
            exp = [[phases[row[j]] for j in columns] for row in rows]
            masks = []
            for row in exp:
                ds = [(row[j]-row[0]-exp[0][j]+exp[0][0]) % 4 for j in range(n)]
                assert all(v in (0,2) for v in ds)
                masks.append(sum((v//2) << j for j,v in enumerate(ds)))
            span = {0}
            for v in masks:
                if v not in span:
                    span |= {u ^ v for u in tuple(span)}
            assert set(masks) == span and len(span) == n
        return n.bit_length()-1

    ranks = {name: head_rank(x) for name,x in {
        'A': A, 'A2': A.power(2), 'A3': A.power(3),
        'A_h_A': A@h@A, 'A_h_A2': A@h@A.power(2),
        'm': mw, 'q': qw,
    }.items()}
    assert ranks == {'A':1, 'A2':2, 'A3':3, 'A_h_A':1, 'A_h_A2':2, 'm':3, 'q':2}

    # Formal tensor-word algebra at widths divisible by four. Words are grouped
    # only when the one-column matrices differ by a root-four scalar. No
    # width-one linear dependence between distinct tensor words is used.
    @lru_cache(None)
    def canonical(x):
        first = next(v for row in x.a for v in row if v != (0,0))
        phase = max((m.gm(first,u),u) for u in roots)[1]
        return x.scale(phase)

    def el(x, c=1):
        return {canonical(x): F(c)} if c else {}

    def add(*xs):
        r = {}
        for x in xs:
            for g,c in x.items():
                r[g] = r.get(g,F(0))+c
        return {g:c for g,c in r.items() if c}

    def scale(x,c):
        return {g:v*c for g,v in x.items() if v*c}

    @lru_cache(None)
    def product(x,y):
        return canonical(x@y)

    def mul(x,y):
        return add(*({product(g,h): c*d} for g,c in x.items() for h,d in y.items()))

    def mm(x,y):
        return [[add(*(mul(x[i][k],y[k][j]) for k in range(3)))
                 for j in range(3)] for i in range(3)]

    def proj(x,r):
        return {g:c for g,c in x.items() if head_rank(g) == r}

    e, a, s0, h0, b0 = el(eye),el(A),el(s),el(h),el(ret)
    ph,nh = scale(add(e,h0),F(1,2)),scale(add(e,scale(h0,-1)),F(1,2))
    ps,ns = scale(add(e,s0),F(1,2)),scale(add(e,scale(s0,-1)),F(1,2))
    zero = {}
    aa,aaa = el(A.power(2)),el(A.power(3))
    ah,ah2 = el(A@h@A),el(A@h@A.power(2))
    C = [[ph,scale(nh,-1),zero],
         [mul(ps,nh),mul(ps,ph),scale(ns,-1)],
         [mul(ns,nh),mul(ns,ph),ps]]
    L = [[a,zero,zero],[e,a,zero],[zero,zero,e]]
    U = [[a,scale(aa,-1),zero],[zero,a,zero],[zero,zero,e]]
    body = mm(mm(L,C),U)
    row0 = [scale(add(aa,ah),F(1,2)),
            scale(add(scale(aa,-1),ah,scale(aaa,-1),scale(ah2,-1)),F(1,2)),zero]
    assert body[0] == row0
    assert [[proj(x,0) for x in row] for row in body] == [
        [zero,zero,zero],[scale(b0,F(1,4)),scale(b0,F(1,4)),zero],[zero,zero,ps]]
    assert [proj(x,3) for x in body[0]] == [zero,scale(aaa,F(-1,2)),zero]
    assert [proj(x,2) for x in body[0]] == [
        scale(aa,F(1,2)),scale(add(aa,ah2),F(-1,2)),zero]
    assert proj(add(scale(body[2][0],-1),body[2][1]),1) == mul(mul(ns,h0),a)
    assert mul(el(A.power(-2)),ah2) == el(mw)
    assert mul(el(A.star()@h),mul(mul(ns,h0),a)) == scale(add(e,scale(el(qw),-1)),F(1,2))

    controls = {
        'q_has_physical_plus_space_rank12_at_W1': True,
        'phase_deleted_h_rejects_rank_one_clock': head_rank(A@s@A) != 1,
        'omitted_cubic_term_rejected': add(row0[1],scale(aaa,F(1,2))) != body[0][1],
        'omitted_clock2_term_rejected': add(row0[1],scale(ah2,F(1,2))) != body[0][1],
        'nonordinary_q_not_asserted_physically_injective': supports(qw) == [4],
    }
    assert all(controls.values())

    # Exhaustive profile classification is finite supplementary bookkeeping;
    # the universal class constraints above apply to arbitrary ordinary Q.
    profiles = list(itertools.combinations_with_replacement(range(5),3))
    high = [r for r in profiles if sum(r) >= 7]
    reasons = {}
    for rs in high:
        if 0 in rs:
            assert rs in [(0,3,4),(0,4,4)] and 1 not in rs and 2 not in rs
            reasons[str(rs)] = 'zero head: classes1,2 absent force nonunimodular last column'
        else:
            assert set(rs) != {1,2,3}
            reasons[str(rs)] = 'positive heads: last column requires all classes1,2,3'

    def power_bounds(r):
        den = 10**32
        target = pow(r,199)*pow(den,200)
        lo,hi = 0,r*den+1
        while hi-lo > 1:
            mid = (lo+hi)//2
            if pow(mid,200) <= target:
                lo=mid
            else:
                hi=mid
        assert pow(lo,200) <= target < pow(hi,200)
        return F(lo,den),F(hi,den)

    coeff = {1:3,7:6,8:3,23:-3}
    lower=upper=F(0)
    for r,c in coeff.items():
        l,u=power_bounds(r)
        lower += c*(l if c>0 else u)
        upper += c*(u if c>0 else l)
    assert lower>0
    from decimal import Decimal,localcontext
    with localcontext() as ctx:
        ctx.prec=60
        decimals=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in (lower,upper)]
    result={
        'status':'PASS_MIXED_INTERFACE_TOTAL_HEAD_GATE',
        'scope':'fixed Cmix, arbitrary ordinary Q/endpoints, fixed prefix and finite collective tail catalogue',
        'formal_coefficient_identities':'checked modulo root-four scalar only; no one-width linear collapse',
        'source_head_ranks':ranks,
        'witness_nonzero_row_counts':{'m':supports(mw),'q':supports(qw)},
        'positive_endpoint_required_profile':[1,2,3],
        'every_endpoint_total_head_rank_at_most':6,
        'profiles_total_at_least7_rejected':reasons,
        'complete_optimistic_price':'3[1]+6[7]+3[8]',
        'maximum_rank6_target_by_concavity':'3[23]',
        'strict_deficit_for_every_t_in_open_0_1':True,
        'deficit_at_199_over_200':{'rational':[str(lower),str(upper)],'decimal':decimals},
        'negative_controls':controls,
        'changed_first_interface_excluded':False,
        'new_kappa':False,
    }
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    def matrix_dump(x):
        return {'denominator_power2':x.k,'nonzero_entries':[
            [i,j,z[0],z[1]] for i,row in enumerate(x.a) for j,z in enumerate(row) if z!=(0,0)]}
    (out/'WITNESSES.json').write_text(json.dumps({'m':matrix_dump(mw),'q':matrix_dump(qw)},indent=2)+'\n')
    tracked={'check.py':Path(__file__),'PROOF.md':Path(__file__).with_name('PROOF.md'),
             'output/RESULT.json':out/'RESULT.json','output/WITNESSES.json':out/'WITNESSES.json'}
    manifest={'dependencies':PINS,'files':{name:hashlib.sha256(p.read_bytes()).hexdigest()
                                         for name,p in tracked.items()}}
    (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(result['status'], 'deficit',decimals,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    run(args.repo,args.out)
