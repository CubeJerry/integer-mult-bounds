#!/usr/bin/env python3
"""Exact first-stage private-rail extraction; six specified rows need repair."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse, gzip, hashlib, json

if not __debug__:
    raise ValueError('This exact replay uses assertions; run without Python -O')
SOURCE_PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CYCLIC_PIN = 'ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'

def load(path, pin):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pin
    return json.loads(gzip.decompress(raw))

def plus(dst, src, factor=F(1)):
    ans = dst.copy()
    for k, v in src.items():
        ans[k] = ans.get(k, F(0)) + factor*v
        if not ans[k]: del ans[k]
    return ans

def span(basis):
    ans = {0}
    for x in basis: ans |= {y ^ x for y in tuple(ans)}
    return frozenset(ans)

def run(ops, initial, public, owneds, spaces, rows):
    loc = dict(enumerate(initial)); rows = {k:dict(v) for k,v in rows.items()}
    moves, counts = Counter(), Counter(); peak = life = 0
    for t, op in enumerate(ops):
        typ, dst = op[:2]
        assert 0 <= dst < public + owneds, (t, op, 'role')
        counts[typ] += 1
        if typ == 'INIT':
            assert dst >= public and dst not in loc, (t, op, 'init')
            loc[dst] = op[2]; rows[dst] = {}; life += 1
        elif typ == 'CLEAR':
            assert dst >= public and loc.get(dst) == op[2], (t, op, 'clear')
            del loc[dst]; del rows[dst]
        elif typ == 'MOVE':
            a,b,owned = op[2:]
            assert type(owned) is bool and owned == (dst >= public)
            assert loc[dst] == a, (t, op, 'source')
            assert spaces[a] < spaces[b] or owned and spaces[b] < spaces[a], (t, op, 'geometry')
            moves[abs((len(spaces[a]).bit_length()-1)-(len(spaces[b]).bit_length()-1))] += 1
            loc[dst] = b
        elif typ in ('ADD', 'COPY'):
            src, c, at = op[2:]
            assert src != dst and loc.get(src) == loc.get(dst) == at, (t, op, 'cochart')
            assert typ != 'COPY' or not rows[dst], (t, op, 'copy')
            rows[dst] = plus(rows[dst], rows[src], F(c))
        elif typ == 'SCALE':
            c, at = op[2:]
            assert F(c) and loc.get(dst) == at
            rows[dst] = {k:F(c)*v for k,v in rows[dst].items()}
        else: raise ValueError(typ)
        peak = max(peak, len(loc)-public)
    assert len(loc) == public
    return rows, loc, dict(instructions=len(ops), counts=dict(counts), moves=dict(moves), peak=peak, lifetimes=life)

def coordinate_expression(target, vectors):
    echelon = {}
    for label, vec in vectors:
        row, expr = dict(vec), {label:F(1)}
        while row:
            pivot = min(row)
            if pivot not in echelon:
                a = row[pivot]
                echelon[pivot] = ({k:v/a for k,v in row.items()}, {k:v/a for k,v in expr.items()})
                break
            a = row[pivot]; r,e = echelon[pivot]
            row = plus(row,r,-a); expr = plus(expr,e,-a)
    row, expr = dict(target), {}
    while row:
        pivot = min(row)
        if pivot not in echelon: return None, row
        a = row[pivot]; r,e = echelon[pivot]
        row = plus(row,r,-a); expr = plus(expr,e,a)
    return expr, {}

def clean(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,list): return [clean(v) for v in x]
    return x

def main(args):
    ROOT, HERE = args.repo, args.output
    HERE.mkdir(parents=True,exist_ok=True)
    source = load(ROOT/'research/shared-wire-split-composition/data/final.json.gz',SOURCE_PIN)
    parent = load(ROOT/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz',CYCLIC_PIN)
    frames = source['frames'] + [x['frame'] for x in parent['additional_charts']]
    spaces = list(map(span, frames)); mapping = {int(k):v for k,v in parent['private_role_map'].items()}
    assert sorted(mapping.values()) == list(range(1480,1880))
    core = set(parent['native_event_to_physical']); ops, lineage, omitted = [], [], Counter()
    for t,op0 in enumerate(parent['program']):
        if t in core: omitted['native'] += 1; continue
        op = list(op0)
        if op[1] < 1480 or op[0] in ('ADD','COPY') and op[2] < 1480:
            omitted['common-access'] += 1; continue
        op[1] -= 1480
        if op[0] in ('ADD','COPY'): op[2] -= 1480
        ops.append(op); lineage.append(t)
    qrows = {i:({i-1480:F(1)} if i>=1480 else {}) for i in range(1880)}
    print('Running original source on all400 independent private inputs', flush=True)
    expected, eloc, ebill = run(parent['program'], parent['initial'],1880,parent['owned_fields'],spaces,qrows)
    assert all(not expected[r] for r in range(1480)), 'common restoration on arbitrary private input'
    print('Running extracted standalone rail', flush=True)
    actual, aloc, abill = run(ops,parent['initial'][1480:],400,parent['owned_fields'],spaces,{i:{i:F(1)} for i in range(400)})
    assert all(eloc[i+1480] == aloc[i] for i in range(400))
    delta = {i:plus(expected[i+1480],actual[i],F(-1)) for i in range(400)}
    delta = {i:r for i,r in delta.items() if r}
    reverse_map = {v-1480:k for k,v in mapping.items()}
    print('Affected source roles:',[reverse_map[i] for i in delta], flush=True)
    vectors = [(i,actual[i]) for i in range(400) if aloc[i] == 127]; repairs = {}
    for i,row in delta.items():
        expr,left = coordinate_expression(row,vectors)
        repairs[i] = {'source_role':reverse_map[i],'row':row,'expression':expr,'unrepresented':left,'facet':aloc[i]}
    output = {'status':'EXPLORATORY_EXACT_RAIL_EXTRACTION','parent_pin':CYCLIC_PIN,'source_pin':SOURCE_PIN,'omitted':dict(omitted),'original_bill':ebill,'extracted_bill':abill,'repairs':repairs}
    (HERE/'EXTRACTION.json').write_text(json.dumps(clean(output),indent=2)+'\n')
    word={'public':400,'owned_fields':parent['owned_fields'],'initial':parent['initial'][1480:],'frames':frames,'program':ops,'source_role_map':{str(k):v-1480 for k,v in mapping.items()},'parent_event':lineage}
    (HERE/'rail-base.json.gz').write_bytes(gzip.compress((json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    print(json.dumps(clean(output),indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args())
