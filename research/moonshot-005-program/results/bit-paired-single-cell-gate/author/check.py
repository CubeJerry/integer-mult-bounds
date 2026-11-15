#!/usr/bin/env python3
"""Exact input-local punctures and native star witnesses at all paired cells."""
import argparse,hashlib,json
from pathlib import Path
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
BASE_SHA='3aaabaf76bbfabccce40fe2dc56c2dfaf7242061de698d19098d64ef8821a8e5'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 B={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in B:x^=B[j]
   else:B[j]=x;break
 return len(B)
def local(chart,r):
 if chart['kind']=='ann':return all(dot(n,r)==0 for n in chart['rows'])
 assert len(chart['rows'])==1
 v=chart['rows'][0]
 return all(r[i]*v[j]==r[j]*v[i]for i in range(8)for j in range(8))
def validate(R,C,c):
 E={i for i,r in enumerate(R)if local(C,r)};assert E==set(c['deleted'])
 st=c['star'];F=st['frame'];assert len(F)==len(set(F))==8 and not E&set(F)
 assert all(dot(R[i],R[j])!=0 for i in F for j in F)
 edges={}
 for a in st['edges']:
  q=a['role'];p=tuple(a['pair']);assert q not in E and q not in F and len(p)==2 and p not in edges
  assert p==tuple(j for j,i in enumerate(F)if dot(R[q],R[i])==0);edges[p]=q
 deg=[sum(j in p for p in edges)for j in range(8)];assert deg==st['degrees'] and min(deg)>=4
 for p,i in edges.items():
  for q,j in edges.items():
   if p<q and set(p)&set(q):assert dot(R[i],R[j])!=0
 keep=[i for i in range(111)if i not in E]
 K=[sum(1<<j for j in keep if i==j or dot(R[i],R[j])==0)for i in keep];assert rank(K)==9
 return {'deleted':sorted(E),'retained_roles':len(keep),'point_frame':F,'edges':len(edges),'degrees':deg,'all_field_star_rank_floor':9,'binary_canonical_attainment_rank':9,'single_cell_rank_ceiling':8}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);a=ap.parse_args();p=Path(__file__).parent;raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA;R=json.loads(raw)['native_roots'];b=a.base.read_bytes();assert hashlib.sha256(b).hexdigest()==BASE_SHA;charts=json.loads(b)['charts'];scan=json.loads((p/'SCAN.json').read_text());out={}
 for name,c in scan.items():out[name]=validate(R,charts[name],c['puncture'])
 assert len(out)==12
 c=json.loads(json.dumps(scan['A15']['puncture']));c['deleted'].append(c['star']['frame'][0])
 try:validate(R,charts['A15'],c)
 except AssertionError:pass
 else:raise AssertionError('invalid deletion accepted')
 c=json.loads(json.dumps(scan['A15']['puncture']));c['star']['edges'][0]['pair']=[0,1,2]
 try:validate(R,charts['A15'],c)
 except AssertionError:pass
 else:raise AssertionError('invalid edge accepted')
 result={'status':'PASS_ALL_TWELVE_SINGLE_CELL_PUNCTURE_CERTIFICATES','native_sha256':ROOT_SHA,'paired_source_sha256':BASE_SHA,'cases':out,'negative_controls':['invalid local puncture','wrong edge incidence'],'new_complete_kappa':False};(p/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
