#!/usr/bin/env python3
"""Exact identical source tariff, without importing a new caller allowance."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path
PIN='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
def need(c,m):
    if not c:raise ValueError(m)
def main(a):
    need(hashlib.sha256(a.engine.read_bytes()).hexdigest()==PIN,'interval engine pin')
    s=importlib.util.spec_from_file_location('inverse_price',a.engine);p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
    raw=a.word.read_bytes();w=json.loads(gzip.decompress(raw));q=Counter()
    for op in w['program']:
        if op[0]=='MOVE':q[abs(len(w['frames'][op[2]])-len(w['frames'][op[3]]))]+=1
    need(q==Counter({2:224,3:224,5:224,6:224}),'literal full inverse tariff')
    value=p.moment(q);r={'status':'PASS_IDENTICAL_INVERSE_SOURCE_TARIFF','word_sha256':hashlib.sha256(raw).hexdigest(),
      'kappa':'1/200','actual_profile':dict(q),'exact_moment':p.enc(value),'display':float(value[0]),
      'added_ordinary_counts':{'ADD':896,'MOVE':896},'owned_fields':0,'old_or_new_caller_allowance_claimed':False,
      'scope':'Every inverse Gaussian rank remains paid. Strictly descending raw orientation and mixed-orientation caller admission stay explicit. No new kappa.'}
    a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'],r['display'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
