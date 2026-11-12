#!/usr/bin/env python3
"""Preterminal source-coupled completion, with exact precomposition evidence.

Prepared for @CubeJerry with OpenAI assistance. No complete supplier or kappa.
The paired-cohort parent is immutable. Run outputs into a separate directory.
"""
from __future__ import annotations
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

SOURCE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT = 'bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17'
PARENT_PAYLOAD = 'bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a'
COUPLED = (17, 19, 30, 38, 40, 47, 52, 60)

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load(p):
    b = p.read_bytes()
    return json.loads(gzip.decompress(b) if p.suffix == '.gz' else b)

def add(x, y, a=F(1)):
    z = x.copy()
    for j, c in y.items():
        v = z.get(j, F(0)) + a*c
        if v: z[j] = v
        else: z.pop(j, None)
    return z

def span(frame):
    s = {0}
    for v in frame:
        s |= {x ^ v for x in tuple(s)}
    return frozenset(s)

def prefix(word, source):
    """All 1880 columns, sparse rational interpreter without parent imports."""
    frames = source['frames'] + [x['frame'] for x in word.get('additional_charts', [])]
    spaces = list(map(span, frames))
    rows = {i: {i: F(1)} for i in range(1880)}
    loc = dict(enumerate(word['initial']))
    for t, op in enumerate(word['program'][:word['marks']['common_starts']]):
        k, r = op[:2]
        if k == 'INIT':
            need(r >= 1880 and r not in rows, 'fresh initializer')
            rows[r] = {}; loc[r] = op[2]
        elif k == 'CLEAR':
            need(r >= 1880 and loc.get(r) == op[2], 'valid retirement')
            del rows[r]; del loc[r]
        elif k == 'MOVE':
            a, b, owned = op[2:]
            need(loc.get(r) == a and owned == (r >= 1880), 'move source/owner')
            need(spaces[a] < spaces[b] or owned and spaces[b] < spaces[a], 'nested move')
            loc[r] = b
        elif k == 'SCALE':
            need(F(op[2]) and loc.get(r) == op[3], 'scale')
            rows[r] = {j: F(op[2])*v for j, v in rows[r].items()}
        elif k in ('ADD', 'COPY'):
            j, c, at = op[2:]
            need(r != j and loc.get(r) == loc.get(j) == at, 'cochart at '+str(t))
            need(k != 'COPY' or not rows[r], 'copy-zero guard')
            rows[r] = add(rows[r], rows[j], F(c))
        else:
            raise ValueError('unknown opcode '+k)
    return rows, loc

def substitution(row, raw):
    """Substitute v_X -> v_X-v_Y+u_Y, v_Y -> 2v_Y-u_Y."""
    replacements = {}
    for x in COUPLED:
        y = x+112
        replacements[raw[x]] = {raw[x]: F(1), raw[y]: F(-1), y: F(1)}
        replacements[raw[y]] = {raw[y]: F(2), y: F(-1)}
    out = {}
    for j, c in row.items():
        out = add(out, replacements.get(j, {j: F(1)}), c)
    return out

def root(v):
    bits = [i for i in range(9) if v >> i & 1]
    if len(bits) == 3:
        return [2*int(i in bits) for i in range(8)] if 8 in bits else [1 if i in bits else -1 for i in range(8)]
    need(len(bits) == 7, 'root weight')
    i, j = [i for i in range(9) if i not in bits]
    return [1 if k == i else -1 for k in range(8)] if j == 8 else [2*(int(k == i)-int(k == j)) for k in range(8)]

