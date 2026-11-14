#!/usr/bin/env python3
"""Exact signed fresh-stage kernel transitions and literal endpoint normal forms."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,json,hashlib,argparse
HERE=Path(__file__).resolve().parent
PINS={'ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a','R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c'}
def need(c,m):
 if not c:raise ValueError(m)
def load(name):
 b=(HERE/'source'/name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'pin')
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
def add(a,b,c):
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
  if e[0]=='ADD':rows[e[1]]=add(rows[e[1]],rows[e[2]],F(e[3]))
  else:need(e[0]=='MOVE','source alphabet')
 roles=w['logical_involution']['role_map'];ports=w['logical_involution']['ports'];R={}
 for h in ports:
  y=int(roles['Y'][str(h)]);row=dict(rows[y]);need(row.pop(y)==1,'Y baseline')
  R[h]={j:row[int(roles['X'][str(j)])]for j in ports if int(roles['X'][str(j)])in row}
  need(len(R[h])==4,'four contacts')
  need(all(dot(B[h]['normal'],B[j]['normal'])==0 for j in R[h]),'orthogonal edges')
 def route(s,h,x):
  q=B[h]['normal'];bb=B[h]['orthogonal_complement'];E=[1<<(9+8*(s-1)+k)for k in range(8)]
  v=x&~(511|sum(E))
  if dot(x&511,q):v^=q
  for b,e in zip(bb,E):
   if dot(x&511,b):v^=e
   if x&e:v^=b
  return v
 n=33;body=sum(1<<i for i in range(9,n));Fbody=[(1<<i)if i>=9 else 0 for i in range(n)]
 def matrix(vs):
  out=[]
  for i in range(n):
   z=0
   for v in vs:
    if(v>>i)&1:z^=v
   out.append(z)
  return out
 def mv(K,x):return sum(dot(r,x)<<i for i,r in enumerate(K))
 def outer(q):return[q if(q>>i)&1 else 0 for i in range(n)]
 counts={};signatures={};kernel_controls={}
 def visit(stage,j,vs,pattern,run_count):
  if stage==4:return
  oldK=matrix(vs);e=int(bool(pattern)and pattern[-1]=='+')
  need(mv(oldK,B[j]['normal'])==e*B[j]['normal'],'incoming current-port eigenstate')
  for h in R[j]:
   shifted=[route(stage,h,route(stage,j,v))for v in vs];K=matrix(shifted);qh=B[h]['normal'];qj=B[j]['normal']
   need(mv(K,qh)==qh,'output normal is removable before update')
   v=route(stage,h,qj);need(mv(K,v)==e*v and dot(v,qh)==0,'forward update eigenvalue')
   for sg,append in [('-',qh),('+',v)]:
    p=pattern+sg;runs=run_count+int(sg=='+' and (not pattern or pattern[-1]=='-'))
    new=shifted+[append];KK=matrix(new);rr=rank(KK);want=24-stage+2*runs
    need(rr==want,'signed run rank formula');need(mv(KK,qh)==(sg=='+')*qh,'new current-port state')
    need(all(mv(KK,x)==x for x in KK),'idempotent kernel')
    counts[p]=counts.get(p,0)+1;signatures.setdefault(p,set()).add(rr)
    if p in ['+','+-','+-+']:
     target=[a^b for a,b in zip(Fbody,outer(qh))]if sg=='+'else Fbody
     need(KK==target,'full alternating endpoint kernel')
    if p=='++':kernel_controls[p]=KK!=Fbody
    visit(stage+1,h,new,p,runs)
 for j in ports:visit(1,j,[1<<i for i in range(9,n)],'',0)
 need(kernel_controls.get('++') is True,'equal rank does not identify nonalternating kernel')
 # Literal in-place dyadic scalar recipe for the actual ordinary port matrix R0.
 a=[{ports.index(j):v for j,v in R[h].items()}for h in ports];target=[dict(x)for x in a];elim=[]
 for k in range(len(ports)):
  p=next(i for i in range(k,len(ports))if a[i].get(k,F(0)))
  if p!=k:a[k],a[p]=a[p],a[k];elim.append(['SWAP',k,p])
  c=a[k][k]
  if c!=1:a[k]={j:v/c for j,v in a[k].items()};elim.append(['SCALE',k,str(1/c)])
  for i in range(len(ports)):
   if i!=k and a[i].get(k,F(0)):
    c=-a[i][k];a[i]=add(a[i],a[k],c);elim.append(['ADD',i,k,str(c)])
 need(a==[{i:F(1)}for i in range(len(ports))],'ordinary elimination')
 recipe=[]
 for op in reversed(elim):
  if op[0]=='SWAP':recipe.append(op)
  elif op[0]=='SCALE':recipe.append(['SCALE',op[1],str(1/F(op[2]))])
  else:recipe.append(['ADD',op[1],op[2],str(-F(op[3]))])
 a=[{i:F(1)}for i in range(len(ports))]
 for op in recipe:
  if op[0]=='SWAP':a[op[1]],a[op[2]]=a[op[2]],a[op[1]]
  elif op[0]=='SCALE':a[op[1]]={j:F(op[2])*v for j,v in a[op[1]].items()}
  else:a[op[1]]=add(a[op[1]],a[op[2]],F(op[3]))
 need(a==target,'literal R0 recipe on112 arbitrary inputs')
 scalars=sorted(set(op[-1]for op in recipe if op[0]!='SWAP'))
 need(all((F(x).denominator&(F(x).denominator-1))==0 for x in scalars),'dyadic coefficients')
 def reduce(word):
  st=[]
  for x in word:
   if st and ((st[-1],x)in [('Q','q'),('q','Q')]or(x.startswith('R')and st[-1]==x)):st.pop()
   else:st.append(x)
  return st
 words=[]
 for r in range(1,10):
  w=[]
  for s in range(1,r+1):w=reduce(([f'R{s}','Q']if s%2 else['q',f'R{s}'])+w)
  want=([f'R{s}'for s in range(r,0,-1)]+['Q'])if r%2 else(['q']+[f'R{s}'for s in range(r,0,-1)]+['Q'])
  need(w==want,'exact alternating signed word');words.append({'length':r,'normal_form':w})
 result={'status':'PASS_SIGNED_FRESH_RUNS_AND_EXACT_ALTERNATING_TARGETS','source_pins':PINS,'path_counts_by_chronological_sign':dict(sorted(counts.items())),'path_ranks':{p:sorted(v)for p,v in sorted(signatures.items())},'alternating_kernels':'F+qhqhT for odd prefixes, F for even prefixes','strict_run_formula':'8m-r+2 times number of positive runs','nonalternating_equal_rank_control':kernel_controls,'exact_operator_words':words,'ordinary_R0_recipe':recipe,'ordinary_R0_recipe_census':dict(Counter(op[0]for op in recipe)),'ordinary_R0_scalar_set':scalars,'scope':'Actual signed endpoint classification and exact ordinary target adapters. No chronological caller exposing those endpoints is asserted; no new kappa.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE/'RESULT.json');main(p.parse_args().out)
