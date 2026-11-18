#!/usr/bin/env python3
"""Independent exact replay of native whole-record source gadgets.

Uses sets of input columns and rational vector-space inclusion. It imports no
author compiler, field arithmetic, matrix data, or author replay routine.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'

def require(t,m):
    if not t:raise ValueError(m)

def qrank(rows):
    a=[[Fraction(x)for x in r]for r in rows];r=0
    for c in range(8):
        k=next((k for k in range(r,len(a))if a[k][c]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r];d=a[r][c];a[r]=[x/d for x in a[r]]
        for k in range(r+1,len(a)):
            if a[k][c]:
                d=a[k][c];a[k]=[x-d*y for x,y in zip(a[k],a[r])]
        r+=1
    return r

def replay(layout,word,events=None,check_semantics=True):
    roots=layout['root_table'];planes=layout['A2'];middles=layout['D4'];donors=word['native_donors'];receivers=word['native_receivers']
    n=len(donors);r=len(word['source_forms'][0]);degree=word['field_polynomial'].bit_length()-1
    require(n==len(receivers),'paired source/receiver counts')
    require(all(0<=x<111 for x in donors+receivers),'actual native input/output owners')
    require(len(set(donors))==n and len(set(receivers))==n,'distinct native owners')
    @lru_cache(None)
    def basis(chart):
        if chart=='G':return ()
        if chart=='Hub':return tuple(tuple(int(j==k)for k in range(8))for j in range(8))
        idx=int(chart[1:])
        if chart.startswith('L'):
            require(0<=idx<111,'native source line');return (tuple(roots[idx]),)
        if chart.startswith('H'):
            require(0<=idx<len(planes),'indexed native A2 plane')
            rows=tuple(tuple(roots[j])for j in planes[idx]);require(qrank(rows)==2,'real A2 rank');return rows
        if chart.startswith('D'):
            require(0<=idx<len(middles),'indexed native D4 flat')
            rows=tuple(tuple(roots[j])for j in middles[idx]);require(qrank(rows)==4,'real D4 rank');return rows
        if chart.startswith('F'):
            require(0<=idx<111,'native destination facet');v=roots[idx];p=next(i for i,x in enumerate(v)if x)
            return tuple(tuple(v[p]*int(t==k)-v[k]*int(t==p)for t in range(8))for k in range(8)if k!=p)
        raise ValueError('unrecognized chart '+chart)
    @lru_cache(None)
    def inclusion(source,target):
        u=basis(source);v=basis(target);a=qrank(u);b=qrank(v)
        require(a<b and qrank(u+v)==b,f'no strict chart inclusion {source}->{target}')
        return b-a
    live={};initial={};seen=set();owned=set();high=0;columns=[]
    for kind,roles in [('X',donors),('Y',receivers)]:
        for j,role in enumerate(roles):
            for c in range(r):
                for b in range(degree):
                    name=f'{kind}{j}_{c}_b{b}';position=len(columns);columns.append(name)
                    initial[name]=frozenset([position]);live[name]=[initial[name],f'L{role}'if kind=='X'else'G'];seen.add(name)
    counts=Counter();profile=Counter();owned_profile=Counter();dirty=0
    for t,event in enumerate(events if events is not None else word['events']):
        counts[event[0]]+=1
        if event[0]=='INIT':
            _,name,chart=event;basis(chart);require(name not in seen,f'fresh helper at {t}');seen.add(name)
            live[name]=[frozenset(),chart];owned.add(name);high=max(high,len(owned))
        elif event[0]=='ADD':
            _,dst,src=event;require(dst!=src and dst in live and src in live,f'live distinct ADD at {t}')
            require(live[dst][1]==live[src][1],f'co-located ADD at {t}')
            live[dst][0]=live[dst][0]^live[src][0]
        elif event[0]=='MOVE':
            _,name,target=event;require(name in live,f'live MOVE at {t}');gap=inclusion(live[name][1],target)
            profile[gap]+=1
            if name in owned:owned_profile[gap]+=1
            live[name][1]=target
        elif event[0]=='CLEAR':
            _,name=event;require(name in owned,f'only live owned helper cleared at {t}')
            dirty+=bool(live[name][0]);owned.remove(name);del live[name]
        else:raise ValueError('unknown event '+event[0])
    require(not owned and set(live)==set(initial),'all owned lifetimes closed, originals retained')
    failures=[]
    for j in range(n):
        for c in range(r):
            for b in range(degree):
                x=f'X{j}_{c}_b{b}'
                if live[x]!=[initial[x],'Hub']:failures.append(x)
    for i in range(n):
        for c in range(r):
            for b in range(degree):
                y=f'Y{i}_{c}_b{b}';want=initial[y]
                for j in range(n):
                    if j!=i:want=want^initial[f'X{j}_{c}_b{b}']
                if live[y]!=[want,f'F{receivers[i]}']:failures.append(y)
    if check_semantics:require(not failures,'source restoration/output identity: '+repr(failures))
    digest=sha256(json.dumps([[name,sorted(live[name][0]),live[name][1]]for name in columns],separators=(',',':')).encode()).hexdigest()
    return {'counts':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),'owned_upward_profile':dict(sorted(owned_profile.items())),'dirty_CLEAR':dirty,'peak_owned_binary_records':high,'original_binary_columns':len(columns),'field_degree':degree,'bank_field_dimension':r,'source_count':n,'simultaneous_identity_blocks':n*(n-1),'final_state_sha256':digest,'semantic_failures':failures,'distinct_strict_move_pairs_checked':inclusion.cache_info().currsize}

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--author-result',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    lr=gzip.decompress(a.layout.read_bytes());require(sha256(lr).hexdigest()==LAYOUT_HASH,'pinned geometry');layout=json.loads(lr)
    wr=a.word.read_bytes();word=json.loads(wr);ar=json.loads(a.author_result.read_text());require(sha256(wr).hexdigest()==ar['word_sha256'],'author word digest')
    got=replay(layout,word);want=ar['invoice']
    for key in ['counts','movement_profile','owned_upward_profile','dirty_CLEAR','peak_owned_binary_records','original_binary_columns']:
        require(json.loads(json.dumps(got[key]))==want[key],'independent invoice agreement '+key)
    i=next(i for i,e in enumerate(word['events'])if e[0]=='ADD'and e[1].startswith('Y'))
    mutant=word['events'][:i]+word['events'][i+1:];miss=replay(layout,word,mutant,False)['semantic_failures'];require(miss,'omitted decoding ADD detected')
    i=next(i for i,e in enumerate(word['events'])if e[0]=='MOVE'and e[1].startswith('E'))
    mutant=word['events'][:i]+word['events'][i+1:]
    try:replay(layout,word,mutant);raise RuntimeError('missing paid source MOVE accepted')
    except ValueError as exc:bad_move=str(exc)
    # Delete a Y baseline bit from the initial state indirectly by inserting a
    # second original into it; this tests that unrestricted input columns matter.
    i=next(i for i,e in enumerate(word['events'])if e[0]=='MOVE'and e[1].startswith('Y'))
    ys=[f'Y0_0_b{k}'for k in range(got['field_degree'])]
    mutant=word['events'][:i]+[['ADD',ys[0],ys[1]]]+word['events'][i:]
    baseline_fail=replay(layout,word,mutant,False)['semantic_failures'];require(baseline_fail,'arbitrary Y baseline corruption detected')
    out={'status':'PASS_INDEPENDENT_NATIVE_WORD_REPLAY','word_sha256':sha256(wr).hexdigest(),'author_result_sha256':sha256(a.author_result.read_bytes()).hexdigest(),'layout_uncompressed_sha256':LAYOUT_HASH,'independent_invoice':got,'negative_controls':{'removed_receiver_ADD':miss,'removed_source_MOVE':bad_move,'corrupted_arbitrary_Y_baseline':baseline_fail},'author_code_imported':False,'geometry_test':'rational strict span inclusion','linear_state_representation':'sets of original binary columns'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],got['source_count'],got['counts'],got['movement_profile'])

if __name__=='__main__':main()
