"""Complete fitting minimization in the actual canonical plus half-sum code."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


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


def partition(halves):
    cover = 0
    for half in halves:
        require(not (half & cover), 'half supports must be disjoint')
        cover |= half
    require(len(halves) == 28 and cover.bit_count() == 103, 'exact half partition')
    return cover


def minimize(words, halves, neighbours):
    full = (1 << 111) - 1
    cover = partition(halves)
    records = []
    for i, local in enumerate(neighbours):
        bad = full ^ local
        best = None
        valid_count = 0
        for ci, canonical in enumerate(words):
            required = (canonical & bad) ^ (1 << i)
            if required & (full ^ cover):
                continue
            selected, candidate, valid = 0, canonical, True
            for j, half in enumerate(halves):
                hit, desired = half & bad, required & half
                if desired and desired != hit:
                    valid = False
                    break
                choose = bool(desired)
                if not hit and 2 * (canonical & half).bit_count() > half.bit_count():
                    choose = True
                if choose:
                    selected |= 1 << j
                    candidate ^= half
            if not valid:
                continue
            valid_count += 1
            require(candidate & bad == 1 << i, 'actual witness fitting row')
            key = ((candidate & local).bit_count(), candidate, ci, selected)
            if best is None or key < best:
                best = key
        require(best is not None, 'receiver fitting exists')
        foreign, row, ci, selected = best
        reconstructed = words[ci]
        for j, half in enumerate(halves):
            if selected >> j & 1:
                reconstructed ^= half
        require(reconstructed == row, 'actual witness coefficients')
        records.append({'receiver': i, 'minimum_foreign_support': foreign,
                        'minimum_capped_charge': int(foreign > 36) + int(foreign > 52),
                        'valid_canonical_representatives': valid_count,
                        'canonical_word_index': ci, 'canonical_word_hex': hex(words[ci]),
                        'half_coefficient_mask_hex': hex(selected), 'fitting_row_hex': hex(row)})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--word', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    programme = args.repo / 'research/moonshot-005-program'
    native = programme / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    require(sha(native) == '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e', 'native pin')
    require(sha(args.word) == '318729fac41fa7871d1e74d440c5af977775655b6eb392ce6f9c1b66ee131176', 'hierarchy pin')
    source = json.loads(native.read_text())
    roots = source['native_roots']
    neighbours = [sum(1 << j for j, other in enumerate(roots)
                      if sum(a * b for a, b in zip(row, other)) == 0) for row in roots]
    canonical = [(1 << i) ^ row for i, row in enumerate(neighbours)]
    base = list(basis(canonical).values())
    require(len(base) == 9, 'canonical dimension')
    words = [0]
    for row in base:
        words += [value ^ row for value in words]
    require(len(set(words)) == 512, 'all canonical words')
    interpreter = programme / 'sessions/2026-11-17-S019/checkpoint3-evidence/C/portable/audit_cp6.py'
    spec = importlib.util.spec_from_file_location('independent_source', interpreter)
    independent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(independent)
    word = json.loads(args.word.read_text())
    cut = word['carrier_interface_before_operation']
    _, snapshots, charts, _ = independent.replay(word, source, [cut])
    values, locations = snapshots[cut]
    halves, fields = [], []
    for group in word['construction']['groups']:
        for half in group['halves']:
            name = half['sum_field']
            row = sum(1 << i for i in values[name])
            require(values[name] == set(half['roles']) and locations[name] == half['chart'], 'actual half field and custody')
            require(len(charts[locations[name]]) == 3, 'actual half chart rank')
            halves.append(row)
            fields.append({'field': name, 'row_hex': hex(row), 'chart': locations[name]})
    records = minimize(words, halves, neighbours)
    charge = sum(row['minimum_capped_charge'] for row in records)
    require(charge == 96, 'exact charge96')
    require(Counter(row['minimum_capped_charge'] for row in records) == {0: 15, 1: 96}, 'charge histogram')
    pure_charge = sum(int(row.bit_count() > 36) + int(row.bit_count() > 52) for row in neighbours)
    require(pure_charge == 222, 'canonical control')
    identity = [1 << i for i in range(111)]
    require(all(row & (((1 << 111) - 1) ^ neighbours[i]) == 1 << i for i, row in enumerate(identity)), 'raw identity fitting')
    require(all((row & neighbours[i]).bit_count() == 0 for i, row in enumerate(identity)), 'raw identity charge zero')
    try:
        partition(halves[:-1] + [halves[0]])
    except ValueError as error:
        overlap = str(error)
    else:
        raise ValueError('Overlapping halves accepted')
    result = {'status': 'PASS_EXACT_CANONICAL_PLUS_HALF_SUM_FITTING_CHARGE',
              'native_sha256': sha(native), 'word_sha256': sha(args.word),
              'interpreter_sha256': sha(interpreter), 'canonical_rank': 9,
              'half_sum_rank': len(basis(halves)), 'combined_rank': len(basis(base + halves)),
              'canonical_basis_hex': list(map(hex, base)), 'actual_half_fields': fields,
              'minimum_total_capped_charge': charge,
              'foreign_support_histogram': dict(sorted(Counter(row['minimum_foreign_support'] for row in records).items())),
              'receivers': records, 'source_cut_chi_upper_bounds': [56, 55],
              'controls': {'pure_canonical_charge': pure_charge, 'raw_identity_charge': 0,
                           'false_bound97_refuted': charge < 97, 'overlap_rejection': overlap},
              'scope': 'Exact code minimum96 in characteristic2, all fields/widths. Frozen-source exclusion assumes normalized global X history remains in C plus these28 half sums. New raw/coded directions and earlier source changes are outside.',
              'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'CERTIFICATE.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(result['status'])
    print('ranks C,D,C+D', result['canonical_rank'], result['half_sum_rank'], result['combined_rank'])
    print('exact minimum charge', charge)


if __name__ == '__main__':
    main()
