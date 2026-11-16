#!/usr/bin/env python3
"""Bank-separated C9 compression: exact cut duals and all-row decoders."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--envelope-result',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(a.envelope_result)=='5bd89e3a32a0649fd3b3c1adf68ebd857100aa653aa2ee4cb1273cfd3f1fc5f0'
assert sha(a.word)=='d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71'
D=json.loads(a.envelope_result.read_text());w=json.loads(a.word.read_text());src=a.repo/w['source_path'];assert sha(src)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(src.read_text())['native_roots']
B=[int(x,16)for x in D['reconstructed_common_bank_rows_hex']]+[1<<j for g in D['private_groups']for j in g]
E=B+[1<<i for i in D['all_six_bank_case']['feedback_closure']]
local=[[1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0]for i in range(111)]
K=[(1<<i)^sum(local[i])for i in range(111)];U=[[int(x,16)for x in g]for g in D['actual_remaining_filter_rows_hex']]
groups=[5,7,9,11];names=[[rec['name']for rec in w['history_cache_metadata']if rec['group']==g]for g in groups]
assert U==[[int(rec['row_hex'],16)for rec in w['history_cache_metadata']if rec['group']==g]for g in groups]
def solver(rows):
 b={};kernel=[]
 for i,r in enumerate(rows):
  co=1<<i
  while r:
   k=r&-r
   if k in b:s,c=b[k];r^=s;co^=c
   else:b[k]=(r,co);break
  if not r:kernel.append(co)
 def solve(x):
  co=0
  while x:
   k=x&-x
   if k not in b:return None
   r,c=b[k];x^=r;co^=c
  return co
 return solve,len(b),kernel
rank=lambda rows:solver(rows)[1]
def value(rows,co):
 assert co is not None and co>>len(rows)==0
 out=0
 for i,r in enumerate(rows):
  if co>>i&1:out^=r
 return out
def dual(rows,extra,which):
 piv={}
 for r,z in [(r,0)for r in rows]+[(r,int(i==which))for i,r in enumerate(extra)]:
  while r:
   b=r&-r
   if b in piv:s,t=piv[b];r^=s;z^=t
   else:piv[b]=(r,z);break
  if not r:assert z==0
 out=0
 for b,(r,z)in sorted(piv.items(),reverse=True):
  if ((r&out).bit_count()%2)^z:out^=b
 assert all(not((r&out).bit_count()%2)for r in rows)
 assert [(r&out).bit_count()%2 for r in extra]==[int(i==which)for i in range(len(extra))]
 return out

cases=[]
for model,BB,masks,expected in [('rank80',B,[[12,5,3]]*3+[[12,5,3,16]],[3,3,3,4]),('rank88_feedback',E,[[1,2]]*3+[[1,2,4]],[2,2,2,3])]:
 cuts=[]
 for i in range(4):
  other=BB+[r for j,rows in enumerate(U)if j!=i for r in rows];current=list(other);chosen=[]
  for j,k in enumerate(K):
   if solver(current)[0](k)is None:chosen.append(j);current.append(k)
  assert len(chosen)==expected[i]
  ds=[dual(other,[K[j]for j in chosen],t)for t in range(len(chosen))]
  cuts.append({'bank':groups[i],'other_bank_plus_side_rank':rank(other),'plus_C9_rank':rank(other+K),'conditional_C9_dimension':len(chosen),'separated_canonical_indices':chosen,'dual_hex':[hex(x)for x in ds]})
 messages=[[value(rows,mask)for mask in masks_i]for rows,masks_i in zip(U,masks)]
 assert [rank(rows)for rows in messages]==expected
 M=BB+sum(messages,[]);solve=solver(M)[0];cert=[solve(k)for k in K];assert all(z is not None for z in cert)
 assert all(value(M,co)==k for co,k in zip(cert,K))
 target_indices=[];current=list(BB)
 for i,k in enumerate(K):
  if solver(current)[0](k)is None:target_indices.append(i);current.append(k)
 decoders=[]
 for i in target_indices:
  co=cert[i];side=co&((1<<len(BB))-1);msg=co>>len(BB);assert K[i]==value(BB,side)^value(sum(messages,[]),msg);decoders.append({'canonical_index':i,'side_coefficient_hex':hex(side),'message_coefficient_hex':hex(msg)})
 cases.append({'model':model,'side_rank':rank(BB),'side_row_count':len(BB),'side_rows_hex':[hex(x)for x in BB],'canonical_quotient_dimension':len(target_indices),'canonical_quotient_basis_indices':target_indices,'bank_dimensions_mod_side':[rank(BB+r)-rank(BB)for r in U],'joint_bank_dimension_mod_side':rank(BB+sum(U,[]))-rank(BB),'cut_certificates':cuts,'minimum_bank_message_dimensions':expected,'minimum_total_scalar_messages':sum(expected),'bank_message_original_row_masks':[[hex(x)for x in mm]for mm in masks],'bank_messages_hex':[[hex(x)for x in mm]for mm in messages],'all111_canonical_witnesses_hex':[hex(x)for x in cert],'quotient_basis_decoders':decoders,'one_message_per_bank_impossible':all(x>1 for x in expected)})
assert rank(K)==9
result={'status':'PASS_EXACT_BANK_SEPARATED_CANONICAL_COMPRESSION','source_word_sha256':sha(a.word),'envelope_result_sha256':sha(a.envelope_result),'native_source_sha256':sha(src),'bank_groups':groups,'bank_charts':['C1','C3','C4','Extra6'],'bank_row_names':names,'bank_rows_hex':[[hex(r)for r in rows]for rows in U],'cases':cases,'proof_scope':'Static fixed-side-information C9 inclusion by bank-separated linear messages; every characteristic-two field and all positive record widths via rank/dual tensoring. No new point-feedback grants after messages, noncanonical optimality, physical delivery, or new kappa claimed.','new_kappa':False}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'cases':[{k:d[k]for k in['model','side_rank','canonical_quotient_dimension','minimum_bank_message_dimensions','minimum_total_scalar_messages','quotient_basis_decoders']}for d in cases],'bank_names':names}))
