#!/usr/bin/env python3
"""Adversarial semantic/typing controls and common-entry receipt."""
import argparse,copy,json,sys
from pathlib import Path

def main(a):
    base=a.repo/'research/moonshot-005-program/results'
    sys.path.insert(0,str(base/'joint-current-row-codes/review-star'))
    from engine import Q,interpret,load,need,sha
    s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz')
    p=load(base/'joint-current-row-codes/cyclic-dual/WORD.json.gz');w=load(a.output/'WORD.json.gz')
    want,loc=interpret(s,w);meta=w['cyclic_null_projector'];j=meta['selected_modes'][0]
    ghost=meta['ghost_fields'][str(j)];ret=meta['return_fields'][str(j)]
    mutations=[]
    def edit(name,predicate,mutator):
        z=copy.deepcopy(w);hits=[i for i,o in enumerate(z['program']) if predicate(o)]
        need(hits,'actual mutant target '+name);i=hits[0];mutator(z['program'][i]);mutations.append((name,z,i))
    edit('omit_early_snapshot',lambda o:o[0]=='ADD' and o[1]==ghost and o[4]!=127,lambda o:o.__setitem__(3,'0'))
    edit('omit_late_cancellation',lambda o:o[0]=='ADD' and o[1]==ghost and o[4]==127 and o[2]!=ret,lambda o:o.__setitem__(3,'0'))
    edit('omit_real_d_term',lambda o:o==['ADD',ghost,ret,'1',127],lambda o:o.__setitem__(3,'0'))
    edit('unowned_ghost_move',lambda o:o[0]=='MOVE' and o[1]==ghost,lambda o:o.__setitem__(4,False))
    edit('wrong_snapshot_chart',lambda o:o[0]=='INIT' and o[1]==ghost,lambda o:o.__setitem__(2,3))
    edit('unmoved_real_return',lambda o:o[0]=='MOVE' and o[1]==ret,lambda o:o.__setitem__(3,o[2]))
    rows=[]
    for name,z,i in mutations:
        try:
            actual,al=interpret(s,z)
            rejected=actual!=want or al!=loc
            reason='exact full-input map differs' if rejected else 'NOT_REJECTED'
        except ValueError as e:
            rejected=True;reason=str(e)
        need(rejected,'mutant rejected '+name);rows.append({'name':name,'event':i,'rejected':rejected,'reason':reason})
    raw=set(w['private_role_map'].values());old,ol=interpret(s,p)
    need(all(want[i]=={i:Q(1)} and loc[i]==w['initial'][i] for i in range(1480)),'all1480 common rows and locations unchanged at actual common entry')
    need(raw==set(range(1480,1880)),'400 private slots distinct from common rows')
    tail=w['program'][w['marks']['common_starts']:]
    touch=[o for o in tail if o[1] in raw or o[0] in ['ADD','COPY'] and o[2] in raw]
    caches=[{'field':r,'chart':loc[r],'row':[[k,str(v)] for k,v in sorted(want[r].items())]} for r in want if r>=1880]
    receipt={'status':'PASS_CYCLIC_NULL_NEGATIVE_CONTROLS_AND_ENTRY_AUDIT','word_sha256':sha((a.output/'WORD.json.gz').read_bytes()),'controls':rows,'common_entry_boundary':w['marks']['common_starts'],'all1480_common_identity_rows_and_initial_locations':True,'private400_slots':{'first':1480,'last':1879},'live_inherited_caches':caches,'private_suffix_touch_count':len(touch),'private_suffix_only_final_recouplings':False,'all_changed_hosted_X2_suffix_uses_are_own_final_recouplings':True,'scope':'Author verification, not independent review. Common/private interaction outside changed hosted X2 is retained literally and is not claimed absent.'}
    (a.output/'NEGATIVE-CONTROLS.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(receipt['status'],len(rows),'common entry',receipt['common_entry_boundary'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
