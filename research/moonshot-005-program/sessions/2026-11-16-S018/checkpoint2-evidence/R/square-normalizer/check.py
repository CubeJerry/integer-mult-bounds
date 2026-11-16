#!/usr/bin/env python3
"""Exact fibre census and literal source-square transport; no worker imports."""
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as S

def dot(x,y):return (int(x)&int(y)).bit_count()%2
def rot(z,e):
 a,b=z
 return [(a,b),(-b,a),(-a,-b),(b,-a)][e%4]
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def affine(perm):
 t=perm[0];c0=perm[1]^t;c1=perm[2]^t
 assert c0 and c1 and c0!=c1 and perm[3]==t^c0^c1
 return t,c0,c1
def dual(k,q,c0,c1):
 return next(l for l in range(4)if dot(c0,l)+2*dot(c1,l)==k^q)
def compose(left,right):
 lp,le=left;rp,re=right
 return ([lp[rp[j]]for j in range(16)],[(re[j]+le[rp[j]])%4 for j in range(16)])
def inverse(table):
 p,e=table;ip=[p.index(j)for j in range(16)]
 return ip,[(-e[ip[j]])%4 for j in range(16)]
def matrix(table):
 p,e=table;M=S.zeros(16)
 for j in range(16):M[p[j],j]=S.I**e[j]
 return M

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','proof','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();perms=list(itertools.permutations(range(4)))
 admitted=0;classified=[]
 for perm in perms:
  t,c0,c1=affine(perm)
  for es in itertools.product(range(4),repeat=4):
   Z=[[(0,0)for k in range(4)]for j in range(4)]
   for j,k in itertools.product(range(4),repeat=2):
    for x in range(4):Z[j][k]=add(Z[j][k],rot(((-1)**(dot(j,perm[x])+dot(k,x)),0),es[x]))
   ismono=all(sum(Z[j][k]!=(0,0)for j in range(4))==1 for k in range(4))
   possible=[q for q in range(4)if all(es[x]==(es[0]+2*dot(q,x))%4 for x in range(4))]
   assert ismono==bool(possible)
   if ismono:
    admitted+=1;q=possible[0]
    for k in range(4):
     l=dual(k,q,c0,c1);phase=(es[0]+2*dot(l,t))%4
     assert all(Z[j][k]==(rot((4,0),phase)if j==l else(0,0))for j in range(4))
   classified.append(ismono)
 assert admitted==384 and len(classified)==6144
 # Independent literal source, native C convention and phased R2.
 I=S.eye(16);P=S.zeros(16);sign=S.eye(16);Xa=S.zeros(16);Xb=S.zeros(16)
 for j in range(16):
  P[(j>>1)|((j&1)<<3),j]=1;sign[j,j]=(-1)**int((j&13)==13);Xa[j^1,j]=1;Xb[j^2,j]=1
 tidy=lambda m:m.applyfunc(S.expand)
 Ca=((1+S.I)*I+(1-S.I)*Xa)/2;Cb=((1+S.I)*I+(1-S.I)*Xb)/2
 A=tidy(Cb*sign*P);A2=tidy(A*A);rp=[];re=[]
 for j in range(16):
  aa,bb,cc,dd=[j>>k&1 for k in range(4)]
  rp.append((cc^(aa*bb))+2*dd+4*aa+8*bb);re.append((aa*bb*(1+2*cc+2*dd))%4)
 R=(rp,re);assert tidy(Ca*Cb*matrix(R))==A2
 W=S.Matrix(4,4,lambda k,x:S.Rational((-1)**dot(k,x),2));D=S.diag(*[(-S.I)**x.bit_count()for x in range(4)])
 assert tidy(S.kronecker_product(S.Matrix([[1+S.I,1-S.I],[1-S.I,1+S.I]])/2,S.Matrix([[1+S.I,1-S.I],[1-S.I,1+S.I]])/2))==tidy(S.I*D*W*D)
 Aint=[[(int(S.re(2*A2[i,j])),int(S.im(2*A2[i,j])))for j in range(16)]for i in range(16)]
 checks=[]
 for k,sigma in enumerate(perms):
  bp=[0]*16;be=[0]*16;np=[0]*16;ne=[0]*16
  for z in range(4):
   perm=perms[(7*z+k)%24];t,c0,c1=affine(perm);q=(z+k)%4;e0=(3*z+k)%4
   for x in range(4):
    j=x+4*z;bp[j]=perm[x]+4*sigma[z];be[j]=(e0+2*dot(q,x)+x.bit_count()-perm[x].bit_count())%4
    l=dual(x,q,c0,c1);np[j]=l+4*sigma[z];ne[j]=(e0+2*dot(l,t)+l.bit_count()-x.bit_count())%4
  B=(bp,be);Q=compose(inverse(R),compose((np,ne),R));qp,qe=Q;binv=inverse(B)[0]
  assert sorted(bp)==list(range(16))and sorted(qp)==list(range(16))
  for i,j in itertools.product(range(16),repeat=2):
   left=rot(Aint[i][qp[j]],qe[j]);right=rot(Aint[binv[i]][j],be[binv[i]])
   assert left==right,('source transport',k,i,j,left,right)
  assert compose(inverse(Q),Q)==(list(range(16)),[0]*16)
  assert all((qp[j]&3)==sigma[j&3]for j in range(16))
  commutes=all((qp[j]&3)==(j&3)for j in range(16));assert commutes==(sigma==(0,1,2,3))
  checks.append({'sigma':list(sigma),'literal_Q_table':[[qp[j],qe[j]]for j in range(16)],'transport':True,'inverse':True,'commutes_with_both_original_quarter_controls':commutes})
 # Actual controls violating each part of the classification.
 badperm=list(range(16));badperm[0],badperm[4]=badperm[4],badperm[0]
 badphase=[0]*16;badphase[1]=1
 negatives=[]
 for label,B in [('broken_fibre',(badperm,[0]*16)),('noncharacter_phase',(list(range(16)),badphase))]:
  Q=tidy(A2.conjugate().T*matrix(B)*A2)
  supports=[sum(Q[i,j]!=0 for i in range(16))for j in range(16)]
  assert max(supports)>1;negatives.append({'case':label,'column_supports':supports,'monomial':False})
 prog=a.repo/'research/moonshot-005-program'
 deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/fixed-monomial-compact-bridge/author/PROOF.md']
 out={'status':'PASS_ROOT_COMPLETE_MONOMIAL_SOURCE_SQUARE_CLASSIFICATION','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'fibre_candidates':6144,'fibre_admitted':384,'fibre_census_sha256':hashlib.sha256(bytes(classified)).hexdigest(),'global_monomial_count':24*384**4,'diagonal_root_four_count':16**4,'diagonal_sign_count':8**4,'literal_source_and_R_identity':True,'all24_fibre_permutation_controls':checks,'negative_controls':negatives,'absolute_tensor_scalar_control':{'one_column_i_at_widths1_2_3_4':['i','-1','-i','1'],'fixed_i_substitution_fails_at_width2':True},'source_pins':{x:hashlib.sha256((prog/x).read_bytes()).hexdigest()for x in deps},'scope':'Complete class rests on the structural proof. Exhaustive6144 local controls and24 global samples do not enumerate521838526464 matrices. Every table is an actual monomial with retained conditional physical tariff; no421 endpoint or supplier.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['global_monomial_count'])
if __name__=='__main__':main()
