#!/usr/bin/env python3
"""Rebuild the optional independent true small-sector phase check."""
import argparse,subprocess,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--matrix',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
repo=a.repo.resolve();here=Path(__file__).resolve().parent;home=here.parents[1];result=repo/'research/moonshot-005-program/results';h=result/'bit-spread-rs-physical-word/author';stream=result/'bit-native-rs-return-distance/stream';k=result/'bit-gf64-actual-k-atlas/author/output';d=result/'bit-minimum-cache-d-atlas/author/output';py=[sys.executable,'-I','-B']
with tempfile.TemporaryDirectory(prefix='independent-phase-') as path:
    tmp=Path(path);mul=tmp/'mul.so';inv=tmp/'inv.so';en=tmp/'stream.so'
    for source,target in ((h/'gf64_matmul.c',mul),(here/'invert.c',inv),(stream/'stream.c',en)):
        subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared',str(source),'-o',str(target)],check=True)
    subprocess.run(py+[str(home/'verify.py'),'--repo',str(repo),'--out',str(tmp/'gauges'),'--emit-gauges'],check=True)
    subprocess.run(py+[str(here.parent/'physical_lift.py'),'--repo',str(repo),'--matrix',str(a.matrix),'--out',str(tmp/'lift'),'--emit-kernel'],check=True)
    subprocess.run(py+[str(home/'author/native_quotient.py'),'--repo',str(repo),'--replay',str(result/'bit-physical-terminal-quotient/author'),'--engine',str(stream),'--h-words',str(h/'output'),'--d-words',str(d),'--k-words',str(k),'--stream-lib',str(en),'--out',str(tmp/'quotient'),'--sector','small'],check=True)
    subprocess.run(py+[str(here/'check.py'),'--repo',str(repo),'--h-author',str(h),'--fast-author',str(here),'--k-words',str(k),'--d-charts',str(d/'CHARTS.json.gz'),'--library',str(mul),'--inv-lib',str(inv),'--kernel',str(tmp/'lift/FULL-SMALL-KERNEL.npz'),'--gauges',str(tmp/'gauges/SMALL-GAUGES.npz'),'--quotient',str(tmp/'quotient/SMALL.npz'),'--out',str(a.out)],check=True)
