#!/usr/bin/env python3
"""Exact eight-channel cut and singular stacked-demand witnesses."""
import argparse,gzip,json
from pathlib import Path
from hashlib import sha256
from field import reduce
from build import PINS,rows80
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();base=a.repo/'research/moonshot-005-program/results'
 lr=gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes());rr=gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes());assert sha256(lr).hexdigest()==PINS['layout']and sha256(rr).hexdigest()==PINS['routes']
 l=json.loads(lr);routes=[json.loads(s)for s in rr.splitlines()];roots=l['root_table'];neighbors=[j for j in range(111)if sum(x*y for x,y in zip(roots[80],roots[j]))==0]
 h=[k for k,H in enumerate(l['A2'])if 5 in H and set(H)<=set(l['D4'][12])];slots=[r for r in routes if r[4]==12 and r[3]in h]
 assert len(h)==4 and len(slots)==8 and sum(r[0]=='X'for r in slots)==4
 first=[[int(c==r or c==8+r)for c in range(480)]for r in range(8)];second=[[int(c==r)for c in range(480)]for r in range(8)];rank=reduce(first+second);assert rank==16>len(slots)
 controls={'omit_second_receiver_rank':reduce(first),'same_flat_receiver_twice_rank':reduce(second+second),'four_plus_four_rank':reduce(first[:4]+second[:4])};assert controls=={'omit_second_receiver_rank':8,'same_flat_receiver_twice_rank':8,'four_plus_four_rank':8}
 ranks={j:reduce(rows80(neighbors,j)+[[int(c==r)for c in range(480)]for r in range(4)])for j in l['D4'][12]};assert ranks[0]==5 and ranks[2]==4 and all(v==8 for j,v in ranks.items()if j not in [0,2])
 result={'status':'PASS_SOURCE_CUT_AND_DEPENDENT_LATE_INTERFACE_GATES','source_pins':PINS,'donor':5,'D':12,'receivers':[80,1],'left_H':h,'actual_cut_routes':slots,'field_cut_capacity':8,'full_stacked_rank':rank,'four_plus_four_stacked_ranks':ranks,'negative_controls':controls,'scope':'D12-only information interface; no claim against distributed multiple-D completion'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'GATES.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='actual_cut_routes'},indent=2,sort_keys=True))
if __name__=='__main__':main()
