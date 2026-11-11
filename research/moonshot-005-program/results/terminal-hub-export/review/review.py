#!/usr/bin/env python3
"""Independent terminal-cut review; no author/predecessor implementation import."""
import argparse, collections, gzip, hashlib, json
from fractions import Fraction as Q
from pathlib import Path

PINS = {
    'native': '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
    'direct': 'f918a319b8133a2fe7ae59da97d47c2a811ee899e0b8253c61bde20c66faa98d',
    'facet': 'e87e4bfcb9772b232e6c443cf2d8ee79a7de356d381eda3aa42040e5e37003c0',
    'proof': '3d8bfe3602feaa9d732a0636a8c72575bafb174318bbb3c960bbf70e7777df2c',
    'certificate': '70a0562b3ecd7693a864b03c8e35dfc067aebb19334914272b9e8fd0a2537fa7',
    'budget': 'b5c4a118bb7e72a31d7ba90a8cd4b72884f9fa6470710850119d709ad3f21f40'
}

def check(condition, message):
    if not condition: raise ValueError(message)

def read_json(path, pin, compressed=False):
    raw = path.read_bytes()
    check(hashlib.sha256(raw).hexdigest() == pin, 'source pin ' + str(path))
    return json.loads(gzip.decompress(raw) if compressed else raw)

def span(frame):
    out = {0}
    for v in frame: out.update({x ^ v for x in list(out)})
    return frozenset(out)

def reverse_row(program, target):
    row = collections.defaultdict(Q, {target: Q(1)})
    for e in reversed(program):
        op, destination = e[:2]
        value = row[destination]
        if op == 'MOVE' or not value: continue
        if op in ('INIT', 'CLEAR'): row[destination] = Q(0)
        elif op == 'SCALE': row[destination] *= Q(e[2])
        elif op in ('ADD', 'COPY'):
            source, weight = e[2:4]
            check(source != destination, 'distinct scalar source')
            if op == 'COPY': row[destination] = Q(0)
            row[source] += value * Q(weight)
        else: raise ValueError('unrecognized source operation ' + op)
    return {i: x for i, x in row.items() if x}

def rank(matrix):
    if not matrix: return 0
    a = [list(row) for row in matrix]
    at = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(at, len(a)) if a[i][column]), None)
        if pivot is None: continue
        a[at], a[pivot] = a[pivot], a[at]
        d = a[at][column]
        a[at] = [x / d for x in a[at]]
        for i in range(at+1, len(a)):
            if a[i][column]:
                d = a[i][column]
                a[i] = [x - d*y for x, y in zip(a[i], a[at])]
        at += 1
        if at == len(a): break
    return at

