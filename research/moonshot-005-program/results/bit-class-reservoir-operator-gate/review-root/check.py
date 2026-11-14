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

def main():
    p=argparse.ArgumentParser()
    for n in ['native','author','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    need(hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest()=='850b4fd5792f9afb21499fd0886c758416f003f0b043d292ca5b975ca0ca981c','proof pin')
    w=json.loads(gzip.decompress(raw));author=json.loads((a.author/'RESULT.json').read_text());groups=author['groups'];roots=[]
    for i in range(111):
        v=list(map(F,w['frames'][str(w['start'][i])]['B'][0]));d=math.lcm(*(x.denominator for x in v));z=[int(x*d)for x in v];g=math.gcd(*z);roots.append([x//g for x in z])
    dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    need(sorted(i for group in groups for i in group)==list(range(111)),'exact partition')
    need(all(dot(i,j)==0 for group in groups for i in group for j in group if i!=j),'class orthogonality')
    K=[sum(1<<j for j in range(111)if i==j or dot(i,j)==0)for i in range(111)];C=basis(K)
    U=[sum(1<<i for i in group)for group in groups];need(len(C)==9 and len(basis(K+U))==19,'code dimensions')
    full=(1<<111)-1;owner={i:c for c,group in enumerate(groups)for i in group}
    for i,k in enumerate(K):
        forbidden=full^k
        need(len(basis([x&forbidden for x in list(C.values())+U]))==17,'restriction rank17')
        need(len(basis([k,U[owner[i]]]))==2 and U[owner[i]]&forbidden==0,'local kernel witnesses')
        contacts=[j for j in range(111)if j!=i and k>>j&1]
        quad=[[roots[j][s]*roots[j][t]for s in range(8)for t in range(s,8)]for j in contacts]
        need(modrank(quad)==28,'canonical quadratic rank28 overQ certified modulo257')
    quotient=[remainder(u,C)for u in U];need(all(quotient) and len(set(quotient))==15,'distinct nonzero quotient lines')
    best_card=[(-1,[])for _ in range(11)];best_geo=[(-1,[])for _ in range(11)]
    for mask in range(1<<15):
        chosen=[c for c in range(15)if mask>>c&1];r=len(basis([quotient[c]for c in chosen]));card=sum(len(groups[c])for c in chosen);geo=sum(len(groups[c])*(1 if len(groups[c])==8 else 2)for c in chosen)
        for cap in range(r,11):
            if card>best_card[cap][0]:best_card[cap]=(card,chosen)
            if geo>best_geo[cap][0]:best_geo[cap]=(geo,chosen)
    need([v[0]for v in best_card]==[0,8,16,24,32,40,54,63,71,85,111],'cardinality rank-cap table')
    table=[dict(rank_cap=r,maximum_cardinality_coverage=best_card[r][0],minimum_cardinality_charge=222-2*best_card[r][0],geometric_saving=best_geo[r][0],minimum_geometric_charge=222-best_geo[r][0],geometric_witness_classes=best_geo[r][1])for r in range(11)]
    need(table[2]['minimum_geometric_charge']==194 and table[10]['minimum_geometric_charge']==72,'geometric boundary controls')
    selected={1,2}; fitting=[U[owner[i]]if owner[i]in selected else K[i]for i in range(111)]
    need(len(basis(fitting))==11 and len(basis([K[i]for i in range(111)if owner[i]not in selected]))==9,'two-seven-class fittingrank11 and retained canonicalrank9')
    out=dict(two_seven_class_fitting_rank=11,two_seven_class_remaining_canonical_rank=9,status='PASS_INDEPENDENT_CLASS_RESERVOIR_NATIVE_RANKS',proof_sha256=hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),classes=[len(g)for g in groups],restriction_checks=111,subset_count=32768,canonical_quadratic_full_rank_checks=111,rank_table=table,scope='Supplied partition validated directly against native geometry; no author engine imported. Geometric table additionally uses the geometric-incidence theorem. No source or new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],[v['minimum_geometric_charge']for v in table])
if __name__=='__main__':main()
