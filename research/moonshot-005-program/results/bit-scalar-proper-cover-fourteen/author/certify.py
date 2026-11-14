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
    for n in ['native','rank3','cliques','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');w=json.loads(gzip.decompress(raw));v=[]
    for i in range(111):
        z=list(map(F,w['frames'][str(w['start'][i])]['B'][0]));q=sum(x*x for x in z);z=[x*(2 if q==1 else 1)for x in z];need(all(x.denominator==1 for x in z),'integer roots');v.append(list(map(int,z)))
    dot=lambda i,j:sum(x*y for x,y in zip(v[i],v[j]));Q=[[z[s]*z[t]for s in range(8)for t in range(s,8)]for z in v];R=json.loads(a.rank3.read_text());C=json.loads(a.cliques.read_text())
    need((R['independent'],R['flat_count'],R['width_cases'])==(220934,74396,11761),'complete rank3 census')
    need(len(R['critical'])==94 and all(x['width']==6 for x in R['critical']),'critical rank3 domain')
    need({k:sum(z['eligible_count']==k for z in R['critical'])for k in [15,16,17]}=={15:54,16:28,17:12},'rank3 gain histogram')
    need(C['orthogonal_counts']=={'1':111,'2':3235,'3':29939,'4':90079,'5':77003,'6':35667,'7':9443,'8':1094},'complete clique census')
    need(C['max_common']['5'][0]==3 and C['max_common']['6'][0]==2,'orthogonal complement bounds')
    need(C['mixed_count']==663805 and C['max_mixed_common'][0]==6,'A1A1A2 bound')
    need(len(C['critical_orthogonal4'])==2 and len(C['critical_orthogonal7'])==6856,'critical clique domains')
    cases=[('rank3',z['flat'],z['orthogonal_roots'])for z in R['critical']]+[('orthogonal4',z['support'],z['orthogonal_roots'])for z in C['critical_orthogonal4']]+[('orthogonal7',z['support'],z['eligible_receivers'])for z in C['critical_orthogonal7']]
    certs=[];first=None
    for kind,S,receivers in cases:
        for i in receivers:
            need(all(dot(i,j)==0 for j in S),'receiver orthogonal to glued support');support=[j for j in range(111)if j!=i and dot(i,j)==0 and j not in S];m=[Q[j]for j in support];rr,cc=pivots(m);need(len(rr)==28,'full quadratic span')
            square=[[m[r][c]for c in cc]for r in rr];D=det(square);need(D!=0,'exact quadratic minor')
            if first is None:first=square
            certs.append(dict(kind=kind,deleted=S,receiver=i,minor_rows=[support[r]for r in rr],minor_columns=cc,determinant=str(D)))
    need(len(certs)==8737,'all required exceptional minors')
    bad=[r[:]for r in first];bad[1]=bad[0][:];need(det(bad)==0,'duplicate minor negative control')
    positive=[54,56,57,59,61,63,64];need(all(dot(i,j)==0 for i in positive for j in positive if i!=j),'orthogonal positive control')
    need(all(len(pivots([v[j]for j in positive if j!=i])[0])==6 for i in positive),'proper foreign support for14 witness')
    a.output.mkdir(parents=True,exist_ok=True)
    def save(name,obj):
        b=gzip.compress(json.dumps(obj,sort_keys=True,separators=(',',':')).encode(),mtime=0);(a.output/name).write_bytes(b);return hashlib.sha256(b).hexdigest()
    cp=save('CASES.json.gz',dict(rank3=R,cliques=C));mp=save('MINORS.json.gz',certs)
    out=dict(status='PASS_SHARP_SCALAR_PROPER_COVER_FOURTEEN',native_sha256=hashlib.sha256(raw).hexdigest(),rank3_cases=94,orthogonal4_cases=2,orthogonal7_cases=6856,exact_integer_minors=8737,cases_sha256=cp,minors_sha256=mp,orthogonal5_complement_max=3,orthogonal6_complement_max=2,mixed_A1_A1_A2_complement_max=6,positive_control=dict(support=positive,chi_saving=14),negative_duplicate_determinant=0,scope='Complete finite native geometric premises for the separate all-field proof; exact-cover capacity14, not cardinality14. No new kappa.')
    (a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(certs))
if __name__=='__main__':main()
