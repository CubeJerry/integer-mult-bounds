#!/usr/bin/env python3
"""Independent quadratic enumeration of the orthogonal-spread port allocation."""
import argparse,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path

def need(v,s):
    if not v:raise ValueError(s)
def xor(xs):
    v=0
    for x in xs:v^=x
    return v
def q(x):return sum(((x>>(2*k))&1)*((x>>(2*k+1))&1)for k in range(4))%2
def polar(x,y):return q(x^y)^q(x)^q(y)
def span(basis):
    values={0}
    for v in basis:values|={u^v for u in list(values)}
    return values
def inv(A):
    d=len(A);w=[[Fraction(x)for x in row]+[Fraction(i==j)for j in range(d)]for i,row in enumerate(A)]
    for c in range(d):
        p=next(r for r in range(c,d)if w[r][c]);w[c],w[p]=w[p],w[c]
        z=w[c][c];w[c]=[v/z for v in w[c]]
        for r in range(d):
            if r!=c:
                z=w[r][c];w[r]=[x-z*y for x,y in zip(w[r],w[c])]
    return [row[d:]for row in w]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results';lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json';pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    lb=gzip.decompress(lp.read_bytes());need(hashlib.sha256(lb).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native layout')
    L=json.loads(lb);B=json.loads(bp.read_text());cols=B['lattice_basis_columns'];inverse=inv([[cols[j][i]for j in range(8)]for i in range(8)])
    change={xor(B['hyperbolic_basis_masks'][k]for k in range(8)if x>>k&1):x for x in range(256)};roots=[]
    for root in L['root_table']:
        cs=[sum(x*y for x,y in zip(row,root))for row in inverse];need(all(x.denominator==1 for x in cs),'integral lattice point')
        roots.append(change[sum((int(x)&1)<<k for k,x in enumerate(cs))])
    need(len(set(roots))==120 and set(roots)=={x for x in range(256)if q(x)},'all nonsingular roots')
    masks=[0,12,22,27,39,41,53,58];spread=[]
    for mask in masks:
        A=[0]*4;t=0
        for r in range(4):
            for c in range(r+1,4):
                if mask>>t&1:A[r]|=1<<c;A[c]|=1<<r
                t+=1
        graph={sum(((u>>k)&1)<<(2*k)for k in range(4))^sum(((A[k]&u).bit_count()%2)<<(2*k+1)for k in range(4))for u in range(16)}
        need(len(graph)==16 and all(not q(v)for v in graph),'maximal singular graph');spread.append(graph)
    spread.append({sum(((u>>k)&1)<<(2*k+1)for k in range(4))for u in range(16)})
    need(all(spread[i]&spread[j]=={0}for i in range(9)for j in range(i)),'pairwise disjoint spread')
    need(set.union(*spread)=={x for x in range(256)if not q(x)},'all135 nonzero singular vectors')
    H=[{roots[j]for j in ids}for ids in L['A2']];D=[{roots[j]for j in ids}for ids in L['D4']]
    need(len(H)==1120 and len(D)==3150,'complete native charts');lookup={frozenset(ds):d for d,ds in enumerate(D)}
    selected=[];radicals=[];dual=[];perps=[]
    for d,ds in enumerate(D):
        V=span(ds);need(len(V)==16 and {x for x in V if q(x)}==ds,'exact D span')
        perp={x for x in range(256)if all(not polar(x,y)for y in ds)};rad=V&perp
        need(len(rad)==4 and all(not q(x)for x in rad),'singular two-dimensional radical')
        radicals.append(sorted(rad-{0}));perps.append(perp)
        partner=lookup[frozenset(x for x in perp if q(x))];dual.append(partner)
        if any(rad<=W for W in spread):selected.append(d)
    marked=set(selected);need(len(marked)==630,'global marked D census')
    need(all((d in marked)==(dual[d]in marked)for d in range(3150)),'perpendicular marking invariance')
    portsets=[];view_count=0;sourceviews=0;changed=0
    old=json.loads(gzip.decompress(pp.read_bytes()))['classes'];byD=[[]for _ in D]
    for h,hs in enumerate(H):
        need(len(span(hs))==4 and all(q(x)for x in hs),'anisotropic H')
        ports=[d for d,ds in enumerate(D)if hs<=ds];chosen=sorted(marked&set(ports))
        need(len(ports)==45 and len(chosen)==9,'all H45/9 counts');portsets.append(chosen)
        if not any(set(C)==set(chosen)for C in old[str(h)]):changed+=1
        for d in ports:byD[d].append(h)
        hp={v for v in range(256)if all(not polar(v,x)for x in hs)}
        need(len(hp)==64 and sum(not q(x)for x in hp)==28,'H perpendicular minus-space zero census')
        for W in spread:need(len(W&hp)==4,'every spread intersection has dimension2')
        for i,v in enumerate(roots):
            if v not in hp:continue
            visible=[d for d in ports if v in perps[d]]
            need(len(visible)==15 and len(marked&set(visible))==3,'all receiver3/12 counts')
            zero_count=sum(not q(x) and not polar(x,v)for x in hp);need(zero_count==16,'five-space zero census')
            view_count+=1
            if i<111:sourceviews+=1
    need(view_count==40320 and changed==1091,'all parent views and changed partitions')
    profiles=0
    for d,parents in enumerate(byD):
        need(len(parents)==16,'sixteen H planes per D')
        for root in D[d]:
            count=sum(root in H[h]for h in parents);need(count==4,'four flags per donor at D');profiles+=1
    w=json.loads(gzip.decompress((a.author/'output/WITNESS.json.gz').read_bytes()))
    need(w['alternating_masks']==masks and w['selected_D']==selected,'emitted spread and D selection')
    supplied_dual=w['perpendicular_D']
    if isinstance(supplied_dual,dict):supplied_dual=[supplied_dual[str(d)]for d in range(3150)]
    need(supplied_dual==dual,'emitted perpendicular partners')
    need([set(x)-{0}for x in w['D_radicals']]==[set(x)for x in radicals],'emitted radical vectors')
    supplied=w['selected_ports_by_H']
    if isinstance(supplied,dict):supplied=[supplied[str(h)]for h in range(1120)]
    need(supplied==portsets,'emitted local port allocation')
    # Mutating one D destroys exact H quotas on every one of its16 parent charts.
    fault=marked^{selected[0]};broken=sum(len(fault&set(d for d,ds in enumerate(D)if hs<=ds))!=9 for hs in H)
    need(broken==16,'single D label fault detected')
    result={'status':'PASS_INDEPENDENT_ORTHOGONAL_SPREAD_PORT_ALLOCATION','spread_spaces':9,'nonzero_singular_vectors':135,'selected_D':630,'unselected_D':2520,'all_H':1120,'all_parent_receiver_views':view_count,'native_receiver_views':sourceviews,'D_donor_profiles':profiles,'perpendicular_pairs_checked':3150,'changed_from_all_old_classes':changed,'H263_marked_ports':portsets[263],
      'component_input_widths_b3840':[768,3072],'component_quotient_widths_b3840':[48,192],
      'negative_control_broken_H_after_one_D_mutation':broken,'scope':'Geometric component capacities, not actual phases/source lifts/endpoint realization.',
      'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,bp,pp]],
      'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'witness_payload_sha256':hashlib.sha256(gzip.decompress((a.author/'output/WITNESS.json.gz').read_bytes())).hexdigest(),'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],flush=True)
if __name__=='__main__':main()
