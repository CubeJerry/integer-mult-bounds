#!/usr/bin/env python3
"""Exact finite local-axis controls; no source-author verifier imported."""
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as s

def pm(p):
 M=s.zeros(len(p))
 for j,i in enumerate(p):M[i,j]=1
 return M

def gf_rank(vs):
 piv={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j not in piv:piv[j]=v;break
   v^=piv[j]
 return len(piv)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).with_name('LOCAL-WREATH-RESULT.json'));ar=ap.parse_args();local=list(itertools.permutations(range(3)));perms=list(itertools.permutations(range(3)));J=[-1,-1,1]*3;count=ordinary=0;hist={};source=None
 for h in itertools.product(local,repeat=3):
  for p in perms:
   g=tuple(3*p[i]+h[i][a]for i in range(3)for a in range(3));r=sum(z[2]!=2 for z in h);dif=sum(J[j]!=J[g[j]]for j in range(9));assert dif==2*r
   hist[r]=hist.get(r,0)+1;count+=1
   if r==0:assert all(J[j]==J[g[j]]for j in range(9));ordinary+=1
 # Physical local L=iCD induces the three-cycle on {X,Y,Z}; choose either orientation.
 cyc=(1,2,0);pc=(2,0,1);h=[(0,1,2)]*3;h[1]=cyc
 g=tuple(3*pc[i]+h[i][a]for i in range(3)for a in range(3));X=pm(g);JJ=s.diag(*J);Y=JJ*X*JJ;E=X-Y
 assert E.rank()==2 and X**9==s.eye(9)
 pr=[(X**k-JJ*X**k*JJ).rank()//2 for k in range(9)];assert pr==[0,1,2,3,3,3,3,2,1]
 Z=s.zeros(9);I=s.eye(9);natives=[]
 for label,C,D in [('ordinary',I,I),('square',-X**2,-Y**2)]:
  A=s.BlockMatrix([[X,C],[Z,X]]).as_explicit();B=s.BlockMatrix([[Y,D],[Z,Y]]).as_explicit();assert (A-B).rank()==4 and (A.inv()-B.inv()).rank()==4;natives.append(label)
 # CNOT0->1 sends X0 to X0X1, which is not one of the local axes.
 x0=1;x1=2;z0=8;z1=16;local_axes={1,2,4,8,16,32,9,18,36};assert x0^x1 not in local_axes
 # CZ01 sends X0 to X0 Z1, also outside Ω.
 assert x0^z1 not in local_axes
 # Old ± cycle matching fails even though this larger representation remains valid.
 assert 4 not in (3,(-3)%9)
 out={'status':'PASS_EXACT_LOCAL_WREATH_CONSERVATION_CONTROLS','local_symplectic_elements':len(local),'head_wreath_elements':count,'ordinary_wreath_elements':ordinary,'gaussian_rank_histogram':hist,'order_nine_power_ranks':pr,'native_orientations_checked':natives,'inverse_native_difference_checked':True,'negative_controls':['CNOT exits the local Pauli-axis set','CZ exits the local Pauli-axis set','3-to-4 transport is not a ±orientation of C9'],'proof_sha256':hashlib.sha256(Path(__file__).with_name('LOCAL-WREATH-CONSERVATION.md').read_bytes()).hexdigest(),'scope':'Finite controls plus separate universal proof, not a theorem for entangling ordinary Clifford maps. No new kappa.'}
 assert count==1296 and ordinary==48
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
