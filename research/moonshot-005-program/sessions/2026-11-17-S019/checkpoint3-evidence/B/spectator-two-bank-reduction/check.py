#!/usr/bin/env python3
"""Exact controls for the two-bank spectator reduction; the universal proof is PROOF.md."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,importlib.util,sys,json,hashlib,random,itertools
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();args.out.mkdir(parents=True,exist_ok=True)
engine=repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
spec=importlib.util.spec_from_file_location('fixed_gaussian_dyadic_arithmetic',engine);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
I=m.eye(16);Z=m.zero(16);I3=m.eye(48)
def neg(M):return M.scale((-1,0))
def half(M):return m.M(M.a,M.k+1).norm()
def tab(dest,phase):return m.monomial([dest(*[(x>>j)&1 for j in range(4)])for x in range(16)],[phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
rot=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
Xb=m.monomial([x^2 for x in range(16)],[0]*16)
A=half(I.scale((1,1))+Xb.scale((1,-1)))@rot
R2=tab(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
S=tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
J=R2.star()@S@R2
F=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*a)
Fh=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*d)
G=tab(lambda a,b,c,d:a+2*b+4*c+8*(d^1),lambda a,b,c,d:0)
Kd=tab(lambda a,b,c,d:a+2*(b^(a*d))+4*(c^(a*d))+8*d,lambda a,b,c,d:2*a*d)
B2=A.power(3)@S@A
assert A@F@A.star()==Fh and J@F==F@J and Kd@Fh==Fh@Kd
assert A@J@A.power(3)==Kd@B2
assert A@J@A.power(2)@S@A==Kd@A.power(4)
assert G@Fh==neg(Fh@G)
for x in (F,Fh,G,J,S,Kd):assert x@x==I
roots=((1,0),(0,1),(-1,0),(0,-1))
def mono_table(X):
 assert X.k==0
 out=[]
 for j in range(X.n):
  rs=[i for i in range(X.n)if X.a[i][j]!=m.Z];assert len(rs)==1
  out.append([rs[0],roots.index(X.a[rs[0]][j])])
 return out
# Exact constructive Gaussian gauges, including rank3 prefixes.
def gauges(X,r):
 size=1<<r;groups={}
 for i,row in enumerate(X.a):groups.setdefault(tuple(j for j,z in enumerate(row)if z!=m.Z),[]).append(i)
 assert len(groups)==16//size
 target=I
 for bit in range(r):
  xb=m.monomial([x^(1<<bit)for x in range(16)],[0]*16)
  target=target@half(I.scale((1,1))+xb.scale((1,-1)))
 assert X.k==target.k
 base=target.a[0][0]
 def phase(z):return next(k for k,u in enumerate(roots)if m.gm(base,u)==z)
 ld=[None]*16;lp=[None]*16;rd=[None]*16;rp0=[None]*16
 for block,(cols,rows)in enumerate(sorted(groups.items())):
  assert len(cols)==len(rows)==size
  es=[[phase(X.a[i][j])for j in cols]for i in rows]
  rp=[es[i][0]for i in range(size)];cp=[(es[0][j]-es[0][0])%4 for j in range(size)]
  masks=[]
  for i in range(size):
   dd=[(es[i][j]-rp[i]-cp[j])%4 for j in range(size)];assert all(z in(0,2)for z in dd)
   masks.append(sum((z//2)<<j for j,z in enumerate(dd)))
  basis=[];span={0:0}
  for z in masks:
   if z not in span:
    bit=1<<len(basis);basis.append(z);span.update({x^z:c|bit for x,c in list(span.items())})
  assert len(basis)==r and set(masks)==set(span)
  ri=[span[z]for z in masks];ci=[sum(((basis[k]>>j)&1)<<k for k in range(r))for j in range(size)];assert sorted(ci)==list(range(size))
  for i,row in enumerate(rows):ld[block*size+ri[i]]=row;lp[block*size+ri[i]]=(rp[i]+ri[i].bit_count())%4
  for j,col in enumerate(cols):rd[col]=block*size+ci[j];rp0[col]=(cp[j]+ci[j].bit_count())%4
 L=m.monomial(ld,lp);R=m.monomial(rd,rp0);assert L@target@R==X
 return {'rank':r,'left':mono_table(L),'right':mono_table(R)}
def add(s,t):return {'op':'ADD','source':s,'target':t}
def scale(b,c):return {'op':'SCALE','bank':b,'coefficient':str(Fraction(c))}
def mon(b,n):return {'op':'MONO','bank':b,'name':n}
def h2(i,j):return [add(j,i),scale(j,-2),add(i,j)]
def h2inv(i,j):return h2(i,j)+[scale(i,Fraction(1,2)),scale(j,Fraction(1,2))]
def route_minus(i,j,n):return h2(i,j)+[mon(j,n)]+h2inv(i,j)
def route_plus(i,j,n):return h2(i,j)+[mon(j,n),scale(j,-1)]+h2inv(i,j)
def swap(i,j):return [add(i,j),scale(j,-1),add(j,i),scale(j,-1),add(i,j),scale(i,-1)]
def replay(word):
 X=I3;bounds=[Fraction(1)]*3;mx=Fraction(1)
 for op in word:
  blocks=[[I if r==c else Z for c in range(3)]for r in range(3)]
  if op['op']=='ADD':blocks[op['target']][op['source']]=I;bounds[op['target']]+=bounds[op['source']]
  elif op['op']=='MONO':blocks[op['bank']][op['bank']]=monos[op['name']]
  else:
   c=Fraction(op['coefficient']);blocks[op['bank']][op['bank']]=m.M(I.scale((c.numerator,0)).a,c.denominator.bit_length()-1).norm();bounds[op['bank']]*=abs(c)
  X=m.block(blocks)@X;mx=max(mx,*bounds)
 return X,str(mx)



# Formal free noncommutative polynomial identity. Only t*t=t is reduced.
def poly(*terms):
 out={}
 for w,c in terms:
  ww=[]
  for x in w:
   if x=='t' and ww and ww[-1]=='t':continue
   ww.append(x)
  w=tuple(ww);out[w]=out.get(w,0)+c
 return {w:c for w,c in out.items()if c}
def pa(x,y):return poly(*(list(x.items())+list(y.items())))
def pn(x):return {w:-c for w,c in x.items()}
def pm(x,y):return poly(*[(u+v,c*d)for u,c in x.items()for v,d in y.items()])
def pmm(X,Y):
 out=[[{}for j in range(len(Y[0]))]for i in range(len(X))]
 for i,j,k in itertools.product(range(len(X)),range(len(Y[0])),range(len(Y))):out[i][j]=pa(out[i][j],pm(X[i][k],Y[k][j]))
 return out
pI={():1};pZ={};aa={('a',):1};tt={('t',):1};nn=pa(pI,pn(tt));a2=pm(aa,aa)
rr=[[{(f'r{i}{j}',):1}for j in range(2)]for i in range(2)]
LL=[[aa,pZ,pZ],[pI,aa,pZ],[pZ,pZ,pI]];UU=[[aa,pn(a2),pZ],[pZ,aa,pZ],[pZ,pZ,pI]]
CC=[[tt,nn,pZ],[pZ,pI,pI],[nn,tt,pZ]];YY=[[pI,pZ,pZ],[pZ,pI,pI],[pZ,pZ,pI]]
QQ=[[rr[0][0],rr[0][1],pZ],[rr[1][0],rr[1][1],pZ],[pn(pa(rr[0][0],rr[1][0])),pn(pa(rr[0][1],rr[1][1])),pI]]
BB=[[pm(pm(aa,tt),aa),pa(pn(pm(pm(aa,tt),a2)),pm(pm(aa,nn),aa))],[pm(nn,aa),pa(pn(pm(nn,a2)),pm(tt,aa))]]
E2p=pmm(pmm(BB,rr),[[aa,pZ],[pI,aa]])
rhs=[[E2p[0][0],E2p[0][1],pZ],[pZ,pZ,aa],[E2p[1][0],E2p[1][1],pZ]]
lhs=YY
for x in (LL,CC,UU,QQ,LL):lhs=pmm(lhs,x)
assert lhs==rhs
Cip=[[tt,pZ,nn],[nn,pZ,tt],[pn(nn),pI,pn(tt)]]
I3p=[[pI if i==j else pZ for j in range(3)]for i in range(3)]
assert pmm(CC,Cip)==I3p and pmm(Cip,CC)==I3p
bf=pmm(pmm(pmm([[aa,pZ],[pZ,pI]],[[tt,nn],[nn,tt]]),[[aa,pZ],[pZ,aa]]),[[pI,pn(aa)],[pZ,pI]])
assert bf==BB
formal_terms=sum(len(e)for row in lhs for e in row)
# Literal source checks and actual fixed recipes.
Ts=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
Sad=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
T=half(I+Ts);N=half(I+neg(Ts));R1p=half(I+Sad);R1m=half(I+neg(Sad));R2p=half(I+S);R2m=half(I+neg(S))
assert A.star()@Ts@A==Sad and A.power(-2)@Ts@A.power(2)==S
assert N@A.power(2)==A.power(2)@R2m and R2m.trace()==(4,0)
Cmat=m.block([[T,N,Z],[Z,I,I],[N,T,Z]])
Cimat=m.block([[T,Z,N],[N,Z,T],[neg(N),I,neg(T)]])
assert Cmat@Cimat==I3 and Cimat@Cmat==I3
Fmat=m.block([[I,Z,Z],[Z,I,Z],[neg(I),neg(I),I]])
Ymat=m.block([[I,Z,Z],[Z,I,I],[Z,Z,I]])
Wmat=m.block([[I,Z,Z],[Z,Z,I],[Z,I,Z]])
Lmat=m.block([[A,Z,Z],[I,A,Z],[Z,Z,I]]);Umat=m.block([[A,neg(A.power(2)),Z],[Z,A,Z],[Z,Z,I]])
L2mat=m.block([[A,Z],[I,A]])
Bmat=m.block([[A@T@A,neg(A@T@A.power(2))+A@N@A],[N@A,neg(N@A.power(2))+T@A]])
monos={'Ts':Ts,'S_ab':S,'S_ad':Sad}
def sub(s,t):return [scale(t,-1),add(s,t),scale(t,-1)]
Cword=[add(1,2)]+swap(1,2)+route_minus(0,2,'Ts')
Ciword=route_minus(0,2,'Ts')+swap(1,2)+sub(1,2)
Fword=[scale(2,-1),add(0,2),add(1,2),scale(2,-1)]
Fiword=[add(0,2),add(1,2)]
words={'C_T':Cword,'C_T_inverse':Ciword,'F':Fword,'F_inverse':Fiword,'Y':[add(2,1)],'Y_inverse':sub(2,1),'output_swap12':swap(1,2),'output_swap12_inverse':swap(1,2)}
expected={'C_T':Cmat,'F':Fmat,'Y':Ymat,'output_swap12':Wmat};stats={};omitted=0
for name in expected:
 X,b=replay(words[name]);Xi,bi=replay(words[name+'_inverse']);assert X==expected[name] and X@Xi==I3 and Xi@X==I3
 for nm in (name,name+'_inverse'):
  X,b=replay(words[nm]);stats[nm]={'counts':dict(Counter(x['op']for x in words[nm])),'prefix_bound':b}
  for j,x in enumerate(words[nm]):
   if x['op']=='ADD':assert replay(words[nm][:j]+words[nm][j+1:])[0]!=X;omitted+=1
# Three independent actual R units verify the completed Q formula, including its inverse.
def part(X,r,c,size=16):return m.M(tuple(tuple(row[c*size:(c+1)*size])for row in X.a[r*size:(r+1)*size]),X.k).norm()
Rwords={'identity':[],'bank_swap01':swap(0,1),'controlled_Sab':route_minus(0,1,'S_ab')}
Rcontrols=[]
for name,rw in Rwords.items():
 R48,_=replay(rw);Ri48,_=replay(rw) # Each chosen R control is an involution.
 assert R48@Ri48==I3
 R32=m.block([[part(R48,i,j)for j in range(2)]for i in range(2)])
 Q48=Fmat@R48
 Qcheck,_=replay(rw+Fword);Qicheck,_=replay(Fiword+rw)
 assert Qcheck==Q48 and Qcheck@Qicheck==I3 and Qicheck@Qcheck==I3
 E32=Bmat@R32@L2mat
 expected48=m.block([[part(E32,0,0),part(E32,0,1),Z],[Z,Z,A],[part(E32,1,0),part(E32,1,1),Z]])
 assert Ymat@Lmat@Cmat@Umat@Qcheck@Lmat==expected48
 Rcontrols.append({'name':name,'actual_Q_and_inverse':True,'literal_reduction_identity':True})
# Explicit sharp source channels outside the pure-three cubic catalogue.
Db=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:b)
g0=R2.star();g1=R2.star()@Db
all_gauges={'A2_R2inv_A':gauges(A.power(2)@g0@A,1),'A2_R2inv_Db_A':gauges(A.power(2)@g1@A,2),'A4':gauges(A.power(4),4),'B2':gauges(B2,2)}
assert A@T@A.power(3)==half(A.power(4)+B2)
# Meaningful negative controls: wrong noncommutative order, omitted row completion,
# and replacing collective T by a claimed half-dimensional projector.
Qbad=m.diagonal([I,I,I]);wrong=Ymat@Lmat@Cmat@Umat@Qbad@Lmat
Ewrong=Bmat@L2mat;wrong_expected=m.block([[part(Ewrong,0,0),part(Ewrong,0,1),Z],[Z,Z,A],[part(Ewrong,1,0),part(Ewrong,1,1),Z]])
assert wrong!=wrong_expected
assert A@T!=T@A and T.trace()==(12,0)
result={'status':'PASS_EXACT_TWO_BANK_REDUCTION_AND_CUBIC_GATE_CONTROLS','scope':'Universal exact noncommutative reduction isolating Gaussian1, actual fixed ordinary words and inverse overheads, and a written universal pure-cubic second-row catalogue obstruction. No R giving independent42 has been constructed.',
 'formal_independent_symbols':['a','t','r00','r01','r10','r11'],'formal_relation':'t*t=t','formal_reduced_monomials':formal_terms,'formal_C_inverse_and_B_factorization':True,
 'actual_R_unit_controls':Rcontrols,'source_rank_changing_channels':{'R2_inverse':1,'R2_inverse_D_b':2},'Gaussian_gauges':len(all_gauges),'omitted_ADD_negative_controls':omitted,'additional_negative_controls':3,
 'invoices':stats,'Q_forward_overhead':{'ADD':2,'SCALE':2},'Q_inverse_overhead':{'ADD':2},'unknown_R_and_endpoint_costs_retained':True,
 'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'source_pins':{str(engine.relative_to(repo)):hashlib.sha256(engine.read_bytes()).hexdigest(),'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md':hashlib.sha256((repo/'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md').read_bytes()).hexdigest()},
 'remaining':'Construct a uniform actual ordinary R with inverse, and ordinary endpoint U,V, proving U B_T R L2 V=diag(G4,G2) with the complete invoice.','no_new_kappa':True}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
(args.out/'WORDS.json').write_text(json.dumps({'monomial_tables':{n:mono_table(x)for n,x in monos.items()},'words':words,'invoices':stats,'R_control_words':Rwords},indent=2)+'\n')
(args.out/'GAUSSIAN-GAUGES.json').write_text(json.dumps(all_gauges,indent=2)+'\n')
(args.out/'FORMAL-IDENTITY.json').write_text(json.dumps({'symbols':result['formal_independent_symbols'],'relation':'t*t=t','reduced_rhs':[[[{'word':list(w),'coefficient':c}for w,c in sorted(e.items())]for e in row]for row in rhs]},indent=2)+'\n')
print(json.dumps({'status':result['status'],'formal_monomials':formal_terms,'primitive_omissions':omitted,'actual_R_controls':len(Rcontrols),'rank_changing_source_classes':[1,2]},indent=2))
