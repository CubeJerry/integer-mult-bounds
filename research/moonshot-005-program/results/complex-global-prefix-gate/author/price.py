#!/usr/bin/env python3
"""Directed complete-caller screens with an explicit extra-mode route premise."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ENGINE='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
CALLER='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'

def main(args):
    if hashlib.sha256(args.engine.read_bytes()).hexdigest()!=ENGINE:
        raise ValueError('interval engine pin')
    spec=importlib.util.spec_from_file_location('global_prefix_intervals',args.engine)
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    raw=args.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==CALLER,'complete caller pin')
    full=json.loads(raw)
    slope=p.add((p.F(1,18),full['invoice']['T']),(p.F(-1,18),full['invoice']['P']))
    seed={1:120,2:112,3:88,5:200,8:216}
    room_profile=p.add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']),(-1,seed))
    room=p.moment(room_profile)
    penalty=p.moment(p.add((-1,slope)))
    p.need(penalty[0]>0,'strict fixed-m penalty')
    facet={1:1,7:1,8:-1}
    p.need(p.moment(facet)[0]>0,'positive but small raw facet-stop tariff')
    scenarios=[]
    specifications=[
        ('full_rank8_new_mode_and_79_raw_facet_stops',p.add((1,{8:1}),(79,facet)),
         'Necessary increment only under all hypotheses of PROOF.md section 6. Every other new expense is granted free.'),
        ('rank7_new_mode_and_79_raw_facet_stops',p.add((1,{7:1}),(79,facet)),
         'Boundary tariff screen, not a construction or universal lower bound for proper-born acquisition. Shows the rank8 premise cannot be dropped.'),
        ('eight_global_modes_and_88_raw_facet_stops',p.add((88,facet)),
         'Boundary tariff screen. Eight-mode completion needs104 exceptions; sixteen existing mode arrivals are granted free. Actual source compilation remains open.'),
        ('all200_XB_5plus3_all104_Y_extra_stop_all16_mode_flags',
         p.add((200,{5:1,3:1,8:-1}),(104,{2:1,3:1,5:-1}),(16,{2:1,1:6,8:-1})),
         'Sufficient envelope if the stated monotone shapes exist and all other changes cost no more. Not a construction or lower bound on every architecture.'),
        ('all200_XB_5plus3_all200_YD_extra_stop_all16_mode_flags',
         p.add((200,{5:1,3:1,8:-1}),(200,{2:1,3:1,5:-1}),(16,{2:1,1:6,8:-1})),
         'Same sufficient envelope including all96 D extra stops. Failure does not exclude cheaper shapes or refunds.')]
    for name,increment,scope in specifications:
        margin=p.moment(p.add((1,room_profile),(-1,increment)))
        first=next((m for m in range(2,100000) if margin[0]-penalty[1]/(m-1)>0),None) if margin[0]>0 else None
        scenarios.append({'name':name,'new_minus_seed_profile':increment,'increment':p.moment(increment),
                          'limiting_margin':margin,'first_positive_fixed_m_for_this_screen':first,'scope':scope})
    p.need(scenarios[0]['limiting_margin'][1]<0,'narrow full-route family fails at every fixed m')
    p.need(scenarios[1]['limiting_margin'][0]>0,'proper-born rank7 tariff remains unexcluded')
    p.need(scenarios[2]['limiting_margin'][0]>0,'eight-mode changed-decoder tariff remains unexcluded')
    pivot_refund={1:1,2:1,3:-1}
    deficit=p.moment(p.add((1,specifications[0][1]),(-1,room_profile)))
    refund=p.moment(pivot_refund)
    minimum_pivot_refunds=next(n for n in range(1,113) if n*refund[0]>deficit[1])
    p.need(minimum_pivot_refunds==27 and 26*refund[1]<deficit[0], 'exact conditional pivot-refund count')
    out={'status':'PASS_SCOPED_GLOBAL_PREFIX_SIGNED_INVOICES','target_exponent':'199/200',
         'full_caller_sha256':CALLER,'interval_engine_sha256':ENGINE,'seed_Q':seed,
         'seed_limiting_room':room,'finite_m_penalty_coefficient':penalty,
         'finite_m_formula':'limiting margin - positive penalty/(m-1), fixed integer m>=2',
         'raw_rank8_facet_stop_increment':p.moment(facet),'scenarios':scenarios,
         'full_rank8_route_minimum_refund_owed':deficit,
         'refund_per_deleted_raw_pivot_1plus2_to3':refund,
         'minimum_such_pivot_refunds_before_any_other_new_expense':minimum_pivot_refunds,
         'refund_warning':'Twenty-seven is arithmetic only. No compatible decoder deleting these stops is constructed. All other new costs remain.',
         'scope':'Rigorous rational enclosures for source-specific movement screens. No physical construction, supplier certificate or new kappa.'}
    args.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'seed_room':float(room[0]),'facet_increment':float(p.moment(facet)[0]),
                      'scenarios':[{'name':s['name'],'increment':float(s['increment'][0]),'margin':float(s['limiting_margin'][0]),'first_m':s['first_positive_fixed_m_for_this_screen']}for s in scenarios],
                      'minimum_pivot_refunds':minimum_pivot_refunds},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
