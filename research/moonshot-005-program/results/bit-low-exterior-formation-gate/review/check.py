#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from functools import lru_cache
BASE=Path('research/moonshot-005-program')
NATIVE=BASE/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
T={14,17,19,20,96,99,101,102};U=sorted(set(range(8,111))-T)
CASES=[(1,'repo',str(BASE/'sessions/2026-11-17-S020/checkpoint10-evidence/A/four-arrival-frame-repair/output/WORD.json'),'a0c4665881feb6cdccd8dc8987387e578719bd191d028dc9851ceb355e85efdc','C/pair-source-audit/output/SINGLE-CUT.json','bb5046f18fadf7ae1f41a3f0012ec8c36b7beb353ae2ba7733a310253de2fa65',410),
(2,'workers','A/two-copy-f4/output/WORD.json','9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550','C/two-copy-source-cut/output/INDEPENDENT-CUT.json','5b105dab7c06497f26532d671f5c4f3d17d46ab32542d8f2a51bf82cd90fe336',812),
(3,'workers','A/three-copy-f8/output/WORD.json','9bc262b41d00df1619ccaa2cc167fff0fdf33a2913f1cec444f0b876412227c6','C/pair-source-audit/output/TRIPLE-CUT.json','fcbc94d829fc340ae8e38f86a175838299c21892aae2ae25a957a547af07e5d9',1218)]
def pinned(path,wanted):
 raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==wanted;return json.loads(raw)
def basis(rows):
 out={}
 for row in rows:
  v=list(map(F,row))
  for j,r in sorted(out.items()):
   c=v[j]
   if c:v=[x-c*y for x,y in zip(v,r)]
  j=next((j for j,c in enumerate(v)if c),None)
  if j is not None:
   c=v[j];out[j]=[x/c for x in v]
 return out
def chart(spec):
 b=basis(spec['rows'])
 if spec['kind']=='span':return b
 assert spec['kind']=='ann';rows=[]
 for f in range(8):
  if f in b:continue
  v=[F(0)]*8;v[f]=1
  for j,r in sorted(b.items(),reverse=True):v[j]=-sum(r[k]*v[k]for k in range(j+1,8))
  rows.append(v)
 return basis(rows)
def contains(b,row):
 v=list(map(F,row))
 for j,r in sorted(b.items()):
  c=v[j]
  if c:v=[x-c*y for x,y in zip(v,r)]
 return not any(v)
@lru_cache(None)
def power(n):
 scale=10**39;target=n**199*scale**200;lo=0;hi=n*scale+1
 while hi-lo>1:
  mid=(hi+lo)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 return F(lo,scale),F(hi,scale)
def moment(profile):
 lo=hi=F(0)
 for n,c in profile.items():
  a,b=power(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
def enc(x):return [str(v)for v in x]
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--workers',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 roots=pinned(a.repo/NATIVE,NATIVE_SHA)['native_roots'];gate=Counter({127:37,64:74,1:-74})
 for j in range(1,9):gate[1+7*j]+=74;gate[7*j]-=74
 allowance=tuple(x/6 for x in moment(gate));reports=[]
 for b,owner,word_name,word_sha,cut_name,cut_sha,count in CASES:
  word=pinned((a.repo if owner=='repo'else a.workers)/word_name,word_sha);cut=pinned(a.workers/cut_name,cut_sha);assert len(cut)==count
  charts={name:chart(spec)for name,spec in word['charts'].items()};positions={(f'C{c}__'if b>1 else'')+k+str(i):('L'+str(i)if k=='X'else'zero')for c in range(b)for k in ['X','Y']for i in range(111)}
  prof=Counter();cut_positions=None
  for ix,op in enumerate(word['operations']):
   if ix==word['carrier_interface_before_operation']:cut_positions=positions.copy()
   if op[0]=='INIT':positions[op[1]]=op[2]
   elif op[0]=='MOVE':prof[abs(len(charts[positions[op[1]]])-len(charts[op[2]]))]+=1;positions[op[1]]=op[2]
   elif op[0]=='CLEAR':del positions[op[1]]
   else:assert op[0]=='ADD'
  assert cut_positions=={f['name']:f['chart']for f in cut}
  memberships=0;membership_cache={}
  for field in cut:
   row=int(field['row_hex'],16);assert 0<=row<1<<(222*b);B=charts[field['chart']];assert len(B)==field['rank']
   for i in U:
    if any(row>>(222*c+i)&1 for c in range(b)):
     memberships+=1;key=(field['chart'],i)
     if key not in membership_cache:membership_cache[key]=contains(B,roots[i])
     assert membership_cache[key],(b,field['name'],i)
  source=tuple(v/b for v in moment(prof));room=(allowance[0]-source[1],allowance[1]-source[0]);profiles=[{4:9*b,1:8*b}]
  profiles += [{4:9*b-m,3:m+1,1:8*b}for m in range(2,b+2)]
  values=[moment(x)for x in profiles];index=min(range(len(values)),key=lambda i:values[i][0]);bill=tuple(v/b for v in values[index])
  assert all(values[index][1]<v[0]for i,v in enumerate(values)if i!=index)
  deficit=(bill[0]-room[1],bill[1]-room[0]);assert deficit[0]>0
  reports.append({'copies':b,'all_original_columns':222*b,'all_current_fields':count,'all_projected_root_memberships_checked':memberships,'leaks':0,'source_profile':dict(sorted(prof.items())),'limiting_room':enc(room),'lowest_admitted_profile':profiles[index],'lower_bill_per_copy':enc(bill),'strict_deficit_per_copy':enc(deficit)})
 a.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_INDEPENDENT_CURRENT_LOCALITY_AND_WEIGHTED_GATE_ARITHMETIC','native_sha256':NATIVE_SHA,'sources':reports,'scope':'Separate rational geometry and directed integer-root arithmetic. Universal chronological quotient argument is reviewed in REVIEW.md; no unrestricted tariff.'};(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
