#!/usr/bin/env python3
"""Independent forward symbolic audit of S008 endpoint reconstruction.

No author verifier imports. Prepared for @CubeJerry with OpenAI assistance.
Apache-2.0. Exact scalar identities tensor with any common field volume.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import time

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(p, msg):
    if not p:
        raise ValueError(msg)

def add(target, source, coefficient):
    for key, value in source.items():
        z = target.get(key, F(0)) + coefficient * value
        if z:
            target[key] = z
        elif key in target:
            del target[key]

def span(vectors):
    s = {0}
    for vector in vectors:
        s.update([a ^ vector for a in tuple(s)])
    return frozenset(s)

def interpret(native, word):
    n = word['public']
    locations = dict(enumerate(word['initial']))
    rows = {i: {i: F(1)} for i in range(n)}
    spaces = [span(f) for f in native['frames']]
    counts, moves = Counter(), Counter()
    peak = lifetimes = 0
    guards = []
    for event, op in enumerate(word['program']):
        tag, target = op[:2]
        need(0 <= target < n + word['owned_fields'], 'role range')
        counts[tag] += 1
        if tag == 'INIT':
            need(target >= n and target not in rows, 'fresh owned initialization')
            rows[target] = {}
            locations[target] = op[2]
            lifetimes += 1
        elif tag == 'CLEAR':
            need(target >= n and locations.get(target) == op[2], 'owned clear')
            del rows[target]
            del locations[target]
        elif tag == 'MOVE':
            old, new, owned = op[2:]
            need(type(owned) is bool and owned == (target >= n), 'ownership')
            need(locations.get(target) == old, 'MOVE actual departure')
            need(spaces[old] < spaces[new] or owned and spaces[new] < spaces[old], 'nested permitted MOVE')
            moves[abs(len(native['frames'][old]) - len(native['frames'][new]))] += 1
            locations[target] = new
        elif tag in ('ADD', 'COPY'):
            source, coefficient, chart = op[2:]
            q = F(coefficient)
            need(source != target and q and locations.get(target) == locations.get(source) == chart, 'actual cochart operands')
            if tag == 'COPY':
                need(not rows[target], 'all-input COPY zero guard')
                guards.append(event)
            add(rows[target], rows[source], q)
        elif tag == 'SCALE':
            coefficient, chart = F(op[2]), op[3]
            need(coefficient and locations.get(target) == chart, 'typed nonzero SCALE')
            rows[target] = {i: coefficient * value for i, value in rows[target].items()}
        else:
            raise ValueError('unknown opcode ' + tag)
        peak = max(peak, len(rows) - n)
    need(set(rows) == set(range(n)), 'all public outputs and no live owned field')
    return rows, locations, dict(counts=dict(counts), move_histogram=dict(sorted(moves.items())), peak_owned=peak, owned_lifetimes=lifetimes, COPY_guards=guards)

def root(v):
    present = [i for i in range(9) if v & (1 << i)]
    if len(present) == 3:
        if 8 in present:
            return [2 if k in present else 0 for k in range(8)]
        return [1 if k in present else -1 for k in range(8)]
    need(len(present) == 7, 'port weight')
    a, b = [i for i in range(9) if i not in present]
    if b == 8:
        return [1 if k == a else -1 for k in range(8)]
    return [2 * (int(k == a) - int(k == b)) for k in range(8)]

def matrix_rank(matrix):
    pivots = {}
    for values in matrix:
        row = {i: F(x) for i, x in enumerate(values) if x}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = row[pivot]
                pivots[pivot] = {i: value / scale for i, value in row.items()}
                break
            add(row, pivots[pivot], -row[pivot])
    return len(pivots)

def root_floor(n, degree):
    lo, hi = 0, 1 << ((n.bit_length() + degree - 1) // degree)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** degree <= n:
            lo = mid
        else:
            hi = mid
    return lo

def native_target(native):
    out = {i: {i: F(1)} for i in range(native['public'])}
    hosted = set(native['hosted']['Dports'])
    for i, x in enumerate(native['live']):
        y = x + 112
        if i in hosted:
            out[y] = {x: F(1), y: F(1)}
        else:
            out[x] = {x: F(1), y: F(-1)}
            out[y] = {x: F(1, 2), y: F(1, 2)}
    for x, y in zip(native['hosted']['X2'], native['hosted']['Y2']):
        out[x] = {x: F(1), y: F(-1)}
    return out

def run(args):
    started = time.monotonic()
    source_bytes = args.source.read_bytes()
    need(hashlib.sha256(source_bytes).hexdigest() == PIN, 'exact immutable source')
    native = json.loads(gzip.decompress(source_bytes))
    payload = gzip.decompress(args.word.read_bytes())
    word = json.loads(payload)
    source_rows, source_locations, source_receipt = interpret(native, native)
    need(source_rows == native_target(native), 'fresh forward full1480 source audit')
    need(source_locations == dict(enumerate(native['final'])), 'native final charts')
    need(source_receipt['COPY_guards'] == [31737], 'source COPY guard position')
    xs = sorted(native['live'])
    main = sorted(set(xs) | {x+112 for x in xs} | set(native['hosted']['X2']) | set(native['hosted']['Y2']))
    raw = {x: 1480+i for i, x in enumerate(main)}
    need(word['initial'] == native['initial'] + [native['initial'][r] for r in main], 'authentic all1880 initial charts')
    need(word['public'] == 1880, 'authentic all1880 input namespace')
    need(word['difference_role_map'] == {str(x): y for x, y in raw.items()}, 'raw roles derived from source')
    aa = [root(native['ports'][i]) for i in range(104)]
    need([[sum(a[i]*a[j] for a in aa) for j in range(8)] for i in range(8)] == [[104*int(i==j) for j in range(8)] for i in range(8)], 'tight frame identity AA^T=104I')
    gram = [[F(sum(a*b for a,b in zip(aa[i],aa[j])),8) for j in range(104)] for i in range(104)]
    coupled = sorted(set(range(104)) - set(native['hosted']['Dports']))
    reverse = {i: (x,y) for i,x,y in zip(native['hosted']['Dports'], native['hosted']['X2'], native['hosted']['Y2'])}
    for i in coupled:
        reverse[i] = (xs[i], xs[i]+112)
    expected = {i: {i:F(1)} for i in range(1880)}
    for bank in [dict(enumerate(range(1480))), raw]:
        for i, x in enumerate(xs):
            c = F(1,2) if i in coupled else F(1)
            row = {bank[x+112]:c}
            for j, donor in enumerate(xs):
                if gram[i][j]:
                    add(row, {bank[donor]:F(1)}, c*gram[i][j])
            expected[bank[x+112]] = row
            xr, _ = reverse[i]
            row = {bank[xr]:F(1)}
            for j in range(104):
                if gram[i][j]:
                    add(row, {bank[reverse[j][1]]:F(1)}, -gram[i][j])
            expected[bank[xr]] = row
    rows, locations, receipt = interpret(native, word)
    need(rows == expected, 'full1880 independent expected output matrix')
    final = native['final'] + [native['final'][r] for r in main]
    need(locations == dict(enumerate(final)), 'all physical final charts')
    need(len(word['program']) == 6952 and receipt['peak_owned'] == 9 and receipt['owned_lifetimes'] == 32, 'literal operation and owner count')
    block = []
    for i in coupled:
        block.append([F(i==j) for j in coupled] + [-gram[i][j] for j in coupled])
    for i in coupled:
        block.append([gram[i][j]/2 for j in coupled] + [F(int(i==j),2) for j in coupled])
    need(matrix_rank(block) == 16, 'coupled16-block invertible')
    need(matrix_rank([[gram[i][j]-int(i==j) for j in range(104)] for i in range(104)]) == 104, 'E8 residual rank104')
    native_hist = Counter(source_receipt['move_histogram'])
    raw_hist = Counter()
    for op in native['program']:
        if op[0]=='MOVE' and op[1] in raw:
            raw_hist[abs(len(native['frames'][op[2]])-len(native['frames'][op[3]]))] += 1
    invoice = json.loads(args.invoice.read_bytes())
    T = {int(k):v for k,v in invoice['T4'].items()}
    P = {int(k):v for k,v in invoice['P4'].items()}
    for r in set(native_hist)|set(raw_hist)|set(receipt['move_histogram']):
        P[r] = P.get(r,0) + 18*(receipt['move_histogram'].get(r,0)-native_hist[r]-raw_hist[r])
    need(all(v>=0 for v in P.values()), 'valid complete paid histogram')
    need(sum(P.values())==42480 and sum(T.values())==27344 and sum(r*T.get(r,0)-r*P.get(r,0) for r in set(T)|set(P))==1888, 'complete count and rank mass')
    den = 10**24
    lower = upper = 0
    for r in set(T)|set(P):
        d = T.get(r,0)-P.get(r,0)
        a = root_floor(r**199 * den**200, 200)
        b = a if a**200 == r**199 * den**200 else a+1
        lower += d*(a if d>=0 else b)
        upper += d*(b if d>=0 else a)
    margin=[str(F(lower,18*den)),str(F(upper,18*den))]
    need(F(14812385620139,10**12) < F(lower,18*den) < F(upper,18*den) < F(14812385620141,10**12), 'source-derived exact budget interval')
    mutants=[]
    for name, predicate, action in [
        ('missing_difference',lambda o:o[0]=='ADD' and o[1]>=1480 and o[2]<1480 and o[3]=='-1','omit'),
        ('missing_reverse_gain',lambda o:o[0]=='ADD' and o[3].startswith('-') and o[2]>=1880,'omit'),
        ('illegal_public_descent',lambda o:o[0]=='MOVE' and o[4] and len(native['frames'][o[2]])>len(native['frames'][o[3]]),'public'),
        ('missing_packet_transport',lambda o:o[0]=='MOVE' and o[4],'omit'),
    ]:
        bad=dict(word);bad['program']=[o.copy() for o in word['program']]
        index=next(i for i,o in enumerate(bad['program']) if predicate(o))
        if action=='omit':bad['program'].pop(index)
        else:bad['program'][index][4]=False
        try:
            actual,_,_=interpret(native,bad)
            need(actual==expected,'mutant endpoint mismatch')
        except ValueError as error:
            mutants.append({'mutation':name,'rejected':str(error)})
        else:
            raise ValueError('accepted mutation '+name)
    result=dict(status='PASS_INDEPENDENT_FORWARD_ENDPOINT_REVIEW',source_sha256=PIN,
                word_payload_sha256=hashlib.sha256(payload).hexdigest(),method='Independent forward symbolic matrices; no author verifier imports',
                source_all1480_rows_checked=True,source_COPY_guards=source_receipt['COPY_guards'],
                candidate_all1880_rows_checked=True,all_inputs_retained=True,coupled_block_rank=16,
                residual_matrix_rank=104,physical=receipt,correct_invoice='P4+18*(actual_word_MOVEs-source_common_MOVEs-source_raw_main_MOVEs)',
                paid_histogram=P,paid_count=sum(P.values()),target_count=sum(T.values()),rank_surplus=1888,
                moment_per_native_exact_bounds=margin,negative_controls=mutants,
                source_audit_method='Fresh forward arbitrary1480-input propagation; differs from author backward adjoints',
                scope='Finite partial normalized-field word and conditional invoice; residual corrections, uniform suppliers and all five foundations remain open.',
                seconds=round(time.monotonic()-started,3))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['seconds'],'output':str(args.output)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--invoice',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