def main(args):
    root = args.repository
    results = root / 'research/moonshot-005-program/results'
    w = read_json(root/'research/shared-wire-split-composition/data/final.json.gz', PINS['native'], True)
    check(hashlib.sha256((args.packet/'PROOF.md').read_bytes()).hexdigest() == PINS['proof'], 'reviewed proof unchanged')
    cert = read_json(args.packet/'CERTIFICATE.json', PINS['certificate'])
    budget = read_json(results/'relay-acquisition-budget/RESULT.json', PINS['budget'])
    K = cert['terminal_input_roles']
    check(len(K) == len(set(K)) == 52, '52 distinct coordinates')
    spaces = list(map(span, w['frames']))
    H = spaces[127]
    check(len(H) == 512, 'nine-dimensional terminal chart')
    moves = [e for e in w['program'] if e[0] == 'MOVE']
    check(len(moves) == 6310, 'all original MOVE census')
    check(all(spaces[e[2]] != H for e in moves), 'no original canonical terminal exit')
    check(max(len(spaces[e[2]]) for e in moves) == 256, 'all MOVE source dimensions at most eight')
    owned = [e for e in moves if e[4]]
    check(len(owned) == 47, 'all 47 owned routes included')
    endpoint_diagonal = []
    for j in K:
        target = j+112
        row = reverse_row(w['program'], target)
        restricted = {k: row[k] for k in K if row.get(k)}
        check(set(restricted) == {j}, 'diagonal restricted endpoint')
        check(spaces[w['final'][target]] != H and len(spaces[w['final'][target]]) == 256, 'rank-eight endpoint outside terminal chart')
        endpoint_diagonal.append(restricted[j])
    check(collections.Counter(endpoint_diagonal) == {Q(1):45, Q(1,2):7}, '52 endpoint diagonal factors')
    determinant = Q(1)
    for x in endpoint_diagonal: determinant *= x
    check(determinant == Q(1,128), 'nonzero determinant over characteristic zero')
    cases = {}
    for name, filename, key in [('direct','ACQUISITION-PREFIX.json','four_aggregates'),('facet','LIFTED-PREFIX.json','eight_facet_copies')]:
        p = read_json(results/'paid-observable-acquisition'/filename, PINS[name])
        check(p['nonentry_donors'] == K, 'actual prefix donor set')
        locations = dict(enumerate(p['initial']))
        values = {i: [Q(0)]*52 for i in locations}
        raw = {int(k):v for k,v in p['difference_role_map'].items()}
        for column,j in enumerate(K): values[raw[j]][column] = Q(1)
        for e in p['program']:
            op,d = e[:2]
            if op == 'ADD':
                check(spaces[locations[d]] == spaces[locations[e[2]]] == spaces[e[4]], 'physical cochart addition')
                values[d] = [x+Q(e[3])*y for x,y in zip(values[d],values[e[2]])]
            elif op == 'INIT':
                check(d not in locations, 'fresh temporary')
                locations[d] = e[2]; values[d] = [Q(0)]*52
            elif op == 'CLEAR':
                check(locations[d] == e[2], 'clear at current chart')
                del locations[d]; del values[d]
            elif op == 'MOVE':
                check(locations[d] == e[2], 'source chart consistency')
                locations[d] = e[3]
            else: raise ValueError('unrecognized prefix operation ' + op)
        for column,j in enumerate(K):
            check(spaces[locations[raw[j]]] == H, 'all 52 raw donors terminal')
            check(values[raw[j]] == [Q(i == column) for i in range(52)], 'raw donor preserved')
        outside = {i: row for i,row in values.items() if spaces[locations[i]] != H and any(row)}
        check(set(outside) == {1931,1932}, 'only two nonzero outside fields')
        outside_rank = rank(list(outside.values()))
        check(outside_rank == 2, 'exact outside rank two')
        rows = [outside[i] for i in (1931,1932)]
        i,j = K.index(2),K.index(4)
        minor = rows[0][i]*rows[1][j] - rows[0][j]*rows[1][i]
        check(minor == Q(-1,8), 'independent minor')
        duplicate_rank = rank(rows * 26)
        check(duplicate_rank == 2, 'duplicating aggregates does not increase information')
        basis = [[Q(i == c) for i in range(52)] for c in range(52)]
        complement = rows + [basis[c] for c in range(52) if K[c] not in (2,4)]
        check(rank(complement) == 52, '50 extra modes close exactly the information deficit')
        check(rank(rows+[basis[0]]) == 3, 'one extra coordinate supplies only one extra mode')
        upper = Q(budget['variants'][key]['remaining_paid_moment_per_native_interval'][1])
        ceiling = upper.numerator // upper.denominator
        check(ceiling == (2 if name == 'direct' else 8), 'fixed invoice call ceiling')
        check(50 > upper and 17 > upper, 'both fixed-invoice exclusions')
        cases[name] = {'outside_rank':outside_rank, 'minor':str(minor), 'export_volume_lower_bound':52-outside_rank, 'new_call_ceiling':ceiling, 'extra_prefix_rank_required':50-ceiling, 'after33_free_retargeted_messages':17, 'duplicate_rank':duplicate_rank, 'complement_rank':rank(complement)}
    # Structural negative control: introducing one terminal exit changes the premise.
    new_edge = ['MOVE',1933,127,541,True]
    check(any(spaces[e[2]] == H for e in moves+[new_edge]), 'new edge detected as a genuine exit')
    receipt = {'status':'PASS_INDEPENDENT_TERMINAL_REVIEW','reviewed_proof_sha256':PINS['proof'],'reviewed_certificate_sha256':PINS['certificate'],'source_sha256':PINS['native'],'all_original_moves':len(moves),'terminal_outdegree':0,'endpoint_rank':52,'endpoint_determinant':str(determinant),'endpoint_coefficients':{'1':45,'1/2':7},'cases':cases,'independence':'Separate source parser, explicit binary-span chart sets, dense Fraction prefix replay and separate reverse-adjoint implementation; no author or predecessor verifier import.'}
    args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(receipt['status'])

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
