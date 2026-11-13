#!/usr/bin/env python3
"""Exact cancellation gate; no floating pricing or source construction."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def need(ok,label):
    if not ok:raise ValueError(label)
def main():
    result=json.loads((HERE/'RESULT.json').read_bytes())
    need(result['source_sha256']=='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9','source pin')
    need(result['eligible_MOVE_events_union']==[40710] and result['zero_MOVE_events']==[],'complete candidate census')
    gain=Counter({int(r):v for r,v in result['credit_histogram'].items()});gain.subtract({1:1,8:1});gain={r:v for r,v in gain.items() if v}
    need(gain=={1:-1},'f8-f1-f8 exact cancellation')
    raw=(ROOT/'reference/pr7481/CALLER-EXACT.json').read_bytes();pin=sha256(raw).hexdigest();need(pin=='255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc','exact Git caller bytes')
    caller=json.loads(raw);copies=sum(e[0]=='J' for e in caller['events']);need(copies==caller['stages']==17,'actual17copies')
    required=Q('3.48481964025734707307');need(-Q(1)<required,'strict native budget failure')
    out={'status':'EXACT_CANCELLING_BUDGET_EXCLUDES_THIS_ONE_PROMISE','source_sha256':result['source_sha256'],'eligible_MOVE_events':[40710],'paid_credit_profile':{'8':1},'lost_original_target':{'helper':1459,'rank':1},'mandatory_new_transport_lower_cost_profile':{'8':1},'native_upper_gain_profile':gain,'native_upper_gain_exact':'-1','valid_power_interval':'0 <= kappa < 1; f(0)=0','per_native_required_gain_at_0038_as_supplied':str(required),'strict_shortfall_from_supplied_requirement':str(required+1),'unchanged_exact_caller_sha256':pin,'native_copies':copies,'full_call_gain_upper_exact':str(-copies),'pricing_method':'Exact cancellation; preparation path lower bound is separately pinned fixed-history whole-field provenance.'}
    (HERE/'BUDGET.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
