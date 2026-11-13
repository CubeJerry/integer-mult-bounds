#!/usr/bin/env python3
"""Semantic, ownership and route controls for actual residual consumers."""
import argparse,copy,json,sys
from pathlib import Path

def main(a):
    base=a.repo/'research/moonshot-005-program/results';sys.path.insert(0,str(base/'joint-current-row-codes/review-star'))
    from engine import interpret,load,need,sha
    s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz');w=load(a.output/'WORD.json.gz')
    p=load(base/'joint-current-row-codes/cyclic-dual/WORD.json.gz');want,wl=interpret(s,w)
    m=w['cyclic_direct_returns'];begin,end=m['begin'],m['end'];temp=m['one_reused_owned_slot'];mutants=[]
    def edit(name,predicate,change):
        z=copy.deepcopy(w);ix=next(i for i in range(begin,end) if predicate(z['program'][i]));change(z['program'][ix]);mutants.append((name,z,ix))
    edit('omit_authentic_d_copy',lambda o:o[0]=='ADD' and o[1]==temp,lambda o:o.__setitem__(3,'0'))
    edit('omit_column_consumer',lambda o:o[0]=='ADD' and o[1]<1880,lambda o:o.__setitem__(3,'0'))
    edit('wrong_owned_flag',lambda o:o[0]=='MOVE',lambda o:o.__setitem__(4,False))
    edit('wrong_lifetime_birth_chart',lambda o:o[0]=='INIT',lambda o:o.__setitem__(2,3))
    edit('unmoved_authentic_return',lambda o:o[0]=='MOVE',lambda o:o.__setitem__(3,o[2]))
    edit('clear_original_instead_of_owned',lambda o:o[0]=='CLEAR',lambda o:o.__setitem__(1,1480))
    checks=[]
    for name,z,ix in mutants:
        try:
            actual,al=interpret(s,z);rejected=actual!=want or al!=wl;reason='actual1880-input map differs' if rejected else 'NOT_REJECTED'
        except ValueError as e:rejected=True;reason=str(e)
        need(rejected,'negative control rejected '+name);checks.append({'name':name,'event':ix,'rejected':True,'reason':reason})
    projection=[o for i,o in enumerate(w['program']) if not(begin<=i<end)]
    need(projection==p['program'],'entire original source instruction projection literal')
    receipt={'status':'PASS_ACTUAL_RESIDUAL_CONSUMER_CONTROLS','word_sha256':sha((a.output/'WORD.json.gz').read_bytes()),'controls':checks,'literal_parent_projection':True,'all1880_input_semantics_checked':True,'scope':'Author checks, not independent review.'}
    (a.output/'NEGATIVE-CONTROLS.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(receipt['status'],len(checks))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
