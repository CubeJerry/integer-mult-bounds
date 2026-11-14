#!/usr/bin/env python3
"""New exact minors; the prior exhaustive flat census is a pinned dependency.
Bareiss utility adapted from root's geometric-facet review.
"""
import argparse,gzip,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path

def need(q,s):
    if not q:raise ValueError(s)

def det(a):
    a=[list(r)for r in a];n=len(a);old=1;sign=1
    if not n:return 1
    for k in range(n-1):
        pivot=next((i for i in range(k,n)if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        q=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                z=q*a[i][j]-a[i][k]*a[k][j];need(z%old==0,'Bareiss exact division');a[i][j]=z//old
            a[i][k]=0
        old=q
    return sign*a[-1][-1]

def pivots(a,p=257):
    a=[[v%p for v in row]for row in a];labels=list(range(len(a)));rows=[];cols=[]
    for j in range(len(a[0])if a else 0):
        k=len(rows);z=next((i for i in range(k,len(a))if a[i][j]),None)
        if z is None:continue
        a[k],a[z]=a[z],a[k];labels[k],labels[z]=labels[z],labels[k];q=pow(a[k][j],-1,p);a[k]=[v*q%p for v in a[k]]
        for i in range(k+1,len(a)):
            q=a[i][j]
            if q:a[i]=[(v-q*w)%p for v,w in zip(a[i],a[k])]
        rows.append(labels[k]);cols.append(j)
        if len(rows)==len(a):break
    return rows,cols

def main():
    p=argparse.ArgumentParser()
    for name in ['native','scalar-package','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    oldraw=(a.scalar_package/'RESULT.json').read_bytes();need(hashlib.sha256(oldraw).hexdigest()=='88a192ec4b859780b02f109fdd0172cf52c6adbab8ae782006fa72b8192716a8','complete result pin')
    need(hashlib.sha256((a.scalar_package/'PROOF.md').read_bytes()).hexdigest()=='8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b','predecessor proof pin')
    old=json.loads(oldraw);w=json.loads(gzip.decompress(raw));v=[]
    for i in range(111):
        r=list(map(F,w['frames'][str(w['start'][i])]['B'][0]));d=math.lcm(*(x.denominator for x in r));r=[int(x*d)for x in r];g=math.gcd(*r);r=[x//g for x in r]
        if sum(x*x for x in r)==1:r=[2*x for x in r]
        need(sum(x*x for x in r)==4,'integer root norm4');v.append(r)
    dot=lambda i,j:sum(x*y for x,y in zip(v[i],v[j]));mon=[(i,j)for i in range(8)for j in range(i,8)];Q=[[r[i]*r[j]for i,j in mon]for r in v]
    rows=old['rank3_maximizers'];need(len(rows)==12 and all(e['width']==6 and e['eligible_count']==17 for e in rows),'complete12 records')
    need(old['rank3_flat_count']==74396 and old['independent_triple_count']==220934 and old['rank3_five_six_cases']==11761,'inherited census')
    cert=[];firstsquare=None
    for e in rows:
        P=e['flat'];B=e['basis'];need(len(pivots([v[j]for j in B])[0])==3,'flat basis independent')
        exactflat=[j for j in range(111)if len(pivots([v[b]for b in B]+[v[j]])[0])==3];need(exactflat==P,'actual full rank3 flat')
        O=[i for i in range(111)if all(dot(i,b)==0 for b in B)];need(O==e['orthogonal_roots'] and len(O)==20,'all orthogonal receivers')
        for i in O:
            S=[j for j in range(111)if j!=i and dot(i,j)==0 and j not in P];mat=[Q[j]for j in S];rr,cc=pivots(mat);need(len(rr)==28,'full quadratic span')
            square=[[mat[r][c]for c in cc]for r in rr];D=det(square);need(D!=0,'nonzero exact minor')
            if firstsquare is None:firstsquare=square
            cert.append(dict(flat=P,receiver=i,forced_support=S,minor_source_indices=[S[r]for r in rr],minor_columns=cc,integer_determinant=str(D)))
    bad=[r[:]for r in firstsquare];bad[1]=bad[0][:];need(det(bad)==0,'duplicate-row control')
    S=[54,56,57,59,61,63,64];need(all(dot(i,j)==0 for i in S for j in S if i!=j),'seven orthogonal control')
    need(all(len(pivots([v[j]for j in S if j!=i])[0])==6 for i in S),'proper foreign spans')
    out=dict(status='PASS_SCALAR_PROPER_COVER_SIXTEEN_CERTIFICATES',native_sha256=hashlib.sha256(raw).hexdigest(),predecessor_result_sha256=hashlib.sha256(oldraw).hexdigest(),extremal_flat_count=12,exact_minor_count=len(cert),certificates=cert,positive_control=dict(support=S,chi_saving=14),negative_control_duplicate_determinant=0,scope='240 new exact native minors plus pinned prior exhaustive classification; all-field theorem separate. No new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out['status'],len(cert))
if __name__=='__main__':main()
