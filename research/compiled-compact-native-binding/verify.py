"""Cold stdlib replay of the scoped current Compact encoding/geometry join."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from time import monotonic

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from binding_sources import authenticate,need

def stable(value):
    if isinstance(value,dict):return {k:stable(v) for k,v in value.items() if k!='seconds'}
    if isinstance(value,(list,tuple)):return [stable(x) for x in value]
    return value

def source_control():
    manifest=json.loads((HERE/'DEPENDENCIES.json').read_text())
    names={'vendor/lifecycle/machine.py','vendor/ordinary/source.py'}
    subset=dict(manifest,files=[r for r in manifest['files'] if r['local_path'] in names],archive_members=[])
    with tempfile.TemporaryDirectory(prefix='compact-source-rejection-') as directory:
        root=Path(directory)
        for name in names:
            target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(HERE/name,target)
        (root/'DEPENDENCIES.json').write_text(json.dumps(subset))
        with (root/'vendor/lifecycle/machine.py').open('ab') as f:f.write(b'\n# changed source control\n')
        try:authenticate(root)
        except ValueError:return 'altered_public_export_rejected_before_import'
    raise ValueError('changed frozen source accepted')

def check(suite):
    count=authenticate()
    selected=json.loads((HERE/'vendor/SELECTED-RESULT.json').read_text())
    need(selected['kappa']=='781451/250000000' and 6030 in selected['source_prs'],'frozen selected source')
    assumptions=sorted(x['id'] for x in selected['assumptions'])
    need(set(assumptions)=={'native_all_columns','owned_erasure','compiler','precision_tape','analytic_recovery'},
         'all five selected assumptions retained')
    report=dict(exports=count,source_control=source_control(),selected_kappa=selected['kappa'],assumptions=assumptions)
    if suite in ('all','quick'):
        import check_records_cost,check_geometry,check_controls
        report['records_cost']=check_records_cost.run()
        report['geometry']=check_geometry.run()
        report['controls']=check_controls.run()
        from check_fixture import run_case
        report['single_bit']=run_case(f=1,K=2,H=1,rho=0,rows=1)
    if suite in ('all','early'):
        from check_fixture import run_case
        report['early']=run_case(f=2,K=1,H=1,late=False)
    if suite in ('all','late'):
        from check_fixture import run_case
        report['late']=run_case(f=2,K=1,H=1,late=True)
    return stable(report)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--suite',choices=('all','quick','early','late'),default='all')
    parser.add_argument('--write-result',action='store_true')
    args=parser.parse_args();start=monotonic()
    result=check(args.suite)
    payload=json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    receipt=dict(schema_version=1,scope='source-level fixed-tape Compact provider on current coded ABI',
                 sha256=hashlib.sha256(payload).hexdigest(),result=result)
    if args.write_result:
        need(args.suite=='all','only a complete receipt may replace RESULT.json')
        (HERE/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    elif args.suite=='all':
        need(json.loads((HERE/'RESULT.json').read_text())==receipt,'complete exact replay receipt differs')
    print(json.dumps(dict(**receipt,elapsed_seconds=round(monotonic()-start,3)),sort_keys=True))
    print('PASS_COMPILED_COMPACT_NATIVE_BINDING_'+args.suite.upper())

if __name__=='__main__':main()
