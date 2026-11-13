#!/usr/bin/env python3
"""Source-bound exact-zero PUBLIC reframe audit; no changed supplier claim."""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import sys
import time

ROOT = Path('/workspace/scratch/19b21bdb3d72')
HERE = Path(__file__).resolve().parent
WORD = ROOT / 'reference/pr7481/WORD.json.gz'
CLIFF = ROOT / 'worker-a/selected/frozen/clifford_exact.py'
PINS = {
    'word': 'acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9',
    'clifford': '2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962',
}
EVENT, OWNER, HELPER = 48865, 1343, 1354


def need(ok, label):
    if not ok:
        raise ValueError(label)


@lru_cache(None)
def rational(text):
    return Q(text)


def add(dst, src, q):
    need(dst is not src, 'distinct ADD fields')
    for k, value in src.items():
        z = dst.get(k, 0) + q * value
        if z:
            dst[k] = z
        else:
            dst.pop(k, None)


def apply(C, op, vector):
    """Literal exact Gaussian-rational gates on an arbitrary physical vector."""
    v = list(vector)
    n = op.n
    for e in op.circuit:
        if e[0] == 'P':
            w = [(Q(0), Q(0))] * len(v)
            for x, a in enumerate(v):
                w[C.mv(e[1], x)] = a
            v = w
        elif e[0] == 'X':
            v = [v[x ^ e[1]] for x in range(len(v))]
        elif e[0] in ('D', 'phase'):
            v = [C.mul_i(a, C.qvalue(e[1], e[2], x, n) if e[0] == 'D' else e[1])
                 for x, a in enumerate(v)]
        elif e[0] == 'C':
            q, sign = e[1:]
            w = []
            for x, (a, b) in enumerate(v):
                c, d = v[x ^ q]
                w.append(((a - sign*b + c + sign*d)/2,
                          (b + sign*a + d - sign*c)/2))
            v = w
        else:
            raise ValueError(e)
    return v


