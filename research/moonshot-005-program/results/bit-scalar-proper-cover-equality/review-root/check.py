#!/usr/bin/env python3
"""Independent equality14 source review using Gram-adjugate membership.
Rank3 method follows the root's credited sharp14 census, independently of
Worker C's double-perpendicular author census. Apache-2.0.
"""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import numpy as np

def need(ok,msg):
    if not ok:raise ValueError(msg)
def bits(mask):
    while mask:
        b=mask&-mask;yield b.bit_length()-1;mask-=b
def mod_basis(matrix,p=521):
    basis={};chosen=[]
    for i,row in enumerate(matrix):
        row=[int(x)%p for x in row]
        for j,b in sorted(basis.items()):
            c=row[j]
            if c:row=[(x-c*y)%p for x,y in zip(row,b)]
        j=next((j for j,x in enumerate(row) if x),None)
        if j is not None:
            inv=pow(row[j],-1,p);basis[j]=[x*inv%p for x in row];chosen.append(i)
    return chosen
def mod_det(matrix,p=521):
    a=[[int(x)%p for x in r] for r in matrix];value=1
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];value=-value
        q=a[j][j];value=value*q%p;inv=pow(q,-1,p)
        for i in range(j+1,len(a)):
            z=a[i][j]*inv%p;a[i]=[(x-z*y)%p for x,y in zip(a[i],a[j])]
    return value%p
def norm(v):
    v=list(map(F,v));scale=2 if sum(x*x for x in v)==1 else 1
    v=[x*scale for x in v];need(all(x.denominator==1 for x in v),'integer roots')
    v=list(map(int,v));need(sum(x*x for x in v)==4,'norm4 roots')
    if next(x for x in v if x)<0:v=[-x for x in v]
    return tuple(v)

