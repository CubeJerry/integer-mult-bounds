#!/usr/bin/env python3
"""Derive per-record legal monotone MOVE intervals from actual literal words."""
import argparse,collections,gzip,hashlib,json,runpy
from pathlib import Path
def main(a):
 m=runpy.run_path(str(a.moment_checker));w=json.loads(gzip.decompress(a.word.read_bytes()));fr=w['frames'];pend={};q=collections.Counter();pubdown=collections.Counter();own=collections.Counter()
 def dim(c):return fr[str(c)]['dim']
 def flush(f):
  if f in pend:
   c,d=pend.pop(f);jump=abs(dim(d)-dim(c));q[jump]+=1
   if f>=222:own[jump]+=1
   elif dim(d)<dim(c):pubdown[jump]+=1
 for op in w['program']:
  tag,f=op[:2]
  if tag=='MOVE':
   _,f,c,d=op
   if f not in pend:pend[f]=(c,d)
   else:
    first,last=pend[f]
    if last!=c:raise ValueError('broken per-record path')
    if(dim(d)-dim(c))*(dim(last)-dim(first))>0:pend[f]=(first,d)
    else:flush(f);pend[f]=(c,d)
  else:
   flush(f)
   if tag=='ADD':flush(op[2])
 for f in list(pend):flush(f)
 if q!={1:26,2:3,3:2,4:2,5:3,6:8,7:209,8:3}or pubdown!={1:1}or sum(k*v for k,v in own.items())!=40:raise ValueError('actual profile mismatch')
 out={'scope':'Actual per-record monotone MOVE profile between all accesses; hypothetical further Hub routes do not establish a complete decoder.','t':'199/200','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'moment_checker_sha256':hashlib.sha256(a.moment_checker.read_bytes()).hexdigest(),'profile':dict(q),'owned_profile':dict(own),'public_downward_profile':dict(pubdown),'owned_rank_length':40,'public_downward_rank_length':1,'integer_allroute_load':42,'rank_length':1596,'moment':m['record'](m['moment'](q)),'conditional_added_Hub_packets':{str(k):m['record'](m['moment'](m['combine']((1,q),(k,{8:1}))))for k in(4,5,6)}}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['moment']['lower_decimal'])
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in('word','moment-checker','output'):p.add_argument('--'+n,type=Path,required=True)
 main(p.parse_args())
