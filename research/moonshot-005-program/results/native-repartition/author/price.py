#!/usr/bin/env python3
"""Exact whole 18-call invoices under the changed complete native interface."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
ENGINE='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
CALLER='3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e'
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def invoice(caller,native):
    T=Counter();P=Counter();calls=0
    for event in caller['events']:
        if event[0]=='J':
            calls+=1;T.update({int(k):v for k,v in native['helpers'].items()});P.update({int(k):v for k,v in native['paid'].items()})
        else:
            ports=len(caller['types'][event[0]]['ports'])
            if event[1]=='QUERY':P[1]+=ports
            elif event[1]=='IDLE_ONE':P[8*len(event[3])]+=ports
    for data in caller['types'].values():
        for row in data['diagonal']:T[row[0]%2+8*sum(row[2:])]+=len(data['ports'])
    need(calls==18,'actual18 native calls')
    return dict(T),dict(P)
def main(args):
    need(sha(args.engine)==ENGINE and sha(args.full)==FULL and sha(args.caller)==CALLER,'price dependencies pinned')
    sp=importlib.util.spec_from_file_location('allhosted_price_interval',args.engine);p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
    full=json.loads(args.full.read_text());oldcaller=json.loads(args.caller.read_text());oldT,oldP=invoice(oldcaller,full['native'])
    need(oldT=={int(k):v for k,v in full['invoice']['T'].items()}and oldP=={int(k):v for k,v in full['invoice']['P'].items()},'literal original full invoice reproduced')
    oldnet=p.add((1,oldT),(-1,oldP));oldN=full['native']['paid'];oldH=full['native']['helpers']
    oldseed={1:120,2:112,3:88,5:200,8:216};oldroom=p.add((F(1,18),oldnet),(1,oldN),(-1,oldH),(-1,oldseed))
    variants=[];stored={}
    for name in('orthogonal','allhosted'):
        receipt=json.loads((args.results/name/'RESULT.json').read_text());caller=json.loads((args.results/name/'CALLER.json').read_text())
        need(sha(args.results/name/'WORD.json.gz')==receipt['word_sha256']and sha(args.results/name/'CALLER.json')==receipt['caller_sha256'],'converted actual word/caller pins')
        N=receipt['new_native'];T,P=invoice(caller,N);net=p.add((1,T),(-1,P));deltaN=p.add((1,N['paid']),(-1,oldN))
        need(deltaN=={int(k):v for k,v in receipt['additional_paid_profile'].items()},'full native adapter profile')
        outer=p.add((F(1,18),net),(1,N['paid']),(-1,N['helpers']),(-F(1,18),oldnet),(-1,oldN),(1,oldH))
        expectedouter={8:16}if name=='allhosted'else{}
        need(outer==expectedouter,'exact caller outside-native change by hosted cardinality')
        need(p.add((1,net),(-1,oldnet))==({1:-432}if name=='allhosted'else p.add((-18,deltaN))),
             'actual caller cancellation is an exact signed profile identity')
        penalty=p.moment(p.add((-F(1,18),net)));need(penalty[0]>0,'finite-m coefficient positive')
        row={'variant':name,'word_sha256':receipt['word_sha256'],'caller_sha256':receipt['caller_sha256'],
             'T':T,'P':P,'native_N':N['paid'],'native_H':N['helpers'],'additional_native_profile':deltaN,
             'outer_per_call_signed_change':outer,'finite_m_penalty':penalty,
             'complete_baseline_ordinary_upper':receipt['complete_ordinary_invoice']['conservative_total']}
        variants.append(row);stored[name]=(net,N,penalty)
    net,N,penalty=stored['allhosted'];sources=[]
    for name in('gram','parity'):
        r=json.loads((args.results/('allhosted-'+name)/'RESULT.json').read_text());Q={int(k):v for k,v in r['source_bill']['moves'].items()}
        need(sha(args.results/('allhosted-'+name)/'WORD.json.gz')==r['word_sha256'],'actual new partial source pin')
        room=p.add((F(1,18),net),(1,N['paid']),(-1,N['helpers']),(-1,Q));value=p.moment(room)
        need(value[0]>0,'actual all-hosted partial source has positive optimistic allowance')
        first=next(m for m in range(2,100000)if value[0]-penalty[1]/(m-1)>0)
        need(value[1]-penalty[0]/(first-2)<0 if first>2 else True,'preceding fixed m fails')
        sources.append({'variant':name,'word_sha256':r['word_sha256'],'actual_Q':Q,
             'limiting_room_profile':room,'limiting_room':value,'first_positive_fixed_m':first,
             'reverse_residual_rank':r['reverse_residual_rank'],'forward_offdiagonal_debt':r['forward_offdiagonal_debt']})
    neworacle=p.add((F(1,18),net),(1,N['paid']),(-1,N['helpers']),(-1,{8:416}))
    oldoracle=p.add((F(1,18),oldnet),(1,oldN),(-1,oldH),(-1,{8:400}))
    need(neworacle==oldoracle,'promotion creates no raw-field oracle credit: extra outer ranks pay exactly the extra raw fields')
    seedgain=p.add((1,sources[0]['limiting_room_profile']),(-1,oldroom))
    need(seedgain=={1:8,3:-8,5:-8,8:8},'exact all-hosted seed gain after all source and caller expenses')
    paritycost=p.add((1,sources[0]['actual_Q']),(-1,sources[1]['actual_Q']))
    need(paritycost=={1:-208,3:-208,4:-208,8:208},'paired all-hosted C4 cost208 full refinements')
    result={'status':'PASS_EXACT_CHANGED_INTERFACE_WHOLE_CALLER_ACCOUNTING','exponent':'199/200',
       'source_full_receipt_sha256':FULL,'interval_engine_sha256':ENGINE,'complete_conversions':variants,
       'partial_sources':sources,'old_seed_limiting_room':p.moment(oldroom),'allhosted_seed_gain_profile':seedgain,
       'allhosted_seed_gain':p.moment(seedgain),'unchanged_optimistic_raw_oracle_allowance':p.moment(neworacle),
       'finite_m_formula':'R_infinity - finite_m_penalty/(m-1); fixed integer m>=2',
       'finite_m_derivation':{'P_m':'m(P-18N)+18N+18(m-1)Q','T_m':'mT-18(m-1)H'},
       'scope':'Full converted native with unchanged physical foundations. Partial sources have genuine paired endpoint debts; positive room is not a complete supplier or a new kappa.'}
    args.output.write_text(json.dumps(p.enc(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'finite_penalties':{r['variant']:float(r['finite_m_penalty'][0])for r in variants},
        'sources':[{'variant':r['variant'],'room':float(r['limiting_room'][0]),'first_m':r['first_positive_fixed_m']}for r in sources],
        'raw_oracle_allowance':float(p.moment(neworacle)[0])},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--caller',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--results',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);main(p.parse_args())
