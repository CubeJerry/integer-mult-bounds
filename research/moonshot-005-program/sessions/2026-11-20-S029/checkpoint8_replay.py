"""Recheck the individual native donor requirement and cross-check the S029 physical receipts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--physical',action='store_true',help='Also reconstruct the full shared-coefficient and two-sided original-owner words')
    a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(exist_ok=True,parents=True)
    R=repo/'research/moonshot-005-program/results';P=R/'bit-native-petersen-converse';E=R/'bit-native-prefix-suffix-stability'
    layout=R/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';w=P/'author/output'
    data={}
    def run(script,flags):
        subprocess.run([sys.executable,'-B',script,*flags],check=True,stdout=subprocess.DEVNULL)
    def audit(k,script,flags,name,reference):
        dest=out/k
        run(script,flags+['--out',dest])
        raw=(dest/name).read_bytes()
        if raw!=reference.read_bytes():raise ValueError(k)
        return k,sha256(raw).hexdigest()
    tasks=[('edge-floor',P/'author/horn.py',['--layout',layout,'--horn',w/'HORN.json.gz','--dual',w/'LOCAL-LEAK.json'],'HORN-RESULT.json',w/'HORN-RESULT.json'),
           ('edge-review',P/'review/arc_review.py',['--repo',repo,'--horn',w/'HORN.json.gz','--dual',w/'LOCAL-LEAK.json'],'RESULT.json',P/'review/output/ARC.json')]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for key,receipt in pool.map(lambda x:audit(*x),tasks):data[key]=receipt
    d=E/'author/output'
    run(E/'author/count.py',[d/'CHARTS.json.gz',d/'COUNT.json'])
    q=json.loads((d/'COUNT.json').read_bytes())
    data['necessary_D_chart_changes_if_endpoints_fixed_as_indicated']={k:v['minimum_D_nodes'] for k,v in q.items()}
    if data['necessary_D_chart_changes_if_endpoints_fixed_as_indicated']!={'L':712,'R':707,'LR':764}:
        raise ValueError('changed true D cut')
    W=R/'bit-native-low-rank-facet-retuning'
    run(W/'verify.py',['--repo',repo,'--out',out/'four-facet'])
    data['four-facet-price-and-rank']=sha256((out/'four-facet/RESULT.json').read_bytes()).hexdigest()
    M=R/'complex-native-contested-restoration'
    run(M/'verify.py',['--repo',repo,'--out',out/'complex'])
    data['complex']=json.loads((out/'complex/REPLAY.json').read_bytes())
    if a.physical:
        B=R/'bit-native-physical-replay/author'
        run(B/'check.py',['--repo',repo,'--out',out/'physical'])
        data['physical_receipts']={str(f.relative_to(out/'physical')):sha256(f.read_bytes()).hexdigest() for f in sorted((out/'physical').glob('*.json'))}
    (out/'VALIDATION.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
