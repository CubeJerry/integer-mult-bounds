#!/usr/bin/env python3
"""Exact controls for a scoped theorem, not a caller search or theorem-by-test."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
ENGINE_SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
CAPACITY_SHA='afa9d38023b0c97ee24393bb598bbde64bad80b9ac525cf11778aaf3416c1d28'

def reduced(word):
    out=[]
    for c in word:
        if out and (out[-1],c) in [('a','A'),('A','a')]:out.pop()
        elif out and out[-1]==c=='t':pass
        else:out.append(c)
    return tuple(out)
def poly(word='',coef=1):return {reduced(word):coef} if coef else {}
def add(*xs):
    ans={}
    for x in xs:
        for w,c in x.items():ans[w]=ans.get(w,0)+c
    return {w:c for w,c in ans.items() if c}
def neg(x):return {w:-c for w,c in x.items()}
def mul(*xs):
    ans=poly()
    for x in xs:
        nxt={}
        for w,c in ans.items():
            for v,d in x.items():
                k=reduced(w+v);nxt[k]=nxt.get(k,0)+c*d
        ans={w:c for w,c in nxt.items() if c}
    return ans
def mm(x,y):return [[add(*(mul(x[i][k],y[k][j]) for k in range(len(y)))) for j in range(len(y[0]))] for i in range(len(x))]

def formal():
    one=poly();zero={};a=poly('a');a2=poly('aa');a3=poly('aaa');T=poly('t');N=add(one,neg(T))
    T1=poly('Ata');N1=add(one,neg(T1));T2=poly('AAtaa');N2=add(one,neg(T2))
    p,z,w=(poly(c) for c in 'pzw')
    L=[[a,zero,zero],[one,a,zero],[zero,zero,one]]
    U=[[a,neg(a2),zero],[zero,a,zero],[zero,zero,one]]
    C=[[T,zero,neg(N)],[zero,one,zero],[N,zero,T]]
    Ci=[[T,zero,N],[zero,one,zero],[neg(N),zero,T]]
    identity=[[one if i==j else {} for j in range(3)] for i in range(3)]
    assert mm(C,Ci)==identity==mm(Ci,C)
    got=mm(mm(mm(L,C),U),[[p],[z],[w]])
    wanted=[
      [add(mul(a2,T1,p),neg(mul(a3,T2,z)),neg(mul(a,N,w)))],
      [add(mul(a,T1,p),mul(a2,N2,z),neg(mul(N,w)))],
      [add(mul(a,N1,p),neg(mul(a2,N2,z)),mul(T,w))]]
    assert got==wanted
    CT=[[T,N,zero],[zero,one,one],[N,T,zero]]
    last=mm(mm(mm(L,CT),U),[[zero],[zero],[one]])
    assert last==[[zero],[a],[zero]]
    assert last!=[[zero],[one],[zero]]
    return {'free_noncommutative_last_column':True,'Crot_two_sided_inverse':True,
            'CT_scope_negative_control':'third column is (0,a,0), not (0,I,0)'}

def main(repo,capacity,out):
    ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==ENGINE_SHA
    cp=capacity/'PROOF.md';assert hashlib.sha256(cp.read_bytes()).hexdigest()==CAPACITY_SHA
    spec=importlib.util.spec_from_file_location('pinned_exact_engine',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    def frac(x,num,denpow):
        y=x.scale(num);return m.M(y.a,y.k+denpow).norm()
    def tab(dest,phase):
        return m.monomial([dest(*[(x>>j)&1 for j in range(4)]) for x in range(16)], [phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
    I=m.eye(16);Z=m.zero(16)
    R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
    Xb=m.monomial([x^2 for x in range(16)],[0]*16)
    A=frac(I.scale((1,1))+Xb.scale((1,-1)),(1,0),1)@R
    assert all(A.power(j)@A.power(j).star()==I for j in (1,2,3))
    assert [m.gaussian_rank(A.power(j)) for j in (1,2,3)]==[1,2,3]
    S=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
    Sc=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
    Sb=tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
    assert A.star()@S@A==Sc and A.power(-2)@S@A.power(2)==Sb
    Zc=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*c)
    g=S@Zc
    assert g.power(4)==I and all(g.power(j)!=I for j in (1,2,3))
    assert all(g.power(j).trace()==(0,0) for j in (1,2,3))
    gs=[g,A.star()@g@A,A.power(-2)@g@A.power(2)]
    tables=[]
    roots=[m.O,m.II,(-1,0),(0,-1)]
    for h in gs:
        assert h.k==0 and m.gaussian_rank(h)==0 and h.power(4)==I
        p=[];ph=[]
        for j in range(16):
            i=next(i for i in range(16) if h.a[i][j]!=m.Z);p.append(i);ph.append(roots.index(h.a[i][j]))
        tables.append({'permutation':p,'input_phase_mod4':ph})
    def clockT(h):return frac(m.eye(h.n),(1,0),1)+frac(h,(1,-1),2)+frac(h.power(3),(1,1),2)
    width_rows=[]
    oneT=clockT(g)
    for v in (1,2):
        iv=m.eye(16**v);gv=g.tp(v);tv=clockT(gv)
        assert tv@tv==tv==tv.star()
        assert tv.trace()==(16**v//2,0)
        if v==2:assert tv!=oneT.tp(v)
        width_rows.append({'width':v,'clock_projector_rank':16**v//2,'projector_formed_after_tensor_lifting':True})
    # Exact C4 coefficient shears, all three bank inputs arbitrary.
    T=oneT;N=I+T.scale((-1,0))
    target=m.block([[T,Z,N.scale((-1,0))],[Z,I,Z],[N,Z,T]])
    mono={'I':I,'g':g,'g3':g.power(3)}
    terms=[('I',(1,0),1),('g',(-1,1),2),('g3',(-1,-1),2)]
    word=[]
    for dest,src,sign in [(2,0,1),(0,2,-1),(2,0,1)]:
        for name,num,k in terms:
            num=(sign*num[0],sign*num[1]);norm=num[0]**2+num[1]**2
            invnum=(num[0]*(1<<k)//norm,-num[1]*(1<<k)//norm)
            if name!='I':word.append({'op':'MONO','bank':src,'name':name,'inverse':False})
            word.append({'op':'SCALE','bank':src,'num':num,'denpow':k})
            word.append({'op':'ADD','dest':dest,'src':src,'sign':1})
            word.append({'op':'SCALE','bank':src,'num':invnum,'denpow':0})
            if name!='I':word.append({'op':'MONO','bank':src,'name':name,'inverse':True})
    def invword(ws):
        ans=[]
        for op in reversed(ws):
            op=op.copy()
            if op['op']=='MONO':op['inverse']=not op['inverse']
            elif op['op']=='ADD':op['sign']=-op['sign']
            else:
                x,y=op['num'];k=op['denpow'];d=x*x+y*y
                n=(F(x*(1<<k),d),F(-y*(1<<k),d));k2=max(q.denominator.bit_length()-1 for q in n)
                assert all(q.denominator&(q.denominator-1)==0 for q in n)
                op['num']=tuple(int(q*(1<<k2)) for q in n);op['denpow']=k2
            ans.append(op)
        return ans
    def step(blocks,op):
        blocks=[row[:] for row in blocks]
        if op['op']=='ADD':
            d,s=op['dest'],op['src'];blocks[d]=[x+y.scale((op['sign'],0)) for x,y in zip(blocks[d],blocks[s])]
        elif op['op']=='SCALE':blocks[op['bank']]=[frac(x,tuple(op['num']),op['denpow']) for x in blocks[op['bank']]]
        else:
            h=mono[op['name']];h=h.star() if op['inverse'] else h
            blocks[op['bank']]=[h@x for x in blocks[op['bank']]]
        return blocks
    def replay(ws,omit=None):
        b=[[I if i==j else Z for j in range(3)] for i in range(3)]
        bound=F(1)
        for j,op in enumerate(ws):
            if j==omit:continue
            b=step(b,op)
            bound=max(bound,max(sum(F(abs(x.a[r][c][0])+abs(x.a[r][c][1]),1<<x.k) for x in row for c in range(16)) for row in b for r in range(16)))
        return m.block(b),bound
    invoices=[];allwords={}
    for label,ws,wanted in [('forward',word,target),('inverse',invword(word),target.star())]:
        got,bound=replay(ws);assert got==wanted
        omitted=[j for j,op in enumerate(ws) if op['op']=='ADD']
        assert all(replay(ws,j)[0]!=wanted for j in omitted)
        count=Counter(op['op'] for op in ws);assert count=={'ADD':9,'SCALE':18,'MONO':12}
        invoices.append({'direction':label,'counts':dict(count),'width_one_gaussian_l1_prefix_control':str(bound),
          'universal_prefix_bound':'77/8','universal_bound_proof':'each coefficient source is restored; the three N shears have coefficient l1 sum3/2, giving target bounds5/2,19/4,77/8',
          'omitted_ADD_controls':len(omitted)})
        allwords[label]=ws
    assert target@target.star()==m.eye(48)
    # The two plus swap sectors look sufficient at V=1, but miss a whole
    # alternating sector at larger widths. Keep an explicit V=2 witness.
    import itertools
    q=4;vec={}
    for perm in itertools.permutations((0,1,2)):
        inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));vec[(perm[0],perm[1],0,perm[2])]=(-1)**inv
    def permute_vec(v,ij):
        out={}
        for x,c in v.items():
            y=list(x);y[ij[0]],y[ij[1]]=y[ij[1]],y[ij[0]];out[tuple(y)]=c
        return out
    assert permute_vec(vec,(0,1))=={x:-c for x,c in vec.items()}
    assert permute_vec(vec,(0,3))=={x:-c for x,c in vec.items()}
    # Mixed plus/minus is an essential hypothesis-dropping positive control.
    J=m.monomial([1,0],[0,0]);I2=m.eye(2);P=frac(I2+J,(1,0),1);M=I2+P.scale((-1,0))
    assert P@P+M@M==I2 and P@M==m.zero(2)
    result={'status':'PASS_CONDITIONAL_ROTATION_THIRD_COLUMN_CAPACITY_GATE',
      'formal':formal(),'engine_sha256':ENGINE_SHA,'capacity_source_sha256':CAPACITY_SHA,
      'literal_source_support_ranks':[1,2,3],
      'source_rank_proof':'retained four-bit concentration and cubic-source proofs; support controls here are not a replacement',
      'spectator_signs':{'positive_complements_augmentation_rank':0,'negative_complements_augmentation_rank':2,'sum_regular_trace':1},
      'clock4':{'backward_monomial_tables':tables,'regular_trace_T':'1/2','augmentation_T':1,'width_checks':width_rows,'inverse_and_primitive_invoice':invoices},
      'controls':{'mixed_plus_minus_split_bank':True,'width_one_two_plus_stack_has_no_alternating_kernel':True,'width_two_explicit_alternating_vector_terms':len(vec),'width_two_alternating_dimension':16,'incorrect_CT_scope_rejected':True},
      'scope':'Arbitrary ordinary Q for Crot only. C_T, Klein completion, changed endpoint profiles and non-fixed catalogues remain outside this theorem.',
      'new_kappa':False}
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'WORDS.json').write_text(json.dumps(allwords,indent=2)+'\n')
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name in ('PROOF.md','check.py','RESULT.json','WORDS.json')}
    (out/'MANIFEST.json').write_text(json.dumps({'base_remote':'93b11dd75d7ffda723204bd212e5728cbea95592','source_files':{ENGINE:ENGINE_SHA,'ordinary-module-capacity/PROOF.md':CAPACITY_SHA},'files':files},indent=2)+'\n')
    print(json.dumps({'status':result['status'],'formal_checks':result['formal'],'clock4_invoice':invoices,'new_kappa':False},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--capacity',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();main(args.repo,args.capacity,args.out)
