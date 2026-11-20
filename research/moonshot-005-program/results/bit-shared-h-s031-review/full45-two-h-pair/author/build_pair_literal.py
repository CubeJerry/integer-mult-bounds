#!/usr/bin/env python3
"""Materialize the admitted width12 pair source; independent check uses literals."""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
base=args.repo/'research/moonshot-005-program/results'
f=load(base/'bit-spread-disjoint-h-sources/author/families.py','retained_families')
p=load(base/'bit-spread-overlap-source/author/pair.py','retained_pair')
a=f.Atlas(args.repo);prm=json.loads((base/'bit-spread-overlap-source/author/output/PARAMETERS.json').read_text())['pair']
# The predecessor's allocation differs from the protected S031 component.
# Keep the algebra, but use the actual current global nine/36 port split.
a.marked=set(json.loads(gzip.decompress((base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz').read_bytes()))['selected_D'])
original_early=f.Chart.early
def find_early(self,j,maps,seed,fixed_centres=()):
    for candidate in range(64):
        try:original_early(self,j,maps,candidate,fixed_centres)
        except ValueError:continue
        prm['12']['early'][str(j)]=candidate
        return
    raise ValueError('no early frame among64 candidates')
f.Chart.early=find_early
found=False
for core in range(32):
    for fill in range(16):
        prm['12']['core']=core;prm['12']['fill']=fill
        try:charts,maps,status=p.pair_source(a,f,12,prm)
        except ValueError as exc:
            print('PAIR_TRIAL_REJECTED',core,fill,str(exc),flush=True)
            continue
        found=True;break
    if found:break
if not found:raise AssertionError('finite coefficient search exhausted')
print('PAIR_CURRENT_ALLOCATION_PARAMETERS',prm['12'],flush=True)
value={'parameters':prm,'status':status,'maps':{str(j):{str(h):M.tolist()for h,M in row.items()}for j,row in maps.items()},
       'H':{str(C.h):{'ports':C.ports,'donors':C.donors,'word':C.V.tolist()}for C in charts}}
payload=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(gzip.compress(payload,mtime=0))
print('MATERIALIZED_RETAINED_WIDTH12_PAIR',hashlib.sha256(payload).hexdigest(),flush=True)
