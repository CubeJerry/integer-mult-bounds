#!/usr/bin/env python3
"""Independent actual-source and endpoint review of the cyclic import exchange."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from decimal import Decimal, localcontext
import argparse, copy, hashlib, importlib.util, json

BASE = '6c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9'
WORD = '47cb0991e41d06efae453f0e2890af6f619ccc44109b46329749bee658a18d15'
MARK = ['ADD', 'CAP46', 'P3']
COPIES = [('Q1', 'C1', 'F74', 'Q1_F74'),
          ('Q3', 'C3', 'F4', 'Q3_F4'),
          ('Q4', 'C4', 'F78', 'Q4_F78')]
E = [8, 9, 19, 20, 36, 37]
SCALE = 10**40

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    s = importlib.util.spec_from_file_location('independent_replay', path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

@lru_cache(None)
def power_bounds(d):
    """Bisection with exact integer powers, distinct from author root routine."""
    if d == 1: return Fraction(1), Fraction(1)
    n = d**199 * SCALE**200
    lo, hi = 0, (d+1)*SCALE
    while hi-lo > 1:
        mid = (lo+hi)//2
        if mid**200 <= n: lo = mid
        else: hi = mid
    assert lo**200 <= n < (lo+1)**200
    return Fraction(lo, SCALE), Fraction(lo+1, SCALE)

def moment(profile):
    low = high = Fraction(0)
    for d, count in profile.items():
        a, b = power_bounds(int(d))
        low += count*(a if count >= 0 else b)
        high += count*(b if count >= 0 else a)
    return low, high

def display(x):
    with localcontext() as ctx:
        ctx.prec = 55
        return {'lower_fraction': str(x[0]), 'upper_fraction': str(x[1]),
                'lower': str(Decimal(x[0].numerator)/Decimal(x[0].denominator)),
                'upper': str(Decimal(x[1].numerator)/Decimal(x[1].denominator))}

def observe(w):
    values = {f'X{i}': 1<<i for i in range(111)}
    values.update({f'Y{i}': 1<<(111+i) for i in range(111)})
    charts = {f'X{i}': f'L{i}' for i in range(111)}
    charts.update({f'Y{i}': 'zero' for i in range(111)})
    captures = []; snapshot = None
    for k, op in enumerate(w['operations'], 1):
        if op == MARK:
            assert snapshot is None
            snapshot = {'step': k, 'values': values.copy(), 'charts': charts.copy()}
        kind, name, *args = op
        if kind == 'INIT': values[name] = 0; charts[name] = args[0]
        elif kind == 'ADD':
            dest = args[0]
            if dest in {t[3] for t in COPIES} | {f'IMPORT_E{i}' for i in [8,9,36]}:
                captures.append({'step': k, 'source': name, 'destination': dest,
                                 'source_chart': charts[name], 'destination_chart': charts[dest],
                                 'source_row_hex': hex(values[name])})
            values[dest] ^= values[name]
        elif kind == 'MOVE': charts[name] = args[0]
        elif kind == 'CLEAR': del values[name], charts[name]
    assert snapshot is not None
    return snapshot, captures

def inventory(snap, C):
    return {n: r for n, r in snap['values'].items() if n != 'P3'
            and r>>111 == 0 and C[snap['charts'][n]] == C['M1']}

def outsider_dual(rows, i):
    equations = {}
    for row, rhs in [(r,0) for r in rows]+[(1<<i,1)]:
        while row:
            pivot=row.bit_length()-1
            if pivot in equations:
                previous, value=equations[pivot]; row^=previous; rhs^=value
            else:
                equations[pivot]=(row,rhs); break
        assert row or rhs==0
    witness=0
    for pivot,(row,rhs) in sorted(equations.items()):
        if ((row&witness).bit_count()%2)^rhs: witness|=1<<pivot
    assert witness>>i&1
    assert all((row&witness).bit_count()%2==0 for row in rows)
    return witness

def main():
    p = argparse.ArgumentParser()
    for name in ['repo','base','word','author-result','engine','out']:
        p.add_argument('--'+name, type=Path, required=True)
    a = p.parse_args()
    assert sha(a.base) == BASE and sha(a.word) == WORD
    old, w = json.loads(a.base.read_text()), json.loads(a.word.read_text())
    assert w['base_word_sha256'] == BASE and w['targets'] == old['targets']
    assert w['source_path'] == old['source_path'] and w['source_sha256'] == old['source_sha256']
    raw = (a.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == w['source_sha256']
    roots = json.loads(raw)['native_roots']; e = load(a.engine)
    C0, H0, report0 = e.replay(old, roots); C, H, report = e.replay(w, roots)
    before, _ = observe(old); after, captures = observe(w)
    v0, c0 = before['values'], before['charts']; v, c = after['values'], after['charts']
    inv0, inv = inventory(before,C0), inventory(after,C)
    assert v['P3'] == 0 and c['P3'] == 'M1'
    assert len(captures) == 30
    capture_facts = []
    for q, old_chart, facet, field in COPIES:
        assert c0[q] == 'M1' and c[q] == old_chart and c[field] == facet
        assert v0[q] == v[q] == v[field]
        assert q not in inv and q in inv0
        assert e.sub(C[old_chart],C[facet]) and len(C[old_chart]) == 6 and len(C[facet]) == 7
        assert [o for o in w['operations'] if o[0]=='MOVE' and o[1]==field] == []
        cohort = [o[1] for o in old['operations'] if o[0]=='ADD' and o[2]==q]
        copied = [r for r in captures if r['destination']==field]
        assert [r['source'] for r in copied] == cohort
        for r in copied:
            j = int(r['source'][1:]); assert int(r['source_row_hex'],16) == 1<<j
            assert r['source_chart'] == r['destination_chart'] == facet
        capture_facts.append({'old_cache':q,'actual_retained_chart':old_chart,
                              'stationary_copy':field,'copy_chart':facet,
                              'cohort':cohort,'equal_actual_row_hex':hex(v[q])})
    for i in [8,9,36]:
        field=f'IMPORT_E{i}'; assert inv[field] == 1<<i
        events=[r for r in captures if r['destination']==field]; assert len(events)==1
        r=events[0]; assert r['source_chart']==r['destination_chart']=='Extra6'
        assert int(r['source_row_hex'],16)==1<<i
        assert e.sub(C[f'L{i}'],C['Extra6']) and e.sub(C['M1'],C['Extra6'])
    assert len(e.bb(inv0.values())) == len(e.bb(inv.values())) == 11
    emask=sum(1<<i for i in E)
    assert len(e.bb(r&emask for r in inv0.values()))==0
    assert len(e.bb(r&emask for r in inv.values()))==3
    owner0={o[1] for o in old['operations'] if o[0]=='INIT'}
    owner={o[1] for o in w['operations'] if o[0]=='INIT'}
    moves0=Counter(tuple(o) for o in old['operations'] if o[0]=='MOVE' and o[1] in owner0)
    moves=Counter(tuple(o) for o in w['operations'] if o[0]=='MOVE' and o[1] in owner)
    assert moves0-moves == Counter({('MOVE',q,'M1'):1 for q in ['Q1','Q3','Q4']})
    assert moves-moves0 == Counter({('MOVE',f'IMPORT_E{i}','M1'):1 for i in [8,9,36]})
    assert sum(moves.values())==sum(moves0.values())==53
    assert report['counts']=={'INIT':124,'ADD':828,'MOVE':483,'CLEAR':124}
    assert report['dirty_CLEAR']==124
    delta={d:report['movement_profile'].get(d,0)-report0['movement_profile'].get(d,0)
           for d in set(report['movement_profile'])|set(report0['movement_profile'])}
    delta={d:n for d,n in delta.items() if n}; assert delta=={1:60,2:-27,5:3,7:-3}
    Q=moment(report['movement_profile']); B={127:37,64:74,1:-74}
    for j in range(1,9): B[1+7*j]=B.get(1+7*j,0)+74; B[7*j]=B.get(7*j,0)-74
    allowance=tuple(x/6 for x in moment(B)); room=(allowance[0]-Q[1],allowance[1]-Q[0])
    price={'moment':Q,'limiting_allowance':allowance,'limiting_room':room,'increment':moment(delta)}
    author=json.loads(a.author_result.read_text())
    for label,bounds in price.items():
        claimed=author['price'][label]
        assert Fraction(claimed['lower_fraction']) <= bounds[0] <= bounds[1] <= Fraction(claimed['upper_fraction'])
    controls=[]
    essential=[['ADD','X60','Q1_F74'],['ADD','X59','Q3_F4'],['ADD','X13','Q4_F78'],
               ['MOVE','Y4','C1'],['ADD','Q1','Y4'],['ADD','Q3_F4','Y4'],
               ['ADD','Q1_F74','Y74'],['ADD','Q4_F78','Y78'],['CLEAR','Q4_F78']]
    for op in essential:
        bad=copy.deepcopy(w); bad['operations'].remove(op)
        try: e.replay(bad,roots)
        except (AssertionError,KeyError) as ex: controls.append({'removed':op,'rejected':str(ex)})
        else: raise AssertionError(('Essential omission accepted',op))
    source_controls=[]
    for i in [8,9,36]:
        field=f'IMPORT_E{i}'
        for op in [['ADD',f'X{i}',field],['MOVE',field,'M1']]:
            bad=copy.deepcopy(w); bad['operations'].remove(op); e.replay(bad,roots)
            snap,_=observe(bad); badinv=inventory(snap,C)
            assert badinv.get(field)!=1<<i
            source_controls.append({'removed':op,'old41_endpoints_pass':True,
                                    'actual_import_contract_fails':True})
        probe=copy.deepcopy(w); ix=probe['operations'].index(MARK)
        probe['operations'][ix:ix]=[['ADD',field,'P3'],['ADD',field,'P3']]
        e.replay(probe,roots)
        bad=copy.deepcopy(probe); bad['operations'].remove(['MOVE',field,'M1'])
        try: e.replay(bad,roots)
        except AssertionError: pass
        else: raise AssertionError(('Nonlocal source probe accepted',field))
    removed=copy.deepcopy(w); names={f'IMPORT_E{i}' for i in [8,9,36]}
    removed['operations']=[o for o in removed['operations'] if not any(n in names for n in o[1:])]
    e.replay(removed,roots); empty,_=observe(removed); emptyinv=inventory(empty,C)
    assert len(e.bb(r&emask for r in emptyinv.values()))==0
    xmask=(1<<111)-1; known=set(w['targets']); observation=[]
    for i in range(111):
        rows=[r&xmask for _,_,chart,r in H if e.sub(C[chart],C[f'F{i}'])]
        rows += [1<<j for j in range(111) if sum(x*y for x,y in zip(roots[i],roots[j]))==0]
        observation.append(rows)
    waves=[]
    while True:
        nxt={i for i,rows in enumerate(observation) if e.fits(rows+[1<<j for j in known],1<<i)}
        assert known<=nxt
        if nxt==known: break
        waves.append(sorted(nxt-known)); known=nxt
    duals=[{'receiver':i,'dual_hex':hex(outsider_dual(rows+[1<<j for j in known],i))}
           for i,rows in enumerate(observation) if i not in known]
    out={'status':'PASS_INDEPENDENT_CYCLIC_IMPORT_SOURCE_AND_ENDPOINT_REVIEW',
         'word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],
         'before':report0,'after':report,'source_cut_step':after['step'],
         'actual_M1_inventory_before':{n:hex(r) for n,r in inv0.items()},
         'actual_M1_inventory_after':{n:hex(r) for n,r in inv.items()},
         'M1_rank_before':11,'M1_rank_after':11,'full_E_projection_rank_before':0,'full_E_projection_rank_after':3,
         'stationary_cache_custody':capture_facts,'all_30_actual_raw_capture_events':captures,
         'owned_moves_before':53,'owned_moves_after':53,'owned_move_exchange_exact':True,
         'exact_profile_difference':delta,'price_method':'Exact integer bisection at scale 10^40 for every 200th root',
         'price':{k:display(z) for k,z in price.items()},'independent_tighter_price_intervals_inside_author_bounds':True,
         'semantic_omission_controls':controls,'source_interface_controls':source_controls,
         'three_legal_query_unquery_probes_pass':True,'all_imports_removed_endpoint_control_passes_with_E_rank_zero':True,
         'fresh_all_record_Xparts_raw_local_feedback_closure':sorted(known),'fresh_feedback_waves':waves,
         'fresh_all_history_outsider_duals':duals,
         'scope':'41 completed endpoints preserved. Three actual independent source directions delivered to M1 in exchange for three removed Q directions; no new complete output, all111 supplier, or inherited frozen-bank claim.'}
    a.out.mkdir(parents=True,exist_ok=True); (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','after','M1_rank_after','full_E_projection_rank_after','price','fresh_feedback_waves']}))

if __name__=='__main__': main()
