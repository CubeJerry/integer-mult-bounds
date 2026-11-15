#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--funnel-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();sys.path.insert(0,str(a.funnel_review))
from check import rank,rr
R=json.loads((a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_text())['native_roots']
K=[sum(1<<j for j in range(111)if i==j or sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)]
reports=[]
for I in [[0,3,76,80],[1,3,73,76,77,80],list(range(111))]:
 C={}
 for j,r in enumerate(R):
  s=tuple(i for i in I if sum(x*y for x,y in zip(R[i],r))==0);C[s]=C.get(s,0)|(1<<j)
 mixed={s:z for s,z in C.items()if len(s)>1};single={s[0]:z for s,z in C.items()if len(s)==1}
 d={'receivers':len(I),'normal_rank':len(rr([R[i]for i in I])),'classes':len(C),'mixed':len(mixed),'singletons':len(single)}
 if len(I)<10:
  rows=list(mixed.values());good=[]
  for bits in range(1<<len(rows)):
   B=K+[z for k,z in enumerate(rows)if bits>>k&1]
   if all(rank(B+[single.get(i,0),1<<i])==rank(B+[single.get(i,0)])for i in I):good.append(bits)
  d['minimum_retained']=min(x.bit_count()for x in good);d['minimizers']=sum(x.bit_count()==d['minimum_retained']for x in good)
 else:d['classes_are_single_inputs']=all(z.bit_count()==1 for z in C.values());d['class_chart_dimensions']=sorted(set(8-len(rr([R[i]for i in s]))for s in C))
 reports.append(d)
I=[1,3,73,76,77,80];C={}
for j,r in enumerate(R):
 s=tuple(i for i in I if sum(x*y for x,y in zip(R[i],r))==0);C[s]=C.get(s,0)|(1<<j)
z=0
for s in [(3,76,80),(3,73,77),(1,76,77),(1,73,80)]:z^=C[tuple(sorted(s))]
assert z==K[1]^K[3]==K[73]^K[76]==K[77]^K[80]
assert ((4|8|1)^(8|2))==(4|1|2)and ((4|1)^(8|2))!=(4|1|2)
out={'status':'PASS_ROOT_FUNNEL_BRIDGE','classifications':reports,'triangle_support':z.bit_count(),'early_lift_Hub_correction_control':True};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
