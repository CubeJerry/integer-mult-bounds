#!/usr/bin/env python3
"""Exact controls for the ordinary row-range gate and spectator kernels; the universal proof is PROOF.md."""
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



P=half(I+F);M=half(I+neg(F));Ph=half(I+Fh);Mh=half(I+neg(Fh))
Zc=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*c)
Tactive=S@Zc;zz=(F@Tactive).power(2)
assert F@F==I and Tactive@Tactive==I and zz@zz==I and zz@F==F@zz and zz@Tactive==Tactive@zz
GG=[I];seen={I}
for h in GG:
 for g0 in (F,Tactive):
  h0=h@g0
  if h0 not in seen:seen.add(h0);GG.append(h0)
assert len(GG)==8 and all(h.trace()==(0,0)for h in GG if h!=I)
# Work in the exact eight-dimensional group algebra, not only its 16x16 image.
def ca(*pairs):
 out={}
 for g,c in pairs:out[g]=out.get(g,Fraction(0))+Fraction(c)
 return {g:c for g,c in out.items()if c}
def aa(x,y):return ca(*(list(x.items())+list(y.items())))
def sm(x,c):return ca(*[(g,c*v)for g,v in x.items()])
def prod(x,y):return ca(*[(g@h,c*d)for g,c in x.items()for h,d in y.items()])
def ss(x):return ca(*[(g.star(),c)for g,c in x.items()])
eI={I:Fraction(1)};eP=ca((I,Fraction(1,2)),(F,Fraction(1,2)));eM=ca((I,Fraction(1,2)),(F,Fraction(-1,2)));eT=ca((I,Fraction(1,2)),(Tactive,Fraction(1,2)));ezp=ca((I,Fraction(1,2)),(zz,Fraction(1,2)));ezm=ca((I,Fraction(1,2)),(zz,Fraction(-1,2)))
def physical(x):
 out=Z
 for g,c in x.items():
  assert c.denominator&(c.denominator-1)==0
  out=out+m.M(g.scale((c.numerator,0)).a,c.denominator.bit_length()-1).norm()
 return out
formal=[]
for sign,ep in [(1,eP),(-1,eM)]:
 RR=prod(ep,aa(ezm,prod(ezp,eT)));PT=prod(ep,eT);Y=aa(sm(prod(ezm,ep),2),ezp)
 assert prod(RR,RR)==RR and ss(RR)==RR and prod(RR,PT)==PT and prod(PT,Y)==RR
 assert RR[I]==Fraction(3,8)
 Rmat=physical(RR);assert Rmat.trace()==(6,0) and Rmat@Rmat==Rmat
 formal.append({'sector':sign,'identity_coefficient':'3/8','coefficients':[{'table':mono_table(g),'coefficient':str(c)}for g,c in RR.items()]})
Rplus=physical(prod(eP,aa(ezm,prod(ezp,eT))));Rminus=physical(prod(eM,aa(ezm,prod(ezp,eT))))
Hactive=A@Tactive@A.star();HactiveJ=A@J@Tactive@J@A.star();mono_table(Hactive);mono_table(HactiveJ)
Tact=half(I+Tactive)
for PP,MM,RP,RM in [(P,M,Rplus,Rminus),(M,P,Rminus,Rplus)]:
 K=m.block([[A@PP@Tact@A,Z,Z],[A@J@MM@Tact@A,Z,Z],[Z,Z,Z]])
 Rblock=m.diagonal([A@RP@A.star(),A@J@RM@J@A.star(),Z]);assert Rblock@K==K and Rblock.trace()==(12,0)
# New spectator-swap source, with literal coordinate-swap pullbacks.
Ts=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
Sad=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
assert Ts@Ts==I and Sad@Sad==I and Ts.trace()==(8,0) and Sad.trace()==(8,0) and S.trace()==(8,0)
assert A.star()@Ts@A==Sad and A.power(-2)@Ts@A.power(2)==S
assert A@J@Ts@A.star()==Kd and A@Ts@A.power(3)==B2 and Ts@J==J@Ts and Ts@F==F@Ts
T=half(I+Ts);N=half(I+neg(Ts));R1m=half(I+neg(Sad));R2m=half(I+neg(S));R1p=half(I+Sad);R2p=half(I+S)
assert T.trace()==(12,0) and R1m.trace()==(4,0) and R2m.trace()==(4,0)
K=m.block([[A@P@T@A,Z,Z],[A@J@M@T@A,Z,Z],[Z,Z,Z]])
Kold=m.block([[A@P@A,Z,Z],[A@J@M@A,Z,Z],[Z,Z,Z]])
assert Kold.star()@Kold==m.diagonal([I,Z,Z]) and K.star()@K==m.diagonal([A.star()@T@A,Z,Z])
Drow=m.diagonal([I,Kd,I]);O=m.block([[Ph,Mh,Z],[Mh,Ph,Z],[Z,Z,I]]);H=O@Drow
assert H@K==m.block([[A@T@A,Z,Z],[Z,Z,Z],[Z,Z,Z]])
assert A@T@A==A.power(2)@R1p and A@T@A.power(2)==A.power(3)@R2p
assert K@m.diagonal([R1m,Z,Z])==m.zero(48) and K@m.diagonal([A@R2m,Z,Z])==m.zero(48)
assert K@m.diagonal([R2m,Z,Z])!=m.zero(48) and K@m.diagonal([A@R1m,Z,Z])!=m.zero(48)
quartic=neg(A@T@A.power(3));E4=neg(half(A.power(4)));E2=neg(half(B2));assert quartic==E4+E2
quarterI=m.M(I.a,2).norm();assert E4@E4.star()==quarterI and E2@E2.star()==quarterI
# Full Gaussian gauges for every prefix word; signs only affect exterior coefficients.
all_gauges={}
for row in range(2):
 for ep,et in itertools.product(range(2),repeat=2):
  h=(J if row else I)@F.power(ep)@Ts.power(et)
  for trailing,r in [(1,2),(2,3)]:all_gauges[f'row{row}_F{ep}_T{et}_rank{r}']=gauges(A@h@A.power(trailing),r)
