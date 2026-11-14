"""Complete orthogonal and mixed support census, independent bitset recursion."""
import gzip,json,math,argparse
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
w=json.loads(gzip.decompress(args.native.read_bytes()));r=[list(map(F,w['frames'][str(w['start'][i])]['B'][0]))for i in range(111)]
D=[[sum(x*y for x,y in zip(a,b))for b in r]for a in r];adj=[sum(1<<j for j in range(111)if D[i][j]==0)for i in range(111)];deg=[x.bit_count()for x in adj];counts=Counter();max_common={5:(-1,[]),6:(-1,[])};orth4=[];orth7=[];full=(1<<111)-1

def members(x):
 while x:
  bit=x&-x;yield bit.bit_length()-1;x^=bit

def walk(chosen,remaining,common):
 n=len(chosen)
 if n:
  counts[n]+=1
  if n in max_common and common.bit_count()>max_common[n][0]:max_common[n]=(common.bit_count(),chosen[:])
  if n==4:
   low=[j for j in members(common)if deg[j]<=56]
   if len(low)>=7:orth4.append(dict(support=chosen[:],eligible_receivers=low,orthogonal_roots=list(members(common))))
  if n==7:
   low=[j for j in members(common)if deg[j]<=59]
   if low:orth7.append(dict(support=chosen[:],eligible_receivers=low))
 if n==8:return
 while remaining:
  bit=remaining&-remaining;i=bit.bit_length()-1;remaining^=bit;walk(chosen+[i],remaining&adj[i],common&adj[i])
walk([],full,full)
print('orth',dict(counts),'max_common',max_common,'critical4/7',len(orth4),len(orth7),flush=True)
mx=(-1,[]);number=0
for i in range(111):
 for j in members(adj[i]&~((1<<(i+1))-1)):
  U=adj[i]&adj[j]
  for a in members(U):
   for b in members(U&~adj[a]&~((1<<(a+1))-1)):
    number+=1;n=(U&adj[a]&adj[b]).bit_count()
    if n>mx[0]:mx=(n,[i,j,a,b])
print('mixed',number,mx,flush=True)
x=dict(orthogonal_counts=dict(counts),max_common=max_common,critical_orthogonal4=orth4,critical_orthogonal7=orth7,mixed_count=number,max_mixed_common=mx)
args.output.write_text(json.dumps(x,indent=2)+'\n')
