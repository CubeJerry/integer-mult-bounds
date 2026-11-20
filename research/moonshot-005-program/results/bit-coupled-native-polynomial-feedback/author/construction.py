"""Structured polynomial-feedback arrays with exact native source inverses."""
from pathlib import Path
import importlib.util
import json
import numpy as np

SUPPORT = (0, 1, 2, 4, 5, 8, 14)
GAPS = (3, 6, 7, 9, 10, 11, 12, 13, 15)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(ok, message):
    if not ok:
        raise ValueError(message)


def context(repo):
    base = repo / "research/moonshot-005-program/results"
    geometric = module(base / "bit-coupled-native-geometric-h-source/component/construction.py", "feedback_geometry")
    f, atlas, previous = geometric.context(repo)
    nodes_path = base / "bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json"
    return geometric, f, atlas, previous, json.loads(nodes_path.read_text()), nodes_path


def polynomial(roots, a):
    result = np.array([1], dtype=np.uint8)
    for x in roots:
        next_row = np.zeros(len(result)+1, dtype=np.uint8)
        next_row[1:] ^= result
        next_row[:-1] ^= a.product[x, result]
        result = next_row
    return result


def quotient(poly, root, a):
    result = np.zeros(16, dtype=np.uint8)
    result[15] = 1
    for t in range(14, -1, -1):
        result[t] = poly[t+1] ^ a.product[root, result[t+1]]
    require(poly[0] == a.product[root, result[0]], "literal polynomial division by a root")
    return result


def field_blocks(geometric, a):
    q = {x: geometric.quadratic(x, a) for x in range(64)}
    nodes = [x for x in range(64) if not q[x]]
    require(len(nodes) == 28 and q[1] == 1, "the common28-node quadric omits1")
    visible = {v: [x for x in nodes if q[v ^ x] ^ q[v] ^ q[x] == 1 ^ q[v]] for v in range(1, 64)}
    require(all(len(xs) == 16 for xs in visible.values()), "all63 sixteen-node native blocks")
    polynomials = {v: polynomial(xs, a) for v, xs in visible.items()}
    require(set.union(*(set(map(int, np.flatnonzero(P[:16]))) for P in polynomials.values())) == set(SUPPORT),
            "the exact seven-position remainder support")
    return nodes, visible, polynomials


def feedback(families, donor, seed=0):
    k = 3
    matrix = np.zeros((k, 16*k), dtype=np.uint8)
    for slot in GAPS:
        block = families.coefficients(f"native-polynomial-feedback/{donor}/{seed}/{slot}", (k, k))
        matrix[:, slot*k:(slot+1)*k] = block
    cycle = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=np.uint8)
    corner = np.zeros((3, 3), dtype=np.uint8)
    corner[0, 0] = 1
    matrix[:, 3*k:4*k] = cycle
    matrix[:, 6*k:7*k] = corner
    return matrix


def source_maps(families, a, global_nodes, donor, seed=0):
    V = feedback(families, donor, seed)
    maps = {}
    eye = np.eye(3, dtype=np.uint8)
    for h in a.by_donor[donor]:
        node = global_nodes["H_nodes"][h]
        powers = a.vandermonde([node], 17)[0]
        maps[h] = np.kron(powers[:16][None, :], eye) ^ a.product[powers[16] ^ 1, V]
    return V, maps


def kernel_columns(P, node, V, a):
    """Unnormalized basis of the entire off-node inverse fibre."""
    k = len(V)
    old = np.kron(quotient(P, node, a)[:, None], np.eye(k, dtype=np.uint8))
    remainder = P[:16].copy()
    remainder[0] ^= 1
    lift = np.kron(remainder[:, None], np.eye(k, dtype=np.uint8))
    return old ^ a.mm(lift, a.mm(V, old))
