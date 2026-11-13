#!/usr/bin/env python3
"""Exact full E7 root-line parabolic orbit and two-proper-subspace certificate."""
from collections import deque,Counter
from itertools import product
from pathlib import Path
import argparse,gzip,hashlib,json
import sympy as sp

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def line(v):
    v=tuple(v)
    return v if next(x for x in v if x)>0 else tuple(-x for x in v)
def main(a):
    path=a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
    raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
    native=json.loads(gzip.decompress(raw))
    roots=[tuple(native['frames'][str(native['start'][i])]['B'][0]) for i in range(111)]
    supports=sorted({tuple(j for j,x in enumerate(r) if x) for r in roots if sum(x!=0 for x in r)==4})
    assert len(supports)==14
    full={tuple(2*int(j==i) for j in range(8)) for i in range(8)}
    for sup in supports:
        for signs in product((-1,1),repeat=3):
            v=[0]*8;v[sup[0]]=1
            for j,s in zip(sup[1:],signs):v[j]=s
            full.add(tuple(v))
    assert len(full)==120 and all(dot(v,v)==4 for v in full)
    for u in full:
        for v in full:
            d=dot(u,v);assert d%2==0
            assert line(tuple(y-d//2*x for x,y in zip(u,v))) in full
    actual=[line(tuple(2*x for x in r) if sum(x!=0 for x in r)==1 else r) for r in roots]
    assert len(set(actual))==111 and set(actual)<=full
    # Full root-line transitivity is checked, not inferred from a name.
    reached={actual[0]};q=deque(reached)
    while q:
        v=q.popleft()
        for u in full:
            d=dot(u,v)//2;w=line(tuple(y-d*x for x,y in zip(u,v)))
            if w not in reached:reached.add(w);q.append(w)
    assert reached==full
    e7=sorted(v[1:] for v in full if v[0]==0);assert len(e7)==63
    generic=tuple(3**i for i in range(7))
    positive=[]
    for r in e7:
        z=dot(r,generic);assert z
        positive.append(r if z>0 else tuple(-x for x in r))
    positive=set(positive)
    sums={tuple(x+y for x,y in zip(u,v)) for u in positive for v in positive}
    simple=sorted(positive-sums);assert len(simple)==7
    cartan=[[dot(u,v)//2 for v in simple] for u in simple]
    assert all(cartan[i][i]==2 for i in range(7))
    assert all(cartan[i][j] in (0,-1) for i in range(7) for j in range(7) if i!=j)
    inv=sp.Matrix(simple).T.inv()
    coeff=[]
    for r in e7:
        c=inv*sp.Matrix(r);assert all(x.q==1 for x in c)
        cc=tuple(int(x) for x in c)
        assert all(x>=0 for x in cc) or all(x<=0 for x in cc)
        coeff.append(cc)
    def mask(v):return sum(1<<j for j,c in enumerate(coeff) if dot(v,c)==0)
    all_masks={};orbits=[]
    for k in range(7):
        start=tuple(int(i==k) for i in range(7));seen={start};q=deque(seen)
        while q:
            v=q.popleft()
            for j in range(7):
                w=line(tuple(v[i]-v[j]*cartan[j][i] for i in range(7)))
                if w not in seen:seen.add(w);q.append(w)
        masks={mask(v) for v in seen};assert len(masks)==len(seen)
        sizes={m.bit_count() for m in masks};assert len(sizes)==1
        for v in seen:
            m=mask(v);assert m not in all_masks
            all_masks[m]=(k,v)
        orbit={'node':k,'line_orbit_size':len(seen),'root_lines':next(iter(sizes)),'representative_normal':start,'representative_mask':hex(mask(start))}
        orbits.append(orbit);print(json.dumps(orbit),flush=True)
    pair=[]
    for o in orbits:
        m=int(o['representative_mask'],16);maxu=max((m|z).bit_count() for z in all_masks)
        witnesses=[(z,k,v) for z,(k,v) in all_masks.items() if (m|z).bit_count()==maxu]
        z,k,v=witnesses[0]
        pair.append({'first_node':o['node'],'max_union':maxu,'second_node':k,'second_normal':v,'second_mask':hex(z),'intersection_size':(m&z).bit_count()})
    maxu=max(p['max_union'] for p in pair)
    out={'status':'PASS_EXACT_FULL_E7_PARABOLIC_ORBIT_ENUMERATION','source_sha256':PIN,'full_E8_lines':120,'actual_lines':111,'full_E7_lines':63,'full_E8_reflection_closure':True,'full_E8_root_line_transitivity':True,'simple_roots':simple,'cartan':cartan,'root_coefficients':coeff,'orbits':orbits,'distinct_maximal_parabolic_root_sets':len(all_masks),'pair_union_by_first_orbit':pair,'max_two_proper_subspace_root_line_union':maxu,'actual_foreign_support_min':min(sum(dot(u,v)==0 for j,v in enumerate(actual) if i!=j) for i,u in enumerate(actual)), 'scope':'Exact certificate premises; universal containment in maximal parabolics uses the separately proved closed-Weyl-chamber argument. No algorithm or supplier bound by this certificate alone.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'max_union':maxu,'orbits':len(orbits),'total_flats':len(all_masks)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
