#!/usr/bin/env python3
"""Independent simple-rank-path and full-caller review of marked route tariffs."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def measure(*terms):
 out=Counter()
 for z,part in terms:
  for r,v in part.items():out[r]+=z*v
 return {r:v for r,v in out.items()if v}
CACHE={};GRID=1<<192
def power(r,t):
 key=r,t
 if key not in CACHE:
  if t==0:CACHE[key]=(F(1),F(1))
  elif t==1:CACHE[key]=(F(r),F(r))
  else:
   value=r**t.numerator*GRID**t.denominator;lo,hi=0,r*GRID+1
   while hi-lo>1:
    mid=(lo+hi)//2
    if mid**t.denominator<=value:lo=mid
    else:hi=mid
   need(lo**t.denominator<=value<hi**t.denominator,'root bracketing')
   CACHE[key]=(F(lo,GRID),F(lo if lo**t.denominator==value else hi,GRID))
 return CACHE[key]
def interval(p,t):
 lo=hi=F(0)
 for r,v in p.items():
  a,b=power(r,t);lo+=v*(a if v>0 else b);hi+=v*(b if v>0 else a)
 return lo,hi
def path_measure(path):
 counts=Counter();I=0
 for u,v in zip(path,path[1:]):
  counts[abs(u-v)]+=1
  I+=int((v==7 and u<7)or(u==7 and v<7))
 return counts,I
def main(a):
 need(sha(a.caller)=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2','caller pin')
 need(sha(a.pivot)=='8fc6d916178b788c1b21077c0e9e3e81602aaf0789c5fd32f7ce8397128b72ba','pivot word pin')
 native=json.loads(a.caller.read_text());author=json.loads(a.author.read_text())
 N,H,P,T=({int(r):F(v)for r,v in native[k].items()}for k in['native_paid','helper_target','paired_paid','paired_target'])
 correction=measure((F(1,36),T),(-F(1,36),P))
 B=measure((1,N),(-1,H),(1,correction));c={1:1,8:1,7:-1};delta={1:56,6:56,7:-56}
 t=F(199,200)
 # Enumerate every simple rank path, rather than using the author's edge potential.
 path_count=0;minima={};strict=0
 for s in [F(0),F(1,2),t,F(1)]:
  lowest=None;optimal=0
  for k in range(8):
   for inner in itertools.permutations(range(1,8),k):
    path=(8,)+inner+(0,);p,I=path_measure(path)
    gap=measure((1,p),(-I,{1:1}),(-1,{7:1}));bounds=interval(gap,s)
    need(bounds[0]>=0,'simple rank path violates tariff')
    path_count+=1
    if bounds==(0,0):optimal+=1
    else:strict+=1
    if lowest is None or bounds[1]<lowest[1]:lowest=bounds
  minima[str(s)]={'minimum_gap':list(map(str,lowest)),'sharp_simple_paths':optimal}
 # Every removed closed walk has nonnegative adjusted edges, independent of rank length.
 loop_controls=0
 for n in [0,1,2,5,17,64]:
  p,I=path_measure([8,7]+[v for unused in range(n)for v in(6,7)]+[0])
  need(not measure((1,p),(-I,{1:1}),(-1,{7:1})),'sharp repeated route')
  loop_controls+=1
 # Recover mandatory capture stops from the literal word, including read accesses.
 w=json.loads(gzip.decompress(a.pivot.read_bytes()));frames=w['frames'];pending={};routes={i:[]for i in range(111)}
 def dim(c):return frames[str(c)]['dim']
 def finish(i):
  if i in pending:
   b,d=pending.pop(i);routes[i].append((b,d))
 for op in w['program']:
  tag,i=op[:2]
  if tag=='MOVE'and i<111:
   b,d=map(dim,op[2:4])
   if i not in pending:pending[i]=(b,d)
   else:
    u,v=pending[i];need(v==b,'continuous physical identity')
    if(v-u)*(d-b)>0:pending[i]=(u,d)
    else:finish(i);pending[i]=(b,d)
  elif tag!='MOVE':
   if i<111:finish(i)
   if tag=='ADD'and op[2]<111:finish(op[2])
 for i in list(pending):finish(i)
 actual=Counter(tuple(v)for v in routes.values())
 need(actual=={((1,7),(7,8)):56,((1,8),):55},'exact original X capture stops')
 certificates={}
 cases=[('eight_Hub',8,0,28,0,138),('nine_Hub',9,0,21,0,131),('ten_Hub',10,0,14,0,124),('nine_Hub_two_rank3',9,2,15,0,125),('fixed_pivot_nine_Hub_two_rank3',9,2,14,1,124)]
 for name,q,b,z,premium,cap in cases:
  gap=measure((1,B),(-(222+q),{7:1}),(-b,{3:1}),(-F(z,2),c),(-premium,delta))
  v=interval(gap,t);need(v[1]<0,'strict caller exclusion')
  claimed=author['target_certificates'][name]
  need(claimed['maximum_ell']==111+z-1==cap,'integer facet cap')
  need({int(k):F(n)for k,n in claimed['signed_measure'].items()}==gap,'independent caller measure')
  need(F(claimed['gap']['lower_rational'])<=v[0]<=v[1]<=F(claimed['gap']['upper_rational']),'independent tighter enclosure')
  certificates[name]={'cap':cap,'forbidden_integer_Z':z,'gap':list(map(str,v))}
 # Nontrivial scope controls: all three discarded stronger statements are false.
 need(interval(measure((1,B),(-231,{7:1}),(-2,{3:1}),(-14,{1:1})),t)[0]>0,'Z14 remains allowed without fixed capture premium')
 need(interval({7:1,8:-1},t)[1]<0,'false 8^t plus incidence tariff')
 need(interval({7:1,6:-1,1:-1},t)[1]<0,'turning proper-born route cannot receive monotone-bank credit')
 # Explicit 6->7->0 has I=2 and price 1+7^t, less than 6^t+I.
 out={'status':'PASS_INDEPENDENT_MARKED_ROUTE_FACET_TARIFF','caller_sha256':sha(a.caller),'pivot_word_sha256':sha(a.pivot),'author_proof_sha256':sha(a.proof),'grid':'2^-192','all_simple_rank_paths_checked':path_count,'strict_path_controls':strict,'simple_path_results':minima,'sharp_repeated_routes':loop_controls,'mandatory_public_X_capture_stops':56,'certificates':certificates,'negative_controls':['generic_125_not_124_without_capture','8_power_t_plus_I_false','proper_born_turn_not_monotone_bank'],'scope':'Unbounded path theorem checked analytically; finite exhaustive rank-path controls corroborate it. Actual disjoint marked routes and retained complete caller are essential. No supplier or new kappa.','new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:out[k]for k in['status','all_simple_rank_paths_checked','mandatory_public_X_capture_stops']}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ['caller','pivot','author','proof','output']:p.add_argument('--'+key,type=Path,required=True)
 main(p.parse_args())
