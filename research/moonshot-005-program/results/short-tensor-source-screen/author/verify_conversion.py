#!/usr/bin/env python3
"""Exact caller-level B-to-HOST2 identity over Q[Q,D]/(Q^4-1)."""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent
EVENTS=[['SCALE',1,'1/2'],['QUERY',0,1,1],['COUPLED',0,1],['SCALE',1,'2'],['SCALE',2,'-1'],['QUERY',2,3,1],['SCALE',2,'-1'],['IDLE',2],['IDLE',3]]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def transform(row,c=F(1),q=0,d=0):return{(i,(j+q)%4,k+d):c*v for(i,j,k),v in row.items()if c*v}
def add(A,B):
    R=A.copy()
    for k,v in B.items():
        R[k]=R.get(k,F(0))+v
        if not R[k]:del R[k]
    return R
def replay(skip=None):
    R=[{(i,0,0):F(1)}for i in range(4)]
    for k,e in enumerate(EVENTS):
        if k==skip:continue
        if e[0]=='SCALE':R[e[1]]=transform(R[e[1]],F(e[2]))
        elif e[0]=='QUERY':R[e[1]]=add(R[e[1]],transform(R[e[2]],q=e[3]))
        elif e[0]=='IDLE':R[e[1]]=transform(R[e[1]],d=1)
        else:
            x,y=e[1:];A=R[x];B=R[y]
            R[x]=transform(add(A,transform(B,F(-1),q=1)),d=1)
            R[y]=transform(add(transform(A,F(1,2),q=-1),transform(B,F(1,2))),d=1)
    return R
def main():
    want=[{(0,0,1):F(1)},{(1,0,1):F(1),(0,3,1):F(1)},{(2,0,1):F(1),(3,1,1):F(-1)},{(3,0,1):F(1)}]
    need(replay()==want,'full exact four-input HOST2 endpoint')
    controls={str(i):replay(skip=i)!=want for i in(0,1,2,5,7)};need(all(controls.values()),'actual local deletion controls')
    C=json.loads((HERE/'source/retained-caller.json').read_text());Js=[e for e in C['events']if e[0]=='J']
    need(len(Js)==18 and all(F(e[3][2])==-1 and F(e[3][3])==F(1,2)for e in Js),'actual coupled coefficient pin')
    W=json.loads((HERE/'source/retained-FULL-RESULT.json').read_text());h=W['native']['helpers'];need(sum(h.values())==1080,'unchanged1080 independent native helpers')
    R=dict(status='PASS_CALLER_LEVEL_B_CONVERSION',events=EVENTS,counts=dict(Counter(e[0]for e in EVENTS)),source_sha256=hashlib.sha256((HERE/'source/retained-caller.json').read_bytes()).hexdigest(),
      exact_endpoint='D*(X, Y+Q^-1 X, U-Q V, V)',paid_addition_per_B_port_per_stage={'1':2,'8':2},native_helper_count=1080,negative_controls=controls,
      scope='Caller-level ordinary/QUERY/body-idle simulation of one coupled native contact. Not a native word conversion or free native HOST2 assertion.')
    (HERE/'CONVERSION.json').write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(R['status'])
if __name__=='__main__':main()
