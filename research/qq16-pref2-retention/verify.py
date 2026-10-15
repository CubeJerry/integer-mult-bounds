#!/usr/bin/env python3
"""Read-only replay of one QQ16 final-record retention repair (stdlib Python).

@CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json
import sys
import tarfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from algebra import (add, adapter_word, basis_banks, decode, decoder_program, expected_selected, eye, factor_word,
                     linear, models, mul, need, observe, operate, ordered_identity,
                     run_decoder_program, run_word, simulate, symbol)

PACKAGE = Path(__file__).resolve().parent
ARCHIVE = 'research/community-frontier1042-audit/selected-replay.tar.gz'
MEMBER = 't16/global/base/split-centres/GLOBAL-TEMPLATE.json.gz'
MEMBER_HASH = 'a179dad87651aba340a5a8ddbcd86a8e757cad87b8a1f8bad48106fbecd38518'
PACKET = 'research/joint-query/certificate.json.gz'
A = [0, 7, 20, 27, 36, 46, 57, 111]
T = [21, 37, 47, 76, 81, 87, 92, 110]


def canonical(data):
    return json.dumps(data, sort_keys=True, indent=2) + '\n'


def source_data(root):
    pins = json.loads((PACKAGE / 'SOURCES.json').read_text())
    hashes = {}
    for item in pins['files']:
        if item['usage'] != 'input':
            continue
        path = item['path']
        actual = sha256((root / path).read_bytes()).hexdigest()
        need(actual == item['sha256'], 'source hash: ' + path)
        hashes[path] = actual
    packet = json.loads(gzip.decompress((root / PACKET).read_bytes()))
    need(packet['A_ports'] == A and packet['T_ports'] == T, 'selected ports')
    with tarfile.open(root / ARCHIVE) as archive:
        matches = [m for m in archive.getmembers() if m.name == MEMBER]
        need(len(matches) == 1 and matches[0].isfile(), 'unique regular recipe member')
        raw = archive.extractfile(matches[0]).read()
    need(sha256(raw).hexdigest() == MEMBER_HASH, 'recipe member hash')
    recipe = json.loads(gzip.decompress(raw))['recipe']
    need(len(recipe) == 19, '19 retained events')
    locals_ = [r for r in recipe if r['kind'] == 'local']
    need([r['stage'] for r in locals_] == list(range(9)), 'stage order')
    need([r['pair'] for r in locals_] == [0, 0, 0, 1, 1, 2, 2, 3, 3], 'actual bank sequence')
    need([r['reverse'] for r in locals_] == [bool(s % 2) for s in range(9)], 'orientations')
    return packet, recipe, hashes


def tail_identity(recipe):
    x = [symbol('x' + str(i)) for i in range(4)]
    y = [symbol('y' + str(i)) for i in range(4)]
    cut = None
    for event in recipe:
        if event['kind'] == 'local':
            k, s = event['pair'], event['stage']
            if event['reverse']:
                x[k] = linear((1, x[k]), (-1, y[k]))
                y[k] = linear((1, y[k]), (1, operate('K'+str(s), symbol('a'+str(s)))))
            else:
                x[k] = linear((1, x[k]), (-1, operate('K'+str(s), symbol('f'+str(s)))))
                y[k] = linear((1, y[k]), (1, x[k]))
            if s == 1:
                cut = x[0]
        elif event['kind'] == 'bridge':
            i, j, c = event['src'], event['dst'], event['coefficient']
            x[j] = linear((1, x[j]), (c, x[i]))
            y[i] = linear((1, y[i]), (-c, y[j]))
        else:
            need(event['kind'] == 'terminal', 'tail event')
            x, y = y, [linear((-1, expr)) for expr in x]
    need(cut == linear((-1, symbol('y0'))), 'post-B1 ordinary cancellation')
    wanted = linear((1, symbol('y0')), (1, operate('K2', symbol('f2'))))
    need(y[0] == wanted, 'completed-X ordinary tail')
    return {'events': len(recipe), 'completed_X_is_final_Y': True,
            'identity': 'C = initial Y_0,U + K_2 f_2'}


def transpose(a):
    return [list(row) for row in zip(*a)]


def actual_sections(packet):
    r = [[Q(row.get(str(p), '0')) for p in range(112)] for row in packet['R_rows']]
    u = [p for p in range(112) if p not in A + T]
    need(packet['U_ports'] == u, 'ordinary partition')
    ra, rt, ru = [[[row[p] for p in ports] for row in r] for ports in (A, T, u)]
    need(mul(ra, transpose(ra)) == mul(rt, transpose(rt)) == add((4, eye(8))), 'actual selected Grams')
    need(mul(ru, transpose(ru)) == add((48, eye(8))), 'actual ordinary Gram')
    return {'LA': ra, 'LT': rt, 'PA': add((Q(1, 4), transpose(ra))),
            'PT': add((Q(1, 4), transpose(rt)))}


def adapter_checks(maps):
    q = len(maps['PA'])
    full = eye(5*q)
    rows = [full[i*q:(i+1)*q] for i in range(5)]
    h, j = mul(maps['PA'], maps['LT']), mul(maps['PT'], maps['LA'])
    need(mul(h, j) == mul(j, h) == eye(q), 'two-sided chart transport')
    a, t, ya, yt, dirty = rows
    expected = [mul(h, t), add((-1, mul(j, a))),
                add((1, ya), (1, a), (-1, mul(h, t))),
                add((1, yt), (1, t), (1, mul(j, a))), dirty]
    word = factor_word()
    actual = run_word(rows, word, maps)
    need(actual == expected, '24-child echo: every arbitrary input column')
    undo = [(op, target, source, -sign) for op, target, source, sign in reversed(word)]
    need(run_word(actual, undo, maps) == rows, 'literal reverse restores all five blocks')
    need(run_word(run_word(rows, undo, maps), word, maps) == rows, 'second inverse order')
    direct = run_word(rows, adapter_word(), {'H': h, 'J': j})
    need(direct == actual, 'compound and leaf representations agree')
    rejected = []
    for index in range(len(word)):
        broken = word[:index] + word[index+1:]
        need(run_word(rows, broken, maps) != expected, 'omitted child ' + str(index))
        rejected.append(index)
    costs = dict(sorted(Counter(op for op, *_ in word).items()))
    need(costs == {'LA': 4, 'LT': 8, 'PA': 8, 'PT': 4}, 'all recursive children billed')
    return {'basis_columns': 5*q, 'compound_adds': 6, 'complete_child_calls': len(word),
            'child_counts': costs, 'borrowed_query_blocks': 1,
            'inverse_orders': 2, 'omitted_child_controls': len(rejected),
            'H_nonzeros': sum(bool(v) for row in h for v in row)}


def model_checks(recipe):
    records, controls = [], []
    for q in (1, 2, 3):
        charts = models(q)
        initial, final, histories, cut = simulate(charts, recipe)
        wanted = expected_selected(initial)
        observations = observe(charts, initial, final, histories)
        need(decode(charts, observations) == wanted, 'all four selected input blocks')
        output, scratch, extra = run_decoder_program(charts, observations)
        padded = [[row + [Q(0)] * extra for row in block] for block in wanted]
        need(output == padded and not any(v for block in scratch for row in block for v in row),
             'literal decoder, all owned dirt discarded and scratch zeroed')
        need(add((-1, mul(charts[2]['LT'], observations['YT']))) == histories[2], 'f2 reconstruction')
        need(final[0][1][1] == cut[0][1], 'native-name final Y_A retains B1 X_A')
        need(add((1, final[0][0][1]), (-2, final[0][1][1])) == cut[1][1], 'recovered B1 Y_A')
        records.append({'query_dimension': q, 'ordinary_dimension': 3*q,
                        'all_bank_basis_columns': 40*q, 'selected_blocks_recovered': 4})
        if q == 2:
            program = decoder_program()
            for index in range(len(program)):
                out, work, _ = run_decoder_program(charts, observations, program[:index]+program[index+1:])
                need(out != padded or any(v for block in work for row in block for v in row),
                     'decoder event omission ' + str(index))
            for fault in ('omit_q0', 'omit_q2', 'omit_f2', 'terminal_sign', 'f2_terminal_sign'):
                need(decode(charts, observations, fault) != wanted, 'decoder control ' + fault)
                controls.append(fault)
            wrong_observations = dict(observations, C=final[0][0][0])
            need(decode(charts, wrong_observations) != wanted, 'former Y is not completed X')
            controls.append('former_y_endpoint')
            for fault in ('omit_adapter', 'wrong_middle_sign', 'missing_y_correction', 'wrong_chart'):
                init2, end2, hist2, _ = simulate(charts, recipe, fault)
                need(decode(charts, observe(charts, init2, end2, hist2)) != wanted, 'adapter control ' + fault)
                controls.append(fault)
    wrong = deepcopy(recipe)
    wrong[3]['pair'] = 1
    try:
        tail_identity(wrong)
    except ValueError:
        controls.append('wrong_F2_bank')
    else:
        raise ValueError('wrong F2 bank accepted')
    wrong = deepcopy(recipe)
    wrong[4]['coefficient'] = 1
    try:
        tail_identity(wrong)
    except ValueError:
        controls.append('wrong_bridge_sign')
    else:
        raise ValueError('wrong bridge sign accepted')
    counts = Counter(event[3] for event in decoder_program() if event[0] == 'add')
    return {'models': records, 'total_basis_columns': sum(r['all_bank_basis_columns'] for r in records),
            'rejected_controls': controls, 'decoder_event_omission_controls': 35,
            'literal_decoder': {'events': 35, 'clear_calls': 13, 'add_calls': dict(sorted(counts.items())),
                                'actual_owned_scratch_coordinates': 112,
                                'actual_owned_output_coordinates': 32,
                                'three_model_owned_dirt_columns': 54}}


def old_loss_fixture(recipe):
    """Concrete rational instance of PR2346's displayed two-bank trajectory.

    This is a regression, not a finite model of the actual regular owner cover.
    """
    charts = []
    for coordinate in (0, 1, 2, 0, 1, 0, 1, 0, 1):
        b = [[Q(j == coordinate) for j in range(3)]]
        charts.append(dict(B=b, K=add((12, transpose(b))), LA=eye(1), LT=eye(1),
                           PA=eye(1), PT=eye(1)))
    v = [[Q(0)] for _ in range(40)]
    for index, value in {1: 1, 3: -1, 4: 1, 8: 1, 9: -1, 12: -1}.items():
        v[index][0] = Q(value)
    _, old, old_f, _ = simulate(charts, recipe, 'omit_adapter')
    _, new, new_f, _ = simulate(charts, recipe)
    observed = []
    for x, y in old:
        observed += [x[1], x[2], y[1], y[2], y[0]]
    observed += list(old_f.values())
    need(all(not any(row[0] for row in mul(block, v)) for block in observed),
         'old final-only observation really loses the fixture')
    initial = basis_banks(1)
    for bank, stages in enumerate(((0, 2), (3, 4), (5, 6), (7, 8))):
        for stage in stages:
            need(mul(charts[stage]['B'], mul(initial[bank][0][0], v)) == [[0]],
                 'all old initial records vanish')
    retained = mul(new[0][1][1], v)
    need(retained == [[1]] and mul(new_f[2], v) == [[-2]], 'new intervention detects old fixture')
    return {'old_all_initial_and_final_observations_zero': True,
            'original_X0_A': '-1', 'new_final_Y0_A': '1', 'new_f2': '-2',
            'scope': 'rational identity fixture, not an actual-cover witness enumeration'}


def replay(root):
    packet, recipe, hashes = source_data(root)
    return {'status': 'PASS_QQ16_PREF2_RETENTION', 'no_new_kappa': True,
            'scope': 'Pair-0 logical final-record decoder; native realization and favorable supplier bill unproved.',
            'source_sha256': hashes, 'recipe_member_sha256': MEMBER_HASH,
            'tail': tail_identity(recipe), 'ordered': ordered_identity(),
            'actual_minor_adapter': adapter_checks(actual_sections(packet)),
            'observations': ['initial B0 X0U', 'initial B2 X0U', 'f0',
                             'final X0A', 'final X0T', 'final Y0A', 'final Y0T', 'final Y0U'],
            'rational_models': model_checks(recipe), 'old_loss_fixture': old_loss_fixture(recipe)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=PACKAGE.parents[1])
    parser.add_argument('--write-result', type=Path)
    args = parser.parse_args()
    result = replay(args.repo.resolve())
    if args.write_result is not None:
        with args.write_result.open('x') as stream:
            stream.write(canonical(result))
    else:
        need(result == json.loads((PACKAGE / 'RESULT.json').read_text()), 'committed result differs')
    print('PASS_QQ16_PREF2_RETENTION pair=0 columns=240 adapter_children=24 controls=71 no_new_kappa')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('FAIL_QQ16_PREF2_RETENTION: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
