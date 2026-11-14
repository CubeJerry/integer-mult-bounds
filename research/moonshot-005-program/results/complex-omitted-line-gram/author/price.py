#!/usr/bin/env python3
"""Complete fixed-m movement bridge for the actual omitted-line source."""
import argparse,json,hashlib,importlib.util,sys
from pathlib import Path

def main(a):
 sp=importlib.util.spec_from_file_location('duplex_moments',a.engine);p=importlib.util.module_from_spec(sp);sys.modules[sp.name]=p;sp.loader.exec_module(p);p.need(hashlib.sha256(a.engine.read_bytes()).hexdigest()=='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1','directed moment engine');raw=a.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==p.FULL,'full caller source');f=json.loads(raw);r=json.loads(a.receipt.read_text());slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']));Q=r['source_bill']['moves'];room=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,Q)));penalty=p.moment(p.add((-1,slope)))
 def bounds(delta):
  lo,hi=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,Q),(-1,delta)))
  m=next((m for m in range(2,100000) if lo-penalty[1]/(m-1)>0),None) if lo>0 else None
  return {'extra_profile':delta,'extra_moment':p.moment(delta),'limiting_room':[lo,hi],'first_m_positive_certified':m,'at_first_m':[lo-penalty[1]/(m-1),hi-penalty[0]/(m-1)] if m else None}
 models={'literal_seed':bounds({}),'all200_XB_at_most3_legs':bounds({2:200,3:400,8:-200}),'all200_XB_legs5_2_1':bounds({1:200,2:200,5:200,8:-200}),'all200_XB_legs5_3':bounds({3:200,5:200,8:-200}),'XB_521_plus_oneextra_stop_eachY':bounds({1:200,2:304,3:104,5:96,8:-200}),'XB_53_plus_oneextra_stop_eachY':bounds({2:104,3:304,5:96,8:-200})}
 out={'status':'PASS_COMPLETE_FIXED_M_DUPLEX_SEED_INVOICE','native_sha256':r['native_sha256'],'word_sha256':r['word_sha256'],'full_sha256':p.FULL,'target_exponent':'199/200','actual_Q':Q,'finite_m_penalty':penalty,'models':models,'scope':'Literal seed is partial. Other rows are sufficient movement envelopes only if one compatible complete compiler meets their full source, route and cache premises; no such compiler is supplied. Every additional owner MOVE, Y refinement, reverse source cost and physical/compiler duty remains charged.'};a.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n');print(json.dumps({k:{'limit':float(v['limiting_room'][0]),'first_m':v['first_m_positive_certified']} for k,v in models.items()},indent=2))
if __name__=='__main__':
 z=argparse.ArgumentParser();z.add_argument('--full',type=Path,required=True);z.add_argument('--engine',type=Path,required=True);z.add_argument('--receipt',type=Path,required=True);z.add_argument('--output',type=Path,required=True);main(z.parse_args())
