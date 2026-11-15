#!/usr/bin/env python3
"""Independent symplectic-cycle, bimodule and rank-potential diagnostics."""
from pathlib import Path
from itertools import product,combinations
import json
import sympy as s

def apply(A,x):
 y=0
 while x:
  b=x&-x;y^=A[b.bit_length()-1];x^=b
 return y
def mul(A,B):return tuple(apply(A,b)for b in B)
def span(A):
 S={0}
 for a in A:S|={x^a for x in list(S)}
 return frozenset(S)
def pairing(x,y):return (((x&7)&(y>>3)).bit_count()+((y&7)&(x>>3)).bit_count())%2
def transpose(A):return tuple(sum(((A[i]>>j)&1)<<i for i in range(len(A)))for j in range(len(A)))
def inverse3(A):
 tab={apply(A,x):x for x in range(8)};assert len(tab)==8
 return tuple(tab[1<<i]for i in range(3))
def stabilizers():
 result=[]
 for A in product(range(1,8),repeat=3):
  if len(span(A))!=8:continue
  B=transpose(inverse3(A))
  for vals in product((0,1),repeat=6):
   M=[[0]*3 for _ in range(3)]
   for (i,j),v in zip([(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)],vals):M[i][j]=M[j][i]=v
   S=tuple(sum(M[i][j]<<i for i in range(3))for j in range(3))
   H=tuple(A[j]|(apply(B,S[j])<<3)for j in range(3))+tuple(b<<3 for b in B)
   assert all(pairing(H[i],H[j])==int(abs(i-j)==3)for i in range(6)for j in range(i))
   result.append(H)
 assert len(set(result))==10752
 return result

def partial_cycle_tests():
 counts={}
 for n in range(4,13,2):
  d=n//2;dist=lambda i,j:min((i-j)%n,(j-i)%n);count=0
  choices=[[None,j]if j==d else[None,j,(-j)%n]for j in range(1,n)]
  for row in product(*choices):
   f={0:0}|{j:v for j,v in enumerate(row,1)if v is not None}
   if len(set(f.values()))!=len(f):continue
   if not all(dist(i,j)==dist(f[i],f[j])for i,j in combinations(f,2)):continue
   assert all(v==j for j,v in f.items())or all(v==(-j)%n for j,v in f.items());count+=1
  counts[n]=count
 return counts
def physical_source():
 I=s.eye(8);X=[];Z=[]
 for b in range(3):
  M=s.zeros(8)
  for j in range(8):M[j^(1<<b),j]=1
  X.append(M);Z.append(s.diag(*[(-1)**(j>>b&1)for j in range(8)]))
 S=s.zeros(8)
 for j,k in enumerate([0,4,1,5,2,6,3,7]):S[k,j]=1
 A=((1+s.I)*I+(1-s.I)*X[1])/2*S
 def same(B,C):return all(s.expand(z)==0 for z in B-C)
 paulis={}
 for x,z in product(range(8),repeat=2):
  M=I
  for b in range(3):
   if x>>b&1:M=M*X[b]
  for b in range(3):
   if z>>b&1:M=M*Z[b]
  paulis[x|(z<<3)]=M
 cols=[]
 for P in X+Z:
  M=s.simplify(A*P*A.conjugate().T);matches=[v for v,N in paulis.items()if any(same(M,c*N)for c in [1,-1,s.I,-s.I])];assert len(matches)==1;cols.append(matches[0])
 assert cols==[4,1,2,32,8,18] and same(A**6,X[0]*X[1]*X[2]) and same(A**12,I)
 return tuple(cols)
def dihedral_potential():
 X=s.zeros(6);T=s.zeros(6)
 for j in range(6):X[(j+1)%6,j]=1;T[(2-j)%6,j]=1
 P=s.diag(1,1,1,-1,-1,-1);I=s.eye(6);Z=s.zeros(6);Y=P*X*P
 assert T*T==I and T*X*T==X.inv() and P*T==T*P
 assert [(X**k-P*X**k*P).rank()for k in range(6)]==[0,2,4,6,4,2]
 def block(A,B):return s.BlockMatrix([[A,B],[Z,A]]).as_explicit()
 Lx=block(X,I);Ly=block(Y,I);Ux=block(X,-X*X);Uy=block(Y,-Y*Y)
 assert (Lx-Ly).rank()==4 and(Ux-Uy).rank()==4
 assert(Lx.inv()-Ly.inv()).rank()==4 and(Ux.inv()-Uy.inv()).rank()==4
 # Reflection fixing0 has the right group relation but not the required sign agreement.
 bad=s.zeros(6)
 for j in range(6):bad[(-j)%6,j]=1
 assert bad*X*bad==X.inv() and bad*P!=P*bad
 # Augmentation invertibility alone does not make an unscaled shadow a unit.
 Rplus=s.eye(3);Rminus=s.eye(3);assert(Rplus+Rminus).det()!=0 and(Rplus-Rminus).det()==0
 assert all((Rplus+c*Rminus).det()!=0 for c in [2,-2])
 return {'native_L_U_inverse_difference_ranks':4,'endpoint_rank_pattern':[0,2,4,6,4,2],'wrong_reflection_rejected':True,'unit_deformation_control':True}
def main():
 identity=(1,2,4,8,16,32);A=physical_source();powers=[identity]
 for _ in range(5):powers.append(mul(A,powers[-1]))
 assert mul(A,powers[-1])==identity and len(set(powers))==6
 L0=span([8,16,32]);cycle=[frozenset(apply(p,v)for v in L0)for p in powers];assert len(set(cycle))==6
 assert all(3-(len(cycle[i]&cycle[j]).bit_length()-1)==min((i-j)%6,(j-i)%6)for i,j in product(range(6),repeat=2))
 H=stabilizers();where={L:i for i,L in enumerate(cycle)};shadow={};components=0;partial_types=set()
 for h in H:
  partial={j:where[L]for j,C in enumerate(cycle)if(L:=frozenset(apply(h,v)for v in C))in where};assert partial[0]==0
  possible=[e for e in [1,-1]if all(k==(e*j)%6 for j,k in partial.items())];assert possible;partial_types.add(tuple(sorted(partial.items())))
  if h in shadow:continue
  components+=1;eps=possible[0]
  for u,v in product(range(6),repeat=2):
   g=mul(powers[u],mul(h,powers[v]));value=((u+eps*v)%6,eps)
   if g in shadow:assert shadow[g]==value
   else:shadow[g]=value
 assert all(shadow[h][0]==0 for h in H) and all(shadow[p]==(j,1)for j,p in enumerate(powers))
 for g,(j,e)in shadow.items():assert shadow[mul(A,g)]==((j+1)%6,e)and shadow[mul(g,A)]==((j+e)%6,e)
 assert components==8955 and len(shadow)==322236
 out={'status':'PASS_ROOT_DIHEDRAL_SHADOW_REVIEW','physical_source_symplectic_columns':list(A),'source_sixth_power':'X_a X_b X_c, not scalar identity','cycle_distances':[0,1,2,3,2,1],'ordinary_stabilizers':len(H),'relevant_double_cosets':components,'basis_elements_checked':len(shadow),'partial_stabilizer_types':len(partial_types),'even_cycle_partial_map_controls':partial_cycle_tests(),'dihedral':dihedral_potential(),'scope':'Exact finite geometry and independent source/unit/rank diagnostics; universal bimodule and faithful all-width quotient arguments reviewed separately; general endpoint Clifford gauges outside scope','new_complete_kappa':False}
 Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
