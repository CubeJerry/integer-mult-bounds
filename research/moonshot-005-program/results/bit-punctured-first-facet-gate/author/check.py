#!/usr/bin/env python3
"""Independent all-column/rational-chart review. No author checker imports."""
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

FRAME = [1,8,9,30,37,46,73,77]

def punctured_star(roots, deleted=(0,)):
    keep = [i for i in range(111) if i not in deleted]
    need(all(i in keep for i in FRAME), 'star point frame meets deleted roles')
    need(all(dot(roots[i],roots[j]) != 0 for i in FRAME for j in FRAME), 'point frame has a forbidden orthogonal pair')
    edges = {}
    for role in keep:
        if role in FRAME:
            continue
        pair = tuple(p for p,i in enumerate(FRAME) if dot(roots[i],roots[role]) == 0)
        if len(pair) == 2:
            need(pair not in edges, 'duplicate edge role in this certificate')
            edges[pair] = role
    need(len(edges) == 27, 'punctured star edge count')
    need(set(edges) == {(a,b) for a in range(8) for b in range(a+1,8)}-{(0,2)}, 'punctured star is not the stated K8 minus one edge')
    degrees = [sum(i in p for p in edges) for i in range(8)]
    need(min(degrees) >= 4, 'star inequality degree premise')
    comparisons = []
    for p,j in edges.items():
        need([t for t,i in enumerate(FRAME) if dot(roots[i],roots[j]) == 0] == list(p), 'edge-point zero mask mismatch')
        for q,k in edges.items():
            if p < q and set(p)&set(q):
                inner = dot(roots[j],roots[k])
                need(inner != 0, 'incident edge roles are actually orthogonal')
                comparisons.append({'edge_roles':[j,k],'inner_product':inner})
    K = [sum(1 << j for j,r in enumerate(roots) if i==j or dot(roots[i],r)==0) for i in range(111)]
    mask = sum(1 << j for j in keep)
    need(len(binary_basis([K[i]&mask for i in keep])) == 9, 'canonical punctured attainment rank')
    return {'deleted_roles':list(deleted),'point_roles':FRAME,'edges':[{'point_indices':list(p),'role':j} for p,j in sorted(edges.items())],
        'degrees':degrees,'incident_edge_checks':comparisons,'punctured_canonical_rank':9,
        'all_field_lower_bound':'rank >= 9V for every field and every positive integer V',
        'characteristic_two_attainment':'exact minimum 9V'}

def dual_counterinput(rows, target, allowed):
    equations = [(row&allowed,0) for row in rows]+[(target,1)]
    B = {}
    for row,rhs in equations:
        while row:
            p = row.bit_length()-1
            if p in B:
                old,b = B[p]; row ^= old; rhs ^= b
            else:
                B[p] = (row,rhs); break
        if not row:
            need(not rhs,'requested separating dual does not exist')
    vector = 0
    for p,(row,rhs) in sorted(B.items()):
        if (row&vector).bit_count()%2 != rhs:
            vector |= 1 << p
    need(vector & ~allowed == 0 and (target&vector).bit_count()%2 == 1,'dual own coordinate or support')
    need(all((row&vector).bit_count()%2 == 0 for row in rows),'dual does not annihilate observations')
    return vector

def literal_histories(word):
    values = {f'X{i}':1<<i for i in range(111)} | {f'Y{i}':1<<(111+i) for i in range(111)}
    places = {f'X{i}':f'L{i}' for i in range(111)} | {f'Y{i}':'zero' for i in range(111)}
    snapshots, pre_feedback, entries = [], [], {}
    packets = {f'P{q}' for q in range(8)}
    for step,op in enumerate(word['operations']):
        kind,name,*rest = op; changed = None
        if op == ['ADD','P0','Y0']:
            pre_feedback.append({'operation_index':step,'chart':places['P0'],'P0_row_hex':hex(values['P0']),'Y0_row_hex':hex(values['Y0']),
                'packet_entry':entries[('P0',places['P0'])]})
        if kind == 'INIT':
            values[name],places[name] = 0,rest[0]
        elif kind == 'ADD':
            values[rest[0]] ^= values[name]
            changed = rest[0] if rest[0] in packets else None
        elif kind == 'MOVE':
            places[name] = rest[0]
            changed = name if name in packets else None
            if changed is not None:
                entries[(name,rest[0])] = {'operation_index':step,'row_hex':hex(values[name])}
        elif kind == 'CLEAR':
            del values[name],places[name]
        else:
            raise ValueError('unknown operation')
        if changed is not None and places[changed] != 'Hub':
            snapshots.append({'operation_index':step,'packet':changed,'chart':places[changed],'row_hex':hex(values[changed])})
    return snapshots,pre_feedback

