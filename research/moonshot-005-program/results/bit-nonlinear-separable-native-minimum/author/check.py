"""Verify the native connectivity, scalar Smith minor and finite sumset boundary controls."""
import argparse
from collections import deque
import gzip
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys


def quotient_graph(witness):
    adjacent = [set() for _ in range(111)]
    for _, i, j, *_ in witness['closure']:
        adjacent[i].add(j)
        adjacent[j].add(i)
    parent = {0: None}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in sorted(adjacent[u]):
            if v not in parent:
                parent[v] = u
                queue.append(v)
    if len(parent) != 111:
        raise ValueError('transcript does not connect native output roles')
    return [parent[v] for v in range(111)], min(map(len, adjacent)), max(map(len, adjacent))


def graph_controls():
    # Look at all zero-fixing permutations in two genuinely different four-symbol groups.
    result = {}
    for name, add in [('C4', lambda x, y: (x+y)%4), ('V4', lambda x, y: x^y)]:
        perms = [(0,)+p for p in itertools.permutations([1,2,3])]
        maps = [(0,)+p for p in itertools.product(range(4), repeat=3)]
        below = 0
        first_non_subgroup = 16
        for p in perms:
            graph = {(i,p[i]) for i in range(4)}
            for f in maps:
                second = {(i,f[i]) for i in range(4)}
                s = {(add(u,x),add(v,y)) for u,v in graph for x,y in second}
                if len(s)<6:
                    if graph != second or s != graph:
                        raise ValueError('false strict sumset classification')
                    below += 1
                elif graph != second or s != graph:
                    first_non_subgroup = min(first_non_subgroup, len(s))
        result[name] = {'tested': len(perms)*len(maps), 'exact': below,
                        'first_non_subgroup_sumset': first_non_subgroup}
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    root = a.repo / 'research/moonshot-005-program/results'
    rig = root / 'bit-global-native-rank-rigidity/author'
    spec = (rig/'output/WITNESS.json.gz').read_bytes()
    w = json.loads(gzip.decompress(spec))
    # Use public geometric proof rather than reimplementing its projection hypotheses.
    import importlib.util
    mod = importlib.util.spec_from_file_location('native_rigidity', rig/'check.py')
    native = importlib.util.module_from_spec(mod)
    mod.loader.exec_module(native)
    layout = root/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    roots = json.loads(gzip.decompress(layout.read_bytes()))['root_table'][:111]
    K = [[int(i == j or sum(x*y for x,y in zip(u,v)) == 0)
          for j,v in enumerate(roots)] for i,u in enumerate(roots)]
    checks = native.audit(w, K)
    parents, lo, hi = quotient_graph(w)
    r, c = w['odd_minor']['rows'], w['odd_minor']['cols']
    matrix = [[K[i][j] for j in c] for i in r]
    determinant = native.det(matrix)
    if abs(determinant) != 2:
        raise ValueError('last Smith divisor')
    no_row = dict(w, closure=[t for t in w['closure'] if 110 not in t[1:3]])
    try:
        quotient_graph(no_row)
    except ValueError as error:
        fault = str(error)
    else:
        raise ValueError('row connectivity mutation passed')
    result = {'finite_controls':graph_controls(),'output_role_parents':parents,
              'row_pair_degree_range':[lo,hi], 'odd_minor_integer_determinant':determinant,
              'geometric_rectangles':checks['rectangle_witnesses'],
              'odd_order_or_non_elementary_index': 'order(A) / order(A[2])',
              'disconnected_mutation':fault, 'compressed_witness_sha256':sha256(spec).hexdigest()}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
