#!/usr/bin/env python3
"""Independent rational-chart / 222-column review of the S015 correction word."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import sympy as sp


@lru_cache(None)
def row_basis(rows):
    if not rows:
        return ()
    matrix = sp.Matrix(rows)
    reduced, _ = matrix.rref()
    return tuple(tuple(x for x in reduced.row(i)) for i in range(reduced.rows)
                 if any(reduced.row(i)))


def chart_basis(chart):
    rows = tuple(tuple(Q(x) for x in r) for r in chart['rows'])
    if chart['kind'] == 'span':
        return row_basis(rows)
    assert chart['kind'] == 'ann'
    if not rows:
        return tuple(tuple(int(i == j) for j in range(8)) for i in range(8))
    return row_basis(tuple(tuple(v) for v in sp.Matrix(rows).nullspace()))


def replay(word, closed):
    bases = {name: chart_basis(value) for name, value in word['charts'].items()}
    inclusion = {}
    def subset(a, b):
        if (a, b) not in inclusion:
            inclusion[a, b] = len(row_basis(bases[a] + bases[b])) == len(bases[b])
        return inclusion[a, b]
    records = {f'X{i}': (f'L{i}', 1 << i, False) for i in range(111)}
    records.update({f'Y{i}': ('zero', 1 << (111+i), False) for i in range(111)})
    counts, profile = Counter(), Counter()
    peak = 0
    cleared = []
    for pos, op in enumerate(word['operations']):
        kind, name, *tail = op
        counts[kind] += 1
        if kind == 'INIT':
            assert name not in records and tail[0] in bases, ('init', pos)
            records[name] = tail[0], 0, True
            peak = max(peak, sum(v[2] for v in records.values()))
        elif kind == 'ADD':
            dst = tail[0]
            assert name != dst and name in records and dst in records, ('add records', pos)
            ca, va, oa = records[name]
            cb, vb, ob = records[dst]
            assert bases[ca] == bases[cb], ('add chart', pos, ca, cb)
            records[dst] = cb, vb ^ va, ob
        elif kind == 'MOVE':
            ca, value, owned = records[name]
            cb = tail[0]
            assert subset(cb, ca) if owned else subset(ca, cb), ('move inclusion', pos, name)
            distance = abs(len(bases[ca]) - len(bases[cb]))
            assert distance > 0, ('zero move', pos)
            profile[distance] += 1
            records[name] = cb, value, owned
        elif kind == 'CLEAR':
            ca, value, owned = records[name]
            assert owned, ('original clear', pos)
            cleared.append((name, ca, hex(value)))
            del records[name]
        else:
            raise AssertionError(('unknown operation', kind))
    for i in range(111):
        assert records[f'X{i}'] == ('Hub', 1 << i, False), ('X endpoint', i)
        want_value = (1 << (111+i)) ^ ((1 << i) if i in [17,26,34] else 0)
        want_chart = f'F{i}' if closed or i in [17,26,34] else 'zero'
        assert records[f'Y{i}'] == (want_chart, want_value, False), ('Y endpoint', i)
    assert sum(v[2] for v in records.values()) == (0 if closed else 170)
    return {'counts': dict(counts), 'profile': dict(sorted(profile.items())),
            'peak': peak, 'rank_length': sum(k*v for k,v in profile.items()),
            'dirty_clears': sum(int(v,16) != 0 for _,_,v in cleared),
            'closed': closed, 'formal_columns':222,
            'completed_targets':[17,26,34]}


@lru_cache(None)
def root_interval(r):
    denominator = 1 << 96
    target = r**199 * denominator**200
    low, high = 0, r*denominator
    if high**200 == target:
        return Q(high,denominator), Q(high,denominator)
    while high-low > 1:
        mid = (low+high)//2
        if mid**200 <= target:
            low = mid
        else:
            high = mid
    assert low**200 <= target < high**200
    return Q(low,denominator), Q(high,denominator)


def interval(profile):
    low = high = Q(0)
    for r, c in profile.items():
        a,b = root_interval(int(r))
        if c < 0:
            a,b = b,a
        low += c*a
        high += c*b
    return low,high


def encode(bounds):
    from decimal import Decimal,localcontext
    low,high=bounds
    with localcontext() as ctx:
        ctx.prec=50
        return {'lower':str(low),'upper':str(high),
                'lower_decimal':str(Decimal(low.numerator)/Decimal(low.denominator)),
                'upper_decimal':str(Decimal(high.numerator)/Decimal(high.denominator))}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--words',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    src=args.repo/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a/two-receiver-output'
    out={'status':'PASS_INDEPENDENT_RECEIVER26_CHRONOLOGY_AND_PRICE','receipts':{},'negative_controls':{},'source_pins':{},'new_complete_kappa':False}
    for mode,source in [('COUPLED','COUPLED-WORD.json'),('UNCOUPLED','UNCOPLED-WORD.json')]:
        baseline=json.loads((src/source).read_text())
        out['source_pins'][source]=hashlib.sha256((src/source).read_bytes()).hexdigest()
        for closed in [False,True]:
            name=mode+'-'+('CLOSED-' if closed else '')+'WORD.json'
            word=json.loads((args.words/name).read_text())
            receipt=replay(word,closed)
            if not closed:
                old_ops=[o for o in word['operations'] if not any(isinstance(x,str) and x.startswith('R26_') for x in o)
                         and not(o[0] in ['MOVE','ADD'] and 'Y26' in o)]
                assert old_ops==baseline['operations'], 'source operations changed'
            else:
                assert receipt['profile']=={1:152,2:20,3:56,4:60,5:22,6:22,7:111,8:1}
                assert receipt['counts']=={'INIT':170,'MOVE':444,'ADD':679 if mode=='COUPLED' else 677,'CLEAR':170}
                assert receipt['peak']==170 and receipt['rank_length']==1627
            receipt['sha256']=hashlib.sha256((args.words/name).read_bytes()).hexdigest()
            out['receipts'][name]=receipt
    direct=json.loads((args.words/'DIRECT-POINT-CONTROL-WORD.json').read_text())
    direct_receipt=replay(direct,True)
    assert direct_receipt['profile']=={1:143,2:19,3:49,4:66,5:22,6:22,7:112,8:1}
    assert direct_receipt['counts']=={'INIT':168,'MOVE':434,'ADD':671,'CLEAR':168}
    out['direct_control']=direct_receipt
    raw=json.loads((args.words/'COUPLED-CLOSED-WORD.json').read_text())
    mutants={}
    bad=copy.deepcopy(raw);bad['operations'].remove(['ADD','DC1_2','Y26']);mutants['omit_final_raw_contribution']=bad
    bad=copy.deepcopy(raw);bad['operations'].remove(['ADD','X15','R26_C7']);mutants['uncaptured_correction']=bad
    bad=copy.deepcopy(raw);idx=next(i for i,o in enumerate(bad['operations'])if o[0]=='CLEAR');bad['operations'][idx]=['CLEAR','X0'];mutants['erase_original_instead_of_owner']=bad
    for name,bad in mutants.items():
        try:
            replay(bad,True)
        except (AssertionError,KeyError) as exc:
            out['negative_controls'][name]={'rejected':True,'reason':str(exc)}
        else:
            raise AssertionError('accepted invalid word '+name)
    profile=out['receipts']['COUPLED-CLOSED-WORD.json']['profile']
    b={127:Q(37,6),64:Q(74,6),1:Q(-74,6)}
    for j in range(1,9):
        b[1+7*j]=b.get(1+7*j,Q(0))+Q(74,6)
        b[7*j]=b.get(7*j,Q(0))-Q(74,6)
    room=b.copy()
    for r,c in profile.items():room[r]=room.get(r,Q(0))-c
    delta={1:9,2:1,3:7,4:-6,7:-1}
    assert interval(delta)[0]>0
    out['movement_moment']=encode(interval(profile))
    out['limiting_movement_room']=encode(interval(room))
    out['excess_over_direct_point']=encode(interval(delta))
    out['scope']='Full rational chart and formal-column replay; all-field/width extension follows from binary linear identities. Dirty erasure and complete supplier admission remain assumed/open.'
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k not in ['receipts','source_pins']}))


if __name__=='__main__':main()
