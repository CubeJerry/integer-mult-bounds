#!/usr/bin/env python3
"""Signed complete-caller invoice for each actual funded-prefix source."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
PIN='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
def main(a):
 if hashlib.sha256(a.engine.read_bytes()).hexdigest()!=PIN:raise ValueError('interval engine pin')
 spec=importlib.util.spec_from_file_location('funded_prefix_interval_engine',a.engine);p=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p;spec.loader.exec_module(p)
 data=a.full.read_bytes();p.need(hashlib.sha256(data).hexdigest()==p.FULL,'full caller source pin');f=json.loads(data);r=json.loads(a.receipt.read_text());slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']));Q=r['source_bill']['moves'];room=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,Q)));penalty=p.moment(p.add((-1,slope)));m=next((m for m in range(2,100000)if room[0]-penalty[1]/(m-1)>0),None)if room[0]>0 else None
 source_seed={1:120,2:112,3:88,5:200,8:216};delta=p.add((1,Q),(-1,source_seed));out={'status':'PASS_ACTUAL_FUNDED_PREFIX_COMPLETE_SIGNED_MOVEMENT_INVOICE','mode':r['mode'],'word_sha256':r['word_sha256'],'full_caller_sha256':p.FULL,'target_exponent':'199/200','actual_Q':Q,'actual_new_minus_seed_profile':delta,'new_minus_seed_moment':p.moment(delta),'limiting_room':room,'finite_m_penalty':penalty,'first_positive_fixed_m':m,'at_first_m':[room[0]-penalty[1]/(m-1),room[1]-penalty[0]/(m-1)]if m else None,'scope':'Positive margin for this actual partial source only. All remaining endpoints, scalar/ordinary/precision/compiler services, compatible strict suppliers and foundational assumptions remain.'};a.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n');print(json.dumps({'mode':r['mode'],'increment':float(out['new_minus_seed_moment'][0]),'limit':float(room[0]),'first_m':m},indent=2))
if __name__=='__main__':
 z=argparse.ArgumentParser();z.add_argument('--full',type=Path,required=True);z.add_argument('--engine',type=Path,required=True);z.add_argument('--receipt',type=Path,required=True);z.add_argument('--output',type=Path,required=True);main(z.parse_args())
