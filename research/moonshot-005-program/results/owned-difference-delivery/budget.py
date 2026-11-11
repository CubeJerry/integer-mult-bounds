#!/usr/bin/env python3
"""Directed integer-root budget for the conditional ten-MOVE difference rewrite."""
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
NATIVE_PATH='research/shared-wire-split-composition/data/final.json.gz'
NATIVE_PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
INVOICE_PATH='research/shared-core-target-obligations/INVOICE-RESULT.json'
INVOICE_PIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
DEN=10**15

def need(ok,msg):
    if not ok:raise ValueError(msg)
def iroot(n,k):
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x:break
        x=y
    while (x+1)**k<=n:x+=1
    while x**k>n:x-=1
    need(x**k<=n<(x+1)**k,'directed root endpoint')
    return x

def run(native,invoice,certificate):
    nb=native.read_bytes();ib=invoice.read_bytes();cb=certificate.read_bytes()
    need(hashlib.sha256(nb).hexdigest()==NATIVE_PIN,'native pin')
    need(hashlib.sha256(ib).hexdigest()==INVOICE_PIN,'invoice pin')
    need(hashlib.sha256(ib+b'\n').hexdigest()!=INVOICE_PIN,'invoice-corruption control')
    w=json.loads(gzip.decompress(nb));a=json.loads(ib);c=json.loads(cb)
    own=Counter(abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])) for e in w['program'] if e[0]=='MOVE' and e[1]>=w['public'])
    need(own=={1:20,2:9,3:2,4:13,5:2,6:1},'source owned profile')
    seen=set();saved=Counter()
    for x in c['witnesses']:
        j=x['before_event'];need(j not in seen,'duplicate saved event');seen.add(j)
        e=w['program'][j];need(e==x['move'] and e[0]=='MOVE' and e[1]>=w['public'],'saved source event')
        r=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));need(r==x['rank'],'saved source rank');saved[r]+=1
    need(saved=={1:6,2:1,3:1,4:1,6:1},'ten-event profile')
    targets={int(k):v for k,v in a['T4'].items()};paid={int(k):v for k,v in a['P4'].items()}
    for r in set(own)|set(saved):paid[r]=paid.get(r,0)+18*(own.get(r,0)-saved.get(r,0))
    q={r:iroot(r**199*DEN**200,200) for r in set(targets)|set(paid)}
    def moment(h):return sum(n*q[r] for r,n in h.items()),sum(n*(q[r]+1) for r,n in h.items())
    tl,th=moment(targets);pl,ph=moment(paid);sl,sh=moment(saved);ol,oh=moment(own)
    lo,hi=tl-ph,th-pl
    need(lo>0 and 7*18*DEN<lo<hi<8*18*DEN,'strict residual paid allowance')
    base_lo,base_hi=int(a['M4_numerator_bounds'][0])-18*oh,int(a['M4_numerator_bounds'][1])-18*ol
    need(base_hi<0,'omitting ten savings must fail target')
    need(lo-18*8*DEN<0 and hi-18*8*DEN<0,'eight extra rank-one arrivals must fail')
    seed_events=[25489,25666,25688,25711,25716,25719,25721,25724,25725]
    seed=Counter()
    for j in seed_events:
        e=w['program'][j];need(e[0]=='MOVE' and e[1]<w['public'],'seed delivery source helper MOVE')
        seed[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
    need(seed=={1:8,2:1},'nine-arrival prefix profile')
    dl,dh=moment(seed);composed_lo,composed_hi=lo-18*dh,hi-18*dl
    need(composed_hi<0,'naive initial-prefix-plus-ten-skip invoice must fail')
    return {'status':'PASS_CONDITIONAL_OWNED_DIFFERENCE_REPAIR_BUDGET','source_sha256':NATIVE_PIN,'invoice_sha256':INVOICE_PIN,
      'certificate_sha256':hashlib.sha256(cb).hexdigest(),'exponent':'199/200','denominator':str(DEN),'removed_per_native':dict(saved),
      'saved_moment_numerator_bounds':[str(sl),str(sh)],'new_T':targets,'new_P':paid,'new_paid_count':sum(paid.values()),
      'productive_count':sum(targets.values()),'rank_surplus':sum(r*n for r,n in targets.items())-sum(r*n for r,n in paid.items()),
      'new_margin_numerator_bounds':[str(lo),str(hi)],'additional_per_native_paid_headroom':{'numerator_bounds':[str(lo),str(hi)],'denominator':str(18*DEN),'new_rank_one_moves_upper':7},
      'virtual_reconstruction_terms':sum(len(x['witness']) for x in c['witnesses']),
      'naive_nine_arrival_composition_control':{'source_events':seed_events,'added_per_native':dict(seed),'cost_numerator_bounds':[str(dl),str(dh)],'margin_numerator_bounds':[str(composed_lo),str(composed_hi)],'scope':'A literal invoice union with these nine added helper routes fails; no universal exclusion of recoded or further-shared constructions.'},
      'controls':['source/invoice pins','distinct exact source occurrences','omitting savings gives negative raw target margin','eight extra rank-one arrivals make target margin negative','nine-arrival initial prefix cannot simply be unioned with remaining duplicated-owned profile'],
      'scope':'Conditional paid-profile arithmetic. Physical current-cochart differences, scalar/lifecycle tariff, source-wide native, uniform compiler and compatible BIT remain unbuilt; no new kappa.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--invoice',type=Path);p.add_argument('--certificate',type=Path)
    z=p.parse_args();here=Path(__file__).resolve()
    locate=lambda name:next((d/name for d in here.parents if (d/name).is_file()),None)
    native=z.source or locate(NATIVE_PATH);invoice=z.invoice or locate(INVOICE_PATH);cert=z.certificate or here.with_name('CERTIFICATE.json')
    need(native is not None and invoice is not None,'run inside repository or pass --source and --invoice')
    print(json.dumps(run(native,invoice,cert),indent=2,sort_keys=True))
