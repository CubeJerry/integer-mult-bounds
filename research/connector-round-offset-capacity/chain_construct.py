#!/usr/bin/env python3
"""Deterministic symmetric-chain prefix covers. @CubeJerry/OpenAI Codex, Apache-2.0."""
import json
from pathlib import Path


def chain_cover(b):
    if type(b) is not int or not 1 <= b <= 12:
        raise ValueError('dimension 1 through 12')
    chains = [[0]]
    for bit in range(b):
        fresh = []
        for chain in chains:
            fresh.append(chain + [chain[-1] | (1 << bit)])
            if len(chain) > 1:
                fresh.append([v | (1 << bit) for v in chain[:-1]])
        chains = fresh
    permutations = []
    locator = [-1] * (1 << b)
    for index, chain in enumerate(chains):
        order = [j for j in range(b) if chain[0] & (1 << j)]
        order += [(a ^ z).bit_length() - 1 for a, z in zip(chain, chain[1:])]
        order += [j for j in range(b) if not chain[-1] & (1 << j)]
        permutations.append(order)
        for subset in chain:
            locator[subset] = index
    return dict(b=b, chains=chains, permutations=permutations, locator=locator)


def connector(cover, D, c, copies=1):
    b = cover['b']; chains = cover['permutations']; M = len(chains)
    if not (type(D) is int and D >= 1 and type(c) is int and c >= D + 1
            and D * M <= c and type(copies) is int and copies >= 1
            and copies * (D + 1) <= c):
        raise ValueError('round and read budgets')
    k = D * b
    if k * copies > 12:
        raise ValueError('finite fixture size')
    rounds = [list(range(k)) for _ in range(c)]
    for group in range(D):
        for j, order in enumerate(chains):
            prefix = [group * b + axis for axis in order]
            rounds[group * M + j] = prefix + [axis for axis in range(k) if axis not in prefix]
    local_reads = {}; correction_classes = dict(before_all=0, after_all=0, same_round=0, between=0)
    for mask in range(1, 1 << k):
        times = []; used_rounds = []
        for group in range(D):
            subset = (mask >> (group * b)) & ((1 << b) - 1)
            if subset:
                r = group * M + cover['locator'][subset]
                used_rounds.append(r); times.append(r * k + subset.bit_count())
        r0 = (-sum(used_rounds)) % c
        if r0 in used_rounds: category = 'same_round'
        elif r0 < min(used_rounds): category = 'before_all'
        elif r0 > max(used_rounds): category = 'after_all'
        else: category = 'between'
        correction_classes[category] += 1
        local_reads[mask] = sorted(times + [r0 * k])
    word = [copy * k + axis for copy in range(copies) for row in rounds for axis in row]
    reads = {}
    for mask in range(1, 1 << (copies * k)):
        times = []
        for copy in range(copies):
            subset = (mask >> (copy * k)) & ((1 << k) - 1)
            if subset: times += [copy * c * k + t for t in local_reads[subset]]
        reads[str(mask)] = sorted(times)
    return dict(groups=D, width=b, characteristic=c, copies=copies, rounds_per_group=M,
                source_word=word, reads=reads, correction_classes=correction_classes)


def main():
    path = Path(__file__).resolve().parent
    covers = [chain_cover(b) for b in range(1, 13)]
    data = dict(schema='symmetric-chain-prefix-cover-v1', covers=covers)
    fixtures = [connector(covers[b-1], D, c, copies) for D, b, c, copies in
                [(1,3,3,1),(2,3,6,1),(3,2,6,1),(3,3,9,1),(2,3,6,2)]]
    (path/'CHAIN-COVERS.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    (path/'CHAIN-FIXTURES.json').write_text(json.dumps(fixtures,separators=(',',':'))+'\n')
    print('GENERATED_CHAIN_PREFIX_COVERS '+json.dumps({'chain_counts':[len(x['chains']) for x in covers],'fixtures':len(fixtures)}))


if __name__ == '__main__': main()
