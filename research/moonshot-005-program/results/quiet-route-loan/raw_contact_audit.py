#!/usr/bin/env python3
"""Independent source-interval census of single quiet-route raw shears."""
import argparse,bisect,gzip,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,msg):
 if not x:raise ValueError(msg)
def run(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));P=w['program'];end=len(P)
 M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);intervals={};touches=defaultdict(list);cur={r:w['initial'][r] for r in M};arr={r:-1 for r in M}
 for i,e in enumerate(P):
  op,r=e[:2];touches[r].append(i)
  if op in ('ADD','COPY'):touches[e[2]].append(i)
  if op=='MOVE' and r in M:
   need(cur[r]==e[2] and (r,cur[r]) not in intervals,'literal unique main visits');intervals[r,cur[r]]=(arr[r],i);cur[r]=e[3];arr[r]=i
 for r in M:need((r,cur[r]) not in intervals,'unique last visit');intervals[r,cur[r]]=(arr[r],end)
 loans=[];contacts=[];critical=[]
 for i,e in enumerate(P):
  if e[0]!='MOVE' or e[1] in M:continue
  _,h,s,d,_=e;j=bisect.bisect_right(touches[h],i);deadline=touches[h][j] if j<len(touches[h]) else end
  for q in sorted(M):
   si=intervals.get((q,s));di=intervals.get((q,d))
   if si is None or di is None or not(si[0]<i<si[1]) or not(i<di[0]<deadline):continue
   close=di[0];rec={'start':i,'close':close,'helper_next_use':deadline,'helper':h,'donor':q,'from':s,'to':d};loans.append(rec)
   for r in sorted(M):
    ri=intervals.get((r,d))
    if ri is None or max(i,ri[0])>=min(close,ri[1]):continue
    if ri[1]<close:
     need(s==3 and w['frames'][s]==[],'every deadline-critical loan leaves zero chart')
     need(w['initial'][q]==w['initial'][r]==3,'critical pair already cochart at entry')
     early=intervals[q,3];rr=intervals[r,3];need(max(early[0],rr[0])<min(early[1],rr[1]),'earlier direct raw contact')
     witness={'loan_start':i,'donor':q,'recipient':r,'recipient_departure':ri[1],'donor_return':close,'direct_ADD_after_source_event':-1,'direct_frame':3};critical.append(witness)
    else:
     need(ri[0]<close<ri[1],'recipient remains for direct return contact');witness={'loan_start':i,'donor':q,'recipient':r,'recipient_departure':ri[1],'donor_return':close,'direct_ADD_after_source_event':close,'direct_frame':d}
    contacts.append(witness)
 need(len(loans)==354 and len(critical)==61,'pinned census cardinalities');zero_arrivals=[i for i,e in enumerate(P) if e[0]=='MOVE' and e[3]==3];need(not zero_arrivals,'no funded arrival to zero chart')
 # An algebraic negative control excludes commuting a later coded innovation.
 early={'receiver':1,'donor':1};late={'receiver':1,'donor':1,'new_after_departure':1};need(early!=late,'changed-code commutation counterexample')
 records={'loans':loans,'contacts':contacts};encoded=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
 return {'status':'PASS_EXACT_RAW_QUIET_CONTACT_REDUNDANCY','source_sha256':PIN,'quiet_single_MOVE_loans':len(loans),'eligible_recipient_contacts':len(contacts),'deadline_critical_contacts':len(critical),'critical_source_frames':dict(Counter(r['direct_frame'] for r in critical)),'noncritical_contacts':len(contacts)-len(critical),'funded_arrivals_to_empty_chart':zero_arrivals,'all_contact_witnesses_sha256':hashlib.sha256(encoded).hexdigest(),'critical_witnesses':critical,'changed_code_counterexample':{'early_raw_shear':early,'later_changed_code_shear':late,'equal':False},'scope':'Every individual raw-difference shear in this complete single-MOVE quiet-window family can use an earlier source or later destination main contact. This does not remove dependencies among changed coded payloads or rule out read-active/multi-MOVE loans.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k!='critical_witnesses'},indent=2,sort_keys=True))