def main():
    p=argparse.ArgumentParser()
    for n in ['native','sharp14-cases','package','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    oldraw=a.sharp14_cases.read_bytes();need(hashlib.sha256(oldraw).hexdigest()=='7567810dd8eab8add727a5d2e4371cb6af588d4e61630e62c43a07f7f5b45932','inherited case pin')
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='758f1a14d992387881ec14e837bc5c8b8c81cc4459e24b4b5a9f39c194ed7af9','author proof pin')
    n=json.loads(gzip.decompress(raw));old=json.loads(gzip.decompress(oldraw));e=json.loads(gzip.decompress((a.package/'output/EVIDENCE.json.gz').read_bytes()))
    roots=[norm(n['frames'][str(n['start'][i])]['B'][0]) for i in range(111)]
    R=np.asarray(roots,dtype=np.int64);D=R@R.T;A=D//2
    need(np.all(D%2==0),'integer half-Gram');deg=np.count_nonzero(D==0,axis=1)
    adj=[sum(int(D[i,j]==0)<<j for j in range(111)) for i in range(111)]
    need(dict(Counter(map(int,deg)))=={55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1},'complete degree histogram')
    caps=[0,1,3,6,12,20,36,111,111];triples=[]
    for r in range(1,9):
        for s in range(r,caps[r]+1):
            for j in range(min(r,s)+1):
                if s<=j+caps[r-j]:
                    b=min(caps[8-r],int(np.count_nonzero(deg<=52+s)))+min(caps[8-r],int(np.count_nonzero(deg<=36+s)))+2*j
                    triples.append((r,s,j,b))
    equality=[z for z in triples if z[3]==14]
    need(len(triples)==569 and equality==[(3,4,1,14),(4,4,1,14),(4,5,1,14),(4,6,1,14),(4,7,1,14),(5,5,4,14),(8,8,7,14)],'complete equality-envelope list')
    ids=np.asarray(list(itertools.combinations(range(111),3)),dtype=np.int64)
    flats={};independent=0
    for start in range(0,len(ids),4096):
        B=ids[start:start+4096];x=A[B[:,0],B[:,1]];y=A[B[:,0],B[:,2]];z=A[B[:,1],B[:,2]]
        determinant=8-2*(x*x+y*y+z*z)+2*x*y*z;need(np.all(determinant>=0),'nonnegative exact triple determinant')
        ok=determinant>0;B=B[ok];x=x[ok];y=y[ok];z=z[ok];determinant=determinant[ok];independent+=len(B)
        d0=A[B[:,0]];d1=A[B[:,1]];d2=A[B[:,2]]
        value=(4-z*z)[:,None]*d0*d0+(4-y*y)[:,None]*d1*d1+(4-x*x)[:,None]*d2*d2+2*(y*z-2*x)[:,None]*d0*d1+2*(x*z-2*y)[:,None]*d0*d2+2*(x*y-2*z)[:,None]*d1*d2
        for b,member in zip(B,value==2*determinant[:,None]):flats.setdefault(np.packbits(member).tobytes(),tuple(map(int,b)))
    need(independent==220934 and len(flats)==74396,'complete triple and flat census')
    rank3=[];larger=[];widths=0
    for key,B in flats.items():
        S=tuple(map(int,np.flatnonzero(np.unpackbits(np.frombuffer(key,dtype=np.uint8))[:111])))
        need(3<=len(S)<=6,'native rank3 flat cap')
        if len(S)<5:continue
        outside=tuple(map(int,np.flatnonzero(np.all(D[:,B]==0,axis=1))))
        for width in (5,6):
            if width>len(S):continue
            widths+=1;eligible=tuple(i for i in outside if deg[i]<=52+width)
            if len(eligible)==14:rank3.append((S,width,outside,eligible))
            if len(eligible)>14:larger.append((S,width,outside,len(eligible)))
    need(widths==11761 and len(rank3)==94,'new rank3 equality cases')
    need(set(rank3)=={(tuple(x['support']),x['width'],tuple(x['outside']),tuple(x['eligible'])) for x in e['rank3_equal14']},'independent equality3 domain agrees')
    need(set(larger)=={(tuple(x['flat']),x['width'],tuple(x['orthogonal_roots']),x['eligible_count']) for x in old['rank3']['critical']},'larger rank3 cases inherited explicitly')
    print('independent rank3 equality census complete',flush=True)
    patterns={tuple(i for i,x in enumerate(v) if x) for v in roots if sum(x!=0 for x in v)==4}
    full={tuple(2*int(i==j) for i in range(8)) for j in range(8)}
    for S in patterns:
        for signs in itertools.product((-1,1),repeat=3):
            v=[0]*8;v[S[0]]=1
            for i,s in zip(S[1:],signs):v[i]=s
            full.add(tuple(v))
    need(len(full)==120 and set(roots)<=full,'complete120 root domain')
    full=sorted(full);FR=np.asarray(full,dtype=np.int64);FD=FR@R.T
    signed=set(full)|{tuple(-x for x in v) for v in full}
    for v,w in itertools.product(full,repeat=2):
        d=sum(x*y for x,y in zip(v,w));need(d%2==0 and tuple(x-d*y//2 for x,y in zip(v,w)) in signed,'reflection closed root completion')
    current=[((i,),adj[i]) for i in range(111)];counts={};equal4=[];d4={};links=[];twooutside=0
    old7={(tuple(x['support']),i) for x in old['cliques']['critical_orthogonal7'] for i in x['eligible_receivers']}
    found7=set();found4=set()
    for size in range(1,9):
        counts[size]=len(current)
        for S,common in current:
            if size==4:
                eligible=tuple(i for i in bits(common) if deg[i]<=56)
                need(len(eligible)<=7,'four-clique outside cap')
                if len(eligible)==7:found4.add(S)
                if len(eligible)==6:equal4.append((S,4,tuple(bits(common)),eligible))
                native_flat=tuple(map(int,np.flatnonzero(np.sum(D[:,S]**2,axis=1)==16)))
                if len(native_flat)==12 and native_flat not in d4:
                    all_flat=np.flatnonzero(np.sum(FD[:,S]**2,axis=1)==16)
                    need(len(all_flat)==12,'native12 flat is the full D4')
                    O=np.flatnonzero(np.all(FD[:,S]==0,axis=1));need(len(O)==12,'complement fullD4 has12 roots')
                    G=FR[O]@FR[O].T;need(np.all(np.count_nonzero(G==0,axis=1)==3),'complement roots have only3 perpendicular neighbors')
                    d4[native_flat]=S
            if size==6:
                need(common.bit_count()<=2,'six-clique outside cap')
                if common.bit_count()==2:
                    i,j=tuple(bits(common));twooutside+=1;need(D[i,j]==0,'outside roots actually orthogonal')
                    for blocked,added in ((i,j),(j,i)):
                        if deg[blocked]<=58:
                            seven=tuple(sorted(S+(added,)));need((seven,blocked) in old7,'seven certificate applies to potentially saving receiver')
                            links.append((S,blocked,added,seven))
            if size==7:
                need(common.bit_count()<=1,'seven-clique outside cap')
                found7.update((S,i) for i in bits(common) if deg[i]<=59)
        if size<8:current=[(S+(i,),C&adj[i]) for S,C in current for i in bits(C>>(S[-1]+1)<<(S[-1]+1))]
    need(counts=={1:111,2:3235,3:29939,4:90079,5:77003,6:35667,7:9443,8:1094},'all clique domains complete')
    need(len(equal4)==9 and set(equal4)=={(tuple(x['support']),x['width'],tuple(x['outside']),tuple(x['eligible'])) for x in e['orthogonal4_equal14']},'all nine equality4 cases')
    need(len(d4)==1121 and set(d4)=={tuple(x['native_D4']) for x in e['full_native_D4']},'all1121 nativeD4 spans')
    need(twooutside==30632 and len(links)==31472,'all six-to-seven cases counted')
    need(set(links)=={(tuple(x['six']),x['blocked_receiver'],x['added_root'],tuple(x['seven'])) for x in e['six_to_seven_links']},'complete inherited-certificate links')
    need(found7==old7 and found4=={tuple(x['support']) for x in old['cliques']['critical_orthogonal4']},'inherited exceptional domains exact')
    print('independent clique and D4 census complete',flush=True)
    mon=list(itertools.combinations_with_replacement(range(7),2));Q=[]
    for i,v in enumerate(roots):
        excluded=next(j for j,x in enumerate(v) if x);free=[j for j in range(8) if j!=excluded]
        Q.append([[w[free[b]]*w[free[c]] for b,c in mon] for w in roots])
    certificates=[]
    for kind,records in [('rank3',rank3),('orthogonal4',equal4)]:
        for S,width,outside,eligible in records:
            found=None
            for i in reversed(eligible):
                available=[j for j in reversed(tuple(bits(adj[i]))) if j not in S]
                chosen=mod_basis([Q[i][j] for j in available])
                if len(chosen)==28:
                    points=[available[j] for j in chosen];minor=[Q[i][j] for j in points];residue=mod_det(minor)
                    need(residue!=0 and mod_det([minor[0]]+minor[:-1])==0,'fresh nonzero minor and duplicate-row rejection')
                    found=dict(kind=kind,support=S,width=width,receiver=i,minor_roots=points,prime=521,residue=residue);break
            need(found is not None,'fresh quadratic obstruction for every equality case');certificates.append(found)
    need(len(certificates)==103,'all103 fresh independent minors')
    low=[i for i,d in enumerate(deg) if d<=56];need(len(low)==12 and len(mod_basis([roots[i] for i in low]))==7,'low-degree roots have rank7 modulo521')
    need(all(sum(x*y for x,y in zip(roots[i],[0,-1,1,0,1,0,0,1]))==0 for i in low),'exact common annihilator gives upper rank7')
    canonical=all(len(mod_basis([Q[i][j] for j in bits(adj[i])]))==28 for i in range(111));need(canonical,'canonical chi2 verified')
    seven=[54,56,57,59,61,63,64];eight=list(range(8))
    for S,foreignrank in [(seven,6),(eight,7)]:need(all(len(mod_basis([roots[j] for j in S if j!=i]))==foreignrank for i in S),'proper-cover boundary controls')
    report=dict(status='PASS_INDEPENDENT_SCALAR_EQUALITY14_REVIEW',native_sha256=hashlib.sha256(raw).hexdigest(),author_proof_sha256=hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest(),rank3=dict(independent_triples=independent,flats=len(flats),width_cases=widths,equality_cases=len(rank3)),clique_counts=counts,orthogonal4_equality_cases=len(equal4),full_native_D4=len(d4),six_two_outside=twooutside,six_to_seven_links=len(links),fresh_prime=521,fresh_quad28_minors=len(certificates),low_degree_rank=7,canonical_chi2=canonical,equality_envelope=equality,controls=['duplicate-row determinant zero','seven-support has six independent foreign roots','eight-support has seven independent foreign roots'],scope='Independent complete new finite premises and separately reviewed all-characteristic-two equality proof; inherited sharp14/gluing premises retained. No new kappa.')
    a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
    (a.output/'INDEPENDENT-MINORS.json.gz').write_bytes(gzip.compress(json.dumps(certificates,sort_keys=True).encode(),mtime=0))
    print(report['status'])
if __name__=='__main__':main()
