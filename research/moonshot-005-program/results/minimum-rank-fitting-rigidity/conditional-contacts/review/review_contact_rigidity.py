#!/usr/bin/env python3
"""Independent source geometry review for invertible-contact block rigidity.

Rebuild nine-dimensional roots and use union/find, rather than importing the
author's producer or using its graph certificates as geometry input.  Exact
algebra is reviewed in CONTACT-RIGIDITY-REVIEW.md; this checks its finite premises.
"""
import argparse
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
B = (5, 56, 69, 100, 65, 77, 96, 103)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def product(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def inverse(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    require(d != 0, 'Invertible control matrix')
    return ((Fraction(a[1][1], d), Fraction(-a[0][1], d)),
            (Fraction(-a[1][0], d), Fraction(a[0][0], d)))


def main(args):
    native = args.repo / 'research/shared-wire-split-composition/data/final.json.gz'
    data = native.read_bytes()
    require(hashlib.sha256(data).hexdigest() == PIN, 'Native source pin')
    source = json.loads(gzip.decompress(data))
    hosted = sorted(source['live'][i] for i in source['hosted']['Dports'])
    require(len(hosted) == len(set(hosted)) == 96 and set(B) <= set(hosted),
            'Hosted source and chosen basis')

    roots = {}
    for i in hosted:
        normal = source['frames'][source['initial'][i]][0]
        positions = [p for p in range(9) if normal & (1 << p)]
        require(len(positions) in (3, 7), 'E8 normal weight')
        if len(positions) == 3:
            root = tuple(2 if p in positions else -1 for p in range(9))
        else:
            p, q = [p for p in range(9) if p not in positions]
            root = tuple(3 * ((k == p) - (k == q)) for k in range(9))
        require(sum(root) == 0 and sum(x * x for x in root) == 18, 'Source root norm')
        roots[i] = root
    dot = lambda i, j: sum(x * y for x, y in zip(roots[i], roots[j]))
    gram = {(i, j): Fraction(dot(i, j), 18) for i in hosted for j in hosted}
    require(all(gram[p, q] == int(p == q) for p in B for q in B), 'Orthogonal B')
    coordinates = {i: tuple(gram[i, b] for b in B) for i in hosted}
    require(all(gram[i, j] == sum(x * y for x, y in zip(coordinates[i], coordinates[j]))
                for i in hosted for j in hosted), 'Gram factorization through B')
    outside = [i for i in hosted if i not in B]
    supports = {i: frozenset(p for p, v in enumerate(coordinates[i]) if v) for i in outside}
    require(all(len(supports[i]) == 4 and
                all(abs(coordinates[i][p]) == Fraction(1, 2) for p in supports[i])
                for i in outside), 'Four dyadic B contacts')
    quads = {q: sorted(i for i in outside if supports[i] == q) for q in set(supports.values())}
    require(len(quads) == 14, 'Fourteen actual support quads')

    pair_checks = []
    for p, q in itertools.combinations(range(8), 2):
        vertices = [i for i in outside if {p, q} <= supports[i]]
        labels = [(side, i) for side in range(2) for i in vertices]
        parents = {v: v for v in labels}

        def representative(v):
            while parents[v] != v:
                parents[v] = parents[parents[v]]
                v = parents[v]
            return v

        edge_count = 0
        for i in vertices:
            for j in vertices:
                if supports[i] & supports[j] == {p, q} and dot(i, j) == 0:
                    edge_count += 1
                    u, v = representative((0, i)), representative((1, j))
                    parents[u] = v
        parts = {}
        for v in labels:
            parts.setdefault(representative(v), set()).add(v)
        expected = [set((side, i) for side, i in labels
                        if (-1 if side else 1) * coordinates[i][p] / coordinates[i][q] == sign)
                    for sign in (-1, 1)]
        require({frozenset(v) for v in parts.values()} == {frozenset(v) for v in expected},
                f'Complete ratio graph {p,q}')
        require(all(len(v) > 1 for v in expected), 'Graph connectivity genuinely used')
        pair_checks.append({'pair': [p, q], 'edges': edge_count,
                            'component_sizes': [len(v) for v in expected]})

    # Independently search all actual rows and all possible middle coordinates,
    # without taking the producer's witnesses or >=5-row shortcut as premises.
    sign_witnesses = []
    for p, r in itertools.combinations(range(8), 2):
        found = None
        for q in range(8):
            if q in (p, r):
                continue
            rows = [i for i in outside if {p, q, r} <= supports[i]]
            for i, j in itertools.combinations(rows, 2):
                s = coordinates[i][p] / coordinates[i][q]
                t = coordinates[i][q] / coordinates[i][r]
                if coordinates[j][p] / coordinates[j][q] == -s and \
                        coordinates[j][q] / coordinates[j][r] == -t:
                    found = {'p': p, 'q': q, 'r': r, 'rows': [i, j],
                             'sigma': int(s), 'tau': int(t)}
                    break
            if found:
                break
        require(found is not None, f'Ordered sign-collapse witness {p,r}')
        sign_witnesses.append(found)

    triples = []
    for triple in itertools.combinations(range(8), 3):
        available = [i for i in outside if set(triple) <= supports[i]]
        require(available and sum(set(triple) <= q for q in quads) == 1,
                'Every triple has an actual row and unique support quad')
        triples.append({'triple': list(triple), 'row': available[0]})

    eye = ((1, 0), (0, 1))
    d = [eye, ((1, 1), (0, 1)), ((1, 0), (1, 1))]
    lam = {(p, q): product(inverse(d[q]), d[p]) for p in range(3) for q in range(3)}
    require(product(d[1], d[2]) != product(d[2], d[1]), 'Noncommuting controls')
    require(all(product(lam[q, r], lam[p, q]) == lam[p, r]
                for p, q, r in itertools.permutations(range(3))), 'Correct ordered cocycle')
    require(product(lam[0, 1], lam[1, 2]) != lam[0, 2], 'Wrong-order mutant rejected')
    # Removing all the ratio-graph constraints leaves isolated vertices, which
    # cannot justify the equality of the contact ratios.
    require(any(min(x['component_sizes']) > 1 for x in pair_checks), 'Missing-edge control')

    author_files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (args.author / name for name in ('PROOF.md', 'GEOMETRY.json',
                                                              'verify_geometry.py', 'MANIFEST.json'))}
    manifest = json.loads((args.author / 'MANIFEST.json').read_text())
    require(all(author_files[name] == sha for name, sha in manifest['files'].items()),
            'Author frozen manifest')
    cert = json.loads((args.author / 'GEOMETRY.json').read_text())
    require(cert['B'] == list(B) and set(cert['hosted']) == set(hosted), 'Author source identity')
    require(cert['source_coordinates'] == {str(i): [str(v) for v in coordinates[i]] for i in hosted},
            'Independent source coordinates agree')
    out = {'status': 'PASS_ROOT_INVERTIBLE_CONTACT_RIGIDITY_REVIEW',
           'source_pin': PIN, 'reviewed_author_files': author_files,
           'hosted_count': 96, 'block_basis': list(B),
           'support_quads': [{'quad': sorted(q), 'rows': v} for q, v in sorted(quads.items(), key=lambda x: sorted(x[0]))],
           'ratio_graphs': pair_checks, 'sign_collapse_witnesses': sign_witnesses,
           'triple_witnesses': triples,
           'negative_controls': {'wrong_noncommuting_order_rejected': True,
                                 'missing_graph_constraints_do_not_imply_gluing': True},
           'classification': 'Proved subject to explicitly invertible allowed B-contact blocks; arbitrary V and every field of characteristic not 2.',
           'scope': 'Finite source premises plus independent algebra review; no contact-invertibility proof, physical implementation, BIT admission or new kappa.'}
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({key: out[key] for key in ('status', 'hosted_count', 'classification')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ('repo', 'author', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    main(parser.parse_args())
