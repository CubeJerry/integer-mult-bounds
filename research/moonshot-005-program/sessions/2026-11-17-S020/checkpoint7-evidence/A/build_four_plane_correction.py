"""Actual quartet correction on four coupled query planes; all222 columns.

The two Y couriers retain arbitrary baselines. Their X garbage is actually
removed at the quartet, and the initial two triangular Y preloads cancel all
baseline cross-terms. No Y-dependent value is ever added to an original X.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE, SHA, HELPER, CHECK, module


def replay_general(word, roots, geometry):
    charts = {n: geometry.chart(c) for n, c in word['charts'].items()}
    v = {f'X{i}': 1 << i for i in range(111)} | {f'Y{i}': 1 << (111+i) for i in range(111)}
    at = {f'X{i}': f'L{i}' for i in range(111)} | {f'Y{i}': 'zero' for i in range(111)}
    owners = set(); born = set(); counts = Counter(); profile = Counter(); peak = dirty = 0
    cut_values = cut_places = None
    for k, op in enumerate(word['operations']):
        if k == word['carrier_interface_before_operation']:
            cut_values, cut_places = dict(v), dict(at)
        kind, name, *args = op; counts[kind] += 1
        if kind == 'INIT':
            assert name not in v and name not in born
            v[name] = 0; at[name] = args[0]; owners.add(name); born.add(name)
        elif kind == 'ADD':
            dest = args[0]
            assert charts[at[name]] == charts[at[dest]], (k, op, 'cochart')
            v[dest] ^= v[name]
        elif kind == 'MOVE':
            before, after = charts[at[name]], charts[args[0]]
            assert geometry.sub(after, before) if name in owners else geometry.sub(before, after), (k, op, 'nested')
            gap = abs(len(before)-len(after)); assert gap > 0, (k, op, 'positive')
            profile[gap] += 1; at[name] = args[0]
        elif kind == 'CLEAR':
            assert name in owners
            dirty += bool(v[name]); owners.remove(name); del v[name], at[name]
        else:
            raise AssertionError(op)
        peak = max(peak, len(owners))
    assert cut_values is not None and not owners and len(v) == 222
    for i in range(111):
        assert v[f'X{i}'] == 1 << i and at[f'X{i}'] == 'Hub', (i, 'X endpoint')
        expected = (1 << (111+i)) ^ int(word['Y_correction_rows_hex'][i], 16)
        assert v[f'Y{i}'] == expected and at[f'Y{i}'] == f'F{i}', (i, 'Y endpoint')
    return charts, cut_values, cut_places, {'input_columns': 222, 'counts': dict(counts),
        'movement_profile': dict(sorted(profile.items())), 'dirty_CLEAR': dirty, 'peak_owned': peak}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True); args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    helper = module(args.repo/HELPER, 'four_plane_helpers'); geometry = module(args.repo/CHECK, 'four_plane_geometry')
    raw = (args.repo/SOURCE).read_bytes(); assert hashlib.sha256(raw).hexdigest() == SHA
    roots = json.loads(raw)['native_roots']; support = [0, 1, 6, 7]; a, b, c, d = support
    signs = [i for i, r in enumerate(roots) if [j for j, x in enumerate(r) if x] == support]
    assert len(signs) == 8
    sources = sorted(support+signs); couriers = [2, 3]
    E = [[int(i == j) for j in range(8)] for i in range(8)]
    charts = {'zero': {'kind': 'span', 'rows': []}, 'Hub': {'kind': 'span', 'rows': E},
              'G': {'kind': 'span', 'rows': [E[i] for i in support]}}
    for i, r in enumerate(roots):
        charts[f'L{i}'] = {'kind': 'span', 'rows': [r]}
        charts[f'F{i}'] = {'kind': 'ann', 'rows': [r]}
    query_roles = {}; query_rows = {}; pairs = {}
    for s in [1, -1]:
        A = f'A{s}'; B = f'B{s}'
        AI = [i for i in signs if roots[i][a] == s*roots[i][b]]
        BI = [i for i in signs if roots[i][c] == s*roots[i][d]]
        charts[A] = {'kind': 'span', 'rows': [roots[i] for i in AI]+[E[c], E[d]]}
        charts[B] = {'kind': 'span', 'rows': [roots[i] for i in BI]+[E[a], E[b]]}
        query_roles[A] = [i for i, r in enumerate(roots) if [j for j in support if r[j]] == [a,b]
                          and r[a] == -s*r[b]]
        query_roles[B] = [i for i, r in enumerate(roots) if [j for j in support if r[j]] == [c,d]
                          and r[c] == -s*r[d]]
        query_rows[A] = sum(1 << i for i in AI+[c,d])
        query_rows[B] = sum(1 << i for i in BI+[a,b])
        for t in [1,-1]:
            I = [i for i in signs if roots[i][a] == s*roots[i][b] and roots[i][c] == t*roots[i][d]]
            assert len(I) == 2
            P = f'PAIR_{s}_{t}'; charts[P] = {'kind': 'span', 'rows': [roots[i] for i in I]}
            early = A if s == t else f'B{t}'
            late = f'B{t}' if s == t else A
            pairs[P] = {'roles': I, 'early': early, 'late': late}
    served = sorted(i for I in query_roles.values() for i in I)
    assert len(served) == len(set(served)) == 29 and not set(served) & set(couriers)
    charts['AXIS_AB'] = {'kind': 'span', 'rows': [E[a], E[b]]}
    charts['AXIS_CD'] = {'kind': 'span', 'rows': [E[c], E[d]]}
    ops = []; sem = defaultdict(list); owners = []; values = {f'X{i}':1 << i for i in range(111)} | {f'Y{i}':1 << (111+i) for i in range(111)}
    at = {f'X{i}':f'L{i}' for i in range(111)} | {f'Y{i}':'zero' for i in range(111)}
    def emit(op, key):
        sem[key].append(len(ops)); ops.append(op); kind, n, *q = op
        if kind == 'INIT': values[n] = 0; at[n] = q[0]; owners.append(n)
        elif kind == 'ADD': values[q[0]] ^= values[n]
        elif kind == 'MOVE': at[n] = q[0]
        elif kind == 'CLEAR': del values[n], at[n]; owners.remove(n)
    def add(x,y,key): emit(['ADD',x,y],key)
    def move(x,p,key): emit(['MOVE',x,p],key)
    for i in range(111):
        emit(['INIT',f'NATIVE_{i}',f'L{i}'],'native_cache_birth')
        add(f'X{i}',f'NATIVE_{i}','native_capture')
    # The only Y-to-Y dependencies are known in advance and inverted at ground.
    for q, courier in [('A-1',couriers[0]),('B-1',couriers[1])]:
        for i in query_roles[q]: add(f'Y{courier}',f'Y{i}','ground_Y_inverse')
    inverse = []
    # Disjoint source pairs; orient the query incidence four-cycle.
    for P, info in pairs.items():
        x, y = info['roles']; early, late = info['early'], info['late']
        move(f'X{x}',P,'sign_pair_arrival'); move(f'X{y}',P,'sign_pair_arrival')
        add(f'X{y}',f'X{x}','sign_pair_encode'); inverse.append((x,y))
        for i in query_roles[early]:
            move(f'Y{i}',P,'query_early_arrival'); add(f'X{x}',f'Y{i}','early_pair_read')
        move(f'X{y}','G','raw_pair_donor_return')
        move(f'X{x}',late,'late_pair_carrier_arrival')
    # Each axis pair supplies one query plane directly and the opposite one via Y.
    axis_data = [('AXIS_CD',c,d,'A1','A-1',couriers[0]),('AXIS_AB',a,b,'B1','B-1',couriers[1])]
    for P, x, y, direct, courier_dest, courier in axis_data:
        move(f'X{x}',P,'axis_pair_arrival'); move(f'X{y}',P,'axis_pair_arrival')
        add(f'X{y}',f'X{x}','axis_pair_encode'); inverse.append((x,y))
        move(f'Y{courier}',P,'axis_courier_arrival'); add(f'X{x}',f'Y{courier}','axis_courier_load')
        move(f'Y{courier}',courier_dest,'axis_courier_delivery')
        move(f'X{y}','G','raw_axis_donor_return'); move(f'X{x}',direct,'axis_carrier_delivery')
    for q, I in query_roles.items():
        pair_carrier = next(info['roles'][0] for info in pairs.values() if info['late'] == q)
        axis_source = f'X{c}' if q == 'A1' else f'X{a}' if q == 'B1' else f'Y{couriers[0]}' if q == 'A-1' else f'Y{couriers[1]}'
        for i in I:
            move(f'Y{i}',q,'query_plane_arrival')
            add(f'X{pair_carrier}',f'Y{i}','late_pair_read'); add(axis_source,f'Y{i}','axis_sum_read')
            assert values[f'Y{i}'] == (1 << (111+i)) ^ query_rows[q]
    for x, y in inverse:
        move(f'X{x}','G','encoded_original_return')
    for x, y in reversed(inverse): add(f'X{y}',f'X{x}','original_inverse')
    for P, x, y, direct, courier_dest, courier in axis_data:
        move(f'Y{courier}','G','courier_cleanup_arrival')
        add(f'X{x}',f'Y{courier}','courier_actual_cleanup'); add(f'X{y}',f'Y{courier}','courier_actual_cleanup')
        assert values[f'Y{courier}'] == 1 << (111+ courier)
    assert all(values[f'X{i}'] == 1 << i for i in range(111))
    cut = len(ops)
    expected = [0] * 111
    for q, I in query_roles.items():
        for i in I: expected[i] = query_rows[q]
    for i in range(111): move(f'X{i}','Hub','public_X_endpoint')
    for i in range(111): move(f'Y{i}',f'F{i}','public_Y_endpoint')
    for n in list(owners): emit(['CLEAR',n],'native_cache_retirement')
    word = {'schema':'quartet-four-query-plane-correction-v1','source_path':SOURCE,'source_sha256':SHA,
            'charts':charts,'operations':ops,'carrier_interface_before_operation':cut,
            'Y_correction_rows_hex':list(map(hex,expected)),
            'construction':{'quartet_support':support,'sign_roles':signs,'source_roles':sources,
                            'courier_Y_roles':couriers,'query_roles':query_roles,
                            'query_rows_hex':{k:hex(v) for k,v in query_rows.items()},'oriented_pairs':pairs,
                            'served_receivers':served},
            'semantic_operation_indices':dict(sem),
            'scope':'Actual four-plane foreign-correction gadget for29 receivers, with all111 native caches, all222 public columns, all X and courier Y restored. No diagonal output or complete supplier.'}
    C, cv, ca, stats = replay_general(word,roots,geometry)
    assert stats['movement_profile'] == {1:57,2:37,3:2,4:41,7:179}
    q = helper.moment(stats['movement_profile']); gate = {127:37,64:74,1:-74}
    for j in range(1,9): gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling = tuple(x/6 for x in helper.moment(gate))
    pin = helper.save(args.out/'WORD.json',word)
    helper.save(args.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,
        'fields':[{'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(v)} for n,v in sorted(cv.items())]})
    controls=[]
    for key in ['ground_Y_inverse','sign_pair_encode','early_pair_read','late_pair_read','axis_sum_read','original_inverse','courier_actual_cleanup']:
        alt=json.loads(json.dumps(word)); index=alt['semantic_operation_indices'][key][0]; del alt['operations'][index]
        alt['carrier_interface_before_operation']-=1
        try: replay_general(alt,roots,geometry)
        except AssertionError: controls.append(key)
        else: raise AssertionError(('negative control accepted',key))
    result={'status':'PASS_ACTUAL_FOUR_QUERY_PLANE_CORRECTION','word_sha256':pin,'source_cut':cut,
            'source_roles':sources,'served_receivers':served,'served_count':len(served),'foreign_terms_per_served_receiver':6,
            'query_population':{k:len(v) for k,v in query_roles.items()},'stats':stats,'moment':helper.record(q),
            'necessary_limiting_room':helper.record((ceiling[0]-q[1],ceiling[1]-q[0])),
            'negative_controls':controls,'scope':word['scope']}
    helper.save(args.out/'RESULT.json',result); print(json.dumps(result,indent=2))


if __name__ == '__main__': main()
