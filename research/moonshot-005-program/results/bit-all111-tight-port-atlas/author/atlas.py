from collections import defaultdict,Counter
from itertools import combinations,product
import json,sys
from pathlib import Path

def bits(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x-=b

def mask(x):return sum(1<<i for i in x)

def source(path):
 R=list(map(tuple,json.loads(Path(path).read_bytes())['native_roots']));full=set(R)
 for sup in {tuple(i for i,x in enumerate(r) if x) for r in R if sum(x!=0 for x in r)==4}:
  for signs in product([-1,1],repeat=3):
   r=[0]*8
   for i,x in zip(sup,(1,*signs)):r[i]=x
   full.add(tuple(r))
 R+=sorted(full-set(R));assert len(R)==120
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));orth=[mask(k for k in range(120) if dot(j,k)==0) for j in range(120)];non=[mask(k for k in range(120) if abs(dot(j,k))==2) for j in range(120)];ids={r:j for j,r in enumerate(R)}
 A=set()
 for i in range(120):
  for j in bits(non[i]):
   if j<i:continue
   sig=dot(i,j)//2;v=tuple(x-sig*y for x,y in zip(R[i],R[j]));p=1 if next(x for x in v if x)!=-abs(next(x for x in v if x)) else -1;v=tuple(p*x for x in v);k=ids[v];A.add(mask((i,j,k)))
 A=sorted(A);assert len(A)==1120
 D=set()
 for i in range(120):
  for j in bits(orth[i] & ~((1<<(i+1))-1)):
   ij=orth[i]&orth[j]
   for k in bits(ij & ~((1<<(j+1))-1)):
    for l in bits(ij&orth[k]&~((1<<(k+1))-1)):
     plus=non[i]&non[j]&non[k]&non[l]
     if plus.bit_count()==8:D.add(mask((i,j,k,l))|plus)
 D=sorted(D);dual={d:__import__('functools').reduce(int.__and__,[orth[i] for i in bits(d)]) for d in D};assert all(v in dual for v in dual.values())
 inside=defaultdict(list)
 for d in D:
  for a in A:
   if a&d==a:inside[a].append(d)
 return R,orth,A,D,dual,inside

def main():
 R,O,A,D,P,L=source(sys.argv[1]);N=(1<<111)-1;ct=Counter();inter=Counter();hist=Counter();total=0; bad=[]
 for a in A:
  m=(a&N).bit_count()
  if not m:continue
  target=__import__('functools').reduce(int.__and__,[O[x] for x in bits(a)])&N
  sets=[P[d]&N for d in L[a]]
  k=1
  while k<5 and not any(__import__('functools').reduce(int.__or__,b)==target for b in combinations(sets,k)):k+=1
  ct[m,k]+=1;total+=k
  mi=min((x&y).bit_count() for x,y in combinations(sets,2));inter[mi]+=1
  hist[len(sets)]+=1
  if k>m:bad.append((list(bits(a)),target.bit_count(),m,k))
 print(len(R),len(D),hist,ct,inter,'sum',total,'excess vs 3552',total-3552,'bad groups',len(bad),bad[:6]);
if __name__=='__main__':main()