def run(word=WORD, clifford=CLIFF, output=HERE/'RESULT.json'):
    start = time.monotonic()
    raw = word.read_bytes()
    need(sha256(raw).hexdigest() == PINS['word'], 'exact word pin')
    need(sha256(clifford.read_bytes()).hexdigest() == PINS['clifford'], 'Clifford pin')
    w = json.loads(gzip.decompress(raw))
    n = w['public']
    mains = set(w['live']) | {r+112 for r in w['live']}
    mains |= set(w['hosted']['X2']) | set(w['hosted']['Y2'])
    need(HELPER not in mains and OWNER < n, 'specialized helper and retained public owner')
    rows = [{r: Q(1)} for r in range(n)] + [None] * w['owned_fields']
    charts = w['initial'] + [None] * w['owned_fields']
    fresh = set()
    counts = Counter()
    for i, e in enumerate(w['program'][:EVENT+1]):
        op, a = e[:2]
        counts[op] += 1
        if op == 'INIT':
            need(a >= n and charts[a] is None, 'owned INIT only')
            rows[a], charts[a] = {}, e[2]
            fresh.add(a)
        elif op == 'CLEAR':
            need(a >= n and charts[a] == e[2], 'owned CLEAR only')
            rows[a], charts[a] = None, None
            fresh.discard(a)
        elif op == 'MOVE':
            need(charts[a] == e[2] and bool(e[4]) == (a >= n), 'MOVE frame and ownership')
            if i == EVENT:
                need(e == ['MOVE', OWNER, 252, 127, False], 'literal target event')
                row = rows[a].copy()
                need(set(row) == {HELPER}, 'all other 1500 input coefficients cancel exactly')
                coefficient = row[HELPER]
                need(not {k:v for k,v in row.items() if k != HELPER}, 'correct zero specialization')
                need(bool({k:v for k,v in row.items() if k != HELPER-1}), 'wrong helper zeroing rejected')
            charts[a] = e[3]
            fresh.discard(a)
        elif op == 'SCALE':
            need(charts[a] == e[-1], 'SCALE frame')
            q = rational(e[2])
            need(q != 0, 'literal nonzero scalar')
            rows[a] = {k: q*v for k, v in rows[a].items() if q*v}
            fresh.discard(a)
        elif op in ('ADD', 'COPY'):
            b, q = e[2], rational(e[3])
            need(charts[a] == charts[b] == e[-1], 'cocharted scalar operands')
            if op == 'COPY':
                need(a >= n and a in fresh and not rows[a], 'fresh-zero COPY contract')
            add(rows[a], rows[b], q)
            fresh.discard(a)
        else:
            raise ValueError(op)
    spec = importlib.util.spec_from_file_location('zero_audit_clifford', clifford)
    C = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = C
    spec.loader.exec_module(C)
    A = C.canonical_frame(9, tuple(w['frames'][252]))
    B = C.canonical_frame(9, tuple(w['frames'][127]))
    move = A.adjoint().then(B)
    zero = [(Q(0), Q(0))] * 512
    for op in (A, B, move):
        for k in (0, 5):
            e = zero.copy()
            e[k] = (Q(1), Q(0))
            numerators, denominator = op.zero_state(k)
            exact = [(Q(a,2**denominator), Q(b,2**denominator)) for a,b in numerators]
            need(apply(C,op,e) == exact, 'literal driver agrees with retained exact state vectors')
    need(apply(C, move, zero) == zero, 'literal converter preserves exact zero')
    basis = None
    for k in range(512):
        latent = zero.copy()
        latent[k] = (coefficient, Q(0))
        before, after = apply(C, A, latent), apply(C, B, latent)
        if before != after:
            basis = k
            need(apply(C, move, before) == after, 'independent exact converter action')
            differing = [i for i, (a, b) in enumerate(zip(before, after)) if a != b]
            break
    need(basis is not None, 'wrong nonzero specialization rejected')
    # No approximate-zero threshold is sound: a scaled nonzero counterexample
    # has the same exact discrepancy, however small its positive dyadic scale.
    tiny = Q(1, 2**100)
    tiny_before = [(a*tiny, b*tiny) for a, b in before]
    tiny_after = [(a*tiny, b*tiny) for a, b in after]
    need(tiny_before != tiny_after, 'tiny nonzero is not exact zero')
    # Fixed-width two's-complement realization of the selected signed grid:
    # zero uses precisely W zero bits at every positive component width.
    for width in (1, 7, 65, 513):
        need(format(0, f'0{width}b') == '0'*width, 'canonical signed grid zero bits')
    result = dict(status='PASS_PUBLIC_EXACT_ZERO_REFRAME_INTERFACE',
        source_sha256=PINS['word'], clifford_sha256=PINS['clifford'],
        source_instructions=len(w['program']), event=EVENT, instruction=w['program'][EVENT],
        public_owner=OWNER, specialized_helper=HELPER,
        exact_latent_row={str(k): str(v) for k, v in row.items()},
        from_frame=w['frames'][252], to_frame=w['frames'][127], paid_rank=7,
        prefix_instructions=EVENT+1, prefix_counts=dict(counts),
        zero_converter_check=True, retained_public_allocation=True,
        wrong_helper_specialization_control=True, independent_basis_driver_cases=6,
        wrong_nonzero_control=dict(latent_helper_basis=basis,
            differing_components=len(differing), first_difference=differing[0],
            before=[str(x) for x in before[differing[0]]],
            after=[str(x) for x in after[differing[0]]]),
        tiny_nonzero_control=True, canonical_zero_width_controls=[1,7,65,513],
        seconds=time.monotonic()-start,
        scope='Local interface equivalence under exact whole-field zero. General all-positive multiplicities proof is structural linearity; this finite test is not an all-size or precision admission. No public CLEAR/INIT, allocation change, machine alphabet extension, or kappa claim.')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--word', type=Path, default=WORD)
    parser.add_argument('--clifford', type=Path, default=CLIFF)
    parser.add_argument('--output', type=Path, default=HERE/'RESULT.json')
    args = parser.parse_args()
    run(args.word, args.clifford, args.output)
