#!/usr/bin/env python3
"""Independent integer-Gaussian source and free noncommutative block checks."""
from pathlib import Path
from hashlib import sha256
from argparse import ArgumentParser
import json

def need(q,msg):
 if not q:raise ValueError(msg)
def ga(a,b):return(a[0]+b[0],a[1]+b[1])
def gm(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def zero(n):return[[(0,0)for _ in range(n)]for _ in range(n)]
def eye(n):
 z=zero(n)
 for i in range(n):z[i][i]=(1,0)
 return z
def mm(a,b):
 n=len(a);z=zero(n)
 for i in range(n):
  for k in range(n):
   if a[i][k]!=(0,0):
    for j in range(n):
     if b[k][j]!=(0,0):z[i][j]=ga(z[i][j],gm(a[i][k],b[k][j]))
 return z
def adj(a):return[[(a[j][i][0],-a[j][i][1])for j in range(len(a))]for i in range(len(a))]
def scale(a,k):return[[(k*x,k*y)for x,y in r]for r in a]
def supp(a):
 rr=[sum(z!=(0,0)for z in r)for r in a];cc=[sum(a[i][j]!=(0,0)for i in range(len(a)))for j in range(len(a))];need(len(set(rr+cc))==1,'flat row/column support');return rr[0]
def pa(a,b):
 z=dict(a)
 for k,v in b.items():z[k]=z.get(k,0)+v
 return{k:v for k,v in z.items()if v}
def ps(a,k):return{t:k*v for t,v in a.items()if k*v}
def normword(w):
 r=[]
 for t in w:
  if r and ((r[-1],t)in [('a','ai'),('ai','a')]):r.pop()
  else:r.append(t)
 return tuple(r)
def pm(a,b):
 z={}
 for x,v in a.items():
  for y,w in b.items():
   t=normword(x+y);z[t]=z.get(t,0)+v*w
 return{k:v for k,v in z.items()if v}
def bm(a,b):return[[sum_poly([pm(a[i][k],b[k][j])for k in range(3)])for j in range(3)]for i in range(3)]
def sum_poly(rows):
 z={}
 for r in rows:z=pa(z,r)
 return z

def main():
 ap=ArgumentParser();ap.add_argument('--proof',type=Path,required=True);ap.add_argument('--pins',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 N=zero(16)
 for j in range(16):
  a,b,c,d=[(j>>k)&1 for k in range(4)];r=b+2*c+4*d+8*a;s=(-1)**(a*b*d)
  N[r][j]=(s,s);N[r^2][j]=(s,-s)
 need(mm(N,adj(N))==mm(adj(N),N)==scale(eye(16),4),'exact unitary source numerator')
 powers=[eye(16)]
 for r in range(4):powers.append(mm(powers[-1],N))
 need([supp(p)for p in powers]==[1,2,4,8,16],'support strata')
 for r,p in enumerate(powers):
  need(all(x*x+y*y==2**r for row in p for x,y in row if(x,y)!=(0,0)),'flat source power moduli')
 inv2=mm(adj(N),adj(N));need(mm(inv2,powers[2])==scale(eye(16),16),'quadratic ordinary control')
 probes=[]
 for s,t in [(0,0),(0,1),(1,2),(2,3)]:
  M=zero(16)
  for j in range(16):
   out=j
   if ((j>>s)^(j>>t))&1:out^=(1<<s)|(1<<t)
   M[out][j]=(1,0)
  for r in [3,4]:
   for label,P in [('left',mm(mm(inv2,M),powers[r])),('right',mm(mm(powers[r],M),inv2))]:
    maxnorm=max(x*x+y*y for row in P for x,y in row)
    # denominator 2^(2+r), so squared bound <=1/2.
    need(2*maxnorm<=2**(2*(2+r)),'inverse pullback strict nonmonomial bound')
    probes.append([s,t,r,label,maxnorm,2**(2*(2+r))])
 Z={};I={():1};a={('a',):1};ai={('ai',):1};a2=pm(a,a);ai2=pm(ai,ai)
 L=[[a,Z,Z],[I,a,Z],[Z,Z,I]];Li=[[ai,Z,Z],[ps(ai2,-1),ai,Z],[Z,Z,I]];U=[[a,ps(a2,-1),Z],[Z,a,Z],[Z,Z,I]]
 need(bm(L,Li)==bm(Li,L)==[[I,Z,Z],[Z,I,Z],[Z,Z,I]],'formal inverse ordered correctly')
 C=[[{(f'c{i}{j}',):1}for j in range(3)]for i in range(3)];Q=[[{(f'q{i}{j}',):1}for j in range(3)]for i in range(3)]
 C[0][2]=C[2][2]=Q[2][1]=Q[2][2]=Z
 E=bm(bm(bm(bm(L,C),U),Q),L)
 c=lambda i,j:C[i][j];q=lambda i,j:Q[i][j]
 expected22=sum_poly([pm(pm(c(2,0),a),q(0,2)),ps(pm(pm(c(2,0),a2),q(1,2)),-1),pm(pm(c(2,1),a),q(1,2))])
 expected02=pm(a,sum_poly([pm(pm(c(0,0),a),q(0,2)),ps(pm(pm(c(0,0),a2),q(1,2)),-1),pm(pm(c(0,1),a),q(1,2))]))
 need(E[2][2]==expected22 and E[0][2]==expected02,'free noncommutative active-column identities')
 proof=args.proof;pins=args.pins
 pin=json.loads(pins.read_text());need(sha256(proof.read_bytes()).hexdigest()==pin['local_proof_sha256'],'author proof pin')
 repo=args.repo
 for p,h in pin['dependencies'].items():need(sha256((repo/p).read_bytes()).hexdigest()==h,'retained dependency '+p)
 result={'status':'PASS_INDEPENDENT_CUBIC_SOURCE_AND_ORDERED_BLOCK_CONTROLS','author_proof_sha256':pin['local_proof_sha256'],'author_source_pins_sha256':sha256(pins.read_bytes()).hexdigest(),'source_power_supports':[1,2,4,8,16],'inverse_pullback_probes':probes,'quadratic_inverse_power_control':True,'free_noncommutative_block_equations_checked':['L inverse left','L inverse right','flagged E22','flagged E02'],'all_width_claim':'Accepted by separate proof review, not inferred from this finite source test.','new_complete_kappa':False}
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
