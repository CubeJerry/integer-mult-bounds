#!/usr/bin/env python3
"""Complete signed invoices and an oracle bound for disjoint clique sums."""
import argparse,hashlib,importlib.util,json
from pathlib import Path

ENGINE='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def main(args):
    if hashlib.sha256(args.engine.read_bytes()).hexdigest()!=ENGINE:raise ValueError('interval engine pin')
    spec=importlib.util.spec_from_file_location('proper_born_clique_interval',args.engine);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    raw=args.full.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==FULL,'complete caller pin');f=json.loads(raw)
    slope=p.add((p.F(1,18),f['invoice']['T']),(p.F(-1,18),f['invoice']['P']))
    oracle=p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,{8:400}))
    seed={1:120,2:112,3:88,5:200,8:216}
    room=p.add((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,seed))
    penalty=p.moment(p.add((-1,slope)));p.need(penalty[0]>0,'strict finite-m penalty')
    family=[]
    for k in range(2,9):
        # Separate add terms deliberately: at k=8 the terminal rank is1.
        delta=p.add((4*k*(k-1),{1:1}),(4*k,{9-k:1}),(-2*k,{8:1}),(-2*k,{3:1,5:1}),(2,{k:1}))
        margin=p.moment(p.add((1,room),(-1,delta)))
        first=next((m for m in range(2,100000)if margin[0]-penalty[1]/(m-1)>0),None)if margin[0]>0 else None
        record={'size':k,'delta_profile':delta,'increment':p.moment(delta),'limiting_margin':margin,
                'first_positive_fixed_m':first,'status':'exact_general_family_formula'}
        if k in (2,4,8):
            receipt=json.loads((args.results/('k'+str(k))/'RESULT.json').read_text())
            actual={int(r):v for r,v in receipt['source_bill']['moves'].items()}
            p.need(actual==p.add((1,seed),(1,delta)),'actual emitted source profile equals cyclic-clique ledger')
            p.need(receipt['reverse_residual_rank']==96-k,'actual rank reduction')
            record.update({'word_sha256':receipt['word_sha256'],'actual_Q':actual,'status':'actual_full_source_invoice','reverse_residual_rank':96-k})
        family.append(record)
    p.need(all(family[k-2]['limiting_margin'][0]>0 for k in (2,3,4)),'exact favorable retained-source sizes')
    p.need(all(family[k-2]['limiting_margin'][1]<0 for k in (5,6,7,8)),'exact unfavorable retained-source sizes')
    wrong_rank1_bucket=p.add((32,{1:1}),(-16,{8:1}),(-16,{3:1,5:1}),(2,{8:1}))
    p.need(wrong_rank1_bucket!=family[6]['delta_profile'],'reject overwriting rather than adding coincident rank-one buckets at k=8')
    # Cohorts of native nonorthogonal roots have k<=8.  For each cohort with
    # m hosted recipients,2*k^t >=2*m*8^(t-1). Summing m=96 yields24*8^t.
    cohort_lower={8:24}
    global_margin=p.moment(p.add((1,oracle),(-1,cohort_lower)))
    p.need(global_margin[1]<0,'complete disjoint fresh-pair cohort architecture fails even raw oracle')
    out={'status':'PASS_EXACT_PAIRED_CLIQUE_INVOICES_AND_SCOPED_GLOBAL_EXCLUSION','exponent':'199/200',
         'full_caller_sha256':FULL,'interval_engine_sha256':ENGINE,'seed_Q':seed,
         'seed_room':p.moment(room),'finite_m_penalty':penalty,
         'finite_m_formula':'limiting margin - positive penalty/(m-1), fixed integer m>=2',
         'family':family,
         'coincident_terminal_rank1_bucket_negative_control_rejected':True,
         'global_disjoint_clique_screen':{'raw_oracle_profile':{8:400},'allowance_after_raw_oracle':p.moment(oracle),
             'hosted_recipients':96,'maximum_native_clique_size':8,'paired_owned_lower_profile':cohort_lower,
             'paired_owned_lower_moment':p.moment(cohort_lower),'limiting_margin':global_margin,
             'scope':'Disjoint cyclic clique-sum replacements with fresh forward and reverse sum transport between each clique plane and chart0. Old Gram mode expenses are entirely refunded; every raw field is granted one direct rank8 movement; coupled entry and all other work are free. Shared payload histories or different receiver geometries are not excluded.'},
         'scope':'Movement only, with complete caller substitution and explicit refunds. Dirty owned erasure, scalar/precision/uniform supplier foundations remain. No new kappa.'}
    args.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'family':[{'k':r['size'],'increment':float(r['increment'][0]),'margin':float(r['limiting_margin'][0]),'first_m':r['first_positive_fixed_m']}for r in family],
                      'raw_oracle_allowance':float(p.moment(oracle)[0]),'global_paired_lower':float(p.moment(cohort_lower)[0]),'global_margin':float(global_margin[0])},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
