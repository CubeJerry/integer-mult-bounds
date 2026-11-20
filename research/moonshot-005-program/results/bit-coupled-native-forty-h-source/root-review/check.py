#!/usr/bin/env python3
"""Review the new forty-centre placement using the separate predecessor constructor."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np


def need(value, message):
    if not value:
        raise ValueError(message)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True)
    cli.add_argument('--out', type=Path, required=True)
    args = cli.parse_args()
    base = args.repo / 'research/moonshot-005-program/results'
    here = base / 'bit-coupled-native-forty-h-source'
    dependencies = {
        'review': base / 'bit-spread-overlap-source/review/check.py',
        'field': base / 'bit-spread-h263-source/review/check.py',
    }
    r = module(dependencies['review'], 'forty_independent_geometry')
    field = module(dependencies['field'], 'forty_independent_field')
    n = r.Native(args.repo, field)
    raw = (here / 'author/output/PARAMETERS.json').read_bytes()
    params = json.loads(raw)
    non_rs = {v['donor']: v for v in json.loads((here/'author/output/NON-RS-WITNESSES.json').read_bytes())}
    non_rs_counts = Counter()
    native = set(range(111))
    singleton = {j for (j, h), q in n.early.items() if q == 45}
    need(len(singleton) == 11, 'eleven actual singleton source stars')
    used, centres = set(), set()
    receipts, coefficients = {}, {}
    cut_counts = Counter()
    phases = Counter()
    for entry in params:
        h, q = entry['centres']
        pair_donors = n.H[h] | n.H[q]
        need(n.H[h] & n.H[q] == {entry['shared_donor']}, 'literal overlap donor')
        need(len(pair_donors) == 5 and pair_donors <= native, 'five genuine native donors')
        need(not pair_donors & used and not pair_donors & singleton, 'disjoint ordinary components')
        need(not {h, q} & centres, 'unique centre labels')
        used |= pair_donors
        centres |= {h, q}
        for z in (h, q):
            phases['fully_early' if all(n.early[j, z] == 30 for j in n.H[z]) else 'mixed'] += 1
        for k in (3, 12):
            charts = [r.Chart(n, z, k) for z in (h, q)]
            maps = r.paired(charts, entry[str(k)])
            need(set(maps) == pair_donors, 'one simultaneously defined source table per donor')
            rank_cache = {}
            chart_results = {}
            for c in charts:
                count, digest = r.test_chart(c, maps)
                chart_results[str(c.h)] = {'native_receivers': count, 'full_parent_receivers': len(c.receivers), 'inverse_lift_sha256': digest}
            for j, source in maps.items():
                if k == 3:
                    certificate = non_rs[j]
                    qs = certificate['planes']
                    need(len(qs) == len(set(qs)) == 16 and set(qs) <= set(source), 'literal non-RS source witness')
                    rho = field.eliminate(np.vstack([source[z] for z in qs]))[0]
                    need(rho == certificate['marked_scalar_rank'] < 48, 'genuine source-information change')
                    need(certificate['minimum_full_bank_defect'] == 16*(48-rho), 'full original-bank defect')
                    non_rs_counts[rho] += 1
                c = next(c for c in charts if j in c.donors)
                r.schedule(n, c, j, source, entry[str(k)]['early'][str(j)], {h, q})
                coefficients[f'{j}/{k}'] = sha256(b''.join(source[z].tobytes() for z in sorted(source))).hexdigest()
                for i in n.adj[j]:
                    view = n.views[j, i]
                    if not {h, q}.intersection(view):
                        key = tuple(sorted(sha256(source[z].tobytes()).digest() for z in view))
                        if key not in rank_cache:
                            rank_cache[key] = field.eliminate(np.vstack([source[z] for z in view]))[0]
                        need(rank_cache[key] == 16*k, 'every exterior original-source view')
                    cut_counts[k] += int(i in native)
            receipts[f'{h},{q},{k}'] = {'charts': chart_results, 'external_rank_classes': len(rank_cache)}
    need(len(params) == 20 and len(centres) == 40 and used == native-singleton, 'exact cover of all one hundred ordinary sources')
    author = json.loads((here / 'author/output/RESULT.json').read_bytes())
    need(coefficients == author['source_coefficient_sha256'], 'independent constructor matches every literal new source coefficient table')
    totals = {}
    for k in (3, 12):
        views = sum(sum(x['native_receivers'] for x in val['charts'].values()) for key, val in receipts.items() if key.endswith(','+str(k)))
        background = sum(len(n.adj[j] & native) for j in singleton)
        need(views == 1341 and cut_counts[k] + background == 6470, 'same full native domain for both components')
        totals[str(k)] = {'native_designated_inverse_fibres': views, 'new_source_foreign_cuts': cut_counts[k], 'unchanged_singleton_foreign_cuts': background}
    need(dict(phases) == author['centre_phases'], 'genuine mixed and fully early placement census')
    cost = json.loads((here / 'author/output/COST.json').read_bytes())
    special = Counter()
    for j, bill in cost['special_donor_costs'].items():
        need(int(j) in used, 'new source bill belongs to genuine changed donor')
        need(bill['inverse_ADD'] == bill['basis_ADD'] + bill['permutation_ADD'], 'paid pure inverse')
        need(bill['forward_ADD'] == bill['inverse_ADD'] + bill['write_ADD'] + bill['read_ADD'], 'paid late source parities')
        need(bill['total_ADD'] == bill['forward_ADD'] + bill['inverse_ADD'], 'full source word and restore')
        need(bill['INIT'] == bill['dirty_CLEAR'], 'balanced stationary source ownership')
        special.update(bill)
    need(dict(special) == cost['special'], 'complete one-hundred-donor invoice')
    bg = cost['background']
    inv = bg['early_basis_ADD'] + bg['source_owner_permutation_ADD']
    cache = bg['snapshot_copy_ADD_INIT_dirty_CLEAR']
    forward = inv + cache + bg['late_evaluation_ADD']
    combined = cost['combined']
    need(combined['source_forward_and_inverse_ADD'] == inv + forward + special['total_ADD'] == 4154915920, 'all111 forward and inverse ADD total')
    need(combined['source_INIT'] == combined['source_dirty_CLEAR'] == cache + special['INIT'] == 1981440, 'every source cache paid')
    need(combined['source_extra_MOVE'] == 0, 'no additional source movement in retained owner compiler')
    result = {
        'status': 'PASS_INDEPENDENT_FORTY_CENTRE_SOURCE_REVIEW',
        'parameters_sha256': sha256(raw).hexdigest(),
        'dependency_sha256': {str(p.relative_to(args.repo)): sha256(p.read_bytes()).hexdigest() for p in dependencies.values()},
        'new_author_constructor_imported': False,
        'scope': 'New exact placement, common source coefficients, all designated inverse fibres and early/exterior ranks; inherited singleton word and native-owner compiler remain admitted dependencies.',
        'native_centres': 40, 'changed_ordinary_donors': 100,
        'non_RS_marked_rank_counts': dict(non_rs_counts),
        'centre_phases': dict(phases), 'components': totals,
        'actual_component_reviews': receipts,
        'complete_source_cost': combined,
        'controls': 'Every designated chart runs the independently written invertible-donor-rescaling fault; it preserves rank and breaks the required original-coordinate lift.',
        'common_D_K_F_continuation': False, 'new_complete_kappa': False,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'], json.dumps(totals, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
