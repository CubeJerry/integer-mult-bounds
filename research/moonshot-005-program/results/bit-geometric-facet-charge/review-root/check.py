#!/usr/bin/env python3
"""Independent native class-code and geometric frontier checks."""
import argparse,gzip,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def basis(xs):
    b={}
    for x in xs:
        while x:
            j=(x&-x).bit_length()-1
            if j in b:x^=b[j]
            else:b[j]=x;break
    return b

def remainder(x,b):
    for j in sorted(b):
        if x>>j&1:x^=b[j]
    return x

def modrank(a,p=257):
    a=[[x%p for x in row]for row in a];i=0
    for j in range(len(a[0])if a else 0):
        z=next((z for z in range(i,len(a))if a[z][j]),None)
        if z is None:continue
        a[i],a[z]=a[z],a[i];inv=pow(a[i][j],-1,p);a[i]=[x*inv%p for x in a[i]]
        for z in range(i+1,len(a)):
            c=a[z][j]
            if c:a[z]=[(x-c*y)%p for x,y in zip(a[z],a[i])]
        i+=1
        if i==len(a):break
    return i

def determinant(a):
    a=[list(row)for row in a];n=len(a);previous=1;sign=1
    if not n:return 1
    for k in range(n-1):
        z=next((z for z in range(k,n)if a[z][k]),None)
        if z is None:return 0
        if z!=k:a[k],a[z]=a[z],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=pivot*a[i][j]-a[i][k]*a[k][j]
                need(v%previous==0,'exact Bareiss division');a[i][j]=v//previous
            a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]

