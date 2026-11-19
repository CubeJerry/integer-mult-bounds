#!/usr/bin/env python3
"""All-original-input endpoint comparison, including all unprescribed Y rows."""
import argparse,gzip,json
from pathlib import Path
from hashlib import sha256
from common import N,B,PUBLIC,fid
def rows(word):
 state={};owned=set()
 def get(k):return state.get(k,1<<k)if k<5*PUBLIC else state[k]
 for action in word['actions']:
  for op in action['word']:
   if op[0]=='INIT':assert op[1]not in owned;owned.add(op[1]);state[op[1]]=0
   elif op[0]=='ADD':state[op[1]]=get(op[1])^get(op[2])
   else:assert op[0]=='CLEAR'and op[1]in owned;owned.remove(op[1]);del state[op[1]]
 assert not owned
 mask=(1<<(5*N*B))-1
 return {k:v&mask for k,v in state.items()if 5*N*B<=k<5*PUBLIC and v&mask}
def rank(rows):
 basis={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p not in basis:basis[p]=v;break
   v^=basis[p]
 return len(basis)
def main():
 p=argparse.ArgumentParser();p.add_argument('--preferred',type=Path,required=True);p.add_argument('--control',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 raw=[gzip.decompress(p.read_bytes())for p in [a.preferred,a.control]];words=list(map(json.loads,raw));preferred,control=map(rows,words)
 mask=sum(1<<(5*fid('X',j,c)+b)for j in words[0]['shared_donors']for c in words[0]['mask_coordinates']for b in range(5))
 rp=rank(v&mask for v in preferred.values());rc=rank(v&mask for v in control.values());delta={k:preferred.get(k,0)^control.get(k,0)for k in set(preferred)|set(control)}
 assert all(v&~mask==0 for v in delta.values());rd=rank(delta.values());assert (rp,rc,rd)==(0,120,120)
 selected={5*fid('Y',i,c)+b for i in [80,1]for c in range(4)for b in range(5)};assert all(delta.get(k,0)==0 for k in selected)
 result={'status':'PASS_FULL_OUTPUT_MASK_LEAKAGE_COMPARISON','preferred_word_pin':sha256(raw[0]).hexdigest(),'control_word_pin':sha256(raw[1]).hexdigest(),'original_mask_fields':24,'original_mask_bits':120,'preferred_all_Y_mask_rank_binary':rp,'control_all_Y_mask_rank_binary':rc,'whole_B_difference_rank_binary':rd,'whole_B_difference_rank_field':rd//5,'difference_supported_only_on_mask_columns':True,'all_selected_target_rows_unchanged':True,'all_original_input_columns_checked':5*PUBLIC}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'MASK-COMPARISON.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