def make(source, parent):
    raw = {int(x): r for x, r in parent['private_role_map'].items()}
    hosted = {source['live'][i] for i in source['hosted']['Dports']}
    need(tuple(x for x in source['live'] if x not in hosted) == COUPLED, 'source coupled set')
    need(len(parent['program'][:400]) == 400 and all(o == ['ADD', raw[x], x, '-1', source['initial'][x]] for x, o in zip(sorted(raw), parent['program'][:400])), 'literal difference boundary')
    temp = 1880
    skip = {}
    for x in COUPLED:
        y = x+112
        need(source['initial'][y] == 3 and len(source['frames'][source['initial'][x]]) == 1, 'actual initial source charts')
        first = next((t, o) for t, o in enumerate(parent['program'][400:], 400) if o[1] == raw[y] or o[0] in ('ADD', 'COPY') and o[2] == raw[y])
        need(first[1] == ['SCALE', raw[y], '1/2', 3], 'first coupled Y use is half-scale')
        skip[first[0]] = x
    ops = []; lineage = []; boundaries = {}; events = {}; preloads = []
    for t, op in enumerate(parent['program']):
        if t == 400:
            for x in COUPLED:
                y = x+112; L = source['initial'][x]; start = len(ops)
                part = [['INIT', temp, 3], ['ADD', temp, raw[y], '1', 3], ['MOVE', temp, 3, L, True], ['ADD', raw[x], temp, '-1', L], ['CLEAR', temp, L]]
                ops.extend(part); lineage.extend([None]*len(part))
                preloads.append({'X': x, 'Y': y, 'line': L, 'first_event': start, 'instructions': len(part)})
        boundaries[t] = len(ops)
        if t in skip:
            continue
        events[t] = len(ops); ops.append(deepcopy(op)); lineage.append(t)
    need(len(skip) == 8 and len(ops) == len(parent['program'])+32, 'exact cancellation and instruction count')
    word = deepcopy(parent)
    word['parent_paired_collection_provenance'] = word.pop('paired_collection')
    word.update(schema='moonshot-S009-preterminal-coupled-eight-v1', program=ops,
                parent_word_sha256=PARENT, parent_event_of_output=lineage,
                native_event_to_physical=[events[t] for t in parent['native_event_to_physical']],
                marks={k: boundaries[v] for k, v in parent['marks'].items()},
                coupled_precondition={'source_roles': list(COUPLED), 'formula': 'x_tilde=x-y; y_tilde=2y', 'realized_double_half_cancellation': True, 'temporary': temp, 'preloads': preloads, 'deleted_parent_half_scales': sorted(skip), 'prior_source_marks_semantics': 'Every old raw-X original/restoration mark now refers to x_tilde; common inputs and hosted X2/Y2 remain unchanged.'})
    if 'all_active_donors_restored' in word['marks']:
        word['marks']['all_preconditioned_donors_restored'] = word['marks'].pop('all_active_donors_restored')
    return word, raw, skip

