#!/usr/bin/env python3
"""Exact activation thresholds and a fourteen-new-point bootstrap lower bound."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib

def solve(rows,v):
 B={}
 for k,r in enumerate(rows):
  c=1<<k
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p][0];c^=B[p][1]
   else:B[p]=(r,c);break
 c=0
 while v:
  p=v.bit_length()-1
  if p not in B:return None
  v^=B[p][0];c^=B[p][1]
 return c

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();source='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=(a.repo/source).read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=[int((i!=72 and dot(R[72],r)!=0)^(dot([0,0,1,1,0,0,1,-1],r)!=0))for i,r in enumerate(R)];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];S=[A[i]for i in [1,3,4,6,73,74,77,78]];Z=[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80];zm=sum(1<<j for j in Z);allS=[0]
 for s in S:allS += [v^s for v in allS]
 masks=[sum(1<<j for j in range(111)if dot(R[i],R[j])!=0)for i in range(111)];records=[]
 for i in range(111):
  if i in Z:continue
  mask=masks[i]&~zm&~(1<<i);candidates=[]
  for c,s in enumerate(allS):
   if s>>i&1:candidates.append(((s&mask).bit_count(),s&mask,c))
  best=min(candidates)if candidates else None;rr={'receiver':i,'h':h[i],'minimum_external_points':best[0]if best else None,'witness_points':[j for j in range(111)if best and best[1]>>j&1],'S_coefficient':best[2]if best else None,'number_of_own_coefficient_one_codewords':len(candidates)}
  if best:
   points=rr['witness_points'];assert all(h[j]==h[i]for j in points);assert solve([s&masks[i]&~(zm|best[1])for s in S],1<<i)is not None
  records.append(rr)
 forced=[r['receiver']for r in records if r['minimum_external_points']is None];assert forced==[19,20]and all(h[j]==1 for j in forced);mins={b:min(r['minimum_external_points']for r in records if r['h']==b and r['minimum_external_points']is not None)for b in [0,1]};assert mins=={0:5,1:7};assert all(not(s>>j&1)for s in S for j in forced)
 def closure(points):
  known=zm|sum(1<<j for j in points);waves=[]
  while True:
   add=0
   for i,mask in enumerate(masks):
    if not(known>>i&1)and solve([s&mask&~known for s in S],1<<i)is not None:add|=1<<i
   if not add:return[i for i in range(111)if known>>i&1],waves
   waves.append([i for i in range(111)if add>>i&1]);known|=add
 points=[26,34,35,47,72];closed,waves=closure(points);assert waves==[[10,27]]and len(closed)==24
 out={'status':'PASS_EXACT_FOURTEEN_POINT_BOOTSTRAP_LOWER_BOUND','source_path':source,'source_sha256':hashlib.sha256(raw).hexdigest(),'retained_S8_rows_hex':[hex(s)for s in S],'freely_granted_closed_set':Z,'all94_exact_activation_records':records,'threshold_histogram_by_h':{str(b):dict(Counter(str(r['minimum_external_points'])for r in records if r['h']==b))for b in [0,1]},'first_h0_activation_requires_at_least':5,'first_h1_activation_requires_at_least_excluding_zero_columns':7,'mandatory_zero_column_point_grants':forced,'minimum_fresh_individually_acquired_point_grants_for_all111_at_least':14,'five_point_attainment_example':{'points':points,'additional_feedback_waves':waves,'closed_set':closed,'closure_size':24},'scope':'Retain the S8 information interface; all17 prior outputs and all proper raw receiver side information are free; arbitrary later completed-point feedback is free; only fresh individually acquired raw-coordinate grants are charged. Nonpoint innovations or nonlocal receiver messages are outside this scope.','new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'THRESHOLD-CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'first thresholds',mins,'mandatory',forced,'lowerbound14','five-point closure',len(closed))
if __name__=='__main__':main()
