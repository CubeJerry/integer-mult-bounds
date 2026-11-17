#!/usr/bin/env python3
"""Literal premises and executable coupled Q; independent of B's engine."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse, hashlib, importlib.util, json


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--arithmetic',type=Path,default=Path(__file__).parents[1]/'klein-interface-review/check.py')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(args.arithmetic.read_bytes()).hexdigest()
    assert digest=='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
    spec=importlib.util.spec_from_file_location('independent_qi_columns',args.arithmetic)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    I=m.eye();Z=[{}for _ in range(16)]
    S=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
    Xb=m.mono([[x^2,0]for x in range(16)])
    Cb=m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(Xb,(F(1,2),F(-1,2))))
    A=m.mm(Cb,S);U=m.power(A,2)
    s=m.mono([[(x&3)|((x&4)<<1)|((x&8)>>1),0]for x in range(16)])
    t=m.mono([[x^12,0]for x in range(16)])
    s1=m.mm(m.mm(m.star(A),s),A);t1=m.mm(m.mm(m.star(A),t),A)
    s2=m.mm(m.mm(m.star(U),s),U);t2=m.mm(m.mm(m.star(U),t),U)
    Ht=m.mm(m.mm(A,t),m.star(A))
    witness=m.mm(m.mm(m.mm(m.mm(U,s1),t2),s1),m.star(U))
    m.table(witness)
    def ismono(B):
        try:m.table(B);return True
        except AssertionError:return False
    assert not ismono(m.mm(m.mm(U,s1),m.star(U)))
    assert m.mm(m.mm(U,t1),m.star(U))==Ht
    assert m.mm(s2,t2)==m.mm(t2,s2)
    for h in [s2,t2,m.mm(s2,t2)]:assert ismono(m.mm(m.mm(U,h),m.star(U)))
    g=m.mm(m.star(S),Xb)
    assert m.mm(m.mm(A,g),A)==S
    assert m.mm(m.mm(U,g),A)==m.mm(A,S)
    mono={'I':I,'s2':s2,'t2':t2,'s2t2':m.mm(s2,t2),'g':g,'g_inverse':m.star(g)}
    def proj(u,v):return m.scale(m.add(I,m.scale(s2,u),m.scale(t2,v),m.scale(m.mm(s2,t2),u*v)),F(1,4))
    R=proj(-1,-1);E=proj(1,1);P=m.add(I,m.scale(R,-1));M=m.add(I,m.scale(E,-1));T=m.add(P,m.scale(E,-1))
    assert m.mm(R,R)==R and m.mm(E,E)==E and m.mm(R,E)==Z
    expected=[[m.scale(R,-1),Z,P],[T,m.mm(E,g),R],[E,m.scale(m.mm(M,g),-1),Z]]
    def shear(i,j,terms):
        ops=[]
        for name,c in terms:
            c=F(c)
            if c==1 and name=='I':ops.append({'op':'ADD','source':j,'target':i});continue
            if name!='I':ops.append({'op':'MONO','bank':j,'name':name})
            ops += [{'op':'SCALE','bank':j,'coefficient':str(c)},{'op':'ADD','source':j,'target':i},{'op':'SCALE','bank':j,'coefficient':str(1/c)}]
            if name!='I':ops.append({'op':'MONO','bank':j,'name':name})
        return ops
    rterms=list(zip(['I','s2','t2','s2t2'],[F(1,4),F(-1,4),F(-1,4),F(1,4)]))
    eterms=[(name,F(1,4))for name in ['I','s2','t2','s2t2']]
    def pshear(i,j,kind,sgn):
        terms=[(n,sgn*c)for n,c in rterms]if kind=='R'else[('I',F(sgn))]+[(n,-sgn*c)for n,c in eterms]
        return shear(i,j,terms)
    def rotation(kind,inverse=False):
        signs=(-1,1,-1)if inverse else(1,-1,1)
        return sum((pshear(i,j,kind,sgn)for(i,j),sgn in zip([(1,0),(0,1),(1,0)],signs)),[])
    swap=[{'op':'ADD','source':0,'target':2},{'op':'SCALE','bank':2,'coefficient':'-1'},{'op':'ADD','source':2,'target':0},{'op':'SCALE','bank':0,'coefficient':'-1'},{'op':'ADD','source':0,'target':2},{'op':'SCALE','bank':2,'coefficient':'-1'}]
    words={'Q':[{'op':'MONO','bank':1,'name':'g'}]+rotation('M')+swap+rotation('R'),'Q_inverse':rotation('R',True)+swap+rotation('M',True)+[{'op':'MONO','bank':1,'name':'g_inverse'}]}
    def replay(word):
        X=[[I if i==j else Z for j in range(3)]for i in range(3)];bounds=[F(1)]*3;peak=F(1)
        for op in word:
            if op['op']=='ADD':
                i,j=op['target'],op['source'];X[i]=[m.add(a,b)for a,b in zip(X[i],X[j])];bounds[i]+=bounds[j]
            elif op['op']=='SCALE':
                i,c=op['bank'],F(op['coefficient']);assert c and c.denominator&(c.denominator-1)==0
                X[i]=[m.scale(a,c)for a in X[i]];bounds[i]*=abs(c)
            else:
                i=op['bank'];X[i]=[m.mm(mono[op['name']],a)for a in X[i]]
            peak=max(peak,*bounds)
        return X,peak
    def bm(X,Y):return [[m.add(*(m.mm(X[i][k],Y[k][j])for k in range(3)))for j in range(3)]for i in range(3)]
    Q,qp=replay(words['Q']);Qi,qip=replay(words['Q_inverse']);assert Q==expected
    id3=[[I if i==j else Z for j in range(3)]for i in range(3)]
    assert bm(Q,Qi)==bm(Qi,Q)==id3
    receipts={n:{'counts':dict(Counter(o['op']for o in w)),'prefix_bound':str(replay(w)[1])}for n,w in words.items()}
    # U*s1*R vanishes after identifying words differing by a left ordinary
    # monomial.  U*s1 itself and U belong to different left cosets.
    reps=[m.mm(m.mm(U,s1),h)for h in [I,s2,t2,m.mm(s2,t2)]]
    equality=[[ismono(m.mm(x,m.star(y)))for y in reps]for x in reps]
    assert equality==[[True,False,True,False],[False,True,False,True],[True,False,True,False],[False,True,False,True]]
    assert ismono(m.mm(m.mm(m.mm(U,s1),t1),m.star(m.mm(U,s1))))
    # Exact quartic column of this explicit Q has complementary Ht sectors.
    ph=m.scale(m.add(I,Ht),F(1,2));mh=m.add(I,m.scale(ph,-1))
    A4=m.power(A,4);B2=m.mm(m.mm(A,s),m.power(A,3))
    plusminus=m.scale(m.add(I,s,m.scale(t,-1),m.scale(m.mm(s,t),-1)),F(1,4))
    minusplus=m.scale(m.add(I,m.scale(s,-1),t,m.scale(m.mm(s,t),-1)),F(1,4))
    assert m.mm(m.mm(A,plusminus),m.power(A,3))==m.scale(m.mm(mh,m.add(A4,B2)),F(1,2))
    assert m.mm(m.mm(A,minusplus),m.power(A,3))==m.scale(m.mm(ph,m.add(A4,m.scale(B2,-1))),F(1,2))
    assert m.col_rank(m.stack(mh,ph))==16
    vectors=[['1/2','1','0'],['1/2','0','0']]
    result={'status':'PASS_EXACT_KLEIN_COUPLED_COLUMN_PREMISES','return_identity':'A g A=R_source; A² g A=A R_source','actual_Q_and_inverse':receipts,'Q_scope':'Explicit coupled unit has a full rank-D quartic component but is excluded from a 421 completion by its fixed last-column left-coset rank2.','last_column_Gaussian2_left_coset_vectors':vectors,'left_coset_rank':2,'necessary_character_capacity':'dim V^H - dim V^<H,s1> <= rank rho(R2) for every ordinary-group irrep','character_capacity_not_evaluated':True,'new_complete_kappa':False,'arithmetic_sha256':digest}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'WORDS.json').write_text(json.dumps({'words':words,'tables':{n:m.table(v)for n,v in mono.items()},'ordinary_conjugacy_witness':m.table(witness),'coset_equality':equality},indent=2)+'\n')
    print(result['status'],json.dumps(receipts))


if __name__=='__main__':main()
