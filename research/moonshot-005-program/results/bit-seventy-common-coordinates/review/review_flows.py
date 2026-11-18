#!/usr/bin/env python3
"""Reconstruct and certify all mixed/late seventy-coordinate route flows.

Independent graph construction; no import of the source or its scipy flow code.
The Dinic engine and driver are recovered S023 review work, completed here.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip
import json
import struct
import subprocess


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def main():
    ap = ArgumentParser()
    for name in ('layout', 'factor', 'author', 'out'):
        ap.add_argument('--' + name, type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    raw = gzip.decompress(a.layout.read_bytes())
    factor = a.factor.read_bytes()
    require(sha256(raw).hexdigest() == '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72', 'layout pin')
    require(sha256(factor).hexdigest() == '346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7', 'factor pin')
    layout, fac = json.loads(raw), json.loads(factor)
    require(fac['denominator'] == 2, 'balanced factor scale')
    roots = layout['root_table']
    planes = [frozenset(x) for x in layout['A2']]
    fours = [frozenset(x) for x in layout['D4']]
    native = frozenset(range(111))
    perp = lambda u, v: sum(x*y for x, y in zip(roots[u], roots[v])) == 0
    facets = [frozenset(v for v in range(120) if perp(u, v)) for u in range(120)]
    index4 = {d: i for i, d in enumerate(fours)}
    dual = [index4[frozenset.intersection(*(facets[u] for u in d))] for d in fours]
    require(dual == layout['dual_D4'], 'exact rational orthogonal D4 complements')
    h_in_d = [[h for h, H in enumerate(planes) if H <= D] for D in fours]
    require(all(len(hs) == 16 for hs in h_in_d), 'sixteen H per D4')
    require(set(Counter(h for hs in h_in_d for h in hs).values()) == {45}, 'forty-five D4 per H')
    increments = dict(fac['factors'])
    multiplicity = [len(H & native) for H in planes]
    early = [(12 // m + increments.get(h, 0)) if m else 0 for h, m in enumerate(multiplicity)]
    late = [max(0, 8 - x) for x in early]
    h_early = [m*x for m, x in zip(multiplicity, early)]
    require(all(0 <= x <= 24 for x in h_early), 'port early/late split')
    author = json.loads(gzip.decompress(a.author.read_bytes()))
    omissions = {j: i for j, i, _, _ in author['late_all_but_one']}
    chunks = [struct.pack('<I', 111)]
    geometry = []
    for j in range(111):
        neighbors = sorted(facets[j] & native)
        hs = [h for h, H in enumerate(planes) if j in H]
        ds = [d for d, D in enumerate(fours) if j in D]
        ks = sorted({k for d in ds for k in h_in_d[dual[d]]})
        require(len(hs) == 28 and sum(45*early[h] for h in hs) == 5760, 'actual early source count')
        require(omissions[j] in neighbors, 'omitted receiver is real')
        ids = {('source',): 0, ('sink',): 1}
        for phase in (0, 1):
            for tag, members in (('H', hs), ('D', ds), ('K', ks), ('F', neighbors)):
                for v in members:
                    ids[phase, tag, v] = len(ids)
        arcs = []
        def arc(u, v, capacity, tag=0):
            if capacity or tag:
                arcs.append((u, v, capacity, tag))
        for tag, members in (('H', hs), ('D', ds), ('K', ks), ('F', neighbors)):
            for v in members:
                arc(ids[0, tag, v], ids[1, tag, v], 12000)
        for h in hs:
            arc(0, ids[0, 'H', h], 45*early[h], 1)
            arc(0, ids[1, 'H', h], 45*late[h])
        for d in ds:
            for h in hs:
                if h in h_in_d[d]:
                    arc(ids[0, 'H', h], ids[0, 'D', d], h_early[h])
                    arc(ids[1, 'H', h], ids[1, 'D', d], 24-h_early[h])
            for k in h_in_d[dual[d]]:
                arc(ids[0, 'D', d], ids[0, 'K', k], 24-h_early[k])
                arc(ids[1, 'D', d], ids[1, 'K', k], h_early[k])
        for k in ks:
            for i in neighbors:
                if i in planes[k]:
                    arc(ids[0, 'K', k], ids[0, 'F', i], 45*late[k])
                    arc(ids[1, 'K', k], ids[1, 'F', i], 45*early[k])
        for i in neighbors:
            arc(ids[1, 'F', i], 1, i, 2)
        require(len({(u, v) for u, v, _, _ in arcs}) == len(arcs), 'unique directed arcs')
        chunks.append(struct.pack('<5I', j, len(ids), len(arcs), len(neighbors), omissions[j]))
        chunks.append(struct.pack('<' + str(len(neighbors)) + 'I', *neighbors))
        chunks.extend(struct.pack('<4I', *edge) for edge in arcs)
        geometry.append([j, len(ids), len(arcs), len(neighbors), sum(45*late[h] for h in hs)])
    binary = b''.join(chunks)
    inp = a.out / 'graphs.bin'
    inp.write_bytes(binary)
    exe = a.out / 'flow-review'
    subprocess.run(['c++', '-std=c++17', '-O3', str(Path(__file__).with_name('driver.cpp')), '-o', str(exe)], check=True)
    receipt = a.out / 'FLOWS.json'
    subprocess.run([str(exe), str(inp), str(receipt)], check=True)
    result = json.loads(receipt.read_text())
    mixed = {(j, i): (value, target) for j, i, k, late_only, value, target, cut in result['cases'] if k == 70 and not late_only}
    late_rows = {(j, i): (value, target) for j, i, k, late_only, value, target, cut in result['cases'] if k == 70 and late_only}
    require(mixed == {(j, i): (value, target) for j, i, value, target in author['mixed']}, 'all 6470 author values independently reproduced')
    require(late_rows == {(j, i): (value, target) for j, i, value, target in author['late_all_but_one']}, 'all 111 late-only values independently reproduced')
    require(all(value == target == cut for _, _, k, _, value, target, cut in result['cases'] if k == 70), 'primal-dual target attainment')
    require(sum(1 for row in result['cases'] if row[2] == 71) == 2, 'two source-cut negative controls')
    summary = {'status': 'PASS_INDEPENDENT_SEVENTY_COORDINATE_FLOWS', 'graph_input_sha256': sha256(binary).hexdigest(), 'author_uncompressed_sha256': sha256(gzip.decompress(a.author.read_bytes())).hexdigest(), 'mixed_cases': len(mixed), 'late_cases': len(late_rows), 'every_directed_capacity_conservation_and_residual_dual_cut_checked': True, 'negative_k71_cases': [x for x in result['cases'] if x[2] == 71], 'geometry': geometry, 'source_independence': 'No author Python imported. Exact native geometry reconstructed; separate C++ integer Dinic engine. Engine provenance retained.'}
    (a.out / 'RESULT.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(summary['status'])


if __name__ == '__main__':
    main()
