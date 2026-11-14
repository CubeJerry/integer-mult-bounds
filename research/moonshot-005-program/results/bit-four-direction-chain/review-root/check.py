#!/usr/bin/env python3
"""Independent native chain fitting, row optimum and real geometry."""
import argparse,gzip,json,hashlib,math,itertools
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

def rank(A,p=None):
    a=[[v%p if p else F(v)for v in row]for row in A];k=0
    for j in range(len(a[0])if a else 0):
        z=next((i for i in range(k,len(a))if a[i][j]),None)
        if z is None:continue
        a[k],a[z]=a[z],a[k];d=pow(a[k][j],-1,p)if p else 1/a[k][j];a[k]=[v*d%p if p else v*d for v in a[k]]
        for i in range(k+1,len(a)):
            d=a[i][j]
            if d:a[i]=[(v-d*w)%p if p else v-d*w for v,w in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def main():
    ap=argparse.ArgumentParser()
    for n in ['native','author','output']:ap.add_argument('--'+n,type=Path,required=True)
    a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    need(hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest()=='3cda8efd61508e3a0cdbb74b0a372a89128297a50bc297c9076efdbb2f51eef3','proof pin')
    w=json.loads(gzip.decompress(raw));v=[]
    for i in range(111):
        z=list(map(F,w['frames'][str(w['start'][i])]['B'][0]));d=math.lcm(*(x.denominator for x in z));v.append([int(x*d)for x in z])
    dot=lambda i,j:sum(x*y for x,y in zip(v[i],v[j]));K=[sum(1<<j for j in range(111)if j==i or dot(i,j)==0)for i in range(111)];C=list(basis(K).values());need(len(C)==9,'canonical rank9')
    T=[j for j in range(111)if all(j!=i and dot(i,j)==0 for i in [7,24,25])];need(len(T)==36 and T[-4:]==[103,105,107,109],'shared support')
    P=sum(1<<j for j in T[:32]);h=[P^(1<<T[-4]),1<<T[-3],1<<T[-2],P^(1<<T[-1])];need(len(basis(C+h))==13,'scalar envelope4')
    def expand(x,c):return sum(1<<(2*j+c)for j in range(111)if x>>j&1)
    q=[expand(h[i],0)^expand(h[i+1],1)for i in range(3)];CW=[expand(x,c)for x in C for c in [0,1]];selectors={7:[1,4],24:[3,4],25:[1,6]};rows=[];supports=[]
    for i in range(111):
        pair=[]
        for c in [0,1]:
            row=expand(K[i],c)
            if i in selectors:
                for z in range(3):
                    if selectors[i][c]>>z&1:row^=q[z]
            need((row>>(2*i)&3)==(1<<c),'diagonal identity');need(all(not(row>>(2*j)&3)for j in range(111)if not(K[i]>>j&1)),'forbidden blocks');pair.append(row);rows.append(row)
        supports.append([j for j in range(111)if j!=i and any(row>>(2*j)&3 for row in pair)])
    need(len(basis(CW+rows))-18==3,'actual quotient3');ell=sum((len(s)>36)+(len(s)>52)for s in supports);need(ell==216,'cardinality216')
    options=0;optimum=0
    full=(1<<111)-1
    for i in range(111):
        mask=(full^K[i])|(1<<i);rb={}
        for cw in C:
            x=cw&mask;y=cw
            while x:
                j=(x&-x).bit_length()-1
                if j in rb:x^=rb[j][0];y^=rb[j][1]
                else:rb[j]=(x,y);break
        need(len(rb)==9,'unique canonical restricted solution')
        allowed=[]
        for out in [0,1]:
            possibilities=[]
            for u in range(8):
                qrow=0
                for k in range(3):
                    if u>>k&1:qrow^=q[k]
                row=qrow;ok=True
                for channel in [0,1]:
                    x=sum(1<<j for j in range(111)if qrow>>(2*j+channel)&1)&mask
                    if out==channel:x^=1<<i
                    solution=0
                    for k in sorted(rb):
                        if x>>k&1:x^=rb[k][0];solution^=rb[k][1]
                    if x:ok=False;break
                    row^=expand(solution,channel)
                if ok:possibilities.append(row)
            allowed.append(possibilities)
        options+=len(allowed[0])*len(allowed[1]);best=2
        for x,y in itertools.product(*allowed):
            count=sum(j!=i and bool((x|y)>>(2*j)&3)for j in range(111));best=min(best,int(count>36)+int(count>52))
        optimum+=best
    need(options==378 and optimum==216,'independent complete fixed-code optimum')
    mon8=[(s,t)for s in range(8)for t in range(s,8)];Q8=[[z[s]*z[t]for s,t in mon8]for z in v]
    for i in range(111):need(rank([Q8[j]for j in range(111)if j!=i and K[i]>>j&1],509)==28,'full canonical real quadratic rank via fresh prime')
    table=[]
    for i,coords,chi in [(7,list(range(7)),2),(24,list(range(1,8)),1),(25,list(range(1,8)),1)]:
        omitted=next(j for j in range(8)if j not in coords);need(v[i][omitted]!=0,'facet coordinate projection isomorphism');Y=[[v[j][c]for c in coords]for j in supports[i]];Q=[[z[s]*z[t]for s in range(7)for t in range(s,7)]for z in Y];d1=rank(Y);d2=rank(Q)
        need(d1==7 and d2==({7:27,24:27,25:26}[i]),'exact changed support ranks')
        if i==7:
            values=[-2*y[1]*y[6]+y[2]**2-4*y[2]*y[5]-y[3]**2-y[4]**2+y[5]**2 for y in Y];need(not any(values),'unique quadratic vanishes')
            S=[[F(0)for _ in range(7)]for _ in range(7)]
            for z,c in [(2,1),(3,-1),(4,-1),(5,1)]:S[z][z]=c
            S[1][6]=S[6][1]=-1;S[2][5]=S[5][2]=-2;need(rank(S)==6 and 28-d2==1,'nonfactorability certificate')
        else:
            sign=-1 if i==24 else 1;f=[y[0]+sign*y[1]-y[3]-y[6]for y in Y];g=[y[0]+sign*y[1]-y[3]+y[6]for y in Y];need(all(x*z==0 for x,z in zip(f,g))and any(f)and any(g),'exact two proper hyperplane cover, single factor fails')
        table.append(dict(receiver=i,support=len(supports[i]),linear_rank=d1,quadratic_rank=d2,gamma=1,chi=chi))
    out=dict(status='PASS_INDEPENDENT_NATIVE_FOUR_DIRECTION_CHAIN',proof_sha256=hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),fitting_rank=len(basis(rows)),actual_quotient_dimension=3,scalar_envelope_dimension=4,enumerated_row_pairs=options,fixed_code_minimum_cardinality_charge=optimum,cardinality_charge=ell,geometric_charge=219,proper_cover_charge=220,changed_supports=table,canonical_quadratic_checks=111,scope='Independent native finite checks plus separate direct universal proof review. No physical source or new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],options,ell,219,220)
if __name__=='__main__':main()
