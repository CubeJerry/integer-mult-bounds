#!/usr/bin/env python3
"""Independent integer-numerator and polynomial checker; no author-helper import."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json

def plus(z,w):return(z[0]+w[0],z[1]+w[1])
def times(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def matmul(A,B):return tuple(tuple(sumg(times(A[i][k],B[k][j])for k in range(len(B)))for j in range(len(B[0])))for i in range(len(A)))
def sumg(it):
 z=(0,0)
 for w in it:z=plus(z,w)
 return z

def monomial(p,q):
 n=len(p);return tuple(tuple(((-1)**q[j],0)if i==p[j]else(0,0)for j in range(n))for i in range(n))
def star(A):return tuple(tuple((A[j][i][0],-A[j][i][1])for j in range(len(A)))for i in range(len(A)))
def source(mask):
 A=[[(0,0)for _ in range(8)]for _ in range(8)]
 for x in range(8):
  y=(x>>1)|((x&1)<<2);sgn=(-1)**(mask>>y&1);A[y][x]=(sgn,sgn);A[y^2][x]=(sgn,-sgn)
 return tuple(tuple(row)for row in A) # denominator2

def trace(A):return sumg(A[i][i]for i in range(len(A)))
def mulscalar(A,z):return tuple(tuple(times(x,z)for x in row)for row in A)
def anf(f):
 ans=f[:]
 for j in range(3):
  for x in range(8):
   if x>>j&1:ans[x]^=ans[x^(1<<j)]
 return ans

def qsign(coeff):
 la,lc,qac=coeff
 return [((la*(x&1))^(lc*(x>>2&1))^(qac*(x&1)*(x>>2&1)))for x in range(8)]
def check():
 reps={};counts={};witnesses=[];neg={'omit_complement':False,'omit_quadratic':False,'omit_global_sign':False}
 for mask in range(256):
  if mask.bit_count()%2==0:continue
  f=[mask>>x&1 for x in range(8)];f0,la,lb,qab,lc,qac,qbc,eta=anf(f);assert eta==1
  AA=qab;LL=la^lb^lc;BB=qac^qbc;JJ=AA^LL;CC=f0^(AA*(JJ^BB^1))
  rep=sum(((JJ*(x>>2&1))^(BB*(x>>1&1)*(x>>2&1))^((x&1)*(x>>1&1)*(x>>2&1)))<<x for x in range(8))
  Z1=monomial(list(range(8)),qsign((la,lb,qac)));T=Z1
  if AA:
   Z2=monomial(list(range(8)),qsign((0,BB,1)));X=monomial([x^7 for x in range(8)],[0]*8);T=matmul(matmul(Z2,X),Z1)
  lhs=matmul(matmul(T,source(mask)),star(T));rhs=mulscalar(source(rep),((-1)**CC,0));assert lhs==rhs
  counts[(rep,CC)]=counts.get((rep,CC),0)+1;witnesses.append({'mask':mask,'rep':rep,'C':CC})
  if AA and matmul(matmul(Z1,source(mask)),star(Z1))!=rhs:neg['omit_complement']=True
  Zbad=monomial(list(range(8)),qsign((la,lb,0)));Tb=Zbad
  if AA:Tb=matmul(matmul(Z2,X),Zbad)
  if matmul(matmul(Tb,source(mask)),star(Tb))!=rhs:neg['omit_quadratic']=True
  if CC and lhs!=source(rep):neg['omit_global_sign']=True
 assert set(counts)==set((r,c)for r in[128,64,112,176]for c in[0,1])
 assert all(v==16 for v in counts.values()) and all(neg.values())
 expected={128:((0,0),(0,0)),64:((1,1),(0,1)),112:((1,1),(0,0)),176:((0,0),(0,-1))}
 widths=[]
 for rep in expected:
  a=source(rep);t=tuple(F(x,2)for x in trace(a));t2=tuple(F(x,4)for x in trace(matmul(a,a)));t3=tuple(F(x,8)for x in trace(matmul(matmul(a,a),a)));e=tuple((x-y)/2 for x,y in zip(times(t,t),t2));assert(t,e)==expected[rep] and t3!=(0,0)
  reps[rep]={'trace':[str(x)for x in t],'trace_square':[str(x)for x in t2],'e2':[str(x)for x in e],'trace_cube':[str(x)for x in t3]}
  def power(z,V):
   out=(F(1),F(0))
   for _ in range(V):out=times(out,z)
   return out
  for V in range(1,9):
   tv=power(t,V);e2v=tuple((x-y)/2 for x,y in zip(power(t,2*V),power(t2,V)));assert(tv==(0,0),e2v==(0,0))==(t==(0,0),e==(0,0));assert power(t3,V)!=(0,0)
   widths.append({'rep':rep,'V':V,'zero_pattern':[tv==(0,0),e2v==(0,0)]})
 # Symbolic polynomial ring Z[z]; ascending coefficient tuples.
 def polyadd(a,b):
  out=tuple((a[i]if i<len(a)else 0)+(b[i]if i<len(b)else 0)for i in range(max(len(a),len(b))));return trim(out)
 def trim(a):
  while len(a)>1 and a[-1]==0:a=a[:-1]
  return a
 def polymul(a,b):
  out=[0]*(len(a)+len(b)-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):out[i+j]+=x*y
  return trim(tuple(out))
 def pm(A,B):
  out=[]
  for i in range(3):
   row=[]
   for j in range(3):
    z=(0,)
    for k in range(3):z=polyadd(z,polymul(A[i][k],B[k][j]))
    row.append(z)
   out.append(row)
  return out
 def const(A):return [[(z,)for z in row]for row in A]
 K=[[(1,),(0,),(-1,1)],[(0,1),(0,),(0,-1)],[(1,),(1,),(-1,)]]
 B=const([[1,0,-1],[0,0,1],[1,1,-1]])
 for lam in[1,-1]:
  DK=const([[1,0,0],[0,lam,0],[0,0,1]]);EK=const([[1,0,lam-1],[0,1,0],[0,0,lam]])
  target=[[(1,),(0,),(-1,lam)],[(0,lam),(0,),(0,-lam)],[(1,),(1,),(-1,)]]
  assert pm(pm(DK,K),EK)==target and pm(EK,EK)==const([[1,0,0],[0,1,0],[0,0,1]])
  FF=[[(1,),(0,1),(0,)],[(0,1),(0,),(0,)],[(0,),(0,),(1,)]];assert pm(FF,B)==K
 wrong=const([[1,0,-1],[0,1,0],[0,0,-1]]);Dminus=const([[1,0,0],[0,-1,0],[0,0,1]])
 assert pm(pm(Dminus,K),wrong)!=[[(1,),(0,),(-1,-1)],[(0,-1),(0,),(0,1)],[(1,),(1,),(-1,)]]
 return {'status':'PASS_INDEPENDENT_SIGN_CLASS_REVIEW','odd_tables':128,'exact_orbit_sizes':{str(k):v for k,v in counts.items()},'spectral_invariants':reps,'width_controls':widths,'symbolic_sign_bridge':True,'literal_extra_cost':{'unit_ADD':2,'SCALE_minus_one':2,'Gaussian':0,'owners':0},'negative_controls':list(neg)+['wrong_minus_two_shear'],'scope':'four projective classes at everyV; eight exact classes oddV and four evenV; no supplier or kappa claim'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);args=ap.parse_args();result=check();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in['status','odd_tables','exact_orbit_sizes','symbolic_sign_bridge','literal_extra_cost']}))
