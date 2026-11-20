#!/usr/bin/env python3
"""Independent reconstruction of all73 two-anchor coefficient blocks."""
from argparse import ArgumentParser
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json
import numpy as np


def need(ok, message):
    if not ok:
        raise ValueError(message)


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
here = Path(__file__).resolve().parent
base = args.repo/'research/moonshot-005-program/results'
for p,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
    need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest() == h,'pin '+p)
spec = importlib.util.spec_from_file_location('old_independent_field',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
layout = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
roots = g.roots_from_files(layout,json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text()))
H = list(map(set,layout['A2']))
adj = [{i for i,y in enumerate(roots) if i != j and not g.b(x,y)} for j,x in enumerate(roots)]
raw = json.loads(gzip.decompress((base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz').read_bytes()))
cert = json.loads(gzip.decompress((here.parent/'output/CERTIFICATE.json.gz').read_bytes()))
I = np.eye(3,dtype=np.uint8)
maps = {int(j):{int(h):np.kron(np.array([[g.power(n,e) for e in range(16)]],dtype=np.uint8),I) for h,n in ns.items()} for j,ns in raw['base_nodes'].items()}
for j in (0,61,62):
    maps[j][263] = np.array(raw['maps'][str(j)]['263'],dtype=np.uint8)
views = {j:{i:sorted(h for h in table if H[h] <= adj[i]) for i in sorted(adj[j])} for j,table in maps.items()}
inverse = {j:{i:g.invert(np.vstack([maps[j][h] for h in visible])) for i,visible in views[j].items()} for j in (0,61)}


def fibre(j,i,h):
    p = views[j][i].index(h)
    return inverse[j][i][:,3*p:3*p+3]


def basis(A):
    return A[:,g.echelon(A)[1]]


anchors = {j:{i:fibre(j,i,263) for i,v in views[j].items() if 263 in v} for j in (0,61)}
families = {642:{i:fibre(61,i,642) for i,v in views[61].items() if i < 111 and i != 80 and 642 in v},
            116:{i:fibre(0,i,116) for i,v in views[0].items() if i < 111 and i != 80 and 116 in v}}
S0 = basis(np.hstack(list(anchors[0].values())))
Sb = basis(np.hstack(list(families[642].values())))
ann0 = g.null(S0.T).T
need(S0.shape == Sb.shape == (48,18) and g.rank(np.hstack([S0,Sb])) == 30,'exact old core intersection')
need(all(not np.any(g.mm(ann0,K)) for K in anchors[61].values()),'both anchor fibres lie in same fixed S0')
need([len(families[h]) for h in (642,116)] == [34,32],'all native companion receivers')
need(all(g.rank(np.hstack([Sb,K])) == 18 for family in families.values() for K in family.values()),'both old companion families lie in the full Sb core')
R = np.array(cert['effective_tail_rows'],dtype=np.uint8)
need(R.shape == (12,48) and not np.any(g.mm(R,S0)) and g.rank(g.mm(R,Sb)) == 12,'complete effective quotient tail coordinates')
coefficient = {}
for h,j,offset in [(116,0,1),(642,61,37)]:
    coefficient[h] = {}
    for i,K in families[h].items():
        blocks = np.zeros((73,48,3),dtype=np.uint8)
        blocks[0] = K
        if i in anchors[j]:
            values = g.mm(R,K)
            for u in range(3):
                for v in range(12):
                    blocks[offset+12*u+v] = g.M[anchors[j][i][:,u,None],values[v,None,:]]
        coefficient[h][i] = blocks
planes = views[45][22]
need(planes == cert['planes'] and len(planes) == 16 and all(not H[h] <= adj[22] for h in (116,263,642)),'actual distant full source view')
Y = np.array(cert['universal_kernel_coefficients'],dtype=np.uint8)
need(Y.shape == (73,48,3) and all(not np.any(g.mm(ann0,X)) for X in Y[1:]),'all variable terms vanish in fixed quotient')
need(g.rank(g.mm(ann0,Y[0])) == 3,'uniform rank-three constant projection')
identities = []
for q in planes:
    cols,origins = [],[]
    for h in (642,116):
        for i,blocks in coefficient[h].items():
            if q != h and H[q] <= adj[i]:
                cols.append(blocks)
                origins.extend([h,i,p] for p in range(3))
    need(origins == cert['origins'][str(q)],'complete actual generator census')
    Z = np.concatenate(cols,axis=2).reshape(73*48,-1)
    L = np.array(cert['constant_combinations'][str(q)],dtype=np.uint8)
    need(np.array_equal(g.mm(Z,L),Y.reshape(73*48,3)),'all73 coefficient identities at quotient '+str(q))
    changed = L.copy()
    changed[next(t for t in range(Z.shape[1]) if np.any(Z[:,t])),0] ^= 1
    need(not np.array_equal(g.mm(Z,changed),Y.reshape(73*48,3)),'mutated constant combination rejected')
    identities.append({'plane':q,'generator_columns':Z.shape[1],'coefficient_blocks':73})

# Both tails are nonzero and independent in this concrete scope control.
weights = np.array([(17*t+11)%64 for t in range(72)],dtype=np.uint8)
need(np.any(weights[:36]) and np.any(weights[36:]),'two genuinely changed anchors')
count = 0
for h,j,offset in [(116,0,0),(642,61,36)]:
    delta = g.mm(weights[offset:offset+36].reshape(3,12),R)
    changed = {q:A.copy() for q,A in maps[j].items()}
    changed[263] ^= delta
    for visible in views[j].values():
        need(g.rank(np.vstack([changed[q] for q in visible])) == 48,'both-tail complete source cuts')
        count += 1
    for i,K in families[h].items():
        expected = K ^ (g.mm(anchors[j][i],g.mm(delta,K)) if i in anchors[j] else np.zeros_like(K))
        evaluated = coefficient[h][i][0].copy()
        for w,C in zip(weights,coefficient[h][i][1:]):
            evaluated ^= g.M[w,C]
        off = np.vstack([changed[q] for q in views[j][i] if q != h])
        need(np.array_equal(expected,evaluated) and g.rank(off) == 45 and g.rank(expected) == 3 and not np.any(g.mm(off,expected)),'entire changed companion fibre')
evaluated = Y[0].copy()
for w,C in zip(weights,Y[1:]):
    evaluated ^= g.M[w,C]
need(g.rank(evaluated) == g.rank(g.mm(ann0,evaluated)) == 3,'independently moving tails retain nonzero kernel')
result = {'status':'PASS_ROOT_BOTH_ANCHOR_TAIL_REVIEW','parameters':72,'coefficient_blocks':73,
          'native_companion_families':[34,32],'witness_receiver':22,'uniform_translation_rank':3,
          'identities':identities,'both_nonzero_tail_control_source_cuts':count,
          'author_executables_imported':False,'all_extensions_and_noncommuting_repetitions':True,
          'complete_global_supplier':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],72,73,3,22,flush=True)
