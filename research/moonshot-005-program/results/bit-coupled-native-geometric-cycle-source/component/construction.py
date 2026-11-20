"""One literal width-three source on a closed four-centre native cycle."""
from pathlib import Path
import importlib.util
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(ok, message):
    if not ok:
        raise ValueError(message)


def context(repo):
    path = repo / "research/moonshot-005-program/results/bit-coupled-native-geometric-h-source/component/construction.py"
    geometric = module(path, "cycle_geometric_predecessor")
    return geometric, *geometric.context(repo)


def complete(matrix, atlas):
    n = len(matrix)
    result = matrix.copy()
    for p in range(n):
        column = np.eye(n, dtype=np.uint8)[:, p:p+1]
        if atlas.rank(np.hstack([result, column])) > result.shape[1]:
            result = np.hstack([result, column])
        if result.shape[1] == n:
            return result
    raise ValueError("basis completion")


def local_core(geometric, families, atlas, previous, parameters):
    data = geometric.build(families, atlas, previous, parameters)
    S = data["core"]
    _, rows = geometric.rref(S.T, atlas)
    left = geometric.inverse(S[rows], atlas)
    coordinates = {i: atlas.mm(left, K[rows]) for i, K in data["fibres"].items()}
    require(all(np.array_equal(atlas.mm(S, coordinates[i]), K) for i, K in data["fibres"].items()),
            "every local fibre is in its18-dimensional core")
    return {"chart": data["chart"], "points": {x: atlas.mm(F, S) for x, F in data["points"].items()},
            "controls": {j: atlas.mm(data["controls"][p], S) for p, j in enumerate(data["chart"].donors)},
            "coordinates": coordinates, "Hword": data["Hword"]}


def build(geometric, families, atlas, previous, parameters):
    centres = parameters["centres"]
    require(centres == [263, 642, 135, 44], "the frozen four-centre cycle")
    local = {h: local_core(geometric, families, atlas, previous, parameters["local"][str(h)]) for h in centres}
    embeddings = {h: families.coefficients(f"geo-embedding/{centres}/{h}", (48, 18)) for h in centres}
    donors = sorted(set.union(*(atlas.planes[h] for h in centres)))
    maps = {}
    bases = {}
    for j in donors:
        incident = [h for h in centres if j in atlas.planes[h]]
        require(1 <= len(incident) <= 2, "at most two incident centres per literal source")
        core = np.hstack([embeddings[h] for h in incident])
        require(atlas.rank(core) == 18*len(incident), "independent incident centre cores")
        basis = complete(core, atlas)
        inverse = geometric.inverse(basis, atlas)
        bases[j] = basis
        tail_width = 48-core.shape[1]
        seed = parameters["source_seeds"][str(j)]
        rows = {}
        for h in atlas.by_donor[j]:
            blocks = []
            for c in incident:
                data = local[c]
                if h == c:
                    block = data["controls"][j]
                else:
                    point = data["chart"].point[j][h]
                    for attempt in range(100):
                        change = families.coefficients(f"geo-independent/{centres}/{j}/{seed}/{h}/{c}/{attempt}", (3, 3))
                        if atlas.rank(change) == 3:
                            break
                    else:
                        raise ValueError("invertible donor-dependent quotient frame")
                    block = atlas.mm(change, data["points"][point])
                blocks.append(block)
            blocks.append(families.coefficients(f"geo-independent-tail/{centres}/{j}/{seed}/{h}", (3, tail_width)))
            rows[h] = atlas.mm(np.hstack(blocks), inverse)
        maps[j] = rows
    return local, embeddings, maps, bases
