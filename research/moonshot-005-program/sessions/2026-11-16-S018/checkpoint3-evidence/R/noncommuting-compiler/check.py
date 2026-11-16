#!/usr/bin/env python3
"""Exact D8 matrix units, internal shear and general physical compilation controls."""
from pathlib import Path
from fractions import Fraction as F
import argparse,itertools,json,hashlib,random
import sympy as s
p=argparse.ArgumentParser()
for n in ['repo','proof','out']:p.add_argument('--'+n,type=Path,required=True)
o=p.parse_args();o.out.mkdir(parents=True,exist_ok=True)
labels=list(itertools.product(range(2),repeat=3));index={g:i for i,g in enumerate(labels)};N=8

def product(a,b):
 u,v,e=a;r,t,f=b
 return(u^(t if e else r),v^(r if e else t),e^f)
mt=[[index[product(a,b)]for b in labels]for a in labels];inverse=[next(j for j in range(N)if mt[i][j]==mt[j][i]==0)for i in range(N)]
def zero():return[F(0)]*N
def basis(i=0):r=zero();r[i]=F(1);return r
one=basis()
def add(a,b):return[x+y for x,y in zip(a,b)]
def scale(a,c):return[x*c for x in a]
def mul(a,b):
 r=zero()
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:r[mt[i][j]]+=x*y
 return r
rho=[]
for eps,eta in itertools.product([1,-1],repeat=2):rho.append([s.Matrix([[eps**(u+v)*eta**e]])for u,v,e in labels])
x=s.diag(1,-1);y=-x;t=s.Matrix([[0,1],[1,0]]);rho.append([x**u*y**v*t**e for u,v,e in labels]);dims=[1,1,1,1,2]
for rr in rho:
 for i,j in itertools.product(range(N),repeat=2):assert rr[i]*rr[j]==rr[mt[i][j]]
units={}
for l,d in enumerate(dims):
 for a,b in itertools.product(range(d),repeat=2):units[l,a,b]=[F(d,N)*F(rho[l][inverse[g]][b,a])for g in range(N)]
for (l,a,b),u in units.items():
 for (q,c,d),v in units.items():assert mul(u,v)==(units[l,a,d]if l==q and b==c else zero())
assert sum(d*d for d in dims)==N and s.Matrix(list(units.values())).rank()==N
identity=zero()
for l,d in enumerate(dims):
 for a in range(d):identity=add(identity,units[l,a,a])
assert identity==one

def eye():return[[one[:]if i==j else zero()for j in range(3)]for i in range(3)]
def matrix_mul(A,B):
 return[[sum_ring([mul(A[i][k],B[k][j])for k in range(3)])for j in range(3)]for i in range(3)]
def sum_ring(rows):
 r=zero()
 for row in rows:r=add(r,row)
 return r

def lower(dst,src,r):
 assert dst!=src;word=[]
 for g,c in enumerate(r):
  if not c:continue
  if g:word.append(['MONOMIAL',src,g])
  if c!=1:word.append(['SCALE',src,str(c)])
  word.append(['ADD',src,dst])
  if c!=1:word.append(['SCALE',src,str(1/c)])
  if g:word.append(['MONOMIAL',src,inverse[g]])
 return word

def replay(word):
 M=eye();peak=F(1);counts={'ADD':0,'SCALE':0,'MONOMIAL':0}
 for op in word:
  counts[op[0]]+=1
  if op[0]=='ADD':M[op[2]]=[add(a,b)for a,b in zip(M[op[2]],M[op[1]])]
  elif op[0]=='SCALE':M[op[1]]=[scale(a,F(op[2]))for a in M[op[1]]]
  else:M[op[1]]=[mul(basis(op[2]),a)for a in M[op[1]]]
  peak=max(peak,max(sum(abs(z)for cell in row for z in cell)for row in M))
 return M,counts,peak

def inv_shears(shears):return[(i,j,scale(r,-1))for i,j,r in reversed(shears)]
def compile_shears(shears):return[op for i,j,r in shears for op in lower(i,j,r)]
e11=units[4,0,0];e12=units[4,0,1]
assert e11==scale(sum_ring([basis(0),basis(index[1,0,0]),scale(basis(index[0,1,0]),-1),scale(basis(index[1,1,0]),-1)]),F(1,4))
assert e12==mul(e11,basis(index[0,0,1]))
example_shears=[(1,0,scale(e12,-1)),(0,1,scale(e11,-1)),(1,0,e12),(0,1,e11)]
example=compile_shears(example_shears);target=eye();target[0][0]=add(one,e12)
actual,ec,ep=replay(example);assert actual==target and ec=={'ADD':16,'SCALE':32,'MONOMIAL':28}
example_inv=compile_shears(inv_shears(example_shears));mi,eic,eip=replay(example_inv);assert matrix_mul(actual,mi)==matrix_mul(mi,actual)==eye()and eic==ec
# Omitting a genuine ADD or an inverse service must fail the exact endpoint.
negative=[]
for kind in ['ADD','MONOMIAL']:
 k=next(i for i,z in enumerate(example)if z[0]==kind);bad=example[:k]+example[k+1:];assert replay(bad)[0]!=target;negative.append({'omitted':example[k],'rejected':True})

