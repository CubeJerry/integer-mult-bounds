"""Independent source-bound owner/chart census; no imported supplier code.

Native scalar semantics and all-column provider contracts remain inherited.
"""
import argparse
import ast
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import re

WORD_HASH = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
RECEIPT_HASH = 'd9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def checked_word(raw):
    need(hashlib.sha256(raw).hexdigest() == WORD_HASH, 'compressed word hash')
    return json.loads(gzip.decompress(raw))

def census(w):
    need(w['public'] == 1480 and len(w['program']) == 71261, 'source dimensions')
    spans = []
    for basis in w['frames']:
        span = {0}
        for v in basis:
            need(v not in span, 'independent binary frame basis')
            span |= {x ^ v for x in tuple(span)}
        spans.append(span)
    dims = list(map(len, w['frames']))
    main = (set(w['live']) | {112+i for i in w['live']}
            | set(w['hosted']['X2']) | set(w['hosted']['Y2']))
    need(len(main) == 400, 'distinct main allocation')
    need(all(0 <= i < w['public'] for i in main), 'main range')
    counts = {name: Counter() for name in ('main', 'helper', 'owned')}
    current = dict(enumerate(w['initial']))
    live_owned = set()
    peak = init = clear = 0
    for index, e in enumerate(w['program']):
        op = e[0]
        if op == 'INIT':
            owner, chart = e[1:3]
            need(w['public'] <= owner < w['public']+w['owned_fields'], 'owned INIT range')
            need(owner not in current, 'fresh owned lifetime')
            current[owner] = chart
            live_owned.add(owner)
            peak = max(peak, len(live_owned))
            init += 1
        elif op == 'CLEAR':
            owner, chart = e[1:3]
            need(owner in live_owned and current[owner] == chart, 'CLEAR chart/lifetime')
            live_owned.remove(owner)
            del current[owner]
            clear += 1
        elif op == 'MOVE':
            owner, a, b = e[1:4]
            need(current.get(owner) == a, 'MOVE actual source chart')
            need(spans[a] < spans[b] or spans[b] < spans[a], 'nested positive paid pair')
            kind = 'main' if owner in main else ('helper' if owner < w['public'] else 'owned')
            counts[kind][abs(dims[a]-dims[b])] += 1
            current[owner] = b
        elif op in ('ADD', 'COPY'):
            a, b, chart = e[1], e[2], e[4]
            need(a != b and current.get(a) == current.get(b) == chart, 'cochart distinct contact')
        elif op == 'SCALE':
            need(current.get(e[1]) == e[3], 'SCALE chart')
        else:
            raise ValueError('unknown source operation at '+str(index))
    need(not live_owned and init == clear == 54 and peak == 43, 'owned chronology')
    need(current == dict(enumerate(w['final'])), 'final chart vector')
    H = Counter()
    for owner in set(range(w['public']))-main:
        a, b = w['initial'][owner], w['final'][owner]
        need(spans[a] < spans[b], 'positive nested helper endpoint')
        H[dims[b]-dims[a]] += 1
    hosted = w['hosted']
    need(len(w['live']) == 104 and len(hosted['Dports']) == 96, 'port counts')
    need((hosted['mode'], hosted['alpha'], hosted['beta'], hosted['alpha2'], hosted['beta2'])
         == ('mix-t0', '-1', '1/2', '-1', '0'), 'mixed-port source parameters')
    equalities = 0
    for pos, index in enumerate(hosted['Dports']):
        x, x2, y2 = w['live'][index], hosted['X2'][pos], hosted['Y2'][pos]
        for endpoint in ('initial', 'final'):
            need(w[endpoint][x] == w[endpoint][x2], 'X/X2 boundary charts')
            need(w[endpoint][112+x] == w[endpoint][y2], 'Y/Y2 boundary charts')
            equalities += 2
    return {'owner_paid': counts, 'helpers': H, 'boundary_equalities': equalities,
            'coupled_port_indices': sorted(set(range(104))-set(hosted['Dports'])),
            'frame_count': len(spans), 'owned_lifetimes': init, 'owned_peak': peak}

