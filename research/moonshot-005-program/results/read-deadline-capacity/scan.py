"""Source-calendar modular lower bounds with common state decoded only on reads."""
import argparse,gzip,hashlib,json,math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
P=1000003
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,s):
 if not b:raise ValueError(s)
def add(a,b,c):
 for j,x in b.items():
  z=(a.get(j,0)+c*x)%P
  if z:a[j]=z
  else:a.pop(j,None)
def insert(row,b):
 a=row.copy()
 while a:
  j=max(a)
  if j not in b:
   u=pow(a[j],-1,P);b[j]={k:x*u%P for k,x in a.items()};return 1
  add(a,b[j],-a[j])
 return 0
def coeff(x):
 f=Fraction(x);need(f.denominator%P!=0,'source denominator invertible');return f.numerator*pow(f.denominator,-1,P)%P
def canon(vs):
 b={}
 for x in vs:
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 for j in sorted(b):
  for k in b:
   if k>j and (b[k]>>j)&1:b[k]^=b[j]
 return tuple(b[j] for j in sorted(b))
def calculate(w,common_mode):
 need(common_mode in ('all_live','read_deadlines','no_common_observations'),'common contract')
 n=w['public'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);N=n+w['owned_fields'];rows=[[{r:1} if r<n else {} for r in range(N)],[{r:1} if r in M else {} for r in range(N)]];aliases={};keys=[aliases.setdefault(canon(f),i) for i,f in enumerate(w['frames'])];spaces=[set([0]) for f in w['frames']]
 for i,f in enumerate(w['frames']):
  for v in f:spaces[i]|={x^v for x in tuple(spaces[i])}
  need(len(spaces[i])==2**len(f),'frame basis independence')
 need(len(aliases)==1094,'canonical chart census')
 frame=w['initial'][:]+[None]*w['owned_fields'];modes=('main_departure_and_endpoint','endpoint_only');cb=defaultdict(dict);db={m:defaultdict(dict) for m in modes};net={m:{k:defaultdict(int) for k in (1,2)} for m in modes};peak={m:{k:defaultdict(int) for k in (1,2)} for m in modes};at={m:{k:{} for k in (1,2)} for m in modes};records=[];initial=defaultdict(int);common_known=[True]*N
 for r in range(n):
  f=keys[frame[r]];initial[f]+=insert(rows[0][r],cb[f])+insert(rows[1][r],db[modes[0]][f]);insert(rows[1][r],db[modes[1]][f])
 need(sum(initial.values())==1880,'initial exact unit ranks')
 def ask(mode,kind,r,i,phase):
  if kind==0 and common_known[r]:return
  f=keys[frame[r]];fresh=insert(rows[kind][r],cb[f] if kind==0 else db[mode][f])
  if kind==0:common_known[r]=True
  if not fresh:return
  affected=modes if kind==0 else (mode,);records.append([i,phase,r,f,kind,mode if kind else 'both'])
  for m in affected:
   for k in (1,2):
    net[m][k][f]+=1
    if net[m][k][f]>peak[m][k][f]:peak[m][k][f]=net[m][k][f];at[m][k][f]=[i,phase,r,kind]
 def fund(r,i,dst):
  f=keys[dst];kind='main' if r in M else 'helper' if r<n else 'owned'
  for m in modes:
   for k in (1,2):net[m][k][f]-=2 if kind=='main' else k if kind=='owned' else 1
 for i,e in enumerate(w['program']):
  op,r=e[:2]
  if op in ('INIT','CLEAR'):
   need(r>=n and (frame[r] is None if op=='INIT' else frame[r]==e[2]),'owned lifetime');frame[r]=e[2] if op=='INIT' else None;rows[0][r]={};rows[1][r]={};common_known[r]=True
  elif op=='MOVE':
   need(frame[r]==e[2] and type(e[4]) is bool and e[4]==(r>=n),'MOVE source/type')
   a,b=spaces[e[2]],spaces[e[3]];need(a<b if r<n else a<b or b<a,'nested positive-rank MOVE')
   if r in M:ask(modes[0],1,r,i,'before-departure')
   fund(r,i,e[3]);frame[r]=e[3];common_known[r]=False
   if common_mode=='all_live':ask(None,0,r,i,'after-arrival')
  elif op in ('ADD','COPY'):
   s=e[2];need(r!=s and frame[r]==frame[s]==e[4],'cochart scalar');c=coeff(e[3]);need(c!=0,'nonzero scalar')
   if common_mode=='read_deadlines':
    ask(None,0,r,i,'before-target-read');ask(None,0,s,i,'before-source-read')
   for j in (0,1):
    if op=='COPY':need(not rows[j][r],'COPYzero')
    add(rows[j][r],rows[j][s],c)
  elif op=='SCALE':
   c=coeff(e[2]);need(frame[r]==e[3] and c!=0,'SCALE')
   if common_mode=='read_deadlines':ask(None,0,r,i,'before-scale-read')
   for j in (0,1):rows[j][r]={k:x*c%P for k,x in rows[j][r].items()}
  else:raise ValueError('unknown opcode')
 if common_mode!='no_common_observations':
  for r in range(n):ask(None,0,r,len(w['program']),'common-endpoint')
 for r in sorted(M):
  for m in modes:ask(m,1,r,len(w['program']),'difference-endpoint')
 floors={m:{str(k):sum(peak[m][k].values()) for k in (1,2)} for m in modes};charts={m:{str(k):{str(f):{'floor':v,'first_maximizer':at[m][k][f]} for f,v in sorted(peak[m][k].items()) if v} for k in (1,2)} for m in modes}
 return {'common_mode':common_mode,'extra_arrival_floors':floors,'by_chart':charts,'records':records,'record_count':len(records),'initial_rank':sum(initial.values())}
def run(source):
 need(all(P%d for d in range(2,math.isqrt(P)+1)),'prime');raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source hash');w=json.loads(gzip.decompress(raw));cases={c:calculate(w,c) for c in ('all_live','read_deadlines','no_common_observations')};need(cases['all_live']['extra_arrival_floors']=={'main_departure_and_endpoint':{'1':106,'2':106},'endpoint_only':{'1':0,'2':0}},'inherited calendar control');need(all(v==0 for d in cases['no_common_observations']['extra_arrival_floors'].values() for v in d.values()),'no-common negative control');need([28048,'after-arrival',449,594,0,'both'] in cases['all_live']['records'] and [30837,'before-target-read',449,594,0,'both'] in cases['read_deadlines']['records'],'actual quiet-loan observation delay');return {'status':'COMPUTED_MODULAR_RIGOROUS_LOWER_BOUND','source_sha256':PIN,'prime':P,'source_events':len(w['program']),'cases':cases,'negative_controls':['Inherited all-live106/0 reproduced','Dropping common observations gives zero','Helper449 actual common demand delayed from28048 to30837'], 'scope':'Common observations only at actual scalar reads and public endpoints; delta observations at main departures plus endpoints, or endpoints only. Fixed funded calendar grants arbitrary payload acquisition. A zero lower bound proves no feasibility.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source);a.output.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':r['status'],'floors':{c:x['extra_arrival_floors'] for c,x in r['cases'].items()},'records':{c:x['record_count'] for c,x in r['cases'].items()}},indent=2))
