#!/usr/bin/env python3
"""Check the witness measure, every real native flat through rank four, and the prices."""
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
from fractions import Fraction as F
from pathlib import Path

PROGRAM = Path('research/moonshot-005-program')
WITNESS = PROGRAM / 'results/bit-induced95-nonlinear-witnesses/check.py'
WITNESS_SHA = 'dfc88d61e874ba0b0f92b1f2616bf0b4e4af88adb09ebe8fbfbce28918d5f13a'
ROOMS = PROGRAM / 'results/bit-low-exterior-formation-gate/author/output/RESULT.json'
ROOMS_SHA = 'befef29e616a3adebe070251a87c6f85c94a81bf687db2dceafdbbf067017145'
LAYERS = {2: F(1), 3: F(19, 20), 4: F(3, 5), 5: F(1)}


def require(test, message):
    if not test:
        raise ValueError(message)


def checked_bytes(path, digest):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, f'dependency changed: {path}')
    return raw


def census(repo):
    path = repo / WITNESS
    checked_bytes(path, WITNESS_SHA)
    spec = importlib.util.spec_from_file_location('induced95', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    roots = json.loads(checked_bytes(repo / module.ROOT_TABLE, module.ROOT_SHA))['native_roots']
    roles, witnesses, _, _ = module.enumerate_witnesses(roots)
    ids = {role: i for i, role in enumerate(roles)}
    weights = {int(k): v for k, v in json.loads(Path(__file__).with_name('WEIGHTS.json').read_text()).items()}
    require(len(weights) == 102 and sum(weights.values()) == 999993, 'witness measure')
    require(all(0 <= k < len(witnesses) and type(v) is int and v > 0 for k, v in weights.items()), 'positive integer weights')
    rows = [roots[i] for i in roles]
    for k, witness in enumerate(witnesses):
        group = witness['isolates'] + witness['petersen']
        rows.append([weights.get(k, 0), *(ids[i] for i in group)])
    data = ''.join(' '.join(map(str, row)) + '\n' for row in rows)
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / 'census'
        subprocess.run([os.environ.get('CXX', 'c++'), '-O3', '-std=c++20', str(Path(__file__).with_name('coverage.cpp')), '-o', str(exe)], check=True)
        result = subprocess.run([str(exe)], input=data, text=True, capture_output=True, check=True)
    counts, widths, masses, axes = [], [], [], []
    for r, line in enumerate(result.stdout.splitlines()):
        rank, count, width, mass, *axis = map(int, line.split())
        require(rank == r and len(axis) == 8, 'flat output')
        counts.append(count)
        widths.append(width)
        masses.append(mass)
        axes.append(axis)
    require(counts == [1, 95, 3399, 55561, 420639], 'complete real flat census')
    require(widths == [0, 1, 3, 6, 12] and axes[-1] == [11] * 8, 'native occupancy')
    require(masses == [0, 191805, 387630, 610722, 827177], 'attained incidence maxima')
    return {'witnesses': len(witnesses), 'positive_weights': len(weights), 'total_weight': sum(weights.values()),
            'real_native_flats': counts, 'max_native_roles': widths, 'max_native_roles_on_each_axis': axes,
            'max_hit_weight': masses, 'integral_geometry_input_sha256': hashlib.sha256(data.encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    result = census(args.repo)
    alpha = [F(m, result['total_weight']) for m in result['max_hit_weight']]
    downward = {(s, d): sum(w for r, w in LAYERS.items() if d <= r < s) for s in range(1, 9) for d in range(s)}
    require(all(load ** 200 <= (s - d) ** 199 for (s, d), load in downward.items()), 'downward charge')
    inlet = {(a, s): alpha[a] * sum(w for r, w in LAYERS.items() if s <= r) for s in range(1, 6) for a in range(s)}
    require(max(inlet.values()) < 1, 'all positive-gap inlets funded')
    eq_bill = 9 * sum(LAYERS.values())
    rooms = json.loads(checked_bytes(args.repo / ROOMS, ROOMS_SHA))['sources']
    margins = []
    for entry in rooms:
        lo, hi = map(F, entry['normalized_room']['rational'])
        margins.append([entry['copies'], str(eq_bill - hi), str(eq_bill - lo)])
    require(F(margins[0][1]) > 0 and all(F(row[2]) < 0 for row in margins[1:]), 'scope of equality exclusion')
    coef = (1 + alpha[4]) / 2
    unit_charges = [alpha[1], alpha[2], alpha[3], coef, coef, alpha[3], alpha[2], alpha[1]]
    require(all(x <= coef for x in unit_charges) and (1 / coef) ** 200 <= 2 ** 199, 'arbitrary-transcript dual')
    floors = []
    for b in range(1, 4):
        min_total_gap = -(-9 * b // coef)
        require((min_total_gap - 1) * coef < 9 * b <= min_total_gap * coef, 'integer gap')
        floors.append({'copies': b, 'nonprivate_integer_gap_floor': min_total_gap,
                       'movement_floor_expression': f'{8*b}+{min_total_gap}*8^(-1/200)'})
    require([row['nonprivate_integer_gap_floor'] for row in floors] == [10, 20, 30], 'physical gaps')
    result.update(layer_weights={str(r): str(w) for r, w in LAYERS.items()}, downward_pairs=len(downward),
                  owned_or_public_inlet_pairs=len(inlet), max_weighted_inlet_charge=str(max(inlet.values())),
                  equality_lower_bill_per_copy=str(eq_bill), equality_margins_vs_normalized_room=margins,
                  arbitrary_transcript_unit_cut_bounds=list(map(str, unit_charges)),
                  arbitrary_transcript_max_cost_coefficient=str(coef), arbitrary_transcript_per_copy_floor=str(8 + 9 / coef),
                  arbitrary_transcript_integral_bounds=floors)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(f'838 witnesses, 102 positive weights, equality cost {eq_bill}, unrestricted cost {8 + 9 / coef} per copy')


if __name__ == '__main__':
    main()
