#!/usr/bin/env python3
"""Geometry-only verification of the fixed-class native middle obstruction."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import gzip
import json

PINS = {
    'layout': '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
    'partitions': '2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25',
}

def read_pinned(path, key):
    data = gzip.decompress(path.read_bytes())
    assert sha256(data).hexdigest() == PINS[key]
    return json.loads(data)

def gf2_rank(rows):
    pivots = {}
    for v in rows:
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return len(pivots)

def main():
    ap = ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    base = args.repo / 'research/moonshot-005-program/results'
    layout = read_pinned(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz', 'layout')
    part = read_pinned(base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz', 'partitions')['classes']
    roots = layout['root_table']
    planes = [frozenset(v) for v in layout['A2']]
    middles = [frozenset(v) for v in layout['D4']]
    assert len(roots)==120 and len(planes)==1120 and len(middles)==3150
    assert len(set(planes))==1120 and len(set(middles))==3150
    assert all(len(x)==3 for x in planes) and all(len(x)==12 for x in middles)
    orth = [{j for j, v in enumerate(roots) if sum(a*b for a,b in zip(u,v))==0} for u in roots]
    duals = []
    lookup = {d:i for i,d in enumerate(middles)}
    for d, V in enumerate(middles):
        W = frozenset.intersection(*(frozenset(orth[j]) for j in V))
        assert W in lookup
        q = lookup[W]
        assert q == layout['dual_D4'][d]
        duals.append(q)
    assert all(duals[duals[d]]==d for d in range(3150))
    plane_by_d = [[h for h,H in enumerate(planes) if H<=D] for D in middles]
    assert all(len(hs)==16 for hs in plane_by_d)
    d_by_h = [[] for _ in planes]
    for d, hs in enumerate(plane_by_d):
        for h in hs:
            d_by_h[h].append(d)
    assert all(len(ds)==45 for ds in d_by_h)
    color = {}
    for h, classes in part.items():
        h = int(h)
        assert len(classes)==5 and all(len(ds)==9 for ds in classes)
        flat = [d for ds in classes for d in ds]
        assert len(set(flat))==45 and set(flat)==set(d_by_h[h])
        for c, ds in enumerate(classes):
            for d in ds:
                color[h,d]=c
    assert len(color)==50400
    receiver_class_incidence = 0
    for i in range(120):
        for h,H in enumerate(planes):
            if H<=orth[i]:
                for ds in part[str(h)]:
                    assert sum(middles[d]<=orth[i] for d in ds)==3
                receiver_class_incidence += 1
    assert receiver_class_incidence==40320
    native = frozenset(range(111))
    singleton = {j:[h for h,H in enumerate(planes) if H&native=={j}] for j in native}
    assert sum(map(len,singleton.values()))==11
    visible = {(i,j):[h for h,H in enumerate(planes) if j in H and H<=orth[i]]
               for i in native for j in orth[i]&native}
    assert len(visible)==6470 and all(len(hs)==16 for hs in visible.values())
    tight = {(i,j):all(len(planes[h]&native)>=2 for h in hs) for (i,j),hs in visible.items()}
    assert sum(tight.values())==6110
    profiles = {}
    for d,D in enumerate(middles):
        for j in D&native:
            hs = [h for h in plane_by_d[d] if j in planes[h]]
            assert len(hs)==4
            profiles[j,d] = tuple(sum(color[h,d]==c for h in hs) for c in range(5))
    def cut(i,d,js):
        ps = {str(j):list(profiles[j,d]) for j in sorted(js)}
        lower = sum(max(p[c] for p in ps.values()) for c in range(5))
        ks = [h for h in plane_by_d[duals[d]] if i in planes[h]]
        assert len(ks)==4
        assert all(middles[d]<=orth[i] for _ in [0])
        return {'receiver':i,'middle':d,'profiles':ps,'dimension_lower':lower,
                'outgoing_capacity':4,'right_planes':ks,'fails':lower>4}
    triangle = []
    for i in [10,33,80,95]:
        for d,D in enumerate(middles):
            js=D&{29,36,77}
            if len(js)>=2 and D<=orth[i]:
                assert all(tight[i,j] for j in js)
                triangle.append(cut(i,d,js))
    assert len(triangle)==156 and sum(z['fails'] for z in triangle)==151
    hist_by_i = {i:dict(sorted(Counter(z['dimension_lower'] for z in triangle if z['receiver']==i).items()))
                 for i in [10,33,80,95]}
    assert hist_by_i[10]=={6:39}
    first = next(z for z in triangle if z['receiver']==10 and z['middle']==81)
    assert first['profiles']=={'29':[0,2,0,2,0],'36':[0,2,0,0,2]}
    assert first['right_planes']==[424,605,674,916]
    all_cuts=[]
    for i in range(111):
        for d,D in enumerate(middles):
            if D<=orth[i]:
                js=[j for j in D&native if tight[i,j]]
                assert js
                all_cuts.append(cut(i,d,js))
    hist=Counter(z['dimension_lower'] for z in all_cuts)
    assert len(all_cuts)==34965 and sum(z['fails'] for z in all_cuts)==34425
    assert dict(hist)=={7:7337,4:540,6:1758,9:9394,8:8282,10:7081,5:98,11:475}
    # A common class renaming cannot remove a count discrepancy.
    p,q=first['profiles'].values()
    for perm in permutations(range(5)):
        assert sum(max(p[perm[c]],q[perm[c]]) for c in range(5))==6
    # Equal class counts are insufficient: two (2,2) subspaces have union rank6.
    a=[1<<i for i in [0,1,4,5]]; b=[1<<i for i in [0,2,4,6]]
    assert gf2_rank(a)==gf2_rank(b)==4 and gf2_rank(a+b)==6
    # Incorrectly allowing independent four-symbol capacity for each class hides the witness.
    assert first['dimension_lower']<=5*first['outgoing_capacity']
    # Independently permuting one donor's class components changes the premise.
    p2=p[:]; p2[3],p2[4]=p2[4],p2[3]
    assert p2==q and sum(max(x,y) for x,y in zip(p2,q))==4
    result={
      'status':'PASS_NATIVE_CLASS_SEPARATION_MIDDLE_GATE','pins':PINS,
      'geometry':{'roots':120,'planes':1120,'middles':3150,'parent_receiver_plane_incidence':40320,
                  'foreign_pairs':6470,'tight_foreign_pairs':6110},
      'triangle':{'comparisons':156,'failures':151,'histograms_by_receiver':hist_by_i,'first_failure':first},
      'all_native':{'comparisons':34965,'failures':34425,'histogram':dict(sorted(hist.items()))},
      'controls':{'global_class_permutations':120,'matching_counts_not_sufficient':True,
                  'invented_per_class_capacity_detected':True,'changed_class_premise_can_pass_local_screen':True},
      'scope':'Fixed class-separated source representation and exact proper sum; not a replacement-return rank bound.',
      'author_source_code_imported':False,'complete_supplier':False,'new_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'CUTS.json.gz').write_bytes(gzip.compress(json.dumps({'triangle':triangle,'all_native':all_cuts},sort_keys=True,separators=(',',':')).encode(),mtime=0))
    print(result['status'])
    print(json.dumps({'triangle':result['triangle'],'all_native':result['all_native']},sort_keys=True))

if __name__=='__main__':
    main()
