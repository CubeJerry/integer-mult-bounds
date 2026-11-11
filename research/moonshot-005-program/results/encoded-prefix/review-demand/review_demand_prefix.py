#!/usr/bin/env python3
"""Independent typed main-demand prefix and retained-input review."""
import argparse,gzip,hashlib,json,math,tempfile
from fractions import Fraction as Q
from pathlib import Path
from collections import Counter
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(c,msg):
 if not c:raise ValueError(msg)
def axpy(a,b,c):
 for k,v in b.items():
  z=a.get(k,Q(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def span(bits):
 s={0}
 for v in bits:s|={x^v for x in s}
 return frozenset(s)
def primitive(row):
 den=1
 for v in row.values():den=math.lcm(den,v.denominator)
 a={k:int(v*den) for k,v in row.items() if v};g=0
 for v in a.values():g=math.gcd(g,abs(v))
 if not a:return {}
 sign=1 if a[max(a)]>0 else -1
 return {k:v//g*sign for k,v in a.items()}
def rem(row,B):
 a=primitive(row)
 while a:
  p=max(a)
  if p not in B:return a
  x=a[p];b=B[p];y=b[p]
  a=primitive({k:Q(y*a.get(k,0)-x*b.get(k,0)) for k in set(a)|set(b) if y*a.get(k,0)-x*b.get(k,0)})
 return {}
def basis(rows):
 B={}
 for row in rows:
  r=rem(row,B)
  if r:B[max(r)]=r
 return B
def run(source,transcript,receipt=None):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'immutable source');w=json.loads(gzip.decompress(raw))
 payload=gzip.decompress(transcript.read_bytes());t=json.loads(payload);need(t['source_sha256']==PIN,'transcript source pin');need(t['frames']==w['frames'],'exact frames')
 mains=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));M=set(mains);n=w['public'];pub=t['public'];S=w['owned_fields'];need((n,len(M),pub,S)==(1480,400,1880,51),'inventory')
 carrier={int(k):v for k,v in t['carrier_map'].items()};need(carrier=={r:n+i for i,r in enumerate(mains)},'carrier map');inverse={v:r for r,v in carrier.items()}
 def mapped(r):return r if r<n else r+400
 original=set(range(n))|set(range(pub,pub+S));frames=list(map(span,w['frames']));need(t['initial']==w['initial']+[w['initial'][r] for r in mains],'boundary charts')
 N=pub+S+t['new_owned'];state=[{i:Q(1)} if i<pub else {} for i in range(N)];cur=t['initial']+[None]*(S+t['new_owned']);active=set(range(pub));si=0;peak=life=0;counts=Counter();extra=Counter();funded_main=0
 def difference(row):
  out={inverse[k]:v for k,v in row.items() if k in inverse};check={}
  for r,v in out.items():check[carrier[r]]=v;check[r]=-v
  need(check==row,'pure main-difference observation');return out
 for pi,e in enumerate(t['program']):
  op,r=e[:2];need(0<=r<N,'owner range');counts[op]+=1
  if r in original:
   need(si<t['source_cut'],'unexpected first-copy mutation');oe=w['program'][si];expected=list(oe);expected[1]=mapped(oe[1])
   if op in ('ADD','COPY'):expected[2]=mapped(oe[2])
   need(e==expected,f'first-copy source order {si}');si+=1
  if op=='INIT':
   need(r>=pub and r not in active and cur[r] is None,'owned INIT');active.add(r);cur[r]=e[2];state[r]={};life+=1
  elif op=='CLEAR':
   need(r>=pub and r in active and cur[r]==e[2],'owned CLEAR')
   if r>=pub+S:raise ValueError('demand-prefix retirement not part of this checked contract')
   active.remove(r);cur[r]=None;state[r]={}
  elif op=='MOVE':
   need(r in active and cur[r]==e[2],'MOVE chart');need(type(e[4]) is bool and e[4]==(r>=pub),'literal MOVE ownership flag');fa,fb=frames[e[2]],frames[e[3]];need(fa<fb if r<pub else fa<fb or fb<fa,'nested MOVE')
   if r in inverse:
    vr=inverse[r];oe=w['program'][si];need(oe[:4]==['MOVE',vr,e[2],e[3]],'funded literal main itinerary');want={j:v for j,v in state[vr].items() if j in M};need(difference(state[r])==want,'literal main departure difference');funded_main+=1
   rank=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));need(rank>0,'positive rank');cur[r]=e[3]
   if r>=pub+S:extra[rank]+=1
  elif op in ('ADD','COPY'):
   s=e[2];need(r in active and s in active and r!=s and cur[r]==cur[s]==e[4],'live cochart ADD');c=Q(e[3]);need(c!=0,'nonzero ADD')
   if op=='COPY':need(not state[r],'all-input COPYzero')
   axpy(state[r],state[s],c)
  elif op=='SCALE':
   need(r in active and cur[r]==e[3],'live SCALE');c=Q(e[2]);need(c!=0,'nonzero SCALE');state[r]={k:v*c for k,v in state[r].items()}
  else:raise ValueError(op)
  peak=max(peak,sum(q>=pub for q in active))
 need(si==t['source_cut'],'source cut')
 reference=[{r:Q(1)} if r<n else {} for r in range(n+S)];rchart=w['initial']+[None]*S
 for e in w['program'][:t['source_cut']]:
  op,r=e[:2]
  if op in ('INIT','CLEAR'):reference[r]={};rchart[r]=e[2] if op=='INIT' else None
  elif op=='MOVE':rchart[r]=e[3]
  elif op=='SCALE':reference[r]={j:Q(e[2])*v for j,v in reference[r].items()}
  else:axpy(reference[r],reference[e[2]],Q(e[3]))
 for r in range(n+S):need(cur[mapped(r)]==rchart[r] and state[mapped(r)]==reference[r],'all-input first-copy equality')
 need(t['current_firstcopy_charts']==rchart,'declared charts')
 for rec in t.get('observations',[]):
  q=rec['owner'];need(q in active and cur[q]==rec['frame'],'current observation');need(difference(state[q])=={int(j):Q(v) for j,v in rec['row']},'formal observation equality')
 decoded=set()
 for d in t['current_decoders']:
  r=d['owner'];f=d['frame'];need(r not in decoded and rchart[r]==f,'virtual decoder role');decoded.add(r);got={}
  for q,c in d['expression']:
   need(q in active and cur[q]==f and (q in inverse or q>=pub+S),'current cochart decoder input');axpy(got,state[q],Q(c))
  want={}
  for j,v in reference[r].items():
   if j in M:want[carrier[j]]=v;want[j]=-v
  need(got==want,'all1880-input difference decoder')
 need(decoded==M,'all400 current main virtual roles')
 retained=set()
 for d in t['retained_input_differences']:
  r=d['main_input'];q=d['holder'];f=d['frame'];need(r in M and r not in retained,'unique retained main input');retained.add(r)
  need(q in active and (q in inverse or q>=pub+S) and cur[q]==f==w['initial'][r],'retained input current initial chart')
  need(difference(state[q])=={r:Q(1)},'exact retained original input difference')
 need(retained==M,'all400 independent input differences retained')
 if receipt:
  a=json.loads(receipt.read_text());need(a['transcript_payload_sha256']==hashlib.sha256(payload).hexdigest(),'author payload digest');need(a['physical_prefix_counts']==dict(counts),'author counts');need(a['live_owned']==peak,'author combined peak');need(a['extra_paid_histogram']=={str(r):v for r,v in sorted(extra.items())},'author extra invoice')
 ghost=332;gf=rchart[ghost];target={j:v for j,v in reference[ghost].items() if j in M};need(target=={33:Q(-1,2),109:Q(1,2),108:Q(1,2)},'exact ghost row')
 qrows=[difference(state[q]) for q in active if (q in inverse or q>=pub+S) and cur[q]==gf];need(bool(rem(target,basis(qrows))),'ghost absent from current difference span');need(not rem(target,basis(qrows+[target])),'ghost span positive control')
 fulltarget={}
 for j,v in target.items():fulltarget[carrier[j]]=v;fulltarget[j]=-v
 need(bool(rem(fulltarget,basis(state[q] for q in active if cur[q]==gf))),'ghost absent even from all current physical destination rows')
 ghost_record={'role':ghost,'chart':gf,'difference':[[j,str(v)] for j,v in sorted(target.items())],'outside_difference_span':True,'outside_all_physical_destination_rows':True}
 return {'status':'PASS_INDEPENDENT_TYPED_MAIN_DEMAND_AND_RETAINED_INPUT_PREFIX','source_sha256':PIN,'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'cut_before_event':si,'physical_events':len(t['program']),'formal_entering_inputs':pub,'first_copy_roles_checked':n+S,'virtual_decoders_checked':len(decoded),'retained_input_differences_checked':len(retained),'physical_counts':dict(counts),'extra_paid_histogram':dict(sorted(extra.items())),'combined_peak_owned':peak,'owned_lifetimes':life,'funded_main_departure_payloads_checked':funded_main,'deferred_helper_witness':ghost_record,'typed_ownership_and_chart_guards':True,'scope':'Exact finite typed demand-prefix. All first-copy roles, 400 current main values and 400 raw input differences checked; no current second-helper decoder or complete supplier/kappa.'}
def controls(source,transcript):
 original=json.loads(gzip.decompress(transcript.read_bytes()));found=[]
 for name in ('wrong_owned_flag','wrong_main_departure_payload','false_input_retention'):
  z=json.loads(json.dumps(original))
  if name=='wrong_owned_flag':
   e=next(e for e in z['program'] if e[0]=='MOVE' and e[1]>=z['public']+z['source_owned']);e[4]=False
  elif name=='wrong_main_departure_payload':
   q=next(e[1] for e in z['program'] if e[0]=='MOVE' and z['source_public']<=e[1]<z['public'])
   e=next(e for e in z['program'] if e[0]=='ADD' and e[1]==q and e[2]>=z['public']+z['source_owned']);e[3]='1'
  else:z['retained_input_differences'][0]['holder']=z['retained_input_differences'][1]['holder']
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'mutant.json.gz';p.write_bytes(gzip.compress(json.dumps(z).encode(),mtime=0))
   try:run(source,p)
   except ValueError as ex:found.append({'mutation':name,'rejection':str(ex)})
   else:raise ValueError('negative control accepted '+name)
 return found
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--transcript',type=Path,required=True);p.add_argument('--author-receipt',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.transcript,a.author_receipt);r['negative_controls']=controls(a.source,a.transcript);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
