#!/usr/bin/env python3
"""Independent first-column normal form and complete square-algebra controls."""
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser()
for n in ['repo','proof','out']:p.add_argument('--'+n,type=Path,required=True)
o=p.parse_args()
def add(*xs):
 z={}
 for d in xs:
  for w,c in d.items():z[w]=z.get(w,0)+c
 return{k:c for k,c in z.items()if c}
def neg(x):return{k:-c for k,c in x.items()}
def mul(x,y):
 z={}
 for u,c in x.items():
  for v,d in y.items():z[u+v]=z.get(u+v,0)+c*d
 return{k:c for k,c in z.items()if c}
def mm(A,B):return[[add(*(mul(A[i][k],B[k][j])for k in range(len(B))))for j in range(len(B[0]))]for i in range(len(A))]
def w(*letters):return{tuple(letters):1}
z={};one=w();a=w('a');L=[[a,z,z],[one,a,z],[z,z,one]];U=[[a,neg(w('a','a')),z],[z,a,z],[z,z,one]]
C=[[w(x)for x in row]for row in [('s','b','c'),('t','d','e'),('u','f','g')]];Q=[[w('q%d%d'%(i,j))for j in range(3)]for i in range(3)]
P=mm(mm(L,C),U)
expected=[[w('a','s','a'),add(w('a','b','a'),neg(w('a','s','a','a'))),w('a','c')],[add(w('s','a'),w('a','t','a')),add(w('b','a'),w('a','d','a'),neg(w('s','a','a')),neg(w('a','t','a','a'))),add(w('c'),w('a','e'))],[w('u','a'),add(w('f','a'),neg(w('u','a','a'))),w('g')]]
assert P==expected
def clean(d):
 out={}
 for letters,c in d.items():
  letters=list(letters)
  for i in range(len(letters)-1):
   if letters[i]=='a'and letters[i+1]in ['s','t']:letters[i],letters[i+1]=letters[i+1]+'hat','a'
  key=tuple(letters);out[key]=out.get(key,0)+c
 return{k:v for k,v in out.items()if v}
P=[[clean(cell)for cell in row]for row in P];E=mm(mm(P,Q),L)
degree=lambda d,k:{u:c for u,c in d.items()if u.count('a')==k}
for j in [0,1]:assert[degree(E[i][j],4)for i in range(3)]==[neg(w('shat','a','a','a',f'q1{j}','a')),neg(w('that','a','a','a',f'q1{j}','a')),z]
assert[degree(E[i][2],3)for i in range(3)]==[neg(w('shat','a','a','a','q12')),neg(w('that','a','a','a','q12')),z]
def remove(d,names):return{u:c for u,c in d.items()if not(set(u)&set(names))}
Er=[[remove(cell,['q12'])for cell in row]for row in E]
assert[degree(Er[i][2],2)for i in range(3)]==[w('shat','a','a','q02'),w('that','a','a','q02'),z]
assert[degree(Er[i][2],0)for i in range(3)]==[z,w('c','q22'),w('g','q22')]
Er=[[remove(cell,['q12','q02','c','g'])for cell in row]for row in E]
assert[Er[i][2]for i in range(3)]==[z,w('a','e','q22'),z]
for j in [0,1]:assert degree(Er[2][j],3)==neg(w('u','a','a',f'q1{j}','a'))
after=[[remove(cell,['u','q11'])for cell in row]for row in Er]
assert[degree(after[i][1],3)for i in range(3)]==[w('shat','a','a','q01','a'),w('that','a','a','q01','a'),z]

# Literal source, including absolute phases, reconstructed independently.
I=s.eye(16);P0=s.zeros(16);X=[s.zeros(16)for _ in range(4)];D=s.eye(16)
for j in range(16):
 aa,bb,cc,dd=[(j>>k)&1 for k in range(4)];P0[(j>>1)|((j&1)<<3),j]=1;D[j,j]=(-1)**(aa*cc*dd)
 for k in range(4):X[k][j^(1<<k),j]=1
tidy=lambda M:M.applyfunc(s.expand)
C0=[((1+s.I)*I+(1-s.I)*x)/2 for x in X];S=D*P0;A=tidy(C0[1]*S);R2=tidy((C0[0]*C0[1]).adjoint()*A*A)
for j in range(16):
 aa,bb,cc,dd=[(j>>k)&1 for k in range(4)];dst=(cc^(aa*bb))+2*dd+4*aa+8*bb;phase=s.I**(aa*bb)*(-1)**(aa*bb*(cc+dd))
 assert R2[:,j]==s.eye(16)[:,dst]*phase

