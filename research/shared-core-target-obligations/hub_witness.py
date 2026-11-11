"""Independent inverse columns and small minors for the one-way repair cut."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import json
from math import isqrt
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
P = 1000000007

def need(ok, message):
    if not ok:
        raise ValueError(message)

def run(path, receipt_path):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PIN, 'source hash')
    need(all(P % d for d in range(2, isqrt(P)+1)), 'prime trial division')
    w = json.loads(gzip.decompress(raw))
    h = w['hosted']
    mains = sorted(set(w['live']) | {i+112 for i in w['live']}
                   | set(h['X2']) | set(h['Y2']))
    pos = {r: i for i, r in enumerate(mains)}
    denominators = set()
    def mod(q):
        f = Q(q)
        need(f.denominator % P != 0, 'denominator invertible modulo prime')
        denominators.add(f.denominator)
        return f.numerator * pow(f.denominator, -1, P) % P
    ops = []
    for e in w['program']:
        if e[1] not in pos:
            continue
        need(e[0] not in ('COPY', 'INIT', 'CLEAR'), 'no main overwrite or lifetime operation')
        if e[0] == 'SCALE':
            q = mod(e[2])
            need(q != 0, 'inverse SCALE exists modulo prime')
            ops.append(('S', pos[e[1]], None, q, pow(q, -1, P)))
        elif e[0] in ('ADD', 'COPY') and e[2] in pos:
            need(e[0] == 'ADD', 'no main-only COPY')
            ops.append(('A', pos[e[1]], pos[e[2]], mod(e[3]), None))
    E = {r: {r: 1} for r in mains}
    for i, x in enumerate(w['live']):
        y = x+112
        if i in h['Dports']:
            E[y][x] = 1
        else:
            E[x][y] = P-1
            E[y] = {x: mod('1/2'), y: mod('1/2')}
    for x, y in zip(h['X2'], h['Y2']):
        E[x][y] = P-1
    full = [r for r in mains if len(w['frames'][w['final'][r]]) == 9]
    groups = defaultdict(list)
    for r in mains:
        if r not in full:
            need(len(w['frames'][w['final'][r]]) == 8, 'all non-FULL sources rank eight')
            groups[w['final'][r]].append(r)
    need(len(full) == 200 and len(groups) == 104, 'FULL/group counts')
    columns = {}
    for s in sorted(r for group in groups.values() for r in group):
        v = [0]*len(mains)
        v[pos[s]] = 1
        for kind, d, t, q, inv in reversed(ops):
            if kind == 'S':
                v[d] = v[d]*inv % P
            else:
                v[d] = (v[d]-q*v[t]) % P
        test = v[:]
        for kind, d, t, q, inv in ops:
            if kind == 'S':
                test[d] = test[d]*q % P
            else:
                test[d] = (test[d]+q*test[t]) % P
        need(all(value == (i == pos[s]) for i, value in enumerate(test)), 'inverse column forward identity')
        columns[s] = [sum(q*v[pos[r]] for r, q in E[row].items()) % P for row in full]
    profile = []
    for frame, source in sorted(groups.items()):
        need(1 <= len(source) <= 2, 'small source groups')
        cols = [columns[s] for s in source]
        pivot = next(((j, i) for j, col in enumerate(cols)
                      for i, value in enumerate(col) if value), None)
        rank = 0
        witness = None
        if pivot is not None:
            j, i = pivot
            rank = 1
            witness = {'rows': [full[i]], 'columns': [source[j]], 'minor_mod_p': cols[j][i]}
            if len(cols) == 2:
                other = 1-j
                k = next((k for k in range(len(full))
                          if (cols[j][i]*cols[other][k]-cols[other][i]*cols[j][k]) % P), None)
                if k is not None:
                    rank = 2
                    witness = {'rows': [full[i], full[k]], 'columns': [source[j], source[other]],
                               'minor_mod_p': (cols[j][i]*cols[other][k]-cols[other][i]*cols[j][k]) % P}
        profile.append({'frame': frame, 'sources': source, 'rank_mod_p': rank, 'minor': witness})
    spaces = set()
    for frame in groups:
        span = {0}
        for v in w['frames'][frame]:
            span |= {x ^ v for x in tuple(span)}
        need(len(span) == 256, 'rank-eight source subspace')
        spaces.add(tuple(sorted(span)))
    need(len(spaces) == 104, 'distinct source subspaces')
    total = sum(g['rank_mod_p'] for g in profile)
    need(total == 119, 'one-way rank-one lower bound')
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw)
    need(receipt['status'] == 'PASS_INDEPENDENT_EXACT_BIGINT_RECOMPUTATION', 'invoice receipt status')
    den = int(receipt['denominator'])
    lo, hi = map(int, receipt['M4_numerator_bounds'])
    need(den == 10**15 and lo < hi < 1771183386*10**9, 'exact favorable H4 moment upper bound')
    repaired = [lo-18*total*den, hi-18*total*den]
    need(repaired[1] < 0, 'repair exceeds target moment budget')
    return {'status': 'PASS_INDEPENDENT_ONE_WAY_HUB_CUT', 'source_sha256': PIN,
            'method': 'Reverse inverse columns with all 200 forward identity checks; explicit one/two-column minors, no Gaussian rank routine',
            'prime': P, 'prime_trial_division_through': isqrt(P),
            'coefficient_denominators': sorted(denominators),
            'full_fields': len(full), 'rank8_fields': len(columns), 'groups': profile,
            'rank_histogram_mod_p': dict(Counter(g['rank_mod_p'] for g in profile)),
            'distinct_rank8_subspaces': len(spaces), 'paid_rank1_lower_bound': total,
            'invoice_result_sha256': hashlib.sha256(receipt_raw).hexdigest(),
            'repaired_moment_numerator_bounds': list(map(str, repaired)),
            'repaired_moment_denominator': str(den),
            'scope': 'Applied one-way original-chart-to-FULL repair grammar only; distinct subspaces do not audit all free ABI adapter or reencoding equivalences.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--word', type=Path, default=Path(__file__).resolve().parents[2]/'research/shared-wire-split-composition/data/final.json.gz')
    p.add_argument('--invoice-result', type=Path, default=Path(__file__).with_name('INVOICE-RESULT.json'))
    args = p.parse_args()
    print(json.dumps(run(args.word, args.invoice_result), indent=2))
