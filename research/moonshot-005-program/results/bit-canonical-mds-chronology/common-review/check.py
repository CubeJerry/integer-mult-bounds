#!/usr/bin/env python3
"""Independent literal replay of the actual canonical/MDS chronology patch."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sympy as sp

ROOT = 'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            j = row.bit_length()-1
            if j in pivots:
                row ^= pivots[j]
            else:
                pivots[j] = row
                break
    return len(pivots)


def xor(rows):
    out = 0
    for row in rows:
        out ^= row
    return out


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def mul4(a, b):
    a0, a1, b0, b1 = a&1, a>>1, b&1, b>>1
    return (a0*b0 ^ a1*b1) | ((a0*b1 ^ a1*b0 ^ a1*b1)<<1)


def mulrows(c, rows):
    return [xor(rows[j] for j in range(2) if (mul4(c, 1<<j)>>i)&1)
            for i in range(2)]


class Geometry:
    def __init__(self, charts):
        self.bases = {}
        for name, desc in charts.items():
            rows = desc['rows']
            if desc['kind'] == 'ann':
                columns = sp.Matrix(rows).nullspace() if rows else list(sp.eye(8).columnspace())
            else:
                assert desc['kind'] == 'span'
                columns = sp.Matrix(rows).T.columnspace() if rows else []
            self.bases[name] = sp.Matrix.hstack(*columns) if columns else sp.zeros(8, 0)

    @lru_cache(None)
    def sub(self, a, b):
        return self.bases[b].row_join(self.bases[a]).rank() == self.bases[b].cols

    @lru_cache(None)
    def same(self, a, b):
        return self.sub(a, b) and self.sub(b, a)

    def dim(self, a):
        return self.bases[a].cols


def expected_aggregates(roots):
    sums = [[0, 0] for _ in range(4)]
    foreign = [j for j in range(111) if j != 3 and dot(roots[j], roots[3]) == 0]
    for j in foreign:
        choices = [t for t, q in enumerate((76, 81, 91, 96))
                   if dot(roots[j], roots[q]) == 0][:2]
        assert len(choices) == 2
        a, b = choices
        deninv = mul4(a^b, a^b)
        left = [1<<(4*j+k) for k in range(2)]
        right = [1<<(4*j+2+k) for k in range(2)]
        for dst, coeff in ((a, b), (b, a)):
            x = mulrows(mul4(deninv, coeff), left)
            y = mulrows(deninv, right)
            for k in range(2):
                sums[dst][k] ^= x[k]^y[k]
    return sums


def replay(word, roots, geo, milestones=True, strict_invoice=True):
    initial = {f'X{j}_{k}':1<<(4*j+k) for j in range(111) for k in range(4)}
    initial.update({f'Y{j}_{k}':1<<(444+4*j+k) for j in range(111) for k in range(4)})
    values = initial.copy()
    places = {f'X{j}_{k}':f'L{j}' for j in range(111) for k in range(4)}
    places.update({f'Y{j}_{k}':'zero' for j in range(111) for k in range(4)})
    owners, born = set(), set()
    count, profile = Counter(), Counter()
    dirty = 0
    basis_roles = (0,1,2,4,8,9,14,30,59)
    canonical = {(i,k):sum(1<<(4*j+k) for j in range(111)
                          if i == j or dot(roots[i], roots[j]) == 0)
                 for i in range(111) for k in range(4)}
    cspace = list(canonical.values())
    assert rank(cspace) == 36
    expected = expected_aggregates(roots)
    completed_seeds, transport, all_partial = [], [], []
    observations = {}
    mark_at = {v:k for k,v in word['milestones'].items()}
    held_names = ('X1_2','X1_3','X2_2','X2_3')
    seed_departures = {}

    def capture(step):
        if not milestones or step not in mark_at:
            return
        name = mark_at[step]
        hub = [values[n] for n in initial if n.startswith('X') and geo.same(places[n], 'Hub')]
        held = [n for n in initial if n.startswith('X') and not geo.same(places[n], 'Hub')]
        record = {'Hub_X_rank':rank(hub), 'held_X':held}
        if name in ('cached_source_aggregate_cut','four_actual_proper_imports_at_I',
                    'actual_canonical36_at_ground_with_D4_retained_at_I'):
            assert tuple(held) == held_names, ('held roster',name)
            d = [values[n] for n in held_names]
            assert rank(hub) == 440 and rank(hub+d) == 444 and rank(d) == 4
            assert 36+rank(hub)-rank(hub+cspace) == 32
            assert 36+rank(d)-rank(d+cspace) == 0
            assert all(values[n] == initial[n] and geo.same(places[n], 'zero')
                       for n in initial if n.startswith('Y')), ('early Y use',name)
            for t in range(4):
                for k in range(2):
                    target = f'A{t}_{k}' if t < 2 else held_names[2*(t-2)+k]
                    assert values[target] == expected[t][k], ('MDS aggregate',name,t,k)
                    assert geo.same(places[target], f'C{t}')
            record.update(Hub_canonical_intersection=32,held_canonical_intersection=0)
        if name == 'four_actual_proper_imports_at_I':
            assert all(geo.same(places[f'D{j}'],'I') and values[f'D{j}'] == values[n]
                       for j,n in enumerate(held_names))
        if name == 'actual_canonical36_at_ground_with_D4_retained_at_I':
            for q, i in enumerate(basis_roles):
                for k in range(4):
                    p = f'P{q}_{k}'
                    assert geo.same(places[p], 'zero') and values[p] == canonical[i,k]
            assert rank(completed_seeds) == 36
            assert rank(transport) == 40
            assert rank(all_partial) == 444
            assert rank([values[f'P{q}_{k}'] for q in range(9) for k in range(4)]
                        +[values[f'D{j}'] for j in range(4)]) == 40
            record.update(ground_canonical_rank=36,completed_Hub_seed_rank=36,
                          completed_seed_transport_rank=40,literal_partial_history_rank=444)
        if name == 'original_local_correction_completed_sources_not_yet_restored':
            for k in range(4):
                assert values[f'Y3_{k}'] == initial[f'Y3_{k}'] ^ initial[f'X3_{k}']
            record['actual_four_copy_receiver3_completed'] = True
        observations[name] = record

    for step, op in enumerate(word['operations']):
        capture(step)
        tag, name, *arg = op
        count[tag] += 1
        if tag == 'INIT':
            assert name not in born and name not in values, ('owner birth',step,op)
            assert arg[0] in geo.bases
            born.add(name); owners.add(name); values[name]=0; places[name]=arg[0]
        elif tag == 'ADD':
            dst = arg[0]
            assert name != dst and name in values and dst in values, ('ADD liveness',step,op)
            assert geo.same(places[name], places[dst]), ('ADD chart',step,op,places[name],places[dst])
            values[dst] ^= values[name]
            if dst.startswith('P'):
                all_partial.append(values[dst])
                if not geo.same(places[dst], 'Hub'):
                    transport.append(values[dst])
        elif tag == 'MOVE':
            assert name in values and arg[0] in geo.bases, ('MOVE liveness',step,op)
            before, after = places[name], arg[0]
            assert geo.sub(after,before) if name in owners else geo.sub(before,after), ('MOVE direction',step,op,before)
            gap = abs(geo.dim(after)-geo.dim(before))
            assert gap > 0, ('zero MOVE',step,op)
            profile[gap] += 1
            if name.startswith('P'):
                all_partial.append(values[name]); transport.append(values[name])
                if geo.same(before,'Hub'):
                    assert name not in seed_departures
                    completed_seeds.append(values[name]); seed_departures[name]=values[name]
            places[name] = after
        elif tag == 'CLEAR':
            assert name in owners, ('CLEAR liveness',step,op)
            dirty += bool(values[name])
            owners.remove(name); del values[name]; del places[name]
        else:
            raise AssertionError(('unknown',op))
    capture(len(word['operations']))
    assert not owners, ('unretired', sorted(owners))
    for j in range(111):
        for k in range(4):
            x,y=f'X{j}_{k}',f'Y{j}_{k}'
            assert values[x] == initial[x] and geo.same(places[x],'Hub'), ('X endpoint',x)
            target = initial[y] ^ (initial[x] if j == 3 else 0)
            assert values[y] == target and geo.same(places[y],f'F{j}'), ('Y endpoint',y)
    if strict_invoice:
        assert count == Counter(INIT=44,ADD=4181,MOVE=1204,CLEAR=44)
        assert profile == Counter({1:16,2:228,3:36,5:268,6:4,7:652}) and dirty == 44
    return {'counts':dict(count),'profile':dict(sorted(profile.items())),
            'dirty_clears':dirty,'observations':observations,
            'completed_seed_rank':rank(completed_seeds),'transport_rank':rank(transport),
            'all_partial_history_rank':rank(all_partial),'columns':888,
            'actual_completed_roles':[3],'physical_binary_copies':4}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA
    roots=json.loads(raw)['native_roots'];word=json.loads((a.source/'WORD.json').read_text())
    geo=Geometry(word['charts'])
    for j,r in enumerate(roots):
        assert word['charts'][f'L{j}']=={'kind':'span','rows':[r]}
        assert word['charts'][f'F{j}']=={'kind':'ann','rows':[r]}
    assert word['charts']['I']=={'kind':'ann','rows':[roots[3],roots[91],roots[96]]}
    assert geo.dim('I')==5 and geo.sub('I','C2') and geo.sub('I','C3')
    out={'status':'INDEPENDENT_LITERAL_CANONICAL_MDS_CHRONOLOGY_PASS','source_word_sha256':hashlib.sha256((a.source/'WORD.json').read_bytes()).hexdigest(),
         'source_proof_sha256':hashlib.sha256((a.source/'PROOF.md').read_bytes()).hexdigest(),
         'native_sha256':ROOT_SHA,'word':replay(word,roots,geo),'negative_controls':[]}
    def mutate(label, fn, geometry=False):
        bad=copy.deepcopy(word);fn(bad)
        try:
            replay(bad,roots,Geometry(bad['charts']) if geometry else geo,milestones=False,strict_invoice=False)
        except (AssertionError,KeyError) as e:
            out['negative_controls'].append({'name':label,'rejected':True,'reason':str(e)[:180]})
        else:
            raise AssertionError(('mutant accepted',label))
    def change_first(w,pred,replace):
        i=next(i for i,o in enumerate(w['operations']) if pred(o));w['operations'][i]=replace(w['operations'][i])
    mutate('wrong_held_binary_bank',lambda w:change_first(w,lambda o:o==['ADD','X1_2','D0'],lambda o:['ADD','X1_3','D0']))
    mutate('wrong_canonical_patch_bank',lambda w:change_first(w,lambda o:o[0]=='ADD' and o[1]=='D0' and o[2].startswith('P'),lambda o:['ADD','D1',o[2]]))
    mutate('wrong_Hub_seed_source_bank',lambda w:change_first(w,lambda o:o[0]=='ADD' and o[1]=='X0_0' and o[2]=='P0_0',lambda o:['ADD','X0_1',o[2]]))
    mutate('no_proper_common_descent',lambda w:change_first(w,lambda o:o==['MOVE','D0','I'],lambda o:['MOVE','D0','zero']))
    mutate('preload_wrong_receiver',lambda w:change_first(w,lambda o:o==['ADD','P0_0','Y3_0'],lambda o:['ADD','P0_0','Y4_0']))
    mutate('swap_stationary_anchor_bank',lambda w:change_first(w,lambda o:o==['ADD','A0_0','Y3_0'],lambda o:['ADD','A0_1','Y3_0']))
    def premature(w):
        i=next(i for i,o in enumerate(w['operations']) if o==['ADD','P0_0','Y3_0'])
        j=next(j for j,o in enumerate(w['operations']) if o[0]=='MOVE' and o[1]=='Y3_0')
        move=w['operations'].pop(j);w['operations'].insert(i,move)
    mutate('Y_leaves_before_canonical_read',premature)
    mutate('wrong_patch_chart',lambda w:w['charts'].__setitem__('I',{'kind':'ann','rows':[roots[3],roots[91],roots[0]]}),True)
    def omit_inverse(w):
        i=max(i for i,o in enumerate(w['operations']) if o[0]=='ADD' and o[1].startswith('X') and o[2].startswith('X'))
        w['operations'].pop(i)
    mutate('missing_actual_source_inverse',omit_inverse)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['word']['counts'],len(out['negative_controls']))


if __name__=='__main__':
    main()
