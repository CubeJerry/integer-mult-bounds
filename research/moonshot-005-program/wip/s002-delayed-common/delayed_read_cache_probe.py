from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
from bisect import bisect_right
import gzip,json,hashlib,time
SOURCE=Path('/workspace/scratch/40edaa02ba04/moonshot/research/shared-wire-split-composition/data/final.json.gz');PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';raw=SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('source hash')
w=json.loads(gzip.decompress(raw));P=w['program'];n=w['public'];rows=[{r:Q(1)} if r<n else {} for r in range(n+w['owned_fields'])];cur=w['initial']+[None]*w['owned_fields'];reads=defaultdict(list);clears=defaultdict(list)
for i,e in enumerate(P):
 if e[0] in ('ADD','COPY'):reads[e[2]].append(i)
 if e[0]=='CLEAR':clears[e[1]].append(i)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,Q(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def rem(row,B):
 v=row.copy()
 while v:
  j=min(v)
  if j not in B:return v
  add(v,B[j],-v[j])
 return v
def insert(row,B):
 v=rem(row,B)
 if v:
  j=min(v);c=v[j];B[j]={k:x/c for k,x in v.items()}
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in s}
 return frozenset(s)
classes={};canon={}
for f,vs in enumerate(w['frames']):canon[f]=classes.setdefault(span(vs),f)
bases=defaultdict(dict)
for r in range(n):insert(rows[r],bases[canon[cur[r]]])
active=[];done=[];unused=[];start=time.time()
for k,e in enumerate(P):
 op,r=e[:2];left=[]
 for a in active:
  if a['deadline']==k:
   v=rem(rows[a['owner']],a['basis']);done.append({j:x for j,x in a.items() if j!='basis'}|{'cache_rank':len(a['basis']),'recoverable':not v,'residual_support':len(v),'residual':[[j,str(c)] for j,c in sorted(v.items())]})
  else:left.append(a)
 active=left
 if op=='MOVE':
  f,d=e[2:4]
  if r>=n:
   t=bisect_right(reads[r],k);deadline=reads[r][t] if t<len(reads[r]) else len(P);z=bisect_right(clears[r],k);clear=clears[r][z] if z<len(clears[r]) else len(P)
   if deadline>=clear:unused.append({'move':k,'owner':r,'clear':clear})
   else:
    frame=P[deadline][4];active.append({'move':k,'owner':r,'from':f,'to':d,'deadline':deadline,'read_event':P[deadline],'frame':frame,'basis':dict(bases[canon[frame]])})
  for a in active:
   if r!=a['owner'] and canon[d]==canon[a['frame']]:insert(rows[r],a['basis'])
  insert(rows[r],bases[canon[d]]);cur[r]=d
 elif op in ('ADD','COPY'):add(rows[r],rows[e[2]],Q(e[3]))
 elif op=='SCALE':rows[r]={j:v*Q(e[2]) for j,v in rows[r].items()}
 elif op=='INIT':rows[r]={};cur[r]=e[2]
 elif op=='CLEAR':rows[r]={};cur[r]=None
 else:raise ValueError(op)
out={'source_sha256':PIN,'checked_moves':len(done),'recoverable':sum(a['recoverable'] for a in done),'erased_without_read':unused,'checks':done,'elapsed_seconds':time.time()-start,'scope':'Each single owned-MOVE replacement; grants complete historical common snapshots before loan and all other-holder arrivals until first external source read. Excludes borrowed-holder post-loan rows, permits free equivalent-frame caching. Exact rational span test; no differential side-information granted.'}
Path('/workspace/scratch/40edaa02ba04/adversarial/DELAYED-READ-CACHE-PROBE.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='checks'})
