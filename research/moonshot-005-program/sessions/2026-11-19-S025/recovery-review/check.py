#!/usr/bin/env python3
"""Fresh scoped read-only review of recovered arrays and semisimple argument.

No author/reviewer algebra implementation is imported. Full finite geometry
is reconstructed; direct field matrices are passed to a fresh rank engine.
Large generated matrix input is an intermediate, not a new proof source.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct
import subprocess

def require(ok,why):
    if not ok: raise ValueError(why)

def content(path):
    raw=path.read_bytes()
    return gzip.decompress(raw) if path.suffix=='.gz' else raw

def read(path): return json.loads(content(path))

def mul(a,b):
    value=0
    for bit in range(7):
        if b>>bit&1: value^=a<<bit
    for bit in range(12,6,-1):
        if value>>bit&1: value^=131<<(bit-7)
    return value

TIMES=[[mul(a,b)for b in range(128)]for a in range(128)]

def vandermonde(n):
    result=[]
    for alpha in range(1,n+1):
        row=[1]
        for _ in range(n-1):row.append(TIMES[row[-1]][alpha])
        result.append(row)
    return result

def binary(matrix):
    result=[]
    for row in matrix:
        for lane in range(7):
            value=0
            for col,entry in enumerate(row):
                for bit in range(7):
                    if TIMES[entry][1<<bit]>>lane&1:value|=1<<(7*col+bit)
            result.append(value)
    return result

def swaps(order):
    current=list(range(len(order)));answer=[]
    for i,want in enumerate(order):
        k=current.index(want)
        if i!=k:
            answer.append((i,k));current[i],current[k]=current[k],current[i]
    require(current==order,'permutation synthesis')
    return answer

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    programme=args.repo/'research/moonshot-005-program'
    root=programme/'results/bit-all-plane-causal-arrays'
    layout_path=programme/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    factor_path=programme/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json'
    require(hashlib.sha256(content(layout_path)).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    require(hashlib.sha256(content(factor_path)).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7','factor pin')
    layout=read(layout_path);factor=read(factor_path)
    roots=layout['root_table'];planes=list(map(frozenset,layout['A2']));ports=list(map(frozenset,layout['D4']))
    orth=[frozenset(j for j,v in enumerate(roots)if sum(a*b for a,b in zip(u,v))==0)for u in roots[:111]]
    native=frozenset(range(111));u=dict(factor['factors'])
    full=read(root/'full/author/output/RESULT.json.gz')
    full_by={entry['H']:entry for entry in full['planes']}
    coefficients=read(root/'punctured/author/output/COEFFICIENTS.json.gz')
    two_by={entry['H']:entry for entry in coefficients['planes']}
    single=read(root/'singleton/author/output/RESULT.json')
    single_by={entry['H']:entry for entry in single['planes']}
    V45=vandermonde(45);V90=vandermonde(90)
    derivative=[[row[t-1] if t%2 else 0 for t in range(90)]for row in V90]
    fields=Counter();conditions=Counter();full_x=Counter();cross_cost=0
    matrix_path=args.out/'MATRICES.bin';cases=0
    def emit(handle,kind,matrix,expected):
        nonlocal cases
        handle.write(struct.pack('<4I',kind,len(matrix),len(matrix[0]),expected))
        handle.write(bytes(x for row in matrix for x in row));cases+=1
    weights=[sum(TIMES[v][1<<bit].bit_count()for bit in range(7))for v in range(128)]
    with matrix_path.open('wb')as handle:
        handle.write(b'\0'*4)
        for h,H in enumerate(planes):
            m=len(H&native)
            if not m:continue
            fields[m]+=1;D=[d for d,P in enumerate(ports)if H<=P]
            require(len(D)==45,'forty-five genuine exits')
            receivers={i:[p for p,d in enumerate(D)if ports[d]<=orth[i]]for i in range(111)if H<=orth[i]}
            require(all(len(S)==15 for S in receivers.values()),'fifteen genuine visible ports')
            x=12//m+u.get(h,0)
            if m==3:
                full_x[x]+=1;entry=full_by[h]
                require(entry['actual_D4_ports']==D and entry['native_donors']==sorted(H&native),'full plane provenance')
                require({int(i):z['ports']for i,z in entry['receiver_subsets'].items()}==receivers,'all full incidences')
                for S in receivers.values():
                    for donor in range(3):
                        emit(handle,0,[[V45[p][15*donor+t]for t in range(15)]for p in S],15)
                        conditions[3]+=1
            elif m==2:
                require(x==6,'real two-donor early count')
                C=[list(bytes.fromhex(row))for row in two_by[h]['C_hex_rows']]
                require(len(C)==90 and all(len(row)==90 for row in C),'full C matrix')
                cross_cost+=sum(weights[v]for row in C for v in row)
                for S in receivers.values():
                    rows=[2*p+bit for p in S for bit in range(2)]
                    for donor in range(2):
                        M=[[V90[p][45*donor+t]for t in range(45)]+[0]*15 for p in rows]
                        M+=[[C[p][45*donor+t]for t in range(45)]+[V90[p][15*donor+t]for t in range(15)]for p in rows]
                        emit(handle,1,M,60);conditions[2]+=1
                S=next(iter(receivers.values()));rows=[2*p+bit for p in S for bit in range(2)]
                M=[[V90[p][t]for t in range(45)]+[0]*15 for p in rows]
                M+=[[0]*45+V90[p][:15]for p in rows]
                emit(handle,3,M,45)
            else:
                require(m==1 and x==12,'real singleton early count')
                entry=single_by[h]
                require(entry['actual_D4_ports']==D,'singleton genuine exits')
                for S in receivers.values():
                    rows=[2*p+bit for p in S for bit in range(2)]
                    emit(handle,2,[V90[p][:60]for p in rows]+[derivative[p][:60]for p in rows],60)
                    conditions[1]+=1
        # A repeated node destroys the Hermite condition; this catches the
        # tempting replacement of a confluent system by repeated values.
        emit(handle,3,V90[:30]+V90[:30],30)
        handle.seek(0);handle.write(struct.pack('<I',cases))
    require(fields=={3:881,2:227,1:11},'all 1119 nonempty plane families')
    require(conditions=={3:88062,2:15098,1:360},'complete actual projection census')
    require(full_x=={4:709,5:84,6:88},'three full-plane timing cases')
    exe=args.out/'rankcheck'
    subprocess.run(['g++','-std=c++17','-O3',str(Path(__file__).with_name('rankcheck.cpp')),'-o',str(exe)],check=True)
    subprocess.run([str(exe),str(matrix_path),str(args.out/'RANKS.json')],check=True)
    # Independently replay the two common-field binary base words.
    base45=read(root/'punctured/author/output/FULL-H-ADD-WORD.json.gz')['ADD']
    base90=read(root/'punctured/author/output/ADD-WORD.json.gz')['ADD']
    for V,word in [(V45,base45),(V90,base90)]:
        value=[1<<j for j in range(7*len(V))]
        for a,b in word:
            require(a!=b and min(a,b)>=0 and max(a,b)<len(value),'distinct in-range ADD')
            value[a]^=value[b]
        require(value==binary(V),'all-column ordinary word equality')
        a,b=word[-1];value[a]^=value[b]
        require(value!=binary(V),'omission of last ADD changes map')
    # Reconstruct input orders directly from the real stripe formula.
    full_swaps=[]
    for residue in range(3):
        order=sorted(range(45),key=lambda p:((residue-p)%3,p))
        full_swaps.append(len(swaps(order)))
    require(full_swaps==[42,42,40],'full physical permutations')
    early_order=[2*p+j for j in range(2)for p in range(45)]
    early_swaps=len(swaps(early_order));late_swaps=[];ground=[0]*45;used=set()
    for stripe in range(6):
        physical=[]
        for p in range(45):
            entries=[('L',j,p,stripe%2)for j in range(2)if(j+p)%3==stripe//2]
            while len(entries)<2:
                entries.append(('Y',-1,p,ground[p]));ground[p]+=1
            require(not any(q in used for q in entries),'real late holders used once')
            used.update(entries);physical+=entries
        order=sorted(range(90),key=lambda i:(physical[i][1] if physical[i][1]>=0 else 2,i))
        late_swaps.append(len(swaps(order)))
    require(early_swaps==80 and late_swaps==[84,84,81,81,85,85] and ground==[8]*45,'punctured permutations and ground holders')
    full_add=881*(24*len(base45)+8*sum(full_swaps)*21)
    two_add=227*(12*len(base90)+6*630+(6*early_swaps+sum(late_swaps))*21)+6*cross_cost
    derivative_add=sum(v.bit_count()for v in binary(derivative))
    singleton_add=11*6*(len(base90)+derivative_add+315)
    require((full_add,two_add,singleton_add)==(917438160,731524866,17530194),'exact local finite cost')
    caches=227*6*630+11*6*315
    require(caches==878850,'stationary cache owners')
    pins={}
    for package in [root,programme/'results/bit-common-semisimple-source-gate']:
        for path in sorted(package.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                pins[str(path.relative_to(args.repo))]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    for path in [layout_path,factor_path]:
        pins[str(path.relative_to(args.repo))]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'uncompressed_sha256':hashlib.sha256(content(path)).hexdigest()}
    (args.out/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
    result={'status':'PASS_FRESH_RECOVERED_LOCAL_ARRAY_REVIEW','field_modulus':131,'families':dict(fields),'direct_original_projection_ranks':dict(conditions),'base_binary_columns_replayed':[315,630],'all_local_ADD':full_add+two_add+singleton_add,'INIT_and_dirty_CLEAR_each':caches,'additional_H_MOVE':0,'full_physical_swaps':full_swaps,'punctured_early_swaps':early_swaps,'punctured_late_swaps':late_swaps,'negative_controls':{'omitted_C_rank':45,'repeated_evaluation_rank':30,'omitted_ADD_changes_map':True},'semisimple_argument_review':'Written proof review; universal nonlinear product-extension argument checked independently, no fresh full scalar-coloring search claimed.','scope':'Local interfaces only; global same-donor coupling, later transport and caller remain open.','new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],result['all_local_ADD'],'ADD',caches,'stationary owners')

if __name__=='__main__':main()