for name,w,r in [('A4',A.power(4),4),('B2',B2,2),('forward_Ts',A@Ts@A.star(),2),('forward_JTsJ',A@J@Ts@J@A.star(),2)]:all_gauges[name]=gauges(w,r)
Cold=m.block([[P,M,Z],[J@M,J@P,Z],[Z,Z,I]]);Rt=m.block([[T,Z,N],[Z,I,Z],[N,Z,T]]);Cn=Cold@Rt;S12=m.block([[I,Z,Z],[Z,Z,I],[Z,I,Z]]);Cs=Cn@S12
Q=m.block([[I,Z,Z],[Z,R2p,R2m],[Z,R2m,R2p]])
monos={'F':F,'Fhat':Fh,'J':J,'Ts':Ts,'S_ab':S,'S_ad':Sad,'Kdec':Kd}
Cword=route_minus(0,2,'Ts')+route_minus(0,1,'F')+[mon(1,'J')];Ciword=[mon(1,'J')]+route_minus(0,1,'F')+route_minus(0,2,'Ts')
words={'C_new':Cword,'C_new_inverse':Ciword,'C_swapped12':swap(1,2)+Cword,'C_swapped12_inverse':Ciword+swap(1,2),'Drow':[mon(1,'Kdec')],'Drow_inverse':[mon(1,'Kdec')],'O':route_minus(0,1,'Fhat'),'O_inverse':route_minus(0,1,'Fhat'),'Q_kernel':route_minus(1,2,'S_ab'),'Q_kernel_inverse':route_minus(1,2,'S_ab')}
expected={'C_new':Cn,'C_swapped12':Cs,'Drow':Drow,'O':O,'Q_kernel':Q};stats={};omitted=0
for name in expected:
 X,b=replay(words[name]);Xi,bi=replay(words[name+'_inverse']);assert X==expected[name] and X@Xi==I3 and Xi@X==I3
 for nm in (name,name+'_inverse'):
  X,b=replay(words[nm]);stats[nm]={'counts':dict(Counter(x['op']for x in words[nm])),'prefix_bound':b}
  for j,x in enumerate(words[nm]):
   if x['op']=='ADD':assert replay(words[nm][:j]+words[nm][j+1:])[0]!=X;omitted+=1
result={'status':'PASS_ORDINARY_ROW_RANGE_AND_TWO_SPECTATOR_KERNELS','scope':'Universal active-SWAP_ab Z_c row-range exclusion for both prefix orientations; exact spectator-SWAP_cd source bridge with two ordinary kernel projectors and full aligned quartic/rank2 components. No full421 caller.',
 'active_swap_group_order':len(GG),'active_swap_nonidentity_traces_zero':True,'formal_row_projector_rank':'3D/8 each','active_swap_total_range_rank':'3D/4',
 'spectator_kernel_rank':'(D-8^V)/2','spectator_prefix_rank':'(D+8^V)/2','rank_half_negative_control':{'V':1,'true_rank_T':12,'false_D_over_2':8},
 'wrong_kernel_controls_rejected':2,'quartic_components_full_D':True,'source_Gaussian_gauges':len(all_gauges),'omitted_ADD_negative_controls':omitted,'invoices':stats,
 'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'source_pins':{str(engine.relative_to(repo)):hashlib.sha256(engine.read_bytes()).hexdigest(),'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md':hashlib.sha256((repo/'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md').read_bytes()).hexdigest()},
 'remaining':'Complete a literal three-native independent421 caller using both spectator kernel channels, actual endpoint inverses, and all physical/source/supplier/recursive bills.','no_new_kappa':True}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
(args.out/'WORDS.json').write_text(json.dumps({'monomial_tables':{n:mono_table(x)for n,x in monos.items()},'words':words,'invoices':stats},indent=2)+'\n')
(args.out/'GAUSSIAN-GAUGES.json').write_text(json.dumps(all_gauges,indent=2)+'\n')
(args.out/'D8-RANGE-CERTIFICATE.json').write_text(json.dumps({'group_tables':[mono_table(g)for g in GG],'traces':[g.trace()for g in GG],'range_projectors':formal,'forward_tables':{'Hactive':mono_table(Hactive),'HactiveJ':mono_table(HactiveJ)}},indent=2)+'\n')
print(json.dumps({'status':result['status'],'gauges':len(all_gauges),'negative_controls':omitted+3,'active_swap_range':'3D/4','spectator_rank':'(D+8^V)/2'},indent=2))
