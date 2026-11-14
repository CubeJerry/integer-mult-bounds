#!/usr/bin/env python3
"""Standalone exact native certificates for the real-geometric facet gate.

Only the pinned native word is read. Geometry ranks are over Q/R, certified
by nonzero minors modulo257; value-code ranks are separately over F2.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from math import lcm
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
S1=[2,9,12,30,38,42]
S2=[2,26,63,65,81,87]
SUPPORTED=[0,24,27,34,53,59,80]
MONOMIALS=[(a,b)for a in range(8)for b in range(a,8)]
PRIME=257


def need(ok,message):
    if not ok:raise ValueError(message)


def indices(v):return [j for j in range(111)if v>>j&1]


def binary_basis(rows):
    piv={}
    for r in rows:
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return piv


def in_binary_span(v,piv):
    while v:
        p=v.bit_length()-1
        if p not in piv:return False
        v^=piv[p]
    return True


def modular_minor(rows):
    if not rows:return {'rank':0,'rows':[],'columns':[],'determinant_mod257':1}
    a=[[int(x)%PRIME for x in r]for r in rows];order=list(range(len(a)))
    selected=[];cols=[];at=0
    for c in range(len(a[0])):
        pivot=next((j for j in range(at,len(a))if a[j][c]),None)
        if pivot is None:continue
        a[at],a[pivot]=a[pivot],a[at];order[at],order[pivot]=order[pivot],order[at]
        selected.append(order[at]);cols.append(c)
        inv=pow(a[at][c],-1,PRIME);a[at]=[(x*inv)%PRIME for x in a[at]]
        for j in range(at+1,len(a)):
            scale=a[j][c]
            if scale:a[j]=[(x-scale*y)%PRIME for x,y in zip(a[j],a[at])]
        at+=1
        if at==len(a):break
    # Recompute the exhibited original minor's determinant, independently of
    # the rectangular pivot bookkeeping above.
    square=[[int(rows[i][c])%PRIME for c in cols]for i in selected];det=1
    for c in range(at):
        p=next((j for j in range(c,at)if square[j][c]),None)
        need(p is not None,'selected original minor is nonsingular')
        if p!=c:square[p],square[c]=square[c],square[p];det=-det
        scale=square[c][c];det=det*scale%PRIME;inv=pow(scale,-1,PRIME)
        for j in range(c+1,at):
            f=square[j][c]*inv%PRIME
            square[j]=[(x-f*y)%PRIME for x,y in zip(square[j],square[c])]
    need(det%PRIME!=0,'nonzero exact modular minor')
    return {'rank':at,'rows':selected,'columns':cols,'determinant_mod257':det%PRIME}


def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin')
    n=json.loads(gzip.decompress(raw));roots=[]
    for i in range(111):
        v=[F(x)for x in n['frames'][str(n['start'][i])]['B'][0]]
        norm=sum(x*x for x in v);v=[x*(2 if norm==1 else 1)for x in v]
        if next(x for x in v if x)<0:v=[-x for x in v]
        need(all(x.denominator==1 for x in v)and sum(x*x for x in v)==4,'integral normalized real source root')
        roots.append(list(map(int,v)))
    need(len(set(tuple(r)for r in roots))==111,'distinct normalized native source lines')
    for i in range(111):
        f=n['frames'][str(n['final'][111+i])];rr=[[F(x)for x in row]for row in f['B']]
        need(f['dim']==7 and all(sum(x*y for x,y in zip(roots[i],row))==0 for row in rr),'native endpoint is perpendicular to own source')
        integer_rows=[]
        for row in rr:
            scale=lcm(*(x.denominator for x in row));integer_rows.append([int(scale*x)for x in row])
        need(modular_minor(integer_rows)['rank']==7,'actual native facet has real rank7')
    dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    K=[sum(1<<j for j in range(111)if i==j or dot(i,j)==0)for i in range(111)]
    C=binary_basis(K);need(len(C)==9,'canonical characteristic-two rank9')
    words=[0]
    for c in C.values():words += [w^c for w in words]
    full=(1<<111)-1;h1=sum(1<<j for j in S1);h2=sum(1<<j for j in S2)
    need(len(binary_basis(K+[h1,h2]))==11,'two independent scalar patch cosets')
    qrows=[[r[x]*r[y]for x,y in MONOMIALS]for r in roots]
    def certificate(mask,expected=None):
        ids=indices(mask);lin=modular_minor([roots[j]for j in ids]);quad=modular_minor([qrows[j]for j in ids])
        if expected is not None:need(quad['rank']==expected,('quadratic certificate rank',ids,quad['rank']))
        return {'source_indices':ids,'linear_rank_mod257':lin['rank'],'quadratic_rank_mod257':quad['rank'],'linear_minor':{**lin,'source_indices':[ids[j]for j in lin['rows']]},'quadratic_minor':{**quad,'source_indices':[ids[j]for j in quad['rows']]}}
    availability=[];forced=[];rho=[]
    for i,ki in enumerate(K):
        z=full^ki;restricted=binary_basis(k&z for k in K)
        need(len(restricted)==8,'each canonical forbidden restriction has rank8')
        modes=[t for t,h in ((1,h1),(2,h2),(3,h1^h2))if in_binary_span(h&z,restricted)]
        need(modes in ([],[1],[2],[1,2,3]),'no extra quotient availability type')
        U=0
        for t in modes:
            h=h1 if t==1 else h2 if t==2 else h1^h2
            need(not(h&z)and not(h>>i&1),'available pure patch lift has zero own and forbidden coefficients')
            U|=h
        availability.append({'receiver':i,'available_nonzero_binary_directions':modes,'available_union_support':indices(U)})
        mask=(ki^(1<<i))&~U
        cert=certificate(mask,28);need(cert['linear_rank_mod257']==7,'forced roots span actual native facet')
        forced.append({'receiver':i,'forced_identity_foreign_support':indices(mask),'certificate':cert})
        ds=[(w&z).bit_count()for w in words if w and not(w>>i&1)]
        rho.append(min(ds))
    census=Counter(tuple(r['available_nonzero_binary_directions'])for r in availability)
    need(census=={():77,(1,):14,(2,):14,(1,2,3):6},'independent native availability census')
    need(Counter(rho)=={18:7,19:24,20:52,21:16,22:11,23:1},'canonical punctured distance census')
    # Rebuild both admitted scalar boundary fittings without importing them.
    fit193=[];fit192=[]
    for i,ki in enumerate(K):
        ds=availability[i]['available_nonzero_binary_directions'];degree=ki.bit_count()-1
        fit193.append(ki^h1 if 1 in ds and degree<=58 else ki^h2 if 2 in ds and degree<=58 else ki)
        fit192.append(ki^h1^h2 if ds==[1,2,3]else ki^h1 if ds==[1]and degree<=58 else ki^h2 if ds==[2]and degree<=58 else ki)
    controls={}
    for name,rows,want in (('admitted_ell193',fit193,193),('admitted_ell192',fit192,192)):
        need(all((row>>i)&1 and not(row&~K[i])for i,row in enumerate(rows)),'literal boundary fitting')
        card=sum((r.bit_count()-1>36)+(r.bit_count()-1>52)for r in rows)
        need(card==want and len(binary_basis(rows))==11,'admitted scalar boundary rank/price')
        need(all(not(sum(1<<j for j in forced[i]['forced_identity_foreign_support'])&~rows[i])for i in range(111)),'all forced positions present in scalar control')
        controls[name]={'rows_hex':[hex(v)for v in rows],'binary_rank':11,'cardinality_charge':card,'geometric_charge':222}
    # Rebuild the15 native orthogonal classes; their real rank floor is72.
    support=lambda r:tuple(j for j,x in enumerate(r)if x)
    patterns=sorted({support(r)for r in roots if len(support(r))==4});comp=lambda s:tuple(j for j in range(8)if j not in s)
    pairs=[(s,comp(s))for s in patterns if s<comp(s)];need(len(pairs)==7,'seven complementary support pairs')
    groups=[[]for _ in range(15)]
    for i,r in enumerate(roots):
        ss=support(r)
        group=0 if len(ss)==1 else 1+2*next(j for j,p in enumerate(pairs)if ss in p)+sum(x<0 for x in r)%2
        groups[group].append(i)
    class_rows=[];class_charge=0;class_certificates=[]
    for g in groups:
        need(len(g)<=8 and all(dot(i,j)==0 for i,j in itertools.combinations(g,2)),'orthogonal class')
        mask=sum(1<<j for j in g)
        for i in g:
            class_rows.append(mask);cert=certificate(mask^(1<<i),len(g)-1)
            need(cert['linear_rank_mod257']==len(g)-1,'independent orthogonal foreign roots')
            charge=int(len(g)==8);class_charge+=charge
            class_certificates.append({'receiver':i,'charge':charge,'certificate':cert})
    need(len(binary_basis(class_rows))==15 and class_charge==72,'existing class-code geometric control')
    controls['fifteen_class']={'groups':groups,'binary_rank':15,'cardinality_charge':0,'geometric_charge':72,'certificates':class_certificates}
    # The candidate supported-coordinate code is excluded regardless of route.
    T=sum(1<<j for j in SUPPORTED);supported=[];card=0
    for i,ki in enumerate(K):
        if i in SUPPORTED:continue
        need(rho[i]>len(SUPPORTED),'uniform supported-code canonical forcing')
        mask=(ki^(1<<i))&~T;cert=certificate(mask,28)
        supported.append({'receiver':i,'certificate':cert});card+=int(mask.bit_count()>36)+int(mask.bit_count()>52)
    need(len(supported)==104 and card==182,'supported-coordinate optimistic cardinality control')
    controls['seven_supported_coordinates']={'supported':SUPPORTED,'canonical_forcing_minimum_rho':min(rho),'cardinality_minimum':182,'geometric_minimum':208,'certificates':supported}
    # A genuine two-proper-chart union must fail full quadratic span.
    union=sum(1<<j for j in range(111)if j!=0 and dot(0,j)==0 and(dot(1,j)==0 or dot(2,j)==0))
    one=sum(1<<j for j in range(111)if j!=0 and dot(0,j)==0 and dot(1,j)==0)
    un=certificate(union);single=certificate(one)
    need(un['linear_rank_mod257']==7 and un['quadratic_rank_mod257']<28,'two-flat union control')
    need(single['linear_rank_mod257']==6 and single['quadratic_rank_mod257']==21,'one-flat control')
    controls['two_proper_charts']={'receiver':0,'normal_sources':[1,2],'vanishing_quadratic':'(root1 dot z)*(root2 dot z)','certificate':un}
    controls['one_proper_chart']={'receiver':0,'normal_source':1,'certificate':single}
    out={'status':'PASS_NATIVE_QUADRATIC_FACET_AND_UNIFORM_TWO_PATCH_GATE_PREMISES','native_sha256':PIN,'geometry_field':'Q, hence R; distinct from the arbitrary characteristic-two value field','modular_certificate_prime':PRIME,'ambient_quadratic_monomials':MONOMIALS,'canonical_binary_rank':9,'canonical_punctured_distances':rho,'S1':S1,'S2':S2,'availability':availability,'forced_identity_certificates':forced,'uniform_two_patch_geometric_charge':222,'retained_all_route_target_cap':194,'controls':controls,'scope':'Exact finite source and rank premises. Universal geometric incidence and arbitrary-field/all-width code conclusions are proved in PROOF.md; no source, supplier, new kappa or foundation is supplied.','complete_supplier':False,'new_kappa':False}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'fixed_two_patch_geometric_charge':222,'supported_coordinate_geometric_minimum':208,'boundary193':controls['admitted_ell193']['cardinality_charge'],'boundary192':controls['admitted_ell192']['cardinality_charge'],'class_geometric_control':72,'two_chart_control_quad_rank':un['quadratic_rank_mod257']}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
