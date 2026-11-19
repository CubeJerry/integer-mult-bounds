#!/usr/bin/env python3
"""Exact full output/mask audit and the shared K370 packet's native support."""
import argparse,gzip,json
from hashlib import sha256
from pathlib import Path
from common import B,N,PUBLIC,fid
def rank(rows):
 basis={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p not in basis:basis[p]=v;break
   v^=basis[p]
 return len(basis)
def main():
 p=argparse.ArgumentParser();p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 wr=gzip.decompress(a.word.read_bytes());w=json.loads(wr);c=json.loads(gzip.decompress(a.certificate.read_bytes()));state={};owned=set();packet=None
 target=next(x['output_field']for x in c['late_K_aggregates']if x['K']==370)
 def get(b):return state.get(b,1<<b)if b<5*PUBLIC else state[b]
 xmask=(1<<(5*N*B))-1
 for act in w['actions']:
  for op in act['word']:
   if op[0]=='ADD':state[op[1]]=get(op[1])^get(op[2])
   elif op[0]=='INIT':assert op[1]not in owned;owned.add(op[1]);state[op[1]]=0
   else:assert op[0]=='CLEAR'and op[1]in owned;owned.remove(op[1]);del state[op[1]]
  if act['tag']=='aggregate-Y-K-370':packet=[get(5*target+b)&xmask for b in range(5)]
 assert not owned and packet is not None
 output={b:v&xmask for b,v in state.items()if 5*N*B<=b<5*PUBLIC and v&xmask}
 mask=sum(1<<(5*fid('X',int(j),col)+bit)for j,cols in w['private_mask_columns_by_donor'].items()for col in cols for bit in range(5));maskrank=rank(v&mask for v in output.values());assert maskrank==0
 donor_ranks={j:rank((v>>(5*j*B))&((1<<(5*B))-1)for v in packet)for j in range(N)};nonzero={j:r for j,r in donor_ranks.items()if r};assert set(nonzero)==set(w['source_donors'])and set(nonzero.values())=={5}
 rb=rank(output.values());fields=sorted({b//5 for b in output});ybits=[5*f+b for f in fields for b in range(5)];xindices={b-5*N*B:k for k,b in enumerate(ybits)};sourcemask=sum(1<<b for b in xindices);principal=[]
 for k,b in enumerate(ybits):
  v=output.get(b,0)&sourcemask;r=1<<k
  while v:
   low=v&-v;pos=low.bit_length()-1;r^=1<<xindices[pos];v^=low
  principal.append(r)
 rp=rank(principal);q=5*N*B-len(ybits)+rp
 assert rb%5==q%5==0
 proper={b-5*N*B:v for b,v in output.items()};rowmask=sum(1<<b for b in proper);squared=[];overlap=set()
 for v in proper.values():
  wv=v&rowmask;z=0
  while wv:
   low=wv&-wv;k=low.bit_length()-1;overlap.add(k//5);z^=proper[k];wv^=low
  squared.append(z)
 square_rank=rank(squared)
 result={'status':'PASS_COMMON_FRAME_FULL_OUTPUT_AND_PACKET_AUDIT','word_pin':sha256(wr).hexdigest(),'all_original_input_columns_in_scope':5*PUBLIC,'private_original_mask_fields':sum(map(len,w['private_mask_columns_by_donor'].values())),'all_Y_mask_response_rank_binary':maskrank,'proper_B_rank_binary':rb,'proper_B_rank_field':rb//5,'affected_output_fields':len(fields),'return_principal_dimension_binary':len(ybits),'return_principal_rank_binary':rp,'exact_return_rank_binary':q,'exact_return_rank_field':q//5,'K370_late_aggregate_output_field':target,'K370_donor_count':len(nonzero),'K370_binary_rank_each_donor':nonzero,'K370_binary_rank_total':rank(packet),'new_complete_kappa':False}
 result.update({'nonzero_Y_output_roles':sorted({(f-N*B)//B for f in fields}),'input_output_coordinate_support_intersection':[[f//B,f%B]for f in sorted(overlap)],'coordinate_support_disjoint':not overlap,'B_squared_rank_binary':square_rank,'B_squared_is_zero':square_rank==0})
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='K370_binary_rank_each_donor'},indent=2,sort_keys=True))
if __name__=='__main__':main()
