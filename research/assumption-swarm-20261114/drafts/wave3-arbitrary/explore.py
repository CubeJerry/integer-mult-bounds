from itertools import permutations
import json,random,time
P=1000003
Q=pow(2,-1,P)
def rank(a,p=P):
 a=[r[:] for r in a];m=len(a);n=len(a[0]);r=0
 for j in range(n):
  k=next((k for k in range(r,m) if a[k][j]%p),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];iv=pow(a[r][j],-1,p)
  a[r]=[x*iv%p for x in a[r]]
  for k in range(r+1,m):
   if a[k][j]%p:
    v=a[k][j];a[k]=[(x-v*y)%p for x,y in zip(a[k],a[r])]
  r+=1
  if r==m:break
 return r
def displacement(order,d,q=Q):
 n=len(order);powers=[pow(q,i,P) for i in range(d+1)]
 h=[[powers[(x^y).bit_count()] for y in order] for x in order]
 return [[(h[i][j]-(h[i-1][j-1] if i*j else 0))%P for j in range(n)] for i in range(n)]
def calc(o,d):return rank(displacement(o,d))
def main():
 result={'field':P,'q_mod':Q,'seed':48261,'gray':[]}
 for d in range(1,8):
  n=1<<d;o=[i^(i>>1) for i in range(n)]
  result['gray'].append({'d':d,'rank':calc(o,d)})
 counts={};best=None
 for tail in permutations(range(1,8)):
  o=(0,)+tail;r=calc(o,3);counts[r]=counts.get(r,0)+1
  if best is None or r<best[0]:best=[r,o]
 result['d3_all_fix0']={'counts':counts,'best':best,'coverage':5040}
 rng=random.Random(48261);counts={};best=None
 for trial in range(20000):
  o=list(range(1,16));rng.shuffle(o);o=[0]+o;r=calc(o,4);counts[r]=counts.get(r,0)+1
  if best is None or r<best[0]:best=[r,o]
 result['d4_random']={'counts':counts,'best':best,'coverage':20000}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
