"""Independent physical replay path for generated encoded-prefix transcript.

This author check never trusts the compiler's declared row identities.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json,collections,time
from pathlib import Path
from fractions import Fraction as F
SOURCE_SHA='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def source_default():
 for parent in Path(__file__).resolve().parents:
  for base in (parent,parent/'moonshot'):
   candidate=base/'research/shared-wire-split-composition/data/final.json.gz'
   if candidate.is_file():return candidate
 return Path('research/shared-wire-split-composition/data/final.json.gz')

def need(v,msg):
 if not v:raise ValueError(msg)
def axpy(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def replay(program,initial_rows,initial_frames,frames,public):
 rows=[r.copy() for r in initial_rows];cur=list(initial_frames);live=set();peak=0;hist=collections.Counter()
 for k,e in enumerate(program):
  op,a=e[:2]
  if op=='INIT':
   need(a>=public and cur[a] is None,'INIT owner');need(not rows[a],'INIT zero');cur[a]=e[2];rows[a]={};live.add(a);peak=max(peak,len(live))
  elif op=='CLEAR':
   need(a in live and cur[a]==e[2],'CLEAR owner');cur[a]=None;rows[a]={};live.remove(a)
  elif op=='MOVE':
   need(cur[a]==e[2],'MOVE source chart');need(e[4]==(a>=public),'MOVE ownership annotation');aa,bb=frames[e[2]],frames[e[3]];small,large=(aa,bb) if len(aa)<len(bb) else (bb,aa)
   need(len(small)<len(large),'MOVE positive rank')
   # Exact binary span inclusion, no full subspace enumeration.
   piv={}
   for x in large:
    while x:
     p=x.bit_length()-1
     if p not in piv:piv[p]=x;break
     x^=piv[p]
   for x in small:
    while x:
     p=x.bit_length()-1;need(p in piv,'MOVE nested frames');x^=piv[p]
   cur[a]=e[3];hist[str(len(large)-len(small))]+=1
  elif op in ('ADD','COPY'):
   b=e[2];need(a!=b and cur[a] is not None and cur[a]==cur[b]==e[4],'ADD source/destination current cochart')
   if op=='COPY':need(not rows[a],'COPY target zero')
   axpy(rows[a],rows[b],F(e[3]))
  elif op=='SCALE':
   need(cur[a]==e[3] and F(e[2])!=0,'SCALE current chart');rows[a]={j:v*F(e[2]) for j,v in rows[a].items() if v*F(e[2])}
  else:raise ValueError(op)
 return rows,cur,live,peak,dict(hist)

def verify(w,t):
 n=w['public'];np=t['public'];no=t['source_owned']+t['new_owned'];m={int(a):b for a,b in t['carrier_map'].items()};cut=t['source_cut']
 need(n==t['source_public'] and np==n+len(m),'public dimensions')
 init=[{i:F(1)} for i in range(np)]+[{} for _ in range(no)];ifr=t['initial']+[None]*no
 actual,cur,live,peak,hist=replay(t['program'],init,ifr,t['frames'],np)
 iu=[{i:F(1)} for i in range(n)]+[{} for _ in range(w['owned_fields'])]
 iv=[{m[i] if i in m else i:F(1)} for i in range(n)]+[{} for _ in range(w['owned_fields'])]
 vu,cu,_,_,_=replay(w['program'][:cut],iu,w['initial']+[None]*w['owned_fields'],w['frames'],n)
 vv,cv,_,_,_=replay(w['program'][:cut],iv,w['initial']+[None]*w['owned_fields'],w['frames'],n)
 def actual_owner(a):return a if a<n else a+len(m)
 need(cu==cv==t['current_firstcopy_charts'],'firstcopy/current chart certificate')
 need(all(actual[actual_owner(a)]==vu[a] for a in range(len(vu))),'firstcopy all-input rows')
 need(len(t['current_decoders'])==sum(x is not None for x in cu),'complete decoder coverage')
 seen=set(); terms=0
 for d in t['current_decoders']:
  a=d['owner'];need(a not in seen,'duplicate decoder');seen.add(a);need(d['frame']==cu[a],'decoder virtual chart');r=actual[actual_owner(a)].copy()
  for q,c in d['expression']:
   need(cur[q]==d['frame'],'decoder CURRENT cochart');axpy(r,actual[q],F(c));terms+=1
  need(r==vv[a],f'exact secondcopy all-input row {a}')
 need(seen=={a for a,f in enumerate(cu) if f is not None},'all current roles decoded')
 for o in t['observations']:
  row={}
  for i,c in o['row']:axpy(row,{m[i]:F(1),i:F(-1)},F(c))
  need(actual[o['owner']]==row and cur[o['owner']]==o['frame'],'actual observation row/frame')
 return {'actual_owned_peak':peak,'live_owned_at_cut':len(live),'all_input_rows':np,'decoded_virtual_roles':len(seen),'decoder_terms':terms,'physical_paid_histogram':hist,'physical_events':len(t['program'])}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=source_default());ap.add_argument('--transcript',type=Path,default=Path(__file__).with_name('prefix.json.gz'));ap.add_argument('--output',type=Path);a=ap.parse_args();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'source SHA256');w=json.loads(gzip.decompress(raw));payload=gzip.decompress(a.transcript.read_bytes());t=json.loads(payload);need(t['source_sha256']==SOURCE_SHA,'transcript source pin');st=time.time();result=verify(w,t)
 controls=[]
 # Each altered transcript is independently run and must fail.
 for label,mutate in [
 ('wrong_first_delivery_sign',lambda p: next(e for e in p['program'] if e[0]=='ADD' and e[1]==1931).__setitem__(3,'1/2')),
 ('wrong_owned_MOVE_flag',lambda p: next(e for e in p['program'] if e[0]=='MOVE' and e[1]==1931).__setitem__(4,False)),
 ('omitted_first_delivery_MOVE',lambda p: p['program'].remove(next(e for e in p['program'] if e[0]=='MOVE' and e[1]==1931))),
 ('invalid_main_snapshot_alias',lambda p: next(e for e in p['program'] if e[0]=='INIT' and e[1]==1936).__setitem__(1,1580)),
 ]:
  z=json.loads(payload);mutate(z)
  try:verify(w,z)
  except ValueError as ex:controls.append({'mutation':label,'rejection':str(ex)})
  else:raise ValueError('negative control survived '+label)
 result.update(status='PASS_EXACT_PHYSICAL_ENCODED_PREFIX',source_sha256=SOURCE_SHA,transcript_payload_sha256=hashlib.sha256(payload).hexdigest(),cut=t['source_cut'],negative_controls=controls,elapsed_seconds=time.time()-st,scope='Exact finite normalized all-input prefix. No completed H4 native, compiler, physical tariff or kappa.')
 s=json.dumps(result,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
if __name__=='__main__':main()
