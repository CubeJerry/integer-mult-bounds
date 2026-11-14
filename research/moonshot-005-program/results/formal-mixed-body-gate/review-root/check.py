#!/usr/bin/env python3
"""Independent exact coefficient replay in noncommutative matrix coefficients."""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
I=((1,0),(0,1));Z=((0,0),(0,0))
def add(a,b):return tuple(tuple(a[i][j]+b[i][j]for j in range(2))for i in range(2))
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(2))for j in range(2))for i in range(2))
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def pm(a,b):
 c={}
 for x,A in a.items():
  for y,B in b.items():c[x^y]=add(c.get(x^y,Z),mul(A,B))
 return {x:A for x,A in c.items()if A!=Z}
def need(x,m):
 if not x:raise ValueError(m)
def main(out):
 pins={'PROOF.md':'d3d22117a4e333e71fb93baadea38a09cc7862d088f14f5a7cf12aee675fce20','MANIFEST.json':'459e7c8a947b00cc4d40e4ba714596143800fba0e368c9580b344e7126e2b064'}
 for n,h in pins.items():need(hashlib.sha256((HERE/'source'/n).read_bytes()).hexdigest()==h,'pin '+n)
 tests=[]
 for m in range(1,8):
  G=[((1,j+1),(j+1,1+(j+1)**2))for j in range(m+1)]
  E=[((2+j,2),(1,3+j))for j in range(m)];C=[((0,j+1),(0,0))for j in range(m)]
  need(all(det(x)!=0 for x in G+E),'invertible surroundings')
  W={0:G[0]}
  for j in range(m):W=pm({0:G[j+1]},pm({1<<j:E[j],0:C[j]},W))
  for s in range(m):
   exact=G[0]
   for j in range(m):exact=mul(G[j+1],mul(C[j]if j==s else E[j],exact))
   degree=(1<<m)-1-(1<<s);need(W.get(degree,Z)==exact and exact!=Z and det(exact)==0,'unique incomplete degree and nonzero rank one')
   tests.append({'m':m,'missing_stage':s+1,'degree':degree,'coefficient':[list(row)for row in exact]})
 # The coefficient algebra is noncommutative in this check.
 need(mul(G[0],E[0])!=mul(E[0],G[0]),'noncommuting control')
 c=((0,1),(0,0));nc=((0,-1),(0,0));need(pm({1:I,0:c},{1:I,0:nc})=={0:I},'repeated-body escape')
 r={'status':'PASS_INDEPENDENT_NONCOMMUTATIVE_PARITY_COEFFICIENTS','proof_pins':pins,'exact_controls':tests,'noncommuting_coefficient_algebra':True,'repeated_body_cancellation':True,'scope':'Universal statement is the direct-sum/unique-term proof. Physical applicability requires a separate representation.','new_kappa':False}
 out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':r['status'],'coefficient_controls':len(tests)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');main(p.parse_args().output)
