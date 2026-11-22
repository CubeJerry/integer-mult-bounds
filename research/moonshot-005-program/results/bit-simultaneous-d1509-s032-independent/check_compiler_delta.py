#!/usr/bin/env python3
"""Independent changed-source binary compiler; frozen H/D costs inherited by exact pins."""
from array import array
import argparse,gzip,hashlib,json,runpy,sys,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
R=runpy.run_path(str(HERE/'check_frames.py'))
rd,wr,need,mm,BASE,ROOT=[R[k] for k in ['rd','wr','need','mm','BASE','ROOT']]
def lift(a):
 # Coefficient bits act on six polynomial-basis input columns.
 rows=[]
 for row in a:
  output=[0]*6
  for j,c in enumerate(row):
   for b in range(6):
    value=int(c)<<b
    for top in range(value.bit_length()-1,5,-1):
     if value>>top&1:value^=67<<(top-6)
    for bit in range(6):
     if value>>bit&1:output[bit]|=1<<(6*j+b)
  rows.extend(output)
 return rows
def compile_matrix(a):
 target=lift(a);n=len(target);work=target[:];ops=array('I');swapcount=0
 for col in range(n):
  pivot=next(j for j in range(col,n) if work[j]>>col&1)
  if pivot!=col:
   swapcount+=1
   for t,s in [(col,pivot),(pivot,col),(col,pivot)]:work[t]^=work[s];ops.extend([t,s])
  for j in range(n):
   if j!=col and work[j]>>col&1:work[j]^=work[col];ops.extend([j,col])
 identity=[1<<j for j in range(n)];need(work==identity,'binary elimination')
 replay=identity[:]
 for i in range(len(ops)-2,-1,-2):replay[ops[i]]^=replay[ops[i+1]]
 need(replay==target,'all-column forward word')
 for i in range(0,len(ops),2):replay[ops[i]]^=replay[ops[i+1]]
 need(replay==identity,'all-column pure phase inverse')
 raw=ops.tobytes() if sys.byteorder=='little' else b''.join(int(x).to_bytes(4,'little') for x in ops)
 return {'field_dimension':len(a),'binary_dimension':n,'ADD_per_direction':len(ops)//2,'elimination_word_uint32le_sha256':hashlib.sha256(raw).hexdigest()},swapcount
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 new=args.package;old=BASE/'bit-shared-h-s031-construction/native-d1509-all-native/output'
 base_review=BASE/'bit-shared-h-s031-construction/native-d1509-all-native/review-b-compiler/output/RESULT.json';review=rd(base_review)
 for p,digest in review['input_sha256'].items():need(hashlib.sha256((BASE/p).read_bytes()).hexdigest()==digest,'old independent invoice input binding')
 er0,er1=rd(old/'PHASE-COMPILER-RECEIPTS.json.gz'),rd(new/'PHASE-COMPILER-RECEIPTS.json.gz')
 source=rd(new/'SOURCES.json.gz');early=rd(new/'EARLY.json.gz');bill=rd(new/'COMPILER-RESULT.json')
 need(er0['H']==er1['H'],'entire inherited H phase receipt')
 need((old/'H-PHYSICAL.json.gz').read_bytes()==(new/'H-PHYSICAL.json.gz').read_bytes() and (old/'D-WORD.json.gz').read_bytes()==(new/'D-WORD.json.gz').read_bytes(),'unchanged H and D words')
 phase0=sum(2*z['early']['ADD_per_direction'] for z in er0['sources'].values());par0=sum(z['exact_parity_form_ADD'] for z in er0['sources'].values());phase1=par1=0;records=[];beg=time.monotonic()
 for j in sorted(early,key=int):
  a=np.array(early[j]['physical_matrix'],dtype=np.uint8);got,swaps=compile_matrix(a);need(got==er1['sources'][j]['early'],'new source binary word digest/count')
  par=sum(sum(v.bit_count() for v in lift(np.array(P,dtype=np.uint8).reshape(-1,480))) for P in source['late_parities'][j].values())
  expected=er1['sources'][j];need(par==expected['exact_parity_form_ADD'],'exact source parity formation')
  need(expected['cache_bindings']==er0['sources'][j]['cache_bindings'] and expected['actual_late_field_parities']==360 and expected['stationary_parity_bits']==2160 and expected['actual_Y_injection_ADD']==2160,'unchanged actual source cache lifetimes')
  phase1+=2*got['ADD_per_direction'];par1+=par;records.append({'source':int(j),'early':got,'three_ADD_swaps':swaps,'parity_form_ADD':par});print('INDEPENDENT_NEW_SOURCE_COMPILER',j,got['ADD_per_direction'],par,round(time.monotonic()-beg,2),flush=True)
 delta=8*(phase1-phase0+par1-par0);total=review['fullbank_ADD']+delta
 need(total==bill['fullbank_ADD_including_phase_inverses']==453937608 and delta==9748152,'exact full local changed invoice')
 need(bill['fullbank_INIT']==bill['fullbank_dirty_CLEAR']==review['fullbank_INIT']==279648 and bill['fullbank_extra_field_exports']==16,'no uncharged new field caches')
 result={'status':'PASS_INDEPENDENT_S032_SOURCE_COMPILER_DELTA','fullbank_ADD':total,'incremental_ADD':delta,'fullbank_INIT':279648,'fullbank_dirty_CLEAR':279648,'retained_gap6_field_exports':16,'new_source_phase_words_replayed_forward_and_pure_inverse':11,'changed_source_receipts':records,'inherited_H_D_by_literal_equality':True,'old_independent_review_sha256':hashlib.sha256(base_review.read_bytes()).hexdigest(),'full_global_invoice':False,'new_kappa':False}
 wr(args.out/'RESULT.json',result);print(result['status'],total,delta,flush=True)
if __name__=='__main__':main()

