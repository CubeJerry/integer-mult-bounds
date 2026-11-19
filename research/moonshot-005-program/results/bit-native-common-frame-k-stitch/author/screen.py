#!/usr/bin/env python3
"""Exact whole-target D pass-through and K-aggregation cut screens."""
import argparse,gzip,json
from pathlib import Path
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from common import PINS,B
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();base=a.repo/'research/moonshot-005-program/results'
 lr=gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes());rr=gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes());assert sha256(lr).hexdigest()==PINS['layout']and sha256(rr).hexdigest()==PINS['routes'];l=json.loads(lr);routes=[json.loads(s)for s in rr.splitlines()];roots=l['root_table'];H=l['A2']
 def dot(i,j):return sum(x*y for x,y in zip(roots[i],roots[j]))
 early=Counter((r[5],r[7])for r in routes if r[0]=='X');late=Counter((r[5],r[1])for r in routes if r[0]=='Y');records=[]
 for i in [80,1]:
  neighbors={j for j in range(111)if dot(i,j)==0};ks=[k for k,S in enumerate(H)if i in S];data=[]
  for k in ks:
   source={j for j in range(111)if all(dot(j,h)==0 for h in H[k])};data.append({'K':k,'native_source_support':sorted(source),'early_terminal_capacity':early[k,i],'late_terminal_capacity':late[k,i],'total_terminal_capacity':early[k,i]+late[k,i]})
  cuts={j:sum(d['total_terminal_capacity']for d in data if j in d['native_source_support'])for j in neighbors};assert set(cuts.values())=={480}and all(d['total_terminal_capacity']==30 for d in data)
  total=sum(d['total_terminal_capacity']for d in data);weighted=sum(len(d['native_source_support'])*d['total_terminal_capacity']for d in data);dmin=Fraction(len(neighbors)*B,12);maxsupport=max(len(d['native_source_support'])for d in data)
  assert weighted==len(neighbors)*B and dmin>total
  records.append({'receiver':i,'foreign_donors':len(neighbors),'K_count':len(ks),'early_terminal_total':sum(d['early_terminal_capacity']for d in data),'late_terminal_total':sum(d['late_terminal_capacity']for d in data),'actual_total_terminal_capacity':total,'independent_D_packet_rank_required_at_least':str(dmin),'independent_D_pass_through_excluded':True,'K_native_support_min':min(len(d['native_source_support'])for d in data),'K_native_support_max':maxsupport,'loose_K_rank_required_at_least':str(Fraction(len(neighbors)*B,maxsupport)),'weighted_K_capacity':weighted,'full_target_rank_demand_sum':len(neighbors)*B,'every_foreign_source_cut_exactly480':True,'every_K_terminal_capacity30':True,'K_details':data})
 out={'status':'PASS_EXACT_GLOBAL_K_SATURATION_SCREEN','source_pins':PINS,'records':records,'interpretation':'Full invertible foreign blocks require rank30 from every native donor supported at every K; each foreign donor has sixteen such K and all480 dimensions must survive. This is necessary, not a full construction.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'SYSTEM-SCREEN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'records':[{k:v for k,v in r.items()if k!='K_details'}for r in records]},indent=2,sort_keys=True))
if __name__=='__main__':main()
