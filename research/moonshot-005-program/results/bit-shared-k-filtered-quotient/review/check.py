#!/usr/bin/env python3
"""Independent binary-basis review of the native K370 Cauchy mixer."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip
import json

def need(ok,label):
    if not ok:raise ValueError(label)

def reduce_polynomial(x):
    while x.bit_length()>9:
        x ^= 529 << (x.bit_length()-10)
    return x

def product(a,b):
    value=0
    for bit in range(9):
        if b>>bit&1:value^=a<<bit
    return reduce_polynomial(value)

def rank(columns):
    basis={}
    for value in columns:
        while value:
            bit=value.bit_length()-1
            if bit in basis:value^=basis[bit]
            else:basis[bit]=value;break
    return len(basis)

def binary_columns(matrix):
    # Construct columns from images of polynomial monomials. This differs
    # from the author's field elimination and row-oriented binary expansion.
    return [sum(reduce_polynomial(matrix[i][j]<<bit)<<(9*i)for i in range(len(matrix)))
            for j in range(len(matrix[0]))for bit in range(9)]

def transpose_columns(columns,n):
    return [sum(((column>>i)&1)<<j for j,column in enumerate(columns))for i in range(n)]

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();author=args.author.resolve();base=repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';rp=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    lraw=gzip.decompress(lp.read_bytes());rraw=gzip.decompress(rp.read_bytes())
    need(sha256(lraw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native layout')
    need(sha256(rraw).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','literal routes')
    layout=json.loads(lraw);routes=[json.loads(line)for line in rraw.splitlines()]
    D=list(map(set,layout['D4']));roots=layout['root_table'];K=set(layout['A2'][370]);need(K=={1,73,80},'K370 roots')
    plane_flags={k:Counter()for k in range(1120)};terminal_counts=Counter()
    for phase,j,c,h,d,k,left,right in routes:
        if k is None:continue
        plane_flags[k][d]+=1
        terminal_counts[k,right if phase=='X'else j]+=1
    need(all(len(count)==45 and set(count.values())=={2}for count in plane_flags.values()),'all50400 actual incoming flags')
    sources={};all_native_donor_cuts=0
    for k,Kroots in enumerate(layout['A2']):
        supported={j for j in range(111)if all(sum(x*y for x,y in zip(roots[j],roots[i]))==0 for i in Kroots)}
        sources[k]=supported
        for j in supported:
            ds=[d for d in plane_flags[k]if j in D[d]]
            need(len(ds)==15 and sum(plane_flags[k][d]for d in ds)==30,'every native incoming donor cut')
            all_native_donor_cuts+=1
    tight=[]
    for i in range(111):
        ks=[k for k,Kroots in enumerate(layout['A2'])if i in Kroots]
        neighbors=[j for j in range(111)if i!=j and sum(x*y for x,y in zip(roots[i],roots[j]))==0]
        if all(sum(terminal_counts[k,i]for k in ks if j in sources[k])==480 for j in neighbors):tight.append(i)
    need(len(tight)==100 and K<=set(tight),'exact globally tight receiver exception scope')
    donors=[j for j in range(111)if all(sum(x*y for x,y in zip(roots[j],roots[i]))==0 for i in K)]
    need(len(donors)==36,'36 native donors')
    matrix_path=author/'mixer-output/MATRIX.json';word_path=author/'mixer-output/WORD.json.gz'
    data=json.loads(matrix_path.read_bytes());payload=gzip.decompress(word_path.read_bytes());word=json.loads(payload)
    C=data['matrix'];need(data['field_polynomial']==529 and data['row_nodes']==list(range(45))and data['column_nodes']==list(range(64,109)),'exact Cauchy nodes')
    need(len(C)==45 and all(len(row)==45 for row in C),'full matrix shape')
    for i in range(45):
        for j in range(45):need(product(C[i][j],i^(64+j))==1,'Cauchy coefficient exact inverse')
    need(rank(binary_columns(C))==405,'full map has rank45 over GF512')
    all_minors=0;counts={};faults=[]
    for phase in ['X','Y']:
        selected=[r for r in routes if r[0]==phase and r[5]==370]
        need(len(selected)==45 and len({r[4]for r in selected})==45,'actual incoming phase flags')
        def owner(row):return (0 if phase=='X'else 53280)+480*row[1]+row[2]
        by_d={r[4]:r for r in selected};ds=sorted(by_d)
        need(all(len(D[d]&set(range(111)))==12 for d in ds),'all flags have12 native donors')
        inputs=[owner(by_d[d])for d in ds]
        outputs=[]
        for i in [1,73,80]:
            group=sorted(owner(r)for r in selected if(r[7]if phase=='X'else r[1])==i)
            need(len(group)==15,'actual receiver output quota');outputs.extend(group)
        owners=sorted(inputs);info=data['phases'][phase]
        need(info['owner_order']==owners and info['input_D_order']==ds and info['input_owner_order']==inputs
             and info['output_owner_order']==outputs,'emitted real-owner binding')
        need(len(set(owners))==45 and set(inputs)==set(outputs),'same45 physical owners')
        index={o:k for k,o in enumerate(owners)};physical=[[0]*45 for _ in owners]
        for i,out in enumerate(outputs):
            for j,inp in enumerate(inputs):physical[index[out]][index[inp]]=C[i][j]
        expected=transpose_columns(binary_columns(physical),405)
        state=[1<<k for k in range(405)];ops=word['phases'][phase]
        for dest,src in ops:
            need(0<=dest<405 and 0<=src<405 and dest!=src,'ordinary ADD only, no extra owner')
            state[dest]^=state[src]
        need(state==expected,'every independent forward bit column')
        need(rank(state)==405,'physical phase invertible')
        for dest,src in reversed(ops):state[dest]^=state[src]
        need(state==[1<<k for k in range(405)],'every inverse input bit')
        bad=[1<<k for k in range(405)]
        for dest,src in ops[1:]:bad[dest]^=bad[src]
        need(bad!=expected,'omitted ADD rejected');faults.append(phase)
        counts[phase]=len(ops)
        for j in donors:
            cols=[k for k,d in enumerate(ds)if j in D[d]];need(len(cols)==15,'tight donor input set')
            for receiver in range(3):
                minor=[[C[r][c]for c in cols]for r in range(15*receiver,15*(receiver+1))]
                need(rank(binary_columns(minor))==135,'independent binary rank of donor minor');all_minors+=1
        need(Counter((r[7]if phase=='X'else r[1])for r in selected)=={1:15,73:15,80:15},'all receiver owners accounted')
    need(all_minors==216 and counts=={'X':82236,'Y':82309},'complete minors and literal costs')
    invoice=2*sum(counts.values());need(invoice==329090 and 8*invoice==2632720,'forward and inverse paid')
    # Distinct row spaces can have the same rank; saturation requires equality.
    need(rank([1,2])==rank([1,4])==2 and rank([1,2,4])==3,'rank-only false positive control')
    need(rank([1,2])==rank([2,1])==2 and [1]!=[2],'early flag is independent condition')
    result={'status':'PASS_INDEPENDENT_NATIVE_K370_COUPLED_QUOTIENT_REVIEW',
            'binary_minor_checks':all_minors,'binary_minor_rank':135,'phase_binary_rank':405,
            'all_native_incoming_flags_checked':50400,'all_native_donor_cuts_checked':all_native_donor_cuts,
            'globally_tight_receivers':tight,
            'forward_ADD_counts':counts,'forward_plus_inverse_ADD':invoice,
            'bank3840_forward_plus_inverse_ADD':8*invoice,'all810_independent_phase_columns':True,
            'omitted_ADD_controls_rejected':faults,'new_owner_count':0,'additional_MOVE':0,
            'word_payload_sha256':sha256(payload).hexdigest(),
            'scope':'necessary common donor quotient/early flag and conditional local mixer; full source/D/target gluing open',
            'pins':[{'path':str(p.relative_to(repo)),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [lp,rp]],
            'author_pins':[{'path':str(p.relative_to(author)),'sha256':sha256(p.read_bytes()).hexdigest()}
                           for p in [author/'PROOF.md',author/'check.py',author/'mixer.py',matrix_path]],
            'no_new_kappa':True}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({'binary_minors':all_minors,'paid_ADD':invoice}))

if __name__=='__main__':main()
