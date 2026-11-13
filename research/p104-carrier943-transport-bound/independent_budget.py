#!/usr/bin/env python3
"""Read-only integer-power certification of the carrier943 charged budget.

The rational log/Taylor engine proposed SEEDS only. This module imports no
price engine and accepts endpoints only after direct integer inequalities.
"""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
from decimal import Decimal,localcontext
import argparse,json
DEN=10**24
INVOICE_SHA='86f71ccbc923db5d7a6753aa971c3a9c8a572680534498ed17be072cfa2aae6b'
CALLER_SHA='255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc'
NATIVE_PAYLOAD_SHA='64fca675b91298868e12f09423b47e0c2327cba7095e35c8919c1953b4ed68b8'
JOINT_INVOICE_VERIFICATION='509baf4514966e4202cfdde379d7adf3085b1cc7'
SEED_ENGINE_SHA='527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb'
SEEDS={1: 1000000000000000000000000, 2: 1994739013082031402569607, 3: 2987501926082327072487717, 4: 3978983730311476647000136, 5: 4969513998807656612904725, 6: 5959286643614129034493265, 7: 6948429692266991257661147, 8: 7937034079270974725608699, 9: 8925167758345614051244775, 16: 15832311526083433921474011, 17: 16817956137672100277947626, 24: 23711904599203106448634941, 25: 24696069384345265691466911, 32: 31581329468346939456575370, 33: 32564437956870624497494194, 40: 39443201965950548594990014, 41: 40425488635599349542494180, 48: 47299061178509685935753346, 49: 48280675188377554828545565, 56: 55149923264941441208124988, 57: 56130967917583110586422217, 64: 62996509975508849504481274, 65: 63977061066141697365554049, 73: 71819476180879423475459646, 137: 134462452743412001454458486}
def need(ok,label):
    if not ok:raise ValueError(label)
def certify_bracket(rank,lower,upper):
    need(isinstance(rank,int) and rank>0 and isinstance(lower,int) and isinstance(upper,int) and 0<lower<=upper,'positive bracket domain')
    target=pow(rank,4981)*pow(DEN,5000)
    need(pow(lower,5000)<=target,'invalid lower integer-power bound')
    need(target<=pow(upper,5000),'invalid upper integer-power bound')
    return Q(lower,DEN),Q(upper,DEN)
def display(interval):
    with localcontext() as ctx:
        ctx.prec=45;values=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in interval]
    return {'exact':list(map(str,interval)),'decimal_display_only':values}
def verify(invoice_path,caller_path=None):
    """Return a deterministic receipt; read supplied files only, write nothing.

    If caller_path is omitted,17 copies are explicitly INHERITED from the
    pinned joint invoice verification. If supplied, exact bytes and17 J events
    are independently checked as well.
    """
    raw=Path(invoice_path).read_bytes();need(sha256(raw).hexdigest()==INVOICE_SHA,'exact CURRENT-PRICE source bytes');invoice=json.loads(raw)
    need(invoice['new_native']==NATIVE_PAYLOAD_SHA,'invoice native payload')
    target={int(r):n for r,n in invoice['after']['T'].items()};paid={int(r):n for r,n in invoice['after']['P'].items()}
    need(all(isinstance(n,int) and n>=0 for n in list(target.values())+list(paid.values())),'integer nonnegative invoice counts')
    ranks=set(target)|set(paid)|{1,4,8};need(ranks==set(SEEDS),'complete invoice and delta rank coverage')
    prices={};certificates=[]
    for r in sorted(ranks):
        a=SEEDS[r];b=a+1
        # Exact integral prices may use a point bracket, after proof by powers.
        if pow(a,5000)==pow(r,4981)*pow(DEN,5000):b=a
        prices[r]=certify_bracket(r,a,b)
        certificates.append({'rank':r,'lower_numerator':a,'upper_numerator':b,'denominator':DEN,'lower_power_le_scaled_rank_power':True,'upper_power_ge_scaled_rank_power':True})
    calls=17;caller_checked=False
    if caller_path is not None:
        b=Path(caller_path).read_bytes();need(sha256(b).hexdigest()==CALLER_SHA,'exact caller bytes');caller=json.loads(b)
        need(sum(e[0]=='J' for e in caller['events'])==caller['stages']==calls,'actual17nativecalls');caller_checked=True
    def moment(profile):
        low=high=Q(0)
        for r,c in profile.items():
            if c:
                a,b=prices[r];low+=c*(a if c>0 else b);high+=c*(b if c>0 else a)
        return low,high
    base={r:target.get(r,0)-paid.get(r,0) for r in ranks};delta={8:1,1:-1,4:-1}
    M=moment(base);native=moment(delta);combined={r:base.get(r,0)+calls*delta.get(r,0) for r in ranks};charged=moment(combined)
    separated=(M[0]+calls*native[0],M[1]+calls*native[1])
    need(separated[0]<=charged[0]<=charged[1]<=separated[1],'direct and separated directed sums agree')
    need(charged[1]<0 and separated[1]<0,'strictly negative M+17(f8-f1-f4)')
    controls={}
    for label,a,b in [('raised_lower',SEEDS[4]+1,SEEDS[4]+2),('lowered_upper',SEEDS[4]-1,SEEDS[4])]:
        try:certify_bracket(4,a,b)
        except ValueError as error:controls[label]=str(error)
        else:raise ValueError('perturbed bracket was accepted: '+label)
    return {'status':'PASS_INDEPENDENT_INTEGER_POWER_CARRIER943_BUDGET','kappa':'19/5000','price_identity':'f(r)^5000=r^4981','denominator':DEN,'invoice_sha256':INVOICE_SHA,'native_payload_sha256':NATIVE_PAYLOAD_SHA,'joint_invoice_verification_commit':JOINT_INVOICE_VERIFICATION,'caller_sha256':CALLER_SHA,'native_calls':calls,'caller_bytes_independently_checked':caller_checked,'call_count_inheritance':'17 native invocations inherited from the pinned joint invoice verification; supplied caller bytes independently authenticate the count.','seed_engine_sha256_provenance_only':SEED_ENGINE_SHA,'rank_brackets':certificates,'signed_invoice_profile':{r:c for r,c in base.items() if c},'native_delta_profile':delta,'M':display(M),'native_delta':display(native),'charged_direct':display(charged),'charged_separated':display(separated),'strict_negative_margin':display((-charged[1],-charged[0])),'perturbed_bracket_controls':controls,'scope':'Price/invoice arithmetic only. Carrier delta applicability, actual source/supplier admission, physical return/stock, all-column and all other foundational obligations remain open; no new physical or kappa claim.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('invoice',type=Path);p.add_argument('--caller',type=Path);a=p.parse_args();print(json.dumps(verify(a.invoice,a.caller),sort_keys=True,indent=2))
