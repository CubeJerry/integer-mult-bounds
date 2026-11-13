#!/usr/bin/env python3
"""Literal eight-target BIT mode-exchange bus on the actual coordinate frame."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,gzip,hashlib,json,importlib.util,copy
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
DEP='a28c7e8037ae99b6aecf21a62a4f784c906016d5e12f100826062cf3d602c5b1'
def main(a):
    src=a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
    raw=src.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
    n=json.loads(gzip.decompress(raw));frames={int(k):v for k,v in n['frames'].items()}
    dep=a.repo/'research/moonshot-005-program/results/bit-rank-nine-shared-interface/build_bit_nine_rail.py'
    assert hashlib.sha256(dep.read_bytes()).hexdigest()==DEP
    sp=importlib.util.spec_from_file_location('retained_replay',dep);r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
    eye=[[int(i==j) for j in range(8)] for i in range(8)]
    assert all(frames[n['start'][i]]['B']==[eye[i]] for i in range(8))
    zero=n['start'][111];hub=n['final'][0]
    flags={0:zero,8:hub,1:n['start'][0],7:n['final'][118]}
    created=[]
    for d in range(2,7):
        found=next((c for c,f in frames.items() if f['dim']==d and all(all(F(x)==0 for x in row[d:]) for row in f['B'])),None)
        if found is None:
            found=max(frames)+1;frames[found]={'dim':d,'B':eye[:d],'A':eye[d:]};created.append(found)
        flags[d]=found
    ops=[];checkpoints=[]
    def move(i,c,d):
        if c!=d:
            assert frames[c]['dim']!=frames[d]['dim'],('alias-only move',i,c,d)
            ops.append(['MOVE',i,c,d])
    move(7,n['start'][7],hub)
    packet=222;ops.extend([['INIT',packet,hub],['ADD',packet,7,hub]])
    prior=hub
    for k in range(7,0,-1):
        c=flags[k]
        move(111+k,zero,c);move(k-1,n['start'][k-1],c);move(packet,prior,c)
        ops.append(['ADD',111+k,packet,c])
        x_add=len(ops);ops.append(['ADD',k-1,packet,c])
        p_add=len(ops);ops.append(['ADD',packet,k-1,c])
        checkpoints.append({'served_role':k,'captured_role':k-1,'chart':c,'source_add_index':x_add,'packet_add_index':p_add,'packet_after':1<<(k-1),'source_after':(1<<(k-1))^(1<<k)})
        move(k-1,c,hub)
        restore=len(ops);ops.append(['ADD',k-1,k,hub]);checkpoints[-1]['hub_restore_index']=restore
        move(111+k,c,n['final'][111+k]);prior=c
    move(packet,prior,zero);ops.extend([['ADD',111,packet,zero],['CLEAR',packet,zero]])
    move(111,zero,n['final'][111])
    bus_ops=len(ops)
    for i in range(8,111):
        move(i,n['start'][i],hub);move(111+i,zero,n['final'][111+i])
    word={'schema':'BIT-source-packet-mode-exchange-eight-target-v1','public':222,'owned_fields':1,'start':n['start'][:222],'final':n['final'][:222],'frames':frames,'program':ops,'scope':'Eight actual coordinate-frame targets complete; other103 Y rows unchanged. Genuine joint source/packet mode exchanges; one owned nonzero clear retains the erasure foundation.'}
    rows,bill=r.replay(word,frames)
    expected=[1<<i for i in range(222)]
    for i in range(8):expected[111+i]^=1<<i
    assert rows==expected
    assert bill['paid_profile']=={1:12,2:4,3:4,4:4,5:4,6:4,7:210}
    # Explicit in-flight values are checked, not only final equality.
    values={i:1<<i for i in range(222)};observations=[];clear_values=[]
    by_index={c['packet_add_index']:c for c in checkpoints}
    for i,e in enumerate(ops):
        if e[0]=='INIT':values[e[1]]=0
        elif e[0]=='ADD':values[e[1]]^=values[e[2]]
        elif e[0]=='CLEAR':clear_values.append({'index':i,'field':e[1],'row':values[e[1]]});del values[e[1]]
        if i in by_index:
            q=by_index[i];assert values[packet]==q['packet_after'] and values[q['captured_role']]==q['source_after'];observations.append(q)
    assert clear_values[0]['row']==1
    controls=[]
    for name,index,action in [('omit_first_source_restoration',checkpoints[0]['hub_restore_index'],'delete'),('omit_first_packet_handoff',checkpoints[0]['packet_add_index'],'delete'),('reverse_first_feedback_order',checkpoints[0]['source_add_index'],'swap')]:
        bad=copy.deepcopy(word)
        if action=='delete':del bad['program'][index]
        else:bad['program'][index],bad['program'][index+1]=bad['program'][index+1],bad['program'][index]
        br,_=r.replay(bad,frames);failed=[i for i,(x,y) in enumerate(zip(br,expected)) if x!=y];assert failed
        controls.append({'name':name,'rejected':True,'wrong_public_rows':failed})
    bad=copy.deepcopy(word);bad['program'][0],bad['program'][2]=bad['program'][2],bad['program'][0]
    try:r.replay(bad,frames)
    except ValueError:controls.append({'name':'form_packet_before_source_reaches_Hub','rejected':True,'failure':'cochart/lifecycle'})
    else:raise AssertionError('invalid early acquisition passed')
    base={7:222,8:1};delta=Counter(bill['paid_profile']);delta.subtract(base)
    ceiling=json.loads((a.repo/'research/moonshot-005-program/results/bit-rank-nine-shared-interface/BUDGET.json').read_text())['at_t_199_over_200']['limiting_Q_allowance']
    lim=F(ceiling['exact_lower']),F(ceiling['exact_upper'])
    tiling=r.moment({7:222,8:14});deficit=tiling[0]-lim[1],tiling[1]-lim[0]
    assert deficit[0]>0
    a.output.mkdir(parents=True,exist_ok=True);sha=r.write_gzip(a.output/'WORD.json.gz',word)
    out={'status':'PASS_ACTUAL_EIGHT_TARGET_MODE_EXCHANGE_BUS','native_sha256':PIN,'retained_replay_sha256':DEP,'word_sha256':sha,'flags':flags,'new_coordinate_flag_charts':created,'bus_only_operations':bus_ops,'bill':bill,'all_input_columns':222,'completed_Y_roles':list(range(8)),'uncompleted_Y_roles':list(range(8,111)),'actual_exchange_observations':observations,'owned_clear_values':clear_values,'negative_controls':controls,'increment_over_direct_original_routes_and_one_packet':dict(sorted((k,v) for k,v in delta.items() if v)),'increment_moment':r.interval_record(r.moment(delta)),'plain_uncoded_orthogonal_bus_tiling_minimum_packets':14,'plain_tiling_optimistic_profile':{7:222,8:14},'plain_tiling_limiting_deficit':r.interval_record(deficit),'scope':'Literal finite scalar F2 word and universal two-ADD identity. Every chart nesting and input coefficient checked. Whole-word physical compiler, uniformity and owned-erasure remain; no complete111-target Q or new kappa. Plain disjoint frame buses cannot reach target even under direct-route grants; coded cross-frame use remains open.'}
    (a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','bus_only_operations','bill','new_coordinate_flag_charts','plain_tiling_limiting_deficit']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
