#!/usr/bin/env python3
"""Couple the Extra6 source37 to50 with an actual rerouted source import.

Retiming PRIVATE16 to M0 preserves its actual sum. One Extra6-to-M0 import
replaces every old lower-chart use of original50, freeing its public itinerary
for the nested-retention triple {19,37,50}.
"""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load

BASE='d5726e001270e007209507c8eb9f385167a7d304a9f09c194381296b569f293f'

def build(old,R):
    w=copy.deepcopy(old)
    w.pop('extra_retention_reassignment',None)
    for name,T in [('P6_K',[19,37]),('P6_A',[50,37]),('P6_B',[50,19])]:
        assert name not in w['charts'];w['charts'][name]={'kind':'span','rows':[R[i]for i in T]}
    ops=[['INIT','P6_RAW37L','L37'],['ADD','X37','P6_RAW37L'],
         ['INIT','P6_RAW50L','L50'],['ADD','X50','P6_RAW50L'],
         ['INIT','P6_RAW37A','P6_A'],['INIT','P6_RAW50B','P6_B'],
         ['INIT','P6_RET','P6_K'],['INIT','IMPORT_RAW50','Extra6']]
    private_sources=[o[1]for o in old['operations']if o[0]=='ADD'and o[2]=='PRIVATE16']
    assert private_sources==['X7','X30','X31','X49','X50']
    obsolete=[o for o in old['operations']if 'HKEEP_L19'in o]
    for o in old['operations']:
        op,n,*q=o
        if 'HKEEP_L19'in o:continue
        if o==['INIT','PRIVATE16','J16']:
            ops.append(['INIT','PRIVATE16','M0']);continue
        if op=='ADD'and q[0]=='PRIVATE16':continue
        if o==['MOVE','X50','J16']:continue
        if o==['MOVE','X50','C0']:
            ops += [['MOVE','X50','P6_B'],['ADD','X50','P6_RAW50B'],
                    ['MOVE','X50','Extra6'],['ADD','X50','EXTRA_AFF'],
                    ['ADD','X50','IMPORT_RAW50'],['MOVE','IMPORT_RAW50','M0'],
                    ['ADD','IMPORT_RAW50','PRIVATE16']]
            continue
        if op=='ADD'and n=='X50'and q[0]in['H1_1','H1_2','Hnew1_0','Q0']:
            ops.append(['ADD','IMPORT_RAW50',q[0]]);continue
        if o==['ADD','PRIVATE16','P0']:continue
        if o==['MOVE','P0','J16']:
            ops.append(['ADD','PRIVATE16','P0'])
        if o==['MOVE','X37','Extra6']:
            ops += [['MOVE','X37','P6_A'],['ADD','X37','P6_RAW37A']]
        if o==['MOVE','P6','L19']:
            ops += [['MOVE','P6','P6_K'],['ADD','P6','P6_RET']]
        if o==['MOVE','Y19','F19']:
            ops += [['MOVE','Y19','L50'],['ADD','P6_RAW50L','Y19'],
                    ['MOVE','Y19','P6_A'],['ADD','P6_RAW37A','Y19']]
        if o==['MOVE','Y37','L19']:
            ops += [['ADD',n,'Y37']for n in['P6','E75','E77','E79']]
            ops.append(o);ops.append(['ADD','HRAW19','Y37']);continue
        if o==['MOVE','Y37','F37']:
            ops += [['MOVE','Y37','P6_B'],['ADD','P6_RAW50B','Y37']]
        if o==['MOVE','Y50','F50']:
            ops += [['MOVE','Y50','L37'],['ADD','P6_RAW37L','Y50'],
                    ['MOVE','Y50','P6_K'],['ADD','P6_RET','Y50']]
        ops.append(o)
        if op=='MOVE'and n in private_sources and n!='X50'and q==['C0']:
            ops.append(['ADD',n,'PRIVATE16'])
    ops += [['CLEAR',n]for n in['P6_RAW37L','P6_RAW50L','P6_RAW37A','P6_RAW50B','P6_RET','IMPORT_RAW50']]
    w['operations']=ops;w['targets']=sorted(w['targets']+[50])
    w['schema']='actual-extra6-triple-source-retimed43-native-word-v1'
    w['source50_retiming']={'old_private_chart':'J16','new_private_chart':'M0',
        'actual_private_sources':private_sources,'source50_actual_new_route':['L50','P6_B','Extra6','Hub'],
        'source50_import_route':['Extra6','M0'],'four_old_M0_cache_reads_replaced':True,
        'P0_private_query_moved_before_J16_descent':True}
    w['extra6_common_triple']={'packet':'P6','roles':[19,37,50],
        'actual_source_row_roles':[37,50],'source_chart':'Extra6','partial_chart':'P6_K',
        'terminal_raw19_added_at':'L19','ground_mask_fields':['E75','E77','E79'],
        'all_three_actual_M1_E_imports_retained':True}
    w['scope']='Actual43 outputs with new37 and50 over the cyclic41 source; complete222-column replay and original restoration. Real raw50 source rerouting/import plus nested Extra6 triple. No complete111 supplier, ordinary recursive theorem, or new kappa.'
    return w