def rejected(thunk):
    try:
        thunk()
    except ValueError:
        return True
    return False

def run(word_path, invoice_path, js_path):
    raw = word_path.read_bytes()
    w = checked_word(raw)
    receipt_raw = invoice_path.read_bytes()
    need(hashlib.sha256(receipt_raw).hexdigest() == RECEIPT_HASH, 'FULL-RESULT hash')
    receipt = json.loads(receipt_raw)
    result = census(w)
    parsed = {name: ast.literal_eval(body) for name, body in
              re.findall(r'const (T|P|H|G|O)=({[^;]*});', js_path.read_text())}
    need(set(parsed) == {'T', 'P', 'H', 'G', 'O'}, 'JS input dictionaries')
    ints = lambda d: {int(r): n for r, n in d.items()}
    need(parsed['T'] == ints(receipt['invoice']['T']), 'complete target transcription')
    need(parsed['P'] == ints(receipt['invoice']['P']), 'complete paid transcription')
    counts = result['owner_paid']
    need(sum(counts.values(), Counter()) == Counter(ints(receipt['native']['paid'])), 'all paid jobs')
    need(parsed['H'] == result['helpers'] == ints(receipt['native']['helpers']), 'helper credit transcription')
    need(parsed['G'] == counts['helper']+counts['owned'], 'nonmain paid transcription')
    need(parsed['O'] == counts['owned'], 'owned paid transcription')
    ordinary = receipt['ordinary']
    need((ordinary['scalar_upper'], ordinary['caller_total'], ordinary['lambda_second_charge'])
         == (1777040, 599605216, 14480000), 'source-invoice scalar/caller/LAMBDA inputs')
    need(ordinary['per_input_conversion'] == 18*1480*104, 'source input conversion tariff')
    routes = ordinary['route_items']
    need(routes == {'moves': 6310, 'helper_boundary': 2160, 'first_main_boundary': 208,
         'second_main_boundary': 192, 'first_main_adapter': 416,
         'second_main_adapter': 384, 'owned_lifetime': 216}, 'all native route categories')
    need(rejected(lambda: checked_word(raw+b'x')), 'corrupted-source hash control')
    bad = deepcopy(w)
    bad['hosted']['X2'][0] = bad['live'][0]
    need(rejected(lambda: census(bad)), 'aliased main allocation control')
    bad = deepcopy(w)
    bad['final'][bad['hosted']['Y2'][0]] = -1
    need(rejected(lambda: census(bad)), 'wrong final chart control')
    need(Counter(e[-1] for e in w['program'] if e[0] == 'MOVE')
         != Counter(ints(receipt['native']['paid'])), 'trailing phase flag is not rank')
    return {'status': 'PASS_INDEPENDENT_SOURCE_OWNER_CHART_CENSUS',
            'word_sha256': WORD_HASH, 'invoice_sha256': RECEIPT_HASH,
            'js_sha256': hashlib.sha256(js_path.read_bytes()).hexdigest(), **result,
            'controls_rejected': ['corrupt compressed source', 'aliased main allocation',
                                  'wrong final chart', 'phase Boolean used as rank'],
            'scope': 'Source owner/frame/contact chronology and profile transcriptions; inherited scalar endpoint, zero-CLEAR, phase-factorization and all-column contracts remain unproved here.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--word', type=Path, default=Path(__file__).resolve().parents[2]/'research/shared-wire-split-composition/data/final.json.gz')
    p.add_argument('--invoice', type=Path, default=Path(__file__).resolve().parents[2]/'research/shared-wire-split-composition/FULL-RESULT.json')
    p.add_argument('--js', type=Path, default=Path(__file__).with_name('exact_invoice.js'))
    args = p.parse_args()
    print(json.dumps(run(args.word, args.invoice, args.js), indent=2))
