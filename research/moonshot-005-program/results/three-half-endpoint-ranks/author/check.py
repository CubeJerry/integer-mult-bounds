#!/usr/bin/env python3
"""All112 actual R0 paths: fresh inverse-cross products lose one Gaussian rank each."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,json,hashlib,argparse
HERE=Path(__file__).resolve().parent
PINS={'ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a','R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c'}
def need(c,m):
 if not c:raise ValueError(m)
def load(name):
 b=(HERE/'source'/name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'source pin')
 return json.loads(gzip.decompress(b)if name.endswith('.gz')else b)
def dot(x,y):return(x&y).bit_count()%2
def rank(a):
 p={}
 for x in a:
  while x:
   k=x.bit_length()-1
   if k in p:x^=p[k]
   else:p[k]=x;break
 return len(p)
def rowadd(a,b,c):
 z=dict(a)
 for j,v in b.items():
  u=z.get(j,F(0))+c*v
  if u:z[j]=u
  else:z.pop(j,None)
 return z
def main(out):
 rt=load('ROUTES.json');w=load('R0-WORD.json.gz');B={x['port']:x for x in rt['route_records']if x['stage']==1}
 rows=[{j:F(1)}for j in range(w['public'])]
 for e in w['program']:
  if e[0]=='ADD':rows[e[1]]=rowadd(rows[e[1]],rows[e[2]],F(e[3]))
  else:need(e[0]=='MOVE','owner-free source')
 roles=w['logical_involution']['role_map'];ports=w['logical_involution']['ports'];R={}
 for h in ports:
  y=int(roles['Y'][str(h)]);row=dict(rows[y]);need(row.pop(y)==1,'baseline')
  R[h]={j:row[int(roles['X'][str(j)])]for j in ports if int(roles['X'][str(j)])in row}
  need(len(R[h])==4 and all(abs(v)==F(1,2)for v in R[h].values()),'four contacts')
  need(all(dot(B[h]['normal'],B[j]['normal'])==0 for j in R[h]),'actual edge orthogonality')
 def route(s,h,x):
  q=B[h]['normal'];bb=B[h]['orthogonal_complement'];E=[1<<(9+8*(s-1)+k)for k in range(8)]
  v=x&~(511|sum(E))
  if dot(x&511,q):v^=q
  for b,e in zip(bb,E):
   if dot(x&511,b):v^=e
   if x&e:v^=b
  return v
 n=33
 def matrix(vs):
  rows=[]
  for i in range(n):
   c=0
   for v in vs:
    if(v>>i)&1:c^=v
   rows.append(c)
  return rows
 def mv(K,x):return sum(dot(r,x)<<i for i,r in enumerate(K))
 def step(vs,s,h,j):
  new=[route(s,h,route(s,j,v))for v in vs];K=matrix(new);q=B[h]['normal']
  need(dot(q,q)==1 and mv(K,q)==q,'removable unit eigenvector')
  return new+[q]
 start=[1<<i for i in range(9,33)];one=Counter();three=Counter();examples={};allproj=True
 for h in ports:
  for j in R[h]:
   K=matrix(step(start,2,h,j));rk=rank(K);need(rk==23,'single inverse-cross rank')
   one[rk]+=1
  for k in R[h]:
   for j in R[k]:
    for i in R[j]:
     vs=step(step(step(start,1,j,i),2,k,j),3,h,k);K=matrix(vs);rk=rank(K)
     need(rk==21,'three inverse-cross rank')
     need(all(mv(K,c)==c for c in K),'projection remains idempotent')
     three[rk]+=1;examples.setdefault(rk,[h,k,j,i])
 # A fresh-stage hypothesis matters: a repeated identical inverse factor can restore rank.
 h=ports[0];j=next(iter(R[h]));first=step(start,1,h,j)
 repeated=matrix([route(1,j,route(1,h,v))for v in first]+[B[j]['normal']])
 need(rank(repeated)!=22,'repeated-stage control')
 # Turning off a real edge's orthogonality invalidates the removal mechanism.
 h=ports[0];q=B[h]['normal'];new=[route(1,h,route(1,h,v))for v in start]
 need(mv(matrix(new),q)==0,'diagonal edge is not removable')
 result={'status':'PASS_ALL112_FRESH_INVERSE_ENDPOINT_RANKS','source_pins':PINS,'ports':len(ports),'first_output_path_ranks':dict(one),'second_output_path_ranks':dict(three),'examples':examples,'every_triple_kernel_is_projection':allproj,'row_support_bounds':{'first':'4 * 2^(23 V)','second':'64 * 2^(21 V)','both_max_for_V_ge_2':'4 * 2^(23 V)'},'negative_controls':{'repeated_stage_rank':rank(repeated),'nonorthogonal_diagonal_edge_eigenvalue':0},'scope':'Exact individual path ranks and universal union support bounds. Cancellations can only lower support. No claim of exact full summed row support, Gaussian endpoint admission, arbitrary ordinary lower bound or new kappa.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'RESULT.json');main(a.parse_args().out)
