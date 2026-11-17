#!/usr/bin/env python3
"""Check native D4s, endpoints, 45-port incidence and finite caller movement."""
import argparse
import gzip
import hashlib
import json
import os
import subprocess
import tempfile
from collections import Counter,defaultdict
from fractions import Fraction as F
from functools import cache
from pathlib import Path


def need(value,msg):
    if not value:
        raise ValueError(msg)


def dot(x,y):
    return sum(a*b for a,b in zip(x,y))


@cache
def price(i):
    scale=10**28
    l,r=0,130*scale
    target=i**199*scale**200
    while r-l>1:
        z=(l+r)//2
        if z**200<=target:l=z
        else:r=z
    return F(l,scale),F(r,scale)


def interval(d):
    lo=hi=F(0)
    for i,m in d.items():
        a,b=price(i)
        lo+=m*(a if m>=0 else b);hi+=m*(b if m>=0 else a)
    return lo,hi


def finite(profile):
    native={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    head={2:1,4:25,6:1,8:410}
    def at(m):
        moments=Counter({k:-18*v for k,v in native.items()})
        for k,v in head.items():moments[k]+=18*v
        moments[1]-=222*m;moments[127]+=111*m
        for j in range(1,9):moments[7*j]-=222*m
        for j in range(1,10):moments[1+7*j]+=222*m
        for k,v in profile.items():moments[k]-=18*(m-1)*F(v,240)
        return interval(moments)
    before=at(2)
    for m in range(4,3000,2):
        current=at(m)
        if current[0]>0:
            need(before[1]<0,'earlier source price')
            return m,before,current
        need(current[1]<0,'ambiguous price')
        before=current
    raise ArithmeticError('no bracket for target')


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--native',type=Path,required=True);cli.add_argument('--layout',type=Path,required=True)
    cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args()
    raw=gzip.decompress(args.layout.read_bytes())
    need(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    w=json.loads(raw);roots=w['root_table']
    native=args.native.read_bytes()
    need(hashlib.sha256(native).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
    need(roots[:111]==json.loads(native)['native_roots'],'root data align')
    with tempfile.TemporaryDirectory() as d:
        exe=Path(d)/'dynkin'
        subprocess.run([os.environ.get('CXX','c++'),'-O3','-std=c++17',str(Path(__file__).with_name('dynkin.cpp')),'-o',str(exe)],check=True)
        r=subprocess.run([str(exe)],input=''.join(' '.join(map(str,v))+'\n' for v in roots),text=True,capture_output=True,check=True)
    rows=iter(r.stdout.splitlines());nstars,nD=map(int,next(rows).split())
    proper={tuple(map(int,line.split())) for line in rows}
    need(len(proper)==nD==3150 and proper==set(map(tuple,w['D4'])),'complete Dynkin-star list')
    D=[set(x) for x in w['D4']];A=[set(x) for x in w['A2']];dual=w['dual_D4']
    orth=[{j for j,v in enumerate(roots) if dot(u,v)==0} for u in roots]
    need(all(set.intersection(*(orth[j] for j in d))==D[dual[k]] and dual[dual[k]]==k for k,d in enumerate(D)),'real orthogonal complements')
    for h in A:
        a,b,c=sorted(h)
        need(abs(dot(roots[a],roots[b]))==2 and abs(dot(roots[b],roots[c]))==2 and abs(dot(roots[a],roots[c]))==2,'A2 triple')
    left=Counter();right=Counter();jcnt=Counter();icnt=Counter();moves=Counter();systematic=Counter()
    labels=defaultdict(set)
    for kind,d,h,j,k,i,source,end in w['routes']:
        levels=[1 if kind=='X' else 0]
        if kind=='X':need(j in range(111),'native X');jcnt[j]+=1
        else:need(kind=='Y' and i in range(111),'native Y');icnt[i]+=1
        if h is not None:
            need(j in A[h] and A[h]<=D[d],'source chart nesting')
            if kind=='Y' and j<111:levels.append(1)
            levels.append(2);left[h,d]+=1
        levels.append(4)
        if k is not None:
            need(i in A[k] and A[k]<=D[dual[d]],'terminal chart nesting')
            levels.append(6);right[dual[d],k]+=1
            if i<111:levels.append(7)
        if kind=='X':levels.append(8)
        for a,b in zip(levels,levels[1:]):
            need(b>a,'strict upward route');moves[b-a]+=1
        for side,role,slot,owned in [('X',j,source,kind=='X'),('Y',i,end,kind=='Y')]:
            if slot is not None:
                row,stripe=slot
                need((row,stripe) not in labels[side,role],'native slot repeated')
                labels[side,role].add((row,stripe))
                if owned:systematic[side,role,stripe]+=1
    need(len(left)==len(right)==50400 and set(left.values())==set(right.values())=={1},'every scalar-on-chart port')
    need(set(jcnt.values())==set(icnt.values())=={240} and len(jcnt)==len(icnt)==111,'originals per native root')
    need(all(len(v)==420 for v in labels.values()) and len(labels)==222 and set(systematic.values())=={16},'MDS coordinates')
    moves[8]+=9*240
    need(moves=={1:133200,2:108360,4:5760,8:2160},'all paid movements')
    m,prior,cur=finite(moves)
    out={'base_layout_sha256':hashlib.sha256(raw).hexdigest(),'dynkin_stars':nstars,'distinct_real_D4s':nD,
         'real_public_trajectories':sum(jcnt.values())+sum(icnt.values()),'ports_per_side':len(left),'binary_copies_for_GF64':1440,
         'whole_field_symbol_movements':dict(sorted(moves.items())),'first_even_m_for_the_normalized_movement_profile':m,
         'margin_at_preceding_m':list(map(str,prior)),'margin_at_first':list(map(str,cur)),
         'sum_source_moment_interval':list(map(str,interval({k:F(v,240) for k,v in moves.items()})))}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(f'PASS {nstars} Dynkin stars, {nD} D4s, 53280 physical routes, first finite movement multiple {m}')


if __name__=='__main__':
    main()
