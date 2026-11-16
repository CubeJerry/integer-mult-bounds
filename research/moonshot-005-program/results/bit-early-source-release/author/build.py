#!/usr/bin/env python3
"""Release old decoder-held originals before subsequent principal Hub loads."""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path

GROUPS=[([3,21],[21,1],[1,21,10]),([76,64],[64,73],[73,64,61]),([80,65],[65,77],[77,65,67]),([4],[6],[6]),([74],[75],[75]),([78],[79],[79])]
EXPECTED='9053904c95084269c8d2df3f883a8c32dfadff763a2c0338a5ebf7c45d4d6267'

def load(path):
    sp=importlib.util.spec_from_file_location('independent_source_replay',path);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);return e

def initial():
    return ({f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)},
            {f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)})

def step(v,at,op):
    kind,n,*q=op
    if kind=='INIT':v[n]=0;at[n]=q[0]
    elif kind=='ADD':v[q[0]]^=v[n]
    elif kind=='MOVE':at[n]=q[0]
    elif kind=='CLEAR':del v[n],at[n]

def representation(rows,target):
    pivots={}
    for k,row in enumerate(rows):
        selector=1<<k
        while row:
            bit=row.bit_length()-1
            if bit in pivots:r,q=pivots[bit];row^=r;selector^=q
            else:pivots[bit]=(row,selector);break
    selector=0
    while target:
        bit=target.bit_length()-1
        if bit not in pivots:return None
        r,q=pivots[bit];target^=r;selector^=q
    return selector

