#!/usr/bin/env python3
"""Directed full-caller invoice of the actual parity-half source only."""
import argparse,json,hashlib,importlib.util,sys
from pathlib import Path
if __name__=='__main__':
 z=argparse.ArgumentParser();z.add_argument('--full',type=Path,required=True);z.add_argument('--engine',type=Path,required=True);z.add_argument('--receipt',type=Path,required=True);z.add_argument('--output',type=Path,required=True);a=z.parse_args()
 assert hashlib.sha256(a.engine.read_bytes()).hexdigest()=='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
 sp=importlib.util.spec_from_file_location('retained_directed_invoice',a.engine);p=importlib.util.module_from_spec(sp);sys.modules[sp.name]=p;sp.loader.exec_module(p)
 raw=a.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==p.FULL,'full caller pin');f=json.loads(raw);r=json.loads(a.receipt.read_text());Q=r['source_bill']['moves'];slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']));room=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,Q)));penalty=p.moment(p.add((-1,slope)));m=next(m for m in range(2,100000) if room[0]-penalty[1]/(m-1)>0)
 out={'status':'PASS_COMPLETE_FIXED_M_PARITY_HALF_SOURCE_INVOICE','word_sha256':r['word_sha256'],'full_sha256':p.FULL,'native_sha256':r['native_sha256'],'target_exponent':'199/200','actual_Q':Q,'limiting_room':room,'finite_m_penalty':penalty,'first_m_positive_certified':m,'at_first_m':[room[0]-penalty[1]/(m-1),room[1]-penalty[0]/(m-1)],'at_previous_m':[room[0]-penalty[1]/(m-2),room[1]-penalty[0]/(m-2)],'scope':'Complete movement invoice of the actual partial source; includes all public, reverse, forward, coupled-entry and anchor-owner moves. Source endpoints remain incomplete, all physical/compiler/uniformity foundations remain; no supplier admission or kappa.'};a.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n');print(out['status'],float(room[0]),m)
