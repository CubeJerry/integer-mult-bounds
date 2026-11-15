#!/usr/bin/env python3
"""Exact controls for clipped rectangular filtration; the proof is universal."""
import argparse,hashlib,itertools,json,random
from fractions import Fraction as F
from pathlib import Path

def rank(M,p):
 A=[[x%p for x in row]for row in M];n=len(A);cols=len(A[0])if A else 0;r=0
 for c in range(cols):
  j=next((i for i in range(r,n)if A[i][c]),None)
  if j is None:continue
  A[r],A[j]=A[j],A[r];z=pow(A[r][c],-1,p);A[r]=[x*z%p for x in A[r]]
  for i in range(r+1,n):
   q=A[i][c]
   if q:A[i]=[(x-q*y)%p for x,y in zip(A[i],A[r])]
  r+=1
  if r==n:break
 return r
def product(A,B,p):
 return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)]for row in A]
def residual(D,E,N,p):
 L=product(D,E,p)if E else[[0]*N for _ in range(N)]
 return [[(int(i==j)-L[i][j])%p for j in range(N)]for i in range(N)]
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);p=a.parse_args();rng=random.Random(1511108);cases=[]
 for prime,c,b,V,ratio in itertools.product([2,3],[4,5],[1,2],[1,2],[F(0),F(1),F(2)]):
  n=c*b;N=n*V;m=int(n*ratio)
  for trial in range(3):
   assignments=[rng.randrange(c)for _ in range(m)];mi=[assignments.count(i)for i in range(c)];E=[[0]*N for _ in range(m*V)];D=[[0]*(m*V)for _ in range(N)];supports=[]
   for alpha,own in enumerate(assignments):
    for r in range(V):
     for col in range(own*b*V,(own+1)*b*V):E[alpha*V+r][col]=rng.randrange(prime)
    targets=rng.sample([j for j in range(c)if j!=own],rng.randrange(4));actual=[]
    for target in targets:
     any_nonzero=False
     for row in range(target*b*V,(target+1)*b*V):
      for col in range(alpha*V,(alpha+1)*V):D[row][col]=rng.randrange(prime);any_nonzero|=bool(D[row][col])
     if any_nonzero:actual.append(target)
    supports.append(actual)
   best=0;total=0;orders=0
   for order in itertools.permutations(range(c)):
    at={x:i for i,x in enumerate(order)};good=[0]*c
    for own,s in zip(assignments,supports):good[own]+=all(at[own]<at[j]for j in s)
    z=sum(max(0,b-mi[i]+good[i])for i in range(c));best=max(best,z);total+=z;orders+=1
   r=rank(residual(D,E,N,prime),prime);lower=(119*n+1249)//1250
   assert r>=V*best and best>=lower
   cases.append({'field':prime,'cohorts':c,'banks':b,'width':V,'channels':m,'channel_allocation':mi,'trial':trial,'actual_rank':r,'max_clipped_filtration':best,'mean_clipped_filtration':str(F(total,orders)),'rational_two_channel_bound':lower})
 # Exact integral of2u^3-1 on[4/5,1].
 a=F(4,5);integral=F(-1,2)-(a**4/F(2)-a);assert integral==F(119,1250);assert 111*integral==F(13209,1250)>9
 controls=[]
 for prime in (2,3):
  N=12;I=[[int(i==j)for j in range(N)]for i in range(N)]
  assert rank(residual(I,I,N,prime),prime)==0;controls.append({'field':prime,'changed_premise':'own-cohort support permitted','rank':0})
  D=[[int(i==(j+1)%N)for j in range(N)]for i in range(N)];E=[[int(j==(i+1)%N)for j in range(N)]for i in range(N)]
  assert rank(residual(D,E,N,prime),prime)==0;controls.append({'field':prime,'changed_premise':'source encoder may mix cohorts','rank':0})
  D=[[(int(i==j)-1)%prime for j in range(N)]for i in range(N)];assert rank(residual(D,I,N,prime),prime)==1<2;controls.append({'field':prime,'changed_premise':'eleven foreign targets per channel','rank':1})
  E=[];D=[[]for _ in range(N)]
  for own in range(N):
   targets=[i for i in range(N)if i!=own]
   for k in range(0,len(targets),3):
    group=targets[k:k+3];E.append([int(j==own)for j in range(N)])
    for i in range(N):D[i].append((-int(i in group))%prime)
  assert len(E)==4*N and rank(residual(D,E,N,prime),prime)==1<2;controls.append({'field':prime,'changed_premise':'four channels per input instead of at most two','rank':1,'channels':len(E),'max_foreign_targets':3})
  # The old one-channel bound is attained by a four-cohort all-ones residual.
  N=4;I=[[int(i==j)for j in range(N)]for i in range(N)];D=[[(int(i==j)-1)%prime for j in range(N)]for i in range(N)];assert rank(residual(D,I,N,prime),prime)==1
 p.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_EXACT_CLIPPED_RECTANGULAR_CONTROLS','cases':cases,'case_count':len(cases),'integral_rational_lower_bound':str(integral),'native_global_floor_per_batch':str(111*integral),'canonical_modes_per_batch':9,'negative_scope_controls':controls,'universal_validity_from_written_proof':True,'no_sharpness_claim_for_two_channel_bound':True,'new_complete_kappa':False};(p.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['cases','negative_scope_controls']}))
if __name__=='__main__':main()
