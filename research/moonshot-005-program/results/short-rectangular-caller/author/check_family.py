#!/usr/bin/env python3
"""Parity controls and exact a9 predecessor comparison; not independent review."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,subprocess,sys
import build
HERE=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    pins=json.loads((HERE/'source/PINS.json').read_text())
    for p in pins:need(hashlib.sha256((HERE/'source'/p['file']).read_bytes()).hexdigest()==p['sha256'],'source pin '+p['file'])
    old=json.loads((HERE/'source/root_A_efree.json').read_text());a=9;n=38;L=19;xy=[]
    for i in range(1,a+1):
        for off in(0,L):
            x=build.vec(n,(off,1),(off+i,1),*[(off+j,2)for j in range(1,i)])
            y=build.vec(n,(off,1),(off+i,-1));xy.append((x,y))
    thin=[build.thin(a,n,off)for off in(0,L)]
    xy.extend((w,e)for w,e,v,y in thin);xy.extend((v,y)for w,e,v,y in thin)
    for i in range(1,a+1):
        for off in(0,L):
            x=build.vec(n,(off,-1),(off+a+i,1),*[(off+a+j,2)for j in range(i+1,a+1)])
            y=build.vec(n,(off,1),(off+a+i,1));xy.append((x,y))
    need(len(xy)==40 and all(x==list(map(F,xx))and y==list(map(F,yy))for(x,y),xx,yy in zip(xy,old['X'],old['Y'])),'a9 exactly reproduces inherited X/Y')
    results={}
    for a in(1,2,4,9):
        out=HERE/'controls'/('a'+str(a));build.main(out,a,17)
        subprocess.run([sys.executable,'-B',str(HERE/'replay.py'),str(out/'CALLER.json.gz'),'--out',str(out/'REPLAY.json')],check=True,capture_output=True,text=True)
        results[str(a)]=dict(caller_sha256=hashlib.sha256((out/'CALLER.json.gz').read_bytes()).hexdigest(),replay_sha256=hashlib.sha256((out/'REPLAY.json').read_bytes()).hexdigest())
    need((HERE/'controls/a4/CALLER.json.gz').read_bytes()==(HERE/'a4-h18/CALLER.json.gz').read_bytes(),'byte deterministic a4 rebuild')
    need((HERE/'a4-h18/REPLAY.json').read_bytes()==(HERE/'a4-h18/REPLAY-OPTIMIZED.json').read_bytes(),'optimized replay agreement')
    R=dict(status='PASS_PARITY_AND_SOURCE_CONTROLS',a9_all_40_source_units_equal=True,normal_optimized_target_replay_equal=True,source_pins_checked=len(pins),parity_cases=results,scope='Finite exact family/source controls supplement the universal proof; they are not independent review.')
    (HERE/'FAMILY-CONTROLS.json').write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(json.dumps(R,sort_keys=True))
if __name__=='__main__':main()
