#!/usr/bin/env python3
"""Independent joint-translation obstruction from literal anchor information."""
import argparse, gzip, hashlib, importlib.util, json
from pathlib import Path
import numpy as np


def need(ok, why):
    if not ok:
        raise AssertionError(why)


def run(repo, out):
    here = Path(__file__).resolve().parent
    base = repo/'research/moonshot-005-program/results'
    for path, digest in json.loads((here/'SOURCE-PINS.json').read_text()).items():
        need(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
    spec = importlib.util.spec_from_file_location('independent_s030_primitives', base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    layout = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    basis = json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    roots = g.roots_from_files(layout, basis)
    H = [set(P) for P in layout['A2']]
    adj = [{i for i, y in enumerate(roots) if i != j and not g.b(x, y)} for j, x in enumerate(roots)]
    data = json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
    maps = {int(j): {int(h): np.array(F, dtype=np.uint8) for h, F in rows.items()} for j, rows in data['maps'].items()}
    reports = []
    for target, other_h, other_anchor, witness, count in [(45, 116, 0, 4, 29), (100, 643, 62, 2, 27)]:
        star = [h for h, P in enumerate(H) if target in P]
        need(target != 10 and witness != 80 and target in adj[witness], 'actual ordinary identity demand')
        families = {}
        for h, anchor in [(642, 61), (other_h, other_anchor)]:
            need({target, anchor} <= H[h] and anchor != 10, 'actual retained anchor incidence')
            families[h] = {}
            for i in range(111):
                if i == 80 or not H[h] <= adj[i]:
                    continue
                visible = [r for r in maps[anchor] if H[r] <= adj[i]]
                need(len(visible) == 16 and g.rank(np.vstack([maps[anchor][r] for r in visible])) == 48, 'full retained source cut')
                K = g.null(np.vstack([maps[anchor][r] for r in visible if r != h]))
                need(K.shape == (48, 3), 'whole retained fibre')
                families[h][i] = K
        def constraints(allowed):
            spaces, annihilators = {}, {}
            for r in star:
                cols = [K for h in allowed if h != r for i, K in families[h].items() if H[r] <= adj[i]]
                Z = np.hstack(cols) if cols else np.zeros((48, 0), dtype=np.uint8)
                spaces[r] = Z[:, g.echelon(Z)[1]]
                annihilators[r] = g.null(Z.T).T
                need(not np.any(g.mm(annihilators[r], spaces[r])), 'forced-space annihilator')
            return spaces, annihilators
        spaces, annihilators = constraints(list(families))
        defects = {}
        for i in sorted(adj[target] & set(range(111))):
            visible = [r for r in star if H[r] <= adj[i]]
            need(len(visible) == 16, 'actual target source view')
            defect = 48-g.rank(np.vstack([annihilators[r] for r in visible]))
            if defect:
                defects[i] = defect
        need(len(defects) == count and set(defects.values()) == {3}, 'complete independent deficient-view census')
        visible = [r for r in star if H[r] <= adj[witness]]
        K = g.null(np.vstack([annihilators[r] for r in visible]))
        need(K.shape == (48, 3) and g.rank(K) == 3, 'three-dimensional common translation space')
        need(all(g.rank(np.hstack([spaces[r], K])) == spaces[r].shape[1] for r in visible), 'translation in every visible forced space')
        for h in families:
            _, alone = constraints([h])
            need(all(g.rank(np.vstack([alone[r] for r in star if H[r] <= adj[i]])) == 48
                     for i in sorted(adj[target] & set(range(111)))), 'one-anchor control')
        reports.append({'target_donor': target, 'anchors': [61, other_anchor], 'interfaces': [642, other_h],
                        'witness_receiver': witness, 'witness_planes': visible, 'kernel': K.tolist(),
                        'forced_space_dimensions': {r: spaces[r].shape[1] for r in visible},
                        'deficient_native_views': defects, 'single_anchor_controls': True})
    result = {'status': 'PASS_ROOT_JOINT_TRANSLATION_KERNEL_REVIEW', 'reports': reports,
              'author_executables_imported': False, 'frozen_anchors_required': True,
              'arbitrary_redesigned_source_functions_excluded': True, 'new_complete_kappa': False}
    out.mkdir(parents=True, exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], 29, 27, 3, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    run(args.repo.resolve(), args.out.resolve())
