"""Exact physical replay of the explicitly weaker main-demand prefix contract."""
from __future__ import annotations
import argparse,gzip,hashlib,json,time
from fractions import Fraction as F
from pathlib import Path
from demand_graph import load_source,source_default,need,PIN,add
from verify_prefix import replay

def basis(rows):
 b={}
 for v in rows:
  r=v.copy()
  for p,w in b.items():
   if r.get(p):add(r,w,-r[p])
  if r:
   p=min(r);c=r[p];b[p]={j:v/c for j,v in r.items()}
 return b

def contained(row,b):
 r=row.copy()
 for p,w in b.items():
  if r.get(p):add(r,w,-r[p])
 return not r

def verify(w,t):
 n=w['public'];np=t['public'];no=t['source_owned']+t['new_owned'];m={int(a):b for a,b in t['carrier_map'].items()};cut=t['source_cut'];need(t['schema']=='moonshot-main-demand-prefix-v1' and t['source_sha256']==PIN,'demand schema/source')
 init=[{i:F(1)} for i in range(np)]+[{} for _ in range(no)];actual,cur,live,peak,hist=replay(t['program'],init,t['initial']+[None]*no,t['frames'],np)
 iu=[{i:F(1)} for i in range(n)]+[{} for _ in range(w['owned_fields'])];iv=[{m[i] if i in m else i:F(1)} for i in range(n)]+[{} for _ in range(w['owned_fields'])]
 u,uc,_,_,_=replay(w['program'][:cut],iu,w['initial']+[None]*w['owned_fields'],w['frames'],n);v,vc,_,_,_=replay(w['program'][:cut],iv,w['initial']+[None]*w['owned_fields'],w['frames'],n)
 def actual_owner(i):return i if i<n else i+len(m)
 need(uc==vc==t['current_firstcopy_charts'],'current source charts');need(all(actual[actual_owner(i)]==u[i] for i in range(len(u)) if uc[i] is not None),'all first-copy rows')
 seen=set()
 for d in t['current_decoders']:
  r=d['owner'];need(r in m and r not in seen and d['frame']==uc[r],'current main decoder');seen.add(r);row=actual[r].copy()
  for q,c in d['expression']:
   need(cur[q]==d['frame'],'current cochart demand observation');add(row,actual[q],F(c))
  need(row==v[r],f'exact current second main row {r}')
 need(seen==set(m),'all 400 current mains')
 inputs=set()
 for d in t['retained_input_differences']:
  r=d['main_input'];q=d['holder'];need(r in m and r not in inputs,'input-difference coverage');inputs.add(r);need(actual[q]=={m[r]:F(1),r:F(-1)},f'original input difference retained {r}');need(cur[q]==d['frame']==w['initial'][r],'retained input current chart')
 need(inputs==set(m),'all400 original input differences retained')
 # Explicitly demonstrate that this is not the old all-live-helper interface.
 target=332;wanted=v[target].copy();add(wanted,u[target],-1)
 candidates=[actual[q] for q in list(m.values())+list(live) if cur[q]==uc[target]]
 missing=not contained(wanted,basis(candidates))
 need(missing,'source-specific distinction from all-live interface')
 return {'all_input_dimensions':np,'first_copy_live_roles':sum(f is not None for f in uc),'current_main_decoders':len(seen),'retained_original_differences':len(inputs),'live_owned':len(live),'peak_owned':peak,'physical_paid_histogram':hist,'physical_events':len(t['program']),'deferred_helper_witness':{'role':target,'current_chart':uc[target],'difference_not_in_current_difference_observation_span':missing}}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=source_default());ap.add_argument('--transcript',type=Path,default=Path(__file__).with_name('demand-prefix.json.gz'));ap.add_argument('--output',type=Path);a=ap.parse_args();w=load_source(a.source);payload=gzip.decompress(a.transcript.read_bytes());t=json.loads(payload);st=time.time();result=verify(w,t);controls=[]
 first_delivery=t['deliveries'][0]['owner']
 for label,mutate in [('wrong_owned_MOVE_flag',lambda z:next(e for e in z['program'] if e[0]=='MOVE' and e[1]==first_delivery).__setitem__(4,False)),('wrong_first_delivery_sign',lambda z:next(e for e in z['program'] if e[0]=='ADD' and e[1]==first_delivery).__setitem__(3,'1/2')),('false_input_retention',lambda z:z['retained_input_differences'][0].__setitem__('holder',z['retained_input_differences'][1]['holder']))]:
  z=json.loads(payload);mutate(z)
  try:verify(w,z)
  except ValueError as ex:controls.append({'mutation':label,'rejection':str(ex)})
  else:raise ValueError('negative control survived '+label)
 result.update(status='PASS_EXACT_MAIN_DEMAND_PREFIX',source_sha256=PIN,transcript_payload_sha256=hashlib.sha256(payload).hexdigest(),cut=t['source_cut'],negative_controls=controls,elapsed_seconds=time.time()-st,scope='All1880 formal inputs; current mains and full input information retained. Second-helper current cochart states are explicitly deferred. No complete native or kappa.')
 s=json.dumps(result,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
if __name__=='__main__':main()
