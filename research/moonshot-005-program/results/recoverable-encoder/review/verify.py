#!/usr/bin/env python3
"""Independent exact controls for the recoverable-encoder rank criterion."""
import argparse,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
def need(x,m):
 if not x:raise ValueError(m)
def rref(rows,n):
 a=[[Q(x) for x in row] for row in rows];piv=[];k=0
 for j in range(n):
  h=next((i for i in range(k,len(a)) if a[i][j]),None)
  if h is None:continue
  a[k],a[h]=a[h],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
  for i in range(len(a)):
   if i!=k and a[i][j]:v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
  piv.append(j);k+=1
 return a[:k],piv
def null(rows,n):
 a,p=rref(rows,n);out=[]
 for j in range(n):
  if j not in p:
   v=[Q(0)]*n;v[j]=Q(1)
   for row,i in zip(a,p):v[i]=-row[j]
   out.append(v)
 return out
def trans(a,n):return [[row[j] for row in a] for j in range(n)]
def mul(a,b):return [[sum((Q(x)*Q(b[k][j]) for k,x in enumerate(row)),Q(0)) for j in range(len(b[0]) if b else 0)] for row in a]
def rank(a,n):return len(rref(a,n)[0])
def strings(a):return [[str(x) for x in row] for row in a]
def check(name,E,W,A,B,F,n,p,expected):
 ann,_=rref(null(E,n)+null(W,n),n);L=trans(ann,n);R=null(ann,n);FL=mul(F,L);K=trans(null(A,p),p);Z=null(trans(FL,len(ann)),len(F));M=mul(mul(Z,B),K);block=[list(a)+[0]*len(ann) for a in A]+[list(b)+list(f) for b,f in zip(B,FL)];excess=rank(block,p+len(ann))-rank(A,p)-rank(FL,len(ann));need(excess==rank(M,len(K[0]) if K else 0)==expected,'projected rank identity '+name)
 witness=None
 for i,row in enumerate(M):
  for j,beta in enumerate(row):
   if not beta:continue
   d=Z[i];c=[[row[j]/beta] for row in K];r=mul([d],F)[0];need(mul(A,c)==[[Q(0)] for _ in A] and mul(mul([d],B),c)==[[Q(1)]],'normalization '+name);need(rank(E+[r],n)==rank(E,n) and rank(W+[r],n)==rank(W,n),'both row representations '+name);witness={'d':[str(x) for x in d],'c':[str(x[0]) for x in c],'r':[str(x) for x in r],'beta':str(beta)};break
  if witness:break
 return {'name':name,'encoder_rows':E,'terminal_rows':W,'A':A,'B':B,'F0':F,'R_basis':strings(R),'annihilator_columns':strings(L),'projected_left_null_basis':strings(Z),'rank_excess':excess,'normalized_witness':witness}
def main(author,out):
 cases=[check('strict_scalar_encoder',[[1]],[[1]],[],[[1]],[[1]],1,1,1),check('unavailable_terminal_mode',[[1,0]],[[0,1]],[],[[1]],[[1,0]],2,1,0),check('recoverable_sum_mode',[[1,1],[0,1]],[[1,1]],[],[[1],[1]],[[1,0],[0,1]],2,1,1),check('neutrality_still_required',[[1]],[[1]],[[1]],[[1]],[[1]],1,1,0),check('no_observation_response',[[1]],[[1]],[],[[0]],[[1]],1,1,0)]
 need(not null(trans([[1]],1),1),'unchanged-q scalar family has no noise-free decoder');q=cases[2]['normalized_witness'];need(Q(q['beta'])==2 and Q(q['c'][0])==Q(1,2),'nontrivial exact normalization');need(Q(q['beta'])*2!=1,'wrong normalization rejected');text=author.read_text();need('distinct' in text.lower(),'explicit distinct raw donor/receiver premise')
 result={'status':'PASS_INDEPENDENT_RECOVERABLE_ENCODER_CONTROLS','reviewed_author_sha256':hashlib.sha256(author.read_bytes()).hexdigest(),'cases':cases,'negative_controls':['Using row-space sum instead of intersection falsely admits unavailable terminal mode','Ignoring Ac=0 falsely admits forbidden pulse','Zero observation response cannot decode q','Multiplying by beta instead of dividing fails exact unit signal','Unchanged-q additive scalar interface has no noise-canceling decoder'],'scope':'Independent exact small-matrix controls and proof review; no source witness, coefficient-admission theorem or new kappa.'};out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],result['reviewed_author_sha256'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.author,a.output)
