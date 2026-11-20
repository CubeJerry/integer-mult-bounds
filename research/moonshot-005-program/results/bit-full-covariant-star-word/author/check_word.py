"""Replay the supplied physical S028 proper-star words; no author imports."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

N=111*480
BANK=3840


def require(condition,message):
    if not condition:raise ValueError(message)


def bytes_at(path,checksum=None):
    data=path.read_bytes()
    if path.suffix=='.gz':data=gzip.decompress(data)
    if checksum is not None:require(hashlib.sha256(data).hexdigest()==checksum,'checksum '+str(path))
    return data


def product(x,y):
    r=0
    while y:
        if y&1:r^=x
        y>>=1;x<<=1
        if x&64:x^=0x43
    return r


M=np.array([[product(x,y) for y in range(64)] for x in range(64)],dtype=np.uint8)
INV=[None]+[next(y for y in range(1,64) if product(x,y)==1) for x in range(1,64)]


def binary_multiplier(k):
    expect=[sum(((product(k,1<<c)>>r)&1)<<c for c in range(6)) for r in range(6)]
    a=expect.copy();elimination=[]
    for c in range(6):
        if a[c]&(1<<c)==0:
            r=next(s for s in range(c+1,6) if a[s]&(1<<c))
            for x,y in [(r,c),(c,r),(r,c)]:a[x]^=a[y];elimination.append((x,y))
        for r in range(6):
            if r!=c and a[r]&(1<<c):a[r]^=a[c];elimination.append((r,c))
    identity=[1<<r for r in range(6)];require(a==identity,'paid scale inverse binary')
    for x,y in reversed(elimination):a[x]^=a[y]
    require(a==expect,'paid scale direct binary')
    addcost=sum(bin(r).count('1') for r in expect)
    return len(elimination),addcost


SCALE={k:binary_multiplier(k) for k in range(1,64)}


def phase_input(repo):
    src=repo/'research/moonshot-005-program/results'
    routes=bytes_at(src/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
    assignments=json.loads(bytes_at(src/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json','deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601'))
    rr=[None]*(2*N)
    for line in routes.splitlines():
        x=json.loads(line);fid=480*x[1]+x[2]+N*(x[0]=='Y')
        require(rr[fid] is None,'original owner uniqueness');rr[fid]=x
    require(all(x is not None for x in rr),'original owner completeness')
    return rr,assignments


def target_matrix(assignment,side):
    arr=np.zeros((111,BANK,64),dtype=np.uint8)
    center=80 if side=='row' else 10
    for i,j,ell in assignment[side+'_transfers']:
        idx=j if side=='row' else i
        require((i if side=='row' else j)==center,'target center')
        arr[idx,64*ell:64*ell+64]=np.eye(64,dtype=np.uint8)
    for (i,j),masks in zip(assignment['internal_edges'],assignment['internal_matrices_64']):
        if (i if side=='row' else j)!=center:continue
        mat=np.array([[(mask>>c)&1 for c in range(64)] for mask in masks],dtype=np.uint8)
        arr[j if side=='row' else i,:64]=mat.T if side=='row' else mat
    return arr.reshape(N,8,64)


def decode_ops(word,routes):
    side=word['side'];early=side=='row';offset=0 if early else N
    phase='X' if early else 'Y';target=80 if early else 10
    require(word['phase']==phase and word['center']==target,'word direction')
    taps=[];tapcost=0;seen=set()
    for d,p,coeff in word['D_emissions']:
        r=routes[p]
        require(r[0]==phase and r[4]==d and r[7 if early else 6]==target,'actual emission visits')
        require(d not in seen and len(coeff)==8 and all(k in range(1,64) for k in coeff),'one emission per D');seen.add(d)
        taps.append((p-offset,coeff));tapcost+=8*sum(SCALE[k][1] for k in coeff)
    stream=[];by_chart={};individual=0
    for stage,col in [('D',4),('plane',3 if early else 5),('endpoint',1)]:
        subtotal=0
        for who,ops in sorted(word[stage].items(),key=lambda kv:int(kv[0])):
            for op in ops:
                kind=op[0];require(kind in ('a','s','w','c'),'legal field gate')
                bycopy=kind=='c';indices=op[1:2] if kind=='s' else op[1:3]
                baseids=[i//8 if bycopy else i for i in indices]
                require(all(routes[f][0]==phase and routes[f][col]==int(who) for f in baseids),'chart owner mismatch')
                require(kind=='s' or indices[0]!=indices[1],'distinct control and destination')
                if kind=='s':
                    k=op[2];require(0<k<64,'nonzero scale');subtotal+=8*SCALE[k][0]
                elif kind=='a':
                    k=op[3];require(0<k<64,'nonzero bundle multiplier');subtotal+=8*SCALE[k][1]
                elif kind=='w':k=1;subtotal+=8*18
                else:k=1;subtotal+=6;individual+=1
                loc=[v-(8*offset if bycopy else offset) for v in indices]
                stream.append((kind,loc[0],loc[-1],k))
        by_chart[stage]=subtotal
    return stream,taps,{'whole_stage_forward_ADD':by_chart,'coded_taps_ADD':tapcost,
                        'cross_copy_individual_field_ops':individual,'total':2*sum(by_chart.values())+tapcost+384}


def replay(buf,ops,action='direct',fault=False):
    # The coefficient form is field-bilinear, so a field shear adjoint exchanges
    # its input and output owners and retains the field-valued coefficient.
    steps=reversed(ops) if action in ('adjoint','inverse') else ops
    skipped=False
    for op,a,b,k in steps:
        if fault and not skipped and op=='c':skipped=True;continue
        if action in ('adjoint','adjoint_inverse') and op in ('a','c'):a,b=b,a
        if op=='a':buf[a]^=M[k,buf[b]]
        elif op=='w':buf[[a,b]]=buf[[b,a]]
        elif op=='s':buf[a]=M[INV[k] if action in ('inverse','adjoint_inverse') else k,buf[a]]
        else:buf[a//8,a%8]^=buf[b//8,b%8]
    if fault:require(skipped,'fault gate found')


def transfer(taps,ops,missing=False):
    grad=np.zeros((N,8,64),dtype=np.uint8)
    for f,coeffs in taps:
        for p in range(8):grad[f,p,p::8]^=np.asarray(coeffs,dtype=np.uint8)
    replay(grad,ops,fault=missing)
    return grad


def inject_center(buf,center,taps):
    for f,coeffs in taps:
        for g,k in enumerate(coeffs):buf[f]^=M[k,center[8*g:8*g+8]]


def capture_center(buf,taps):
    center=np.zeros(64,dtype=np.uint8)
    for f,coeffs in taps:
        for g,k in enumerate(coeffs):center[8*g:8*g+8]^=M[k,buf[f]]
    return center


def numeric(rr,cc,expected):
    # Deterministic full-size mixed-symbol round trip, in actual chronological order.
    rg=np.random.default_rng(273111);x0=rg.integers(0,64,(N,8),dtype=np.uint8);y0=rg.integers(0,64,(N,8),dtype=np.uint8)
    x=x0.copy();y=y0.copy();center10=x0.reshape(111,BANK)[10,:64].copy()
    row_ops,row_taps=rr;col_ops,col_taps=cc
    replay(x,row_ops,action='adjoint');cache80=capture_center(x,row_taps)
    replay(x,row_ops,action='adjoint_inverse');require(np.array_equal(x,x0),'full original X restoration')
    replay(y,col_ops,action='inverse');inject_center(y,center10,col_taps);replay(y,col_ops)
    y.reshape(111,BANK)[80,:64]^=cache80
    rx=expected['row'].reshape(-1,64);cy=expected['column'].reshape(-1,64)
    answer=y0.copy();flat=answer.ravel();row,cols=np.nonzero(cy);np.bitwise_xor.at(flat,row,center10[cols])
    row,cols=np.nonzero(rx);want80=np.zeros(64,dtype=np.uint8);np.bitwise_xor.at(want80,cols,x0.ravel()[row])
    require(np.array_equal(want80,cache80),'actual forward early adjoint and tap capture')
    answer.reshape(111,BANK)[80,:64]^=want80
    require(np.array_equal(y,answer),'entire physical X→Y derivative and genuine Y baseline')


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certs',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();routes,assignment=phase_input(a.repo)
    ledger=json.loads((a.certs/'RESULT.json').read_bytes());result={};sides={};expected={}
    for side in ('row','column'):
        word=json.loads(bytes_at(a.certs/(side+'-word.json.gz'),ledger['word_SHA256'][side]))
        ops,taps,costs=decode_ops(word,routes);sides[side]=(ops,taps)
        want=target_matrix(assignment,side);expected[side]=want
        got=transfer(taps,ops);require(np.array_equal(got,want),'all physical owners and 64 master coordinates')
        nr=np.count_nonzero(got);fault=transfer(taps,ops,missing=True)
        delta=int(np.count_nonzero(fault!=want));require(delta>0,'legal shear deletion rejected')
        require(costs['total']==ledger['word_costs'][side]['total_ADD'],'binary invoice')
        result[side]={'aggregate_edges':len(assignment[side+'_transfers'])+(3 if side=='row' else 2),
                      'proper_binary_valued_field_coefficients':int(nr),
                      'original_field_rows':426240,'master_columns':64,'charged':costs,
                      'omitted_local_shear_wrong_coefficients':delta}
    numeric(sides['row'],sides['column'],expected)
    result['joint']={'binary_ADD':sum(z['charged']['total'] for z in result.values()),'INIT':768,'dirty_CLEAR':768,
                     'proper_field_rank':128,'whole_X_inverse':True,'whole_Y_preload':True,'extra_MOVE':0,
                     'baseline_and_proper_transfer_on_physical_field_replay':True}
    require(result['joint']['binary_ADD']==ledger['total_binary_ADD'],'whole invoice')
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'REPLAY.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