# J=R2^-1 T R2 permutes original(a,b) independently of(c,d).
# Exhaust every possible two-fibre transition and root-four phase. The proof
# is disjoint output spectator pairs; this larger local census is a control.
def gm(x,y):return(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def ga(x,y):return(x[0]+y[0],x[1]+y[1])
def gs(x,k):return(x[0]*k,x[1]*k)
phases=[(1,0),(0,1),(-1,0),(0,-1)]
def branches(j):
 aa,bb,cc,dd=[(j>>k)&1 for k in range(4)];r=(j>>1)|((j&1)<<3);sgn=(-1)**(aa*bb*dd)
 return[(r,gs((1,1),sgn)),(r^2,gs((1,-1),sgn))]
cases=0
for src in range(16):
 right=branches(src);assert(right[0][0]&3)!=(right[1][0]&3)
 for j,k in itertools.product(range(16),repeat=2):
  if(j&3)==(k&3):continue
  for ph,qh in itertools.product(phases,repeat=2):
   col={}
   for middle,phase,(_,coef)in zip([j,k],[ph,qh],right):
    for dest,left in branches(middle):col[dest]=ga(col.get(dest,(0,0)),gm(left,gm(phase,coef)))
   col={dest:c for dest,c in col.items()if c!=(0,0)}
   assert len(col)==4 and all(c[0]*c[0]+c[1]*c[1]==4 for c in col.values())
   cases+=1
assert cases==49152

# Actual noncommuting normal-form unit with genuine idle coupling. This is
# only a premise control, not a positive421 endpoint.
Da=s.diag(*[s.I**(j&1)for j in range(16)]);Db=s.diag(*[s.I**((j>>1)&1)for j in range(16)])
ss=Db;tt=(I+Db*Db)/2;bb=X[0]*X[1];uu=X[2];ee=Da;ff=I+uu*ss.adjoint()*bb;dd=X[1];Z=s.zeros(16)
actual=ss.row_join(bb).row_join(Z).col_join(tt.row_join(dd).row_join(ee)).col_join(uu.row_join(ff).row_join(Z))
r10=-uu*ss.adjoint();r12=I;r00=ss.adjoint()-ss.adjoint()*bb*r10;r02=-ss.adjoint()*bb
r20=-ee.adjoint()*(tt*r00+dd*r10);r22=-ee.adjoint()*(tt*r02+dd)
actual_inv=r00.row_join(Z).row_join(r02).col_join(r10.row_join(Z).row_join(r12)).col_join(r20.row_join(ee.adjoint()).row_join(r22))
assert tidy(actual*actual_inv)==tidy(actual_inv*actual)==s.eye(48)
assert tidy(A*ss*A.adjoint())==Da and tidy(A*tt*A.adjoint())==(I+Da*Da)/2
assert ss*bb!=bb*ss and ee*bb!=bb*ee
outside=S.adjoint();word2=tidy(A*outside*A);word3=tidy(A*A*outside*A);conj=tidy(A*A*outside*(A*A).adjoint())
support=lambda M:sorted({sum(z!=0 for z in row)for row in M.tolist()})
assert support(word2)==[1]and support(word3)==[2]and support(conj)==[4]
prog=o.repo/'research/moonshot-005-program';deps=['results/complex-source-square-controls/ADMISSION.md','results/complex-first-interface-gates/ADMISSION.md','results/complex-four-bit-cubic-source/author/PROOF.md']
r={'status':'PASS_ROOT_CLEAN_FIRST_COLUMN_SQUARE_ALGEBRA_REVIEW','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'formal_noncommuting_product_and_component_degree_equations':True,'literal_R2_formula':'(a,b,c,d)->(c xor ab,d,a,b), phase i^(ab)*(-1)^(ab(c+d))','independent_four_path_cases':cases,'four_path_integer_denominator':4,'all_four_path_amplitudes_abs':'1/2','noncommuting_normal_form_control':{'two_sided_unit':True,'both_clean_first_blocks':True,'actual_idle_coupling':True,'not_a_positive_endpoint':True},'outside_square_control':{'ordinary':'S^-1','support_AqA':[1],'support_A2qA':[2],'support_A2qAinv2':[4],'not_a_positive_endpoint':True},'source_pins':{n:hashlib.sha256((prog/n).read_bytes()).hexdigest()for n in deps},'scope':'Universal direct-image and word-class proof reviewed separately. No B execution code imported. Finite path census is a control. Fixed catalogue, phases, physical costs and all global foundations retained.'}
o.out.parent.mkdir(parents=True,exist_ok=True);o.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
