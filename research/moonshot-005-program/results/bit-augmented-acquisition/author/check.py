#!/usr/bin/env python3
"""Author all-column verifier, adapted from the earlier independent delayed-source checker."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import Counter
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import sympy as sp

ROOT_PATH = "research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json"
ROOT_SHA256 = "8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e"
DONORS = [16, 19, 38, 49, 50, 56, 57]
SCALE = 1 << 160

def need(test, why):
    if not test:
        raise ValueError(why)

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def binary_basis(rows):
    out = {}
    for j, value in enumerate(rows):
        tag = 1 << j
        while value:
            pivot = value.bit_length() - 1
            if pivot in out:
                value ^= out[pivot][0]
                tag ^= out[pivot][1]
            else:
                out[pivot] = (value, tag)
                break
    return out

def solve(basis, target):
    tag = 0
    while target:
        k = target.bit_length() - 1
        if k not in basis:
            return None
        target ^= basis[k][0]
        tag ^= basis[k][1]
    return tag

def combination(rows, tag):
    out = 0
    for j, row in enumerate(rows):
        if tag >> j & 1:
            out ^= row
    return out

def support(row, n=111):
    return [j for j in range(n) if row >> j & 1]

def chart_basis(chart):
    rows = chart["rows"]
    need(all(len(row) == 8 for row in rows), "chart ambient dimension is not eight")
    need(chart["kind"] in ("ann", "span"), "unknown chart kind")
    M = sp.Matrix(rows) if rows else sp.zeros(0, 8)
    if chart["kind"] == "span":
        return tuple(tuple(x) for x in M.rowspace())
    return tuple(tuple(x) for x in M.nullspace())

def replay(word, roots):
    charts = {name: chart_basis(chart) for name, chart in word['charts'].items()}
    dims = {name: len(basis) for name, basis in charts.items()}
    @lru_cache(None)
    def contained(a, b):
        joined = charts[a] + charts[b]
        return (sp.Matrix(joined).rank() if joined else 0) == dims[b]
    need(dims['Hub'] == 8 and dims['zero'] == 0, 'extreme chart dimensions')
    for j, root in enumerate(roots):
        need(chart_basis({'kind':'span', 'rows':[root]}) == charts[f'L{j}'], 'native input line changed')
        need(chart_basis({'kind':'ann', 'rows':[root]}) == charts[f'F{j}'], 'native output facet changed')
    need(word['order'] == list(range(8)), 'review is scoped to native first-eight cyclic queries')
    need(roots[:8] == [[2 * int(i == j) for j in range(8)] for i in range(8)], 'actual orthogonal axis frame')
    K = [sum(1 << j for j, root in enumerate(roots) if i == j or dot(roots[i], root) == 0) for i in range(111)]
    hm = K[0] ^ K[4]
    h = [hm >> i & 1 for i in range(111)]
    W = [row & (hm if h[i] else ((1 << 111)-1) ^ hm) for i, row in enumerate(K)]
    need(word['h_coordinates'] == 9 and int(word['W_pivot_h_hex'], 16) == hm, 'pivot is not h9')
    need(word['W_rows_hex'] == [hex(row) for row in W], 'actual fitting rows changed')
    need(len(binary_basis(K)) == 9 and len(binary_basis(W)) == 15, 'native code ranks')
    need(len(binary_basis(K+W)) == 16, 'native canonical extension rank')
    values = {f'X{j}':1 << j for j in range(111)} | {f'Y{j}':1 << (111+j) for j in range(111)}
    places = {f'X{j}':f'L{j}' for j in range(111)} | {f'Y{j}':'zero' for j in range(111)}
    packets = {f'P{q}' for q in range(8)}
    owned, born = set(), set()
    paths, seed_reads = {n:[] for n in packets}, {n:[] for n in packets}
    seed_rows, history, events, chart_visits, exchanges = {}, [], [], [], []
    counts, moves = Counter(), Counter()
    extra_captures = []
    peak = dirty = 0
    handoff = None
    completed = set(word['completed_targets'])
    need(completed == ({0} if word['coupled'] else set()), 'claimed outputs exceed scoped construction')
    def originals_restored():
        need(all(values[f'X{j}'] == 1 << j and places[f'X{j}'] == 'Hub' for j in range(111)), 'an original X is not restored at Hub')
    for index, op in enumerate(word['operations']):
        kind, name, *rest = op
        counts[kind] += 1
        changed = None
        if kind == 'INIT':
            need(name not in values and name not in born, 'duplicate or reborn owner')
            need(len(rest) == 1 and rest[0] in charts, 'invalid INIT')
            values[name], places[name] = 0, rest[0]
            owned.add(name); born.add(name); peak = max(peak, len(owned))
            if name in packets:
                originals_restored()
                need(rest[0] == 'Hub', 'packet not created at Hub')
                paths[name].append(8)
        elif kind == 'ADD':
            need(len(rest) == 1, 'ADD arity')
            target = rest[0]
            need(name in values and target in values and name != target, 'dead or self ADD')
            need(contained(places[name], places[target]) and contained(places[target], places[name]), 'noncochart ADD')
            if target in packets and places[target] == 'Hub':
                need(name.startswith('X') and name[1:].isdigit(), 'unaccounted seed source')
                originals_restored(); seed_reads[target].append(int(name[1:]))
            if target.startswith('EXTRA_'):
                need(name.startswith('X') and values[name] == 1 << int(name[1:]), 'new acquisition is not an actual pure original input')
                extra_captures.append({'operation_index':index,'source':name,'cache':target,'chart':places[name],'value_hex':hex(values[name])})
            values[target] ^= values[name]
            if target in packets:
                changed = target
            if (name, target) in [('P0','Y0'), ('Y0','P0')]:
                exchanges.append({'operation_index':index,'operation':op,'P0':hex(values['P0']),'Y0':hex(values['Y0']),'chart':places['P0']})
        elif kind == 'MOVE':
            need(len(rest) == 1 and name in values and rest[0] in charts, 'invalid MOVE')
            need(name not in owned or name in packets, 'an auxiliary owner moves')
            src, dest = places[name], rest[0]
            need(contained(dest, src) if name in owned else contained(src, dest), 'wrong-direction or incomparable MOVE')
            delta = abs(dims[src] - dims[dest])
            need(delta > 0, 'zero-rank MOVE')
            moves[delta] += 1
            if name in packets:
                if src == 'Hub':
                    need(name not in seed_rows, 'packet returned to Hub')
                    seed_rows[name] = values[name]
                paths[name].append(dims[dest]); changed = name
                if dims[dest] > 0:
                    chart_visits.append({'packet':name,'operation_index':index,'chart':dest,'dimension':dims[dest]})
            places[name] = dest
        elif kind == 'CLEAR':
            need(not rest and name in owned, 'CLEAR does not retire a live owner')
            dirty += bool(values[name]); owned.remove(name)
            del values[name], places[name]
        else:
            raise ValueError('unknown opcode '+kind)
        if changed is not None and places[changed] != 'Hub':
            history.append(values[changed])
            events.append({'operation_index':index,'packet':changed,'chart':places[changed],'row_hex':hex(values[changed])})
        if index+1 == word['handoff']:
            originals_restored()
            handoff = {n:[places[n], values[n]] for n in sorted(owned)}
            need(handoff == word['expected'], 'handoff owner chart/value mismatch')
    need(handoff is not None, 'handoff was not reached')
    originals_restored()
    for j in range(111):
        need(values[f'Y{j}'] == (1 << (111+j)) ^ ((1 << j) if j in completed else 0), 'wrong original Y endpoint')
        need(places[f'Y{j}'] == (f'F{j}' if word['closed'] or j in completed else 'zero'), 'wrong original Y chart')
    need(len(owned) == (0 if word['closed'] else len(born)), 'owner endpoint mismatch')
    need(paths == {name:list(range(8, -1, -1)) for name in packets}, 'cyclic packet path dimensions changed')
    need([seed_rows[f'P{q}'] for q in range(8)] == word['seeds'], 'seed metadata mismatch')
    need(all(seed_reads[n] == support(seed_rows[n]) for n in packets), 'seed source reads do not match actual seed')
    raw = {n:v[1] for n,v in handoff.items() if n.startswith('C')}
    need(len(raw) == 80 and all(raw.values()), 'actual nonzero colored raw cache count')
    need(all(not (v >> 111) and all(h[j] == int(n.split('_')[-1]) for j in support(v)) for n,v in raw.items()), 'cache mixes classes or public y inputs')
    extra = {n:v[1] for n,v in handoff.items() if n.startswith('EXTRA_')}
    need(extra == {'EXTRA_A0':sum(1<<i for i in [49,50,84,87,100,102]),'EXTRA_A1':sum(1<<i for i in [18,20,70,72])}, 'actual acquired rows changed')
    need(len(extra_captures)==10 and {int(x['source'][1:]) for x in extra_captures}=={18,20,49,50,70,72,84,87,100,102}, 'extra capture inventory')
    D = list(raw.values())+list(extra.values())
    need(len(binary_basis(D)) == 42, 'actual cache increment rank')
    need(solve(binary_basis(D),1) is not None, 'actual x0 point is not in increment space')
    need(42+15-len(binary_basis(D+W)) == 9, 'actual increment W intersection')
    need(word['increment_space_dimension'] == 42 and word['increment_W_intersection'] == 9, 'incorrect increment metadata')
    terminal = [handoff[f'P{q}'][1] for q in range(8)]
    need(all(not (v >> 111) for v in terminal), 'terminal public y contamination')
    spare=word['spare_packet_terminal_zero'];tr=7 if spare else 8
    need(len(binary_basis(terminal)) == tr, 'terminal rank')
    need(tr+15-len(binary_basis(terminal+W)) == tr-1, 'terminal W intersection')
    selected = [8,14,22,30,38,59,66]
    need(word['terminal_W_roles'] == ([None]+selected[:-1]+[None] if spare else [None]+selected), 'W-terminal metadata')
    need(terminal[1:] == ([W[i] for i in selected[:-1]]+[0] if spare else [W[i] for i in selected]), 'seven actual W terminals changed')
    need(len(binary_basis(D+terminal[1:])) == 48, 'seven actual terminal lifts do not complement increment space')
    raw0 = [0,0]
    for n,v in raw.items():
        if n.startswith('C0_'):
            raw0[int(n.split('_')[-1])] ^= v
    depth = word['delayed_feedback_depth']
    need(depth == 4 and word['delayed_feedback_chart'] == 'A15', 'reviewed depth-four delayed chart')
    prefix = 0
    class0_prefix = 0
    class0_suffix = 0
    class1_suffix = 0
    for name,row in raw.items():
        if name.startswith('C0_'):
            length,color = map(int,name.split('_')[1:])
            if length < depth:
                prefix ^= row
                if color == 0: class0_prefix ^= row
            elif color == 0:
                class0_suffix ^= row
            else:
                class1_suffix ^= row
    need(seed_rows['P0'] == 1 ^ raw0[0] ^ prefix ^ extra['EXTRA_A0'], 'P0 missing exact earlier-read compensation')
    need([hex(v) for v in raw0] == [word['raw_class_zero_query0_hex'], word['raw_class_one_query0_hex']], 'raw0 metadata changed')
    need(word['coupled'] and terminal[0] == class1_suffix, 'P0 delayed terminal formula')
    if word['coupled']:
        need(len(exchanges) == 2 and exchanges[0]['chart'] == exchanges[1]['chart'] == 'A15', 'delayed singular exchange chronology')
        need(int(exchanges[0]['P0'],16) == 1 ^ raw0[0], 'actual incoming kernel row')
        need(word['operations'][exchanges[0]['operation_index']-1] == ['MOVE','P0','A15'], 'kernel value is not the actual cell boundary')
        need(int(exchanges[0]['Y0'],16) == (1 << 111) ^ 1 ^ class0_prefix, 'delayed Y0 pending correction')
        need(int(exchanges[1]['P0'],16) == (1 << 111) ^ class0_suffix, 'actual delayed feedback packet value')
    else:
        need(not exchanges, 'unexpected coupling in control')
    B = binary_basis(history)
    witnesses = []
    for i,row in enumerate(W):
        tag = solve(B,row)
        need(tag is not None and combination(history,tag) == row, 'native W row absent from literal history')
        witnesses.append({'role':i,'W_row_hex':hex(row),'history_indices':support(tag,len(history))})
    cache_witnesses = []
    for name,row in (raw|extra).items():
        tag = solve(B,row)
        need(tag is not None and combination(history,tag) == row, 'an actual raw increment not in literal history')
        cache_witnesses.append({'cache':name,'row_hex':hex(row),'history_indices':support(tag,len(history))})
    covers = []
    for i in range(111):
        hit = next((v for v in chart_visits if contained(v['chart'],f'F{i}')),None)
        need(hit is not None, 'a receiver has no positive-dimensional actual packet chart')
        covers.append({'receiver':i,**hit})
    masks = [sum(1 << j for j,r in enumerate(roots) if dot(r,roots[i])) for i in range(111)]
    fitted = [i for i,m in enumerate(masks) if solve(binary_basis([r&m for r in terminal]),1 << i) is not None]
    y_rank = len(binary_basis([r >> 111 for r in history]))
    kernel = 1 ^ raw0[0]
    local_A = [1 << j for j,root in enumerate(roots) if all(dot(v,root)==0 for v in word['charts']['A15']['rows'])]
    need(solve(binary_basis(local_A+[1]),kernel) is None, 'delayed kernel collapses to point0 plus cell-local data')
    G = terminal+[kernel]
    cap = lambda A,B:len(binary_basis(A))+len(binary_basis(B))-len(binary_basis(A+B))
    kernel_receipt={'actual_kernel_hex':hex(kernel),'point0_plus_cell_local_rank':len(binary_basis(local_A+[1])),
        'point0_plus_cell_local_plus_kernel_rank':len(binary_basis(local_A+[1,kernel])),
        'normalized_code_rank':len(binary_basis(G)),'normalized_code_C_intersection':cap(G,K),
        'normalized_code_W_intersection':cap(G,W),'kernel_beyond_terminals':len(binary_basis(G))-tr,
        'punctured_terminal_rank':len(binary_basis([v & ~1 for v in terminal])),
        'punctured_normalized_code_rank':len(binary_basis([v & ~1 for v in G])),
        'class_zero_prefix_hex':hex(class0_prefix),'class_zero_suffix_hex':hex(class0_suffix),'class_one_suffix_hex':hex(class1_suffix),
        'scope':'A genuinely mixed one-width kernel; the existing complete target rank/arrival gate still excludes a sole width-V kernel.'}
    return {'status':'PASS_AUGMENTED_ACQUISITION_WORD','closed':word['closed'],'coupled':word['coupled'],
        'all_original_columns':222,'completed_targets':sorted(completed),'counts':dict(counts),'movement_profile':dict(sorted(moves.items())),
        'rank_length':sum(r*n for r,n in moves.items()),'owned_peak':peak,'live_owned':len(owned),'dirty_clears':dirty,
        'history_rank':len(B),'history_public_y_rank':y_rank,'history_pure_X_dimension':len(B)-y_rank,
        'history_W_intersection':15,'history_K_intersection':len(B)+9-len(binary_basis(history+K)),
        'extra_pure_captures':extra_captures,'actual_cache_increment_rank':42,'actual_cache_increment_W_intersection':9,'terminal_rank':tr,'terminal_W_intersection':tr-1,
        'terminal_fitted_roles_with_free_local_corrections':fitted,'terminal_W_roles':selected,'seed_source_reads':seed_reads,
        'packet_paths':paths,'exchanges':exchanges,'kernel_receipt':kernel_receipt,'new_complete_kappa':False,
        'evidence':{'history_events':events,'all111_W_witnesses':witnesses,'raw_increment_witnesses':cache_witnesses,'positive_chart_coverage':covers}}

def iroot(n, k):
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // pow(x, k - 1)) // k
        if y >= x:
            break
        x = y
    while pow(x, k) > n:
        x -= 1
    while pow(x + 1, k) <= n:
        x += 1
    return x

@lru_cache(None)
def power(rank):
    integer = pow(rank, 199) * pow(SCALE, 200)
    low = iroot(integer, 200)
    need(pow(low, 200) <= integer < pow(low + 1, 200), "directed power invariant")
    return F(low, SCALE), F(low if pow(low, 200) == integer else low + 1, SCALE)

def add(*terms):
    result = Counter()
    for coefficient, profile in terms:
        for rank, count in profile.items():
            result[rank] += coefficient * count
    return dict(result)

def moment(profile):
    low = high = F(0)
    for rank, coefficient in profile.items():
        left, right = power(rank)
        low += coefficient * (left if coefficient >= 0 else right)
        high += coefficient * (right if coefficient >= 0 else left)
    return low, high

def encode(interval):
    left, right = interval
    with localcontext() as ctx:
        ctx.prec = 60
        ctx.rounding = ROUND_FLOOR
        a = str(Decimal(left.numerator) / Decimal(left.denominator))
        ctx.rounding = ROUND_CEILING
        b = str(Decimal(right.numerator) / Decimal(right.denominator))
    return {"lower": a, "upper": b,
            "lower_fraction": str(left), "upper_fraction": str(right)}

def invoice(profile):
    N = {1: 1386, 2: 1253, 3: 62, 4: 47, 5: 9, 6: 104, 7: 10}
    H = {2: 1, 4: 25, 6: 1, 8: 410}
    P2 = add((36, N), (444, {1: 1}), (444, {7*j: 1 for j in range(1, 9)}))
    T2 = add((36, H), (222, {127: 1}), (444, {1+7*j: 1 for j in range(1, 10)}))
    allowance = add((1, N), (-1, H), (F(1, 36), T2), (F(-1, 36), P2))
    displayed = {127: F(37, 6), 64: F(74, 6), 1: F(-74, 6)}
    for j in range(1, 9):
        displayed[1+7*j] = displayed.get(1+7*j, F(0)) + F(74, 6)
        displayed[7*j] = displayed.get(7*j, F(0)) - F(74, 6)
    need({r: v for r, v in allowance.items() if v} == displayed, "caller allowance cancellation")
    rows = []
    first_positive = None
    for m in range(2, 202, 2):
        paid = add((F(m, 2), P2), (-18*(m-1), N), (18*(m-1), profile))
        target = add((F(m, 2), T2), (-18*(m-1), H))
        margin = moment(add((1, target), (-1, paid)))
        if first_positive is None and margin[0] > 0:
            first_positive = m
        if m in (2, 4, 6, 8, 10, 12):
            rows.append({"m": m, "target_minus_paid": encode(margin), "strictly_positive": margin[0] > 0})
    return {"exponent": "199/200", "directed_method": "binary fixed-point scale2^160 and exact integer200th root",
            "moment": encode(moment(profile)), "limiting_allowance": encode(moment(allowance)),
            "limiting_room": encode(moment(add((1, allowance), (-1, profile)))),
            "finite_even_m_checks": rows, "first_positive_even_m_in_2_to_200": first_positive,
            "scope": "movement-only necessary interface; all remaining supplier costs retained", "new_complete_kappa": False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--word',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);a=parser.parse_args()
    rb=(a.repo/ROOT_PATH).read_bytes();need(hashlib.sha256(rb).hexdigest()==ROOT_SHA256,'root source pin')
    roots=json.loads(rb)['native_roots'];roots=[roots[str(i)]for i in range(111)]if isinstance(roots,dict)else roots
    wb=a.word.read_bytes();word=json.loads(wb);receipt=replay(word,roots)
    a.out.mkdir(parents=True,exist_ok=True);evidence=receipt.pop('evidence');(a.out/'HISTORY.json').write_text(json.dumps(evidence,indent=2,sort_keys=True)+'\n')
    if word['closed']:
        receipt['invoice']=invoice(receipt['movement_profile'])
    result={'status':'PASS_AUTHOR_AUGMENTED_ACQUISITION_SOURCE','word_sha256':hashlib.sha256(wb).hexdigest(),'receipt':receipt,'negative_controls':{},'new_complete_kappa':False}
    mutants={
        'omit_extra0_deposit':['ADD','X49','EXTRA_A0'],
        'omit_extra1_deposit':['ADD','X18','EXTRA_A1'],
        'omit_extra0_packet_read':['ADD','EXTRA_A0','P0'],
        'omit_extra1_packet_read':['ADD','EXTRA_A1','P1'],
        'omit_later_correction':['ADD','C0_1_0','Y0'],
        'omit_preload_suffix':['ADD','C0_4_0','Y0'],
        'omit_actual_feedback':['ADD','Y0','P0'],
        'omit_y0_capture':['ADD','Y0','YM0'],
        'omit_y0_unmask':['ADD','YM0','P0'],
        'omit_class_one_suffix':['ADD','C0_4_1','P0'],
    }
    for label,op in mutants.items():
        bad=copy.deepcopy(word);i=bad['operations'].index(op);del bad['operations'][i]
        if i<bad['handoff']:bad['handoff']-=1
        try:replay(bad,roots)
        except(ValueError,KeyError)as e:result['negative_controls'][label]={'rejected':True,'reason':str(e)}
        else:raise ValueError('accepted delayed-source mutant '+label)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'counts':receipt['counts'],'kernel':receipt['kernel_receipt'],'mutants':len(result['negative_controls'])},sort_keys=True))

if __name__=='__main__':main()

