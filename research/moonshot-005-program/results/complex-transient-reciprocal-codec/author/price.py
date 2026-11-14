#!/usr/bin/env python3
"""Exact movement-only arithmetic for actual transient paired source words."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

def main(a):
 if hashlib.sha256(a.interval_engine.read_bytes()).hexdigest()!='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1':raise ValueError('retained directed moment engine pin')
 s=importlib.util.spec_from_file_location('transient_interval_engine',a.interval_engine);p=importlib.util.module_from_spec(s);sys.modules[s.name]=p;s.loader.exec_module(p)
 raw=a.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==p.FULL,'full caller source');f=json.loads(raw)
 slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']));penalty=p.moment(p.add((-1,slope)))
 results=[]
 for name,path in [('parent-codec',a.parent_codec),('reciprocal-alignment',a.balanced),('aligned-codec',a.balanced_codec)]:
  rawr=path.read_bytes();r=json.loads(rawr);Q=r['source_bill']['moves'];room=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,Q)));delta=p.moment({int(k):v for k,v in r['move_delta'].items()});results.append({'source':name,'receipt_sha256':hashlib.sha256(rawr).hexdigest(),'word_sha256':r['word_sha256'],'actual_Q':Q,'limiting_remaining_moment':room,'change_against_its_actual_baseline':delta,'display':{'remaining_limit':float(room[0]),'movement_change':float(delta[0])}})
 blank=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,{8:400})))
 retained=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,{8:400,9:8,1:8})))
 global8=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,{8:400,9:16,1:8})));p.need(global8[1]<0,'sixteen global trips still fail even before source refinement')
 out={'status':'PASS_EXACT_TRANSIENT_CODEC_INVOICE','full_caller_sha256':p.FULL,'interval_engine_sha256':hashlib.sha256(a.interval_engine.read_bytes()).hexdigest(),'target_kappa':'1/200','finite_m_penalty':penalty,'finite_m_room':'limiting room - penalty/(m-1), integer m>=2 fixed independently of input size','sources':results,'optimistic400_direct_raw_limit':blank,'after8_forward_rank9_and8_coupled_rank1':retained,'after8_forward_and8_reverse_rank9_and8_coupled_rank1':global8,'scope':'Actual partial source invoice and necessary optimistic complete budget. Does not price complete reverse acquisition from rank alone. Global coupled source construction, uniformity, ordinary/owned/precision/compiler and strict suppliers remain open.'}
 a.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n');print(json.dumps({'sources':[r['display'] for r in results],'optimistic_complete_global8_margin':float(global8[0])},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--interval-engine',type=Path,required=True);p.add_argument('--parent-codec',type=Path,required=True);p.add_argument('--balanced',type=Path,required=True);p.add_argument('--balanced-codec',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
