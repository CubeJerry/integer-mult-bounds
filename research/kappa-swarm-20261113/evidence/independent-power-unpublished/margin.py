#!/usr/bin/env python3
"""Standalone exact-power full .0038 margin; does not import budget_price."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from fractions import Fraction as Q
import argparse,gzip,json,time
import powers as P
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
def run(output):
    start=time.monotonic();pins={}
    def load(path,zipped=False):
        b=(ROOT/path).read_bytes();pins[path]=sha256(b).hexdigest();return json.loads(gzip.decompress(b) if zipped else b)
    w=load('reference/pr7481/WORD.json.gz',True);P.need(pins['reference/pr7481/WORD.json.gz']=='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9','native pin')
    caller=load('reference/pr7481/CALLER-EXACT.json');P.need(pins['reference/pr7481/CALLER-EXACT.json']=='255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc','exact caller bytes')
    calls=sum(e[0]=='J' for e in caller['events']);P.need(calls==caller['stages']==17,'actual17copies')
    ip='reference/pr7481/producer54/validation_signed/adapted/CURRENT-PRICE.json';iv=load(ip);P.need(pins[ip]=='86f71ccbc923db5d7a6753aa971c3a9c8a572680534498ed17be072cfa2aae6b','invoice pin')
    payload=sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest();P.need(payload==iv['new_native'],'invoice native payload')
    T={int(r):c for r,c in iv['after']['T'].items()};A={int(r):c for r,c in iv['after']['P'].items()};base={r:T.get(r,0)-A.get(r,0) for r in T.keys()|A.keys()}
    F={5:1,3:1,1:2,4:-2};profile={r:base.get(r,0)+calls*F.get(r,0) for r in base.keys()|F.keys()};full=P.moment(profile);threshold=-Q(252581,10000)
    P.need(full[1]<threshold,'full integer-power margin below-25.2581')
    wrong_count=P.moment({r:base.get(r,0)+18*F.get(r,0) for r in base.keys()|F.keys()});P.need(wrong_count[0]>threshold,'18copies mutation must fail threshold')
    badF={5:1,3:1,1:2,4:2};wrong_sign=P.moment({r:base.get(r,0)+calls*badF.get(r,0) for r in base.keys()|badF.keys()});P.need(wrong_sign[0]>0,'wrong target sign must fail')
    cert=P.CERTIFICATES[4];N=pow(4,4981)*P.DP;P.need(pow(cert['lower_numerator']+1,5000)>N,'incorrect lower price bound rejected')
    out=dict(status='PASS_INDEPENDENT_INTEGER_POWER_FULL_MARGIN',kappa='19/5000',price_identity='f(r)^5000=r^4981',input_sha256=pins,native_payload_sha256=payload,
        native_calls=calls,upper_envelope_profile=F,baseline=P.display(P.moment(base)),native_envelope=P.display(P.moment(F)),full=P.display(full),threshold=str(threshold),
        threshold_slack=P.display((threshold-full[1],threshold-full[0])),integer_price_certificates=[P.CERTIFICATES[r] for r in sorted(P.CERTIFICATES)],
        controls=dict(wrong18copies_rejected=True,wrong_target_sign_rejected=True,wrong_price_bracket_rejected=True),seconds=time.monotonic()-start,
        scope='Fixed .0038 upper-envelope price only. No budget_price import; Decimal is a seed, all signs use integer-power certified rational bounds. Envelope is not achievable kappa or physical supplier.')
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['input_sha256','integer_price_certificates']},indent=2))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=HERE/'MARGIN.json');x=a.parse_args();run(x.output)
