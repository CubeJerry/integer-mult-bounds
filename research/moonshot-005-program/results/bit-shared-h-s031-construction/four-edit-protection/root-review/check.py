#!/usr/bin/env python3
"""Independent core identities and literal native five-edit saturation audit."""
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
    spec = importlib.util.spec_from_file_location('independent_s030_arithmetic', base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
    a = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    Q = [x for x in range(64) if a.qf(x) == 0]
    def divided(d, c):
        return np.array([a.power(c, d-r) if r <= d else 0 for r in range(16)], dtype=np.uint8)
    cores = {}
    for c in Q:
        core = np.column_stack([divided(0,c), divided(1,c), divided(3,c), divided(7,c),
                                divided(13,c)^divided(4,c), divided(15,c)])
        need(a.rank(core) == 6, 'six core directions')
        actual = divided(15,c)^a.M[a.power(c,2), divided(13,c)]
        expected = np.zeros(16,dtype=np.uint8)
        expected[14], expected[15] = c, 1
        need(np.array_equal(actual,expected), 'exact divided-difference identity')
        cores[c] = core
    need(len(Q) == 28, 'geometric nodes')
    for c in Q:
        for d in Q:
            if c != d:
                need(a.rank(np.hstack([cores[c],cores[d]])) == 10, 'all ordered two-core ranks')
    samples = [a.rank(np.hstack([cores[c] for c in Q[:r]])) for r in range(1,7)]
    need(samples == [6,10,13,14,15,16], 'literal core envelope sharpness samples')
    layout = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    basis = json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
    roots = a.roots_from_files(layout,basis)
    H = [set(P) for P in layout['A2']]
    adj = [{i for i,y in enumerate(roots) if i != j and not a.b(x,y)} for j,x in enumerate(roots)]
    node_data = json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes = node_data['H_nodes']
    star = [h for h,P in enumerate(H) if 0 in P]
    need(len(star) == 28 and {nodes[h] for h in star} == set(Q), 'actual donor-0 geometric labels')
    witness = json.loads((here.parent/'output/FIVE-EDIT-WITNESS.json').read_text())
    maps = {int(c):np.array(row,dtype=np.uint8) for c,row in witness['maps'].items()}
    evaluation = lambda c:np.array([a.power(c,d) for d in range(16)],dtype=np.uint8)
    need(set(maps) == set(Q) and all(row.shape == (16,) and np.all(row<64) for row in maps.values()), 'literal scalar source')
    changed = sorted(c for c in Q if not np.array_equal(maps[c],evaluation(c)))
    need(changed == [0,3,5,7,8], 'exact five edited quotients')
    determinants = {}
    for i in sorted(adj[0]):
        visible = [h for h in star if H[h] <= adj[i]]
        need(len(visible) == 16 and len({nodes[h] for h in visible}) == 16, 'actual source cut nodes')
        M = np.vstack([maps[nodes[h]] for h in visible])
        need(a.rank(M) == 16, 'every geometric source cut invertible')
        determinants[i] = hashlib.sha256(M.tobytes()).hexdigest()
    native = [i for i in range(111) if i != 80 and H[17] <= adj[i] and H[806] <= adj[i] and i in adj[0]]
    need(native == [1,7,10,11,12,48,55,56,73,81,90,95,96,97,102], 'literal fifteen native saturation receivers')
    need(nodes[17] == 10 and nodes[806] == 0, 'actual H and R node labels')
    columns, old_columns = [], []
    for i in native:
        off = [h for h in star if h != 17 and H[h] <= adj[i]]
        K = a.null(np.vstack([maps[nodes[h]] for h in off]))
        K0 = a.null(np.vstack([evaluation(nodes[h]) for h in off]))
        need(K.shape == K0.shape == (16,1), 'entire off-H scalar fibres')
        columns.append(K);old_columns.append(K0)
    joined = np.hstack(columns)
    need(a.rank(joined) == 15 and not np.any(a.mm(maps[0][None,:],joined)), 'actual edited R kernel is saturated')
    need(a.rank(joined[:,:-1]) == 14, 'one fewer receiver rank control')
    need(a.rank(np.hstack(old_columns)) == 5, 'unedited geometric source control')
    result = {'status':'PASS_ROOT_FOUR_EDIT_PROTECTION_AND_SHARPNESS_REVIEW',
              'node_core_identities':28,'two_core_pairs':756,'sample_core_ranks':samples,
              'effective_edit_bounds':[5,9,12,13,14],'five_edit_source_cuts':len(determinants),
              'witness_receivers':native,'propagation_rank':15,'unedited_propagation_rank':5,
              'source_matrix_hashes':determinants,'universal_bound_reviewed_analytically':True,
              'five_edit_counterexample_extends_by_tensor':True,'new_complete_kappa':False}
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],63,15,5,flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    run(args.repo.resolve(),args.out.resolve())
