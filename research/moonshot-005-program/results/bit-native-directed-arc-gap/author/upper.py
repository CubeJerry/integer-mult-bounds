"""Compile an actual binary vector fitting with a completely absent reciprocal native pair."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from pathlib import Path


def need(x,msg):
    if not x:raise ValueError(msg)


def binary_rank(rows):
    basis={}
    for v in rows:
        while v:
            h=v.bit_length()-1
            if h in basis:v^=basis[h]
            else:basis[h]=v;break
    return len(basis)


def main():
    p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--witness',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--receipt-name',default='UPPER-RESULT.json');a=p.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','native roots')
    v=json.loads(raw)['root_table'][:111];adj=[sum(1<<j for j,q in enumerate(v) if sum(x*y for x,y in zip(w,q))==0) for w in v]
    w=json.loads(a.witness.read_bytes());b=w['bank'];bad=w['erased_reciprocal_pair'];need(len(set(bad))==2 and adj[bad[0]]>>bad[1]&1,'genuine proper pair');sent=[0]*111;rank=0;atom_types=Counter();minimum=0;allrows=0
    for atom in w['words']:
        kind=atom['kind'];S=atom['owners'];count=atom['multiplicity'];need(len(set(S))==len(S) and len(set(S)&set(bad))<=1 and count>0,'valid erased two-direction atom')
        if kind=='clique':
            sm=sum(1<<q for q in S);need(all(sm & ~(adj[i]|1<<i)==0 for i in S),'native complete proper clique')
        else:need(kind=='canonical','known binary atoms')
        atom_types[kind]+=count
        for _ in range(count):
            kept=[i for i in S if sent[i]<b]
            if not kept:continue
            sk=sum(1<<q for q in kept)
            rows=[sk if kind=='clique' else (adj[i]|1<<i)&sk for i in kept]
            need(all((row>>i&1) and not row & ~(adj[i]|1<<i) for row,i in zip(rows,kept)),'every actual scalar own term and structural zero')
            for i in kept:sent[i]+=1
            rank+=binary_rank(rows);allrows+=len(kept)
    need(len(set(sent))==1 and sent[0]==b and allrows==111*b,'all native original coordinates assigned exactly once')
    truth={'bank':b,'native_rows':allrows,'erased_both_proper_directions':bad,'atom_counts':dict(atom_types),'exact_binary_fitting_rank':rank,'excess_over_9b':rank-9*b,'erased_corank':b,'corank_to_excess':f'{b}/{rank-9*b}','native_layout_sha256':sha256(raw).hexdigest(),'witness_sha256':sha256(a.witness.read_bytes()).hexdigest()}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/a.receipt_name).write_text(json.dumps(truth,indent=2,sort_keys=True)+'\n');print(truth)


if __name__=='__main__':main()
