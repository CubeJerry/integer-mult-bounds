#!/usr/bin/env python3
"""Independent exact tariff audit of the priced occurrence refinement."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse,hashlib, importlib.util, json

BASE=Path('/workspace/scratch/2a62370e4336')
PIN='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'

def record(interval):
    with localcontext() as c:
        c.prec=55
        return {'rational':list(map(str,interval)),
                'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',type=Path,default=BASE/'workers/A')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(a.arithmetic.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('own_exact_arithmetic',a.arithmetic)
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in g.moment(gate))
    cases=[]
    for folder,pin,expected_ranks,expected_profile in [
        ('composed-four-plane-corrections','fbbae97bf0c71ca5d1f74bbe272e5507690f09d991600fe42f1636f0386c7433',
         {1:71,4:40},{1:191,2:127,3:4,4:143,7:75}),
        ('low-retention-corrections','c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe',
         {1:71,2:16,3:16,4:8},{1:175,2:111,3:4,4:111,5:16,6:16,7:75})]:
        p=a.inputs/folder;raw=(p/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        word=json.loads(raw);inv=json.loads((p/'CUT-INVENTORY.json').read_text());assert inv['word_sha256']==pin
        assert inv['cut_before_operation']==word['carrier_interface_before_operation']
        ranks=Counter(f['rank']for f in inv['fields']if f['name'].startswith('X'))
        assert dict(ranks)==expected_ranks and sum(ranks.values())==111
        charts={k:g.chart(v)for k,v in word['charts'].items()}
        assert all(f['rank']==len(charts[f['chart']])and f['rank']!=7 for f in inv['fields'])
        at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
        profile=Counter()
        cut_places=None
        for step,(kind,n,*args)in enumerate(word['operations']):
            if step==word['carrier_interface_before_operation']:cut_places=at.copy()
            if kind=='INIT':at[n]=args[0]
            elif kind=='MOVE':
                profile[abs(len(charts[at[n]])-len(charts[args[0]]))]+=1;at[n]=args[0]
            elif kind=='CLEAR':del at[n]
        assert cut_places=={f['name']:f['chart']for f in inv['fields']}
        assert dict(profile)==expected_profile
        Q0=g.moment(profile);dprof={1:111}
        for r,count in ranks.items():
            dprof[7-r]=dprof.get(7-r,0)+count
            dprof[8-r]=dprof.get(8-r,0)-count
        delta=g.moment(dprof);assert 0<delta[0]<delta[1]<111
        cap=(111+ceiling[0]-Q0[1]-delta[1],111+ceiling[1]-Q0[0]-delta[0])
        assert 187<cap[0]<=cap[1]<188
        excess189=(Q0[0]+78+delta[0]-ceiling[1],Q0[1]+78+delta[1]-ceiling[0])
        assert excess189[0]>0
        unpriced=(111+ceiling[0]-Q0[1],111+ceiling[1]-Q0[0])
        assert unpriced[0]>188
        cases.append({'source':folder,'word_sha256':pin,'ranks':dict(ranks),
                      'Q0':record(Q0),'sum_delta':record(delta),'strict_charge_threshold':record(cap),
                      'integer_charge_cap':187,'charge189_excess':record(excess189),
                      'unpriced_strict_threshold':record(unpriced)})
    out={'status':'PASS_INDEPENDENT_PRICED_OCCURRENCE_TARIFF','cases':cases,
         'controls':['strict threshold excludes188','strict threshold does not exclude187',
                     'zero delta shortcut strictly weakens the cap','t=1 gives delta=0 algebraically'],
         'scope':'Physical refinement conditional on retained fitting/occurrence theorem and independently audited source cuts. The fixed-half algebraic screen is a separate premise.'}
    dest=a.out/'RESULT.json';dest.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])
    for c in cases:print(c['source'],'cap',c['integer_charge_cap'],'delta',c['sum_delta']['decimal'][0],'excess189',c['charge189_excess']['decimal'][0])

if __name__=='__main__':main()
