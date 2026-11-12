#!/usr/bin/env python3
"""Source-bound dyadic rank-eight broadcast prefix, with 1,880 input columns.

This is a partial construction. Side-information corrections are not supplied.
Prepared for CubeJerry with OpenAI assistance; Apache-2.0.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import itertools
import json
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def space(frame):
    out = {0}
    for v in frame:
        out |= {u ^ v for u in tuple(out)}
    return frozenset(out)

def root(v):
    bits = [i for i in range(9) if v >> i & 1]
    if len(bits) == 3:
        return [2 * (i in bits) for i in range(8)] if 8 in bits else [1 if i in bits else -1 for i in range(8)]
    require(len(bits) == 7, 'weight three or seven required')
    i, j = [i for i in range(9) if i not in bits]
    return [1 if k == i else -1 for k in range(8)] if j == 8 else [2 * ((k == i) - (k == j)) for k in range(8)]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def add(a, b, scale):
    z = a.copy()
    for i, v in b.items():
        value = z.get(i, Q(0)) + scale * v
        if value:
            z[i] = value
        else:
            z.pop(i, None)
    return z

def rank(rows):
    pivots = {}
    for row in rows:
        x = {i: Q(v) for i, v in enumerate(row) if v}
        while x:
            i = min(x)
            if i not in pivots:
                z = x[i]
                pivots[i] = {j: v / z for j, v in x.items()}
                break
            x = add(x, pivots[i], -x[i])
    return len(pivots)

def build(w):
    xs = sorted(w['live'])
    mains = sorted(set(xs) | {i + 112 for i in xs} | set(w['hosted']['X2']) | set(w['hosted']['Y2']))
    require(len(xs) == 104 and len(mains) == 400 and w['public'] == 1480, 'source dimensions')
    qm = {r: 1480 + i for i, r in enumerate(mains)}
    ports = [w['frames'][w['initial'][r]][0] for r in xs]
    require(ports == w['ports'], 'exact source port order')
    roots = [root(v) for v in ports]
    require(rank(roots) == 8, 'rank eight')
    coupled = sorted(set(range(104)) - set(w['hosted']['Dports']))
    require(len(coupled) == 8, 'eight coupled blocks')
    weight = {r: Q(1, 2) if i in coupled else Q(1) for i, r in enumerate(xs)}
    C = list(map(space, w['frames']))
    require(C[3] == {0} and len(C[127]) == 512, 'entry and hub charts')
    for r, v in zip(xs, ports):
        require(C[w['initial'][r]] == {0, v}, 'donor source line')
        require(C[w['initial'][r + 112]] == {0}, 'receiver initial chart')
        require(w['final'][r] == 127, 'donor ends at hub')
        require(C[w['final'][r + 112]] == {u for u in range(512) if (u & v).bit_count() % 2 == 0}, 'receiver facet')
    temp = 1880 + w['owned_fields']
    ops, marks, reservations = [], [], []
    def emit(op, why):
        marks.append({'physical_event': len(ops), 'purpose': why})
        ops.append(op)
    for r in mains:
        emit(['ADD', qm[r], r, '-1', w['initial'][r]], 'form_actual_difference')
    for event, op in enumerate(w['program']):
        if op[0] == 'MOVE' and op[1] in xs:
            require(op[4] is False, 'raw donor uses public main reservation')
            reservations.append({'source_event': event, 'physical_event': len(ops), 'logical_role': op[1], 'source': op[2], 'target': op[3]})
            emit(['MOVE', qm[op[1]], op[2], op[3], False], 'funded_donor_route')
    for i in coupled:
        emit(['SCALE', qm[xs[i] + 112], '1/2', 3], 'coupled_receiver_normalization')
    for k in range(8):
        emit(['INIT', temp, 127], 'packet_init')
        for r, a in zip(xs, roots):
            if a[k]:
                emit(['ADD', temp, qm[r], str(a[k]), 127], 'packet_encode')
        emit(['MOVE', temp, 127, 3, True], 'new_rank9_packet')
        for r, a in zip(xs, roots):
            if a[k]:
                emit(['ADD', qm[r + 112], temp, str(weight[r] * a[k] / 8), 3], 'receiver_packet_mix')
        emit(['CLEAR', temp, 3], 'packet_retire')
    ys = {r + 112 for r in xs}
    for event, op in enumerate(w['program']):
        if op[0] == 'MOVE' and op[1] in ys:
            require(op[4] is False, 'raw receiver uses public main reservation')
            reservations.append({'source_event': event, 'physical_event': len(ops), 'logical_role': op[1], 'source': op[2], 'target': op[3]})
            emit(['MOVE', qm[op[1]], op[2], op[3], False], 'funded_receiver_route')
    require(len({r['source_event'] for r in reservations}) == len(reservations), 'reservation used at most once')
    return dict(schema='moonshot-eight-packet-prefix-v1', source_sha256=PIN, public=1880,
                owned_fields=w['owned_fields'] + 1, initial=w['initial'] + [w['initial'][r] for r in mains],
                program=ops, marks=marks, reservations=reservations, donor_roles=xs,
                difference_role_map={str(r): q for r, q in qm.items()}, ports=ports, roots=roots,
                coupled_port_indices=coupled, receiver_weights={str(r): str(weight[r]) for r in xs},
                status='Partial actual-input broadcast prefix; side-information corrections and continuation open')

def execute(w, meta, ops):
    C = list(map(space, w['frames']))
    rows = {i: {i: Q(1)} for i in range(1880)}
    loc = dict(enumerate(meta['initial']))
    counts, hist = Counter(), Counter()
    lifetimes = peak = 0
    for op in ops:
        tag, dst = op[:2]
        require(0 <= dst < 1880 + meta['owned_fields'], 'role bound')
        counts[tag] += 1
        if tag == 'INIT':
            require(dst >= 1880 and dst not in loc, 'fresh owned initialization')
            rows[dst] = {}; loc[dst] = op[2]; lifetimes += 1
        elif tag == 'CLEAR':
            require(dst >= 1880 and loc.get(dst) == op[2], 'owned erasure contract')
            del rows[dst]; del loc[dst]
        elif tag == 'ADD':
            src, scalar, frame = op[2:]
            require(dst != src and loc.get(dst) == loc.get(src) == frame, 'cochart scalar access')
            require(Q(scalar) != 0, 'nonzero coefficient')
            rows[dst] = add(rows[dst], rows[src], Q(scalar))
        elif tag == 'SCALE':
            require(loc.get(dst) == op[3] and Q(op[2]) != 0, 'typed nonzero scale')
            rows[dst] = {i: Q(op[2]) * v for i, v in rows[dst].items()}
        elif tag == 'MOVE':
            a, b, own = op[2:]
            require(loc.get(dst) == a and type(own) is bool and own == (dst >= 1880), 'typed owned flag and source')
            require(C[a] < C[b] or own and C[b] < C[a], 'proper nested transport')
            loc[dst] = b; hist[abs(len(w['frames'][a]) - len(w['frames'][b]))] += 1
        else:
            raise ValueError('unknown operation')
        peak = max(peak, len(loc) - 1880)
    require(len(loc) == 1880, 'no live packet owners at boundary')
    return rows, loc, dict(counts=dict(counts), move_histogram=dict(sorted(hist.items())), owned_lifetimes=lifetimes, peak_owned=peak)

def expected_rows(w, meta):
    qm = {int(r): q for r, q in meta['difference_role_map'].items()}
    out = {i: {i: Q(1)} for i in range(1480)}
    out.update({q: {q: Q(1), r: Q(-1)} for r, q in qm.items()})
    xs, roots = meta['donor_roles'], meta['roots']
    for i, r in enumerate(xs):
        c = Q(meta['receiver_weights'][str(r)])
        row = {qm[r + 112]: c, r + 112: -c}
        for j, d in enumerate(xs):
            g = dot(roots[i], roots[j])
            if g:
                row = add(row, {qm[d]: Q(1), d: Q(-1)}, c * g / 8)
        out[qm[r + 112]] = row
    return out

def run(source, outdir, write):
    data = source.read_bytes(); require(hashlib.sha256(data).hexdigest() == PIN, 'source SHA256')
    w = json.loads(gzip.decompress(data)); meta = build(w)
    all_ports = [v for v in range(512) if v.bit_count() in (3, 7)]
    for v, z in itertools.product(all_ports, repeat=2):
        g = dot(root(v), root(z))
        require(g == 8 if v == z else g in ((0,) if (v & z).bit_count() % 2 else (-4, 4)), 'all120 Gram parity')
    payload = (json.dumps(meta, sort_keys=True, separators=(',', ':')) + '\n').encode()
    word = outdir / 'PREFIX.json.gz'
    if write:
        outdir.mkdir(parents=True, exist_ok=True); word.write_bytes(gzip.compress(payload, mtime=0))
    else:
        require(gzip.decompress(word.read_bytes()) == payload, 'full reconstructed prefix')
    rows, loc, bill = execute(w, meta, meta['program'])
    expected = expected_rows(w, meta); require(rows == expected, 'all1880 input-column postconditions')
    qm = {int(r): q for r, q in meta['difference_role_map'].items()}
    require(all(loc[i] == w['initial'][i] for i in range(1480)), 'common charts unchanged')
    xs = meta['donor_roles']; used = set(xs) | {r + 112 for r in xs}
    require(all(loc[q] == (w['final'][r] if r in used else w['initial'][r]) for r, q in qm.items()), 'exact raw route postconditions')
    require(bill['owned_lifetimes'] == 8 and bill['peak_owned'] == 1, 'serial packet lifetime count')
    nnz = sum(bool(a) for row in meta['roots'] for a in row)
    require(bill['counts']['ADD'] == 400 + 2 * nnz and bill['counts']['SCALE'] == 8, 'ordinary operations counted')
    # All input information survives: invert each receiver row using retained qX;
    # the nonzero receiver weight is then inverted. Other q and common rows persist.
    for i, r in enumerate(xs):
        recovered = rows[qm[r + 112]].copy(); c = Q(meta['receiver_weights'][str(r)])
        for j, d in enumerate(xs):
            recovered = add(recovered, rows[qm[d]], -c * dot(meta['roots'][i], meta['roots'][j]) / 8)
        recovered = {k: v / c for k, v in recovered.items()}
        require(recovered == {qm[r + 112]: Q(1), r + 112: Q(-1)}, 'global information preservation')
    controls = []
    for name, purpose, mutation in [('wrong_packet_sign','packet_encode','sign'), ('missing_rank9_route','new_rank9_packet','omit'), ('public_descent','new_rank9_packet','flag'), ('missing_difference','form_actual_difference','omit'), ('missing_receiver_normalization','coupled_receiver_normalization','omit'), ('duplicate_funded_route','funded_receiver_route','duplicate')]:
        at = next(x['physical_event'] for x in meta['marks'] if x['purpose'] == purpose)
        bad = [x.copy() for x in meta['program']]
        if mutation == 'omit': bad.pop(at)
        elif mutation == 'flag': bad[at][4] = False
        elif mutation == 'duplicate': bad.insert(at, bad[at].copy())
        else: bad[at][3] = str(-Q(bad[at][3]))
        try:
            r, _, _ = execute(w, meta, bad); require(r == expected, 'mutated boundary')
        except ValueError as error:
            controls.append({'mutation': name, 'rejection': str(error)})
        else:
            raise ValueError('accepted mutant ' + name)
    return dict(status='PASS_ACTUAL_DYADIC_EIGHT_PACKET_PREFIX', source_sha256=PIN,
        word_payload_sha256=hashlib.sha256(payload).hexdigest(), independent_physical_inputs=1880,
        source_ports=104, source_port_weights=dict(Counter(v.bit_count() for v in meta['ports'])),
        all120_Gram_pairs_checked=14400, root_rank=8, root_nonzeros=nnz,
        source_main_reservations_used=len(meta['reservations']),
        source_main_reservations_remaining=sum(op[0]=='MOVE' and op[1] in qm for op in w['program'])-len(meta['reservations']),
        new_paid_move_histogram={9:8}, new_paid_moment='8 * 9^(199/200)',
        prefix_instructions=len(meta['program']), bill=bill, all1480_common_values_and_charts_unchanged=True,
        global_input_information_preserved=True, private_receiver_outputs_corrected=False,
        corrections_required='At Y_i subtract c_i/8 * sum_{j!=i} (a_i dot a_j) qX_j; c_i=1 or1/2.',
        negative_controls=controls,
        scope='Finite typed prefix under retained native/all-column and owned-erasure semantics. No physical side-information delivery, complete shared word, uniform supplier, or new kappa.')

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--source', type=Path, required=True); p.add_argument('--outdir', type=Path, default=Path(__file__).resolve().parent); p.add_argument('--write-word', action='store_true'); p.add_argument('--output', type=Path)
    a = p.parse_args(); result = run(a.source, a.outdir, a.write_word); text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if a.output: a.output.write_text(text)
    print(text, end='')
