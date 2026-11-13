#!/usr/bin/env python3
"""Directed integer-power complete seventeen-call .0038 budgets."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from decimal import Decimal,localcontext
from functools import lru_cache
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DEN=10**24
CERTS={}
def need(ok,label):
    if not ok:raise ValueError(label)
@lru_cache(None)
def price(r):
    need(isinstance(r,int) and 1<=r<=137,'rank price domain')
    scaled=r**4981*DEN**5000
    with localcontext() as ctx:
        ctx.prec=85;a=int(Decimal(r)**(Decimal(4981)/5000)*DEN)
    while a**5000>scaled:a-=1
    while (a+1)**5000<=scaled:a+=1
    need(a**5000<=scaled<(a+1)**5000,'exact directed integer-power bracket')
    b=a if a**5000==scaled else a+1;CERTS[r]={'lower':a,'upper':b,'denominator':DEN,'identity':'f(r)^5000=r^4981'}
    return Q(a,DEN),Q(b,DEN)
def moment(profile):
    lo=hi=Q(0)
    for r,n in profile.items():
        if n:
            a,b=price(int(r));lo+=n*(a if n>0 else b);hi+=n*(b if n>0 else a)
    return lo,hi
def display(v):
    with localcontext() as ctx:
        ctx.prec=40;dec=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in v]
    return {'exact':list(map(str,v)),'decimal_display_only':dec}
def main():
    pins={}
    def load(path,expected):
        b=(ROOT/path).read_bytes();pins[path]=sha256(b).hexdigest();need(pins[path]==expected,'pinned budget input');return json.loads(b)
    data=json.loads((HERE/'RESULT.json').read_bytes());need(data['status']=='COMPLETE_SIX_SINGLE_RANK1_ZERO_PROMISE_CENSUS','all six complete before pricing')
    caller=load('reference/pr7481/CALLER-EXACT.json','255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc');copies=sum(e[0]=='J' for e in caller['events']);need(copies==caller['stages']==17,'actual17nativecalls')
    iv=load('reference/pr7481/producer54/validation_signed/adapted/CURRENT-PRICE.json','86f71ccbc923db5d7a6753aa971c3a9c8a572680534498ed17be072cfa2aae6b');need(iv['new_native']==data['source_payload_sha256'],'full invoice native payload')
    base=Counter({int(r):n for r,n in iv['after']['T'].items()});base.subtract({int(r):n for r,n in iv['after']['P'].items()});base_iv=moment(base);required=(-base_iv[1]/copies,-base_iv[0]/copies)
    cases=[]
    for c in data['cases']:
        native={int(r):n for r,n in c['native_gain_profile'].items()};gain=moment(native);whole=base.copy();whole.update({r:copies*n for r,n in native.items()});full=moment(whole)
        cases.append({'helper':c['helper'],'zero_MOVE_events':c['zero_MOVE_events'],'new_nonzero_cache_events':c['new_nonzero_cache_events'],'all_credited_events':c['eligible_MOVE_events_union'],'credit_histogram':c['credit_histogram'],'lost_original_target_rank':1,'native_gain_profile':native,'native_gain':display(gain),'complete17call_optimistic_moment':display(full),'optimistic_complete_0038_positive':full[0]>0,'optimistic_complete_0038_negative':full[1]<0})
    out={'status':'COMPLETE_DIRECTED_INTEGER_POWER_SIX_HELPER_BUDGETS','source_sha256':data['source_sha256'],'input_sha256':pins,'kappa':'19/5000','native_calls':copies,'baseline_moment':display(base_iv),'required_native_gain':display(required),'cases':cases,'price_certificates':CERTS,'scope':'Optimistic moments only. Zero input preparation grants no new paid jobs; all ordinary work, owned lifetimes, public zero-reframe and actual cache implementation remain unresolved and free in this upper budget. No physical or kappa success is inferred.'}
    (HERE/'BUDGET.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'cases':[{'helper':c['helper'],'native_gain':c['native_gain']['decimal_display_only'],'full':c['complete17call_optimistic_moment']['decimal_display_only'],'positive':c['optimistic_complete_0038_positive']} for c in cases]},indent=2))
if __name__=='__main__':main()
