#!/usr/bin/env python3
"""Literal receiver26 composition, not a complete decoder or supplier."""
import argparse,copy,hashlib,json,sys
from pathlib import Path

def extend(w,roots,rank,mask,closed=False):
    word=copy.deepcopy(w);charts=word['charts'];ops=[]
    for name,source in [('H','D6'),('K7','D7'),('K22','D22')]:
        charts['R26_'+name]={'kind':'ann','rows':charts[source]['rows']+[roots[26]]}
    charts['R26_J']={'kind':'ann','rows':charts['R26_K7']['rows']+charts['R26_K22']['rows']}
    assert [8-rank(charts['R26_'+n]['rows'])for n in['J','K7','K22','H']]==[3,4,4,5]
    groups=[('C7','K7','D7',[5,15]),('C22','K22','D22',[41,57,89,110])]
    intercept={f'X{j}':('R26_'+c,'R26_'+k,d)for c,k,d,js in groups for j in js}
    ops=[['INIT','R26_'+c,'R26_'+k]for c,k,d,js in groups];positions={}
    for count,o in enumerate(w['operations'],1):
        if o[0]=='MOVE'and o[1]in intercept:
            c,k,d=intercept.pop(o[1]);assert o[2]==d
            ops += [['MOVE',o[1],k],['ADD',o[1],c]]
        ops.append(o);positions[count]=len(ops)
    assert not intercept
    word['markers']={k:positions[v]for k,v in w['markers'].items()}
    for key in['first_add_index','second_add_index']:
        i=word['exchange'][key]
        if i is not None:word['exchange'][key]=positions[i+1]-1
    ops += [['MOVE','R26_C22','R26_J'],['MOVE','DC1_2','R26_H'],
            ['MOVE','Y26','R26_J'],['ADD','R26_C22','Y26'],
            ['MOVE','Y26','R26_K7'],['ADD','R26_C7','Y26'],
            ['MOVE','Y26','R26_H'],['ADD','DC1_2','Y26'],['MOVE','Y26','F26']]
    word['operations']=ops;word['markers']['handoff']=len(ops)
    word['expected_owned_at_handoff']['DC1_2']['chart']='R26_H'
    for c,k,d,js in groups:
        word['expected_owned_at_handoff']['R26_'+c]={'chart':'R26_'+('J'if c=='C22'else k),'value_hex':hex(mask(js))}
    word['completed_targets']=[17,26,34];word['schema']='receiver26-source-correction-chronology-v1'
    word['receiver26']={'raw_cache':'DC1_2','raw_support':[5,15,26,41,57,89,110],
                       'local_correction_groups':[g[3]for g in groups],
                       'additional_moving_owners':['R26_C22','DC1_2'],
                       'scope':'Partial three-output word; unchanged source operations with legal capture insertions.'}
    if closed:
        for name in word['expected_owned_at_handoff']:ops.append(['CLEAR',name])
        for j in range(111):
            if j not in word['completed_targets']:ops.append(['MOVE',f'Y{j}',f'F{j}'])
    word['closed_partial']=closed
    return word

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,default=Path(__file__).parent/'receiver26-output');a=parser.parse_args()
    src=a.repo/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a';sys.path.insert(0,str(src))
    from shared_facet_source import source_geometry,rank_q,mask
    from coupled_two_receiver import replay
    from eight_packet_source import price
    roots,h,pins=source_geometry(a.repo);a.out.mkdir(exist_ok=True,parents=True)
    result={'status':'PASS_ACTUAL_RECEIVER26_SOURCE_CORRECTION_COMPOSITION','source_pins':pins,'receipts':{},'negative_controls':{},'new_complete_kappa':False}
    for coupled in[False,True]:
        sourcepath=src/'two-receiver-output'/('COUPLED-WORD.json'if coupled else'UNCOPLED-WORD.json')
        original=json.loads(sourcepath.read_text())
        result['source_'+str(coupled)]={'path':str(sourcepath.relative_to(a.repo)),'sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest()}
        for closed in[False,True]:
            word=extend(original,roots,rank_q,mask,closed);receipt=replay(word,roots,h)
            receipt['status']=result['status'];receipt['completed_targets']=word['completed_targets']
            name=('COUPLED-'if coupled else'UNCOUPLED-')+('CLOSED-'if closed else'')+'WORD.json'
            (a.out/name).write_text(json.dumps(word,indent=2,sort_keys=True)+'\n');result['receipts'][name]=receipt
    baseline=extend(json.loads((src/'two-receiver-output/COUPLED-WORD.json').read_text()),roots,rank_q,mask)
    mutations={'omit_pair_capture':['ADD','X15','R26_C7'],'omit_four_capture':['ADD','X110','R26_C22'],
               'omit_raw_export':['MOVE','DC1_2','R26_H'],'omit_correction_descent':['MOVE','R26_C22','R26_J'],
               'omit_pair_read':['ADD','R26_C7','Y26'],'omit_four_read':['ADD','R26_C22','Y26'],'omit_raw_read':['ADD','DC1_2','Y26']}
    for label,op in mutations.items():
        bad=copy.deepcopy(baseline);i=bad['operations'].index(op);del bad['operations'][i]
        bad['markers']={k:v-int(v>i)for k,v in bad['markers'].items()}
        for key in['first_add_index','second_add_index']:
            j=bad['exchange'][key]
            if j is not None and j>i:bad['exchange'][key]-=1
        try:replay(bad,roots,h)
        except(ValueError,KeyError)as e:result['negative_controls'][label]={'rejected':True,'reason':str(e)}
        else:raise ValueError('Accepted mutant '+label)
    profile=result['receipts']['COUPLED-CLOSED-WORD.json']['movement_profile']
    assert profile=={1:152,2:20,3:56,4:60,5:22,6:22,7:111,8:1},profile
    bill=price(profile);bill['scope']='Actual three-output partial word; movement margin is necessary only.'
    direct=copy.deepcopy(original)
    direct['operations'] += [['MOVE','R26','zero'],['ADD','R26','Y26']]
    direct['expected_owned_at_handoff']['R26']['chart']='zero'
    direct['markers']['handoff']=len(direct['operations']);direct['completed_targets']=[17,26,34]
    for name in direct['expected_owned_at_handoff']:direct['operations'].append(['CLEAR',name])
    for j in range(111):
        if j not in direct['completed_targets']:direct['operations'].append(['MOVE',f'Y{j}',f'F{j}'])
    direct['operations'].append(['MOVE','Y26','F26'])
    direct['closed_partial']=True
    direct_receipt=replay(direct,roots,h);direct_receipt['completed_targets']=[17,26,34]
    direct_price=price(direct_receipt['movement_profile'])
    (a.out/'DIRECT-POINT-CONTROL-WORD.json').write_text(json.dumps(direct,indent=2,sort_keys=True)+'\n')
    result['direct_point_control']={'receipt':direct_receipt,'price':direct_price,
       'scope':'Same three completed targets and original source; this does not reproduce the mixed-export source interface.'}
    for name,value in[('RESULT.json',result),('PRICE.json',bill)]:
        (a.out/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'completed_targets':[17,26,34],'profile':profile,
                      'counts':result['receipts']['COUPLED-CLOSED-WORD.json']['counts'],
                      'moment':bill['moment']['lower_decimal'],'room':bill['limiting_room']['lower_decimal']}))

if __name__=='__main__':main()
