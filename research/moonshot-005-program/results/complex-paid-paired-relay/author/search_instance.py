#!/usr/bin/env python3
from pathlib import Path
import gzip,json,itertools,argparse
from fractions import Fraction as F
parser=argparse.ArgumentParser();parser.add_argument('--seed',type=Path,required=True);parser.add_argument('--native',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
n=json.loads(gzip.decompress(args.native.read_bytes()));w=json.loads(gzip.decompress(args.seed.read_bytes()))
def span(bs):
 s={0}
 for b in bs:s|={v^b for v in tuple(s)}
 return s
def basis(vs):
 d={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j in d:v^=d[j]
   else:
    d[j]=v
    for k in d:
     if k!=j and d[k]>>j&1:d[k]^=v
    break
 return [d[j]for j in sorted(d,reverse=True)]
def extend(bs,ambient):
 s=span(bs); reps=[]
 for v in sorted(ambient):
  if v not in s:
   reps.append(v);s|={x^v for x in tuple(s)}
 return reps
ports=n['live'];host={n['live'][k] for k in n['hosted']['Dports']};vec={h:n['frames'][n['initial'][h]][0] for h in ports}
def root(v):
 one=[i for i in range(9)if v>>i&1]
 if len(one)==3:return [2 if i in one else -1 for i in range(9)]
 zero=[i for i in range(9)if not(v>>i&1)];return [3*(int(i==zero[0])-int(i==zero[1]))for i in range(9)]
r={h:root(vec[h])for h in ports};G={(h,j):F(sum(x*y for x,y in zip(r[h],r[j])),18)for h in ports for j in ports}
best=[];count=0
for group in w['duplex']['groups']:
 c3=group['C_frame'];V=extend(c3,range(512));quot={i:0 for i in range(64)}
 for i in range(64):
  for j,v in enumerate(V):
   if i>>j&1:quot[i]^=v
 ds=set()
 for a,b in itertools.combinations(range(1,64),2):
  if a^b<=b:continue
  key=tuple(sorted(span(c3+[quot[a],quot[b]])));ds.add(key)
 assert len(ds)==651
 for d in sorted(ds):
  targets=[h for h in group['hosted'] if all((vec[h]&z).bit_count()%2==0 for z in d)]
  if not targets:continue
  db=basis(d)
  for normal in range(1,32):
   cc=[]
   for mask in range(32):
    if (normal&mask).bit_count()%2:continue
    v=0
    for j,b in enumerate(db):
     if mask>>j&1:v^=b
    cc.append(v)
   donors=[j for j in sorted(host) if vec[j] in cc]
   if not donors:continue
   parts={}
   for h in targets:
    row=[G[h,j]for j in donors]
    if not all(row):continue
    sig=tuple(x/row[0]for x in row)
    parts.setdefault(sig,[]).append(h)
   for sig,ts in parts.items():
    score=len(ts)*len(donors)
    item={'pairs':score,'donors':donors,'receivers':ts,'C':basis(cc),'D':db,'C3':c3,'C3_chart':group['C'],'P':[str(G[ts[0],j])for j in donors],'Q':[str(G[h,donors[0]]/G[ts[0],donors[0]])for h in ts]}
    if not best or score>best[0]['pairs']:best=[item]
    elif score==best[0]['pairs'] and item not in best:best.append(item)
   count+=1
print(json.dumps({'candidates_tested':count,'max_pairs':best[0]['pairs'],'ties':len(best),'best':best[:8]},indent=2))
args.output.write_text(json.dumps({'candidates_tested':count,'max_pairs':best[0]['pairs'],'ties':len(best),'best':best[:8]},indent=2)+'\n')
