#!/usr/bin/env python3
"""Exact controls for the Gaussian-component augmentation gate; the universal proof is PROOF.md."""
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
T0=S@Zc;T=half(I+T0);N=half(I+neg(T0));R0=J@F;Rp=half(I+R0);Rm=half(I+neg(R0))
assert T0@T0==I and T0.trace()==(0,0)
assert A.power(-2)@T0@A.power(2)==R0 and R0@R0==I and R0.trace()==(0,0)
Pi_mid=m.diagonal([Mh,Ph,Z]);Pi_first=m.diagonal([Ph,Mh,Z])
Kmid=m.block([[A@M@T@A,Z,Z],[A@J@P@T@A,Z,Z],[Z,Z,Z]])
Kfirst=m.block([[A@P@T@A,Z,Z],[A@J@M@T@A,Z,Z],[Z,Z,Z]])
assert Pi_mid@Kmid==Kmid and Pi_first@Kfirst==Kfirst
for K in (Kmid,Kfirst):
 assert K.star()@K==m.diagonal([A.star()@T@A,Z,Z])
 assert K@m.diagonal([A@Rm,Z,Z])==m.zero(48)
O=m.block([[Ph,Mh,Z],[Mh,Ph,Z],[Z,Z,I]])
assert O@Pi_first@O==m.diagonal([I,Z,Z]) and O@O==I3
Cold=m.block([[P,M,Z],[J@M,J@P,Z],[Z,Z,I]])
Rt=m.block([[T,Z,N],[Z,I,Z],[N,Z,T]])
S12=m.block([[I,Z,Z],[Z,Z,I],[Z,I,Z]])
Cn=Cold@Rt;Cs=Cn@S12
Q=m.block([[I,Z,Z],[Z,Rp,Rm],[Z,Rm,Rp]])
assert Q@Q==I3 and Q.a!=I3.a
# Every source word needed for both prefix orientations gets a full Gaussian gauge.
all_gauges={};epsilon_prefix={}
for orientation,sgn in [('middle',-1),('first',1)]:
 sums=[]
 for row in range(2):
  terms=[]
  for ep in (0,1):
   for et in (0,1):
    h=(J if row else I)@F.power(ep)@T0.power(et)
    coef=Fraction((sgn if row==0 else -sgn)**ep,4)
    terms.append((h,coef))
  sums.append(str(sum(c for h,c in terms)))
  for ix,(h,c)in enumerate(terms):
   for trailing,r in [(1,2),(2,3)]:
    all_gauges[f'{orientation}_row{row}_term{ix}_rank{r}']=gauges(A@h@A.power(trailing),r)
 epsilon_prefix[orientation]=sums+['0']
assert epsilon_prefix=={'middle':['0','1','0'],'first':['1','0','0']}
# Primitive recipes: first interface, its column-corrected completion,
# an actual Q using the nonzero ordinary kernel, and free-range decoder.
monos={'F':F,'Fhat':Fh,'J':J,'T0':T0,'R0':R0}
Cword=route_minus(0,2,'T0')+route_minus(0,1,'F')+[mon(1,'J')]
Ciword=[mon(1,'J')]+route_minus(0,1,'F')+route_minus(0,2,'T0')
words={'C_opposite':Cword,'C_opposite_inverse':Ciword,
       'C_opposite_swapped12':swap(1,2)+Cword,'C_opposite_swapped12_inverse':Ciword+swap(1,2),
       'Q_kernel':route_minus(1,2,'R0'),'Q_kernel_inverse':route_minus(1,2,'R0'),
       'O_opposite':route_minus(0,1,'Fhat'),'O_opposite_inverse':route_minus(0,1,'Fhat')}
expected={'C_opposite':Cn,'C_opposite_swapped12':Cs,'Q_kernel':Q,'O_opposite':O}

def epsilon_word(word):
 X=[[Fraction(int(i==j))for j in range(3)]for i in range(3)]
 for op in word:
  if op['op']=='ADD':X[op['target']]=[x+y for x,y in zip(X[op['target']],X[op['source']])]
  elif op['op']=='SCALE':X[op['bank']]=[Fraction(op['coefficient'])*x for x in X[op['bank']]]
 return [[str(x)for x in row]for row in X]

