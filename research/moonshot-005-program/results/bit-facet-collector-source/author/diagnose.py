#!/usr/bin/env python3
"""Exact characteristic-two local-code and actual-kernel-visibility certificates."""
import argparse,json,hashlib
from pathlib import Path

def basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return b
def red(x,b):
 for p in sorted(b,reverse=True):
  if x>>p&1:x^=b[p]
 return x
def rank(rows):return len(basis(rows))
def dual(rows,target):
 b=basis(rows);r=red(target,b);assert r;z=r&-r
 for p in sorted(b):
  if (b[p]&z).bit_count()&1:z^=1<<p
 assert all((x&z).bit_count()%2==0 for x in rows)and(target&z).bit_count()%2==1
 return z
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,default=Path(__file__).parent/'output/WORD.json');p.add_argument('--out',type=Path,default=Path(__file__).parent/'verification/CODE-DIAGNOSTIC.json');a=p.parse_args()
wb=a.word.read_bytes();w=json.loads(wb);rp=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';rb=rp.read_bytes();assert hashlib.sha256(rb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(rb)['native_roots'];M=(1<<222)-1
local=[sum(3<<(2*j)for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)]
C=[(local[i]&(sum(1<<(2*j+a)for j in range(111))))|(1<<(2*i+a))for i in range(111)for a in range(2)];assert[hex(x)for x in C]==w['canonical_rows_hex'];T=[w['expected'][n][1]for n in w['packets']];K=[int(x,16)for x in w['kernel_rows_hex']];G=T+K;assert rank(C)==18 and rank(T)==19 and rank(G)==22 and rank(C+G)==22
rows=[];hist={};visible_fit=[];global_fit=[]
for i in range(111):
 J=local[i]|(3<<(2*i));forbidden=M^J;cr=rank([x&forbidden for x in C]);gr=rank([x&forbidden for x in G]);assert cr==16;r=rank(G)-gr-2;hist[r]=hist.get(r,0)+1
 visible=K[:2]if i==0 else K[2:]if i==1 else[];H=T+visible;mask=M^local[i];hb=basis([x&mask for x in H]);gb=basis([x&mask for x in G]);fits=[red(1<<(2*i+a),hb)==0 for a in range(2)];assert all(red(1<<(2*i+a),gb)==0 for a in range(2));global_fit.append(i)
 rec={'role':i,'canonical_forbidden_rank':cr,'G_forbidden_rank':gr,'local_quotient_dimension':r,'visible_kernel_count':len(visible),'visible_bank_fits':fits}
 if all(fits):visible_fit.append(i)
 else:
  bank=next(a for a in range(2)if not fits[a]);z=dual([x&mask for x in H],1<<(2*i+bank));assert not z&local[i];rec['failure_dual']={'bank':bank,'row_hex':hex(z),'support_columns':[j for j in range(222)if z>>j&1]}
 rows.append(rec)
assert hist=={3:1,2:1,1:9,0:100};assert all(rows[i]['local_quotient_dimension']<2 for i in range(2,111));lower=2*sum(r<2 for r in [x['local_quotient_dimension']for x in rows]);assert lower==218
result={'status':'PASS_FIXED_CODE_CHI_218_AND_VISIBILITY_DIAGNOSTIC','word_sha256':hashlib.sha256(wb).hexdigest(),'native_sha256':hashlib.sha256(rb).hexdigest(),'canonical_rank':18,'terminal_rank':19,'global_normalized_rank':22,'global_canonical_quotient':4,'local_quotient_dimension_histogram':hist,'universal_tensor_lift_charge_lower_bound':218,'potential_positive_saving_roles':[0,1],'actual_visible_information_fitted_roles':visible_fit,'actual_visible_information_failed_roles':[i for i in range(111)if i not in visible_fit],'positive_control_all_kernels_globally_granted_fits_all':global_fit,'rows':rows,'scope':'Fixed rowspace G tensor k^s, every characteristic-two field and positive s; arbitrary block recoding within that rowspace. No claim that dimension>=2 guarantees a saving; no claim for changed terminals or imported modes.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['rows','actual_visible_information_failed_roles','positive_control_all_kernels_globally_granted_fits_all']},indent=2))
