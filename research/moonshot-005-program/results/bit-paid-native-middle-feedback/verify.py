#!/usr/bin/env python3
"""Verify two native cache-feedback words and all genuinely changed proper branches."""
import argparse, gzip, json, subprocess, sys, tempfile
from pathlib import Path

def run(args):
    subprocess.run([str(x)for x in args],check=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--heavy',action='store_true',help='rebuild the original 10656-square matrix and re-synthesize both words')
    a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();out.mkdir(exist_ok=True,parents=True)
    home=Path(__file__).resolve().parent;base=repo/'research/moonshot-005-program/results'
    native=base/'bit-native-rs-return-distance';h=base/'bit-spread-rs-physical-word/author'
    d=base/'bit-minimum-cache-d-atlas/author/output';k=base/'bit-gf64-actual-k-atlas/author/output'
    def py(file,options):
        run([sys.executable,'-I','-B',file,*options])
    def equal(actual,baseline):
        if json.loads(actual.read_bytes())!=json.loads(baseline.read_bytes()):
            raise ValueError('replay discrepancy in '+str(baseline))
    with tempfile.TemporaryDirectory(prefix='true-d-f-feedback-')as td:
        tmp=Path(td);cc=['cc','-std=c11','-O3','-march=native','-fPIC','-shared']
        run([*cc,native/'stream/stream.c','-o',tmp/'stream.so'])
        for name in ('d','joint'):
            dest=tmp/name;dest.mkdir();ref=home/'author'/name
            (dest/'KERNEL.npy').write_bytes(gzip.decompress((ref/'KERNEL.npy.gz').read_bytes()))
            (dest/'RESULT.json').write_bytes((ref/'RESULT.json').read_bytes())
        if a.heavy:
            run([*cc,h/'gf64_matmul.c','-o',tmp/'mul.so'])
            run([*cc,'-I',native/'author',home/'author/solve.c','-o',tmp/'solve.so'])
            author=['--repo',repo,'--transfer',h,'--k-words',k,'--d-charts',d/'CHARTS.json.gz','--mult',tmp/'mul.so']
            py(native/'author/build_minor.py',[*author,'--rank-lib',tmp/'solve.so','--sector','small','--mode','all','--build-only','--out',tmp/'matrix'])
            args=[*author,'--solve',tmp/'solve.so','--matrix',tmp/'matrix']
            py(home/'author/feedback.py',[*args,'--out',tmp/'d-new'])
            py(home/'author/facets.py',[*args,'--prior',tmp/'d-new','--out',tmp/'joint-new'])
            for name in ('d','joint'):
                fresh=tmp/(name+'-new');old=tmp/name;equal(fresh/'RESULT.json',old/'RESULT.json')
                if (fresh/'KERNEL.npy').read_bytes()!=(old/'KERNEL.npy').read_bytes():raise ValueError('reconstructed '+name+' kernel')
        common=['--repo',repo,'--replay',base/'bit-physical-terminal-quotient/author','--engine',native/'stream','--h-words',h/'output','--d-words',d,'--k-words',k,'--stream-lib',tmp/'stream.so','--feedback',tmp/'d']
        py(home/'review/d/check.py',[*common,'--out',out/'d'])
        py(home/'review/joint/check.py',[*common,'--joint',tmp/'joint','--out',out/'joint'])
        py(home/'review/joint/foreign.py',['--repo',repo,'--d-feedback',tmp/'d','--joint',tmp/'joint','--out',out/'joint'])
        for name,files in [('d',['RESULT.json']),('joint',['RESULT.json','FOREIGN.json'])]:
            for f in files:equal(out/name/f,home/'review'/name/f)
    D=json.loads((out/'d/RESULT.json').read_bytes());J=json.loads((out/'joint/RESULT.json').read_bytes())
    report={'frozen_actual_return_fields':426240,'D_only_actual_rank':426240-D['fixed_bank_return_rank_decrease'],'joint_D_F_actual_rank':426240-J['all_copy_return_fields_saved'],'D_only_binary_return_MOVEs_saved':6*D['fixed_bank_return_rank_decrease'],'joint_binary_return_MOVEs_saved':6*J['all_copy_return_fields_saved'],'D_only_extra_ADDs':D['extra_ADDs_at_3840'],'joint_extra_ADDs':J['total_extra_ADDs'],'additional_INIT_each_and_dirty_CLEAR_each':0,'additional_proper_MOVEs':0,'admitted_multiplier_supplier':False}
    (out/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report)
if __name__=='__main__':main()
