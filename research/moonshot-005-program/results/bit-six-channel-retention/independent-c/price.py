#!/usr/bin/env python3
"""Independent rational interval invoice for both literal source profiles."""
import argparse,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    path=Path(__file__).with_name('retained')/'interval_price.py';spec=importlib.util.spec_from_file_location('interval',path);t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
    a21=json.loads((a.out/'21/RESULT.json').read_text());a27=json.loads((a.out/'27/RESULT.json').read_text())
    c21={int(k):v for k,v in a21['profile'].items()};c27={int(k):v for k,v in a27['profile'].items()}
    delta=Counter(c27)
    for k,v in c21.items():delta[k]-=v
    assert {k:v for k,v in delta.items()if v}=={1:12,3:3,7:-3}
    B=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
    for j in range(1,9):B[1+7*j]+=Fraction(74,6);B[7*j]-=Fraction(74,6)
    prices=[]
    for n,c in [(21,c21),(27,c27)]:
        room=B.copy()
        for k,v in c.items():room[k]-=v
        assert t.interval(room)[0]>7
        prices.append({'targets':n,'profile':c,'price':t.report(t.interval(c)),'limiting_room':t.report(t.interval(room))})
    result={'status':'PASS_INDEPENDENT_LITERAL_SOURCE_INVOICES','exponent':'199/200','prices':prices,
            'increment_27_over_21':t.report(t.interval(delta)), 'exact_increment_coefficients':dict(delta),
            'limiting_allowance':t.report(t.interval(B)),
            'scope':'Complete partial-source MOVE profiles only. Actual INIT,ADD,CLEAR counts remain explicit in review receipts. No completed all111 supplier or new kappa.'}
    (a.out/'PRICE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