def main():
    ap=argparse.ArgumentParser()
    for name in ['native','package','output']:ap.add_argument('--'+name,type=Path,required=True)
    a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='8fed71e8698ce84e1fa0f09deb7433f3338f21f3a35b912d08e2de046426d8ab','reviewed proof pin')
    w=json.loads(gzip.decompress(raw));author=json.loads((a.package/'RESULT.json').read_text());roots=[]
    for i in range(111):
        r=list(map(F,w['frames'][str(w['start'][i])]['B'][0]));den=math.lcm(*(x.denominator for x in r));z=[int(x*den)for x in r];g=math.gcd(*z);z=[x//g for x in z]
        if sum(x*x for x in z)==1:z=[2*x for x in z]
        if next(x for x in z if x)<0:z=[-x for x in z]
        need(sum(x*x for x in z)==4,'normalized integer roots');roots.append(z)
    mon=[(i,j)for i in range(8)for j in range(i,8)];quad=[[r[i]*r[j]for i,j in mon]for r in roots]
    need(author['ambient_quadratic_monomials']==[list(x)for x in mon],'monomial conventions')
    dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    K=[sum(1<<j for j in range(111)if i==j or dot(i,j)==0)for i in range(111)];C=basis(K);need(len(C)==9,'binary canonical rank')
    words=[0]
    for c in C.values():words += [x^c for x in words]
    h1=sum(1<<j for j in [2,9,12,30,38,42]);h2=sum(1<<j for j in [2,26,63,65,81,87]);hs=[0,h1,h2,h1^h2]
    need(len(basis(K+[h1,h2]))==11,'two-patch quotient independence')
    full=(1<<111)-1;checked=[];rho=[];census={}
    def certify(cert,expected_support,rank_wanted):
        need(cert['source_indices']==expected_support,'exact forced support')
        m=cert['quadratic_minor'];ids=m['source_indices'];cols=m['columns']
        need(len(ids)==len(set(ids))==len(cols)==len(set(cols))==rank_wanted,'minor dimensions and distinct indices')
        need(ids==[expected_support[j]for j in m['rows']] and all(0<=c<36 for c in cols),'actual native minor coordinates')
        square=[[quad[j][c]for c in cols]for j in ids];det=determinant(square)
        need(det!=0 and det%257==m['determinant_mod257'],'independent exact integer determinant')
        return det
    for i,ki in enumerate(K):
        facet=w['frames'][str(w['final'][111+i])];rr=[list(map(F,row))for row in facet['B']]
        ints=[]
        for row in rr:
            den=math.lcm(*(x.denominator for x in row));ints.append([int(x*den)for x in row])
        need(facet['dim']==7 and modrank(ints)==7 and all(sum(x*y for x,y in zip(roots[i],row))==0 for row in rr),'actual seven-dimensional receiver facet')
        z=full^ki;R=basis([c&z for c in C.values()]);need(len(R)==8,'canonical restriction rank8')
        available=[j for j in range(1,4)if not remainder(hs[j]&z,R)]
        need(available==author['availability'][i]['available_nonzero_binary_directions'],'independent local availability')
        census[str(available)]=census.get(str(available),0)+1;U=0
        for j in available:
            need(hs[j]&z==0 and not(hs[j]>>i&1),'pure own-zero local patch representative');U|=hs[j]
        forced=[j for j in range(111)if j!=i and ki>>j&1 and not(U>>j&1)]
        fact=author['forced_identity_certificates'][i];need(fact['receiver']==i and fact['forced_identity_foreign_support']==forced,'correct forced identity positions')
        det=certify(fact['certificate'],forced,28);checked.append(det)
        dist=min((x&z).bit_count()for x in words if x and not(x>>i&1));rho.append(dist)
    need(rho==author['canonical_punctured_distances'],'all111 independently enumerated punctured distances')
    T=author['controls']['seven_supported_coordinates']['supported'];need(T==[0,24,27,34,53,59,80],'supported code fixed scope')
    supported=[]
    for fact in author['controls']['seven_supported_coordinates']['certificates']:
        i=fact['receiver'];need(i not in T and rho[i]>len(T),'supported canonical forcing')
        forced=[j for j in range(111)if j!=i and K[i]>>j&1 and j not in T]
        supported.append(certify(fact['certificate'],forced,28))
    need(len(supported)==104,'all outside-support receivers certified')
    controls={}
    for name in ['admitted_ell192','admitted_ell193']:
        rows=[int(x,16)for x in author['controls'][name]['rows_hex']]
        W=basis(K+[h1,h2]);need(len(rows)==111 and all(row>>i&1 and not(row&~K[i]) and not remainder(row,W)for i,row in enumerate(rows)),'actual boundary code fitting')
        ell=sum(int((x.bit_count()-1)>36)+int((x.bit_count()-1)>52)for x in rows)
        need(ell==int(name[-3:]) and len(basis(rows))==11,'algebraic boundary is preserved')
        need(all(all(row>>j&1 for j in author['forced_identity_certificates'][i]['forced_identity_foreign_support'])for i,row in enumerate(rows)),'forced identity geometry survives boundary fitting')
        controls[name]=dict(cardinality=ell,geometric=222,rank=11)
    groups=author['controls']['fifteen_class']['groups'];need(sorted(i for g in groups for i in g)==list(range(111)),'class partition')
    need(all(dot(i,j)==0 for g in groups for i in g for j in g if i!=j),'orthogonal class geometry')
    need(sum(len(g)for g in groups if len(g)==8)==72,'class geometric72 scope control')
    for label,normals,want in [('one_proper_chart',[1],21),('two_proper_charts',[1,2],27)]:
        desired=[j for j in range(111)if j!=0 and dot(0,j)==0 and any(dot(n,j)==0 for n in normals)]
        cert=author['controls'][label]['certificate'];certify(cert,desired,want)
        need(all(any(dot(n,j)==0 for n in normals)for j in desired),'genuine vanishing product')
        controls[label]=dict(quadratic_rank=want,linear_rank=modrank([roots[j]for j in desired]))
    tmask=sum(1<<j for j in T);fit=[1<<i if i in T else k&~tmask for i,k in enumerate(K)]
    need(all(row>>i&1 and not(row&~K[i])for i,row in enumerate(fit)),'supported-code upper fitting')
    supported_ell=sum(int(x.bit_count()-1>36)+int(x.bit_count()-1>52)for x in fit);need(supported_ell==182,'supported cardinality182')
    sample=author['forced_identity_certificates'][0]['certificate']['quadratic_minor'];square=[[quad[j][c]for c in sample['columns']]for j in sample['source_indices']]
    damaged=[row[:]for row in square];damaged[1]=damaged[0][:];need(determinant(damaged)==0,'duplicate-row invalidates minor')
    wrong_field=modrank(square,2);need(wrong_field<28,'value field cannot certify real geometry')
    out=dict(status='PASS_INDEPENDENT_EXACT_GEOMETRIC_FACET_CERTIFICATES',native_sha256=hashlib.sha256(raw).hexdigest(),author_proof_sha256=hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest(),two_patch_integer_minors=len(checked),supported_integer_minors=len(supported),availability_census=census,minimum_punctured_distance=min(rho),two_patch_geometric_charge=222,supported_geometric_charge=208,supported_cardinality_charge=supported_ell,controls=controls,negative_controls=dict(duplicated_minor_row_determinant=0,wrong_characteristic_minor_rank=wrong_field),scope='Independent exact integer minors overQ/R and separate F2 code restrictions; universal proof reviewed separately. No new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(checked),len(supported),wrong_field)
if __name__=='__main__':main()
