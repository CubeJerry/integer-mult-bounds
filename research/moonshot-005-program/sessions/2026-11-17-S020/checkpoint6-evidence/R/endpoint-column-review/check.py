"""Independent sparse Q(i) reconstruction of the actual endpoint column."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse, hashlib, importlib.util, json

ARITHMETIC='research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint2-evidence/C/klein-interface-review/check.py'
ARITHMETIC_SHA='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
WORD_SHA='5fc8f08284825e5314edb4b35a19ac8afdf890bfa2a1863fab1d9ab8fac35979'
PROOF_SHA='5eb77f12da9888d1efddf7ba444be788b9ab93b3652700775d3b464da34715ab'

def arithmetic(repo):
    path=repo/ARITHMETIC
    assert hashlib.sha256(path.read_bytes()).hexdigest()==ARITHMETIC_SHA
    spec=importlib.util.spec_from_file_location('independent_column_Qi',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def case(m,width):
    def tensor(B,C):
        return [{i*len(C)+j:m.times(x,y) for i,x in bc.items() for j,y in cc.items()} for bc in B for cc in C]
    def mul(*xs):
        ans=m.eye(len(xs[0]))
        for x in xs:ans=m.mm(ans,x)
        return ans
    def tp(x):
        out=m.eye(1)
        for _ in range(width):out=tensor(out,x)
        return out
    def table(bits,destination,phase):
        return m.mono([[destination(*[(x>>k)&1 for k in range(bits)]),phase(*[(x>>k)&1 for k in range(bits)])%4] for x in range(1<<bits)])
    i16=m.eye(16)
    R=table(4,lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
    Xb=table(4,lambda a,b,c,d:a+2*(b^1)+4*c+8*d,lambda *q:0)
    A=mul(m.add(m.scale(i16,(F(1,2),F(1,2))),m.scale(Xb,(F(1,2),F(-1,2)))),R)
    R2=table(4,lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
    sab=table(4,lambda a,b,c,d:b+2*a+4*c+8*d,lambda *q:0)
    s=table(4,lambda a,b,c,d:a+2*b+4*d+8*c,lambda *q:0)
    s1=table(4,lambda a,b,c,d:d+2*b+4*c+8*a,lambda *q:0)
    g=table(4,lambda a,b,c,d:c+2*b+4*a+8*d,lambda *q:0)
    j=mul(m.star(R2),sab,R2);k=mul(A,j,s,m.star(A));m.table(k)
    zs=table(2,lambda s,t:s+2*t,lambda s,t:2*s)
    zt=table(2,lambda s,t:s+2*t,lambda s,t:2*t)
    xs=table(2,lambda s,t:(s^1)+2*t,lambda *q:0)
    xt=table(2,lambda s,t:s+2*(t^1),lambda *q:0)
    a=tensor(m.eye(4),tp(A));n=len(a);I=m.eye(n);Z=[{} for _ in range(n)]
    S=tensor(zs,tp(s));S1=tensor(zs,tp(s1));T=tensor(zt,m.eye(16**width));X=tensor(xt,m.eye(16**width))
    J=tensor(m.eye(4),tp(j));K=tensor(zs,tp(k));G=tensor(xs,tp(g))
    assert mul(m.star(a),S,a)==S1 and mul(a,J,S,m.star(a))==K
    assert mul(J,S)==mul(S,J) and mul(G,S1,m.star(G))==m.scale(S,-1)
    assert mul(X,T)==m.scale(mul(T,X),-1)
    half=lambda q:m.scale(q,F(1,2))
    P=half(m.add(I,T));N=half(m.add(I,m.scale(T,-1)))
    Ps=half(m.add(I,S));Ns=m.add(I,m.scale(Ps,-1));P1=half(m.add(I,S1));N1=m.add(I,m.scale(P1,-1))
    c=(F(1,2),F(1,2));ci=(F(1),F(-1));neg=lambda x:(-x[0],-x[1])
    def bm(B,C):return [[m.add(*(mul(B[i][k],C[k][j]) for k in range(len(C)))) for j in range(len(C[0]))] for i in range(len(B))]
    def identity():return [[I if i==j else Z for j in range(3)] for i in range(3)]
    def diag(x,y,z):return [[x,Z,Z],[Z,y,Z],[Z,Z,z]]
    def route(i,j,E):
        q=identity();q[i][i]=q[j][j]=m.add(I,m.scale(E,-1));q[i][j]=q[j][i]=E;return q
    C=[[mul(Ps,P),m.scale(Ns,-1),m.scale(mul(Ps,N),-1)],[mul(J,Ns,P),mul(J,Ps),m.scale(mul(J,Ns,N),-1)],[N,Z,P]]
    p=N;z=mul(X,P,N1);w=mul(X,G,P,P1)
    assert m.add(mul(m.star(p),p),mul(m.star(z),z),mul(m.star(w),w))==I
    assert mul(P,z)==mul(P,w)==Z and mul(S1,z)==m.scale(z,-1) and mul(S,w)==m.scale(w,-1)
    Q=bm(bm(diag(I,X,mul(X,G)),route(1,2,mul(P,N1))),route(0,2,N))
    assert [Q[i][2] for i in range(3)]==[p,z,w]
    O0=[[P,m.scale(N,c),m.scale(N,neg(c))],[mul(P,X),m.scale(N,c),m.scale(N,c)],[Z,m.add(P,m.scale(N,c)),mul(N,X)]]
    H=[[I,m.scale(m.star(K),-1),Z],[I,m.star(K),Z],[Z,Z,I]]
    Hi=[[half(I),half(I),Z],[m.scale(K,F(-1,2)),half(K),Z],[Z,Z,I]]
    assert bm(H,Hi)==bm(Hi,H)==identity();O=bm(Hi,O0)
    B=m.add(N,m.scale(P,ci));CG=m.add(N,mul(P,G));E21=identity();E21[2][1]=mul(S,J)
    I0=bm(bm(bm(E21,diag(I,m.scale(X,-1),mul(X,CG))),route(1,2,mul(P,N1))),diag(m.add(N,m.scale(P,c)),I,B))
    ell=m.add(m.scale(m.add(m.scale(mul(S,J,z),-1),w),ci),mul(X,p))
    assert [I0[i][2] for i in range(3)]==[Z,m.scale(z,neg(ci)),ell]
    L=[[a,Z,Z],[I,a,Z],[Z,Z,I]];U=[[a,m.scale(mul(a,a),-1),Z],[Z,a,Z],[Z,Z,I]]
    D=diag(m.power(a,4),m.power(a,2),a)
    E=bm(bm(bm(bm(L,C),U),Q),L);target=bm(bm(O,D),I0)
    assert [E[i][2] for i in range(3)]==[target[i][2] for i in range(3)]
    x=mul(a,m.add(m.scale(mul(S,J,z),-1),w))
    full_column=[[m.add(m.scale(mul(a,a,z),-1),m.scale(x,-1))],[m.add(m.scale(mul(a,a,z),-1),x)],[m.add(m.scale(mul(a,a,z),-1),mul(a,p))]]
    assert bm(bm(bm(H,L),C),bm(U,[[p],[z],[w]]))==full_column
    mon={'I':I,'S':S,'T':T,'minusT':m.scale(T,-1),'J':J,'K':K,'X':X,'XG':mul(X,G),'H1':m.add(N,mul(P,S1)),'DN':m.add(P,m.scale(N,(F(0),F(1)))),'minusX':m.scale(X,-1),'XCG':mul(X,CG),'SJ':mul(S,J),'minusSJ':m.scale(mul(S,J),-1)}
    for q in mon.values():m.table(q);assert mul(q,m.star(q))==I
    units={'C':C,'Q0':Q,'O0':O0,'O':O,'I0':I0}
    return locals()

def primitive_replay(m,c,word,omit=None,measure=False):
    B=c['identity']();maximum=F(1);n=c['n']
    for index,op in enumerate(word):
        if index==omit:continue
        kind=op['op']
        if kind=='ADD':
            dst,src=op['target'],op['source'];assert dst!=src
            B[dst]=[m.add(x,y) for x,y in zip(B[dst],B[src])]
        elif kind=='SCALE':
            cf=tuple(map(F,op['coefficient']));assert cf!=(0,0)
            assert all(x.denominator&(x.denominator-1)==0 for x in cf)
            bank=op['bank'];B[bank]=[m.scale(x,cf) for x in B[bank]]
        else:
            assert kind=='MONO';g=c['mon'][op['name']]
            if op['inverse']:g=m.star(g)
            bank=op['bank'];B[bank]=[m.mm(g,x) for x in B[bank]]
        if measure:
            for row in B:
                norm=[F(0)]*n
                for block in row:
                    for col in block:
                        for i,(re,im) in col.items():norm[i]+=abs(re)+abs(im)
                maximum=max(maximum,*norm)
    return B,maximum

def verify_uniform_bound(m,macros,word):
    # Source cancellation is used only after explicit inverse instructions.
    compiled=[];b=[F(1)]*3;peak=F(1)
    for op in macros:
        if op['op']!='SHEAR':
            compiled.append(op)
            if op['op']=='ADD':b[op['target']]+=b[op['source']]
            elif op['op']=='SCALE':
                re,im=map(F,op['coefficient']);b[op['bank']]*=abs(re)+abs(im)
            peak=max(peak,*b);continue
        dst,src=op['target'],op['source'];assert dst!=src
        original=b[src]
        for name,raw in op['terms']:
            cf=tuple(map(F,raw));assert cf!=(0,0)
            weight=abs(cf[0])+abs(cf[1]);peak=max(peak,original*weight)
            mono=lambda inverse:{'op':'MONO','name':name,'bank':src,'inverse':inverse}
            scal=lambda value:{'op':'SCALE','bank':src,'coefficient':list(map(str,value))}
            if name!='I':compiled.append(mono(False))
            if cf!=(1,0):compiled.append(scal(cf))
            compiled.append({'op':'ADD','target':dst,'source':src})
            b[dst]+=original*weight;peak=max(peak,*b)
            if cf!=(1,0):compiled.append(scal(m.div((F(1),F(0)),cf)))
            if name!='I':compiled.append(mono(True))
    assert compiled==word
    return peak

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    assert hashlib.sha256((args.author/'WORDS.json').read_bytes()).hexdigest()==WORD_SHA
    assert hashlib.sha256((args.author/'PROOF.md').read_bytes()).hexdigest()==PROOF_SHA
    m=arithmetic(args.repo);words=json.loads((args.author/'WORDS.json').read_text())
    expected={'C':((8,8,5),(8,8,5)),'Q0':((8,8,4),(8,8,4)),'O0':((20,28,15),(20,28,15)),'O':((22,32,16),(22,30,16)),'I0':((14,20,13),(14,20,13))}
    author=json.loads((args.author/'RESULT.json').read_text());cases=[];controls=0
    for width in[0,1]:
        c=case(m,width);receipt={}
        for name,ws in words.items():
            forward,pf=primitive_replay(m,c,ws['forward'],measure=True)
            inverse,pb=primitive_replay(m,c,ws['inverse'],measure=True)
            assert forward==c['units'][name]
            assert c['bm'](forward,inverse)==c['bm'](inverse,forward)==c['identity']()
            bounds={};counts={}
            for j,direction in enumerate(['forward','inverse']):
                count=Counter(op['op'] for op in ws[direction]);assert tuple(count[k] for k in['ADD','SCALE','MONO'])==expected[name][j]
                uniform=verify_uniform_bound(m,ws[direction+'_macros'],ws[direction]);assert str(uniform)==author['receipts'][name]['uniform_triangle_prefix_'+direction]
                assert (pf if j==0 else pb)<=uniform
                bounds[direction]=str(uniform);counts[direction]=dict(count)
                if width==1 and name!='O0':
                    target=forward if j==0 else inverse
                    for k,op in enumerate(ws[direction]):
                        if op['op']=='ADD':assert primitive_replay(m,c,ws[direction],omit=k)[0]!=target;controls+=1
            receipt[name]={'counts':counts,'uniform_triangle_bounds':bounds,'exact_reduced_prefix_bounds':{'forward':str(pf),'inverse':str(pb)}}
            print('reviewed tail width',width,name,flush=True)
        assert c['E']!=c['target']
        witness=m.add(c['E'][0][0],m.scale(c['target'][0][0],-1))[0].get(0,m.Z)
        if width==1:assert witness==(F(-3,16),F(5,16))
        wrongG=c['tensor'](m.eye(4),c['tp'](c['g']))
        assert c['mul'](wrongG,c['S1'],m.star(wrongG))==c['S']
        assert c['mul'](wrongG,c['S1'],m.star(wrongG))!=m.scale(c['S'],-1)
        cases.append({'tail_width':width,'all_unit_input_columns':3*c['n'],'endpoint_column_inputs':c['n'],'source_relations':True,'units':receipt,'missing_distinguished_sigma_flip_rejected':True,'full_identity_false':True,'defect_row0_column0':[str(x) for x in witness]})
    assert controls==104
    result={'status':'PASS_INDEPENDENT_PREFIX_THREE_BANK_ENDPOINT_COLUMN','arithmetic_sha256':ARITHMETIC_SHA,'author_words_sha256':WORD_SHA,'author_proof_sha256':PROOF_SHA,'cases':cases,'omitted_ADD_controls':controls,'all_width_proof_basis':'Exact fixed-prefix Pauli relations and tensoring of literal one-tail source equalities; every coefficient service and inverse is physically replayed.','scope':'Positive single input column with actual invertible ordinary endpoints. Full three-input identity is explicitly false for these endpoint words. No supplier and no new complete kappa.','new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],controls,'omission controls',flush=True)

if __name__=='__main__':main()
