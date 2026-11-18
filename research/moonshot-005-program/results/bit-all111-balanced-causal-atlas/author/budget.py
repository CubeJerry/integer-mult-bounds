#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from functools import cache
from pathlib import Path
import json

@cache
def bound(d):
    scale=10**32;n=d**199*scale**200;low=0;high=d*scale+1
    while high-low>1:
        m=(low+high)//2
        if m**200<=n:low=m
        else:high=m
    return F(low,scale),F(low+(low**200!=n),scale)

def iv(v):
    l=h=0
    for k,c in v.items():
        x,y=bound(k);l+=c*(x if c>=0 else y);h+=c*(y if c>=0 else x)
    return l,h

def add(*terms):
    t=Counter()
    for c,v in terms:
        for l,n in v.items():t[l]+=c*n
    return t

def brackets(z):return [str(x) for x in z]

def run(prof):
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    P=add((36,N),(1,{1:444}),(1,{7*j:444 for j in range(1,9)}))
    T=add((36,H),(1,{127:222}),(1,{1+7*j:444 for j in range(1,10)}))
    limit=add((F(1,36),T),(F(-1,36),P),(1,N),(-1,H));q=iv(prof);room=iv(add((1,limit),(-1,prof)))
    assert room[0]>0
    for m in range(2,100000,2):
        gap=iv(add((F(m,2),T),(-F(m,2),P),(-18*(m-1),H),(18*(m-1),N),(-18*(m-1),prof)))
        if gap[0]>0:break
        assert gap[1]<0
    qmax=iv(limit);loss=(5760*(1-q[1]/qmax[0]),5760*(1-q[0]/qmax[1]))
    return {'profile':{d:str(x) for d,x in prof.items()},'moment':brackets(q),'limiting_room':brackets(room),'moment_decimal':('%.12f'%float(q[0])),'room_decimal':('%.12f'%float(room[0])),'first_even_passing_frozen_movement':m,'first_positive_Tm_minus_Pm':brackets(gap),'normalized_loss_bound_per_5760':brackets(loss)}

if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();ps={'original':{1:F(555),2:F(903,2),4:24,8:9},'four_marginal_surpluses':{1:F(6757,12),2:F(54487,120),4:F(207,10),8:9},'balanced':{1:F(4451,8),2:F(7213,16),4:24,8:9}}
    out={k:run(v) for k,v in ps.items()};a.out.write_text(json.dumps(out,indent=2)+'\n');print({k:[z['moment_decimal'],z['room_decimal'],z['first_even_passing_frozen_movement']] for k,z in out.items()})