def sl_factors(A):
 A=A.copy();m=A.rows;assert A.cols==m and A.det()==1;elims=[]
 def do(i,j,c):
  c=s.cancel(c)
  if not c:return
  row=list(A.row(j))
  for z in range(m):A[i,z]=s.cancel(A[i,z]+c*row[z])
  elims.append((i,j,F(c)))
 for c in range(m):
  if A[c,c]==0:
   r=next(r for r in range(c+1,m)if A[r,c]!=0)
   for i,j,z in [(c,r,1),(r,c,-1),(c,r,1)]:do(i,j,z)
  for r in range(m):
   if r!=c and A[r,c]!=0:do(r,c,-A[r,c]/A[c,c])
 for i in range(m-1):
  if A[i,i]==1:continue
  z=1/A[i,i];j=m-1
  for u,v,c in [(i,j,-1),(j,i,1),(i,j,-1),(i,j,z),(j,i,-1/z),(i,j,z)]:do(u,v,c)
 assert A==s.eye(m)and len(elims)<=(m-1)*(m+9)
 return[(i,j,-c)for i,j,c in reversed(elims)]

def lift(l,fac):
 d=dims[l];shears=[]
 for row,col,c in fac:
  i,a=divmod(row,d);j,b=divmod(col,d)
  if i!=j:shears.append((i,j,scale(units[l,a,b],c)))
  else:
   assert a!=b;j=(i+1)%3;X=scale(units[l,a,0],c);Y=units[l,0,b]
   shears.extend([(j,i,scale(Y,-1)),(i,j,scale(X,-1)),(j,i,Y),(i,j,X)])
 return shears

def from_components(blocks):
 Q=[[zero()for _ in range(3)]for _ in range(3)]
 for l,d in enumerate(dims):
  for i,j,a,b in itertools.product(range(3),range(3),range(d),range(d)):
   Q[i][j]=add(Q[i][j],scale(units[l,a,b],F(blocks[l][i*d+a,j*d+b])))
 return Q
rng=random.Random(1803);delta=F(2);us=[];blocks=[];generic_shears=[];factor_counts=[]
for l,d in enumerate(dims):
 m=3*d;A=s.eye(m)
 # A signed pivot plus nontrivial entries, including internal-component coordinates.
 for i,j,c in [(0,1,1),(1,0,-1),(0,1,1)]+[(rng.randrange(m),rng.randrange(m),rng.choice([-2,-1,1,2]))for _ in range(12)]:
  if i==j:continue
  for z in range(m):A[i,z]+=c*A[j,z]
 assert A.det()==1;us.append(A.copy());fac=sl_factors(A);factor_counts.append(len(fac));generic_shears+=lift(l,fac)
 Q=A.copy()
 for i in range(d):
  for j in range(m):Q[i,j]*=delta
 assert Q.det()==delta**d;blocks.append(Q)
generic=compile_shears(generic_shears)+[['SCALE',0,str(delta)]]
G,gc,gp=replay(generic);wanted=from_components(blocks);assert G==wanted
generic_inv=[['SCALE',0,str(1/delta)]]+compile_shears(inv_shears(generic_shears));Gi,gic,gip=replay(generic_inv);assert matrix_mul(G,Gi)==matrix_mul(Gi,G)==eye()
Lbound=4*sum((3*d-1)*(3*d+9)for d in dims)
for cnt in [gc,gic]:assert cnt['ADD']<=Lbound*N and cnt['SCALE']<=2*Lbound*N+1 and cnt['MONOMIAL']<=2*Lbound*(N-1)
# An algebraic unit with unmatched component determinants is outside the theorem.
bad=[s.eye(3*d)for d in dims];bad[0][0,0]=2;assert all(B.det()!=0 for B in bad)
assert not all(B.det()==bad[0].det()**d for B,d in zip(bad,dims))
negative.append({'unequal_component_determinants':'unit but rejected by this sufficient compiler condition','rejected':True})

# Reconstruct every literal source monomial without author checker imports.
Id=s.eye(16);P=s.zeros(16);Xb=s.zeros(16);phase=s.eye(16);J=s.zeros(16)
for z in range(16):
 a,b,c,d=[(z>>j)&1 for j in range(4)];P[(z>>1)|((z&1)<<3),z]=1;Xb[z^2,z]=1;phase[z,z]=(-1)**(a*c*d);J[a+2*b+4*(d^(a*b))+8*(c^(a*b)),z]=1
