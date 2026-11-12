#!/usr/bin/env python3
"""Fuse unobserved private-carrier transport in the authenticated unit17 word."""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

SOURCE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT = 'c75f595393d32f0ddefed906e9dab02e6e09b764730684541375d6979c6c349c'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def touches(op):
    if op[0] in ('ADD', 'COPY'):
        return (op[1], op[2])
    return (op[1],)


def space(frame):
    out = {0}
    for v in frame:
        out.update(x ^ v for x in tuple(out))
    return frozenset(out)


def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def profile(program, roles, dimensions):
    return Counter(abs(dimensions[e[3]] - dimensions[e[2]]) for e in program if e[0] == 'MOVE' and e[1] in roles)


def pow_bounds(r, denominator=10**30):
    if not r:
        return (Fraction(0), Fraction(0))
    target = r**199 * denominator**200
    lo, hi = 0, r * denominator + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid**200 <= target:
            lo = mid
        else:
            hi = mid
    need(lo**200 <= target < (lo + 1)**200, 'directed integer root')
    return Fraction(lo, denominator), Fraction(lo if lo**200 == target else lo + 1, denominator)


def main(args):
    source_bytes = args.source.read_bytes()
    parent_bytes = args.parent.read_bytes()
    need(hashlib.sha256(source_bytes).hexdigest() == SOURCE, 'native source pin')
    need(hashlib.sha256(parent_bytes).hexdigest() == PARENT, 'parent word pin')
    native, parent = map(lambda b: json.loads(gzip.decompress(b)), (source_bytes, parent_bytes))
    frames = list(map(space, native['frames']))
    dimensions = list(map(len, native['frames']))
    raw = set(map(int, parent['difference_role_map'].values()))
    need(raw == set(range(1480, 1880)), 'private carrier range')
    program = parent['program']
    pending, blocks = {}, []
    for event, op in enumerate(program):
        if op[0] == 'MOVE' and op[1] in raw:
            pending.setdefault(op[1], []).append(event)
        else:
            for role in touches(op):
                if role in pending:
                    blocks.append((role, pending.pop(role)))
    blocks.extend(pending.items())
    blocks.sort(key=lambda item: item[1][-1])
    replacements, deleted, certificates = {}, set(), []
    for role, events in blocks:
        first, last = program[events[0]], program[events[-1]]
        old = first[2]
        for event in events:
            op = program[event]
            need(op == ['MOVE', role, old, op[3], False], 'contiguous private route')
            need(frames[old] < frames[op[3]], 'strict upward source nesting')
            old = op[3]
        endpoint = last[3]
        need(frames[first[2]] < frames[endpoint], 'fused upward nesting')
        for event in range(events[0], events[-1] + 1):
            op = program[event]
            if role in touches(op):
                need(event in events, 'no intervening use of the transported carrier')
        replacement = ['MOVE', role, first[2], endpoint, False]
        replacements[events[-1]] = replacement
        deleted.update(events[:-1])
        certificates.append({'role': role, 'parent_events': events, 'emitted_at_parent_event': events[-1], 'replacement': replacement})
    fused = []
    marks = []
    lineage = []
    for event, (op, mark) in enumerate(zip(program, parent['marks'])):
        if event in deleted:
            continue
        fused.append(replacements.get(event, op))
        marks.append('fused_private_route' if event in replacements else mark)
        lineage.append(event)
    need(len(replacements) == len(blocks), 'one output per route segment')
    for rec in certificates:
        rec['physical_event'] = lineage.index(rec['emitted_at_parent_event'])
    word = {k: v for k, v in parent.items() if k not in ('program', 'marks', 'funded_raw_reservations', 'schema')}
    word.update(schema='unit17-unobserved-private-route-fusion-v1', program=fused, marks=marks,
                parent_word_sha256=PARENT, parent_event_of_output=lineage,
                private_route_blocks=certificates,
                reservation_accounting='Old raw reservations are replaced by the emitted fused transport profile. Removed source stops cannot be reused for free.')
    old_profile = profile(program, raw, dimensions)
    new_profile = profile(fused, raw, dimensions)
    powers = {r: pow_bounds(r) for r in range(1, 10)}
    saved_low = saved_high = Fraction(0)
    for r in range(1, 10):
        c = old_profile[r] - new_profile[r]
        saved_low += c * powers[r][0 if c >= 0 else 1]
        saved_high += c * powers[r][1 if c >= 0 else 0]
    invoice_bytes = args.invoice.read_bytes()
    need(hashlib.sha256(invoice_bytes).hexdigest() == 'b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248', 'complete H4 invoice pin')
    invoice = json.loads(invoice_bytes)
    target = Counter({int(r): n for r, n in invoice['T4'].items()})
    paid = Counter({int(r): n for r, n in invoice['P4'].items()})
    for r in old_profile.keys() | new_profile.keys():
        paid[r] += 18 * (new_profile[r] - old_profile[r])
    paid[1] += 18 * 17
    need(all(n >= 0 for n in paid.values()), 'nonnegative actual paid profile')
    all_powers = {r: pow_bounds(r) for r in target.keys() | paid.keys()}
    margin_low = margin_high = Fraction(0)
    for r in all_powers:
        c = target[r] - paid[r]
        margin_low += c * all_powers[r][0 if c >= 0 else 1]
        margin_high += c * all_powers[r][1 if c >= 0 else 0]
    baseline_low = baseline_high = Fraction(0)
    original_paid = {int(r): n for r, n in invoice['P4'].items()}
    for r in target.keys() | original_paid.keys():
        c = target[r] - original_paid.get(r, 0)
        baseline_low += c * all_powers[r][0 if c >= 0 else 1]
        baseline_high += c * all_powers[r][1 if c >= 0 else 0]
    args.output.mkdir(parents=True, exist_ok=True)
    payload = serialize(word)
    blob = gzip.compress(payload, compresslevel=9, mtime=0)
    (args.output / 'WORD.json.gz').write_bytes(blob)
    result = dict(status='BUILT_EXACT_UNOBSERVED_PRIVATE_ROUTE_FUSION', source_sha256=SOURCE,
                  parent_word_sha256=PARENT, parent_instructions=len(program), instructions=len(fused),
                  removed_moves=len(deleted), old_raw_profile=dict(sorted(old_profile.items())),
                  new_raw_profile=dict(sorted(new_profile.items())),
                  old_raw_calls=sum(old_profile.values()), new_raw_calls=sum(new_profile.values()),
                  unchanged_raw_rank=sum(r*n for r,n in old_profile.items()),
                  new_raw_rank=sum(r*n for r,n in new_profile.items()),
                  saved_moment_lower=str(saved_low), saved_moment_upper=str(saved_high),
                  saved_moment_decimal=float(saved_low),
                  word_sha256=hashlib.sha256(blob).hexdigest(), payload_sha256=hashlib.sha256(payload).hexdigest(),
                  route_segments=len(certificates), operations=dict(sorted(Counter(e[0] for e in fused).items())),
                  conditional_caller=dict(T4=dict(sorted(target.items())), P_rewritten_partial=dict(sorted(paid.items())),
                      target_positions=sum(target.values()), paid_positions=sum(paid.values()),
                      rank_surplus=sum(r*(target[r]-paid[r]) for r in target.keys() | paid.keys()),
                      remaining_moment_per_native_lower=str(margin_low/18),
                      remaining_moment_per_native_upper=str(margin_high/18),
                      remaining_moment_per_native_decimal=float(margin_low/18),
                      original_H4_allowance_lower=str(baseline_low/18), original_H4_allowance_upper=str(baseline_high/18),
                      remaining_private_cross_dependencies=191,
                      caveat='Actual completed partial word, conditional caller accounting only. The remaining191 private dependencies and every supplier/physical obligation are still charged when implemented; positive slack is not a full certificate.'),
                  scope='Exact word transformation preserves the full parent input/output contract; inherited scalar and physical foundations remain. Complete supplier is not constructed. The invoice requires all retained paths and later duties to be recomputed.')
    (args.output / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('instructions','removed_moves','new_raw_calls','saved_moment_decimal','word_sha256')}))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--parent', type=Path, required=True)
    ap.add_argument('--invoice', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    main(ap.parse_args())
