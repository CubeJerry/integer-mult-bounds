#!/usr/bin/env python3
"""Independent integer-root intervals from independently replayed profiles."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache

def need(ok,s):
    if not ok:raise ValueError(s)

def root(n,k):
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:break
        x=y
    while pow(x,k)>n:x-=1
    while pow(x+1,k)<=n:x+=1
    return x

@lru_cache(None)
def interval(r):
    D=10**30;n=pow(r,199)*pow(D,200);z=root(n,200)
    need(pow(z,200)<=n<pow(z+1,200),'directed integer-root bound')
    return F(z,D),F(z+1,D)

def add(*parts):
    out={}
    for c,h in parts:
        for k,v in h.items():out[int(k)]=out.get(int(k),F(0))+c*F(v)
    return {k:v for k,v in out.items()if v}

def moment(h):
    lo=hi=F(0)
    for r,c in h.items():
        a,b=interval(r)
        lo+=c*(a if c>0 else b);hi+=c*(b if c>0 else a)
    return lo,hi

def hist(b,a,rows=0,price=0,n=1):
    target=add((2,{1+2*a*b:1}),*[(4,{1+j*b:1}) for j in range(1,a+1)])
    paid=add((4,{1:1}),(8*a,{b:1}),*[(4,{j*b:1}) for j in range(1,a)])
    if rows:paid=add((1,paid),(F(4*a*rows,n),{price:1}))
    return add((1,target),(-1,paid))

def main():
    p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='c92dba80feb66103f1155f9f368f753d484eb954365d85cc09a4adeacf17bbda','frozen author proof')
    pins=json.loads((a.package/'source/PINS.json').read_text())
    for row in pins:need(hashlib.sha256((a.package/'source'/row['file']).read_bytes()).hexdigest()==row['sha256'],'source pin '+row['file'])
    caller=json.loads((a.package/'source/caller.json').read_text());stage_events=[e for e in caller['events'] if e[0]=='J']
    need(len(stage_events)==18 and {e[1] for e in stage_events}==set(range(1,19)),'all distinct caller stages')
    source_counts={}
    for typ,index in [('A',2),('B',3)]:
        d=caller['types'][typ];targets={};idles={};queries=0
        for diag in d['diagonal']:
            need(diag[0]%2==1 and diag[1]==0 and set(diag[2:])<={0,1},'actual productive head/body pattern')
            rank=sum(diag[2:]);targets[rank]=targets.get(rank,0)+1
        for e in caller['events']:
            if e[0]==typ and e[1]=='QUERY':queries+=1
            if e[0]==typ and e[1]=='IDLE_ONE':
                need(len(set(e[3]))==len(e[3]),'whole independent idle body blocks')
                rank=len(e[3]);idles[rank]=idles.get(rank,0)+1
        mains={sum(isinstance(x,int) for x in e[index]) for e in stage_events}
        need(mains==({4} if typ=='A' else {2}),'public main role count from invocation operands')
        need(targets=={18:2,**{j:4 for j in range(1,10)}} and queries==4,'productive/query inventory')
        need(idles=={j:(40 if typ=='B' and j==1 else 4) for j in range(1,9)},'wrapper idle inventory')
        need(18*next(iter(mains))+idles[1]==76,'type-B mains and whole idles exactly cancel')
        source_counts[typ]=dict(targets=targets,idles=idles,queries=queries,mains=next(iter(mains)))
    source=json.loads((a.package/'RESULT.json').read_text());cases={}
    for name,h,n,rows,price in [('complex_square',81,10816,64,49),('bit_square_hub_packets',64,12321,81,64),('complex_cube_free_control',729,104**3,0,0),('bit_cube_free_control',512,111**3,0,0)]:
        b=h-1;cases[name]={}
        for stages in (2,4,6,18):
            q=stages//2;free=moment(hist(b,q));full=moment(hist(b,q,rows,price,n));old=source['cases'][name]['stages'][str(stages)]
            for interval_value,key in [(free,'free_decoder_gap_per_port'),(full,'row_model_gap_per_port')]:
                previous=list(map(F,old[key]['exact']));need(interval_value[0]<=previous[0]<=previous[1]<=interval_value[1],'independent interval encloses author')
            cases[name][stages]=dict(free=list(map(str,free)),row=list(map(str,full)),free_decimal=float(free[0]),row_decimal=float(full[0]))
        first=moment(hist(b,1,rows,price,n));difference=moment(add((1,hist(b,2,rows,price,n)),(-1,hist(b,1,rows,price,n))))
        need(first[1]<0 and difference[1]<0,'infinite-stage initial signs')
    boundaries={}
    for b,a0,want in [(36,9,1),(37,9,-1),(134,1,1),(135,1,-1),(80,1,1),(80,2,-1),(63,2,1),(63,3,-1)]:
        value=moment(hist(b,a0));need(value[0]>0 if want>0 else value[1]<0,'strict adjacent bound sign')
        boundaries[str((b,a0))]=list(map(str,value))
    extension_increment=moment(add((2,{541:1}),(2,{271:1}),(-12,{135:1})))
    need(extension_increment[1]<0,'root extension: second increment negative at b135')
    cap=tuple(x*F(10816,4) for x in moment(hist(80,1)))
    oldcost=moment({49:64});ratio=(cap[0]/oldcost[1],cap[1]/oldcost[0])
    reductions=(1-ratio[1],1-ratio[0]);need(reductions[0]>F(34,100),'more than34percent reduction needed')
    no_queries=moment(add((1,hist(80,1,64,49,10816)),(4,{1:1})))
    need(no_queries[0]>0,'query omission falsely makes square favorable')
    report=dict(status='PASS_INDEPENDENT_TENSOR_CALLER_PREFLIGHT',source_counts=source_counts,cases=cases,boundaries=boundaries,two_stage_cap=list(map(str,cap)),required_reduction=list(map(str,reductions)),all_even_free_dimension_extension=dict(minimum_rejected_h=136,b135_second_increment=list(map(str,extension_increment)),proof='ROOT-EXTENSION.md'),negative_control='mandatory query omission gives false favorable square',scope='Pinned eighteen-stage interface and explicitly hypothetical other even-stage invoices; helper endpoint-credit grammar retained. No larger native, compatible supplier or new kappa.')
    a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()

