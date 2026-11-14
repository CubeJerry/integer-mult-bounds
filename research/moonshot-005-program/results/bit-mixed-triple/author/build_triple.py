#!/usr/bin/env python3
"""Triple mixed-Y preload and three zero-through packet exchanges.

Extends frozen joint builder 8ba6e02ab8f93321980e11a8c3c6e8202b7f54b57e9c60481cd3de784c443f18.
Extends the mixed-Y two-ADD exchange by a cyclic three-receiver acquisition schedule.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def rref(rows):
    a = [[F(x) for x in r] for r in rows]
    p = 0
    for c in range(8):
        q = next((i for i in range(p, len(a)) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        scale = a[p][c]
        a[p] = [x/scale for x in a[p]]
        for j in range(len(a)):
            if j != p:
                scale = a[j][c]
                a[j] = [x-scale*y for x, y in zip(a[j], a[p])]
        p += 1
    return tuple(tuple(row) for row in a[:p])


def perpendicular(basis):
    b = rref(basis)
    pivots = [next(i for i, x in enumerate(row) if x) for row in b]
    out = []
    for f in range(8):
        if f in pivots:
            continue
        v = [F(0)]*8
        v[f] = 1
        for p, row in zip(pivots, b):
            v[p] = -row[f]
        out.append(v)
    return rref(out)


def included(a, b):
    return len(rref(list(a)+list(b))) == len(b)


def encode_basis(basis):
    return [[int(x) if x.denominator == 1 else str(x) for x in row] for row in basis]


def replay(word):
    frames = {int(c): f for c, f in word['frames'].items()}
    spaces = {c: rref(f['B']) for c, f in frames.items()}
    for c, f in frames.items():
        need(len(spaces[c]) == f['dim'], ('chart rank', c))
        a = rref(f['A'])
        need(len(a)+len(spaces[c]) == 8 and all(dot(x, y) == 0 for x in a for y in spaces[c]),
             ('chart orthogonal complement', c))
    where = dict(enumerate(word['start']))
    rows = {i: 1 << i for i in range(222)}
    counts = Counter()
    paid = Counter()
    lifetimes = peak = 0
    clears = []
    snapshots = {}
    selected = set(word.get('snapshot_indices', []))
    move_pairs = set()
    routes = {i: [where[i]] for i in rows}
    for n, op in enumerate(word['program']):
        kind, a = op[:2]
        counts[kind] += 1
        if kind == 'INIT':
            need(a >= 222 and a not in rows, ('zero-born owned field', n, op))
            rows[a], where[a] = 0, op[2]
            routes[a] = [op[2]]
            lifetimes += 1
            peak = max(peak, len(rows)-222)
        elif kind == 'ADD':
            _, a, b, c = op
            need(a != b and a in rows and b in rows and where[a] == where[b] == c,
                 ('cocharted active ADD', n, op))
            rows[a] ^= rows[b]
        elif kind == 'MOVE':
            _, a, c, d = op
            need(a in rows and where[a] == c, ('MOVE source', n, op))
            dc, dd = len(spaces[c]), len(spaces[d])
            need(abs(dc-dd) == 1, ('unit-rank MOVE', n, op))
            small, large = (spaces[c], spaces[d]) if dc < dd else (spaces[d], spaces[c])
            need(included(small, large), ('real chart inclusion', n, op))
            direction = word['directions'].get(str(a), 'up' if a < 222 else 'stationary')
            need((dd > dc if direction == 'up' else dd < dc if direction == 'down' else False), ('declared monotone direction', n, op))
            where[a] = d
            routes[a].append(d)
            paid[abs(dc-dd)] += 1
            move_pairs.add((c, d))
        elif kind == 'CLEAR':
            _, a, c = op
            need(a >= 222 and a in rows and where[a] == c, ('owned CLEAR', n, op))
            clears.append({'operation': n, 'field': a, 'chart': c, 'row_hex': hex(rows[a])})
            del rows[a]
            del where[a]
        else:
            raise ValueError(('unsupported operation', n, op))
        if n in selected:
            snapshots[str(n)] = {'rows': {str(i): hex(rows[i]) for i in (111, 112, 113, 222, 223, 224) if i in rows},
                                 'all_X_restored_at_Hub': all(rows[i] == 1 << i and where[i] == word['hub'] for i in range(111))}
    need(set(rows) == set(range(222)), 'all owned lifetimes retired')
    need([where[i] for i in range(222)] == word['final'], 'all public endpoint charts')
    return {'rows': [rows[i] for i in range(222)], 'counts': dict(counts),
            'paid_profile': dict(sorted(paid.items())), 'owned_lifetimes': lifetimes,
            'peak_owned': peak, 'clear_rows': clears, 'snapshots': snapshots,
            'routes': routes, 'exact_nested_move_pairs': len(move_pairs)}


def emit(native):
    frames = {int(c): f for c, f in native['frames'].items()}
    spaces = {c: rref(f['B']) for c, f in frames.items()}
    key_to_id = {b: c for c, b in spaces.items()}
    for c in native['start'][:222]+native['final'][:222]:
        key_to_id[spaces[c]] = c
    created = []
    eye = [tuple(F(i == j) for j in range(8)) for i in range(8)]
    hub, zero, f0 = native['final'][0], native['start'][111], native['final'][111]
    need((len(spaces[hub]), len(spaces[zero]), len(spaces[f0])) == (8, 0, 7), 'actual endpoint dimensions')

    def chart(basis):
        b = rref(basis)
        if b in key_to_id:
            return key_to_id[b]
        c = max(frames)+1
        frames[c] = {'dim': len(b), 'B': encode_basis(b), 'A': encode_basis(perpendicular(b))}
        spaces[c] = b
        key_to_id[b] = c
        created.append(c)
        return c

    ops = []
    where = dict(enumerate(native['start'][:222]))

    def unit_move(i, target, preferred=None):
        current = where[i]
        if current == target:
            return
        small, large = spaces[current], spaces[target]
        need(len(small) != len(large), ('no alias-only route', i, current, target))
        if len(small) < len(large):
            need(included(small, large), ('ascending route inclusion', i, current, target))
            candidates = ([preferred] if preferred is not None else [])+list(large)
            basis = small
            for v in candidates:
                nb = rref(list(basis)+[v])
                if len(nb) == len(basis):
                    continue
                need(included(nb, large), 'intermediate flag inside destination')
                nxt = target if len(nb) == len(large) else chart(nb)
                ops.append(['MOVE', i, current, nxt])
                current, basis = nxt, nb
            need(current == target, 'ascending flag completed')
        else:
            need(included(large, small), ('descending route inclusion', i, current, target))
            # Build the same increasing subspace flag and traverse it backward.
            basis = large
            ids = [target]
            for v in small:
                nb = rref(list(basis)+[v])
                if len(nb) == len(basis):
                    continue
                nxt = current if len(nb) == len(small) else chart(nb)
                ids.append(nxt)
                basis = nb
            need(ids[-1] == current, 'descending flag constructed')
            for nxt in reversed(ids[:-1]):
                ops.append(['MOVE', i, current, nxt])
                current = nxt
        where[i] = target

    def add(a, b, c):
        need(where.get(a) == where.get(b) == c and a != b, ('author cochart', a, b, c))
        ops.append(['ADD', a, b, c])
        return len(ops)-1

    def init(i, c):
        need(i not in where, 'new owned lifetime')
        ops.append(['INIT', i, c])
        where[i] = c
        return len(ops)-1

    def clear(i, c):
        need(where.get(i) == c, 'clear cochart')
        ops.append(['CLEAR', i, c])
        del where[i]

    roots = [[F(x) for x in native['frames'][str(native['start'][i])]['B'][0]] for i in range(111)]
    facets = native['final'][111:114]
    bridge = tuple(eye[0][j]+eye[1][j]+eye[2][j] for j in range(8))
    common_chart = chart(eye[3:8])
    groups = {mask: [j for j in range(8,111) if sum((roots[j][i]==0)<<i for i in range(3))==mask] for mask in range(8)}
    need([len(groups[m]) for m in range(8)] == [7,12,16,15,16,15,15,7], 'three-receiver exact source partition')
    for y in (111,112,113):
        unit_move(y, common_chart)
    acquired=[]
    snapshots=[]
    # The common input aggregate, including the five required coordinates,
    # uses original X3. Donors reach Hub before X3 is restored there.
    carrier=3
    donors=list(range(4,8))+groups[7]
    unit_move(carrier,common_chart)
    for j in donors:
        unit_move(j,common_chart)
        add(carrier,j,common_chart)
        unit_move(j,hub,preferred=bridge)
    reads=[add(y,carrier,common_chart) for y in (111,112,113)]
    snapshots.extend(reads)
    unit_move(carrier,hub,preferred=bridge)
    restores=[add(carrier,j,hub) for j in donors]
    acquired.append({'kind':'common','carrier':carrier,'donors':donors,'chart':common_chart,'deposit_operations':reads,'restoration_operations':restores})
    # Direct each triangle edge from the Y that reads its carrier at rank six
    # toward the Y that reads the same carrier later at its final facet.
    orientations=[(0,1),(1,2),(2,0)]
    parked=[]
    for i,j in orientations:
        c=chart([v for k,v in enumerate(eye) if k not in (i,j)])
        unit_move(111+i,c)
        k=3-i-j
        carrier=k
        donors=groups[(1<<i)|(1<<j)]
        unit_move(carrier,c)
        for d in donors:
            unit_move(d,c)
            add(carrier,d,c)
            unit_move(d,hub,preferred=bridge)
        first=add(111+i,carrier,c)
        unit_move(carrier,facets[j])
        parked.append({'kind':'pair','first_receiver':i,'second_receiver':j,'carrier':carrier,'donors':donors,'chart':c,'first_deposit_operation':first})
    # This phase boundary resolves the directed triangle: no Y needs to wait
    # for another Y to ascend before it can perform its first edge read.
    for i in range(3):
        unit_move(111+i,facets[i])
    for g in parked:
        carrier,j=g['carrier'],g['second_receiver']
        g['second_deposit_operation']=add(111+j,carrier,facets[j])
        unit_move(carrier,hub,preferred=bridge)
        g['restoration_operations']=[add(carrier,d,hub) for d in g['donors']]
        acquired.append(g)
    # The one-receiver remainder is local to the flat omitting i and 3.
    for i in range(3):
        indices=groups[1<<i]
        carrier=indices[0]
        donors=indices[1:]
        c=chart([v for k,v in enumerate(eye) if k not in (i,3)])
        need(all(included(spaces[native['start'][d]], spaces[c]) for d in indices),'exclusive source support')
        unit_move(carrier,c)
        for d in donors:
            unit_move(d,c)
            add(carrier,d,c)
            unit_move(d,hub,preferred=bridge)
        unit_move(carrier,facets[i])
        read=add(111+i,carrier,facets[i])
        unit_move(carrier,hub,preferred=bridge)
        restores=[add(carrier,d,hub) for d in donors]
        acquired.append({'kind':'exclusive','receiver':i,'carrier':carrier,'donors':donors,'chart':c,'deposit_operation':read,'restoration_operations':restores})
    for i in range(111):
        unit_move(i,hub,preferred=bridge)
    prefix=len(ops)-1
    snapshots.append(prefix)
    handoffs=[]
    for i in range(3):
        packet,facet=222+i,facets[i]
        canonical=[j for j in range(111) if j==i or dot(roots[j],roots[i])==0]
        foreign=[j for j in canonical if j!=i]
        birth=init(packet,hub)
        for j in canonical:
            add(packet,j,hub)
        ready=len(ops)-1
        unit_move(packet,facet)
        complete=add(111+i,packet,facet)
        reload=add(packet,111+i,facet)
        unit_move(packet,zero)
        ground=len(ops)-1
        clear(packet,zero)
        snapshots.extend([birth,ready,complete,reload,ground])
        handoffs.append({'coordinate':i,'packet':packet,'facet':facet,'packet_birth_operation':birth,
                         'packet_ready_snapshot':ready,'complete_Y_operation':complete,'reload_mixed_operation':reload,
                         'packet_ground_snapshot':ground,'canonical_row_hex':hex(sum(1<<j for j in canonical)),
                         'foreign_row_hex':hex(sum(1<<j for j in foreign)),
                         'mixed_preload_row_hex':hex((1<<(111+i))^sum(1<<j for j in foreign))})
    for i in range(3,111):
        unit_move(111+i,native['final'][111+i])
    used=set(native['start'][:222]+native['final'][:222])
    for op in ops:
        used.update(op[-2:] if op[0]=='MOVE' else [op[-1]])
    word={'schema':'BIT-triple-mixed-Y-preloads-zero-through-v1','public':222,'owned_fields':3,'hub':hub,
          'start':native['start'][:222],'final':native['final'][:222],
          'frames':{c:frames[c] for c in sorted(used)},'program':ops,
          'directions':{str(222+i):'down' for i in range(3)},'snapshot_indices':snapshots,
          'scope':'Actual scalar-F2 partial source. Three coordinate original Ys acquire y_i+K_i+x_i before packets; all111 X restore; three zero-through exchanges complete Y0,Y1,Y2. Other108 Y unchanged. No extra ascending mover. No complete source or kappa.'}
    metadata={'facets':facets,'common_chart':common_chart,'groups':acquired,'source_partition':groups,
              'orientations':orientations,'mixed_preloads_and_restored_X_snapshot':prefix,'handoffs':handoffs,
              'new_charts':[c for c in created if c in used]}
    return word,metadata


def main(args):
    raw=args.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'native exact source')
    native=json.loads(gzip.decompress(raw))
    word,metadata=emit(native)
    receipt=replay(word)
    expected=[1<<i for i in range(222)]
    for i in range(3):expected[111+i]^=1<<i
    need(receipt['rows']==expected,'all222 independent public input directions')
    need(receipt['paid_profile']=={1:1578},'three packet routes and no extra ascent')
    need(receipt['owned_lifetimes']==3 and receipt['peak_owned']==1,'only three sequential packet lifetimes')
    prefix=receipt['snapshots'][str(metadata['mixed_preloads_and_restored_X_snapshot'])]
    need(prefix['all_X_restored_at_Hub'],'all X restored before any packet')
    for h in metadata['handoffs']:
        y,p=111+h['coordinate'],h['packet']
        need(prefix['rows'][str(y)]==h['mixed_preload_row_hex'],'all mixed preloads acquired physically')
        need(receipt['snapshots'][str(h['complete_Y_operation'])]['rows'][str(y)]==hex(expected[y]),'receiver completed')
        need(receipt['snapshots'][str(h['reload_mixed_operation'])]['rows'][str(p)]==h['mixed_preload_row_hex'],'zero-through new packet value')
    need([c['row_hex'] for c in receipt['clear_rows']]==[h['mixed_preload_row_hex'] for h in metadata['handoffs']],'unknown-Y-bearing CLEAR values')
    controls=[]
    def without(index):
        bad=json.loads(json.dumps(word));del bad['program'][index];bad['snapshot_indices']=[];return bad
    omissions=[('omit_common_read',metadata['groups'][0]['deposit_operations'][0]),
               ('omit_common_restore',metadata['groups'][0]['restoration_operations'][0])]
    for g in metadata['groups'][1:4]:
        omissions.append(('omit_pair_first_'+str(g['first_receiver']),g['first_deposit_operation']))
        omissions.append(('omit_pair_second_'+str(g['second_receiver']),g['second_deposit_operation']))
        omissions.append(('omit_pair_restore_'+str(g['first_receiver']),g['restoration_operations'][0]))
    for g in metadata['groups'][4:]:omissions.append(('omit_exclusive_'+str(g['receiver']),g['deposit_operation']))
    for name,index in omissions:
        br=replay(without(index));wrong=[i for i,(a,b) in enumerate(zip(br['rows'],expected)) if a!=b]
        need(wrong,('semantic negative control',name));controls.append({'name':name,'rejected':True,'wrong_public_rows':wrong})
    for h in metadata['handoffs']:
        bad=json.loads(json.dumps(word));bad['snapshot_indices']=[]
        i,j=h['complete_Y_operation'],h['reload_mixed_operation'];bad['program'][i],bad['program'][j]=bad['program'][j],bad['program'][i]
        need(replay(bad)['rows']!=expected,'reverse exchange order')
        controls.append({'name':'reverse_exchange_order_'+str(h['coordinate']),'rejected':True})
    # Geometry control: move one Y directly to its facet before its first
    # pair read. The unchanged read then fails actual cocharting.
    g=metadata['groups'][1]
    bad=json.loads(json.dumps(word));bad['snapshot_indices']=[]
    idx=g['first_deposit_operation'];y=111+g['first_receiver'];c=g['chart'];f=metadata['facets'][g['first_receiver']]
    bad['program'].insert(idx,['MOVE',y,c,f])
    try:replay(bad)
    except ValueError:pass
    else:raise ValueError('early facet ascent negative control accepted')
    controls.append({'name':'early_facet_ascent_before_first_pair_read','rejected':True})
    visits={str(f):[i for i in range(111) if f in receipt['routes'][i]] for f in metadata['facets']}
    need(all(len(v)==2 for v in visits.values()),'two original-X facet arrivals per served receiver')
    args.output.mkdir(parents=True,exist_ok=True)
    data=json.dumps(word,separators=(',',':'),sort_keys=True).encode();zipped=gzip.compress(data,mtime=0)
    (args.output/'WORD.json.gz').write_bytes(zipped)
    receipt.pop('rows');receipt.pop('routes')
    result={'status':'PASS_ACTUAL_TRIPLE_MIXED_Y_ZERO_THROUGH_SOURCE','native_sha256':PIN,
            'builder_predecessor_sha256':'10c182a4998884037c607ac8c694a361ba0d7b4fc6e6afbc15119c317ba7ca1e',
            'word_sha256':hashlib.sha256(zipped).hexdigest(),'canonical_word_json_sha256':hashlib.sha256(data).hexdigest(),
            'metadata':metadata,'receipt':receipt,'negative_controls':controls,'original_X_facet_arrivals':visits,
            'completed_Y_indices':[0,1,2],'remaining_Y_indices':list(range(3,111)),
            'extra_upward_MOVEs':0,'pure_local_owned_caches':0,
            'hypothetical_eight_packet_profile_after_five_more_routes':{1:1618},
            'unknown_original_Y_in_packet_and_CLEAR':True,'complete_source_claimed':False,'complete_kappa_claimed':False,
            'scope':word['scope']}
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'counts':receipt['counts'],'paid_profile':receipt['paid_profile'],'peak_owned':receipt['peak_owned'],'facet_X_arrivals':visits,'negative_controls':len(controls)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
