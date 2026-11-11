#!/usr/bin/env python3
"""Exact target gate after granting deletion of the entire paired BIT query layer."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PINS={'research/paired-query-only-bit/EFREE-CALLER.json.gz':'757b3523798f840bdb02028b23708c3416627a99ea09e7a3c4bcdc5cd0c7ce4b','research/paired-query-only-bit/EFREE-RESULT.json':'a46b6c6040f75184cab5467656811ad988c216e3bc8e44d595a5015b6e49620b','research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz':'51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'}
def need(c,m):
 if not c:raise ValueError(m)
def load(root,name):
 raw=(root/name).read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS[name],'source pin '+name)
 return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)
def enclosure(r,D):
 target=r**199*D**200;lo=0;hi=r*D+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 need(lo**200<=target<hi**200,'exact integer power enclosure')
 return F(lo,D),F(hi,D)
def run(root):
 caller=load(root,next(k for k in PINS if 'CALLER' in k));ledger=load(root,next(k for k in PINS if 'RESULT' in k));word=load(root,next(k for k in PINS if 'WORD' in k))
 dims={int(k):v['dim'] for k,v in word['frames'].items()};pn=Counter();tn=Counter()
 for e in word['program']:
  if e[0]=='MOVE':pn[abs(dims[e[2]]-dims[e[3]])]+=1
 need(word['public']==659,'native census')
 for r in range(222,word['public']):tn[abs(dims[word['start'][r]]-dims[word['final'][r]])]+=1
 counts=Counter(e[0] for e in caller['events']);need((counts['LOCAL'],counts['QUERY'],counts['IDLE_ONE'])==(36,4,32),'literal event census')
 n=caller['ports'];need(n==111 and caller['stages']==18,'caller parameters');paid=Counter({r:c*36 for r,c in pn.items()});targets=Counter({r:c*36 for r,c in tn.items()});queries=[]
 for i,e in enumerate(caller['events']):
  if e[0]=='QUERY':paid[1]+=n;queries.append(i)
  elif e[0]=='IDLE_ONE':paid[caller['body_rank']*len(e[2])]+=n
 for e in caller['diagonal']:targets[e['q']+caller['body_rank']*len(e['stages'])]+=n
 need(paid==Counter({int(k):v for k,v in ledger['paid'].items()}),'literal paid profile');need(targets==Counter({int(k):v for k,v in ledger['targets'].items()}),'literal target profile');need(caller['events'][349]==['QUERY',19,20],'proposal occurrence')
 D=2**88;lo=hi=F(0);roots={}
 for r in sorted(set(paid)|set(targets)):
  a,b=enclosure(r,D);roots[str(r)]=[str(a),str(b)];c=targets[r]-paid[r]
  if c<0:a,b=b,a
  lo+=c*a;hi+=c*b
 cases={str(k):[str(lo+k*n),str(hi+k*n)] for k in range(5)}
 need(hi+444<0,'entire query layer insufficient');need(lo+445>0,'445-credit boundary control');need(hi+111+18*18<0 and lo+111+19*18>0,'18-versus19 uniform credits')
 try:need(5<=len(queries),'credit exceeds original query census')
 except ValueError:five_rejected=True
 else:raise ValueError('fifth-query control accepted')
 return {'status':'PASS_ENTIRE_BIT_QUERY_LAYER_TARGET_EXCLUSION','source_pins':PINS,'target_kappa':'1/200','power_exponent':'199/200','power_grid':str(D),'native_paid':dict(sorted(pn.items())),'native_helpers':dict(sorted(tn.items())),'paid':dict(sorted(paid.items())),'targets':dict(sorted(targets.items())),'paid_jobs':sum(paid.values()),'productive_fields':sum(targets.values()),'query_events':queries,'jobs_per_query':111,'actual_queries':4,'native_calls':36,'changed_calls_in_PR7177':18,'margin_intervals_by_free_queries_removed':cases,'remaining_deficit_after_query349':[str(-(hi+111)),str(-(lo+111))],'remaining_deficit_after_all_queries':[str(-(hi+444)),str(-(lo+444))],'minimum_total_unit_credits':445,'minimum_extra_unit_credits_beyond_query349':334,'minimum_uniform_net_unit_credits_per18changed_calls':19,'rank_power_intervals':roots,'controls':{'fifth_original_query_rejected':five_rejected,'444_unit_credits_fail':True,'445_unit_credits_pass_raw_gate_only':True,'18_uniform_net_credits_fail':True,'19_uniform_net_credits_pass_raw_gate_only':True},'scope':'Exact1/200 raw-gate exclusion with native/IDLE/targets fixed, all QUERY costs freely removed and new fees nonnegative. No provider or new kappa; no claim about changed native/targets or a global single crossing.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repository);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:r[k] for k in ['status','query_events','actual_queries','remaining_deficit_after_all_queries','minimum_total_unit_credits','minimum_extra_unit_credits_beyond_query349','scope']},indent=2))
