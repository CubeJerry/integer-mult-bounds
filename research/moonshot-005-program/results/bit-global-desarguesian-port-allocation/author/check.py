#!/usr/bin/env python3
"""Exact finite certificate of globally compatible Desarguesian nine-port sets.

No optimizer, floating arithmetic, NumPy or author geometry module is used.
The finite certificate is sufficient independently of its LP discovery.
"""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def xor(xs):
    out=0
    for x in xs:out^=x
    return out
def independent(xs):
    pivots={};out=[]
    for value in xs:
        x=value
        while x:
            p=x.bit_length()-1
            if p not in pivots:pivots[p]=x;out.append(value);break
            x^=pivots[p]
    return out
def nullspace(equations,n):
    pivots={}
    for x in equations:
        while x:
            p=x.bit_length()-1
            if p not in pivots:pivots[p]=x;break
            x^=pivots[p]
    out=[]
    for p in range(n):
        if p in pivots:continue
        x=1<<p
        for c,row in sorted(pivots.items()):
            if (row&x).bit_count()%2:x^=1<<c
        need(all(not(row&x).bit_count()%2 for row in equations),'exact binary null vector');out.append(x)
    return out
def apply(J,x):return xor((J>>(6*p))&63 for p in range(6)if x>>p&1)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    package=Path(__file__).resolve().parents[1];pins=json.loads((package/'SOURCE-PINS.json').read_text())['files']
    for name,h in pins.items():need(hashlib.sha256((a.repo/name).read_bytes()).hexdigest()==h,'source pin '+name)
    base=a.repo/'research/moonshot-005-program/results'
    path=base/'bit-orthogonal-spread-port-allocation/review/check.py';spec=importlib.util.spec_from_file_location('reviewed_quadratic_geometry',path);G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
    layout=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());cols=B['lattice_basis_columns']
    inv=G.inv([[cols[j][i]for j in range(8)]for i in range(8)])
    change={xor(B['hyperbolic_basis_masks'][k]for k in range(8)if x>>k&1):x for x in range(256)};roots=[]
    for root in layout['root_table']:
        cs=[sum(x*y for x,y in zip(row,root))for row in inv];need(all(x.denominator==1 for x in cs),'integral root coordinates')
        roots.append(change[sum((int(x)&1)<<k for k,x in enumerate(cs))])
    need(len(set(roots))==120 and set(roots)=={x for x in range(256)if G.q(x)},'all actual nonsingular roots')
    H=[set(ids)for ids in layout['A2']];D=[set(ids)for ids in layout['D4']]
    need(len(H)==1120 and len(D)==3150,'complete atlas')
    witness=json.loads(gzip.decompress((package/'author/WITNESS.json.gz').read_bytes()))
    selected=set(witness['selected_D']);need(len(selected)==630,'marked D count')
    radicals=[];perps=[];Dlookup={frozenset(ids):d for d,ids in enumerate(D)}
    for d,ids in enumerate(D):
        ds={roots[j]for j in ids};V=G.span(ds);perp={x for x in range(256)if all(not G.polar(x,y)for y in ds)};rad=V&perp
        need(len(V)==16 and len(rad)==4 and all(not G.q(x)for x in rad),'actual singular D radical')
        partner=Dlookup[frozenset(j for j,x in enumerate(roots)if x in perp)]
        need((d in selected)==(partner in selected),'global perpendicular covariance')
        radicals.append(rad);perps.append(perp)
    selected_lines={frozenset(radicals[d])for d in selected};need(len(selected_lines)==315,'315 radical lines, paired D')
    parents=[[]for _ in D];views=0;native_views=0;point_checks=0;endo_hist=Counter();portsets=[]
    for h,ids in enumerate(H):
        hs={roots[j]for j in ids};hp={x for x in range(256)if all(not G.polar(x,y)for y in hs)}
        need(len(G.span(hs))==4 and len(hp)==64,'anisotropic H and six-space perpendicular')
        ports=[d for d,ds in enumerate(D)if ids<=ds];chosen=sorted(selected&set(ports));need(len(ports)==45 and len(chosen)==9,'all45/9 port counts');portsets.append(chosen)
        for d in ports:parents[d].append(h)
        singular={x for x in hp if x and not G.q(x)};need(len(singular)==27,'minus-space singular census')
        need(Counter(x for d in chosen for x in radicals[d]if x)==Counter({x:1 for x in singular}),'all27 point reservations');point_checks+=27
        supplied=witness['local_structures'][h];need(supplied['H']==h,'indexed local structure')
        b=supplied['coordinate_basis'];need(len(b)==6 and G.span(b)==hp,'literal six-space coordinate basis')
        labels={xor(b[p]for p in range(6)if mask>>p&1):mask for mask in range(64)};inverse={v:k for k,v in labels.items()};J=supplied['J']
        need(all(apply(J,apply(J,x))^apply(J,x)^x==0 for x in range(64)),'order-three irreducible field operator')
        need(all(G.q(inverse[apply(J,x)])==G.q(inverse[x])for x in range(64)),'quadratic-preserving field operator')
        equations=[]
        for d in chosen:
            rad={labels[x]for x in radicals[d]};need({apply(J,x)for x in rad}==rad,'every marked radical is one F4 line')
            r,s=sorted(rad-{0})[:2]
            ann=independent(z for z in range(64)if not(z&r).bit_count()%2 and not(z&s).bit_count()%2);need(len(ann)==4,'radical annihilator')
            for v in [r,s]:
                for z in ann:equations.append(sum(z<<(6*p)for p in range(6)if v>>p&1))
        kernel=nullspace(equations,36);endo_hist[len(kernel)]+=1;need(len(kernel)==2,'unique local field structure up to conjugacy')
        for i,x in enumerate(roots):
            if x not in hp:continue
            visible=[d for d in ports if x in perps[d]]
            need(len(visible)==15 and len(selected&set(visible))==3,'all receiver three/twelve split');views+=1;native_views+=int(i<111)
    profiles=0
    for d,ps in enumerate(parents):
        need(len(ps)==16,'all sixteen H flags at D')
        for j in D[d]:need(sum(j in H[h]for h in ps)==4,'every D donor has four flags');profiles+=1
    need(point_checks==30240 and views==40320 and profiles==37800,'complete finite quantifiers')
    need(portsets[263]==[110,132,720,810,1509,1735,1994,2621,2836],'literal new H263 component binding')
    # Exhaust all maximal singular four-spaces to distinguish the new marking
    # from every possible allocation formed from an orthogonal spread.
    zeros=[x for x in range(1,256)if not G.q(x)];level={frozenset({0})};level_counts=[]
    for dimension in range(4):
        new=set()
        for W in level:
            for x in zeros:
                if x not in W and all(not G.polar(x,y)for y in W):new.add(W|{x^y for y in W})
        level=new;level_counts.append(len(level))
    need(level_counts==[135,1575,2025,270],'all singular subspaces by dimension')
    hist=Counter()
    for W in level:
        lines={frozenset({0,x,y,x^y})for x in W if x for y in W if y not in(0,x)};need(len(lines)==35,'all lines in a singular four-space');hist[len(lines&selected_lines)]+=1
    need(hist=={0:72,7:135,15:63},'no complete marked maximal singular four-space')
    old=json.loads(gzip.decompress((base/'bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz').read_bytes()))
    changed=len(selected^set(old['selected_D']));need(changed==840,'changed global marking')
    result={'status':'PASS_GLOBAL_DESARGUESIAN_PORT_ALLOCATION','selected_D':630,'unselected_D':2520,'selected_radical_lines':315,'all_H':1120,'all_point_reservations':point_checks,'all_parent_receiver_views':views,'native_receiver_views':native_views,'D_donor_profiles':profiles,'perpendicular_D_checks':3150,'local_endomorphism_dimension_histogram':dict(endo_hist),'unique_F4_structures_up_to_conjugacy':1120,'H263_ports':portsets[263],'changed_D_labels':changed,'maximal_singular_four_space_selected_line_histogram':dict(hist),'source_word':False,'common_middle_word':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],1120,630,30240,40320,flush=True)

if __name__=='__main__':main()
