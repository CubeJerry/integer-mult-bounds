#!/usr/bin/env python3
"""Replace the now-expensive old Y2 backup with a real native raw2 return."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from optimize_word import independent_replay


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.base.read_bytes();base=json.loads(raw);before=independent_replay(base);ops=base['operations']
    assert not any(o[0]=='ADD'and o[1]=='Y2'for o in ops)
    anchor=ops.index(['ADD','ZFIRST3','P3'])
    assert ops[anchor+1:anchor+5]==[['ADD','H6_0','P3'],['ADD','Q2','P3'],['ADD','P3','BACK2'],['ADD','BACK2','P3']]
    result=[['INIT','COMMON_RAW2','L2'],['ADD','X2','COMMON_RAW2'],['MOVE','COMMON_RAW2','zero']]
    for k,o in enumerate(ops):
        if k in [anchor+1,anchor+2] or 'BACK2'in o:continue
        if o[0]=='ADD'and o[2]=='Y2':continue
        if o[0]=='MOVE'and o[1]=='Y2':
            if o[2]=='F2':result.extend([['ADD','COMMON_RAW2','Y2'],o])
            continue
        result.append(o)
    result.append(['CLEAR','COMMON_RAW2'])
    word={k:copy.deepcopy(base[k])for k in ['source_path','source_sha256','charts','targets']}
    word.update(operations=result,schema='native-raw2-backup-replacement-v1',base_word_sha256=hashlib.sha256(raw).hexdigest(),scope='Same partial endpoints; expensive BACK2 source/route and old Y2 code replaced by a fully paid native raw2 return. Old source metadata is not inherited.')
    after=independent_replay(word)
    delta={d:after['movement_profile'].get(d,0)-before['movement_profile'].get(d,0)for d in range(1,9)}
    assert {d:n for d,n in delta.items()if n}=={1:-1,3:-1,5:-1,7:1}
    module_path=a.repo/'research/moonshot-005-program/results/bit-composed-coded-source/author/price.py';spec=importlib.util.spec_from_file_location('price',module_path);price=importlib.util.module_from_spec(spec);spec.loader.exec_module(price)
    bill=price.invoice(after['movement_profile'])
    controls=[]
    for deletion in [['ADD','X2','COMMON_RAW2'],['MOVE','COMMON_RAW2','zero'],['ADD','COMMON_RAW2','Y2'],['CLEAR','COMMON_RAW2']]:
        bad=copy.deepcopy(word);bad['operations'].remove(deletion)
        try:independent_replay(bad)
        except AssertionError:controls.append(deletion)
        else:raise AssertionError(('accepted omission',deletion))
    a.out.mkdir(parents=True,exist_ok=True);encoded=(json.dumps(word,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(encoded)
    report={'status':'PASS_ACTUAL_RAW2_BACKUP_REPLACEMENT','base_word_sha256':word['base_word_sha256'],'word_sha256':hashlib.sha256(encoded).hexdigest(),'before':before,'after':after,'exact_movement_difference':'[7]-[5]-[3]-[1]','all_old_partial_endpoints_retained':True,'source_metadata_not_inherited':True,'semantic_controls':controls,'scope':'Literal all222-column endpoint and geometry/custody proof; new raw2 transport is paid; no full supplier or new kappa.'}
    (a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'PRICE.json').write_text(json.dumps(bill,indent=2)+'\n');print(report['word_sha256'],after['counts'],'Q',bill['moment']['lower'],'room',bill['limiting_room']['lower'])


if __name__=='__main__':main()
