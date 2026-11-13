#!/usr/bin/env python3
"""Exact fixed-m and limiting moment allowances, with full helper-credit loss."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mcopy',HERE/'build_mcopy.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def main(a):
    raw=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes()
    b.need(hashlib.sha256(raw).hexdigest()==b.FULL_PIN,'Complete caller source pin')
    full=json.loads(raw)
    T,P=[{int(k):v for k,v in full['invoice'][x].items()} for x in ['T','P']]
    H,N=[{int(k):v for k,v in full['native'][x].items()} for x in ['helpers','paid']]
    M=b.moment({k:T.get(k,0)-P.get(k,0) for k in set(T)|set(P)})
    GH=b.moment({k:N.get(k,0)-b.RAW.get(k,0)-H.get(k,0) for k in set(N)|set(b.RAW)|set(H)})
    d=(-M[1]/18,-M[0]/18);limit=(GH[0]-d[1],GH[1]-d[0])
    b.need(d[0]>0,'Selected caller has a strict target deficit')
    rows=[]
    for m in [2,3,4,5,8,16,32,64]:
        allowance=(limit[0]-d[1]/(m-1),limit[1]-d[0]/(m-1))
        rows.append({'copies':m,'extra_moment_allowance':allowance,'decimal':float(allowance[0])})
    receipt=json.loads((a.output/'PURE-RAIL-RESULT.json').read_text())
    word=(a.output/'rail-repaired.json.gz').read_bytes()
    b.need(hashlib.sha256(word).hexdigest()==b.RAIL_PIN==receipt['word_sha256'],'Actual rail identity')
    Q={int(k):v for k,v in receipt['ordinary_bill']['moves'].items()}
    c=b.moment({k:Q.get(k,0)-b.RAW.get(k,0) for k in set(Q)|set(b.RAW)})
    # Dropping the helper-target loss would grant an additional positive H moment.
    Hmoment=b.moment(H)
    b.need(Hmoment[0]>0,'Omitted helper-credit loss must change the invoice')
    result={'status':'PASS_EXACT_MULTIPLICITY_BUDGET','exponent':'199/200','full_caller_pin':b.FULL_PIN,
      'rail_pin':b.RAIL_PIN,'selected_M':M,'per_native_selected_deficit':d,'G_minus_H_moment':GH,
      'strict_limit':limit,'rows':rows,'current_rail_extra_moment':c,
      'current_rail_limit_remaining':(limit[0]-c[1],limit[1]-c[0]),
      'strict_allocation_rule':'c < limit and m-1 > deficit/(limit-c), for exact symbolic quantities.',
      'omitted_helper_loss_overcredit_bounds':Hmoment,'complete_supplier':False,
      'scope':'Exact complete conditional recursive-moment arithmetic. No missing endpoints or physical services are waived.'}
    (a.output/'MULTIPLICITY-BUDGET.json').write_text(json.dumps(b.clean(result),indent=2)+'\n')
    print(result['status'],float(limit[0]),float(limit[0]-c[1]))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);main(parser.parse_args())
