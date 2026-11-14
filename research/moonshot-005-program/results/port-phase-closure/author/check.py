#!/usr/bin/env python3
"""Independent exact all-class phase conjugacy and complete2048-case spectrum.
No numpy, floating arithmetic, root checker or author builder is imported.
@CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse,gzip,hashlib,json
from collections import Counter,deque
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
BASE=Path(__file__).resolve().parents[3]
WORD=BASE/'worker-b/logical-involution-112/output/R0-minimal/WORD.json.gz'
PIN='c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'
def need(x,m):
    if not x:raise ValueError(m)
def span(vs):
    s={0}
    for v in vs:s|={x^v for x in tuple(s)}
    return s
def root(v):
    if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
    q=[i for i in range(9)if not(v>>i&1)];need(len(q)==2,'exact native root type')
    return [3*(int(i==q[0])-int(i==q[1]))for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def aff(c,t):return tuple(c^((t&x).bit_count()%2)for x in range(8))
def add(a,b):return tuple((x+y)%4 for x,y in zip(a,b))

def geometry(w):
    m=w['logical_involution'];P=m['ports'];v={int(h):n for h,n in m['normals'].items()};Z=m['omitted_frame'];rho={h:root(v[h])for h in P};rz=[root(z)for z in Z]
    gram={h:{j:F(dot(rho[h],rho[j]),18)for j in P}for h in P};a={h:[F(dot(rho[h],r),18)for r in rz]for h in P};classes={}
    for h in P:classes.setdefault(tuple(i for i in range(8)if a[h][i]),[]).append(h)
    need(len(classes)==14 and all(len(t)==8 for t in classes.values()),'fourteen exact classes')
    H=[[(-1)**(((x&1)*((y>>1)&1)+((x>>1)&1)*(y&1))%2)for y in range(4)]for x in range(4)]
    canonical=[[0 if (i//4)==(j//4)else -H[i%4][j%4]for j in range(8)]for i in range(8)]
    refs=[];radicals=Counter()
    for modes,ports in sorted(classes.items()):
        parts={-1:[],1:[]}
        for h in ports:
            sign=1
            for i in modes:sign*=1 if a[h][i]>0 else -1
            parts[sign].append(h)
        T,S=parts[-1],parts[1];UT=span(v[h]for h in T);US=span(v[h]for h in S);W=UT&US;rr=sorted(W-{0});aa,bb=rr[:2];ww=[0,aa,bb,aa^bb];u=min(v[h]for h in T);vv=min(v[h]for h in S)
        need(len(W)==4 and len(UT)==len(US)==8 and len(span(UT|US))==16,'native rank2 common radical')
        need({u^z for z in W}=={v[h]for h in T}and{vv^z for z in W}=={v[h]for h in S},'two affine radical planes')
        label=[u^z for z in ww]+[vv^z for z in ww];lookup={n:h for h,n in v.items()};ordered=[lookup[n]for n in label]
        J=[[2*gram[ordered[i]][ordered[4+j]]for j in range(4)]for i in range(4)];need(all(x in(-1,1)for row in J for x in row),'exact cross signs')
        diagonal=[J[i][0]for i in range(4)]+[J[0][j]*J[0][0]for j in range(4)]
        R2=[[2*(F(i==j)-gram[h][k])for j,k in enumerate(ordered)]for i,h in enumerate(ordered)]
        need([[diagonal[i]*R2[i][j]*diagonal[j]for j in range(8)]for i in range(8)]==canonical,'exact signed-permutation conjugacy to one standard cross Fourier swap')
        patterns={tuple((n&z).bit_count()%2 for n in label)for z in range(512)};want={aff(c,t)for c in range(2)for t in range(8)}
        need(patterns==want,'all and only sixteen affine Boolean one-column phases')
        need(all(label[x]==u^((vv^u)if x&4 else 0)^(aa if x&1 else 0)^(bb if x&2 else 0)for x in range(8)),'literal affine coordinate formula')
        radicals[tuple(sorted(W))]+=1
        witness=next(z for z in range(512)if tuple((n&z).bit_count()%2 for n in label)==aff(0,1))
        refs.append({'modes':list(modes),'canonical_port_order':ordered,'native_labels':label,'diagonal_signs':[int(x)for x in diagonal],'radical_basis':[aa,bb],'affine_base':u,'half_direction':u^vv,'repeated_character_native_column':witness})
    need(len(radicals)==7 and set(radicals.values())=={2},'seven common radicals each used twice')
    return canonical,refs

def phase_family():
    generators=sorted({aff(c,t)for c in range(2)for t in range(8)});zero=(0,)*8;distance={zero:0};q=deque([zero])
    while q:
        x=q.popleft()
        for g in generators:
            z=add(x,g)
            if z not in distance:distance[z]=distance[x]+1;q.append(z)
    polynomial={}
    for c,a,b,d in product(range(4),repeat=4):
        for e,f,g in product(range(2),repeat=3):
            vals=tuple((c+a*(x&1)+b*((x>>1)&1)+d*((x>>2)&1)+2*(e*(x&1)*((x>>1)&1)+f*(x&1)*((x>>2)&1)+g*((x>>1)&1)*((x>>2)&1)))%4 for x in range(8))
            need(vals not in polynomial,'unique quadratic normal form');polynomial[vals]=(c,a,b,d,e,f,g)
    need(len(distance)==len(polynomial)==2048 and set(distance)==set(polynomial),'complete phase semigroup is exactly the Z4 quadratic group')
    need(max(distance.values())==5,'every phase attained by at most five genuine columns')
    return distance,polynomial

def spectrum(R2,bits):
    phase=[(1,0),(0,1),(-1,0),(0,-1)]
    cols=[[(k,R2[k][j]*phase[bits[k]][0],R2[k][j]*phase[bits[k]][1])for k in range(8)if R2[k][j]]for j in range(8)]
    re=[[int(i==j)for j in range(8)]for i in range(8)];im=[[0]*8 for _ in range(8)];den=0;maxden=0
    for exponent in range(1,49):
        nr=[[0]*8 for _ in range(8)];ni=[[0]*8 for _ in range(8)]
        for i in range(8):
            for j,col in enumerate(cols):
                x=y=0
                for k,a,b in col:x+=re[i][k]*a-im[i][k]*b;y+=re[i][k]*b+im[i][k]*a
                nr[i][j]=x;ni[i][j]=y
        den+=1
        while den and all(x%2==0 for row in nr+ni for x in row):nr=[[x//2 for x in row]for row in nr];ni=[[x//2 for x in row]for row in ni];den-=1
        re,im=nr,ni;maxden=max(maxden,den)
        if all(im[i][j]==0 and re[i][j]==(2**den if i==j else 0)for i in range(8)for j in range(8)):
            need(48%exponent==0,'every exact first order divides48');return exponent,maxden
    raise ValueError('period48 failed for phase '+str(bits))

def old_lambda(R2,bits):
    J=[(-1)**(z//2)for z in bits]
    M=[[R2[i][j]*J[j]for j in range(8)]for i in range(8)]
    square=[[sum(M[i][k]*M[k][j]for k in range(8))for j in range(8)]for i in range(8)]
    involution=square==[[4*int(i==j)for j in range(8)]for i in range(8)]
    need(involution==(len(set(J))==1),'old-lambda involution iff the half-turn signs are constant')
    return involution

def symplectic_table():
    def multiply(A,B):return [[sum(x*y for x,y in zip(r,c))%2 for c in zip(*B)]for r in A]
    I=[[int(i==j)for j in range(4)]for i in range(4)];H=[[int(j==[3,2,1,0][i])for j in range(4)]for i in range(4)];rows=[]
    for a,b,c in product(range(2),repeat=3):
        D=[r[:]for r in I];D[2][0]=a;D[2][1]=c;D[3][0]=c;D[3][1]=b;S=multiply(D,H);P=[r[:]for r in I];order=None
        for k in range(1,7):
            P=multiply(P,S)
            if P==I:order=k;break
        need(order in(2,3,4,6),'two-qubit symplectic order from exact phase Hessian')
        square_order=order//2 if order%2==0 else order;need(square_order in(1,2,3),'squared action order divides one,two,or three')
        rows.append({'a_parity':a,'b_parity':b,'cross_phase':c,'symplectic_matrix':S,'binary_order_U':order,'binary_order_U_squared':square_order})
    return rows

def outside_family_control(R2,family):
    bits=(0,0,0,1,0,0,0,1);need(bits not in family,'odd quadratic phase genuinely outside the character closure')
    phase=[(1,0),(0,1),(-1,0),(0,-1)];columns=[[(k,R2[k][j]*phase[bits[k]][0],R2[k][j]*phase[bits[k]][1])for k in range(8)if R2[k][j]]for j in range(8)]
    re=[[int(i==j)for j in range(8)]for i in range(8)];im=[[0]*8 for _ in range(8)]
    for _ in range(48):
        nr=[[sum(re[i][k]*a-im[i][k]*b for k,a,b in columns[j])for j in range(8)]for i in range(8)]
        ni=[[sum(re[i][k]*b+im[i][k]*a for k,a,b in columns[j])for j in range(8)]for i in range(8)];re,im=nr,ni
    entry=next(({'row':i,'column':j,'real_error':str(F(re[i][j],2**48)-int(i==j)),'imaginary_error':str(F(im[i][j],2**48))}for i in range(8)for j in range(8)if re[i][j]!=2**48*int(i==j)or im[i][j]),None)
    need(entry is not None,'arbitrary independent port phases can violate period48')
    return {'phase':list(bits),'formula':'x1*x2 with odd coefficient1','forty_eighth_power_nonidentity_entry':entry,'scope':'Excludes extending this theorem to arbitrary independent port phases; no infinite-order claim.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--word',type=Path,default=WORD);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();raw=a.word.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'frozen literal112 source');w=json.loads(gzip.decompress(raw))
    R2,conjugacies=geometry(w);distance,poly=phase_family();records=[];orders=Counter();maxden=0;lambdas=Counter()
    for i,bits in enumerate(sorted(distance)):
        order,den=spectrum(R2,bits);orders[order]+=1;maxden=max(maxden,den);ok=old_lambda(R2,bits);lambdas[ok]+=1;records.append({'phase':list(bits),'quadratic_coefficients':list(poly[bits]),'minimum_width':distance[bits],'order':order,'max_reduced_denominator_power':den,'old_lambda_normalized_involution':ok})
        if i%512==0:print(json.dumps({'checked':i,'total':2048}),flush=True)
    need(dict(orders)=={2:4,4:220,6:256,8:416,12:256,16:384,24:512}and lcm(*orders)==48 and maxden==1,'complete independent exact spectrum')
    one=[r for r in records if r['minimum_width']==1 and 4%r['order']!=0];need(one,'genuine one-column counterexample to fourth-power identity')
    need(all(old_lambda(R2,aff(c,t))for c in range(2)for t in range(8)),'every genuine one-column old-lambda positive control')
    repeated=tuple(2*x for x in aff(0,1));need(repeated in distance and distance[repeated]==2 and not old_lambda(R2,repeated),'width-two repeated-character old-lambda failure')
    result={'status':'PASS_ALL_CLASSES_ALL_WIDTHS_NORMALIZED_CHARACTER_PERIOD48','word_sha256':PIN,'class_conjugacies':conjugacies,'canonical_twice_R':R2,'symplectic_proof_table':symplectic_table(),'phase_count':2048,'minimum_width_histogram':dict(Counter(distance.values())),'order_histogram':dict(orders),'least_common_period':48,'max_reduced_denominator_power':maxden,'one_column_fourth_power_counterexample':one[0],'old_lambda_involution_count':dict(lambdas),'old_lambda_width_two_counterexample':list(repeated),'outside_character_family_control':outside_family_control(R2,distance),'sharp_common_period_witnesses':{str(k):next(r for r in records if r['order']==k)for k in[16,24]},'records':records,'scope':'Exact normalized port matrix diag(i^phase)R0. Every width follows from phase-group closure and all14 source conjugacies. Physical stage adapters, common stage identity, ordinary implementation and productive heads remain separate.'}
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:result[k]for k in['status','phase_count','order_histogram','least_common_period','max_reduced_denominator_power','old_lambda_involution_count']}),flush=True)

if __name__=='__main__':main()
