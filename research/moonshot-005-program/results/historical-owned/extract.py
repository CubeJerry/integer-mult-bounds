import argparse,gzip,json,hashlib
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
cli=argparse.ArgumentParser();cli.add_argument('--source',type=Path,required=True);cli.add_argument('--output',type=Path,required=True);args=cli.parse_args();raw=args.source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883':raise ValueError('source pin')
w=json.loads(gzip.decompress(raw));M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);n=w['public'];N=n+w['owned_fields'];targets={28141,33554,34467,37597};charts={470,431,394,520};rows=[{r:F(1)} if r in M else {} for r in range(N)];frames=w['initial'][:]+[None]*w['owned_fields'];version=[-1]*N;bases={kind:{f:{} for f in charts} for kind in ('owned','owned_main','all')};observations={};out=[]
def add(a,b,c):
 for k,v in b.items():
  z=a.get(k,F(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def insert(row,b,idx):
 v=row.copy();z={idx:F(1)}
 while v:
  p=min(v)
  if p not in b:
   c=v[p];b[p]=({k:x/c for k,x in v.items()},{k:x/c for k,x in z.items()});return
  a=v[p];u,y=b[p];add(v,u,-a);add(z,y,-a)
def solve(row,b):
 v=row.copy();z={}
 while v:
  p=min(v)
  if p not in b:return None
  a=v[p];u,y=b[p];add(v,u,-a);add(z,y,a)
 return z
def save(r,i,op):
 f=frames[r]
 if f not in charts or not rows[r]:return
 idx=len(observations);kind='owned' if r>=n else 'main' if r in M else 'helper';observations[idx]={'event':i,'phase':'after','role':r,'kind':kind,'chart':f,'value_version_event':version[r],'operation':op,'row':{str(k):str(v) for k,v in sorted(rows[r].items())}}
 for mode in bases:
  if mode=='all' or kind=='owned' or mode=='owned_main' and kind=='main':insert(rows[r],bases[mode][f],idx)
for r in range(n):save(r,-1,'INPUT')
for i,e in enumerate(w['program']):
 op,r=e[:2]
 if i in targets:
  rec={'event':i,'owner':r,'from':e[2],'to':e[3],'rank':abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])),'target_row':{str(k):str(v) for k,v in sorted(rows[r].items())},'witnesses':{}}
  for mode in bases:
   z=solve(rows[r],bases[mode][e[3]]);rec['witnesses'][mode]=None if z is None else [{'coefficient':str(c),'observation':observations[j]} for j,c in sorted(z.items())]
  b=bases['owned_main'][e[3]];res=rows[r].copy()
  for p,(u,y) in sorted(b.items()):
   if p in res:add(res,u,-res[p])
  if res:
   p=min(res);dual={p:F(1)}
   for j,(u,y) in sorted(b.items(),reverse=True):
    v=-sum((v*dual.get(k,F(0)) for k,v in u.items() if k!=j),F(0))
    if v:dual[j]=v
   rec['owned_main_obstruction']={'functional':{str(k):str(v) for k,v in sorted(dual.items())},'target_response':str(sum((v*dual.get(k,F(0)) for k,v in rows[r].items()),F(0)))}
  out.append(rec);print(i,{m:None if z is None else len(z) for m,z in rec['witnesses'].items()},flush=True)
 if op=='MOVE':frames[r]=e[3]
 elif op in ('INIT','CLEAR'):rows[r]={};frames[r]=e[2] if op=='INIT' else None;version[r]=i
 elif op=='SCALE':rows[r]={k:v*F(e[2]) for k,v in rows[r].items()};version[r]=i
 elif op in ('ADD','COPY'):add(rows[r],rows[e[2]],F(e[3]));version[r]=i
 save(r,i,op)
 if i==max(targets):break
args.output.write_text(json.dumps(out,indent=2)+'\n')
