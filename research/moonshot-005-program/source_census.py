"""Rebuild the recovered H4 planning census from immutable selected bytes.

This checks finite source geometry and profile relations, not an H4 word.
No contributor scientific implementation is imported.
"""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research/shared-wire-split-composition/data/final.json.gz'
INVOICE = ROOT / 'research/shared-wire-split-composition/FULL-RESULT.json'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def basis(vectors):
    pivots = {}
    for value in vectors:
        while value:
            p = value.bit_length() - 1
            if p in pivots:
                value ^= pivots[p]
            else:
                pivots[p] = value
                break
    return pivots


def contained(vectors, pivots):
    for value in vectors:
        while value:
            p = value.bit_length() - 1
            if p not in pivots:
                return False
            value ^= pivots[p]
    return True


def main():
    data = SOURCE.read_bytes()
    need(hashlib.sha256(data).hexdigest() ==
         '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883', 'source pin')
    raw = INVOICE.read_bytes()
    need(hashlib.sha256(raw).hexdigest() ==
         'd9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7', 'invoice pin')
    word, invoice = json.loads(gzip.decompress(data)), json.loads(raw)
    frames = word['frames']; spans = [basis(f) for f in frames]
    need(all(len(f) == len(s) for f, s in zip(frames, spans)), 'independent frame bases')
    n = word['public']; hosted = word['hosted']
    mains = set(word['live']) | {x+112 for x in word['live']} | set(hosted['X2']) | set(hosted['Y2'])
    helpers = set(range(n)) - mains
    paid = {kind: Counter() for kind in ('main', 'helper', 'owned')}
    current = word['initial'][:] + [None] * word['owned_fields']
    live_owned = set(); peak = lifetimes = 0
    for index, event in enumerate(word['program']):
        op, owner = event[:2]
        if op == 'INIT':
            need(owner >= n and current[owner] is None, f'init {index}')
            current[owner] = event[2]; live_owned.add(owner); lifetimes += 1
            peak = max(peak, len(live_owned))
        elif op == 'CLEAR':
            need(owner >= n and current[owner] == event[2], f'clear {index}')
            current[owner] = None; live_owned.remove(owner)
        elif op == 'MOVE':
            a, b = event[2:4]
            need(current[owner] == a, f'move entry {index}')
            small, large = (a, b) if len(frames[a]) < len(frames[b]) else (b, a)
            rank = len(frames[large]) - len(frames[small])
            need(rank > 0 and contained(frames[small], spans[large]), f'nested move {index}')
            paid['owned' if owner >= n else 'main' if owner in mains else 'helper'][rank] += 1
            current[owner] = b
        elif op in ('ADD', 'COPY', 'SCALE'):
            need(current[owner] == event[-1], f'scalar target chart {index}')
            if op != 'SCALE':
                need(current[event[2]] == event[-1], f'scalar source chart {index}')
        else:
            raise ValueError(f'unknown op {op}')
    need(current[:n] == word['final'] and not live_owned, 'complete frame/lifetime return')
    targets = Counter()
    for h in helpers:
        a, b = word['initial'][h], word['final'][h]
        need(contained(frames[a], spans[b]), 'helper inclusion')
        r = len(frames[b])-len(frames[a]); need(r > 0, 'helper positive target')
        targets[r] += 1
    cochart = 0
    for j, port in enumerate(hosted['Dports']):
        for boundary in ('initial', 'final'):
            for a, b in ((word['live'][port], hosted['X2'][j]), (word['live'][port]+112, hosted['Y2'][j])):
                need(word[boundary][a] == word[boundary][b], 'paired exact boundary chart')
                cochart += 1
    plain = lambda x: {str(k): v for k, v in sorted(x.items())}
    need(plain(targets) == invoice['native']['helpers'], 'helper profile')
    need(plain(sum(paid.values(), Counter())) == invoice['native']['paid'], 'complete native paid profile')
    need((len(mains),len(helpers),peak,lifetimes,cochart) == (400,1080,43,54,384), 'source census')
    recovered = json.loads((ROOT/'research/moonshot-005-recovery-20261111/review-bus/SOURCES.json').read_text())['source_census']
    for kind in paid:
        need(plain(paid[kind]) == {k:v for k,v in recovered[kind].items() if v}, f'recovered {kind}')
    need(not contained([2], basis([1])), 'nonnested negative control')
    need(len(basis([1,1])) != 2, 'dependent-basis negative control')
    print(json.dumps({'status':'PASS_RECOVERED_H4_SOURCE_CENSUS','source_sha256':hashlib.sha256(data).hexdigest(),
        'events':len(word['program']),'frames':len(frames),'main_fields':len(mains),'helpers':len(helpers),
        'paid':{k:plain(v) for k,v in paid.items()},'helper_targets':plain(targets),
        'owned_peak':peak,'owned_lifetimes':lifetimes,'boundary_equalities':cochart,
        'scope':'Finite selected-source census, not H4 construction or physical admission.'},indent=2))


if __name__ == '__main__':
    main()