def cut_values(word,operation):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    for o in word['operations']:
        if o==operation:return v,at
        op,n,*q=o
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='MOVE':at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='CLEAR':del v[n],at[n]
    raise AssertionError(operation)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--price-engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);assert old['schema']=='actual-extra37-retention-preserve42-native-word-v1'
    src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots']
    e=load(a.engine,'extra43_geometry');price=load(a.price_engine,'extra43_price');_,_,before=e.replay(old,R)
    w=build(old,R);w['base_word_sha256']=hashlib.sha256(raw).hexdigest();C,H,after=e.replay(w,R)
    dot=lambda i,j:sum(a*b for a,b in zip(R[i],R[j]))
    assert all(dot(i,j)==0 for i in[19,37,50]for j in[19,37,50]if i!=j)
    ov,oa=cut_values(old,['MOVE','P0','J16']);v,at=cut_values(w,['MOVE','P0','J16'])
    assert v['PRIVATE16']==ov['PRIVATE16'] and v['P0']==ov['P0']^ov['PRIVATE16']
    assert v['IMPORT_RAW50']==1<<50 and at['IMPORT_RAW50']=='M0'
    for n in ['H1_1','H1_2','Hnew1_0','Q0']:assert v[n]==ov[n]
    v,at=cut_values(w,['MOVE','Y16','SH2'])
    assert v['EXTRA_AFF']==v['P6_RET']==(1<<37)^(1<<50)
    assert v['P6']^v['E75']^v['E77']^v['E79']==sum(1<<i for i in[19,37,50])
    assert all(v[f'IMPORT_E{i}']==1<<i and at[f'IMPORT_E{i}']=='M1'for i in[8,9,36])
    delta={1:8,2:1,3:-2,4:3,5:1,6:-1,7:-2};expected=before['movement_profile'].copy()
    for d,n in delta.items():expected[d]=expected.get(d,0)+n
    assert after['movement_profile']==expected,(after['movement_profile'],expected)
    tests=[['MOVE','IMPORT_RAW50','M0'],['ADD','IMPORT_RAW50','PRIVATE16'],
           ['ADD','IMPORT_RAW50','H1_1'],['ADD','X50','EXTRA_AFF'],
           ['ADD','X37','P6_RAW37A'],['ADD','X50','P6_RAW50B'],
           ['ADD','P6','P6_RET'],['MOVE','Y19','L50'],['ADD','P6_RAW37A','Y19'],
           ['ADD','HRAW19','Y37'],['ADD','P6_RAW50B','Y37'],
           ['ADD','P6_RAW37L','Y50'],['ADD','P6_RET','Y50'],['CLEAR','IMPORT_RAW50']]
    controls=[]
    for op in tests:
        bad=copy.deepcopy(w);bad['operations'].remove(op)
        try:e.replay(bad,R)
        except (AssertionError,KeyError)as ex:controls.append({'removed':op,'failure':str(ex)})
        else:raise AssertionError(('accepted omission',op))
    # Restoring the obsolete source50 J16 stop is incompatible with its new plane.
    bad=copy.deepcopy(w);ix=bad['operations'].index(['MOVE','X50','P6_B']);bad['operations'].insert(ix,['MOVE','X50','J16'])
    try:e.replay(bad,R)
    except AssertionError as ex:controls.append({'inserted':['MOVE','X50','J16'],'failure':str(ex)})
    else:raise AssertionError('accepted incomparable original50 route')
    Q=price.moment(after['movement_profile']);B={127:37,64:74,1:-74}
    for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
    lim=tuple(x/6 for x in price.moment(B));room=lim[0]-Q[1],lim[1]-Q[0]
    a.out.mkdir(parents=True,exist_ok=True);encoded=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(encoded)
    out={'status':'PASS_ACTUAL_EXTRA6_TRIPLE43_WITH_RETIMED_SOURCE50','word_sha256':hashlib.sha256(encoded).hexdigest(),'base_word_sha256':w['base_word_sha256'],'native_source_sha256':old['source_sha256'],'before':before,'after':after,'new_outputs_over42':[50],'actual_common_triple':[19,37,50],'source50_import_actual_value_hex':hex(1<<50),'old_PRIVATE16_and_four_M0_cache_values_preserved':True,'all_three_actual_M1_E_imports_preserved':True,'exact_movement_increment':'8[1]+[2]-2[3]+3[4]+[5]-[6]-2[7]','signed_movement_increment':delta,'linear_rank_volume_increment':sum(d*n for d,n in delta.items()),'price':{'moment':price.display(Q),'limiting_allowance':price.display(lim),'limiting_room':price.display(room),'increment':price.display(price.moment(delta))},'negative_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','word_sha256','after','price']}))

if __name__=='__main__':main()
