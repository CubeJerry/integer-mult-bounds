#!/usr/bin/env python3
"""Independent exact rational replay, source cuts and movement account.
@CubeJerry with OpenAI assistance. Apache-2.0. No author engine imported.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def span(frame):
    s={0}
    for v in frame:
        need(v not in s,'independent chart basis')
        s|={w^v for w in tuple(s)}
    return frozenset(s)

def plus(a,b,c):
    r=dict(a)
    for i,x in b.items():
        z=r.get(i,F(0))+c*x
        if z:r[i]=z
        else:r.pop(i,None)
    return r

def replay(w,mode='seed',controls=False,hook=None):
    spaces=[span(f) for f in w['frames']]
    public=w['public'];rows={i:{i:F(1)}for i in range(public)};loc=dict(enumerate(w['initial']))
    raw=Counter();owned=Counter();counts=Counter();peak=0;lifetimes=0;trace={};retire=[]
    marks=w.get('echo',{}).get('markers',{})
    relays=w.get('echo',{}).get('relay_fields',[])
    entry=None
    for t,o in enumerate(w['program']):
        if hook: hook(t,'before',o,rows,loc)
        code=o[0];counts[code]+=1
        if code=='INIT':
            _,i,c=o;need(i>=public and i not in rows,'fresh owner');rows[i]={};loc[i]=c;lifetimes+=1
        elif code=='CLEAR':
            _,i,c=o;need(i>=public and loc[i]==c,'owned clear chart');retire.append((t,i,c,dict(rows[i])))
            if i in relays and mode not in ['dirty_echo','zero_erasure']:
                need(not rows[i],'declared clean relay not zero')
                C=w['echo']['C'];D=w['echo']['D']
                want=C if mode=='zero_roundtrip' and i==relays[0] else D
                need(c==want,'declared clean relay retirement chart')
            del rows[i];del loc[i]
        elif code=='MOVE':
            _,i,c,d,isowned=o;need(i in rows and loc[i]==c,'actual departure chart')
            need((spaces[c]<spaces[d] or spaces[d]<spaces[c]),'strict nested move')
            need(isowned==(i>=public),'owner classification')
            rank=abs(len(w['frames'][c])-len(w['frames'][d]));(owned if isowned else raw)[rank]+=1
            if mode=='dirty_echo' and i in relays and d==127:
                trace['borrowed_Hub_'+str(i)]=dict(rows[i])
            if mode=='seed' and i in [400,401] and d==127:
                trace['borrowed_Hub_'+str(i)]=dict(rows[i])
            loc[i]=d
        elif code=='ADD':
            _,i,j,c,f=o;need(loc.get(i)==f and loc.get(j)==f,'cocharted read')
            rows[i]=plus(rows[i],dict(rows[j]),F(c))
        elif code=='SCALE':
            _,i,c,f=o;need(loc.get(i)==f,'cocharted scale');rows[i]={j:F(c)*x for j,x in rows[i].items() if F(c)*x}
        else:raise ValueError('unrecognized instruction '+code)
        if hook: hook(t+1,'after',o,rows,loc)
        peak=max(peak,len(rows)-public)
        if t+1==marks.get('relay_entry'):entry={i:dict(rows[i])for i in relays}
        if t+1==marks.get('relay_restoration'):
            need(entry is not None,'real relay entry captured')
            need(all(rows[i]==entry[i]for i in relays),'restored exact dirty relay values')
            trace['relay_restoration']=True
    need(set(rows)==set(range(public)),'all owners retired')
    return rows,loc,dict(raw),dict(owned),dict(counts),peak,lifetimes,trace,retire

