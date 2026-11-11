#!/usr/bin/env python3
"""Exact cost-ledger verification; no native/supplier replay. Apache-2.0."""
import argparse
import ast
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATUS = 'PASS_TARGET_BIT_BOOTSTRAP'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def step(C, b):
    need(0 <= b < C < Q(1, 2), 'step domain')
    return C / (1 + C - b)


def closed(C, b, h):
    need(type(h) is int and h >= 0, 'fixed nonnegative depth')
    y = C ** h * (C - b) / (1 - b)
    return (C - y) / (1 - y)


def gaps(C, b, rho, out):
    a = (1 - rho) * C + rho * b
    return (out - b, a - out, rho - a, 1 - a - rho)


def witness(C, b, out):
    need(b < out < step(C, b), 'attainable strict target')
    lower = step(C, b)
    upper = min((C - out) / (C - b), (1 - C) / (1 - C + b))
    rho = (lower + upper) / 2
    need(min(gaps(C, b, rho, out)) > 0, 'constructed witness')
    return rho


def authenticate(roots):
    manifest = json.loads((HERE / 'SOURCES.json').read_text())
    found = {}
    for f in manifest['files']:
        candidates = [root / f['path'] for root in roots]
        path = next((p for p in candidates if p.is_file()), None)
        need(path is not None, 'missing source: ' + f['path'])
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        need(blob == f['git_blob'], 'Git blob: ' + f['path'])
        need(hashlib.sha256(data).hexdigest() == f['sha256'], 'SHA256: ' + f['path'])
        found[f['path']] = data.decode()
    return found


def source_outer(text, k, g, cap):
    """Extract unchanged source arithmetic; no supplier or gate bypass claimed."""
    tree = ast.parse(text)
    gate = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'gate')
    start = next(i for i, n in enumerate(gate.body)
                 if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                 and n.targets[0].id == 'k')
    end = next(i for i in range(start, len(gate.body))
               if isinstance(gate.body[i], ast.Assign)
               and isinstance(gate.body[i].targets[0], ast.Name)
               and gate.body[i].targets[0].id == 'functional')
    block = ast.Module(body=gate.body[start:end + 1], type_ignores=[])
    ns = {'F': Q, 'claim': k, 'gap': g, 'cap': cap}
    exec(compile(ast.fix_missing_locations(block), '<pinned-outer-section>', 'exec'), ns)
    need(len(ns['checks']) == 54 and len(ns['functional']) == 4, 'source outer inventory')
    return ns['checks'] + ns['functional']


@lru_cache(None)
def log_bounds(r):
    """Positive atanh series, with explicit geometric tail; r>=1."""
    need(type(r) is int and r >= 1, 'log domain')
    y = Q(r - 1, r + 1)
    n = 128
    lower = 2 * sum((y ** (2*j + 1) / (2*j + 1) for j in range(n)), Q(0))
    tail = 2 * y ** (2*n + 1) / ((2*n + 1) * (1-y*y))
    return lower, lower + tail


def exp_negative(x, terms):
    value = term = Q(1)
    for j in range(1, terms + 1):
        term *= -x / j
        value += term
    return value


def power_bounds(r, k):
    ll, lu = log_bounds(r)
    need(0 <= k * lu < 1, 'small exponential domain')
    return r * exp_negative(k*lu, 15), r * exp_negative(k*ll, 14)


def lift_guard():
    cap = Q(51, 10000)
    low = sum((power_bounds(r, cap)[0]*log_bounds(r)[0] for r in (9,4)), Q(0))
    low -= sum((r*log_bounds(r)[1] for r in (7,3,5)), Q(0))
    need(low > Q(9,100), 'uniform lift derivative through .0051')
    # Existing absolute-curvature sufficient condition fails at the target.
    d1lo = sum((r*log_bounds(r)[0] for r in (7,3,5)), Q(0))
    d1lo -= sum((r*log_bounds(r)[1] for r in (9,4)), Q(0))
    curvaturelo = sum((r*log_bounds(r)[0]**2 for r in (7,3,5,9,4)), Q(0))
    old_lower = d1lo + Q(1,200)*curvaturelo
    need(old_lower > Q(11,100), 'old sufficient guard genuinely fails')
    return {'interval_cap': str(cap), 'derivative_lower_proved': '9/100',
            'gain_lower': '(9/100)*k for 0<k<=51/10000',
            'old_guard_at_target_lower': '11/100'}


