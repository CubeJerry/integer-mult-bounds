#!/usr/bin/env python3
"""Exact controls for the repeated binary rank-two source obstruction."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import gzip
import json

PINS = {
    'native': '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
    'layout': '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
    'factor': '346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7',
    'admitted_color_review': '55062cf00045a9d8888fbea8cd613d9c8db65ef570381c282aa004e73d8aa0ae',
}


def need(value, message):
    if not value:
        raise ValueError(message)


def bits(v):
    while v:
        b = v & -v
        yield b.bit_length() - 1
        v -= b


def rank(rows):
    basis = {}
    for v in rows:
        while v and v.bit_length() in basis:
            v ^= basis[v.bit_length()]
        if v:
            basis[v.bit_length()] = v
    return len(basis)


def multiply(A, B):
    out = []
    for row in A:
        v = 0
        for j in bits(row):
            v ^= B[j]
        out.append(v)
    return out


def binary_graph_controls(m):
    gl = [list(x) for x in product(range(4), repeat=2) if rank(x) == 2]
    need(len(gl) == 6, 'GL2 binary size')
    spaces = []
    for maps in product(gl, repeat=m - 1):
        rows = [1, 2]
        for j, A in enumerate(maps, 1):
            for t in range(2):
                rows[t] |= A[t] << (2 * j)
        spaces.append(frozenset((rows[0], rows[1], rows[0] ^ rows[1])))
    need(len(set(spaces)) == 6 ** (m - 1), 'every binary graph plane once')
    adjacency = [sum(1 << j for j, V in enumerate(spaces) if i != j and U & V)
                 for i, U in enumerate(spaces)]
    maximal = []

    def cliques(R, P, X):
        if not P and not X:
            maximal.append(R)
            return
        pivot = max(bits(P | X), key=lambda u: (P & adjacency[u]).bit_count())
        choices = P & ~adjacency[pivot]
        for v in list(bits(choices)):
            cliques(R | (1 << v), P & adjacency[v], X & adjacency[v])
            P &= ~(1 << v)
            X |= 1 << v

    cliques(0, (1 << len(spaces)) - 1, 0)
    span_hist = Counter()
    for C in maximal:
        members = [spaces[j] for j in bits(C)]
        common = set(members[0])
        for W in members[1:]:
            common &= W
        need(bool(common), 'all maximal intersecting families share a line')
        dimension = rank(v for W in members for v in W)
        need(dimension <= m + 1, 'binary graph star span')
        span_hist[dimension] += 1
    # These valid coefficient operators do not commute.
    A, B = [3, 2], [1, 3]
    need(rank(A) == rank(B) == 2 and multiply(A, B) != multiply(B, A),
         'noncommuting coefficient control')
    return {'donors': m, 'graph_planes': len(spaces), 'maximal_intersecting_families': len(maximal),
            'family_size_histogram': dict(Counter(x.bit_count() for x in maximal)),
            'span_dimension_histogram': dict(span_hist), 'noncommuting_GL2_control': True}


def gf4_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return result


def gf4_control():
    matrices = [[[0, 1], [1, 0]], [[0, 1], [1, 1]], [[0, 3], [1, 0]]]
    spaces = []
    for A in matrices:
        W = set()
        for a, b in product(range(4), repeat=2):
            W.add((a, b, gf4_mul(a, A[0][0]) ^ gf4_mul(b, A[1][0]),
                   gf4_mul(a, A[0][1]) ^ gf4_mul(b, A[1][1])))
        need(len(W) == 16 and len({v[2:] for v in W}) == 16, 'GF4 graph projection')
        spaces.append(W)
    pair_sizes = [len(U & V) for U, V in combinations(spaces, 2)]
    need(pair_sizes == [4, 4, 4] and len(set.intersection(*spaces)) == 1,
         'GF4 top does not have a common line')
    return {'modulus': 7, 'matrices': matrices, 'pair_intersection_sizes': pair_sizes,
            'joint_intersection_size': 1, 'binary_field_hypothesis_essential': True}


def main():
    ap = ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    pg = args.repo / 'research/moonshot-005-program'
    paths = {
        'native': pg / 'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json',
        'layout': pg / 'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
        'factor': pg / 'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json',
        'admitted_color_review': pg / 'results/bit-stripe-varying-port-cut/review/output/RESULT.json.gz',
    }
    raw = {k: (gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes())
           for k, p in paths.items()}
    for k, value in raw.items():
        need(sha256(value).hexdigest() == PINS[k], k + ' pin')
    source, layout, factor, old = [json.loads(raw[k])
                                   for k in ('native', 'layout', 'factor', 'admitted_color_review')]
    R, H, D = layout['root_table'], layout['A2'], layout['D4']
    need(R[:111] == source['native_roots'], 'original native roots')
    HM = [sum(1 << j for j in h) for h in H]
    DM = [sum(1 << j for j in d) for d in D]
    O = [sum(1 << j for j, s in enumerate(R) if sum(a * b for a, b in zip(r, s)) == 0)
         for r in R[:111]]
    native = (1 << 111) - 1
    K = [(o & native) ^ (1 << i) for i, o in enumerate(O)]
    need(rank(K) == 9, 'canonical rank9')
    for i, o in enumerate(O):
        need(rank([k & (native ^ (o & native)) for k in K]) == 9, 'canonical outside restriction')
    visible = [[i for i, o in enumerate(O) if hm & o == hm] for hm in HM]
    D_receivers = [sum(1 << i for i, o in enumerate(O) if dm & o == dm) for dm in DM]
    singleton = {next(j for j in h if j < 111): n for n, h in enumerate(H)
                 if sum(j < 111 for j in h) == 1}
    need(len(singleton) == 11, 'singleton count')
    fac = dict(factor['factors'])
    for h, Hh in enumerate(H):
        m = sum(j < 111 for j in Hh)
        if not m:
            continue
        x = 12 // m + fac.get(h, 0)
        need(max(8, x) == (12 if m == 1 else 8), 'actual source bundle capacity')

    def tight(j, i):
        return j not in singleton or i not in visible[singleton[j]]

    old_records = {entry['plane']: entry for entry in old['records']}
    hist, shared_hist = Counter(), Counter()
    uncovered_total, covered_base = 0, 0
    entries = []
    for h, hm in enumerate(HM):
        donors = list(bits(hm & native))
        if len(donors) < 2:
            continue
        targets = [i for i in visible[h] if all(tight(j, i) for j in donors)]
        ports = [d for d, dm in enumerate(DM) if hm & dm == hm]
        need(len(ports) == 45, '45 actual ports')
        target_port_sets = [sum(1 << v for v, d in enumerate(ports) if D_receivers[d] >> i & 1)
                            for i in targets]
        need(all(v.bit_count() == 15 for v in target_port_sets), '15 receiver-visible ports')
        pair_counts = Counter((a & b).bit_count() for a, b in combinations(target_port_sets, 2))
        need(set(pair_counts) <= {3, 6}, 'all target pairs share3 or6 physical ports')
        shared_hist.update(pair_counts)
        port_masks = [sum(1 << k for k, i in enumerate(targets) if D_receivers[d] >> i & 1)
                      for d in ports]
        uncovered = port_masks.count(0)
        previous = old_records[h]
        need(previous['native_donors'] == donors and previous['joint_tight_receivers'] == targets,
             'inherited exact color instance')
        need(previous['port_neighborhoods'] == sorted(set(port_masks) - {0})
             and previous['uncovered_ports'] == uncovered, 'inherited exact port incidence')
        alpha = previous['rank_cap']
        need(1 <= alpha <= len(donors), 'admitted color cap range')
        beta = alpha + 1
        covered_base += beta
        uncovered_total += uncovered
        hist[len(donors), alpha] += 1
        entries.append({'H': h, 'native_donors': donors, 'joint_tight_receivers': targets,
                        'inherited_alpha': alpha, 'new_binary_base_capacity': beta,
                        'shared_port_pair_histogram': dict(pair_counts), 'uncovered_ports': uncovered})
    need(hist == {(2, 1): 204, (2, 2): 23, (3, 1): 630, (3, 2): 249, (3, 3): 2},
         'admitted histogram and reconstructed instances')
    need(covered_base == 2492 and uncovered_total == 1436 and len(entries) == 1108,
         'all ordinary covered information')
    information = Fraction(covered_base + 11 * 3) + Fraction(2 * uncovered_total, 15)
    required = 102 * 32
    need(information == Fraction(40747, 15) and required - information == Fraction(8213, 15),
         'strict rational information inequality')
    binary_controls = [binary_graph_controls(m) for m in (2, 3)]
    field_control = gf4_control()
    result = {
        'status': 'PASS_REPEATED_BINARY_TWO_SOURCE_GATE', 'source_sha256': PINS,
        'base_source_dimension': 32, 'base_ordinary_quotient_dimension': 2,
        'identical_repetition_required': True, 'binary_base_field_required': True,
        'arbitrary_nonlinear_downstream_allowed': True,
        'ordinary_planes': 1108, 'inherited_color_cap_histogram': [[list(k), v] for k, v in sorted(hist.items())],
        'all_pair_shared_port_histogram': dict(shared_hist), 'covered_capacity_per_replication': 2492,
        'uncovered_ports': 1436, 'singleton_capacity_per_replication': 33,
        'information_capacity_per_replication': str(information), 'required_per_replication': required,
        'strict_deficit_per_replication': str(required - information),
        'base_balanced_r180': {'information_capacity': int(180 * information),
                              'required': 180 * required, 'deficit': int(180 * (required - information))},
        'binary_graph_controls': binary_controls, 'GF4_scope_control': field_control,
        'inherited_coloring_search_reexecuted': False, 'new_complete_kappa': False,
        'extra_repair_or_changed_canonical_covered': False,
        'scope': 'One binary32-coordinate quotient base repeated identically; original exact balanced interface.',
    }
    args.out.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(entries, separators=(',', ':')) + '\n').encode()
    result['native_incidence_payload_sha256'] = sha256(payload).hexdigest()
    (args.out / 'NATIVE-INCIDENCE.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    (args.out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], '488964 < 587520; deficit98556; field/replication scopes retained')


if __name__ == '__main__':
    main()
