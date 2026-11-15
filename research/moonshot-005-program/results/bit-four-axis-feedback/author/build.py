#!/usr/bin/env python3
"""Compose a retained coded history with three literal axis receivers.

This adapts the programme's admitted stationary-history exchange mechanism
to the actual h9 colored source. It is a partial source, not a supplier.
"""
import argparse,copy,hashlib,json
from pathlib import Path

def prevalue(word,match):
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    for op in word['operations'][:word['handoff']]:
        kind,name,*rest=op
        if kind=='INIT':values[name]=0
        elif kind=='ADD':values[rest[0]]^=values[name]
        elif kind=='CLEAR':del values[name]
        if op==match:return values['P1']
    raise ValueError('capture location absent')

def build(base,closed):
    w=copy.deepcopy(base)
    marker=['MOVE','P1','A30'];g=prevalue(base,marker)
    S=base['expected']['P1'][1]^g
    assert S==sum(1<<i for i in[0,5,6,7])
    captures={
        ('ADD','X0','C6_2_0'):('PURE0_A192','A192','X0',1),
        ('ADD','X0','C7_1_0'):('PURE0_F7','F7','X0',1),
        ('ADD','X7','C6_1_0'):('PURE7_F6','F6','X7',1<<7),
    }
    ops=[];seen=set();capture_count=0
    for op in base['operations'][:base['handoff']]:
        ops.append(op)
        if tuple(op) in captures:
            name,chart,source,row=captures[tuple(op)]
            ops += [['INIT',name,chart],['ADD',source,name]]
            w['expected'][name]=[chart,row];seen.add(name)
        if op==marker:
            ops += [['INIT','KEEP_P1_A30','A30'],['ADD','P1','KEEP_P1_A30'],['ADD','KEEP_P1_A30','P1']]
            capture_count+=1
    assert len(seen)==3 and capture_count==1
    w['expected']['KEEP_P1_A30']=['A30',g]
    w['expected']['P1']=['zero',S]
    # All receivers use the actual terminal S, then genuine stationary reads.
    decoders={
        5:[('L0','C1_7_0'),('A126','C1_6_0'),('A62','C1_5_0')],
        6:[('L5','R5'),('A192','PURE0_A192'),('F6','PURE7_F6')],
        7:[('L6','R6'),('A159','C7_6_0'),('F7','PURE0_F7')],
    }
    for i,chain in decoders.items():
        ops.append(['ADD','P1',f'Y{i}'])
        for chart,owner in chain:
            ops += [['MOVE',f'Y{i}',chart],['ADD',owner,f'Y{i}']]
        if chain[-1][0]!=f'F{i}':ops.append(['MOVE',f'Y{i}',f'F{i}'])
    w['handoff']=len(ops);w['closed']=closed
    if closed:
        ops += [['CLEAR',n]for n in w['expected']]
        ops += [['MOVE',f'Y{i}',f'F{i}']for i in range(111)if i not in[0,5,6,7]]
    w['operations']=ops;w['completed_targets']=[0,5,6,7]
    w['schema']='colored-four-axis-two-mixed-kernel-source-v1'
    w['historical_free_W_roles']=base['terminal_W_roles'][1:]
    w['terminal_W_roles']=[None,None]+base['terminal_W_roles'][2:]
    w['stationary_kernel']={'packet':'P1','chart':'A30','row_hex':hex(g),'owner':'KEEP_P1_A30',
        'terminal_row_hex':hex(S),'canonical_W_role_modulo_local':8}
    w['pure_captures']=[{'owner':n,'chart':ch,'source':s,'row_hex':hex(v)}for n,ch,s,v in captures.values()]
    w['decoder_chains']={str(i):[list(x)for x in chain]for i,chain in decoders.items()}
    w['new_complete_kappa']=False
    return w

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=a.source.read_bytes();base=json.loads(data)
    assert base['delayed_feedback_depth']==4 and base['completed_targets']==[0]
    a.out.mkdir(parents=True,exist_ok=True)
    for closed,name in[(False,'WORD.json'),(True,'CLOSED-WORD.json')]:
        w=build(base,closed);w['base_word_sha256']=hashlib.sha256(data).hexdigest()
        (a.out/name).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'EMITTED_FOUR_AXIS_TWO_KERNEL_PARTIAL_WORDS','base_word_sha256':hashlib.sha256(data).hexdigest(),'new_complete_kappa':False}))
if __name__=='__main__':main()
