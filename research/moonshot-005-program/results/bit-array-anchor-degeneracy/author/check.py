#!/usr/bin/env python3
"""Evaluate nonzero native array-anchor polynomial witnesses over GF(64)."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import gzip
import json
from pathlib import Path
import numpy as np

def need(value, message):
    if not value:
        raise ValueError(message)

def multiply(a,b):
    out=0
    for i in range(6):
        if (b>>i)&1:
            out ^= a<<i
    for i in range(10,5,-1):
        if (out>>i)&1:
            out ^= 0x43<<(i-6)
    return out

MUL=np.array([[multiply(a,b) for b in range(64)] for a in range(64)],dtype=np.uint8)
INV=np.array([0]+[next(b for b in range(1,64) if MUL[a,b]==1) for a in range(1,64)],dtype=np.uint8)

def det(matrix):
    a=np.asarray(matrix,dtype=np.uint8).copy()
    need(a.ndim==2 and a.shape[0]==a.shape[1], 'square determinant')
    answer=1
    for col in range(len(a)):
        nz=np.flatnonzero(a[col:,col])
        if not len(nz):
            return 0
        pivot=col+int(nz[0])
        a[[col,pivot]]=a[[pivot,col]]
        x=int(a[col,col]);answer=int(MUL[answer,x])
        a[col]=MUL[INV[x],a[col]]
        a[col+1:] ^= MUL[a[col+1:,col,None],a[col][None,:]]
    return answer

def polynomial(nodes):
    p=np.array([1],dtype=np.uint8)
    for a in nodes:
        q=np.zeros(len(p)+1,dtype=np.uint8)
        q[:-1]^=MUL[a,p];q[1:]^=p;p=q
    return p

def evaluate(p,a):
    value=0
    for c in reversed(p):
        value=int(MUL[value,a])^int(c)
    return value

def powers(a):
    row=[1]
    for _ in range(15):
        row.append(int(MUL[row[-1],a]))
    return row

def vandermonde(nodes):
    value=1
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:
            value=int(MUL[value,a^b])
    return value

def main():
    cli=ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    here=Path(__file__).resolve().parents[1]
    pins=json.loads((here/'SOURCE-PINS.json').read_text())
    for path,entry in pins['files'].items():
        raw=(args.repo/path).read_bytes()
        need(len(raw)==entry['bytes'] and sha256(raw).hexdigest()==entry['sha256'], 'source pin '+path)
    base=args.repo/'research/moonshot-005-program/results'
    g=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    roots=np.asarray(g['root_table'],dtype=np.int16)
    planes=[frozenset(p) for p in g['A2']]
    orth=roots@roots.T==0
    stars={j:[h for h,p in enumerate(planes) if j in p] for j in range(111)}
    nodes={j:{h:n+1 for n,h in enumerate(star)} for j,star in stars.items()}
    visible={h:{i for i in range(111) if all(orth[i,j] for j in p)} for h,p in enumerate(planes)}
    singles={next(j for j in p if j<111) for p in planes if sum(j<111 for j in p)==1}
    eligible=set(range(111))-singles-{10}
    certificate=json.loads(gzip.decompress((base/'bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz').read_bytes()))['witnesses']
    need(len(certificate)==99 and {row['anchor'] for row in certificate}==eligible, 'complete eligible source domain')
    cache={};minors=[];rows=[];duplicate_control=None
    def adjugate_column(j,h,r):
        key=j,h,r
        if key in cache:
            return cache[key]
        hs=[q for q in stars[j] if r in visible[q]]
        need(len(hs)==16 and h in hs and r!=80, 'literal admissible native view')
        xs=[nodes[j][q] for q in hs]
        determinant=vandermonde(xs)
        need(determinant==det([powers(x) for x in xs]) and determinant, 'exact Vandermonde determinant')
        p=polynomial([nodes[j][q] for q in hs if q!=h])
        pivot=evaluate(p,nodes[j][h]);need(pivot, 'off-centre polynomial is nonzero at centre')
        c=MUL[int(MUL[determinant,INV[pivot]]),p]
        need([evaluate(c,x) for x in xs]==[determinant if q==h else 0 for q in hs], 'M times adjugate-column is det(M) insertion')
        cache[key]=c
        return c
    for record in certificate:
        j=record['anchor'];k,l=record['leaf_donors'];h1,h2,h3=record['centres'];i=record['final_receiver']
        need(k in eligible and l in eligible and len({j,k,l})==3, 'distinct eligible triangle roles')
        need({j,k}<=planes[h1] and {j,l}<=planes[h2] and {k,l}<=planes[h3], 'native triangle centres')
        need(i in visible[h3] and i!=80 and not orth[i,j], 'final identity receiver outside anchor star')
        values=[];mapped=[]
        for block,(leaf,h) in zip(record['propagations'],[(k,h1),(l,h2)]):
            need(block['leaf']==leaf and block['centre']==h, 'propagation edge')
            expected={q for q in stars[leaf] if q!=h3 and i in visible[q]}
            entries=block['quotient_propagations']
            need(len(entries)==15 and {e['leaf_plane'] for e in entries}==expected, 'all final off-centre leaf quotients')
            found=[]
            for entry in entries:
                q,R=entry['leaf_plane'],entry['anchor_plane'];receivers=entry['receivers']
                need(len(receivers)==len(set(receivers))==15 and R in stars[j] and R!=h and q!=h, 'fifteen off-centre propagation receivers')
                need(all(r in visible[h]&visible[q]&visible[R] for r in receivers), 'literal common visibility')
                C=np.column_stack([adjugate_column(j,h,r) for r in receivers])
                need(all(evaluate(c,nodes[j][R])==0 for c in C.T), 'all directions lie in the transported quotient kernel')
                value=det(C[1:,:]);need(value, 'selected fifteen-row propagation minor nonzero')
                values.append(value);minors.append(value);found.append(R)
                if duplicate_control is None:
                    fault=C[1:,:].copy();fault[:,-1]=fault[:,0]
                    need(det(fault)==0, 'duplicate propagation column kills determinant')
                    duplicate_control={'anchor':j,'centre':h,'leaf_plane':q,'correct_minor':value,'fault_minor':0}
            need(len(set(found))==15,'distinct transported quotient planes');mapped.append(found)
        need(mapped==record['distinct_anchor_plane_sets'] and len(values)==30, 'exact thirty records and final sets')
        A,B=map(set,mapped);union=sorted(A|B)
        need(len(A&B)==10 and len(union)==20, 'twenty final distinct anchor planes')
        selected=union[:16];xs=[nodes[j][q] for q in selected]
        final=det([powers(x) for x in xs])
        need(final and final==vandermonde(xs), 'chosen sixteen-plane final determinant')
        fault=xs[:-1]+[xs[0]]
        need(det([powers(x) for x in fault])==0, 'duplicate final plane kills determinant')
        delta=final
        for x in values:
            delta=int(MUL[delta,x])
        need(delta, 'entire explicit polynomial has nonzero RS value')
        rows.append({'anchor':j,'quotient_width_checked':1,'propagation_minor_values':values,
                     'final_sixteen_planes':selected,'final_determinant':final,'polynomial_value':delta})
    need(len(minors)==2970, 'complete polynomial witness census')
    result={'status':'PASS_NONZERO_ARRAY_ANCHOR_POLYNOMIALS', 'anchors':99,
            'propagation_minors':len(minors),'distinct_adjugate_columns':len(cache),
            'nonzero_minor_value_histogram':dict(sorted(Counter(minors).items())),
            'degree_formula':'7200*t*t-434*t','scalar_degree':6766,
            'positive_width_extension':'proved by tensor products in PROOF.md; not inferred from this finite check',
            'chosen_minor_is_only_sufficient_for_saturation':True,
            'duplicate_column_control':duplicate_control,'duplicate_final_plane_controls':99,
            'witnesses':rows,'all_foundations_retained':True,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],99,2970,len(cache),flush=True)

if __name__=='__main__':
    main()
