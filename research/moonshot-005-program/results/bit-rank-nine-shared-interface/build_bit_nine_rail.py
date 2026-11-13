#!/usr/bin/env python3
"""Actual rank-nine binary partial rail and fixed-even-m shared-native word.

No complete Q, productive-target certificate, physical compiler, or new kappa.
"""
import argparse
import collections
import gzip
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def need(ok, why):
    if not ok:
        raise ValueError(why)

def add_basis(basis, row, witness):
    while row:
        pivot = row.bit_length()-1
        if pivot not in basis:
            basis[pivot] = (row, witness)
            return True
        old, mask = basis[pivot]
        row ^= old
        witness ^= mask
    return False

def solve(basis, row):
    witness = 0
    while row:
        pivot = row.bit_length()-1
        if pivot not in basis:
            return None
        old, mask = basis[pivot]
        row ^= old
        witness ^= mask
    return witness

def replay(word, frames):
    public = word['public']
    rows = {i: 1 << i for i in range(public)}
    where = dict(enumerate(word['start']))
    counts = collections.Counter()
    paid = collections.Counter()
    lifetimes = peak = 0
    checked_pairs = set()
    for index, e in enumerate(word['program']):
        op, a = e[:2]
        counts[op] += 1
        if op == 'INIT':
            need(a >= public and a not in rows, ('INIT', index))
            rows[a] = 0
            where[a] = e[2]
            lifetimes += 1
            peak = max(peak, len(rows)-public)
        elif op == 'CLEAR':
            need(a >= public and where.get(a) == e[2], ('CLEAR', index))
            del rows[a]
            del where[a]
        elif op == 'ADD':
            b = e[2]
            chart = e[3]
            need(a != b and where.get(a) == where.get(b) == chart, ('cochart', index, e))
            rows[a] ^= rows[b]
        elif op == 'SWAP':
            # The retained native's SWAP relabels whole (chart,value) roles.
            # It is not a free same-chart value transfer between fixed roles.
            b = e[2]
            need(a != b and a in rows and b in rows, ('SWAP', index))
            rows[a], rows[b] = rows[b], rows[a]
            where[a], where[b] = where[b], where[a]
        elif op == 'MOVE':
            source, target = e[2:]
            need(where.get(a) == source, ('MOVE', index))
            rank = abs(frames[target]['dim']-frames[source]['dim'])
            need(rank > 0, ('rank', index))
            pair = (source, target)
            if pair not in checked_pairs:
                small, large = sorted((frames[source], frames[target]), key=lambda f:f['dim'])
                need(all(sum(Fraction(x)*Fraction(y) for x,y in zip(u,v)) == 0
                         for u in small['B'] for v in large['A']), ('nested charts', pair))
                checked_pairs.add(pair)
            paid[rank] += 1
            where[a] = target
        else:
            raise ValueError((op, index))
    need(set(rows) == set(range(public)), 'Retired owned bank')
    need([where[i] for i in range(public)] == word['final'], 'All public endpoint charts')
    return [rows[i] for i in range(public)], {
        'operations': len(word['program']), 'counts': dict(counts),
        'paid_profile': dict(sorted(paid.items())),
        'retired_lifetimes': lifetimes, 'peak_owned': peak,
        'all_input_directions_replayed': public,
        'distinct_exact_nested_move_pairs': len(checked_pairs),
    }

def write_gzip(path, obj):
    raw = json.dumps(obj, separators=(',', ':'), sort_keys=True).encode()
    path.write_bytes(gzip.compress(raw, mtime=0))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def power_interval(rank, bits=128):
    den = 1 << bits
    target = rank**199 * den**200
    low, high = 0, rank*den+1
    while high-low > 1:
        middle = (low+high)//2
        if middle**200 <= target:
            low = middle
        else:
            high = middle
    need(low**200 <= target < (low+1)**200, 'Directed integer200th-root bracket')
    return Fraction(low,den), Fraction(low if low**200 == target else low+1,den)

def moment(profile):
    lower = upper = Fraction(0)
    for rank, coefficient in profile.items():
        lo, hi = power_interval(rank)
        if coefficient >= 0:
            lower += coefficient*lo
            upper += coefficient*hi
        else:
            lower += coefficient*hi
            upper += coefficient*lo
    return lower, upper

def signed(*terms):
    out = collections.defaultdict(Fraction)
    for scale, profile in terms:
        for rank, count in profile.items():
            out[rank] += scale*count
    return {r:c for r,c in out.items() if c}

def interval_record(interval):
    with localcontext() as context:
        context.prec = 60
        decimal = [str(Decimal(x.numerator)/Decimal(x.denominator)) for x in interval]
    return {'exact_lower':str(interval[0]), 'exact_upper':str(interval[1]),
            'decimal_for_display':decimal, 'decimals_are_not_the_certificate':True}