def main():
    parser=argparse.ArgumentParser()
    for n in ['repo','base','engine','out']:parser.add_argument('--'+n,type=Path,required=True)
    args=parser.parse_args();raw=args.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
    old=json.loads(raw);e=load(args.engine);source=(args.repo/old['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==old['source_sha256'];roots=json.loads(source)['native_roots'];charts,old_history,before=e.replay(old,roots)
    ops=old['operations'];v,at=initial();reference=[]
    for op in ops:reference.append((v.copy(),at.copy()));step(v,at,op)
    first_decoder=min(k for k,o in enumerate(ops)if o[0]=='MOVE'and o[1]in {'Y3','Y21','Y76','Y64','Y80','Y65','Y4','Y74','Y78'})
    moved=set();blocks=[];anchors=[]
    for group,(ys,returns,restores)in enumerate(GROUPS):
        ynames={f'Y{i}'for i in ys};rnames={f'X{i}'for i in returns};dnames={f'X{i}'for i in restores}
        assert not any(o[0]=='ADD'and o[1]in ynames for o in ops)
        receiver=[k for k,o in enumerate(ops)if(o[0]=='ADD'and o[2]in ynames)or(o[0]=='MOVE'and(o[1]in ynames or(o[1]in rnames and o[2]=='Hub')))]
        restoration=[k for k,o in enumerate(ops)if k>=first_decoder and o[0]=='ADD'and o[2]in dnames]
        assert receiver and restoration and all(reference[k][1][ops[k][1]]=='Hub'for k in restoration)
        block=receiver+restoration;assert not moved&set(block);moved.update(block);blocks.append(block)
        if group<5:
            target=f'P{group+1}'
            anchor=next(k for k,o in enumerate(ops)if o[0]=='ADD'and o[2]==target and reference[k][1][target]=='Hub')
        else:anchor=first_decoder
        assert max(k for k,o in enumerate(ops[:anchor])if o[0]=='MOVE'and o[1]==f'P{group}'and o[2]=='zero')<anchor
        anchors.append(anchor)
    assert len(set(anchors))==6
    v,at=initial();new=[];repairs=[];release_reports=[];stage_sources=[]
    def emit(k):
        op=ops[k];kind,name,*q=op
        if kind=='ADD':
            desired=reference[k][0][name]
            assert charts[at[name]]==charts[at[q[0]]],('source chart',k,op,at[name],at[q[0]])
            if v[name]!=desired:
                assert name.startswith('X')and at[name]=='Hub'and not desired>>111,('untranslatable source',k,op)
                donors=[f'X{i}'for i in range(111)if at[f'X{i}']=='Hub'and f'X{i}'!=q[0]]
                selector=representation([v[n]for n in donors],desired);assert selector is not None,('Hub reconstruction missing',k,op)
                replacement=[['ADD',n,q[0]]for j,n in enumerate(donors)if selector>>j&1]
                assert replacement
                for instruction in replacement:new.append(instruction);step(v,at,instruction)
                repairs.append({'old_step':k,'old_instruction':op,'old_row_hex':hex(desired),'replacement':replacement})
                return
        new.append(copy.deepcopy(op));step(v,at,op)
    def hub_report(label):
        rows=[v[f'X{i}']for i in range(111)if at[f'X{i}']=='Hub'];known=[i for i in range(111)if e.fits(rows,1<<i)]
        return {'label':label,'new_step':len(new),'actual_Hub_original_rank':len(e.bb(rows)),'raw_columns_available':known,'missing_raw_columns':sorted(set(range(111))-set(known))}
    for k,op in enumerate(ops):
        if k in anchors:
            group=anchors.index(k)
            assert at[f'P{group}']=='zero'
            for old_index in blocks[group]:emit(old_index)
            for i in GROUPS[group][2]:assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
            release_reports.append(hub_report('after_group_'+str(group)))
        if k in moved:continue
        if op[0]=='ADD'and op[2]in [f'P{i}'for i in range(6)]and at[op[2]]=='Hub'and not any(x['label']==op[2]for x in stage_sources):stage_sources.append(hub_report(op[2]))
        emit(k)
    word=copy.deepcopy(old);word.update(operations=new,schema='early-held-original-release-v1',base_word_sha256=EXPECTED,scope='Same partial endpoints and all owned source values; legacy receivers and original restorations run early, and changed Hub source reads use actual equal-row recipes. Movement unchanged; no all111 supplier or new kappa.')
    C,H,after=e.replay(word,roots)
    assert Counter((n,charts[c],v)for _,n,c,v in old_history)==Counter((n,C[c],v)for _,n,c,v in H)
    assert after['movement_profile']==before['movement_profile']
    for key in ['INIT','MOVE','CLEAR']:assert after['counts'][key]==before['counts'][key]
    assert after['dirty_CLEAR']==before['dirty_CLEAR']and after['peak_owned']==before['peak_owned']
    assert sorted(o for o in old['operations']if o[0]=='MOVE')==sorted(o for o in new if o[0]=='MOVE')
    # Full original values and explicit protected contracts remain independently
    # checked; the new code does not infer a larger source space from endpoint
    # equality alone.
    expected=old['protected_source_contracts'];nv,na=initial();contracts={}
    for op in new:
        if op[0]=='CLEAR'and op[1]in expected:contracts[op[1]]={'value_hex':hex(nv[op[1]]),'chart':na[op[1]]}
        step(nv,na,op)
    assert contracts==expected
    controls=[]
    if repairs:
        bad=copy.deepcopy(word);index=next(i for i in range(len(new))if new[i:i+len(repairs[0]['replacement'])]==repairs[0]['replacement'])
        bad['operations'][index:index+len(repairs[0]['replacement'])]=[repairs[0]['old_instruction']]
        try:e.replay(bad,roots)
        except(AssertionError,KeyError)as ex:controls.append({'omitted_Hub_reconstruction':repairs[0]['old_instruction'],'failure':str(ex)})
        else:raise AssertionError('Dropped Hub repair accepted')
    for omit in [['ADD','X21','Y3'],['ADD','X10','X21']]:
        bad=copy.deepcopy(word);omitted_index=max(i for i,o in enumerate(bad['operations'])if o==omit);bad['operations'].pop(omitted_index)
        try:e.replay(bad,roots)
        except(AssertionError,KeyError)as ex:controls.append({'omitted':omit,'failure':str(ex)})
        else:raise AssertionError(('Dropped release prerequisite accepted',omit))
    args.out.mkdir(parents=True,exist_ok=True);encoded=(json.dumps(word,indent=2)+'\n').encode();(args.out/'WORD.json').write_bytes(encoded)
    result={'status':'PASS_EARLY_RELEASE_WITH_EXPANDED_ACTUAL_HUB_SOURCES','word_sha256':hashlib.sha256(encoded).hexdigest(),'base_word_sha256':EXPECTED,'native_source_sha256':old['source_sha256'],'before':before,'after':after,'release_groups':[{'receivers':a,'returning_originals':b,'restored_originals':c,'old_operation_indices':d,'anchor_old_step':anchor}for(a,b,c),d,anchor in zip(GROUPS,blocks,anchors)],'actual_Hub_sources_before_principal_loads':stage_sources,'actual_Hub_sources_after_releases':release_reports,'Hub_source_reconstructions':repairs,'retained_protected_source_contracts':contracts,'movement_multiset_identical':True,'full_222_column_history_multiset_identical_in_field_chart_and_value':True,'negative_controls':controls,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'word_sha256':result['word_sha256'],'after':after,'source_ranks':[x['actual_Hub_original_rank']for x in stage_sources],'release_ranks':[x['actual_Hub_original_rank']for x in release_reports],'Hub_repairs':len(repairs)}))

if __name__=='__main__':main()
