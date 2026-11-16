#!/usr/bin/env python3
"""Rational enclosure of every literal MOVE, with exact predecessor delta."""
import argparse,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    path=Path(__file__).with_name('retained')/'interval_price.py';sp=importlib.util.spec_from_file_location('interval',path);t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
    raw=(a.out/'RESULT.json').read_bytes();r=json.loads(raw);c={int(k):v for k,v in r['profile'].items()};base={1:96,2:72,3:53,4:13,5:71,6:20,7:99,8:1};delta=Counter(c)
    for k,v in base.items():delta[k]-=v
    assert {k:v for k,v in delta.items()if v}=={2:-3,3:3,6:3,7:-3}
    B=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
    for j in range(1,9):B[1+7*j]+=Fraction(74,6);B[7*j]-=Fraction(74,6)
    room=B.copy()
    for k,v in c.items():room[k]-=v
    assert t.interval(room)[0]>7
    result={'status':'PASS_LITERAL_THIRD_RETENTION_INVOICE','receipt_sha256':hashlib.sha256(raw).hexdigest(),
            'exponent':'199/200','profile':c,'moment':t.report(t.interval(c)),
            'predecessor_moment':t.report(t.interval(base)),'exact_delta_coefficients':{k:v for k,v in delta.items()if v},
            'increment':t.report(t.interval(delta)),'limiting_allowance':t.report(t.interval(B)),'limiting_room':t.report(t.interval(room)),
            'scope':'All30 partial-source endpoints and allMOVE commands priced.102INIT,858ADD,102dirtyCLEAR remain explicit and are not discharged by movement margin.81 endpoints and full supplier costs remain open. No new kappa.'}
    (a.out/'PRICE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
