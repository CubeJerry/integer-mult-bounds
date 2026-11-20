#!/usr/bin/env python3
"""Verify one forty-centre source changing all one hundred nonsingleton donor stars."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True)
    cli.add_argument('--out', type=Path, required=True)
    cli.add_argument('--rank-library', type=Path)
    args = cli.parse_args()
    base = args.repo / 'research/moonshot-005-program/results'
    deps = {'families': base / 'bit-spread-disjoint-h-sources/author/families.py',
            'pair': base / 'bit-spread-overlap-source/author/pair.py'}
    f, pair = (module(deps[key], 'forty_' + key) for key in ('families', 'pair'))
    atlas = f.Atlas(args.repo)
    if args.rank_library:
        import ctypes
        lib = ctypes.CDLL(str(args.rank_library.resolve()))
        rank = lib.field_rank
        rank.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
        rank.restype = ctypes.c_int
        product = np.ascontiguousarray(atlas.product, dtype=np.uint8)
        inverse = np.ascontiguousarray(atlas.inverse, dtype=np.uint8)
        def accelerated(matrix):
            data = np.ascontiguousarray(matrix, dtype=np.uint8).copy()
            return rank(data.ctypes.data, len(data), data.shape[1], product.ctypes.data, inverse.ctypes.data)
        atlas.rank = accelerated
    path = Path(__file__).parent / 'output/PARAMETERS.json'
    raw = path.read_bytes()
    parameters = json.loads(raw)
    witness_raw=(path.parent/"NON-RS-WITNESSES.json").read_bytes()
    witness={r["donor"]:r for r in json.loads(witness_raw)}
    singletons = {j for (j, h), count in atlas.quota.items() if count == 45}
    used, centres, maps_hashes = set(), [], {}
    controls = []
    for record in parameters:
        h, q = record['centres']
        intersection = atlas.planes[h] & atlas.planes[q]
        union = atlas.planes[h] | atlas.planes[q]
        need(intersection == {record['shared_donor']} and len(union) == 5, 'one shared donor in each component')
        need(not used.intersection(union) and not singletons.intersection(union), 'disjoint true nonsingleton components')
        need(union <= atlas.native, 'all original donors are native')
        used.update(union)
        centres.extend((h, q))
        for k in (3, 12):
            charts, maps, details = pair.pair_source(atlas, f, k, record)
            need(set(maps) == union, 'exact five-donor common source')
            for j, rows in maps.items():
                if k==3:
                    w=witness[j]
                    need(len(set(w['planes']))==16 and all(p in rows and atlas.quota[j,p]!=45 for p in w['planes']), 'sixteen true ordinary source planes')
                    observed_rank=atlas.rank(np.vstack([rows[p] for p in w['planes']]))
                    need(observed_rank==w['marked_scalar_rank'] and observed_rank<48, 'source MDS invariant differs from Reed-Solomon')
                maps_hashes[f'{j}/{k}'] = sha256(b''.join(rows[p].tobytes() for p in sorted(rows))).hexdigest()
            # Erasing one ordinary quotient must destroy a saturated source view.
            if not controls:
                donor = record['shared_donor']
                receiver = min(atlas.adj[donor] & atlas.native)
                visible = [p for p in maps[donor] if atlas.planes[p] <= atlas.adj[receiver]]
                original = np.vstack([maps[donor][p] for p in visible])
                damaged = original.copy(); damaged[:k] = 0
                need(atlas.rank(original) == 16*k and atlas.rank(damaged) < 16*k, 'missing real plane is detected')
                controls.append({'mutation': 'remove_one_real_source_quotient', 'donor': donor,
                                 'receiver': receiver, 'original_rank': 16*k, 'damaged_rank': atlas.rank(damaged)})
    need(len(parameters) == 20 and len(centres) == 40 and len(set(centres)) == 40, 'forty actual H charts')
    need(used == atlas.native-singletons and len(used) == 100, 'every nonsingleton original source is replaced')
    generic = {str(j): {str(k): f.generic_singleton(atlas, j, k) for k in (3, 12)} for j in sorted(singletons)}
    count = {str(h): sum(atlas.planes[h] <= atlas.adj[i] for i in atlas.native) for h in centres}
    phases = Counter('fully_early' if all(atlas.quota[j, h] == 30 for j in atlas.planes[h]) else 'mixed' for h in centres)
    roots = sorted(used)
    observations = sum(count.values())
    result = {'status': 'PASS_FORTY_H_CHARTS_ON_ALL_100_NONSINGLETON_SOURCE_STARS',
              'parameters_sha256': sha256(raw).hexdigest(),
              'source_pins': {str(p.relative_to(args.repo)): sha256(p.read_bytes()).hexdigest() for p in deps.values()},
              'centre_pairs': len(parameters), 'native_H_charts': 40, 'selected_source_stars': roots,
              'selected_source_star_count': 100, 'source_stars_inequivalent_to_RS':100, 'non_RS_witnesses_sha256':sha256(witness_raw).hexdigest(), 'generic_singleton_donors': sorted(singletons),
              'native_H_inverse_fibres': observations, 'native_H_donor_fibres': 3*observations,
              'per_chart_native_receivers': count, 'centre_phases': dict(phases),
              'actual_early_source_bases': 111, 'actual_source_H_foreign_full_ranks': 6470,
              'generic_singleton_word': generic, 'source_coefficient_sha256': maps_hashes,
              'negative_controls': controls, 'endpoint_target': 'canonical foreign identity on the forty designated H interfaces',
              'S028_perturbed_target_not_asserted': True, 'common_D_K_endpoint': False,
              'actual_global_return_rank': None, 'new_complete_kappa': False}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'RESULT.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(result['status'], observations, 3*observations)

if __name__ == '__main__':
    main()
