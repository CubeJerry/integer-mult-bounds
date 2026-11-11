#!/usr/bin/env python3
"""Verify short dual certificates directly, without the control-space search."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def span(frame):
 a={0}
 for x in frame:a.update({x^y for y in list(a)})
 return frozenset(a)
def add(a,j,z):
 z=a.get(j,F(0))+z
 if z:a[j]=z
 else:a.pop(j,None)
def check_case(w,C,case,mutant=None):
 k,h,x=case['event'],case['helper'],case['donor'];e=w['program'][k]
 need(e[0]=='MOVE' and e[1]==h and not e[4],'actual public-helper departure')
 M=set(w['live'])|{j+112 for j in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 need(h not in M and 0<=h<w['public'] and x in M,'public helper and raw main donor')
 path=[C[w['initial'][x]]]
 for op in w['program']:
  if op[0]=='MOVE' and op[1]==x:path.append(C[op[3]])
 need(C[e[2]] in path and C[w['final'][x]]==C[127],'donor source access and finalhub')
 at=path.index(C[e[2]]);allowed=set(path[at:]);a={int(j):F(v) for j,v in case['dual_final_output_functional'].items()};loc=dict(enumerate(w['final']))
 need(a and all(j<w['public'] and C[loc[j]]!=C[127] for j in a),'nonzero offhub output functional')
 def control_zero(j):
  need(j not in loc or C[loc[j]] not in allowed or not a.get(j),'a future permitted station control changes the dual')
 for j in loc:control_zero(j)
 # Invariant: every currently live role in any allowed station has zero
 # adjoint. Only changed adjoints or changed locations need rechecking.
 for t in range(len(w['program'])-1,k,-1):
  op=w['program'][t];tag,j=op[:2];changed=[]
  if tag=='ADD':
   s=op[2];add(a,s,a.get(j,F(0))*F(op[3]));changed=[s]
  elif tag=='COPY':
   s=op[2];need(s!=j,'distinct COPY roles');add(a,s,a.get(j,F(0))*F(op[3]));a.pop(j,None);changed=[s,j]
  elif tag=='SCALE':
   z=a.get(j,F(0))*F(op[2]);a.pop(j,None)
   if z:a[j]=z
   changed=[j]
  elif tag=='MOVE':loc[j]=op[2];changed=[j]
  elif tag=='CLEAR':loc[j]=op[2];a.pop(j,None);changed=[j]
  elif tag=='INIT':loc.pop(j,None);a.pop(j,None)
  else:raise ValueError('unknown opcode')
  for j in changed:control_zero(j)
 need(loc[h]==e[3],'adjoint reaches post-departure location')
 target=a.get(h,F(0));need(target==F(case['target_pairing'])==1,'normalized nonzero pulse response')
 # A new outside snapshot at this exact destination would break the theorem.
 if mutant=='add_destination_station':
  allowed.add(C[e[3]]);control_zero(h)
 if mutant=='erase_initial_pulse':
  need(F(0)==target,'erased pulse falsely accepted')
 return {'event':k,'helper':h,'donor':x,'dual_support':len(case['dual_final_output_functional']),'target_pairing':str(target),'remaining_station_charts':len(allowed),'suffix_instructions_checked':len(w['program'])-k-1}
def main(args):
 p=args.repository/'research/shared-wire-split-composition/data/final.json.gz';raw=p.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin');w=json.loads(gzip.decompress(raw));C=list(map(span,w['frames']));cert=json.loads((args.package/'CERTIFICATE.json').read_text());need(cert['native_sha256']==PIN,'certificate source pin');cases=cert['cases'];need(len(cases)==103 and len({(c['event'],c['donor']) for c in cases})==103,'103 distinct pinned cases');results=[check_case(w,C,c) for c in cases]
 controls=[]
 for mutation in ['add_destination_station','erase_initial_pulse']:
  try:check_case(w,C,cases[0],mutation)
  except ValueError as e:controls.append({'mutation':mutation,'rejection':str(e)})
  else:raise ValueError('negative control accepted')
 out={'status':'PASS_103_EXACT_ITINERARY_CONTROL_DUALS','native_sha256':PIN,'certificate_sha256':hashlib.sha256((args.package/'CERTIFICATE.json').read_bytes()).hexdigest(),'cases':len(results),'source_events':len({c['event'] for c in cases}),'dual_support_histogram':dict(sorted(collections.Counter(r['dual_support'] for r in results).items())),'all_duals_use_only_final_public_outputs':True,'COPY_zero_guard_not_needed_for_obstruction':True,'negative_controls':controls,'scope':'An initial helper pulse at each listed departure cannot be neutralized offhub using arbitrary future additive field controls at any station on the donor remaining original itinerary. Free stationary caches, arbitrary field-coordinate mixing, and all finalhub corrections are granted. This does not exclude jointly designed source pulses or controls at additional stations. No new kappa.','checked_cases':results};args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repository',type=Path,required=True);ap.add_argument('--package',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
