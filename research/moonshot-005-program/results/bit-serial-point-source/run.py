#!/usr/bin/env python3
"""Emit the serial three-output source, explicit W witnesses and rejecting controls."""
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
    result={'status':'PASS_SERIAL_POINT_THREE_OUTPUT_W_HISTORY','source_pins':pins,'receipts':{},'history_witnesses':{},'negative_controls':{},'new_complete_kappa':False}
    for closed in[False,True]:
        w=c.build(roots,h,closed);r=c.replay(w,roots,h)
        name=('CLOSED-'if closed else'')+'WORD.json'
        (a.out/name).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n');result['receipts'][name]=r
        if not closed:
            witness=history_certificate(w,roots,h)
            (a.out/'HISTORY.json').write_text(json.dumps(witness,indent=2,sort_keys=True)+'\n')
            result['history_witnesses']['HISTORY.json']={k:v for k,v in witness.items()if k not in['history_basis','W_rows']}
    base=c.build(roots,h,False)
    changes={'omit_first_public_y_prefix':['ADD','Y34','Y17'],
             'omit_second_public_y_prefix':['ADD','Y17','Y9'],
             'omit_x17_capture':['ADD','X17','PAIR_C17'],
             'omit_x9_capture':['ADD','X9','TRIPLE_C9'],
             'omit_first_feedback':['ADD','Y34','P4'],
             'omit_second_feedback':['ADD','Y17','P4'],
             'omit_second_public_y_capture':['ADD','Y17','YM17'],
             'omit_second_public_y_cancel':['ADD','YM17','P4'],
             'omit_last_output_delivery':['ADD','P4','Y9'],
             'omit_D_mode_read':['ADD','DC0_1','P0']}
    for label,op in changes.items():
        bad=copy.deepcopy(base);i=bad['operations'].index(op);del bad['operations'][i]
        bad['markers']={k:v-int(v>i)for k,v in bad['markers'].items()}
        for k in['first_add_index','second_add_index']:
            j=bad['exchange'][k]
            if j>i:bad['exchange'][k]-=1
        try:c.replay(bad,roots,h)
        except(ValueError,KeyError)as e:result['negative_controls'][label]={'rejected':True,'reason':str(e)}
        else:raise ValueError('Accepted mutant '+label)
    q=result['receipts']['CLOSED-WORD.json']['movement_profile']
    assert q=={1:105,2:39,3:23,4:29,5:53,6:29,7:115,8:1}
    price=c.price(q);price['scope']='Actual closed three-output partial source, including all remaining Y ascents. Movement positivity alone is not supplier admission.'
    source=repo/'research/moonshot-005-program/results/bit-coupled-singular-delivery/worker-a'
    dependencies=[source/n for n in['coupled_two_receiver.py','shared_facet_source.py','full_singular_history.py','eight_packet_source.py','price.py','triple_source.py','two-receiver-output/COUPLED-WORD.json']]
    dependencies += [repo/'research/moonshot-005-program/results/bit-orthogonal-staircase/ADMISSION.md',repo/'research/moonshot-005-program/results/bit-orthogonal-staircase/author/PROOF.md']
    result['dependency_sha256']={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dependencies}
    result['local_author_sha256']={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest()for n in['construct.py','run.py']}
    for name,value in[('RESULT.json',result),('PRICE.json',price)]:
        (a.out/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'completed_targets':[9,17,34],
       'profile':q,'counts':result['receipts']['CLOSED-WORD.json']['counts'],
       'dirty_clears':result['receipts']['CLOSED-WORD.json']['dirty_clears'],
       'history':result['history_witnesses'],'moment':price['moment']['lower_decimal'],'room':price['limiting_room']['lower_decimal']}))
if __name__=='__main__':main()
