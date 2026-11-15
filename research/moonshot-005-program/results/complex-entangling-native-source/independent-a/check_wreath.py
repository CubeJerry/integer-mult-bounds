#!/usr/bin/env python3
"""Independent signed-axis formula, native differences and scope controls."""
import argparse,itertools,hashlib,json
from pathlib import Path
from exact import *
def mm(A,B):return [[sum(A[i][k]*B[k][j]for k in range(len(A)))for j in range(len(A))]for i in range(len(A))]
def sub(A,B):return [[a-b for a,b in zip(x,y)]for x,y in zip(A,B)]
def rank101(A):
 A=[[x%101 for x in r]for r in A];m=len(A);n=len(A[0]);k=0
 for j in range(n):
  p=next((i for i in range(k,m)if A[i][j]),None)
  if p is None:continue
  A[k],A[p]=A[p],A[k];q=pow(A[k][j],-1,101);A[k]=[x*q%101 for x in A[k]]
  for i in range(m):
   if i!=k and A[i][j]:
    q=A[i][j];A[i]=[(x-q*y)%101 for x,y in zip(A[i],A[k])]
  k+=1
  if k==m:break
 return k
def block(E,C,upper=True):
 n=len(E);Z0=[[0]*n for _ in range(n)]
 return [E[i]+C[i]for i in range(n)]+[Z0[i]+E[i]for i in range(n)]if upper else [E[i]+Z0[i]for i in range(n)]+[C[i]+E[i]for i in range(n)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);perms=list(itertools.permutations(range(3)));J=[-1,-1,1]*3;hist={};ordinary=0;native=0
 for local in itertools.product(perms,repeat=3):
  r=sum(p[2]!=2 for p in local)
  for coord in perms:
   p=[3*coord[i]+local[i][z]for i in range(3)for z in range(3)];X0=[[int(p[j]==i)for j in range(9)]for i in range(9)];X1=[[J[i]*X0[i][j]*J[j]for j in range(9)]for i in range(9)];E=sub(X0,X1);assert rank101(E)==2*r
   hist[r]=hist.get(r,0)+1
   if r==0:assert E==[[0]*9 for _ in range(9)];ordinary+=1
   if r==1:
    C=sub(mm(X0,X0),mm(X1,X1));Z0=[[0]*9 for _ in range(9)]
    assert rank101(block(E,Z0))==4 and rank101(block(E,C))==4 and rank101(block(E,C,False))==4
    Xi=list(map(list,zip(*X0)));Yi=list(map(list,zip(*X1)));Ei=sub(Xi,Yi);Ci=sub(mm(Xi,Xi),mm(Yi,Yi));assert rank101(block(Ei,Ci,False))==4;native+=1
 assert sum(hist.values())==1296 and ordinary==48 and native==288
 # These are actual computational monomials; their multi-axis images show
 # why the local9-point permutation representation does not cover them.
 CNOT=permutation([x^((x&1)<<1)for x in range(8)]);CZ=monomial(list(range(8)),[2*(x&1)*((x>>2)&1)for x in range(8)])
 cn=pauli_image(CNOT,1,0);cz=pauli_image(CZ,1,0);assert cn[:2]==(3,0)and cz[:2]==(1,4)
 assert mixing_rank(CNOT)[0]==mixing_rank(CZ)[0]==0
 scope=(a.source/'LOCAL-WREATH-SCOPE.md').read_text();assert 'm≥1' in scope and 'm=0' in scope
 out={'status':'PASS_INDEPENDENT_LOCAL_WREATH_CONSERVATION_CHECKS','proof_sha256':hashlib.sha256((a.source/'LOCAL-WREATH-CONSERVATION.md').read_bytes()).hexdigest(),'scope_correction_sha256':hashlib.sha256((a.source/'LOCAL-WREATH-SCOPE.md').read_bytes()).hexdigest(),'quotient_group_order':1296,'rank_histogram':hist,'ordinary_elements':ordinary,'rank1_native_coefficients':native,'all_source_and_inverse_difference_ranks':4,'literal_CNOT_X0_image':cn,'literal_CZac_X0_image':cz,'zero_native_one_query_price':1,'zero_native_one_query_target':1,'m_at_least1_required_only_for_strict_pricing_corollaries':True,'universal_scope':'Fixed finite uniform one-column local-Clifford wreath group, scalar coefficients may depend on tensor width; all-inventory validity follows from the independently reviewed representation proof, not enumeration.','new_complete_kappa':False}
 (a.out/'WREATH-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
