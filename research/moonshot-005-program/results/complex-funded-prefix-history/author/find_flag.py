#!/usr/bin/env python3
"""Bounded native flag screen for a funded paired prefix trajectory."""
from __future__ import annotations
import argparse, gzip, hashlib, json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

NATIVE = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SEED = '6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def read(path, pin):
    blob = path.read_bytes()
    need(hashlib.sha256(blob).hexdigest() == pin, 'exact source pin')
    return json.loads(gzip.decompress(blob))

def span(vectors):
    result = {0}
    for v in vectors:
        result |= {x ^ v for x in result}
    return frozenset(result)

def basis(space):
    current = {0}
    out = []
    for v in sorted(space):
        if v not in current:
            out.append(v)
            current |= {x ^ v for x in current}
    need(current == space, 'complete canonical span')
    return out

def root(v):
    on = [i for i in range(9) if v >> i & 1]
    if len(on) == 3:
        return [2 if i in on else -1 for i in range(9)]
    off = [i for i in range(9) if not (v >> i & 1)]
    need(len(off) == 2, 'native root type')
    return [3 * (int(i == off[0]) - int(i == off[1])) for i in range(9)]

def main(args):
    native = read(args.native, NATIVE)
    seed = read(args.seed, SEED)
    ports = native['live']
    hosted = {ports[i] for i in native['hosted']['Dports']}
    group = next(g for g in seed['duplex']['groups'] if args.receiver in g['ports'])
    J = group['ports']
    mode = args.mode
    need(mode in group['modes'], 'mode supports receiver class')
    normals = {h: native['frames'][native['initial'][h]][0] for h in ports}
    z = seed['duplex']['omitted_frame'][mode]
    zr = root(z)
    g = {h: F(sum(x*y for x,y in zip(zr,root(normals[h]))),18) for h in ports}
    C3 = span(group['C_frame'])
    final = frozenset(v for v in range(512) if not (v & normals[args.receiver]).bit_count() % 2)
    donors = [h for h in ports if h not in J and g[h] and normals[h] in final]
    final_by_h = {h: frozenset(v for v in range(512) if not (v & normals[h]).bit_count() % 2) for h in J}
    @lru_cache(None)
    def extensions(space):
        result = set()
        for v in final - space:
            result.add(space | frozenset(x ^ v for x in space))
        return tuple(sorted(result, key=lambda s: tuple(sorted(s))))
    def inspect(chain):
        sd = {j: next(3+k for k,C in enumerate(chain) if normals[j] in C) for j in donors}
        rd = {h: max(3+k for k,C in enumerate(chain) if C <= final_by_h[h]) for h in J}
        pairs = [(h,j) for h in J for j in donors if sd[j] <= rd[h]]
        raw = Counter({1:-1,2:-1,3:1})  # One omitted D pivot route.
        for j,d in sd.items():
            count = 2 if j in hosted else 1
            raw[8] -= count
            raw[d-1] += count
            raw[9-d] += count
        for h,d in rd.items():
            if 3 < d < 8:
                count = 2 if h in hosted else 1
                raw[5] -= count
                raw[d-3] += count
                raw[8-d] += count
        active = sorted(set(sd.values()) | set(rd.values()))
        dims = [1,*active,9]
        owned = Counter({8:-2})
        for a,b in zip(dims,dims[1:]):
            owned[b-a] += 2
        delta = {k:raw[k]+owned[k] for k in raw.keys()|owned.keys() if raw[k]+owned[k]}
        moment = sum(v * k**(199/200) for k,v in delta.items())
        return {'pairs':pairs,'source_dimensions':sd,'receiver_dimensions':rd,
                'active_dimensions':active,'raw_delta':dict(raw),'owned_delta':dict(owned),
                'signed_delta':delta,'planning_float_movement_increment':moment,
                'chain':[basis(C) for C in chain]}
    count = 0
    best = None
    def visit(chain):
        nonlocal count,best
        if chain[-1] == final:
            count += 1
            result = inspect(chain)
            key = (len(result['pairs']),-result['planning_float_movement_increment'])
            if best is None or key > best[0]:
                best = key,result
            return
        for C in extensions(chain[-1]):
            visit(chain+[C])
    visit([C3])
    need(count == 9765, 'complete five-dimensional flag count')
    answer = best[1]
    for h,j in answer['pairs']:
        gram = F(sum(x*y for x,y in zip(root(normals[h]),root(normals[j]))),18)
        need(gram == 2*g[h]*g[j], 'exact cross-class correction coefficient')
    answer.update(status='FINITE_NATIVE_FLAG_CANDIDATE',mode=mode,receiver=args.receiver,
                  receiver_class=J,donors=donors,flags_examined=count,
                  paired_coefficients_removed=len(answer['pairs']),
                  native_sha256=NATIVE,seed_sha256=SEED,
                  scope='Finite candidate geometry and planning floats only; actual source, chronology and rigorous complete invoice must be built.')
    args.output.write_text(json.dumps(answer,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:answer[k] for k in ['status','mode','receiver','flags_examined','paired_coefficients_removed','planning_float_movement_increment','source_dimensions','receiver_dimensions','active_dimensions']},indent=2))

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--receiver',type=int,default=0)
    p.add_argument('--mode',type=int,default=0)
    main(p.parse_args())
