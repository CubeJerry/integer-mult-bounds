#!/usr/bin/env python3
"""Exact movement interval and peak owned inventory for the coupling word."""
import argparse,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--word',type=Path,required=True);p.add_argument('--result',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();w=json.loads(a.word.read_text());r=json.loads(a.result.read_text());assert hashlib.sha256(a.word.read_bytes()).hexdigest()==r['word_sha256'];s=importlib.util.spec_from_file_location('interval',Path(__file__).with_name('retained')/'interval_price.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t);profile={int(k):v for k,v in r['profile'].items()};owners=set();peak=0
for o in w['operations']:
 if o[0]=='INIT':owners.add(o[1]);peak=max(peak,len(owners))
 elif o[0]=='CLEAR':owners.remove(o[1])
assert not owners and peak==114
B=Counter({127:Fraction(37,6),64:Fraction(74,6),1:Fraction(-74,6)})
for j in range(1,9):B[1+7*j]+=Fraction(74,6);B[7*j]-=Fraction(74,6)
B.subtract(profile);out={'word_sha256':r['word_sha256'],'counts':r['counts'],'peak_simultaneous_owned_fields':peak,'movement_profile':profile,'movement_price':t.report(t.interval(profile)),'remaining_limiting_movement_room':t.report(t.interval(B)),'increment_over_cheaper34':{'ADD':3,'MOVE':0,'INIT':0,'CLEAR':0,'movement_price':0},'scope':'Exact complete literal-word movement invoice. Three additional ADDs remain chargeable; no complete supplier or kappa certificate.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'PRICE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
