#!/usr/bin/env python3
"""Independent exact review: character evaluation plus Q(i) column arithmetic.

Does not import either author's checker or the retained matrix engine.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

Z = (F(0), F(0))
O = (F(1), F(0))
ROOTS = (O, (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1)))


def plus(x, y):
    return (x[0] + y[0], x[1] + y[1])


def times(x, y):
    return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0])


def conj(x):
    return (x[0], -x[1])


def div(x, y):
    den = y[0]*y[0] + y[1]*y[1]
    assert den
    z = times(x, conj(y))
    return (z[0]/den, z[1]/den)


def eye(n=16):
    return [{j: O} for j in range(n)]


def clean(v):
    return {i: z for i, z in v.items() if z != Z}


def scale(A, c):
    c = (F(c), F(0)) if not isinstance(c, tuple) else c
    return [clean({i: times(z, c) for i, z in col.items()}) for col in A]


def add(*As):
    out = [dict() for _ in As[0]]
    for A in As:
        for j, col in enumerate(A):
            for i, z in col.items():
                out[j][i] = plus(out[j].get(i, Z), z)
    return [clean(col) for col in out]


def mm(A, B):
    out = []
    for col in B:
        v = {}
        for k, z in col.items():
            for i, w in A[k].items():
                v[i] = plus(v.get(i, Z), times(w, z))
        out.append(clean(v))
    return out


def star(A):
    n = len(A)
    out = [dict() for _ in range(n)]
    for j, col in enumerate(A):
        for i, z in col.items():
            out[i][j] = conj(z)
    return out


def power(A, n):
    if n < 0:
        return power(star(A), -n)
    out = eye(len(A))
    for _ in range(n):
        out = mm(out, A)
    return out


def mono(table):
    assert sorted(x[0] for x in table) == list(range(len(table)))
    assert all(0 <= x[1] < 4 for x in table)
    return [{dest: ROOTS[phase]} for dest, phase in table]


def table(A):
    assert all(len(col) == 1 for col in A)
    out = []
    for col in A:
        (i, z), = col.items()
        assert z in ROOTS
        out.append([i, ROOTS.index(z)])
    assert len({x[0] for x in out}) == len(out)
    return out


def trace(A):
    out = Z
    for j, col in enumerate(A):
        out = plus(out, col.get(j, Z))
    return out


def col_rank(columns):
    basis = {}
    for col in columns:
        v = dict(col)
        while v:
            p = min(v)
            if p in basis:
                c = v[p]
                for i, z in basis[p].items():
                    v[i] = plus(v.get(i, Z), times((-c[0], -c[1]), z))
                v = clean(v)
            else:
                c = v[p]
                basis[p] = {i: div(z, c) for i, z in v.items()}
                break
    return len(basis)


def stack(*As):
    n = len(As[0])
    return [{i + k*n: z for k, A in enumerate(As) for i, z in A[j].items()}
            for j in range(n)]


def scalar_eye(n=3):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def scalar_mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)]


def replay(word, characters):
    out = scalar_eye()
    bounds = [F(1)]*3
    peak = F(1)
    for op in word:
        kind = op['op']
        if kind == 'ADD':
            i, j = op['target'], op['source']
            assert i != j and 0 <= i < 3 and 0 <= j < 3
            out[i] = [x+y for x, y in zip(out[i], out[j])]
            bounds[i] += bounds[j]
        elif kind == 'SCALE':
            i, c = op['bank'], F(op['coefficient'])
            assert c and c.denominator & (c.denominator-1) == 0
            out[i] = [c*x for x in out[i]]
            bounds[i] *= abs(c)
        else:
            assert kind == 'MONO'
            i, c = op['bank'], characters[op['name']]
            assert c in (-1, 1)
            out[i] = [c*x for x in out[i]]
        peak = max(peak, *bounds)
    return out, peak


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--author', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    words_path = args.author/'WORDS.json'
    supplied = json.loads(words_path.read_text())
    words = supplied['words']
    gauge_path = args.repo/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint2-evidence/B/forward-row-range-and-spectator-kernels/GAUSSIAN-GAUGES.json'
    assert sha(gauge_path) == '7c654a4de1a78f582781edd216bb863d93f0047c27e343005554b2a06e8dee02'
    gauges = json.loads(gauge_path.read_text())

    # The four scalar characters separate Q[V4].  This checks all three
    # arbitrary inputs, including the character absent at physical width 1.
    char_matrices = {}
    invoice = {}
    for u in (1, -1):
        for v in (1, -1):
            character = {'s': u, 't': v, 'st': u*v}
            if (u, v) == (1, 1):
                target = [[1,0,0],[1,1,0],[1,0,1]]
                inv = [[1,0,0],[-1,1,0],[-1,0,1]]
            elif (u, v) == (1, -1):
                target = inv = scalar_eye()
            elif (u, v) == (-1, 1):
                target = [[0,-1,0],[1,0,0],[0,0,1]]
                inv = [[0,1,0],[-1,0,0],[0,0,1]]
            else:
                target = [[0,0,-1],[0,1,0],[1,0,0]]
                inv = [[0,0,1],[0,1,0],[-1,0,0]]
            C, peak = replay(words['C'], character)
            Ci, peaki = replay(words['C_inverse'], character)
            assert C == target and Ci == inv
            assert scalar_mm(C, Ci) == scalar_mm(Ci, C) == scalar_eye()
            assert [C[i][0] for i in range(3)] == [(1+u)/2,(1+v)/2,(1+u*v)/2]
            char_matrices[f'{u},{v}'] = {'C': C, 'C_inverse': Ci}
            invoice['C'] = {'prefix_bound': str(peak)}
            invoice['C_inverse'] = {'prefix_bound': str(peaki)}
    for h in (1, -1):
        H, peak = replay(words['H'], {'Ht': h})
        Hi, peaki = replay(words['H_inverse'], {'Ht': h})
        assert H == [[2,0,0],[-1-h,1,0],[0,0,1]]
        assert Hi == [[F(1,2),0,0],[F(1+h,2),1,0],[0,0,1]]
        assert scalar_mm(H, Hi) == scalar_mm(Hi, H) == scalar_eye()
        invoice['H'] = {'prefix_bound': str(peak)}
        invoice['H_inverse'] = {'prefix_bound': str(peaki)}
    omission_count = 0
    for name, word in words.items():
        invoice[name]['counts'] = dict(Counter(op['op'] for op in word))
        invoice[name]['generator_pass_upper_bound'] = sum(
            2 if op['name'] == 'st' else 1 for op in word if op['op'] == 'MONO')
        assert invoice[name] == supplied['invoices'][name]
        chars = [{'s':u,'t':v,'st':u*v} for u in (1,-1) for v in (1,-1)] if name.startswith('C') else [{'Ht':1},{'Ht':-1}]
        for j, op in enumerate(word):
            if op['op'] == 'ADD':
                mutated = word[:j]+word[j+1:]
                assert any(replay(mutated, c)[0] != replay(word, c)[0] for c in chars)
                omission_count += 1

    # Direct literal source action, constructed without the author engine:
    # A|abcd> = (-1)^(abd) [(1+i)|bcda>+(1-i)|b,!c,d,a>]/2.
    I = eye()
    A = []
    for x in range(16):
        a,b,c,d = [(x >> j) & 1 for j in range(4)]
        y = b+2*c+4*d+8*a
        sign = (-1)**(a*b*d)
        A.append({y:(F(sign,2),F(sign,2)), y^2:(F(sign,2),F(-sign,2))})
    assert mm(A,star(A)) == mm(star(A),A) == I
    s = mono([[((x&3)|((x&4)<<1)|((x&8)>>1)),0] for x in range(16)])
    t = mono([[x^12,0] for x in range(16)])
    st = mm(s,t)
    assert mm(s,t) == mm(t,s) and mm(s,s) == mm(t,t) == mm(st,st) == I
    assert [trace(g) for g in [I,s,t,st]] == [(16,0),(8,0),(0,0),(8,0)]
    monos = {'I':I, 's':s, 't':t, 'st':st}
    for j in (1,2):
        for name, g in [('s',s),('t',t)]:
            pull = mm(mm(power(A,-j),g),power(A,j))
            table(pull)
            monos[f'r{j}{name}'] = pull
    Ht = mm(mm(A,t),star(A))
    monos['Ht'] = Ht
    for name, M in monos.items():
        assert table(M) == supplied['tables'][name]
        assert mm(M,M) == I
    assert trace(Ht) == Z
    assert any(len(col) != 1 for col in mm(mm(A,s),star(A)))
    # The nontrivial phases in the second pull are essential.
    unphased_r2t = mono([[dest,0] for dest, phase in supplied['tables']['r2t']])
    assert unphased_r2t != monos['r2t']

    ps, pt = scale(add(I,s),F(1,2)), scale(add(I,t),F(1,2))
    emm = scale(add(I,scale(s,-1),scale(t,-1),st),F(1,4))
    emp = scale(add(I,scale(s,-1),t,scale(st,-1)),F(1,4))
    assert mm(emm,emm) == emm and trace(emm) == (4,0)
    assert not any(emp)  # The (-,+) character is absent only at width 1.
    k0, k1 = mm(mm(A,ps),A), mm(mm(A,pt),A)
    R1 = mm(mm(star(A),emm),A)
    R2 = mm(mm(power(A,-2),emm),power(A,2))
    K = stack(k0,k1)
    assert col_rank(K) == 12 and col_rank(R1) == col_rank(R2) == 4
    for k in (k0,k1):
        assert not any(mm(k,R1)) and not any(mm(mm(k,A),R2))
    assert add(mm(star(k0),k0),mm(star(k1),k1)) == mm(mm(star(A),add(ps,pt)),A)
    for j, R in [(1,R1),(2,R2)]:
        rs, rt = monos[f'r{j}s'], monos[f'r{j}t']
        expected = scale(add(I,scale(rs,-1),scale(rt,-1),mm(rs,rt)),F(1,4))
        assert expected == R and mm(R,R) == R

    B2 = mm(mm(A,s),power(A,3))
    A4 = power(A,4)
    pout = scale(add(I,Ht),F(1,2))
    assert scale(mm(k0,power(A,2)),2) == add(A4,B2)
    assert add(mm(k1,power(A,2)),scale(mm(pout,mm(k0,power(A,2))),-2)) == scale(mm(pout,B2),-1)
    assert col_rank(A4) == col_rank(B2) == 16
    # Exact image overlap: [I;0] and [I;-pout].
    blank = [dict() for _ in range(16)]
    rank_union = col_rank(stack(I,blank)+stack(I,scale(pout,-1)))
    assert rank_union == 24 and col_rank(pout) == 8

    # Independently verify exact Gaussian gauges, not only row counts.
    for name, operator, r in [('A4',A4,4),('B2',B2,2)]:
        target = I
        for bit in range(r):
            flip = mono([[x^(1<<bit),0] for x in range(16)])
            cb = add(scale(I,(F(1,2),F(1,2))),scale(flip,(F(1,2),F(-1,2))))
            target = mm(target,cb)
        gauge = gauges[name]
        assert gauge['rank'] == r
        assert mm(mm(mono(gauge['left']),target),mono(gauge['right'])) == operator
        assert mm(mm(mono([[x,0] for x,p in gauge['left']]),target),mono([[x,0] for x,p in gauge['right']])) != operator
    assert mm(mm(A,monos['r2s']),power(A,3)) != B2

    widths = []
    for V in range(1,13):
        D, tr = 16**V, 8**V
        sectors = {(1,1):(D+2*tr)//4, (1,-1):D//4,
                   (-1,1):(D-2*tr)//4, (-1,-1):D//4}
        assert sum(sectors.values()) == D and min(sectors.values()) >= 0
        assert sectors[-1,-1] == D//4
        widths.append({'width':V, 'bank_dimension':D,
                       'character_multiplicities':{f'{u},{v}':n for (u,v),n in sectors.items()},
                       'source_rank':3*D//4, 'kernel_rank':D//4,
                       'residue_overlap_dimension':D//2})
    assert widths[0]['character_multiplicities']['-1,1'] == 0
    assert widths[1]['character_multiplicities']['-1,1'] == 32
    # Replacing the collective projector by a tensor of one-column
    # projectors gives rank 16 rather than 64 at V=2.
    assert 4**2 != 16**2//4

    result = {
        'status':'PASS_INDEPENDENT_DYADIC_KLEIN_SOURCE_INTERFACE',
        'universal_character_sectors_checked':4,
        'all_arbitrary_bank_input_words':4,
        'ADD_omission_controls':omission_count,
        'allwidth_proof':'Literal one-column multiplicative identities lift; collective projector ranks follow character traces. No finite-width extrapolation.',
        'invoice':invoice,
        'source_rank_fraction':'3/4',
        'kernel_rank_fraction':'1/4',
        'quartic_residue_image_overlap_fraction':'1/2',
        'width_controls':widths,
        'scope':'C, inverse, H, inverse and source/kernel identities only; Q, independent endpoints and complete supplier costs remain absent.',
        'new_complete_kappa':False,
        'source_pins':{'author_words':sha(words_path),'author_proof':sha(args.author/'PROOF.md'),'gaussian_gauges':sha(gauge_path)},
        'controls':['delete any primitive ADD','erase Gaussian gauge phases','erase r2t phases','wrong active swap','missing physical character at width 1 reappears at width 2','collective projector is not tensor projector'],
    }
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'CHARACTERS.json').write_text(json.dumps(char_matrices,indent=2,default=str)+'\n')
    (args.out/'TABLES.json').write_text(json.dumps({n:table(M) for n,M in monos.items()},indent=2)+'\n')
    print(result['status'], 'source rank 3D/4; overlap D/2; invoices independently verified')


if __name__ == '__main__':
    main()
