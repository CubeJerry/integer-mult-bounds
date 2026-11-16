#!/usr/bin/env python3
"""Reassign the actual P6 retention to37; pay one ground copy to preserve20."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load

BASE='47cb0991e41d06efae453f0e2890af6f619ccc44109b46329749bee658a18d15'

def build(old):
    w=copy.deepcopy(old)
    ops=[['INIT','GROUND20','L20'],['ADD','X20','GROUND20'],['MOVE','GROUND20','zero']]
    for o in old['operations']:
        if o in [['MOVE','X20','Extra6'],['ADD','X20','EXTRA_AFF'],
                 ['MOVE','Y20','L19'],['ADD','HKEEP_L19','Y20']]:
            continue
        if o==['MOVE','X37','Hub']:
            ops += [['MOVE','X37','Extra6'],['ADD','X37','EXTRA_AFF']]
        if o==['MOVE','Y20','F20']:
            ops += [['ADD','GROUND20','Y20']]
        if o==['MOVE','Y37','F37']:
            ops += [['MOVE','Y37','L19'],['ADD','HKEEP_L19','Y37']]
        ops.append(o)
    ops.append(['CLEAR','GROUND20'])
    w['operations']=ops
    w['targets']=sorted(w['targets']+[37])
    w['base_word_sha256']=BASE
    w['schema']='actual-extra37-retention-preserve42-native-word-v1'
    w['extra_retention_reassignment']={'previous_raw_retention':20,'new_raw_retention':37,
        'packet':'P6','source_chart':'Extra6','retention_chart':'L19',
        'preserved_previous_output_by':'GROUND20: actual nativeL20→zero unit move',
        'old_X20_Extra6_stop_replaced_by_X37_stop':True,
        'all_three_actual_M1_imports_retained':True}
    w['scope']='Actual42 outputs including37, all222 formal columns and original restoration; changes one P6 retained source and pays one native raw20 ground copy. Three actual M1 imports remain. No complete111 supplier or new kappa.'
    return w

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE
    old=json.loads(raw);src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots']
    e=load(a.engine,'extra42_geometry');price=load(a.price_engine,'extra42_price')
    _,_,before=e.replay(old,R);w=build(old);C,H,after=e.replay(w,R)
    assert e.sub(C['L19'],C['F37'])
    expected=before['movement_profile'].copy();expected[1]+=1;assert after['movement_profile']==expected
    assert after['counts']=={'INIT':125,'ADD':830,'MOVE':484,'CLEAR':125} and after['dirty_CLEAR']==125
    observed=[(s,n,ch,r)for s,n,ch,r in H if n in ['GROUND20','EXTRA_AFF','HKEEP_L19'] and r]
    assert all(r==1<<37 for s,n,ch,r in observed if n in ['EXTRA_AFF','HKEEP_L19'])
    assert all(r==1<<20 for s,n,ch,r in observed if n=='GROUND20')
    tests=[['ADD','X20','GROUND20'],['MOVE','GROUND20','zero'],['ADD','GROUND20','Y20'],
           ['MOVE','X37','Extra6'],['ADD','X37','EXTRA_AFF'],['MOVE','Y37','L19'],
           ['ADD','HKEEP_L19','Y37'],['CLEAR','GROUND20']]
    controls=[]
    for op in tests:
        bad=copy.deepcopy(w);bad['operations'].remove(op)
        try:e.replay(bad,R)
        except (AssertionError,KeyError)as ex:controls.append({'removed':op,'failure':str(ex)})
        else:raise AssertionError(('accepted semantic omission',op))
    Q=price.moment(after['movement_profile']);B={127:37,64:74,1:-74}
    for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
    lim=tuple(x/6 for x in price.moment(B));room=lim[0]-Q[1],lim[1]-Q[0]
    a.out.mkdir(parents=True,exist_ok=True);encoded=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(encoded)
    out={'status':'PASS_ACTUAL_EXTRA37_RETENTION_PRESERVE42','word_sha256':hashlib.sha256(encoded).hexdigest(),'base_word_sha256':BASE,'native_source_sha256':old['source_sha256'],'before':before,'after':after,'new_outputs':[37],'all_three_real_M1_imports_retained':True,'changed_retention_events':[{'step':s,'field':n,'chart':ch,'value_hex':hex(r)}for s,n,ch,r in observed],'exact_movement_increment':'[1]','price':{'moment':price.display(Q),'limiting_allowance':price.display(lim),'limiting_room':price.display(room)},'negative_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','word_sha256','after','price']}))

if __name__=='__main__':main()