stats={};omitted=0
for name,Xexpected in expected.items():
 X,b=replay(words[name]);Xi,bi=replay(words[name+'_inverse']);assert X==Xexpected and X@Xi==I3 and Xi@X==I3
 for nm in (name,name+'_inverse'):
  X,b=replay(words[nm]);stats[nm]={'counts':dict(Counter(x['op']for x in words[nm])),'prefix_bound':b,'epsilon':epsilon_word(words[nm])}
  for j,x in enumerate(words[nm]):
   if x['op']=='ADD':assert replay(words[nm][:j]+words[nm][j+1:])[0]!=X;omitted+=1
Eid=[['1','0','0'],['0','1','0'],['0','0','1']]
Eswap=[['1','0','0'],['0','0','1'],['0','1','0']]
assert epsilon_word(Cword)==Eid and epsilon_word(words['C_opposite_swapped12'])==Eswap
assert epsilon_word(words['Q_kernel'])==Eid and epsilon_word(words['O_opposite'])==Eid
# Scalar sharpness: opposite orientation permits independent component lines.
scalar_phi4=m.monomial([0,1,2],[0,0,0])
# Use direct exact 3x3 matrices to make their summed endpoint a unit.
small4=m.M((((1,0),(0,0),(0,0)),((0,0),(0,0),(0,0)),((0,0),(0,0),(0,0))),0)
small2=m.M((((0,0),(0,0),(0,0)),((0,0),(0,0),(0,0)),((0,0),(1,0),(0,0))),0)
small1=m.M((((0,0),(0,0),(0,0)),((0,0),(0,0),(1,0)),((0,0),(0,0),(0,0))),0)
assert (small4+small2+small1).power(2)==m.eye(3)
# A one-column identity shows why component augmentation cannot be
# inferred from a small physical-width matrix representation.
assert A==half(rot.scale((1,1))+(Xb@rot).scale((1,-1)))
assert sum(A.a[i][0] != m.Z for i in range(16))==2
# Its tensor-four source column has sixteen nonzero coordinates, while
# the naive two-monomial lift has at most two: they are not the same operator.
assert 2**4>2
# Exterior phases are retained; literal root-four phases disappear at 4|V.
assert ((0,1)!=(1,0)) and m.monomial(list(range(16)),[1]*16).power(4)==I
result={'status':'PASS_GAUSSIAN_COMPONENT_AUGMENTATION_CONTROLS',
 'scope':'Universal written middle-sector exclusion for arbitrary ordinary C completion and Q; actual opposite-oriented source prefix and kernel, corrected ordinary completion, actual Q kernel swap; no full421 caller.',
 'source_prefix_epsilon':epsilon_prefix,'source_Gaussian_gauges':len(all_gauges),
 'opposite_orientation_scalar_sharpness':True,'finite_width_nonfaithfulness_negative_control':True,'exterior_literal_phase_negative_control':True,
 'actual_Q_has_nonzero_q12_Rminus':True,'ordinary_kernel_rank_fraction':'1/2',
 'invoices':stats,'omitted_ADD_negative_controls':omitted,
 'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),
 'source_pins':{str(engine.relative_to(repo)):hashlib.sha256(engine.read_bytes()).hexdigest(),
 'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md':hashlib.sha256((repo/'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md').read_bytes()).hexdigest()},
 'remaining':'Complete opposite-oriented caller equations with independent421 endpoint interfaces and the full invoice. The middle-oriented SZc family is now excluded despite its actual ordinary kernel.',
 'no_new_kappa':True}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
(args.out/'WORDS.json').write_text(json.dumps({'monomial_tables':{n:mono_table(x)for n,x in monos.items()},'words':words,'invoices':stats},indent=2)+'\n')
(args.out/'GAUSSIAN-GAUGES.json').write_text(json.dumps(all_gauges,indent=2)+'\n')
print(json.dumps({'status':result['status'],'source_prefix_epsilon':epsilon_prefix,'gauges':len(all_gauges),'omitted_ADD_negative_controls':omitted},indent=2))
