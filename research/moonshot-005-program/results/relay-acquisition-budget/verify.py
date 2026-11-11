"""Independent exact raw-gate budgets for two source-authentic acquisition routes."""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS = {
    'source': '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
    'invoice': 'b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248',
    'lifetime_result': '594999b1ba54a5dd5ef12a397acf9bc642edf347697042f9ed89ff07b3c9e7ea',
    'independent_source_rows': '91a38186efe495c3b35c1aae18c182bc1308e424700b4159fd347d2ae813712c',
}


def need(predicate, message):
    if not predicate:
        raise ValueError(message)


def pinned(path, name):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PINS[name], 'pin ' + name)
    return raw


def root200(n):
    x = 1 << ((n.bit_length() + 199) // 200)
    while True:
        y = (199*x + n//x**199)//200
        if y >= x:
            break
        x = y
    while x**200 > n:
        x -= 1
    while (x+1)**200 <= n:
        x += 1
    need(x**200 <= n < (x+1)**200, 'integer root')
    return x


def power(r, denominator):
    n = r**199 * denominator**200
    a = root200(n)
    b = a if a**200 == n else a+1
    return F(a, denominator), F(b, denominator)


def space(basis):
    values = {0}
    for vector in basis:
        values.update(x ^ vector for x in tuple(values))
    return frozenset(values)


def run(repository, lifetime, source_rows):
    source_path = repository/'research/shared-wire-split-composition/data/final.json.gz'
    w = json.loads(gzip.decompress(pinned(source_path, 'source')))
    invoice = json.loads(pinned(repository/'research/shared-core-target-obligations/INVOICE-RESULT.json', 'invoice'))
    prior = json.loads(pinned(lifetime/'RESULT.json', 'lifetime_result'))
    base = prior['variants']['eight']
    wordraw = gzip.decompress((lifetime/'eight.json.gz').read_bytes())
    need(hashlib.sha256(wordraw).hexdigest() == base['transcript_payload_sha256'], 'S8 word pin')
    word = json.loads(wordraw)
    rows = json.loads(pinned(source_rows, 'independent_source_rows'))['rows']
    r = {int(k): F(v) for k, v in rows['1481@30824'].items()}
    mnew = {}
    for name in ['130@30773', '151@30773', '399@30775']:
        for k, v in rows[name].items():
            mnew[int(k)] = mnew.get(int(k), F(0)) + F(v)
    mnew = {k: v for k, v in mnew.items() if v}
    support = set(r) | set(mnew)
    main = set(w['live']) | {q+112 for q in w['live']} | set(w['hosted']['X2']) | set(w['hosted']['Y2'])
    entry = {q for q in main if w['initial'][q] == 3}
    nonentry = main-entry
    need(len(entry) == len(nonentry) == 200 and all(w['final'][q] == 127 for q in nonentry), '200 nonentry itinerary endpoints')
    support_entry, support_nonentry = support & entry, support & nonentry
    need([len(r), len(mnew), len(support), len(support_entry), len(support_nonentry)] == [59, 26, 60, 8, 52], 'actual relay support')
    spaces = list(map(space, w['frames']))
    dims = list(map(len, w['frames']))
    need(spaces[3] < spaces[541] < spaces[127] and [dims[i] for i in [3, 541, 127]] == [0, 7, 9], 'nested acquisition geometry')
    entry_facets = {q: w['final'][q] for q in sorted(support_entry)}
    need(all(dims[f] == 8 and spaces[f] < spaces[127] for f in entry_facets.values()), 'eight actual final facets')
    owned = Counter(abs(dims[e[2]]-dims[e[3]]) for e in word['program'] if e[0] == 'MOVE' and e[1] >= w['public'])
    targets = Counter({int(k): v for k, v in invoice['T4'].items()})
    paid = Counter({int(k): v for k, v in invoice['P4'].items()})
    for rank, count in owned.items():
        paid[rank] += 18*count
    need(dict(paid) == {int(k): v for k, v in base['new_P'].items()} and dict(targets) == {int(k): v for k, v in base['new_T'].items()}, 'fresh full S8 invoice')
    denominator = 10**30
    powers = {rank: power(rank, denominator) for rank in set(targets) | set(paid) | {1, 2, 3, 7, 9}}

    def margin(profile):
        lo = hi = F(0)
        for rank in set(targets) | set(profile):
            count = targets[rank]-profile[rank]
            a, b = powers[rank]
            lo += count*(a if count >= 0 else b)
            hi += count*(b if count >= 0 else a)
        return lo, hi

    variants = {}
    for name, calls, expected in [
        ('four_aggregates', {2: 2, 7: 2}, (153090, 3328, 2)),
        ('eight_facet_copies', {1: 8, 2: 2}, (153198, 3436, 8)),
    ]:
        new = Counter(paid)
        for rank, count in calls.items():
            new[rank] += 18*count
        raw = margin(new)
        remaining = [x/18 for x in raw]
        cost = [sum(count*powers[rank][i] for rank, count in calls.items()) for i in [0, 1]]
        surplus = sum(rank*(targets[rank]-new[rank]) for rank in set(targets) | set(new))
        count_expected, surplus_expected, ceiling = expected
        need(sum(new.values()) == count_expected and surplus == surplus_expected, 'full counts and surplus ' + name)
        need(F(ceiling) < remaining[0] <= remaining[1] < F(ceiling+1), 'strict remaining moment ' + name)
        variants[name] = {
            'calls_per_native': calls, 'calls_callerwide': {k: 18*v for k, v in calls.items()},
            'new_P': dict(sorted(new.items())), 'paid_positions': sum(new.values()),
            'target_positions': sum(targets.values()), 'rank_surplus': surplus,
            'raw_margin_interval': list(map(str, raw)),
            'per_native_added_paid_moment_interval': list(map(str, cost)),
            'remaining_paid_moment_per_native_interval': list(map(str, remaining)),
            'further_positive_rank_arrival_ceiling': ceiling,
        }
    direct_remaining = list(map(F, variants['four_aggregates']['remaining_paid_moment_per_native_interval']))
    repair_upper = direct_remaining[1]-2*powers[2][0]
    rank3_upper = direct_remaining[1]-powers[3][0]
    need(repair_upper < 0 and rank3_upper < 0, 'direct profile cannot fund paused repairs or rank3')
    facet_remaining = list(map(F, variants['eight_facet_copies']['remaining_paid_moment_per_native_interval']))
    rank9_upper = facet_remaining[1]-powers[9][0]
    need(rank9_upper < 0, 'facet profile cannot fund one further rank9 call')
    saving = [2*powers[7][0]-8, 2*powers[7][1]-8]
    need(saving[0] > 0, 'eight facets cost less than two rank7 calls')
    return {
        'status': 'PASS_TWO_ACQUISITION_TARGET_BUDGETS', 'source_pins': PINS,
        'eight_word_payload_sha256': base['transcript_payload_sha256'],
        'raw_main_entry_nonentry_counts': [200, 200], 'nonentry_final_chart': 127,
        'relay_support_counts': {'r': 59, 'Mnew': 26, 'union': 60, 'entry': 8, 'nonentry': 52},
        'entry_support_final_facets': entry_facets,
        'chart_dimensions': {'3': 0, '541': 7, '127': 9},
        'native_repetitions': 18, 'new_T': dict(sorted(targets.items())),
        'S8_raw_margin_interval': list(map(str, margin(paid))),
        'power_grid': str(denominator), 'variants': variants,
        'facet_route_per_native_moment_saving_interval': list(map(str, saving)),
        'negative_controls': {
            'direct_plus_paused_loan_two_rank2_repairs_remaining_upper': str(repair_upper),
            'direct_plus_one_rank3_call_remaining_upper': str(rank3_upper),
            'facet_plus_one_rank9_call_remaining_upper': str(rank9_upper),
        },
        'scope': 'Complete provisional paid invoices with all S8 terms fixed and 18 copies of every additional complete call. Geometry and relay supports are source facts. Actual retiming, aggregation, scalar, ownership, precision, and joint composition remain separate construction obligations. No supplier admission or new kappa.'
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--lifetime', type=Path, required=True)
    parser.add_argument('--source-rows', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.repository, args.lifetime, args.source_rows)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'])