def run(roots):
    sources = authenticate(roots)
    selected = json.loads(sources['certificates/selected-result.json'])
    need(Q(selected['kappa']) == Q(363005817,100000000000), 'selected starting frontier')
    need([a['id'] for a in selected['assumptions']] ==
         ['native_all_columns','owned_erasure','compiler','precision_tape','analytic_recovery'],
         'five actual selected assumptions')
    application = sources['docs/research/pr-intake-evidence/pr7000-application/PROOF-REVIEW.md']
    need('covered\nsaving is .0038525298' in application and '.00385248' in application,
         'selected current application of repaired BIT geometry')
    cur = sources['research/paired-query-only-bit/check.py']
    need("RAW = Q('.00385253')" in cur and 'GAP = Q(1, 10 ** 10)' in cur,
         'current covered constants')
    need("atom = Q('.004')" in cur and "claim == Q('.00385248')" in cur,
         'current atom and ordinary price')
    bridge = sources['research/kappa-rebuild/bit/DELAYED-COVER-BRIDGE.md']
    need('delta>a_BIT' in bridge and 'delta<1-a_BIT' in bridge,
         'source separators, not C<rho')
    cases = comparisons = witnesses = 0
    # Universal statements are proved in PROOF; this finite exact grid corroborates.
    for ci in range(1, 20):
        C = Q(ci, 40)
        for j in range(0, 10):
            b = C * j / 10
            star = step(C, b)
            need(b < star < C < Q(1,2), 'one-step strict order')
            need((C-star)/(1-star) == C*(C-b)/(1-b), 'cross-ratio identity')
            for ri in range(1,100):
                rho = Q(ri,100)
                a = (1-rho)*C + rho*b
                need(min(rho,a,1-rho) <= star, 'all sampled rho obey upper bound')
                comparisons += 1
            for z in (Q(1,10),Q(1,2),Q(9,10)):
                out = b + z*(star-b)
                witness(C,b,out)
                need((C > out*(1-b)/(1-out)) == (out < star), 'inverse criterion')
                witnesses += 1
            recurrent = b
            for h in range(1,9):
                recurrent = step(C,recurrent)
                need(recurrent == closed(C,b,h), 'exact optimized finite-depth identity')
                cases += 1
    k = Q(1,200)
    b0 = Q('.00385248')
    Csel = Q('.0038525298')
    need(Csel < k and Q(1,250) < k, 'selected frozen-contract obstructions')
    inverse = k*(1-b0)/(1-k)
    need(inverse == Q(3112961,621875000), 'one-stage covered threshold')
    C = Q('.0050001')
    s1,s2 = closed(C,b0,1),closed(C,b0,2)
    need(s1 < k < s2, 'exact two-stage need')
    previous = b0
    rows = []
    for out in (Q('.00499424'),Q('.00500007')):
        rho=Q('.0051'); gs=gaps(C,previous,rho,out)
        need(min(gs)>0,'hypothetical complete witness gaps')
        rows.append({'old':str(previous),'rho':str(rho),'new':str(out),
                     'improvement_relaxation_adapter_stock_gaps':list(map(str,gs))})
        previous=out
    controls = {}
    def rejects(label, action):
        try: action()
        except ValueError: controls[label]='REJECT'
        else: raise ValueError('negative control accepted: '+label)
    rejects('one_step_supremum_equality',lambda:witness(C,b0,s1))
    rejects('one_stage_target_requires_two',lambda:witness(C,b0,k))
    rejects('covered_target_equality',lambda:witness(k,b0,k))
    rejects('old_atom_exponent_at_moonshot',lambda:need(min(gaps(C,b0,Q('.004'),k))>0,'atom gap'))
    a=(1-Q('.0051'))*C+Q('.0051')*b0
    rejects('zero_relaxation',lambda:need(min(gaps(C,b0,Q('.0051'),a))>0,'relaxation'))
    rejects('missing_stock_gap',lambda:need(min(gaps(C,b0,Q(999,1000),Q('.003853')))>0,'stock'))
    selected_outer=sources['research/shared-wire-split-composition/interval_gate.py']
    outer=source_outer(selected_outer,k,Q(1,10**8),previous)
    need(min(outer)>0,'hypothetical current 54+4 outer join')
    rejects('BIT_at_target_has_no_outer_slack',lambda:need(min(source_outer(selected_outer,k,Q(1,10**8),k))>0,'BIT gap'))
    return {'status':STATUS,'base_commit':'e54523517d0f03e58352e647c403a5af3e525a57',
            'scope':'Exact strict cost-ledger and source arithmetic; no new covered supplier or kappa',
            'finite_grid':{'stage_identities':cases,'rho_upper_comparisons':comparisons,'constructed_witnesses':witnesses},
            'target':str(k),'selected_ordinary':str(b0),'selected_covered':str(Csel),
            'one_stage_C_strict_threshold':str(inverse),'hypothetical_covered':str(C),
            'one_stage_supremum':str(s1),'two_stage_supremum':str(s2),'witness_stages':rows,
            'outer_join':{'strict_count':54,'functional_count':4,'minimum_gap':str(min(outer)),
                          'complex_tested_hypothetical':str(k+Q(7,10**8)),
                          'complex_uniform_hypothetical':str(k+Q(6,10**8))},
            'lift_guard':lift_guard(),'negative_controls':controls,
            'new_kappa':None,'foundational_assumptions_discharged':[]}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-root',type=Path,action='append')
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=run(args.source_root or [HERE.parents[1]])
    expected=HERE/'RESULT.json'
    if args.write:expected.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(expected.read_text()),'frozen exact receipt')
    print(json.dumps(result,indent=2))
