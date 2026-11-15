#!/usr/bin/env python3
"""Emit and check the point-seeded source and explicit W-history witnesses."""
import argparse,copy,hashlib,json
from pathlib import Path
import construct as c

def history_certificate(word,roots,h):
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    charts={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    B={};selected=[]
    for step,o in enumerate(word['operations']):
        if o[0]=='INIT':values[o[1]]=0;charts[o[1]]=o[2]
        elif o[0]=='ADD':values[o[2]]^=values[o[1]]
        elif o[0]=='MOVE':charts[o[1]]=o[2]
        elif o[0]=='CLEAR':del values[o[1]];del charts[o[1]]
        for packet in range(8):
            n=f'P{packet}'
            if n not in values or charts[n]=='Hub':continue
            original=values[n];row=original;expression=1<<len(selected)
            while row:
                k=row.bit_length()-1
                if k in B:v,e=B[k];row^=v;expression^=e
                else:
                    B[k]=(row,expression)
                    selected.append({'packet':n,'operation_index':step,'chart':charts[n],'row_hex':hex(original)})
                    break
    W=[c.mask(j for j,r in enumerate(roots)if h[j]==h[i]and(j==i or c.dot(r,roots[i])==0))for i in range(111)]
    witnesses=[]
    for i,original in enumerate(W):
        row=original;expression=0
        while row:
            k=row.bit_length()-1
            if k not in B:raise ValueError('Missing W row '+str(i))
            v,e=B[k];row^=v;expression^=e
        actual=0
        for j,s in enumerate(selected):
            if expression>>j&1:actual^=int(s['row_hex'],16)
        assert actual==original
        witnesses.append({'role':i,'W_row_hex':hex(original),'selected_history_coefficients_hex':hex(expression)})
    seeds=[int(s,16)for s in word['initial_seed_rows_hex']]
    modes=[int(s,16)for s in word['proper_mode_rows_hex']]
    R=c.rank_f2(seeds+modes)
    terminal=[int(word['expected_owned_at_handoff'][f'P{i}']['value_hex'],16)for i in range(8)]
    T=c.rank_f2(terminal)
    return {'status':'PASS_LITERAL_ALL111_W_HISTORY_RELATIONS','all_input_columns':222,
            'history_basis':selected,'W_rows':witnesses,'history_rank':len(selected),
            'seed_plus_full_mode_rank':R,'seed_plus_full_mode_W_intersection':R+15-c.rank_f2(seeds+modes+W),
            'terminal_rank':T,'terminal_W_intersection':T+15-c.rank_f2(terminal+W),
            'scope':'Each binary row identity tensors with I_V over every characteristic-two field; no global availability of history is granted.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path)
    parser.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=parser.parse_args()
    repo=a.repo or next((p for p in Path(__file__).resolve().parents if(p/'AGENTS.md').exists()),None)
    if repo is None:raise ValueError('Specify --repo')
    repo=repo.resolve();roots,h,pins=c.configure(repo);a.out.mkdir(exist_ok=True,parents=True)
    result={'status':'PASS_POINT_SEEDED_TWO_OUTPUT_W_HISTORY','source_pins':pins,'receipts':{},'history_witnesses':{},'negative_controls':{},'new_complete_kappa':False}
    for coupled in[False,True]:
        for closed in[False,True]:
            w=c.build(roots,h,closed,coupled);r=c.replay(w,roots,h)
            name=('COUPLED-'if coupled else'UNCOUPLED-')+('CLOSED-'if closed else'')+'WORD.json'
            (a.out/name).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n');result['receipts'][name]=r
            if not closed:
                witness=history_certificate(w,roots,h);wn=name.replace('WORD','HISTORY')
                (a.out/wn).write_text(json.dumps(witness,indent=2,sort_keys=True)+'\n')
                result['history_witnesses'][wn]={k:v for k,v in witness.items()if k not in['history_basis','W_rows']}
    base=c.build(roots,h,False,True)
    changes={'omit_point_seed':['ADD','X34','P4'],'omit_original_y_capture':['ADD','Y34','YM'],
             'omit_feedback':['ADD','Y34','P4'],'omit_ground_y_cancel':['ADD','YM','P4'],
             'omit_mode_read':['ADD','DC0_1','P0'],'omit_second_delivery':['ADD','P5','Y17'],
             'omit_second_correction':['ADD','SC3_1','Y17']}
    for label,op in changes.items():
        bad=copy.deepcopy(base);i=bad['operations'].index(op);del bad['operations'][i]
        bad['markers']={k:v-int(v>i)for k,v in bad['markers'].items()}
        for k in['first_add_index','second_add_index']:
            j=bad['exchange'][k]
            if j is not None and j>i:bad['exchange'][k]-=1
        try:c.replay(bad,roots,h)
        except(ValueError,KeyError)as e:result['negative_controls'][label]={'rejected':True,'reason':str(e)}
        else:raise ValueError('Accepted mutant '+label)
    q=result['receipts']['COUPLED-CLOSED-WORD.json']['movement_profile']
    assert q=={1:121,2:32,3:30,4:44,5:48,6:22,7:113,8:1}
    price=c.price(q);price['scope']='Actual closed two-output partial source. Movement positivity alone is not supplier admission.'
    source=repo/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a'
    result['dependency_sha256']={str((source/n).relative_to(repo)):hashlib.sha256((source/n).read_bytes()).hexdigest()for n in['coupled_two_receiver.py','shared_facet_source.py','full_singular_history.py','eight_packet_source.py','price.py','triple_source.py','two-receiver-output/COUPLED-WORD.json','two-receiver-output/UNCOPLED-WORD.json']}
    for name,value in[('RESULT.json',result),('PRICE.json',price)]:
        (a.out/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'completed_targets':[17,34],
       'profile':q,'coupled_counts':result['receipts']['COUPLED-CLOSED-WORD.json']['counts'],
       'uncoupled_counts':result['receipts']['UNCOUPLED-CLOSED-WORD.json']['counts'],
       'history':result['history_witnesses'],'moment':price['moment']['lower_decimal'],'room':price['limiting_room']['lower_decimal']}))
if __name__=='__main__':main()
