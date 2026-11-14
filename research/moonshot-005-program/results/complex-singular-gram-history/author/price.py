#!/usr/bin/env python3
"""Complete signed source invoices for Gram-preserving singular histories."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ENGINE='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def main(args):
    if hashlib.sha256(args.engine.read_bytes()).hexdigest()!=ENGINE:raise ValueError('interval engine pin')
    spec=importlib.util.spec_from_file_location('singular_gram_interval',args.engine);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    raw=args.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==FULL,'full caller pin');f=json.loads(raw)
    slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']))
    seed={1:120,2:112,3:88,5:200,8:216}
    room=p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,seed))
    penalty=p.moment(p.add((-1,slope)));p.need(penalty[0]>0,'finite-m penalty remains strictly positive')
    unit={1:1,3:-1,5:-1,8:1};p.need(p.moment(unit)[0]>0,'every capture/self-return unit has a positive full signed price')
    variants=[]
    for variant in('hybrid','native'):
        r=json.loads((args.results/variant/'RESULT.json').read_text());d=2*r['s']-r['u']
        delta=p.add((d,unit));margin=p.moment(p.add((1,room),(-1,delta)))
        Q={int(k):v for k,v in r['source_bill']['moves'].items()}
        p.need(Q==p.add((1,seed),(1,delta)),'actual source word equals the entire signed route ledger')
        first=next((m for m in range(2,100000)if margin[0]-penalty[1]/(m-1)>0),None)if margin[0]>0 else None
        variants.append({'variant':variant,'word_sha256':r['word_sha256'],'s':r['s'],'u':r['u'],'d':d,
                         'actual_Q':Q,'delta_profile':delta,'increment':p.moment(delta),
                         'limiting_margin':margin,'first_positive_fixed_m':first,
                         'reverse_residual_rank':r['reverse_residual_rank'],'forward_history_rank':r['forward_global_history_rank']})
    p.need(variants[0]['limiting_margin'][0]>0 and variants[1]['limiting_margin'][1]<0,'hybrid feasible and full native frame infeasible in this template')
    # Exact source enumeration and 70 explicit coupled four-set witnesses show
    # u<=3 in an authentic orthogonal eight-frame. With s=8, d>=13.
    native_lower=p.add((13,unit));native_margin=p.moment(p.add((1,room),(-1,native_lower)))
    p.need(native_margin[1]<0,'all-native fixed-fourteen-codec capture template exceeds current room')
    # The continuation is a real L->0 move, and every hosted basis row also has
    # a separate paired 0->L delivery. Neither may disappear from the ledger.
    missing_continuations=p.add((1,variants[0]['delta_profile']),(-variants[0]['s'],{1:1}))
    missing_adjoint=p.add((1,variants[0]['delta_profile']),(-(variants[0]['s']-variants[0]['u']),{1:1}))
    p.need(missing_continuations!=variants[0]['delta_profile']and missing_adjoint!=variants[0]['delta_profile'],'both omission controls change the actual invoice')
    result={'status':'PASS_EXACT_SINGULAR_GRAM_HISTORY_INVOICES','exponent':'199/200',
            'source_pins':{'full_caller':FULL,'interval_engine':ENGINE},'seed_Q':seed,'seed_room':p.moment(room),
            'one_capture_or_adjoint_signed_profile':unit,'one_signed_unit_price':p.moment(unit),
            'finite_m_penalty':penalty,'finite_m_formula':'limiting_margin - positive_penalty/(m-1), fixed integer m>=2',
            'variants':variants,'all_native_frame_template':{'source_max_coupled_intersection':3,'minimum_d':13,
              'minimum_delta_profile':native_lower,'minimum_increment':p.moment(native_lower),'limiting_margin_upper_bound':native_margin,
              'scope':'All eight Gram basis roots are authentic native ports; every actual basis port is captured; all14 remaining mode classes use4 hosted pivots in each reciprocal codec exactly as in the stated compiler. Changed decoders, shared paired continuations, additional local channels and changed native interfaces are not excluded.'},
            'negative_controls':['missing_native_forward_continuation','missing_paired_hosted_self_delivery'],
            'scope':'Whole caller movement accounting and real source refunds, retaining ordinary local/scalar, native, compiler, erasure, precision and recovery foundations. No new kappa.'}
    args.output.write_text(json.dumps(p.enc(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'unit_price':float(p.moment(unit)[0]),'variants':[{'variant':z['variant'],'increment':float(z['increment'][0]),'margin':float(z['limiting_margin'][0]),'m':z['first_positive_fixed_m']}for z in variants]},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