def main(a):
    a.output.mkdir(parents=True, exist_ok=True)
    raw = (a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'Native pin')
    s = json.loads(gzip.decompress(raw))
    frames = {int(k): v for k, v in s['frames'].items()}
    dot = lambda u, v: sum(x*y for x, y in zip(u, v))
    roots = [[Fraction(x) for x in frames[s['start'][i]]['B'][0]] for i in range(111)]
    g2 = [[int(x*(2 if dot(r, r) == 1 else 1)) for x in r] for r in roots]
    need(all(dot(r, r) == 4 for r in g2), 'Normalized roots')
    fitting = []
    for i in range(111):
        row = 0
        for j in range(111):
            inner = dot(g2[i], g2[j])
            need(inner % 2 == 0, 'Integral doubled Gram')
            bit = 1 ^ ((inner//2) & 1)
            need(i == j or bit == int(inner == 0), 'Foreign contact support')
            row |= bit << j
        need(row >> i & 1, 'Identity diagonal')
        fitting.append(row)
    basis = {}
    encoders = []
    selected = []
    for i, row in enumerate(fitting):
        if add_basis(basis, row, 1 << len(encoders)):
            encoders.append(row)
            selected.append(i)
    need(len(encoders) == 9, 'Rank-nine fitting')
    decoder = [solve(basis, row) for row in fitting]
    need(all(x is not None for x in decoder), 'Decoder')
    program = [['MOVE', i, s['start'][i], 1] for i in range(111)]
    for k, encoder in enumerate(encoders):
        program.append(['INIT', 222, 1])
        program += [['ADD', 222, i, 1] for i in range(111) if encoder >> i & 1]
        program.append(['MOVE', 222, 1, 0])
        program += [['ADD', 111+i, 222, 0] for i, mask in enumerate(decoder) if mask >> k & 1]
        program.append(['CLEAR', 222, 0])
    program += [['MOVE', 111+i, 0, s['final'][111+i]] for i in range(111)]
    word = {'schema': 'BIT-rank-nine-partial-rail-v1', 'public': 222,
            'start': s['start'][:222], 'final': s['final'][:222],
            'frames': s['frames'], 'program': program,
            'scope': 'Exact scalar F2 partial main map X=x,Y=y+Kx. Every MOVE and owned lifetime charged; foreign residual K+I remains.'}
    rows, receipt = replay(word, frames)
    expected = [1 << i for i in range(111)] + [(1 << (111+i)) ^ fitting[i] for i in range(111)]
    need(rows == expected, 'All222-input partial endpoint')
    residual = [r ^ (1 << i) for i, r in enumerate(fitting)]
    rb = {}
    for row in residual:
        add_basis(rb, row, 0)
    receipt.update({'source_sha256': PIN, 'status': 'PASS_EXACT_PARTIAL_RAIL_NOT_COMPLETE_Q',
                    'fitting_rank': 9, 'fitting_rows': fitting,
                    'encoder_source_rows': selected, 'encoder_rows': encoders,
                    'decoder_masks': decoder, 'residual_rank': len(rb),
                    'residual_nonzero_coefficients': sum(r.bit_count() for r in residual),
                    'word_sha256': write_gzip(a.output/'RAIL.json.gz', word)})
    native_rows, nr = replay(s, frames)
    native_expected = [1 << i for i in range(659)]
    for i in range(111):
        native_expected[111+i] ^= 1 << i
    need(native_rows == native_expected, 'Actual native all659 endpoint')
    m = a.multiplicity
    need(m >= 2 and m % 2 == 0, 'Paired caller requires fixed positive even multiplicity')
    public = 659 + 222*(m-1)
    starts = s['start'] + s['start'][:222]*(m-1)
    finals = s['final'] + s['final'][:222]*(m-1)
    def private(k, i):
        return 659+222*k+i
    lifted = []
    for k in range(m-1):
        lifted += [['ADD', i, private(k, i), s['start'][i]] for i in range(222)]
    # The common native's own owned labels are moved above every public input.
    for e in s['program']:
        q = list(e)
        q[1] = q[1] if q[1] < 659 else public+q[1]-659
        if q[0] in ('ADD', 'SWAP'):
            q[2] = q[2] if q[2] < 659 else public+q[2]-659
        lifted.append(q)
    for k in range(m-1):
        for e in program:
            q = list(e)
            q[1] = private(k, q[1]) if q[1] < 222 else public+237
            if q[0] in ('ADD', 'SWAP'):
                q[2] = private(k, q[2]) if q[2] < 222 else public+237
            lifted.append(q)
        lifted += [['ADD', i, private(k, i), s['final'][i]] for i in range(222)]
    mw = {'schema': 'BIT-fixed-even-m-shared-native-partial-v1', 'public': public,
          'start': starts, 'final': finals, 'frames': s['frames'], 'program': lifted,
          'multiplicity': m, 'scope': 'Actual scalar partial word. Productive targets for a complete Q are conditional; no all-width compiler or new kappa.'}
    mr, info = replay(mw, frames)
    want = [1 << i for i in range(public)]
    for i in range(111):
        want[111+i] ^= 1 << i
        for k in range(m-1):
            want[private(k, 111+i)] ^= fitting[i] << (659+222*k)
            want[111+i] ^= residual[i] << (659+222*k)
    need(mr == want, 'All independent shared-native endpoint columns')
    need(all(mr[i] == 1 << i for i in range(222,659)), 'Common helper endpoints')
    info.update({'source_sha256': PIN, 'status': 'PASS_EXACT_SHARED_NATIVE_PARTIAL_WORD',
                 'multiplicity': m, 'private_residual_rank_each': len(rb),
                 'common_error_is_sum_of_private_residuals': True,
                 'word_sha256': write_gzip(a.output/f'M{m}-WORD.json.gz', mw)})
    # Missing Q-completion is kept as a premise in every productive profile.
    N = collections.Counter({int(r): c for r,c in nr['paid_profile'].items()})
    H = collections.Counter({2: 1,4: 25,6: 1,8: 410})
    scale = lambda k,c: collections.Counter({r:k*n for r,n in c.items()})
    P2 = scale(36,N)
    T2 = scale(36,H)
    P2[1] += 444
    T2[127] += 222
    for j in range(1,9): P2[7*j] += 444
    for j in range(1,10): T2[1+7*j] += 444
    Q = collections.Counter({int(r): c for r,c in receipt['paid_profile'].items()})
    Pm = scale(m//2,P2)
    Tm = scale(m//2,T2)
    for r,c in N.items(): Pm[r] -= 18*(m-1)*c
    for r,c in Q.items(): Pm[r] += 18*(m-1)*c
    for r,c in H.items(): Tm[r] -= 18*(m-1)*c
    need(min(Pm.values()) >= 0 and min(Tm.values()) >= 0, 'Nonnegative complete histograms')
    profile = lambda c: dict(sorted((r,n) for r,n in c.items() if n))
    budget = {'status': 'EXACT_PROVISIONAL_PROFILE_IDENTITY_COMPLETION_REQUIRED',
              'native_paid': profile(N), 'helper_target': profile(H),
              'paired_paid': profile(P2), 'paired_target': profile(T2),
              'Q_paid': profile(Q), 'multiplicity': m,
              'conditional_complete_paid': profile(Pm), 'conditional_complete_target': profile(Tm),
              'formula': 'P_m=(m/2)P2-18(m-1)N+18(m-1)Q; T_m=(m/2)T2-18(m-1)H',
              'premises': ['Q must implement every main target at every required width.', 'Each even-m root pairing uses the actual unchanged E-free scalar caller.', 'All new physical maps, ordinary work and owned costs must be admitted.', 'Strict covered and ordinary BIT saving and compatible complex supplier remain open.']}
    M2 = signed((1,T2),(-1,P2))
    limiting = signed((1,N),(-1,H),(Fraction(1,36),M2))
    rooms = {str(j): interval_record(moment(signed((1,limiting),(-1,Q),(Fraction(1,36*(j-1)),M2))))
             for j in (2,4,6,8,16,32)}
    budget['at_t_199_over_200'] = {
        'original_paired_margin': interval_record(moment(M2)),
        'Q_moment': interval_record(moment(Q)),
        'limiting_Q_allowance': interval_record(moment(limiting)),
        'limiting_remaining_completion_room': interval_record(moment(signed((1,limiting),(-1,Q)))),
        'fixed_even_m_remaining_completion_room': rooms,
        'mcopy_conditional_complete_margin': interval_record(moment(signed((1,Tm),(-1,Pm)))),
        'formula': 'allowance_m=(N-H)_t+[m/(36(m-1))]*(T2-P2)_t; room=allowance_m-Q_t',
    }
    need(moment(M2)[1] < 0, 'Original paired target fails')
    need(moment(signed((1,Tm),(-1,Pm)))[0] > 0, 'Provisional m4 margin before omitted completion is positive')
    for name, obj in [('RAIL-RESULT.json',receipt),(f'M{m}-RESULT.json',info),('BUDGET.json',budget)]:
        (a.output/name).write_text(json.dumps(obj, indent=2)+'\n')
    print(json.dumps({'rail':{k:receipt[k] for k in ['operations','paid_profile','residual_rank','residual_nonzero_coefficients','peak_owned']}, 'mcopy':info}, indent=2))

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--multiplicity',type=int,default=4)
    main(p.parse_args())