tidy=lambda M:M.applyfunc(s.expand);A=tidy(((1+s.I)*Id+(1-s.I)*Xb)*phase*P/2);A2=tidy(A*A)
Za=s.diag(*[(-1)**(z&1)for z in range(16)]);Zb=s.diag(*[(-1)**((z>>1)&1)for z in range(16)]);Hx=tidy(A2.adjoint()*Za*A2);Hy=tidy(A2.adjoint()*Zb*A2)
assert tidy(Hx*Hx)==tidy(Hy*Hy)==J*J==Id and tidy(J*Hx*J)==Hy
roots=[s.Integer(1),s.I,s.Integer(-1),-s.I]
def table(M):
 r=[]
 for j in range(16):
  ids=[i for i in range(16)if M[i,j]!=0];assert len(ids)==1;i=ids[0];r.append([i,roots.index(s.expand(M[i,j]))])
 assert len(set(i for i,e in r))==16;return r
literal=[tidy(Hx**u*Hy**v*J**e)for u,v,e in labels];tables=[table(M)for M in literal];assert len(set(str(T)for T in tables))==8
for i,j in itertools.product(range(N),repeat=2):assert tidy(literal[i]*literal[j])==literal[mt[i][j]]
E12=sum((s.Rational(c.numerator,c.denominator)*M for c,M in zip(e12,literal)),s.zeros(16));assert E12!=s.zeros(16)and E12*E12==s.zeros(16)
assert any(sum(z!=0 for z in row)>1 for row in (Id+E12).tolist())
# Tensor characters use trace(g)^V, keeping the literal table phase at every width.
multiplicities=[]
for V in [1,2,3,4]:
 mm=[]
 for rr in rho:
  z=sum(s.trace(M)**V*s.trace(rr[inverse[g]])for g,M in enumerate(literal))/8;assert z.is_Integer and z>=0;mm.append(int(z))
 assert sum(d*z for d,z in zip(dims,mm))==16**V;multiplicities.append({'V':V,'component_multiplicities':mm})
assert all(x>0 for x in multiplicities[1]['component_multiplicities'])
# Width-one invertibility alone misses an absent irreducible block.
hidden=units[1,0,0]
hidden16=sum((s.Rational(c.numerator,c.denominator)*M for c,M in zip(hidden,literal)),s.zeros(16))
assert hidden16==s.zeros(16) and multiplicities[0]['component_multiplicities'][1]==0
assert multiplicities[1]['component_multiplicities'][1]==16
negative.append({'hidden_component_singular_candidate':'I minus the scalar component1 projector on every bank','width1_physical_map':'identity','width2_kernel_dimension':48,'abstract_component_unit_test_rejects':True})

artifacts={'EXAMPLE-WORD.json':example,'EXAMPLE-INVERSE-WORD.json':example_inv,'GENERAL-WORD.json':generic,'GENERAL-INVERSE-WORD.json':generic_inv}
for name,word in artifacts.items():(o.out/name).write_text(json.dumps({'operations':word,'group_labels':labels,'literal_group_tables':tables,'owner_births':0,'Gaussian_queries':0},indent=2)+'\n')
def coeff_height(word):
 fs=[F(z[2])for z in word if z[0]=='SCALE'];return{'max_abs_numerator':max(abs(z.numerator)for z in fs),'max_denominator':max(z.denominator for z in fs)}
prog=o.repo/'research/moonshot-005-program';deps=['results/complex-source-square-controls/ADMISSION.md','results/complex-nondiagonal-cyclic/author/NONDIAGONAL-CYCLIC-IMPLEMENTATION.md','results/fixed-monomial-compact-bridge/author/PROOF.md']
r={'status':'PASS_ROOT_NONCOMMUTING_SPLIT_COMPILER_CONTROLS','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'group_order':8,'component_dimensions':dims,'all64_matrix_unit_products':True,'matrix_unit_basis_rank':8,'literal_source_and_group_tables_verified':True,'matrix_units':{str(k):list(map(str,v))for k,v in units.items()},'tensor_width_controls':multiplicities,'example':{'counts':ec,'inverse_counts':eic,'prefix_coefficient_l1_norm_bound':str(ep),'inverse_prefix_bound':str(eip),'borrowed_banks_restored':True,'single_bank_nonmonomial':True,'coefficient_heights':coeff_height(example)},'general':{'delta':str(delta),'component_determinants':[str(B.det())for B in blocks],'scalar_factor_counts':factor_counts,'cross_bank_shears':len(generic_shears),'counts':gc,'inverse_counts':gic,'prefix_coefficient_l1_norm_bound':str(gp),'inverse_prefix_bound':str(gip),'conservative_L_bound':Lbound,'coefficient_heights':coeff_height(generic)},'negative_controls':negative,'word_hashes':{n:hashlib.sha256((o.out/n).read_bytes()).hexdigest()for n in artifacts},'source_pins':{n:hashlib.sha256((prog/n).read_bytes()).hexdigest()for n in deps},'scope':'Exact rational D8 implementation controls for the general Q(i) proof. Every all-width identity follows from the literal group algebra; finite tensor multiplicity checks are controls only. Explicit determinant condition, full physical costs and all five foundations remain. No421 endpoint or supplier.'}
(o.out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],gc,'example',ec)
