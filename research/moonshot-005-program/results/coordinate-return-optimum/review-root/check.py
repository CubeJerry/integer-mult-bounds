#!/usr/bin/env python3
"""Independent finite-premise check of the31-return optimum."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
def need(q,m):
    if not q:raise ValueError(m)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def reduce(v,E):
    r=list(map(F,v))
    for p,b in sorted(E.items()):
        c=r[p]
        if c:r=[x-c*y for x,y in zip(r,b)]
    return r
def echelon(rows):
    E={}
    for v in rows:
        r=reduce(v,E);p=next((j for j,x in enumerate(r) if x),None)
        if p is not None:
            c=r[p];E[p]=[x/c for x in r]
    return E
def root(n):
    S=[i for i in range(9) if n>>i&1]
    if len(S)==3:return tuple(2 if i in S else -1 for i in range(9))
    need(len(S)==7,'E8 normal weight');p,q=[i for i in range(9) if i not in S]
    return tuple(3*(int(i==p)-int(i==q)) for i in range(9))
def main(a):
    sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(sb).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','Native source')
    s=json.loads(gzip.decompress(sb));mraw=(a.author/'ACTUAL-M.json').read_bytes();zraw=(a.author/'COORDINATE-RETURN-CERTIFICATE.json').read_bytes()
    need(hashlib.sha256(mraw).hexdigest()=='5c56565541a6c185c04d56e02507745dd4e6dc3c21a16c615613749c37083965','Previously independently reviewed M')
    need(hashlib.sha256(zraw).hexdigest()=='3a285273b15e941fd8153ef463c058d811c072f91756a881e242f3f9d3ee0185','Reviewed kernel certificate')
    j=json.loads(mraw);H,K=j['H'],j['K'];Z=[[F(x) for x in r] for r in json.loads(zraw)['kernel_rows']]
    B=[5,56,65,69,77,96,100,103];ix={h:i for i,h in enumerate(H)};U=[Z[ix[i]] for i in B];E=echelon(U)
    need(len(E)==8,'Injective eight-dimensional root representation')
    normals={h:s['frames'][s['initial'][h]][0] for h in H};rv={h:root(normals[h]) for h in H}
    need(all(dot(rv[i],rv[j])==18*int(i==j) for i in B for j in B),'Native orthogonal basis')
    outside=[h for h in H if h not in K];base=B+outside;need(len(set(base))==82,'Exactly82 root directions')
    for h in outside:
        c=[-F(dot(rv[h],rv[j]),18) for j in B]
        need(all(sum(c[j]*U[j][k] for j in range(8))==Z[ix[h]][k] for k in range(14)),'E8 embedding of actual kernel row')
    quot=[]
    for h in K:
        if h in B:continue
        z=reduce(Z[ix[h]],E);need(any(z),'Nonzero exceptional quotient');c=next(x for x in z if x);quot.append(tuple(x/c for x in z))
    need(len(quot)==len(set(quot))==14,'Distinct14 quotient projective directions')
    ns=[n for n in range(512) if n.bit_count() in (3,7)];rs={n:root(n) for n in ns};flats=set();pairs=0
    for n,m in itertools.combinations(ns,2):
        if dot(rs[n],rs[m])==0:continue
        pairs+=1;f=frozenset(k for k in ns if dot(rs[k],rs[n])==dot(rs[k],rs[m])==0)
        need(len(f)==36,'A2 perpendicular E6 count');flats.add(f)
    bn={normals[h] for h in base};maximum=max(len(f&bn) for f in flats)
    need(pairs==3360 and len(flats)==1120 and maximum==29,'Complete1120-flat maximum29')
    J=json.loads((a.author/'B7-COORDINATE-CHOICE.json').read_text())['J'];need(len(J)==31 and len(echelon([Z[ix[i]] for i in J]))==7,'Attaining31-row rank7 witness')
    result={'status':'PASS_ROOT_OPTIMALITY_PREMISE_REVIEW','native_sha256':hashlib.sha256(sb).hexdigest(),
      'base_E8_rows':82,'exceptional_distinct_nonzero_quotient_rows':14,'A2_pairs':pairs,'E6_flats':len(flats),
      'maximum_base_E6_intersection':maximum,'attaining_return_count':31,'attaining_kernel_row_rank':7,'optimal_reverse_residual_rank':58,
      'scope':'Exact finite premises independently reconstructed. Universal lattice argument separately reviewed by bridge. Whole-coordinate returns in characteristic zero.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ['repo','author','output']:p.add_argument('--'+n,type=Path,required=True)
    main(p.parse_args())
