#!/usr/bin/env python3
"""Compile every supplied source/H phase and charge real stationary caches."""
from pathlib import Path
from argparse import ArgumentParser
from array import array
import gzip,hashlib,json
import numpy as np

def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&64:a^=67
 return c
ROWS=[[sum(((mul(v,1<<c)>>r)&1)<<c for c in range(6))for r in range(6)]for v in range(64)]
WEIGHT=np.array([sum(x.bit_count()for x in row)for row in ROWS],dtype=np.uint64)
def binary_rows(A):
 out=[]
 for row in A:
  r=[0]*6
  for c,v in enumerate(row):
   for q,w in enumerate(ROWS[int(v)]):r[q]|=w<<(6*c)
  out+=r
 return out

def compile_phase(A):
 n=len(A)*6;rows=binary_rows(A);digest=hashlib.sha256();buf=array('I');adds=0
 def add(t,s):
  nonlocal adds
  rows[t]^=rows[s];buf.extend([t,s]);adds+=1
  if len(buf)>=8192:digest.update(buf.tobytes());del buf[:]
 for q in range(n):
  bit=1<<q
  if not rows[q]&bit:
   p=next(r for r in range(q+1,n)if rows[r]&bit);add(q,p);add(p,q);add(q,p)
  for r in range(n):
   if r!=q and rows[r]&bit:add(r,q)
 if rows!=[1<<q for q in range(n)]:raise ValueError('binary phase elimination residual')
 digest.update(buf.tobytes());return {'field_dimension':len(A),'binary_dimension':n,'ADD_per_direction':adds,'elimination_word_uint32le_sha256':digest.hexdigest()}

def main(repo,package,out):
 out.mkdir(parents=True,exist_ok=True);s=read(package/'output/SOURCES.json.gz');early=read(package/'output/EARLY.json.gz');hs=read(package/'output/H-PHYSICAL.json.gz');d=read(package/'output/D-WORD.json.gz');old=read(repo/'research/moonshot-005-program/results/bit-shared-h-s031-construction/d-aligned-full45-pair/output/COEFFICIENTS.json.gz');records={'sources':{},'H':{}};rawroutes=[json.loads(x)for x in gzip.decompress((repo/'research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()];tot={'phase_forward_inverse_ADD':0,'source_parity_cache_INIT':0,'source_parity_form_ADD':0,'source_parity_inject_ADD':0,'source_parity_dirty_CLEAR':0,'H_early_cache_INIT':0,'H_early_cache_copy_ADD':0,'H_late_cross_ADD':0,'H_early_cache_dirty_CLEAR':0}
 for j,e in sorted(early.items(),key=lambda q:int(q[0])):
  A=np.array(e['physical_matrix'],dtype=np.uint8);p=compile_phase(A);tot['phase_forward_inverse_ADD']+=2*p['ADD_per_direction'];P=np.vstack([np.array(M,dtype=np.uint8).reshape(-1,480)for M in s['late_parities'][j].values()]);n=6*len(P);weight=int(WEIGHT[P].sum());tot['source_parity_cache_INIT']+=n;tot['source_parity_form_ADD']+=weight;tot['source_parity_inject_ADD']+=n;tot['source_parity_dirty_CLEAR']+=n;records['sources'][j]={'early':p,'actual_late_field_parities':len(P),'stationary_parity_bits':n,'exact_parity_form_ADD':weight,'actual_Y_injection_ADD':n,'cache_bindings':[{'H':int(h),'Y_owner':[x[1],x[2]],'row':q,'cache_label':f'source-parity/{j}/{h}/{q}'}for h,M in s['late_parities'][j].items()for q,x in enumerate(sorted([x for x in rawroutes if x[0]=='Y'and x[3]==int(h)and x[6]==int(j)],key=lambda x:(x[1],x[2])))]};print('COMPILED_SOURCE',j,p['ADD_per_direction'],weight,flush=True)
 for h,z in sorted(hs.items(),key=lambda q:int(q[0])):
  E=np.array(z['early'],dtype=np.uint8);B=np.array(z['late'],dtype=np.uint8);G=np.array(z['cross'],dtype=np.uint8);paid=False
  if int(h)==642:E=np.array(old['H']['642']['physical']['extension'],dtype=np.uint8);paid=True
  er=compile_phase(E);br=compile_phase(B)if len(B)else None;tot['phase_forward_inverse_ADD']+=2*(er['ADD_per_direction']+(br['ADD_per_direction']if br else 0));n=6*len(z['X_owners'])if np.any(G)else 0;weight=int(WEIGHT[G].sum())if len(G)else 0;tot['H_early_cache_INIT']+=n;tot['H_early_cache_copy_ADD']+=n;tot['H_late_cross_ADD']+=weight;tot['H_early_cache_dirty_CLEAR']+=n;records['H'][h]={'early':er,'late':br,'paid_H642_extension':paid,'stationary_original_early_cache_bits':n,'exact_late_cross_ADD':weight,'cache_bindings':[[x[1],x[2]]for x in z['X_owners']]if n else[]}
  if int(h)in[263,642,947]:print('COMPILED_H',h,er['ADD_per_direction'],br['ADD_per_direction']if br else 0,weight,flush=True)
 dc=d['compiler'];base_add=tot['phase_forward_inverse_ADD']+tot['source_parity_form_ADD']+tot['source_parity_inject_ADD']+tot['H_early_cache_copy_ADD']+tot['H_late_cross_ADD']+dc['including_pure_inverse_ADDs'];base_init=tot['source_parity_cache_INIT']+tot['H_early_cache_INIT']+dc['INIT']+12;base_clear=tot['source_parity_dirty_CLEAR']+tot['H_early_cache_dirty_CLEAR']+dc['dirty_CLEAR']+12
 result={'status':'PASS_CHRONOLOGICAL_FIVE_SOURCE_H_D_COMPILERS','base480_field_pair_copies':8,'source_phase_words':5,'H_phase_modules':len(hs),'D_phase_dimensions':[19,16],'base_counts':tot,'D_base_counts':{k:v for k,v in dc.items()if isinstance(v,int)},'H642_base_paid_fields':2,'fullbank_ADD_including_phase_inverses':8*base_add,'fullbank_INIT':8*base_init,'fullbank_dirty_CLEAR':8*base_clear,'fullbank_extra_MOVE_binary_records':96,'extra_MOVE_gap':6,'fullbank_extra_field_exports':16,'base_peak_cache_bits_if_lifetimes_overlap':base_init,'global_reverse_phase_compiler_dependency':True,'full_global_supplier_invoice':False,'new_complete_kappa':False};payload=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();(out/'PHASE-COMPILER-RECEIPTS.json.gz').write_bytes(gzip.compress(payload,mtime=0));result['phase_receipt_sha256']=hashlib.sha256(payload).hexdigest();(out/'COMPILER-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],result['fullbank_ADD_including_phase_inverses'],result['fullbank_INIT'],result['fullbank_extra_field_exports'],flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.package.resolve(),q.out.resolve())
