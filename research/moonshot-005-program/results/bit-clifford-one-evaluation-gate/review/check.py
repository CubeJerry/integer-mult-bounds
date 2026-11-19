#!/usr/bin/env python3
"""Separate column-action review of the one-vector Clifford source gate."""
from argparse import ArgumentParser
from pathlib import Path
from fractions import Fraction
from collections import Counter
from itertools import combinations
import gzip, hashlib, json
from sympy import Matrix

def span(vectors):
    piv = {}
    for v in vectors:
        while v:
            k = (v & -v).bit_length() - 1
            if k not in piv:
                piv[k] = v
                break
            v ^= piv[k]
    return list(piv.values())

def act(cols, v):
    y = 0
    while v:
        low = v & -v
        y ^= cols[low.bit_length() - 1]
        v ^= low
    return y

def product(a, b):
    return [act(a, c) for c in b]

def flat(a):
    return sum(c << (16 * k) for k, c in enumerate(a))

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();p=args.repo/'research/moonshot-005-program'
    source=p/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(source.read_bytes())
    assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    data=json.loads(raw);roots=data['root_table'];planes=data['A2']
    witness=json.loads((args.author/'BASIS.json').read_text())
    basis=Matrix.hstack(*[Matrix(c) for c in witness['lattice_basis_columns']])
    assert abs(basis.det())==16
    gram=basis.T*basis/2
    assert gram.det()==1 and all(v.q==1 for v in gram)
    assert all(int(gram[i,i])%2==0 for i in range(8))
    inv=basis.inv(); masks=[]
    for r in roots:
        v=inv*Matrix(r);assert all(c.q==1 for c in v)
        masks.append(sum((int(c)&1)<<i for i,c in enumerate(v)))
    def bil(v,w):
        return sum(int(gram[i,j]) for i in range(8) for j in range(8) if v>>i&1 and w>>j&1)%2
    def q(v):
        x=Matrix([(v>>i)&1 for i in range(8)])
        return int((x.T*gram*x)[0]/2)%2
    hyp=witness['hyperbolic_basis_masks'];assert len(span(hyp))==8
    assert all(q(v)==0 for v in hyp)
    assert all(bil(v,w)==int(i//2==j//2 and i!=j) for i,v in enumerate(hyp) for j,w in enumerate(hyp))
    coordinates={}
    for c in range(256):
        v=0
        for i in range(8):
            if c>>i&1:v^=hyp[i]
        coordinates[v]=c
    assert len(set(masks))==120 and all(q(v)==1 for v in masks)
    assert sum(q(v) for v in range(256))==120
    I=[1<<i for i in range(16)]
    def gamma(v):
        c=coordinates[v];out=[]
        for s in range(16):
            target=0
            for k in range(4):
                if (c>>(2*k+int(bool(s>>k&1))))&1:target^=1<<(s^(1<<k))
            out.append(target)
        return out
    gs=[gamma(v) for v in range(256)]
    for v in range(256):
        assert product(gs[v],gs[v])==([0]*16 if not q(v) else I)
        for w in range(256):
            assert [a^b for a,b in zip(product(gs[v],gs[w]),product(gs[w],gs[v]))]==([0]*16 if not bil(v,w) else I)
    dot=lambda a,b:sum(x*y for x,y in zip(roots[a],roots[b]))
    adjacent=[{j for j in range(120) if j!=i and dot(i,j)==0} for i in range(120)]
    assert all((j in adjacent[i])==(bil(masks[i],masks[j])==0) for i in range(120) for j in range(i))
    local=[]
    for H in planes:
        j,k=H[:2];a,b=gs[masks[j]],gs[masks[k]]
        mats=[I,a,b,product(a,b)]
        assert len(span(map(flat,mats)))==4
        local.append(mats)
    hist=Counter();critical=None
    for i in range(111):
        for j in sorted(adjacent[i]&set(range(111))):
            hs=[h for h,H in enumerate(planes) if j in H and set(H)<=adjacent[i]]
            assert len(hs)==16
            mats=[x for h in hs for x in local[h]]
            rank=len(span(map(flat,mats)));assert rank==14;hist[rank]+=1
            W=[v for v in range(256) if bil(masks[i],v)==0]
            wb=span(W);assert len(wb)==7 and masks[j] in W
            envelope=[gs[v] for v in wb]+[product(gs[masks[j]],gs[v]) for v in wb]
            assert len(span(map(flat,envelope)))==14
            assert len(span([*map(flat,envelope),*map(flat,mats)]))==14
            if (i,j)==(5,77):critical=(hs,mats)
    assert sum(hist.values())==6470
    hs,mats=critical
    assert len(span([act(a,1) for a in mats]+[act(a,128) for a in mats]))==16
    all_j=[a for h,H in enumerate(planes) if 77 in H for a in local[h]]
    changed_scope_rank=len(span(map(flat,all_j)))
    assert changed_scope_rank>14
    frame=[9,30,37,46,52,77,92,101]
    assert all(dot(a,b)!=0 for a,b in combinations(frame,2))
    edge={}
    for j in range(111):
        endpoints=tuple(k for k,v in enumerate(frame) if j in adjacent[v])
        if len(endpoints)==2:assert endpoints not in edge;edge[endpoints]=j
    assert all(e in edge for e in combinations(range(7),2)) and edge[0,5]==5
    for e,j in edge.items():
        for f,k in edge.items():
            if j!=k and set(e)&set(f):assert k not in adjacent[j]
    budget_path=p/'results/bit-irreducible-low-excess-target/review/output/BUDGET.json'
    budget=json.loads(budget_path.read_text())
    assert Fraction(budget['base_room'][1])<Fraction(279,1000)
    assert 8**199>7**200 and Fraction(7,24)-Fraction(279,1000)==Fraction(19,1500)
    assert Fraction(1,24)>Fraction(1,30)
    pins={str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [source,budget_path]}
    result={'status':'PASS_INDEPENDENT_CLIFFORD_SOURCE_GATE_REVIEW','author_code_imported':False,
      'matrix_convention':'column actions with lowest-pivot elimination','native_envelopes':dict(hist),
      'critical_visible_planes':hs,'local_A2_algebras':len(planes),'gamma_squares':256,'gamma_pairs':65536,
      'two_evaluation_control_rank':16,'allow_nonvisible_H_control_rank':changed_scope_rank,
      'source_rank_upper':'7/8','return_excess_lower':'1/24','target_excess':'1/30',
      'movement_rational_gap':'19/1500','native_frame':frame,'source_pins':pins,'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