def main(args):
    repo = args.repo; out = args.output; out.mkdir(parents=True, exist_ok=True)
    sp = repo/'research/shared-wire-split-composition/data/final.json.gz'
    pp = repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz'
    rp = repo/'research/moonshot-005-program/results/paired-cohort/output/RESULT.json'
    sb, pb = sp.read_bytes(), pp.read_bytes()
    need(sha(sb) == SOURCE and sha(pb) == PARENT and sha(gzip.decompress(pb)) == PARENT_PAYLOAD, 'immutable input pins')
    source, parent, receipt = load(sp), load(pp), load(rp)
    word, raw, skip = make(source, parent)
    oldrows, oldloc = prefix(parent, source); rows, loc = prefix(word, source)
    need(oldloc == loc and set(oldrows) == set(rows), 'same physical prefix boundary')
    for r in rows:
        need(rows[r] == substitution(oldrows[r], raw), 'full1880-column precomposition at '+str(r))
    q = {x: {r: F(1), x: F(-1)} for x, r in raw.items()}
    for x in COUPLED:
        need(rows[raw[x]] == add(q[x], q[x+112], F(-1)), 'coupled reverse completed before common source')
    for y in parent['newly_completed_firstY_receivers']:
        need(rows[raw[y]] == add(q[y], q[y-112]), 'eight previous forward endpoints preserved')
    oldtail = parent['program'][parent['marks']['common_starts']:]
    need(word['program'][word['marks']['common_starts']:] == oldtail, 'literal unchanged common suffix')
    # Reuse the admitted full-word type and tariff functions; this is not independent review.
    rec = repo/'research/moonshot-005-program/results/cohort-reconstruction'
    sys.path.insert(0, str(rec))
    spec = importlib.util.spec_from_file_location('preterminal_parent_tools', rec/'build.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    bill = module.typed(source, word); oldbill = module.typed(source, parent)
    need(bill.pop('final_locations') == oldbill.pop('final_locations'), 'all final source charts unchanged')
    delta = {k: bill['opcode_counts'].get(k, 0)-oldbill['opcode_counts'].get(k, 0) for k in bill['opcode_counts'].keys() | oldbill['opcode_counts'].keys()}
    need({k:v for k,v in delta.items() if v} == {'ADD':16,'SCALE':-8,'MOVE':8,'INIT':8,'CLEAR':8}, 'full ordinary delta '+str(delta))
    need(bill['raw_histogram'] == oldbill['raw_histogram'], 'all raw source routes unchanged')
    T = {int(r): c for r,c in receipt['conditional_caller']['T4'].items()}
    P = {int(r): c for r,c in receipt['conditional_caller']['P_partial'].items()}
    P[1] = P.get(1,0)+18*8
    lo,hi = module.interval({r:T.get(r,0)-P.get(r,0) for r in T.keys() | P.keys()})
    xs = source['live']; roots = {x: root(source['frames'][source['initial'][x]][0]) for x in xs}
    H = {}
    for x in xs:
        c = F(1,2) if x in COUPLED else F(1)
        row = {d: c*F(sum(a*b for a,b in zip(roots[x],roots[d])),8) for d in xs}
        row[x] -= c
        for d,a in parent['corrections'].get(str(x+112), []): row[d] += F(a)
        H[x] = {d:a for d,a in row.items() if a}
    before = sum(map(len,H.values())); expanded = before+sum(sum(d in COUPLED for d in row) for row in H.values())
    need(before == receipt['forward_residual_coefficients'] == 4601, 'inherited exact residual matrix')
    # Independent-input preconditioner determinant is 2 per coupled pair.
    for x,y in [(F(a),F(b)) for a in range(-3,4) for b in range(-3,4)]:
        xp,yp=x-y,2*y
        need((xp+yp/2,yp/2)==(x,y), 'precondition inverse')
        need((xp,(xp+yp)/2)==(x-y,(x+y)/2), 'coupled target identity')
    negative = {}
    # These finite mutants test the exact source constructor, not the universal proof.
    mutations = {'wrong_sign': lambda w: w['program'][443].__setitem__(3,'1'),
                 'wrong_initial_target': lambda w: w['program'][402].__setitem__(3,source['initial'][19]),
                 'missing_preload_motion': lambda w: w['program'][402].__setitem__(3,3)}
    # first 8 preloads start at400. The last ADD is438, not443; bind by provenance.
    mutations['wrong_sign'] = lambda w: w['program'][403].__setitem__(3,'1')
    for name, mutate in mutations.items():
        bad=deepcopy(word); mutate(bad)
        try:
            badrows,badloc=prefix(bad,source)
            need(badloc==oldloc and all(badrows[r]==substitution(oldrows[r],raw) for r in oldrows), 'bad precomposition')
        except ValueError:
            negative[name]=True
        else: raise ValueError('mutant survived '+name)
    bad=deepcopy(word)
    # Reinstating a removed half-scale halves an original Y mode incorrectly.
    at=bad['marks']['all_preconditioned_donors_restored']
    bad['program'].insert(at,['SCALE',raw[129],'1/2',3]); bad['marks']['common_starts']+=1
    try:
        badrows,badloc=prefix(bad,source)
        need(all(badrows[r]==substitution(oldrows[r],raw) for r in oldrows),'retained half-scale')
    except ValueError: negative['unremoved_half_scale']=True
    else: raise ValueError('half-scale mutant survived')
    payload=json.dumps(word,sort_keys=True,separators=(',',':')).encode(); blob=gzip.compress(payload,mtime=0,compresslevel=9)
    (out/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_PRETERMINAL_EIGHT_COUPLED_SOURCE_COMPOSITION','source_sha256':SOURCE,'parent_word_sha256':PARENT,'parent_payload_sha256':PARENT_PAYLOAD,'parent_receipt_sha256':sha(rp.read_bytes()),'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'independent_input_columns':1880,'coupled_reverse_endpoints_completed':list(COUPLED),'preserved_completed_firstY_receivers':parent['newly_completed_firstY_receivers'],'full_prefix_precomposition_rows':len(rows),'literal_common_suffix_unchanged':True,'bill':bill,'ordinary_increment':delta,'new_paid_move_histogram':{'1':8},'all_raw_routes_unchanged':True,'input_precondition_determinant':'256','input_precondition_inverse':'y=y_tilde/2; x=x_tilde+y_tilde/2','forward_residual_count_in_preconditioned_donor_basis':before,'forward_residual_count_in_original_difference_basis':expanded,'forward_residual_formula':'H*(qX-D_U*qY_U); H exactly inherited from parent','remaining_hosted_reverse_residual_rank':96,'conditional_caller':{'T4':T,'P_partial':P,'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T.get(r,0)-P.get(r,0)) for r in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18),'remaining_moment_per_native_decimal':float(lo/18),'new_paid_calls_over_parent_per_native':8},'negative_controls':negative,'status_scope':'Proved finite source precomposition and exact algebra. Eight coupled reverse duties now complete; forward code remains partial, all96 hosted reverse diagonals remain, no complete supplier or new kappa. Unbounded chart/erasure/compiler/precision/source/analytic contracts retained.'}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['status','word_payload_sha256','ordinary_increment','forward_residual_count_in_original_difference_basis','conditional_caller']},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
