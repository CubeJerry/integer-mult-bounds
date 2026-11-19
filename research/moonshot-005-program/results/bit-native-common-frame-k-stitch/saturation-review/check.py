#!/usr/bin/env python3
"""Independent K-boundary census and sparse-row saturation controls."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip,json
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','word':'806dca8703c7ca75854b91d9946f81c5df72b77614aa3b62b5a2e2c53692411a','certificate':'3b11e44b0fbb7b43b3f5699774935e8bd77e7096589ef8973f866d5a9f4e1cf1'}
XF=111*480*5;PUBLIC=2*XF

def load(path,key,jsonl=False):
    raw=gzip.decompress(path.read_bytes());assert sha256(raw).hexdigest()==PINS[key]
    return[json.loads(x)for x in raw.splitlines()]if jsonl else json.loads(raw)

def rank(rows):
    p={}
    for v in rows:
        while v:
            k=v.bit_length()-1
            if k in p:v^=p[k]
            else:p[k]=v;break
    return len(p)

def combine(rows,v):
    out=0
    for k,row in enumerate(rows):
        if v>>k&1:out^=row
    return out

def actual_support(W,field):
    bits=sorted({z for a in W['actions']for op in a['word']for z in op[1:]if z<PUBLIC});col={z:i for i,z in enumerate(bits)}
    values={z:1<<i for z,i in col.items()}
    for a in W['actions']:
        for op in a['word']:
            if op[0]=='INIT':values[op[1]]=0
            elif op[0]=='ADD':values[op[1]]^=values[op[2]]
            else:del values[op[1]]
        if a['tag']=='aggregate-Y-K-370':
            support=set()
            for bit in range(5):
                v=values[5*field+bit]
                while v:
                    low=v&-v;src=bits[low.bit_length()-1];v^=low
                    if src<XF:support.add(src//5//480)
            return support
    raise AssertionError('missing aggregate')

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results';L=load(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout')
    routes=load(base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','routes',True)
    W=load(a.author/'output/WORD.json.gz','word');C=load(a.author/'output/CERTIFICATE.json.gz','certificate')
    roots=L['root_table'];planes=list(map(set,L['A2']));dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    source={k:{j for j in range(111)if all(dot(j,h)==0 for h in H)}for k,H in enumerate(planes)}
    published=json.loads((a.author/'output/SYSTEM-SCREEN.json').read_text());records=[]
    for i in [80,1]:
        ks=[k for k,H in enumerate(planes)if i in H];assert len(ks)==28
        early=Counter(r[5]for r in routes if r[0]=='X'and r[7]==i);late=Counter(r[5]for r in routes if r[0]=='Y'and r[1]==i)
        assert sum(early.values())==360 and sum(late.values())==480 and set(early)|set(late)==set(ks)
        neighbors={j for j in range(111)if dot(i,j)==0};cuts={j:[k for k in ks if j in source[k]]for j in neighbors}
        assert all(len(v)==16 for v in cuts.values())and all(early[k]+late[k]==30 for k in ks)
        weighted=sum(30*len(source[k])for k in ks);assert weighted==len(neighbors)*480
        p=next(r for r in published['records']if r['receiver']==i)
        for d in p['K_details']:
            k=d['K'];assert d['native_source_support']==sorted(source[k])and d['early_terminal_capacity']==early[k]and d['late_terminal_capacity']==late[k]and d['total_terminal_capacity']==30
        assert {d['K']for d in p['K_details']}==set(ks)
        records.append({'receiver':i,'foreign_donors':len(neighbors),'verified_K_profiles':len(ks),'verified_donor_cuts':len(cuts),'early':360,'late':480,'weighted_capacity':weighted})
    group=next(g for g in C['late_K_aggregates']if g['K']==370);rr=next(r for r in routes if r[0]=='Y'and 111*480+r[1]*480+r[2]==group['output_field'])
    assert rr[5]==370 and rr[1]==1
    support=actual_support(W,group['output_field']);missing=source[370]-support
    assert len(source[370])==36 and len(support)==31 and missing=={15,69,70,92,107}
    deficient=[1,2,0];count=0;dense_examples=[]
    for M in product(range(8),repeat=3):
        if rank(M)!=3:continue
        rows=[combine(deficient,row)for row in M];assert rank(rows)==2
        if all(rows):dense_examples.append(rows)
        count+=1
    assert count==168 and dense_examples
    assert rank([1,2,3])==2 and all([1,2,3])
    oversized=[1,2,0,4];assert rank(oversized)==3
    out={'status':'PASS_INDEPENDENT_NATIVE_K_SATURATION_REVIEW','pins':PINS,'records':records,
         'native_K370_support':sorted(source[370]),'actual_packet_support':sorted(support),'missing_donors':sorted(missing),
         'basis_change_controls':count,'all_rows_nonzero_not_sufficient':True,'extra_channel_repair_control':True,
         'author_code_imported_or_executed':False,'author_proof_sha256':sha256((a.author/'SATURATION.md').read_bytes()).hexdigest(),
         'author_screen_sha256':sha256((a.author/'output/SYSTEM-SCREEN.json').read_bytes()).hexdigest(),
         'applies_to_all_near_minimum_fittings':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print('56 K profiles,122 tight donor cuts,5 missing packet donors,168 basis controls')
if __name__=='__main__':main()
