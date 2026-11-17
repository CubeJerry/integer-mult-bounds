"""Exact source certificate for the coordinate-supported continuation gate."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


def basis(rows):
    result = {}
    for value in rows:
        while value:
            pivot = value.bit_length() - 1
            if pivot in result:
                value ^= result[pivot]
            else:
                result[pivot] = value
                break
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--one-stage', type=Path, required=True)
    parser.add_argument('--two-stage', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    programme = args.repo / 'research/moonshot-005-program'
    native = programme / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    require(digest(native) == '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e', 'native source pin')
    source = json.loads(native.read_text())
    roots = source['native_roots']
    full = (1 << 111) - 1
    neighbours = []
    for i, row in enumerate(roots):
        neighbours.append(sum(1 << j for j, other in enumerate(roots)
                              if sum(a * b for a, b in zip(row, other)) == 0))
    canonical = [(1 << i) ^ row for i, row in enumerate(neighbours)]
    base = list(basis(canonical).values())
    require(len(base) == 9, 'canonical dimension nine')
    words = [0]
    for row in base:
        words += [value ^ row for value in words]
    require(len(words) == len(set(words)) == 512, 'complete binary code')
    census = []
    sharp = None
    for i in range(111):
        foreign = full ^ neighbours[i] ^ (1 << i)
        weights = Counter((row & foreign).bit_count() for row in words)
        zeros = [row for row in words if not (row & foreign)]
        require(set(zeros) == {0, canonical[i]}, 'exact one-dimensional foreign kernel')
        minimum = min(weight for weight in weights if weight)
        require(minimum >= 18, 'minimum distance eighteen')
        witness = next(row for row in words if (row & foreign).bit_count() == minimum)
        census.append({'receiver': i, 'degree': neighbours[i].bit_count(),
                       'foreign_projection_rank': len(basis(row & foreign for row in base)),
                       'minimum_nonzero_weight': minimum,
                       'weight_histogram': dict(sorted(weights.items())),
                       'minimum_word_hex': hex(witness),
                       'minimum_projection_hex': hex(witness & foreign)})
        if minimum == 18 and sharp is None:
            removed = witness & foreign
            punctured_rank = len(basis(row & foreign & (full ^ removed) for row in base))
            require(punctured_rank < 8, 'eighteen-coordinate deletion creates extra kernel')
            sharp = {'receiver': i, 'deleted_roles': [j for j in range(111) if removed >> j & 1],
                     'remaining_projection_rank': punctured_rank,
                     'new_kernel_dimension': 9 - punctured_rank}
    histogram = Counter(row['minimum_nonzero_weight'] for row in census)
    require(histogram == {18: 7, 19: 24, 20: 52, 21: 16, 22: 11, 23: 1}, 'distance histogram')
    require(min(row['degree'] for row in census) == 55 and max(row['degree'] for row in census) == 62, 'native degrees')
    require(55 - 17 > 36 and 111 - 17 == 94, 'uniform proper-cover lower bound')
    require(len(basis(base[:-1])) == 8, 'missing-mode control')
    controls = []
    for label, condition in [
        ('false uniform distance19', min(histogram) >= 19),
        ('eight modes labelled full canonical bank', len(basis(base[:-1])) == 9),
        ('granted own coordinate still has foreign support', bool((1 << 0) & neighbours[0])),
    ]:
        try:
            require(condition, label)
        except ValueError as error:
            controls.append({'mutation': label, 'rejected': str(error)})
        else:
            raise ValueError('Invalid control passed: ' + label)

    interpreter = programme / 'sessions/2026-11-17-S019/checkpoint3-evidence/C/portable/audit_cp6.py'
    spec = importlib.util.spec_from_file_location('prior_independent_interpreter', interpreter)
    independent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(independent)
    allowance_profile = {127: 37, 64: 74, 1: -74}
    for j in range(1, 9):
        allowance_profile[1 + 7 * j] = allowance_profile.get(1 + 7 * j, 0) + 74
        allowance_profile[7 * j] = allowance_profile.get(7 * j, 0) - 74
    allowance = tuple(x / 6 for x in independent.moment(allowance_profile))
    pins = [
        ('one-stage', args.one_stage, 'ccb08f86b54924ae4f2af1a5647750ef00294666f3e8a80ec77761d8e1dc526d', 9),
        ('two-stage', args.two_stage, '318729fac41fa7871d1e74d440c5af977775655b6eb392ce6f9c1b66ee131176', 8),
    ]
    cuts = []
    for name, path, pin, expected_cap in pins:
        require(digest(path) == pin, 'exact source word')
        word = json.loads(path.read_text())
        cut = word['carrier_interface_before_operation']
        stats, snapshots, charts, events = independent.replay(word, source, [cut])
        values, locations = snapshots[cut]
        code_names = set(word['construction']['canonical_fields'])
        code = [sum(1 << j for j in values[n]) for n in code_names]
        require(len(basis(code)) == len(basis(code + canonical)) == 9, 'actual ground canonical bank')
        require(all(locations[n] == 'zero' for n in code_names), 'ground custody')
        low = [i for i in range(111) if locations[f'X{i}'] != 'Hub']
        require(len(low) == 47, 'exact remaining low X count')
        require(all(values[f'Y{i}'] == {111 + i} and locations[f'Y{i}'] == 'zero' for i in range(111)), 'all initial Y values at ground')
        require(not any(len(charts[locations[n]]) == 7 for n in values), 'no initial live facet record')
        planted_locations = dict(locations, PLANTED_LOCAL_SUM='F0')
        try:
            require(not any(len(charts[place]) == 7 for place in planted_locations.values()),
                    'planted initial rank-seven source changes the cut premise')
        except ValueError as error:
            controls.append({'source': name, 'mutation': 'extra initial facet sum', 'rejected': str(error)})
        else:
            raise ValueError('Planted initial facet source accepted')
        prefix_visits = [event for event in events if event[0] < cut and not event[-1] and len(charts[event[3]]) == 7]
        require(not prefix_visits, 'no prefix public facet arrival')
        for n, row in values.items():
            if n in code_names:
                continue
            chart = charts[locations[n]]
            require(all(independent.subset(charts[f'L{j}'], chart)
                        for j in row if j < 111), 'actual initial local X support')
        moment = independent.moment(stats['movement_profile'])
        room = (allowance[0] - moment[1], allowance[1] - moment[0])
        cap = room[1].numerator // room[1].denominator
        require(cap == expected_cap, 'exact necessary extra owned move cap')
        upper = len(low) + cap
        require(94 > upper, 'strict proper-cover contradiction')
        cuts.append({'source': name, 'word_sha256': pin, 'cut': cut,
                     'live_fields': len(values), 'remaining_X_facet_arrivals_at_most': len(low),
                     'extra_positive_owned_moves_at_most': cap, 'chi_upper': upper, 'chi_lower': 94,
                     'room': independent.interval_json(room), 'movement': independent.interval_json(moment)})
    proof_dependency = programme / 'results/bit-all-route-rank-gap/author/PROOF.md'
    result = {'status': 'PASS_CANONICAL_COORDINATE_SUPPORTED_CONTINUATION_GATE',
              'native_sha256': digest(native), 'interpreter_sha256': digest(interpreter),
              'arrival_proof_sha256': digest(proof_dependency),
              'canonical_basis_hex': list(map(hex, base)), 'canonical_rank': 9,
              'distance_histogram': dict(sorted(histogram.items())),
              'all_receiver_census': census, 'sharp_eighteen_deletion_control': sharp,
              'source_cuts': cuts,
              'negative_controls': controls,
              'scope': 'Every characteristic-two field and positive width; monotone public routes and arbitrary nested owned routes; normalized X histories in C plus one common set of at most17 coordinates. General coded exports are outside.',
              'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'CERTIFICATE.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'])
    print('distance histogram', dict(sorted(histogram.items())))
    print('chi lower 94; source upper bounds', [item['chi_upper'] for item in cuts])


if __name__ == '__main__':
    main()
