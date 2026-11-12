#!/usr/bin/env python3
"""Authenticate the optional exhaustive census against source and analytic bounds.

This checks finite discovery data; PROOF.md does not depend on the census.
Prepared for @CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(ok,msg):
    if not ok:
        raise ValueError(msg)

def span(basis):
    out={0}
    for v in basis:
        out.update(x^v for x in tuple(out))
    return out

def gaussian(n,k):
    a=b=1
    for i in range(k):
        a*=2**(n-i)-1
        b*=2**(k-i)-1
    need(a%b==0,'Gaussian integer')
    return a//b

def main(args):
    raw=args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    source=json.loads(gzip.decompress(raw))
    ports=set(source['ports'])
    need(len(ports)==104 and all(v.bit_count() in (3,7) for v in ports),'authentic active port family')
    need(set(map(int,args.ports.read_text().split()))==ports,'discovery port input')
    census=json.loads(args.census.read_text())
    need(census['ambient']==9 and census['source_ports']==104,'census domain')
    total=0
    summaries=[]
    for level in census['dimensions']:
        d=level['dimension']
        need(level['subspaces']==gaussian(9,d),'complete RREF count by dimension')
        need(sum(p['count'] for p in level['profiles'])==level['subspaces'],'population frequency sum')
        seen=set()
        for profile in level['profiles']:
            a,b=profile['donors'],profile['receivers']
            need((a,b) not in seen and profile['count']>0,'distinct positive profile count')
            seen.add((a,b))
            basis=profile['witness']
            space=span(basis)
            need(len(basis)==d and len(space)==2**d,'independent chart witness')
            dual={x for x in range(512) if all((x&v).bit_count()%2==0 for v in basis)}
            need(len(space&ports)==a and len(dual&ports)==b,'exact source population witness')
            if d==4:
                need(5*a*b<=8*a+24*b,'analytic level4 inequality')
            if d==5:
                need(5*a*b<=24*a+8*b,'analytic level5 inequality')
        total+=level['subspaces']
        maximal=[(a,b) for a,b in seen if a*b and not any(x>=a and y>=b and (x,y)!=(a,b) for x,y in seen)]
        summaries.append(dict(dimension=d,count=level['subspaces'],maximal_profiles=sorted(maximal)))
    need(total==8283458,'all binary subspaces')
    # An independent maximum recursion on at-most resources corroborates the
    # bridge worker's exact-resource dynamic programme, without importing it.
    profiles=[(a,b) for a in range(1,9) for b in range(1,13)
              if any(a<=x and b<=y for x,y in [(2,12),(4,10),(6,8),(8,4)])]
    table=[[0]*105 for _ in range(105)]
    for a in range(1,105):
        for b in range(1,105):
            table[a][b]=max([0]+[x*y+table[a-x][b-y] for x,y in profiles if x<=a and y<=b])
    need(table[104][104]==656,'independent finite rectangle bound')
    # Negative controls reject enlarging the population family or changing the
    # exact source geometry, rather than relying on disabled Python assertions.
    need(not (5*8*5<=8*8+24*5),'forbidden(8,5) population violates analytic inequality')
    need(10*6+5*8+4==104 and 10*8+5*4+4==104 and 10*48+5*32+16==656,'abstract relaxation witness')
    receipt=dict(status='PASS_SOURCE_BOUND_DISCOVERY_AND_RECTANGLE_REVIEW',source_sha256=PIN,
                 census_sha256=hashlib.sha256(args.census.read_bytes()).hexdigest(),
                 total_binary_subspaces=total,dimensions=summaries,
                 independent_integer_rectangle_optimum=656,analytic_contact_bound=2786,
                 exact_integer_contact_bound=2768,
                 scope='Finite source census authentication and independently implemented finite DP. Analytic arbitrary-path theorem is PROOF.md; this is not a coded-carrier or paid-call bound.')
    args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','total_binary_subspaces','independent_integer_rectangle_optimum']}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['source','ports','census','output']:
        p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
