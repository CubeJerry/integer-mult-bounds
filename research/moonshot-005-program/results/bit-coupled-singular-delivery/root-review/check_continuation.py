#!/usr/bin/env python3
"""Root's separate symbolic and dual-certificate check, all 222 inputs."""
import argparse,hashlib,json
from pathlib import Path

def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b
def contains(b,x):
    while x:
        p=x.bit_length()-1
        if p not in b:return False
        x^=b[p]
    return True

p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--gate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
raw=a.source.read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
roots=json.loads(raw)['native_roots'];word=json.loads(a.word.read_text());gate=json.loads(a.gate.read_text())
assert hashlib.sha256(a.word.read_bytes()).hexdigest()==gate['word_sha256']
v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
for op in word['operations']:
    if op[0]=='INIT':assert op[1] not in v;v[op[1]]=0
    elif op[0]=='ADD':v[op[2]]^=v[op[1]]
    elif op[0]=='CLEAR':del v[op[1]]
    elif op[0]!='MOVE':raise AssertionError(op)
donors=[16,19,38,49,50,56,57]
rows=[v[f'P{i}'] for i in range(8)]+[1<<j for j in donors]
assert all(x < 1<<111 for x in rows)
assert all(v[f'X{i}']==1<<i for i in range(111))
for i in range(111):assert v[f'Y{i}']==((1<<(111+i))^((1<<i) if i in (17,34) else 0))
published=[int(x,16) for x in gate['global_rows_hex']]
assert len(basis(rows))==len(basis(published))==len(basis(rows+published))==15
outs=[];fits=[]
for i,r in enumerate(roots):
    mask=sum(1<<j for j,s in enumerate(roots) if sum(x*y for x,y in zip(r,s))!=0)
    outs.append(mask)
    if contains(basis([x&mask for x in rows]),1<<i):fits.append(i)
assert fits==gate['feasible_receivers']==[16,17,19,38,49,50,56,57,59,60]
failed=set(range(111))-set(fits)
assert len(gate['infeasible_duals'])==101
for q in gate['infeasible_duals']:
    i=q['role'];z=int(q['dual_hex'],16)
    assert i in failed and z & (1<<i) and not z & ~outs[i]
    assert all((z&r).bit_count()%2==0 for r in rows)
    failed.remove(i)
assert not failed
frame=[0,15,31,35,40,41,106,110]
assert not set(frame)&set(donors+[17,34])
assert all(sum(x*y for x,y in zip(roots[i],roots[j]))==(4 if i==j else 2) for i in frame for j in frame)
restricted=[sum(((r>>j)&1)<<i for i,j in enumerate(frame)) for r in rows]
duals=[49,90,146]
assert len(basis(restricted))==5 and len(basis(duals))==3
assert all((x&z).bit_count()%2==0 for x in restricted for z in duals)
result={'status':'PASS_ROOT_FROZEN_HANDOFF_AND_101_DUALS','formal_inputs':222,'global_rank':15,'feasible_receivers':fits,'exact_duals_verified':101,'already_completed':[17,34],'currently_unserved_blocked':100,'shared_export_frame':frame,'frame_gram_diagonal':4,'frame_gram_off_diagonal':2,'restricted_global_rank':5,'independent_frame_duals':duals,'necessary_new_information':'3V','scope':'No further owned descent/new nonlocal source for the101-dual gate. Frame cut requires3V new information under actual ingress accounting. Neither excludes changed source schedules.','new_kappa':False}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