def frozen_access(word,roots):
    histories,exchange = literal_histories(word)
    bases = {name:chart_basis(c) for name,c in word['charts'].items()}
    compatible = {i:{name for name,b in bases.items() if all(dot(v,roots[i])==0 for v in b)} for i in range(111)}
    terminal = [word['expected'][f'P{q}'][1] for q in range(8)]
    need(all(v>>111 == 0 for v in terminal),'terminal y contamination')
    need(len(binary_basis(terminal)) == 8,'terminal dimension')
    rows,failures,positive = [],[],[]
    congruences = 0
    for i in range(111):
        mask = sum(1 << j for j,r in enumerate(roots) if dot(roots[i],r))
        observed = [s for s in histories if s['chart'] in compatible[i]]
        for item in observed:
            row = int(item['row_hex'],16); q = int(item['packet'][1:])
            if i != 0:
                need((row^terminal[q])&mask == 0,'nonlocal terminal congruence fails away from F0')
                congruences += 1
        projected = [row&mask for row in terminal]
        history_projected = [int(item['row_hex'],16)&mask for item in observed]
        terminal_fit = solve(binary_basis(projected),1 << i) is not None
        full_fit = solve(binary_basis(projected+history_projected),1 << i) is not None
        if i != 0:
            need(len(binary_basis(projected+history_projected)) == len(binary_basis(projected)),'accessible history adds a nonlocal mode')
            need(terminal_fit == full_fit,'nonterminal information changes fitting outside F0')
        record = {'receiver':i,'compatible_history_count':len(observed),'terminal_projected_rank':len(binary_basis(projected)),
            'full_projected_rank':len(binary_basis(projected+history_projected)),'terminal_fits':terminal_fit,'full_fits':full_fit}
        if i != 0 and not terminal_fit:
            dual = dual_counterinput(terminal,1 << i,mask)
            need(all((int(s['row_hex'],16)&dual).bit_count()%2==0 for s in observed),'dual misses an actual compatible history')
            record['dual_input_hex'] = hex(dual);failures.append(i)
        if terminal_fit:
            positive.append(i)
        rows.append(record)
    need(rows[0]['full_fits'] and not rows[0]['terminal_fits'],'actual Y0 is not a positive control for exceptional facet')
    need(len(failures) == 99 and len(positive) == 11,'frozen fitting census changed')
    need(exchange and exchange[0]['chart']=='F0','frozen feedback is not at first facet')
    return {'terminal_rows_hex':[hex(v)for v in terminal],'receiver_records':rows,'terminal_fitting_roles':positive,
        'excluded_receiver_roles':failures,'exact_terminal_congruences_checked':congruences,'exchange':exchange,
        'scope':'All actual source observations in each receiver downset, every terminal, free local X coordinates and arbitrary y symbols are granted. No new feedback or changed source state is granted.'}

def main():
    parser = argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--word',type=Path,required=True);parser.add_argument('--deep-word',type=Path)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    raw = (args.repo/ROOT_PATH).read_bytes();need(hashlib.sha256(raw).hexdigest()==ROOT_SHA256,'native source changed')
    roots = json.loads(raw)['native_roots'];roots = [roots[str(i)]for i in range(111)]if isinstance(roots,dict)else roots
    wb = args.word.read_bytes();word=json.loads(wb)
    need(hashlib.sha256(wb).hexdigest()=='2586e9eb28e25b241305d4237ffd59914cd2a7ed30bd2aacc193d45107b6e8ac','frozen source word changed')
    star = punctured_star(roots);access=frozen_access(word,roots)
    controls = {}
    try:punctured_star(roots,(0,1))
    except ValueError as e:controls['delete_a_point_in_the_displayed_star']={'rejected':True,'reason':str(e)}
    else:raise ValueError('invalid punctured star was accepted')
    bad=copy.deepcopy(word);bad['expected']['P0'][1]^=1
    try:frozen_access(bad,roots)
    except ValueError as e:controls['claim_kernel_point_is_a_terminal']={'rejected':True,'reason':str(e)}
    else:raise ValueError('wrong terminal was accepted')
    need(access['receiver_records'][0]['full_fits'] and not access['receiver_records'][0]['terminal_fits'],'exceptional-facet control')
    controls['extend_terminal_congruence_to_exceptional_facet']={'rejected':True,'reason':'Receiver0 full projected space fits; terminal projected space does not.'}
    result={'status':'PASS_PUNCTURED_NINE_AND_FIRST_FACET_LOCALITY','native_sha256':ROOT_SHA256,'word_sha256':hashlib.sha256(wb).hexdigest(),
        'punctured_star':star,'frozen_access':access,'negative_controls':controls,'new_complete_kappa':False}
    if args.deep_word:
        db=args.deep_word.read_bytes();dw=json.loads(db);_,pre=literal_histories(dw)
        need(len(pre)==1 and int(pre[0]['P0_row_hex'],16)==1,'deeper exploratory kernel is not x0')
        need(dw['feedback_chart']==pre[0]['chart'],'deep feedback chart metadata')
        local = int(pre[0]['packet_entry']['row_hex'],16)^1
        basis = chart_basis(dw['charts'][pre[0]['chart']])
        need(not(local>>111),'point-kernel local translation has public-y contamination')
        need(all(sp.Matrix(basis+(tuple(roots[j]),)).rank()==len(basis) for j in support(local)), 'entry differs from x0 by a nonlocal X form')
        result['deeper_point_kernel_control']={'word_sha256':hashlib.sha256(db).hexdigest(),'actual_pre_feedback':pre[0],
            'entry_minus_x0_local_row_hex':hex(local),'scope':'Exact entry/interior rows and chart-local translation only; not a complete independent source admission. After absorbing the local translation, its x-kernel disappears when column0 is deleted.'}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'star_edges':27,'star_degrees':star['degrees'],'frozen_excluded_receivers':len(access['excluded_receiver_roles']),
        'terminal_fit_roles':access['terminal_fitting_roles'],'congruences':access['exact_terminal_congruences_checked']},sort_keys=True))

if __name__ == '__main__':main()

