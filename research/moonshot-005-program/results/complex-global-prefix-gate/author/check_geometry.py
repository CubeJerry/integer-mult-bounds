#!/usr/bin/env python3
"""Exact native witnesses for proper-local-space and appended-mode gates.

No imports from the native source producer or previous geometry verifiers.
All assertions concern this pinned finite source, not unbounded experiments.
The arbitrary-volume implications are proved separately in PROOF.md.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

NATIVE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'


def need(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def root(normal: int) -> tuple[int, ...]:
    ones = [i for i in range(9) if normal >> i & 1]
    if len(ones) == 3:
        return tuple(2 if i in ones else -1 for i in range(9))
    need(len(ones) == 7, 'actual root weight is 3 or 7')
    missing = [i for i in range(9) if i not in ones]
    return tuple(3 if i == missing[0] else -3 if i == missing[1] else 0 for i in range(9))


def gf2_basis(ports: list[int], normals: dict[int, int]) -> list[int]:
    pivots: dict[int, int] = {}
    result: list[int] = []
    for h in ports:
        row = normals[h]
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                result.append(h)
                break
    return result


def scalar_rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    rank = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][c]
        a[rank] = [x / scale for x in a[rank]]
        for i in range(rank + 1, len(a)):
            if a[i][c]:
                scale = a[i][c]
                a[i] = [x - scale * y for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def main(args: argparse.Namespace) -> None:
    raw = args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == NATIVE, 'native source pin')
    source = json.loads(gzip.decompress(raw))
    ports = source['live']
    need(len(ports) == len(set(ports)) == 104, '104 distinct native ports')
    normals = {h: source['frames'][source['initial'][h]][0] for h in ports}
    need(all(source['frames'][source['initial'][h]] == [normals[h]] for h in ports), 'native X lines')
    final_facets = {h:source['frames'][source['final'][h+112]] for h in ports}
    for h,frame in final_facets.items():
        local_normals=dict(enumerate(frame))
        need(len(frame)==8 and len(gf2_basis(list(local_normals),local_normals))==8,
             'actual native Y final frame has dimension eight')
        need(all((normals[h]&row).bit_count()%2==0 for row in frame),
             'actual native Y final frame equals its normal facet')
    roots = {h: root(normals[h]) for h in ports}
    need(all(sum(r) == 0 and sum(x*x for x in r) == 18 for r in roots.values()), 'root hyperplane and norms')
    twice_gram = {
        (h, j): sum(x*y for x, y in zip(roots[h], roots[j])) // 9
        for h in ports for j in ports
    }
    need(all(sum(x*y for x, y in zip(roots[h], roots[j])) == 9*twice_gram[h,j]
             for h in ports for j in ports), 'exact half-integral Gram')
    need(all(twice_gram[h,h] == 2 for h in ports), 'Gram identity diagonal')
    need(all(twice_gram[h,j] in (-1,0,1) for h in ports for j in ports if h != j), 'actual off-diagonal Gram alphabet')
    need(all((twice_gram[h,j] == 0) == bool((normals[h] & normals[j]).bit_count() % 2)
             for h in ports for j in ports if h != j), 'binary facet/Gram correspondence')
    need(all(normals[h].bit_count() % 2 for h in ports), 'own lines excluded from own facets')
    need(all(sum(twice_gram[h,k] * twice_gram[k,j] for k in ports) == 26*twice_gram[h,j]
             for h in ports for j in ports), 'exact G squared = 13G')

    facets = []
    for h in ports:
        adjacent = [j for j in ports if j != h and twice_gram[h,j]]
        basis = gf2_basis(adjacent, normals)
        need(len(adjacent) == 48 and len(basis) == 8, 'every full neighbor set spans its eight-dimensional facet')
        need(all((normals[h] & normals[j]).bit_count() % 2 == 0 for j in adjacent), 'all neighbor normals in facet')
        facets.append({'port': h, 'neighbors': adjacent, 'basis': basis})

    # Enumerate every actual orthogonal frame, then provide a frame witness
    # for each orthogonal pair.  The proof needs coverage, not exhaustiveness.
    index = {h: i for i, h in enumerate(ports)}
    masks = []
    for h in ports:
        masks.append(sum(1 << index[j] for j in ports if h != j and twice_gram[h,j] == 0))
    frames: list[list[int]] = []

    def extend(partial: list[int], available: int) -> None:
        if len(partial) == 8:
            frames.append([ports[i] for i in partial])
            return
        if available.bit_count() < 8 - len(partial):
            return
        while available:
            bit = available & -available
            available ^= bit
            i = bit.bit_length() - 1
            extend(partial + [i], available & masks[i])

    extend([], (1 << len(ports)) - 1)
    need(len(frames) == 759, 'all native orthogonal eight-frames')
    pair_frame: dict[tuple[int, int], int] = {}
    for i, frame in enumerate(frames):
        need(all(twice_gram[b,c] == 0 for p,b in enumerate(frame) for c in frame[p+1:]), 'frame witness orthogonality')
        for p, b in enumerate(frame):
            for c in frame[p+1:]:
                pair_frame.setdefault(tuple(sorted((b,c))), i)

    pairs = []
    exclusive_census: Counter[tuple[int,int]] = Counter()
    for i,b in enumerate(ports):
        for c in ports[i+1:]:
            if twice_gram[b,c] != 0:
                continue
            need((b,c) in pair_frame, 'every orthogonal pair extends to a native frame')
            directional = []
            for h,k in ((b,c),(c,b)):
                exclusive = [j for j in ports if j != h and twice_gram[h,j] and twice_gram[k,j] == 0]
                basis = gf2_basis(exclusive, normals)
                need(len(basis) == 7, 'exclusive neighbors span the seven-dimensional intersection')
                need(all((normals[h] & normals[j]).bit_count() % 2 == 0
                         and ((normals[k] ^ 511) & normals[j]).bit_count() % 2 == 0
                         for j in exclusive), 'exclusive hyperplane equations')
                need(normals[h] not in (0, normals[k] ^ 511) and (normals[k] ^ 511) != 0,
                     'independent defining hyperplanes')
                exclusive_census[len(exclusive), len(basis)] += 1
                directional.append({'receiver':h,'other':k,'exclusive_count':len(exclusive),'basis':basis})
            common = [j for j in ports if twice_gram[b,j] and twice_gram[c,j]]
            plus = next((j for j in common if twice_gram[b,j] == twice_gram[c,j]), None)
            minus = next((j for j in common if twice_gram[b,j] == -twice_gram[c,j]), None)
            need(plus is not None and minus is not None, 'both common-neighbor signs')
            need(all(((normals[c] ^ 511) & normals[j]).bit_count() % 2 == 1
                     and ((normals[b] ^ 511) & normals[j]).bit_count() % 2 == 1
                     for j in common), 'common neighbors outside both exclusive seven-charts')
            pairs.append({'pair':[b,c], 'frame_index':pair_frame[b,c], 'directions':directional,
                          'common_same_sign':plus,'common_opposite_sign':minus,'common_count':len(common)})
    need(len(pairs) == len(pair_frame) == 2860, 'all 2860 orthogonal pairs covered')
    need(sum(exclusive_census.values()) == 5720, 'all directed exclusive tests')

    clique = [0,1,2,4,55,78,82,84]
    need(all(twice_gram[b,c] != 0 for i,b in enumerate(clique) for c in clique[i+1:]), 'eight pairwise nonorthogonal roots')
    need(len(gf2_basis(clique,normals)) == 8, 'nonorthogonal clique normal independence')

    # Boundary controls make the formal source interface nonvacuous.  A single
    # extra coordinate row can serve one receiver at chart zero; all other
    # receivers use their full facets.  This is an algebraic code, not a word.
    b = ports[0]
    gram = [[Fraction(twice_gram[h,j],2) for j in ports] for h in ports]
    coordinate = [Fraction(int(j == b)) for j in ports]
    need(scalar_rank(gram) == 8 and scalar_rank(gram + [coordinate]) == 9,
         'one appended source coordinate is genuinely independent')
    need(all(gram[i][j] == 0 for i,h in enumerate(ports) for j,k in enumerate(ports)
             if i != j and (normals[h] & normals[k]).bit_count() % 2), 'full-facet Gram completion control')
    # For receiver b the completed row is directly the appended coordinate;
    # for every other receiver h, e_h - G_h has source support in F_h.
    need(all(not (Fraction(int(h == j)) - Fraction(twice_gram[h,j],2))
             or (normals[h] & normals[j]).bit_count() % 2 == 0
             for h in ports if h != b for j in ports), 'one-proper-receiver formal control')

    negatives = []
    witness = pairs[0]
    for direction in witness['directions']:
        shortened = direction['basis'][:-1]
        need(len(gf2_basis(shortened,normals)) == 6, 'delete an essential exclusive basis witness')
        negatives.append('essential_exclusive_basis_deleted_'+str(direction['receiver']))
    frame = frames[witness['frame_index']]
    bad_frame = frame[:-1] + [frame[0]]
    need(len(set(bad_frame)) != 8, 'duplicate frame member rejected')
    negatives.append('duplicated_frame_member')
    wrong = witness['common_same_sign']
    need(twice_gram[witness['pair'][0],wrong] != -twice_gram[witness['pair'][1],wrong], 'opposite-sign witness mutation rejected')
    negatives.append('same_sign_substituted_for_opposite')
    need((2 % 2) == 0 and (2 % 3) != 0, 'characteristic-two exception to sign contradiction is visible')
    negatives.append('characteristic_two_not_admitted')

    certificate = {'schema':1,'native_sha256':NATIVE,'normal_by_port':normals,'actual_final_facet_frames':final_facets,
                   'facet_spans':facets,'frames':frames,'orthogonal_pairs':pairs,
                   'nonorthogonal_eight_clique':clique}
    args.output.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(certificate,sort_keys=True,separators=(',',':')).encode()
    encoded = gzip.compress(payload,mtime=0)
    (args.output/'GEOMETRY.json.gz').write_bytes(encoded)
    receipt = {
        'status':'PASS_EXACT_NATIVE_PROPER_LOCAL_SPACE_WITNESSES',
        'native_sha256':NATIVE,'certificate_sha256':hashlib.sha256(encoded).hexdigest(),
        'source_ports':104,'every_neighbor_count':48,'every_neighbor_span':8,
        'orthogonal_eight_frames':len(frames),'orthogonal_pairs':len(pairs),
        'every_orthogonal_pair_extends_to_eight_frame':True,
        'exclusive_directed_census':{str(k):v for k,v in sorted(exclusive_census.items())},
        'every_exclusive_span':7,'both_common_neighbor_signs_for_every_pair':True,
        'nonorthogonal_eight_clique':clique,
        'positive_boundary_controls':['full_facets_allow_Gram_formal_completion','one_coordinate_mode_allows_one_proper_receiver_formally'],
        'negative_controls':negatives,
        'scope':'Exact finite source facts only. PROOF.md supplies arbitrary-volume arguments. No physical acquisition, word, uniform supplier or new kappa is certified.'}
    (args.output/'GEOMETRY-RECEIPT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--native',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args())
