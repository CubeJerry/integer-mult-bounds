"""Replay every retirement against the actual current virtual-role row spaces."""
from __future__ import annotations
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(p,msg):
 if not p:raise ValueError(msg)
def add(a,b,c):
 for k,x in b.items():
  y=a.get(k,F(0))+c*x
  if y:a[k]=y
  else:a.pop(k,None)
def span(rows):
 piv={}
 for row in rows:
  x=dict(row)
  for p,b in piv.items():
   if x.get(p):add(x,b,-x[p])
  if x:
   p=min(x);c=x[p];piv[p]={j:v/c for j,v in x.items()}
 return piv
def contains(row,basis):
 r=row.copy()
 for p,b in basis.items():
  if r.get(p):add(r,b,-r[p])
 return not r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--transcript',type=Path,default=Path(__file__).with_name('retired-prefix.json.gz'));ap.add_argument('--output',type=Path);a=ap.parse_args()
 source=a.source
 if source is None:
  source=next((base/'research/shared-wire-split-composition/data/final.json.gz' for p in Path(__file__).resolve().parents for base in (p,p/'moonshot') if (base/'research/shared-wire-split-composition/data/final.json.gz').is_file()),None)
 need(source is not None,'source path');raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));payload=gzip.decompress(a.transcript.read_bytes());t=json.loads(payload);n=w['public'];np=t['public'];m={int(k):v for k,v in t['carrier_map'].items()};nr=np+t['source_owned']+t['new_owned'];physical=[{} for _ in range(nr)];pcharts=t['initial']+[None]*(nr-np)
 for main,carrier in m.items():physical[carrier]={main:F(1)}
 virtual=[{i:F(1)} if i in m else {} for i in range(n+w['owned_fields'])];vcharts=w['initial']+[None]*w['owned_fields'];live=set();source_index=0;checks=[]
 for step,e in enumerate(t['program']):
  op,r=e[:2]
  if r<n:
   need(e==w['program'][source_index],'source subsequence');source_index+=1
   if op=='MOVE':vcharts[r]=e[3]
   elif op in ('ADD','COPY'):add(virtual[r],virtual[e[2]],F(e[3]))
   elif op=='SCALE':virtual[r]={j:F(e[2])*v for j,v in virtual[r].items()}
   else:raise ValueError('this prefix has source-owned events')
  if op=='INIT':need(r>=np and r not in live and pcharts[r] is None,'owned INIT');live.add(r);physical[r]={};pcharts[r]=e[2]
  elif op=='MOVE':need(pcharts[r]==e[2] and e[4]==(r>=np),'current move and owner annotation');pcharts[r]=e[3]
  elif op in ('ADD','COPY'):
   need(pcharts[r]==pcharts[e[2]]==e[4],'current scalar');add(physical[r],physical[e[2]],F(e[3]))
  elif op=='SCALE':physical[r]={j:F(e[2])*v for j,v in physical[r].items()}
  elif op=='CLEAR':
   f=e[2];need(r in live and pcharts[r]==f,'owned CLEAR');available=[q for q in list(m.values())+list(live-{r}) if pcharts[q]==f];basis=span(physical[q] for q in available);needed=[i for i,c in enumerate(vcharts) if c==f]
   need(all(contains(virtual[i],basis) for i in needed),'unsafe retirement')
   checks.append({'physical_event':step,'after_source_event':source_index-1,'retired_owner':r,'chart':f,'live_virtual_roles_checked':len(needed),'needed_rank':len(span(virtual[i] for i in needed)),'remaining_observation_rank':len(basis),'payload_zero':not physical[r]})
   live.remove(r);pcharts[r]=None;physical[r]={}
  else:raise ValueError(op)
 need(source_index==t['source_cut'],'complete source prefix')
 # A main-only retirement test would accept the empty main span but lose q.
 need(contains({},span([])) and not contains({0:F(1)},span([])),'all-role negative control')
 result={'status':'PASS_ALL_CURRENT_CHART_RETIREMENTS','source_sha256':PIN,'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'cut':t['source_cut'],'retirements_checked':len(checks),'dirty_retirements':sum(not x['payload_zero'] for x in checks),'checks':checks,'negative_control':'Main-only zero demand does not authorize deleting a nonzero live helper difference.','scope':'Exact rational local retirement invariant; dirty erasure remains inherited owned_erasure premise.'}
 s=json.dumps(result,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
if __name__=='__main__':main()
