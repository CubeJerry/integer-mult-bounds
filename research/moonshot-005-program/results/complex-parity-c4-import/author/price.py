#!/usr/bin/env python3
"""Exact whole caller invoices for C4 parity and actual coupled import."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ENGINE='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def main(args):
    if hashlib.sha256(args.engine.read_bytes()).hexdigest()!=ENGINE:raise ValueError('interval engine pin')
    spec=importlib.util.spec_from_file_location('C4_parity_interval',args.engine);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    raw=args.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==FULL,'full caller pin');f=json.loads(raw)
    slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']))
    seed={1:120,2:112,3:88,5:200,8:216};oldparity={1:168,2:288,3:360,5:280,6:8,8:8}
    room=p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,seed))
    penalty=p.moment(p.add((-1,slope)));p.need(penalty[0]>0,'finite-m penalty')
    newbase={1:320,2:112,3:288,4:200,5:200,8:16}
    delta={1:200,3:200,4:200,8:-200};p.need(p.add((1,newbase),(-1,seed))==delta,'complete raw refinement delta')
    records=[]
    for variant in('base','imported'):
        r=json.loads((args.results/variant/'RESULT.json').read_text());one=int(variant=='imported')
        Q={int(k):v for k,v in r['source_bill']['moves'].items()};p.need(Q==p.add((1,newbase),(one,{1:1})),'literal source whole histogram')
        d=p.add((1,delta),(one,{1:1}));margin=p.moment(p.add((1,room),(-1,d)))
        first=next(m for m in range(2,100000)if margin[0]-penalty[1]/(m-1)>0)
        records.append({'variant':variant,'word_sha256':r['word_sha256'],'actual_Q':Q,'delta_from_seed':d,
                        'increment_from_seed':p.moment(d),'limiting_room':margin,'first_positive_fixed_m':first,
                        'current_a_debt':r['current_a_offdiagonal_debt'],'hosted_residual_rank':56})
    refund=p.add((1,oldparity),(-1,newbase));refund_value=p.moment(refund)
    p.need(refund_value[0]>0,'C4 chronology is strictly cheaper than credited parity chronology')
    oldroom=p.moment(p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,oldparity)))
    p.need(oldroom[1]<1 and records[0]['limiting_room'][0]>1 and records[1]['limiting_room'][0]>0,'actual one-rank import fits only after the source refund')
    two_imports=p.moment(p.add((1,room),(-1,delta),(-2,{1:1})))
    p.need(two_imports[1]<0,'two independent extra unit returns exceed this retained base allowance')
    result={'status':'PASS_EXACT_C4_PARITY_AND_REAL_IMPORT_INVOICES','exponent':'199/200','full_caller_sha256':FULL,
            'interval_engine_sha256':ENGINE,'seed_Q':seed,'credited_parity_Q':oldparity,'new_base_Q':newbase,
            'seed_limiting_room':p.moment(room),'old_parity_limiting_room':oldroom,'source_refund_from_old_parity':refund,
            'source_refund_moment':refund_value,'finite_m_penalty':penalty,
            'finite_m_formula':'limiting_room - finite_m_penalty/(m-1), fixed integer m>=2',
            'variants':records,'two_extra_unit_returns_limiting_room':two_imports,
            'scope':'Actual partial sources with complete signed caller movement accounting. Same credited384-term layer, new chronology and a genuine coupled column import. No new kappa.'}
    args.output.write_text(json.dumps(p.enc(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'refund':float(refund_value[0]),'variants':[{'variant':r['variant'],'increment':float(r['increment_from_seed'][0]),'room':float(r['limiting_room'][0]),'m':r['first_positive_fixed_m']}for r in records]},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
