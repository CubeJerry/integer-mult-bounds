#!/usr/bin/env python3
"""Replace specified isolated Y decoders, then remove their dead source work."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from optimize_word import dead_pass,fuse_routes,independent_replay


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--points',type=int,nargs='+',required=True);p.add_argument('--protect',nargs='*',default=[]);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();old=json.loads(raw);before=independent_replay(old);points=set(a.points);names={f'Y{i}':i for i in points}
    assert points<=set(old['targets'])
    assert not any(o[0]=='ADD'and o[1]in names for o in old['operations'])
    ops=[]
    for i in sorted(points):ops.extend([['INIT',f'DIRECT_RAW{i}',f'L{i}'],['ADD',f'X{i}',f'DIRECT_RAW{i}'],['MOVE',f'DIRECT_RAW{i}','zero']])
    for o in old['operations']:
        if o[0]=='ADD'and o[2]in names:continue
        if o[0]=='MOVE'and o[1]in names:
            i=names[o[1]]
            if o[2]==f'F{i}':ops.extend([['ADD',f'DIRECT_RAW{i}',o[1]],o])
            continue
        ops.append(o)
    ops += [['CLEAR',f'DIRECT_RAW{i}']for i in sorted(points)]
    w={k:copy.deepcopy(old[k])for k in ['source_path','source_sha256','charts','targets']};w['operations']=ops
    direct=independent_replay(w);rounds=[]
    for _ in range(12):
        count=len(w['operations']);w,d=dead_pass(w,keep_owned=a.protect);w,m=fuse_routes(w);rounds.append({'dead':d,'fused_moves':m})
        if len(w['operations'])==count:break
    else:raise AssertionError('not stabilized')
    before_birth=independent_replay(w)
    uses={}
    for k,o in enumerate(w['operations']):
        if o[0]=='INIT':uses[o[1]]=[(k,o)]
        else:
            for name in o[1:]:
                if name in uses:uses[name].append((k,o))
    changes={};remove=set();witnesses=[]
    for name,events in uses.items():
        prefix=[]
        for k,o in events[1:]:
            if o[0]=='MOVE':prefix.append((k,o))
            else:break
        if not prefix:continue
        changes[name]=prefix[-1][1][2];remove.update(k for k,_ in prefix);witnesses.append({'owner':name,'old_birth':events[0][1][2],'new_birth':changes[name],'empty_moves':prefix,'first_nonmove_use':events[len(prefix)+1]})
    w['operations']=[(['INIT',o[1],changes[o[1]]]if o[0]=='INIT'and o[1]in changes else o)for k,o in enumerate(w['operations'])if k not in remove]
    after=independent_replay(w)
    def retained(word):
        values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};seen={}
        for op,n,*q in word['operations']:
            if op=='INIT':values[n],at[n]=0,q[0]
            elif op=='ADD':values[q[0]]^=values[n]
            elif op=='MOVE':at[n]=q[0]
            elif op=='CLEAR':
                if n in a.protect:seen[n]={'value_hex':hex(values[n]),'chart':at[n]}
                del values[n],at[n]
        assert set(seen)==set(a.protect)
        return seen
    retained_before,retained_after=retained(old),retained(w);assert retained_before==retained_after
    w.update(schema='isolated-point-service-replacement-v1',base_word_sha256=hashlib.sha256(raw).hexdigest(),direct_points=sorted(points),protected_source_contracts=retained_after,scope='Partial endpoints and explicitly protected source values/charts only; expensive point services replaced by fully paid native raw returns and exact dead-code/birth reduction. Other source/history must be audited anew.')
    price_path=a.repo/'research/moonshot-005-program/results/bit-composed-coded-source/author/price.py';spec=importlib.util.spec_from_file_location('price',price_path);price=importlib.util.module_from_spec(spec);spec.loader.exec_module(price);bill=price.invoice(after['movement_profile'])
    delta={d:after['movement_profile'].get(d,0)-before['movement_profile'].get(d,0)for d in range(1,9)}
    controls=[]
    for i in sorted(points):
        for op in [['ADD',f'X{i}',f'DIRECT_RAW{i}'],['MOVE',f'DIRECT_RAW{i}','zero'],['ADD',f'DIRECT_RAW{i}',f'Y{i}']]:
            bad=copy.deepcopy(w);bad['operations'].remove(op)
            try:independent_replay(bad)
            except AssertionError:controls.append(op)
            else:raise AssertionError(('accepted omission',op))
    a.out.mkdir(parents=True,exist_ok=True);blob=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(blob)
    report={'status':'PASS_ACTUAL_ISOLATED_POINT_SERVICE_REPLACEMENT','word_sha256':hashlib.sha256(blob).hexdigest(),'base_word_sha256':w['base_word_sha256'],'points':sorted(points),'before':before,'direct_before_reduction':direct,'before_birth_relocations':before_birth,'after':after,'protected_source_contracts':retained_after,'birth_relocations':witnesses,'signed_movement_difference':{d:n for d,n in delta.items()if n},'reduction_rounds':rounds,'semantic_controls':controls,'scope':w['scope'],'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'PRICE.json').write_text(json.dumps(bill,indent=2)+'\n');print(report['word_sha256'],after['counts'],'Q',bill['moment']['lower'],'room',bill['limiting_room']['lower'],'births',changes)


if __name__=='__main__':main()
