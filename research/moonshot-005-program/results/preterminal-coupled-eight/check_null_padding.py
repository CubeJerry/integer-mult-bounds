#!/usr/bin/env python3
"""Exact corroboration of the padded adjoint identity and source column gate."""
import argparse, gzip, hashlib, json, random
from fractions import Fraction as F
from pathlib import Path

def need(q,s):
 if not q:raise ValueError(s)
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum((x*y for x,y in zip(r,c)),F(0)) for c in zip(*B)] for r in A]
def rank(A):
 B=[r[:] for r in A];k=0
 if not B:return 0
 for j in range(len(B[0])):
  p=next((i for i in range(k,len(B)) if B[i][j]),None)
  if p is None:continue
  B[k],B[p]=B[p],B[k];d=B[k][j];B[k]=[x/d for x in B[k]]
  for i in range(len(B)):
   if i!=k:
    q=B[i][j];B[i]=[x-q*y for x,y in zip(B[i],B[k])]
  k+=1
  if k==len(B):break
 return k
def inv(A):
 n=len(A);B=[r[:]+e for r,e in zip(A,eye(n))]
 for j in range(n):
  p=next((i for i in range(j,n) if B[i][j]),None);need(p is not None,'nonsingular')
  B[j],B[p]=B[p],B[j];d=B[j][j];B[j]=[x/d for x in B[j]]
  for i in range(n):
   if i!=j:
    q=B[i][j];B[i]=[x-q*y for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B]
def sub(A,B):return [[x-y for x,y in zip(r,s)] for r,s in zip(A,B)]
def main(a):
 rng=random.Random(91009);checks=[]
 for p in range(2,9):
  for u in range(1,p):
   h=p-u
   for rep in range(3):
    M=eye(p)
    for z in range(4*p):
     i,j=rng.sample(range(p),2);q=F(rng.choice([-2,-1,1,2]));M[i]=[x+q*y for x,y in zip(M[i],M[j])]
    N=inv(M);m=min(p,rep+1);I=rng.sample(range(p),m);E=[eye(p)[i] for i in I];A=mm(E,M);J=[[F(i==j+u) for j in range(h)] for i in range(p)]
    # Basis columns correspond to hosted dual originals followed by receiver d.
    Z=[r+[-x for x in s] for r,s in zip(mm(tr(N),J),tr(E))]
    decoded=mm(tr(M),Z);want=[r+[-x for x in s] for r,s in zip(J,tr(A))]
    need(decoded==want,'padded transpose identity')
    rr=rank([r[:u] for r in A]);need(rank(Z)==h+rr,'sharp complete-bank rank')
    need(mm(N,M)==eye(p),'primal inverse')
    checks.append({'p':p,'u':u,'m':m,'extra_full_bank_rank':rr})
 # A fixed genuinely nonorthogonal factor detects wrong transpose handling.
 M=[[F(1),F(1)],[F(0),F(1)]];J=[[F(0)],[F(1)]]
 need(mm(tr(M),mm(M,J))!=J,'wrong primal-as-dual encoder is rejected')
 need(rank([[F(0),F(-1)],[F(1),F(0)]])==2,'one hosted field cannot retain rank-two complete bank')
 src=a.repo/'research/moonshot-005-program/results/cohort-reconstruction/eight/WORD.json.gz';b=src.read_bytes();need(hashlib.sha256(b).hexdigest()=='9170345cd487cb996a3a793ade61072bbd169b69a9116e5216b52b05259b6754','frozen cohort pin');w=json.loads(gzip.decompress(b));U={17,19,30,38,40,47,52,60};groups=[]
 for g in w['cohort_collection']['groups']:
  us=[d for d in g['donors'] if d in U]
  if us:
   A=[]
   for y in g['receivers']:
    weights={int(d):F(v) for d,v in w['corrections'][str(y)]};A.append([weights.get(d,F(0)) for d in us])
   r=rank(A);need(r==len(us),'source coupled columns independent')
   groups.append({'chart':g['chart'],'coupled_donors':us,'receivers':g['receivers'],'matrix':[[str(x) for x in row] for row in A],'rank':r})
 need(sum(g['rank'] for g in groups)==8 and len(groups)==6,'eight source dual dimensions in six groups')
 result={'status':'PASS_PADDED_ADJOINT_AND_SOURCE_COLUMN_CAPACITY','universal_proof':'NULL-PADDED-ADJOINT.md','finite_rational_cases':len(checks),'cases':checks,'source_cohort_word_sha256':hashlib.sha256(b).hexdigest(),'source_coupled_groups':groups,'negative_controls':['wrong primal-as-dual encoder differs','rank-two logical bank cannot fit one hosted field'],'scope':'Finite corroboration and exact source application; universal theorem follows from written matrix proof. No global source scheduler or new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'NULL-PADDING-CHECK.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],len(checks),'cases')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
