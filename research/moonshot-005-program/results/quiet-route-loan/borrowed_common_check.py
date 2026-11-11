#!/usr/bin/env python3
"""One dirty-input functional proves common449 is temporarily unavailable."""
import argparse,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(c,m):
 if not c:raise ValueError(m)
def run(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));n=w['public'];M=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));C={r:n+i for i,r in enumerate(M)};need(1477 not in C,'dual is a dirty helper input')
 p=n+len(M);v=[Q(1) if r==1477 else Q(0) for r in range(p+w['owned_fields'])];cur=w['initial']+[w['initial'][r] for r in M]+[None]*w['owned_fields']
 def phys(r):return r if r<n else r+400
 for e in w['program'][:28048]:
  op,r=e[:2];r=phys(r)
  if op in ('ADD','COPY'):v[r]+=Q(e[3])*v[phys(e[2])]
  elif op=='SCALE':v[r]*=Q(e[2])
  elif op in ('INIT','CLEAR'):v[r]=Q(0);cur[r]=e[2] if op=='INIT' else None
  elif op=='MOVE':
   cur[r]=e[3]
   if e[1] in C:cur[C[e[1]]]=e[3]
  else:raise ValueError(op)
 h=449;d=C[907];r=C[977];target=v[h];need(target==1 and cur[h]==cur[d]==3 and cur[r]==594,'source instance dual and charts')
 v[h]+=v[d];v[d]-=v[h];v[h]+=v[d];cur[h]=594;v[r]+=v[h]
 holders=[i for i,f in enumerate(cur) if f==594];need(holders==[449,977,1206,1427,1869],'all current destination holders');need(all(v[i]==0 for i in holders),'dual vanishes on complete destination span');need(v[d]==-1 and cur[d]==3,'dirty common payload physically retained at source')
 return {'status':'PASS_DIRTY_COMMON_NOT_CURRENTLY_LOCAL','source_sha256':PIN,'cut_before_source_event':28049,'dual_input':'entering dirty helper1477','dual_column':1477,'desired_common449_coefficient':'1','actual_destination_holders':holders,'actual_destination_coefficients':['0']*len(holders),'retained_dirty_common_payload_holder':d,'retained_holder_frame':3,'retained_holder_coefficient':'-1','scope':'Exact one-coordinate witness that current common449 is unavailable at chart594 during the quiet loan. It is restored before the next source use.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
