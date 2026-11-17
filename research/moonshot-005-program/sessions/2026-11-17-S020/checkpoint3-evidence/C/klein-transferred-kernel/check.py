#!/usr/bin/env python3
"""Exact dyadic kernel transfer and executable coupled second interface."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse, hashlib, importlib.util, json


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--arithmetic',type=Path,default=Path(__file__).parents[1]/'klein-interface-review/check.py')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(args.arithmetic.read_bytes()).hexdigest()=='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
    spec=importlib.util.spec_from_file_location('independent_qi',args.arithmetic);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    I=m.eye();Z=[{}for _ in range(16)]
    def prod(*xs):
        ans=I
        for x in xs:ans=m.mm(ans,x)
        return ans
    source=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
    Xb=m.mono([[x^2,0]for x in range(16)])
    A=prod(m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(Xb,(F(1,2),F(-1,2)))),source);U=m.power(A,2)
    s=m.mono([[(x&3)|((x&4)<<1)|((x&8)>>1),0]for x in range(16)])
    t=m.mono([[x^12,0]for x in range(16)])
    s1=prod(m.star(A),s,A);s2=prod(m.star(U),s,U);t2=prod(m.star(U),t,U)
    h_table=[]
    for x in range(16):
        a,c,d=x&1,(x>>2)&1,(x>>3)&1
        delta=int(a==d);h_table.append([x^(4*delta),((1-2*c)*delta)%4])
    h=m.mono(h_table)
    G=m.mono([[d,2 if x in(13,15)else 0]for x,d in enumerate([0,1,3,5,7,9,4,13,2,8,6,11,10,15,14,12])])
    assert prod(h,h)==I and prod(s1,h)==prod(h,s1)
    transported_h=prod(U,h,m.star(U));m.table(transported_h)
    assert prod(G,s1,m.star(G))==s2
    assert prod(G,h,m.star(G))==prod(s2,t2)
    R=m.scale(prod(m.add(I,m.scale(s2,-1)),m.add(I,m.scale(t2,-1))),F(1,4))
    N=m.scale(prod(m.add(I,m.scale(s1,-1)),m.add(I,h)),F(1,4))
    P=m.add(I,m.scale(N,-1));V=prod(G,N);Vi=m.star(V)
    assert prod(N,N)==N and prod(R,R)==R
    assert prod(Vi,V)==N and prod(V,Vi)==R
    assert prod(R,V)==V and m.trace(N)==m.trace(R)==(4,0)
    E=m.scale(prod(m.add(I,s2),m.add(I,t2)),F(1,4));M=m.add(I,m.scale(E,-1));PR=m.add(I,m.scale(R,-1))
    g=prod(m.star(source),Xb)
    assert prod(A,g,A)==source and prod(U,g,A)==prod(A,source)
    # The right support of P_H(s1-I) is covered by N: h lies in H and
    # commutes with s1, so P_H(s1-I)(I-N)=0 in the coset module.
    assert prod(s1,N)==m.scale(N,-1) and prod(h,N)==N
    assert m.col_rank(m.stack(P,V))==16
    monos={'I':I,'s2':s2,'t2':t2,'s2t2':prod(s2,t2),'g':g,'g_inverse':m.star(g)}
    Vterms=[];Viterms=[]
    for n,B,c in [('G',G,F(1,4)),('Gs1',prod(G,s1),F(-1,4)),('Gh',prod(G,h),F(1,4)),('Gs1h',prod(G,s1,h),F(-1,4))]:
        monos[n]=B;monos[n+'_inverse']=m.star(B);Vterms.append((n,c));Viterms.append((n+'_inverse',c))
    for n in ['s2','t2','s2t2']:
        monos[n+'_inverse']=m.star(monos[n])
    def shear(i,j,terms):
        ops=[]
        for name,c in terms:
            if name=='I' and c==1:ops.append({'op':'ADD','source':j,'target':i});continue
            if name!='I':ops.append({'op':'MONO','bank':j,'name':name})
            ops += [{'op':'SCALE','bank':j,'coefficient':str(c)},{'op':'ADD','source':j,'target':i},{'op':'SCALE','bank':j,'coefficient':str(1/c)}]
            if name!='I':ops.append({'op':'MONO','bank':j,'name':name[:-8]if name.endswith('_inverse')else name+'_inverse'})
        return ops
    def vrot(inverse=False):
        signs=(-1,1,-1)if inverse else(1,-1,1)
        return sum((shear(i,j,[(n,sgn*c)for n,c in terms])for(i,j),terms,sgn in zip([(1,0),(0,1),(1,0)],[Vterms,Viterms,Vterms],signs)),[])
    def mrot(inverse=False):
        signs=(-1,1,-1)if inverse else(1,-1,1)
        return sum((shear(i,j,[('I',F(sgn))]+[(n,F(-sgn,4))for n in ['I','s2','t2','s2t2']])for(i,j),sgn in zip([(1,0),(0,1),(1,0)],signs)),[])
    swap=[{'op':'ADD','source':0,'target':2},{'op':'SCALE','bank':2,'coefficient':'-1'},{'op':'ADD','source':2,'target':0},{'op':'SCALE','bank':0,'coefficient':'-1'},{'op':'ADD','source':0,'target':2},{'op':'SCALE','bank':2,'coefficient':'-1'}]
    words={'Q_column':swap+vrot(),'Q_column_inverse':vrot(True)+swap,
           'Q_high_low':[{'op':'MONO','bank':1,'name':'g'}]+mrot()+swap+vrot(),
           'Q_high_low_inverse':vrot(True)+swap+mrot(True)+[{'op':'MONO','bank':1,'name':'g_inverse'}]}
    def replay(word):
        X=[[I if i==j else Z for j in range(3)]for i in range(3)];bounds=[F(1)]*3;peak=F(1)
        for op in word:
            if op['op']=='ADD':
                i,j=op['target'],op['source'];X[i]=[m.add(a,b)for a,b in zip(X[i],X[j])];bounds[i]+=bounds[j]
            elif op['op']=='SCALE':
                i,c=op['bank'],F(op['coefficient']);assert c and c.denominator&(c.denominator-1)==0
                X[i]=[m.scale(a,c)for a in X[i]];bounds[i]*=abs(c)
            else:
                i=op['bank'];X[i]=[prod(monos[op['name']],a)for a in X[i]]
            peak=max(peak,*bounds)
        return X,peak
    def bm(X,Y):return [[m.add(*(prod(X[i][k],Y[k][j])for k in range(3)))for j in range(3)]for i in range(3)]
    id3=[[I if i==j else Z for j in range(3)]for i in range(3)]
    expected_column=[[Z,m.scale(Vi,-1),P],[Z,PR,V],[I,Z,Z]]
    expected_hl=[[m.scale(prod(Vi,M),-1),m.scale(prod(Vi,E,g),-1),P],[prod(PR,M),prod(E,g),V],[E,m.scale(prod(M,g),-1),Z]]
    all_outputs={n:replay(w)[0]for n,w in words.items()}
    assert all_outputs['Q_column']==expected_column and all_outputs['Q_high_low']==expected_hl
    for n in ['Q_column','Q_high_low']:
        assert bm(all_outputs[n],all_outputs[n+'_inverse'])==bm(all_outputs[n+'_inverse'],all_outputs[n])==id3
    receipts={n:{'counts':dict(Counter(o['op']for o in w)),'prefix_bound':str(replay(w)[1])}for n,w in words.items()}
    # Essential phase controls.
    h_unphased=m.mono([[d,0]for d,q in h_table]);G_unphased=m.mono([[d,0]for d,q in m.table(G)])
    def ismono(B):
        try:m.table(B);return True
        except AssertionError:return False
    assert not ismono(prod(U,h_unphased,m.star(U)))
    assert prod(G_unphased,h,m.star(G_unphased))!=prod(s2,t2)
    assert not ismono(prod(U,s1,m.star(U)))
    result={'status':'PASS_EXPLICIT_DYADIC_KLEIN_KERNEL_TRANSFER','N0_rank':'D/4','N0_regular_trace':'1/4','N0_augmentation':0,
            'identities':['A² h A^-2 ordinary','G s1 G^-1=s2','G h G^-1=s2 t2','G N0 G^-1=R2','V*V=N0','VV*=R2'],
            'old_irrep_comparison':'Resolved positively: N<=N0 and N0 is ordinarily unitarily equivalent to R2.',
            'last_column':'(I-N0,G N0,0)^T; isometric and satisfies the Gaussian2 left-coset condition.',
            'actual_words':receipts,'scope':'Coupled second-interface source bridge. Remaining forbidden classes and independent endpoint equations are not solved.',
            'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'WORDS.json').write_text(json.dumps({'words':words,'tables':{n:m.table(B)for n,B in monos.items()},'h':h_table,'G':m.table(G),'A2_h_Aminus2':m.table(transported_h)},indent=2)+'\n')
    print(result['status'],json.dumps(receipts))


if __name__=='__main__':main()
