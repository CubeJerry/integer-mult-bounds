#!/usr/bin/env python3
"""Independent native two-patch facts. Apache-2.0; @CubeJerry/OpenAI."""
import argparse,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b

def present(x,b):
    while x:
        p=x.bit_length()-1
        if p not in b:return False
        x^=b[p]
    return True

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--native',type=Path,required=True)
    p.add_argument('--author-proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    raw=a.native.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    w=json.loads(gzip.decompress(raw))
    roots=[[Q(x)for x in w['frames'][str(w['start'][i])]['B'][0]]for i in range(111)]
    K=[sum(int(i==j or sum(x*y for x,y in zip(roots[i],roots[j]))==0)<<j for j in range(111))for i in range(111)]
    C=basis(K);need(len(C)==9,'canonical rank')
    S1={2,9,12,30,38,42};S2={2,26,63,65,81,87}
    h1=sum(1<<i for i in S1);h2=sum(1<<i for i in S2)
    need(len(basis(K+[h1,h2]))==11,'independent quotient directions')
    masks=[0,h1,h2,h1^h2];allbits=(1<<111)-1
    categories={};facts=[]
    for i,ki in enumerate(K):
        z=allbits^ki;restricted=basis([c&z for c in C.values()])
        need(len(restricted)==8,'restriction rank8')
        available=tuple(j for j,m in enumerate(masks)if present(m&z,restricted))
        need(available in [(0,),(0,1),(0,2),(0,1,2,3)],'availability class')
        categories.setdefault(available,[]).append(i)
        facts.append(dict(receiver=i,availability=list(available),degree=ki.bit_count()-1))
    counts={','.join(map(str,k)):len(v)for k,v in categories.items()}
    need(counts=={'0':77,'0,1':14,'0,2':14,'0,1,2,3':6},'availability census')
    J=categories[(0,1,2,3)]
    need(J==[33,57,68,79,102,106],'double-availability roles')
    need([K[i].bit_count()-1 for i in J]==[60,58,58,58,58,58],'double-group degrees')
    need(len(S1-S2)==len(S2-S1)==5 and S1&S2=={2},'region sizes')
    for label,S in [(1,S1),(2,S2)]:
        U=sorted(categories[(0,label)]+J)
        actual=[i for i in range(111)if all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for j in S)]
        need(U==actual and len(U)==20,'pure local representatives')
        need(sum(K[i].bit_count()-1<=58 for i in categories[(0,label)])==12,'eligible exclusive group')
    need(min(k.bit_count()-1 for k in K)==55,'minimum degree')
    reports=[]
    for name,extra,want in [('canonical',[],222),('first',[h1],205),('sum',[h1^h2],216),('full',[h1,h2],192)]:
        b=list(basis(K+extra).values());words=[0]
        for row in b:words += [x^row for x in words]
        F=[];ell=0
        for i,ki in enumerate(K):
            choices=[x for x in words if (x>>i)&1 and x&~ki==0]
            need(bool(choices),'feasible scalar row')
            row=min(choices,key=lambda x:(int(x.bit_count()-1>36)+int(x.bit_count()-1>52),x.bit_count(),x))
            F.append(row);ell+=int(row.bit_count()-1>36)+int(row.bit_count()-1>52)
        need(ell==want,'scalar minimum '+name)
        reports.append(dict(space=name,ell=ell,rank=len(basis(F)),canonical_quotient=len(basis(K+F))-9,rows_hex=[hex(x)for x in F]))
    need(reports[-1]['rank']==11 and reports[-1]['canonical_quotient']==2,'full-space control')
    out=dict(status='PASS_INDEPENDENT_TWO_PATCH_AVAILABILITY_AND_SCALAR_CONTROLS',author_proof_sha256=hashlib.sha256(a.author_proof.read_bytes()).hexdigest(),native_sha256=hashlib.sha256(raw).hexdigest(),availability_census=counts,receiver_facts=facts,scalar_controls=reports,scope='Universal matrix zero-pattern proof reviewed separately; author15-hyperplane enumeration not independently rerun.')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])

if __name__=='__main__':main()
