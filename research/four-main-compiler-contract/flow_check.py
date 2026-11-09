"""Literal ambient-cap flow corroboration. @CubeJerry/OpenAI, Apache-2.0."""
from collections import Counter
from itertools import product
from math import prod
import json

def need(x,m):
    if not x:raise ValueError(m)

def flow(n,cap,actual_ambient=None):
    actual_ambient=cap if actual_ambient is None else actual_ambient
    need(cap>=3 and n>=cap,'valid finite example');depth=0
    while cap*2**(depth+1)<=n:depth+=1
    units={}
    for d in range(depth+1):
        for rounds in product(range(4),repeat=d):
            for labels in product((2,3),repeat=depth-d):
                column=prod(labels)
                if cap*column<=n:
                    need(actual_ambient*column<=n,'actual unit fits ambient geometry')
                    units[rounds,labels]=column
    sources=Counter();exits=Counter();edges={}
    for (rounds,labels),column in units.items():
        for rank in (2,3):
            parent=(rounds[:-1],(rank,)+labels)
            if not rounds or parent not in units:
                size=rank*column
                need(cap*size>n and size<=n,'source in cap interval');sources[size]+=1
            else:
                paid=(parent,rounds[-1]);need(paid not in edges,'one child per paid position')
                need(units[parent]==rank*column,'exact integer matching');edges[paid]=((rounds,labels),rank)
        for paid_position in range(4):
            if not labels:exits[column]+=1
            else:
                child=(rounds+(paid_position,),labels[1:])
                need(child in units and labels[0]*units[child]==column,'every request matched')
    expected={(key,j) for key in units if key[1] for j in range(4)}
    need(set(edges)==expected,'no lost duplicated invented request');need(set(exits)=={1},'exit bound')
    sm=sum(k*v for k,v in sources.items());em=sum(k*v for k,v in exits.items())
    need(sm-em==sum(units.values()),'exact internal rank-potential cancellation')
    return dict(top_rank=n,ambient_cap=cap,depth=depth,units=len(units),internal_edges=len(edges),sources=sum(sources.values()),source_mass=sm,exits=sum(exits.values()),exit_mass=em)

def verify():
    receipts=[flow(n,cap) for cap in (3,4,5,7) for n in (cap,cap+1,2*cap,3*cap,6*cap,12*cap)]
    rejected=False
    try:flow(30,3,actual_ambient=5)
    except ValueError:rejected=True
    need(rejected,'smaller target cap cannot certify actual geometry')
    return dict(status='PASS_LITERAL_AMBIENT_CAP_FLOWS',cases=len(receipts),wrong_geometry_control=rejected,receipts=receipts,scope='Finite corroboration; universal claim is proved separately.')

if __name__=='__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True));print('PASS_LITERAL_AMBIENT_CAP_FLOWS')
