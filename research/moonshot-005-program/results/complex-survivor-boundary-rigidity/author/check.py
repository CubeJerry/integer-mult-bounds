#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Exact rational certificate for five-message boundary-bank rigidity.

This checks finite source identities. PROOF.md supplies the all-width operator
and arbitrary independent boundary-bijection implications.
"""
import argparse
import hashlib
import importlib.util
import json
import platform
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def clean(row):
    return {i: x for i, x in row.items() if x}


def exact_inverse(matrix):
    n = len(matrix)
    augmented = [list(row) + [Q(i == j) for j in range(n)]
                 for i, row in enumerate(matrix)]
    determinant = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if augmented[i][j]), None)
        require(pivot is not None, 'invertible finite component')
        if pivot != j:
            augmented[pivot], augmented[j] = augmented[j], augmented[pivot]
            determinant = -determinant
        coefficient = augmented[j][j]
        determinant *= coefficient
        augmented[j] = [x / coefficient for x in augmented[j]]
        for i in range(n):
            if i == j or not augmented[i][j]:
                continue
            coefficient = augmented[i][j]
            augmented[i] = [x - coefficient * y
                            for x, y in zip(augmented[i], augmented[j])]
    return determinant, [row[n:] for row in augmented]


def sparse_product(left, right):
    answer = []
    for row in left:
        result = defaultdict(Q)
        for k, coefficient in row.items():
            for j, other in right[k].items():
                result[j] += coefficient * other
        answer.append(clean(result))
    return answer


def strings(matrix):
    return [[str(x) for x in row] for row in matrix]


parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
package = Path(__file__).resolve().parent.parent
pins = json.loads((package / 'SOURCE-PINS.json').read_text())
for name, digest in pins['files'].items():
    require(hashlib.sha256((args.repo / name).read_bytes()).hexdigest() == digest,
            'source pin: ' + name)
inputs = args.repo / 'research/moonshot-005-program/results/complex-native-funded-donor-cuts/inputs'
spec = importlib.util.spec_from_file_location('s031_boundary_literal', inputs / '7833-construction.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)
original = source.load_word(inputs / 'DOUBLE-CANDIDATE.json.gz')
word = source.compensated(original, True)
original_rows = source.all_public_rows(original)
rows = source.all_public_rows(word)
ends = sorted(word.terminals)
n = len(word.inputs)
require(n == len(ends) == 1289, 'complete endpoint inventory')
require(set(word.inputs) == {~j for j in range(n)}, 'public input-axis encoding')
require(all(rows[e] == original_rows[e] for e in ends),
        'genuine paid fifth-channel control preserves all original terminal rows')
E = [{j: Q(x, denominator) for j, x in row.items()}
     for denominator, row in (rows[e] for e in ends)]

# Reconstruct the inverse from the complete exact target. The bipartite
# components are discovered from source support, not loaded from exploration.
adjacency = [set() for _ in range(2 * n)]
for i, row in enumerate(E):
    for j in row:
        adjacency[j].add(n + i)
        adjacency[n + i].add(j)
unseen = set(range(2 * n))
components = []
while unseen:
    start = min(unseen)
    reached, todo = {start}, [start]
    while todo:
        for neighbour in adjacency[todo.pop()] - reached:
            reached.add(neighbour)
            todo.append(neighbour)
    unseen -= reached
    axes = sorted(j for j in reached if j < n)
    outputs = sorted(j - n for j in reached if j >= n)
    require(len(axes) == len(outputs) and len(axes) in (1, 2),
            'nonempty square endpoint component of order at most two')
    components.append((axes, outputs))
require(Counter(len(a) for a, _ in components) == {1: 889, 2: 200},
        'complete target component census')
inverse = [{} for _ in range(n)]
for axes, outputs in components:
    _, local = exact_inverse([[E[i].get(j, Q(0)) for j in axes] for i in outputs])
    for j, coefficients in zip(axes, local):
        inverse[j] = {i: x for i, x in zip(outputs, coefficients) if x}
identity = [{j: Q(1)} for j in range(n)]
require(sparse_product(E, inverse) == identity, 'right exact full inverse')
require(sparse_product(inverse, E) == identity, 'left exact full inverse')
print('Verified complete 1289-field target and its two-sided exact inverse.', flush=True)


def span(frame):
    values = {0}
    for vector in frame:
        values |= {x ^ vector for x in values}
    require(len(values) == 1 << len(frame), 'independent chart basis')
    return tuple(sorted(values))


spaces, canonical = {}, {}
for chart, frame in enumerate(word.frames):
    canonical[chart] = spaces.setdefault(span(frame), len(spaces))
require(len(spaces) == 1102, 'physical chart count after equal-span identification')
input_bank = [canonical[word.inputs[~j]] for j in range(n)]
output_bank = [canonical[word.terminals[e]] for e in ends]
inverse_block_support = {(input_bank[j], output_bank[i])
                         for j, row in enumerate(inverse) for i in row}

certificate = json.loads((package / 'WITNESSES.json').read_text())
candidates = certificate['candidates']
require(candidates == [86, 97232, 97241, 97323, 99064], 'five named survivor occurrences')
m = len(candidates)
position = {e: j for j, e in enumerate(candidates)}
require(all(e in word.routes for e in candidates), 'all candidate occurrences are messages')

# Introduce an independent additive field after every named message. H records
# its effect on the pre-output payload of every other named message; B records
# the complete terminal response. Rational scalar cancellation in H therefore
# remains valid for arbitrary whole-field vector/operator perturbations.
derivative = {e: [Q(0)] * m for e in word.inputs}
H = [[Q(0)] * m for _ in range(m)]
for e in word.schedule:
    value = [sum((q * derivative[f][j] for f, q in word.forms[e].items()), Q(0))
             for j in range(m)]
    if e in position:
        H[position[e]] = value.copy()
        value[position[e]] += 1
    derivative[e] = value
B = [derivative[e] for e in ends]
P = [{j: Q(x, denominator) for j, x in row.items()}
     for denominator, row in (rows[e] for e in candidates)]
R = [[sum((coefficient * B[i][k] for i, coefficient in row.items()), Q(0))
      for k in range(m)] for row in inverse]
Qrows = sparse_product(P, inverse)
G = [[sum((coefficient * B[i][k] for i, coefficient in row.items()), Q(0))
      for k in range(m)] for row in Qrows]
require(H == [[Q(0)] * m for _ in range(m)], 'zero inter-candidate interaction H')
require(G == [[Q(i == j == 0) for j in range(m)] for i in range(m)],
        'P E^-1 B equals diag(1,0,0,0,0)')


def verify_witness(witness):
    edge = witness['edge']
    k = position[edge]
    j, i = witness['input_axis'], witness['output_axis']
    require(word.inputs[~j] == witness['input_chart'], 'witness source chart')
    require(ends[i] == witness['terminal_slot'], 'witness terminal slot')
    require(word.terminals[ends[i]] == witness['terminal_chart'], 'witness terminal chart')
    require((input_bank[j], output_bank[i]) not in inverse_block_support,
            'entire original inverse physical-bank block is zero')
    products = [R[j][h] * Qrows[h].get(i, Q(0)) for h in range(m)]
    coefficient = Q(witness['isolated_coefficient'])
    require(coefficient != 0, 'isolating coefficient is nonzero')
    require(products == [coefficient if h == k else Q(0) for h in range(m)],
            'witness isolates exactly the named operator')
    require(strings([products])[0] == witness['all_five_products'],
            'explicit product row matches exact source')
    return {**witness, 'whole_old_inverse_bank_block_zero': True,
            'source_bank_input_count': input_bank.count(input_bank[j]),
            'terminal_bank_output_count': output_bank.count(output_bank[i])}


witnesses = [verify_witness(w) for w in certificate['witnesses']]
require([w['edge'] for w in witnesses] == candidates, 'one witness per candidate')
print('Verified H, P E^-1 B, and five whole-bank isolation witnesses.', flush=True)

# Independent literal replay controls exercise simultaneous deletion and
# nontrivial scaling, with every one of the 1289 terminal rows compared.
controls = []
for name, scales in [('delete_four_invertible_survivors', [1, 0, 0, 0, 0]),
                     ('nontrivial_simultaneous_rescaling', [2, 3, -1, Q(1, 2), 4]),
                     ('delete_all_five', [0, 0, 0, 0, 0])]:
    forms = word.forms.copy()
    for e, scale in zip(candidates, scales):
        forms[e] = {f: Q(scale) * coefficient for f, coefficient in word.forms[e].items()
                    if scale * coefficient}
    changed = source.Literal(word.schedule, forms, word.routes, word.terminals,
                             word.inputs, word.frames)
    actual = source.all_public_rows(changed)
    expected_rows = []
    for i, original_row in enumerate(E):
        expected = defaultdict(Q, original_row)
        for k in range(m):
            for j, coefficient in P[k].items():
                expected[j] -= B[i][k] * (1 - scales[k]) * coefficient
        expected = clean(expected)
        denominator, numerators = actual[ends[i]]
        require(expected == {j: Q(x, denominator) for j, x in numerators.items()},
                'full literal replay of ' + name)
        expected_rows.append(expected)
    determinant_ratio = Q(scales[0])
    if determinant_ratio:
        D = [1 / Q(scales[0]) - 1] + [1 - Q(x) for x in scales[1:]]
        delta = [1 - Q(x) for x in scales]
        # Expand the two complete matrix products using verified E^-1 and
        # G=P E^-1 B. Their residuals factor through these exact 5x5 matrices.
        # This certifies every entry without cubic multiplication of the
        # deliberately dense changed endpoint and inverse.
        right_residual = [[Q(i == j) * (D[i] - delta[i])
                           - delta[i] * G[i][j] * D[j]
                           for j in range(m)] for i in range(m)]
        left_residual = [[Q(i == j) * (D[i] - delta[i])
                          - D[i] * G[i][j] * delta[j]
                          for j in range(m)] for i in range(m)]
        require(right_residual == left_residual == [[Q(0)] * m for _ in range(m)],
                'zero factorized residuals of both complete inverse products: ' + name)
    else:
        kernel = {j: R[j][0] for j in range(n) if R[j][0]}
        require(bool(kernel), 'nonzero singularity witness')
        require(all(sum((x * kernel.get(j, Q(0)) for j, x in row.items()), Q(0)) == 0
                    for row in expected_rows), 'deleted edge 86 yields an exact full-target kernel')
    controls.append({'name': name, 'scales': [str(x) for x in scales],
                     'all_terminal_rows_verified': n,
                     'determinant_ratio_at_scalar_width': str(determinant_ratio),
                     'inverse_control': 'exact factorized left/right product residuals' if determinant_ratio else 'explicit nonzero kernel vector'})
    print('Verified literal and inverse/kernel control:', name, flush=True)

negative_controls = []
for name, mutation in [('wrong_isolating_coefficient', {'isolated_coefficient': '1'}),
                       ('wrong_terminal_role', {'terminal_slot': ends[0]})]:
    forged = {**certificate['witnesses'][0], **mutation}
    try:
        verify_witness(forged)
    except ValueError as error:
        negative_controls.append({'mutation': name, 'rejected': str(error)})
    else:
        raise ValueError('negative certificate control was accepted: ' + name)

result = {
    'status': 'PASS_S031_FIVE_MESSAGE_OPERATOR_BOUNDARY_RIGIDITY',
    'scope': 'Frozen other internal forms and routes; arbitrary whole-field linear maps on five messages; arbitrary independent bijections at each original physical input/output bank.',
    'not_claimed': 'No rigidity for other internal recoding, new communication, merged banks, changed caller contracts, or a new kappa.',
    'source_files': pins['files'],
    'endpoint_fields': n,
    'endpoint_components': {'one_by_one': 889, 'two_by_two': 200},
    'full_two_sided_inverse_verified': True,
    'canonical_charts': len(spaces),
    'candidates': candidates,
    'candidate_routes': {str(e): list(word.routes[e]) for e in candidates},
    'candidate_grades': {str(e): word.grade(word.routes[e]) for e in candidates},
    'H': strings(H),
    'P_E_inverse_B': strings(G),
    'witnesses': witnesses,
    'literal_and_inverse_controls': controls,
    'negative_controls': negative_controls,
    'environment': {'python': sys.version, 'platform': platform.platform(),
                    'arithmetic': 'fractions.Fraction; exact integers; standard library only'},
    'review_status': 'author replay; independent mathematical admission is separate'
}
args.out.mkdir(parents=True, exist_ok=True)
(args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(result['status'], n, len(witnesses))
print('H = 0; P E^-1 B = diag(1,0,0,0,0); all five inverse-bank isolators verified.')
