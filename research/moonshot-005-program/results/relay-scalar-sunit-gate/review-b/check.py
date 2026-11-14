#!/usr/bin/env python3
"""Independent scalar-family arithmetic: no author implementation imported."""
from fractions import Fraction as Q
from pathlib import Path
from math import gcd
import gzip,json,hashlib,argparse

def need(c,m):
 if not c:raise ValueError(m)
def unit(q):
 q=Q(q)
 for z in(abs(q.numerator),q.denominator):
  if z==0:return False
  for p in(2,3,5):
   while z%p==0:z//=p
  if z!=1:return False
 return True
triples=[(1,1,2),(1,2,3),(1,3,4),(1,4,5),(2,3,5),(1,5,6),(3,5,8),(1,8,9),(4,5,9),(1,9,10),(1,15,16),(1,24,25),(9,16,25),(2,25,27),(5,27,32),(1,80,81),(3,125,128)]
orbits=[]
for a,b,c in triples:
 need(a+b==c and gcd(a,b)==1 and all(unit(x)for x in(a,b,c)),'coprime S235 triple')
 t=Q(a,c);o=frozenset([t,1-t,1/t,1/(1-t),t/(t-1),(t-1)/t]);orbits.append(o)
need(len(set(orbits))==17,'seventeen distinct published-count witnesses')
xs=set().union(*orbits);need(len(xs)==99,'sixfold symmetry count with exceptional orbit')
lams=[]
for x in xs:
 if x==Q(4,9):continue
 l=(1-2*x)/(8-18*x)
 if not l:continue
 if not unit(Q(1,l.denominator)):continue
 if all(unit(1-e*l)for e in[8,9,10,13]):lams.append(l)
need(sorted(lams)==[Q(1,18),Q(1,12),Q(7,64),Q(1,5),Q(1,4)],'complete conditional finite list')
quad={str(l):str((1-9*l)**2-l*l/2)for l in sorted(lams)}
need(all(not unit(Q(q))for q in quad.values()),'no quadratic unit')
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--proof',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();repo=args.repo;src=repo/'research/moonshot-005-program/results/proper-chart-relay/author/20/WORD.json.gz';need(hashlib.sha256(src.read_bytes()).hexdigest()=='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c','source pin');w=json.loads(gzip.decompress(src.read_bytes()))
def root(b):
 if b.bit_count()==3:return[2 if b>>i&1 else-1 for i in range(9)]
 z=[i for i in range(9)if not(b>>i&1)];need(len(z)==2,'native root');return[3*(int(i==z[0])-int(i==z[1]))for i in range(9)]
roots=[root(z)for z in w['relay']['ground_Gram_frame']];gs=[]
for h in w['relay']['unrestored_ports']:
 r=root(w['frames'][w['initial'][w['source_role_map'][str(h)]]][0]);gs.append([Q(sum(x*y for x,y in zip(r,t)),18)for t in roots])
C=[[sum(r[i]*r[j]for r in gs)for j in range(8)]for i in range(8)]
cols=[[1,1,1,1,0,0,0,0],[1,-1,1,-1,0,0,0,0],[0,0,0,0,1,1,-1,1],[0,0,0,0,1,-1,-1,-1],[1,0,-1,0,0,0,0,0],[0,0,0,0,1,0,1,0],[0,1,0,-1,0,0,0,0],[0,0,0,0,0,1,0,-1]]
B=[[Q(0)for _ in range(8)]for _ in range(8)]
for i,v in enumerate([13,8,10,9]):B[i][i]=v
for j in[4,6]:B[j][j]=Q(17,2);B[j+1][j+1]=Q(19,2);B[j][j+1]=B[j+1][j]=Q(-1,2)
# Direct intertwining CP=PB, with mutually orthogonal nonzero columns.
need(all(sum(C[i][k]*cols[j][k]for k in range(8))==sum(cols[k][i]*B[k][j]for k in range(8))for i in range(8)for j in range(8)),'actual Gram block decomposition')
need(all(sum(x*y for x,y in zip(cols[i],cols[j]))==0 for i in range(8)for j in range(8)if i!=j),'basis independence')
proof=args.proof;out={'status':'PASS_INDEPENDENT_SCALAR_FAMILY_REVIEW','reviewed_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'orbit_count':17,'ordered_solution_count':99,'lambda_candidates':list(quad),'quadratic_factors':quad,'source_polynomial_verified_by':'independently reconstructed exact dyadic block intertwiner CP=PB','published_completeness':'von Kanel--Matschke arXiv1605.06079v1 TheoremA n3; read manuscript p7 and symmetry count preceding it','no_new_kappa':True}
args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2))
