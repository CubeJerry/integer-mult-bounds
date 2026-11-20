#!/usr/bin/env python3
"""Raw-DAG backward review; no author/source-construction code imports."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def add(row, other, scale=F(1)):
    for j, x in other.items():
        y = row.get(j, 0) + scale*x
        if y:
            row[j] = y
        else:
            row.pop(j, None)


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
pkg = Path(__file__).resolve().parent
for path, digest in json.loads((pkg/'SOURCE-PINS.json').read_text())['files'].items():
    need(sha256((args.repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
base = args.repo/'research/moonshot-005-program/results'
raw = gzip.decompress((base/'complex-native-funded-donor-cuts/inputs/DOUBLE-CANDIDATE.json.gz').read_bytes())
need(sha256(raw).hexdigest() == '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48', 'unpacked source')
w = json.loads(raw)
n = len(w['initial'])
need(n == len(w['final']) == 1289, 'complete endpoint inventory')
old_forms = {e: {j: F(x) for j, x in row} for e, row in w['forms']}
forms = {e: row.copy() for e, row in old_forms.items()}
schedule = [e for e in w['schedule'] if e != 95914]
del forms[95914]
routes = {e: (u, v) for e, u, v in w['moves'] if e != 95914}
routes.update({94019: (3, 278), 90369: (3, 304), 88: (278, 127)})
observer = max(schedule)+1
schedule.insert(schedule.index(90369)+1, observer)
routes[observer] = (3, 282)
forms[94019] = {~1288: F(1)}
forms[90369] = old_forms[94019].copy()
forms[88] = {**old_forms[95914], 94019: F(-845660160)}
forms[observer] = old_forms[90369].copy()
for e in schedule:
    if e in (94019, 90369, 88, observer):
        continue
    if 94019 in forms[e]:
        forms[e][90369] = forms[e].pop(94019)
    if 90369 in old_forms[e]:
        forms[e][observer] = forms[e].pop(90369)
ends = [w['first_output']+i for i in range(n)]
terminal_chart = dict(zip(ends, w['final']))
holders = {~j: chart for j, chart in enumerate(w['initial'])}
for e in schedule:
    chart = routes[e][0] if e in routes else terminal_chart[e]
    need(all(holders.get(j) == chart for j in forms[e]), 'actual local operands '+str(e))
    if e in routes:
        holders[e] = routes[e][1]
candidates = [86, 97232, 97241, 97323, 99064]
pos = {e: j for j, e in enumerate(candidates)}


def backward(slot, rows, order, capture=True):
    weights = {slot: F(1)}
    exposures = [F(0)]*5
    for e in reversed(order):
        q = weights.pop(e, 0)
        if e in pos and capture:
            exposures[pos[e]] = q
        if q:
            add(weights, rows[e], q)
    need(all(j < 0 for j in weights), 'complete backwards source expansion')
    return {~j: q for j, q in weights.items()}, exposures


E, B = [], []
for slot in ends:
    row, response = backward(slot, forms, schedule)
    old, _ = backward(slot, old_forms, w['schedule'], False)
    need(row == old, 'compensated full target '+str(slot))
    E.append(row)
    B.append(response)
print('Reconstructed all 1289 endpoints by reverse DAG expansion.', flush=True)
P, H = [], []
for k, slot in enumerate(candidates):
    row, response = backward(slot, forms, schedule)
    need(response[k] == 1, 'self injection response')
    response[k] = F(0)
    P.append(row)
    H.append(response)
need(H == [[F(0)]*5 for _ in range(5)], 'zero pre-payload interaction')

# Sparse elimination of the complete target, without component inversion.
pivots = {}
for i, entry in reversed(list(enumerate(E))):
    row, right = entry.copy(), {i: F(1)}
    while row:
        j = min(row)
        q = row[j]
        if j not in pivots:
            pivots[j] = ({k: x/q for k, x in row.items()}, {k: x/q for k, x in right.items()})
            break
        left, previous = pivots[j]
        add(row, left, -q)
        add(right, previous, -q)
    else:
        raise ValueError('singular complete endpoint')
need(set(pivots) == set(range(n)), 'all source pivots')
inverse = [{} for _ in range(n)]
for j in reversed(range(n)):
    row, right = pivots[j]
    inverse[j] = right.copy()
    for k, x in row.items():
        if k != j:
            add(inverse[j], inverse[k], -x)


def product(left, right):
    out = []
    for row in left:
        value = {}
        for j, q in row.items():
            add(value, right[j], q)
        out.append(value)
    return out


identity = [{j: F(1)} for j in range(n)]
need(product(E, inverse) == product(inverse, E) == identity, 'two complete inverse identities')
Q = product(P, inverse)
R = [[sum((q*B[i][j] for i, q in row.items()), F(0)) for j in range(5)] for row in inverse]
G = [[sum((q*B[i][j] for i, q in row.items()), F(0)) for j in range(5)] for row in Q]
need(G == [[F(i == j == 0) for j in range(5)] for i in range(5)], 'diagonal channel feedback')
canonical, names = [], {}
for frame in w['frames']:
    span = {0}
    for x in frame:
        span |= {y^x for y in tuple(span)}
    need(len(span) == 2**len(frame), 'chart basis')
    canonical.append(names.setdefault(tuple(sorted(span)), len(names)))
need(len(names) == 1102, 'all physical chart aliases identified')
ib = [canonical[c] for c in w['initial']]
ob = [canonical[c] for c in w['final']]
support = {(ib[j], ob[i]) for j, row in enumerate(inverse) for i in row}
table = [(86, 17, 131, F(-63, 128)), (97232, 17, 150, F(1, 2)),
         (97241, 19, 129, F(-1, 2)), (97323, 17, 776, F(1)),
         (99064, 19, 150, F(1, 2))]
witnesses = []
for j, (edge, a, b, coefficient) in enumerate(table):
    need(edge == candidates[j], 'isolation ordering')
    need((ib[a], ob[b]) not in support, 'entire inverse bank block zero')
    products = [R[a][k]*Q[k].get(b, 0) for k in range(5)]
    need(products == [coefficient if k == j else 0 for k in range(5)], 'single operator isolation')
    witnesses.append({'edge': edge, 'input_axis': a, 'output_axis': b,
                      'terminal_slot': ends[b], 'products': [str(x) for x in products],
                      'whole_bank_zero': True, 'input_bank_size': ib.count(ib[a]),
                      'output_bank_size': ob.count(ob[b])})
print('Verified all five inverse-bank isolators independently.', flush=True)


def vecsum(terms):
    out = [F(0), F(0)]
    for q, v in terms:
        out[0] += q*v[0]
        out[1] += q*v[1]
    return tuple(out)


def channel(k, v):
    a, b = v
    return [(a+b*b, b), (a*a, b+a*a), (a+b**3, b),
            (a+a*b, b**3), (a**3, b*b)][k]


def inverse_channel_zero(v):
    a, b = v
    return a-b*b, b


nonlinear_controls = []
for seed in (1, 2):
    x = [(F((i*seed)%7-3), F((i+seed)%5-2)) for i in range(n)]
    values = {~i: value for i, value in enumerate(x)}
    for e in schedule:
        value = vecsum((q, values[i]) for i, q in forms[e].items())
        values[e] = channel(pos[e], value) if e in pos else value
    target = [values[e] for e in ends]
    payload = [vecsum((q, x[i]) for i, q in row.items()) for row in P]
    delta = [vecsum([(1, channel(j, v)), (-1, v)]) for j, v in enumerate(payload)]
    expected = [vecsum([(1, vecsum((q, x[j]) for j, q in E[i].items()))]
                       + [(B[i][j], delta[j]) for j in range(5)]) for i in range(n)]
    need(target == expected, 'nonlinear literal endpoint formula')
    observed = [vecsum((q, target[i]) for i, q in row.items()) for row in Q]
    correction = [vecsum([(1, inverse_channel_zero(observed[0])), (-1, observed[0])])]
    correction += [vecsum([(1, observed[j]), (-1, channel(j, observed[j]))]) for j in range(1, 5)]
    restored = [vecsum([(1, vecsum((q, target[i]) for i, q in row.items()))]
                       + [(R[a][j], correction[j]) for j in range(5)])
                for a, row in enumerate(inverse)]
    need(restored == x, 'nonlinear inverse restores every original field')
    nonlinear_controls.append({'seed': seed, 'width': 2, 'fields_restored': n})

# Constant offsets are an essential positive control for the nonlinear theorem.
offsets = [(F(j+1), F(2-j)) for j in range(5)]
out_shift = [vecsum((B[i][j], offsets[j]) for j in range(5)) for i in range(n)]
need(any(any(v) for v in out_shift), 'nontrivial permitted translation control')
values = {~i: (F(0), F(0)) for i in range(n)}
for e in schedule:
    value = vecsum((q, values[i]) for i, q in forms[e].items())
    values[e] = vecsum([(1, value), (1, offsets[pos[e]])]) if e in pos else value
need([values[e] for e in ends] == out_shift, 'literal constant-offset positive control')
kernel = {a: row[0] for a, row in enumerate(R) if row[0]}
need(bool(kernel), 'nonzero edge-86 deletion kernel')
need([sum((q*kernel.get(a, 0) for a, q in row.items()), F(0)) for row in P] == [1, 0, 0, 0, 0], 'kernel channel coordinates')
need(all(sum((q*kernel.get(a, 0) for a, q in row.items()), F(0)) == B[i][0] for i, row in enumerate(E)), 'edge-86 deletion cancels complete target')
nonlinear_dependencies = []
for j, (_, a, b, _) in enumerate(table):
    for k in range(1, 5):
        step = (F(k), F(k+1))
        inputs = [tuple(q*value for value in step) for q in [row.get(b, 0) for row in Q]]
        changes = [vecsum([(1, inverse_channel_zero(inputs[0])), (-1, inputs[0])])]
        changes += [vecsum([(1, inputs[h]), (-1, channel(h, inputs[h]))]) for h in range(1, 5)]
        actual = vecsum((R[a][h], changes[h]) for h in range(5))
        if any(actual):
            nonlinear_dependencies.append({'edge': candidates[j], 'step': [str(x) for x in step], 'inverse_difference': [str(x) for x in actual]})
            break
    else:
        raise ValueError('failed nonlinear dependency control')
result = {'status': 'PASS_ROOT_NONLINEAR_FIVE_MESSAGE_BOUNDARY_REVIEW',
          'endpoint_fields': n, 'physical_charts': len(names),
          'source_method': 'raw JSON; explicit paid surgery; reverse DAG derivatives; whole sparse elimination',
          'author_code_imported': False, 'full_endpoint_restored_by_control': True,
          'H': [[str(v) for v in row] for row in H],
          'G': [[str(v) for v in row] for row in G], 'witnesses': witnesses,
          'nonlinear_full_word_controls': nonlinear_controls,
          'nonlinear_inverse_dependencies': nonlinear_dependencies,
          'edge_86_deletion_noninjective': True,
          'translation_positive_control': True,
          'theorem': 'With other forms and routes fixed, arbitrary per-message functions compatible with independent boundary-bank bijections are exactly translations. Zero-preserving functions are identity.',
          'not_claimed': 'No restriction on coupled internal recoding or new communication; no new supplier or exponent.'}
args.out.mkdir(parents=True, exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
print(result['status'], n, len(witnesses), flush=True)
