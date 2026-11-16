#!/usr/bin/env python3
"""Exact endpoint-preserving reduction of a finite linear record word.

The reduced word is a different source interface: unobserved history and stock
are not promised to survive. No full supplier or exponent claim is made.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from review_leaf_capacity import chart_basis, echelon


def forward(w):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
    sources=[]
    for op,n,*q in w['operations']:
        sources.append(v[n] if op=='ADD' else None)
        if op=='INIT':v[n]=0
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='CLEAR':del v[n]
    return v,sources


def dead_pass(w):
    final,src=forward(w)
    adj={f'{p}{i}':1<<(i+(111 if p=='Y' else 0)) for p in 'XY' for i in range(111)}
    keep=[True]*len(w['operations']);removed=[]
    for k in reversed(range(len(keep))):
        op,n,*q=w['operations'][k]
        if op=='CLEAR':adj[n]=0
        elif op=='ADD':
            if not adj[q[0]] or not src[k]:
                keep[k]=False;removed.append({'index':k,'operation':w['operations'][k],
                                             'reason':'zero_final_sensitivity' if not adj[q[0]] else 'zero_source_value'})
            else:adj[n]^=adj[q[0]]
        elif op=='INIT':del adj[n]
    ops=[o for k,o in enumerate(w['operations']) if keep[k]]
    used={n for op,*q in ops if op=='ADD' for n in q}
    dead={o[1] for o in ops if o[0]=='INIT' and o[1] not in used}
    ops=[o for o in ops if not (o[0] in ('INIT','MOVE','CLEAR') and o[1] in dead)]
    z=copy.deepcopy(w);z['operations']=ops
    assert forward(z)[0]==final
    return z,{'removed_ADD':removed,'removed_owners':sorted(dead)}


def fuse_routes(w):
    """Only fuse consecutive per-record moves with no intervening record use."""
    ops=copy.deepcopy(w['operations']);keep=[True]*len(ops);pending={};removed=[]
    for k,o in enumerate(ops):
        op,n,*q=o
        if op=='MOVE':
            if n in pending:
                old=pending[n];keep[old]=False;removed.append({'index':old,'operation':ops[old]})
            pending[n]=k
        elif op=='ADD':
            pending.pop(n,None);pending.pop(q[0],None)
        elif op in ('INIT','CLEAR'):
            pending.pop(n,None)
    z=copy.deepcopy(w);z['operations']=[o for k,o in enumerate(ops) if keep[k]]
    assert forward(z)[0]==forward(w)[0]
    return z,removed


def independent_replay(w):
    C={n:tuple(tuple(x for x in row) for row in chart_basis(r)) for n,r in w['charts'].items()}
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
    at={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
    owned=set();born=set();counts=Counter();profile=Counter();dirty=peak=0;memo={}
    def sub(x,y):
        k=(x,y)
        if k not in memo:memo[k]=len(echelon(C[x]+C[y])[0])==len(C[y])
        return memo[k]
    for step,(op,n,*q) in enumerate(w['operations'],1):
        counts[op]+=1
        if op=='INIT':
            assert n not in v and n not in born
            v[n]=0;at[n]=q[0];owned.add(n);born.add(n)
        elif op=='ADD':
            assert n in v and q[0] in v and sub(at[n],at[q[0]]) and sub(at[q[0]],at[n]),(step,n,q)
            v[q[0]]^=v[n]
        elif op=='MOVE':
            assert n in v
            assert sub(q[0],at[n]) if n in owned else sub(at[n],q[0]),(step,n,q,'direction')
            d=abs(len(C[q[0]])-len(C[at[n]]));assert d>0
            profile[d]+=1;at[n]=q[0]
        elif op=='CLEAR':
            assert n in owned;dirty+=bool(v[n]);owned.remove(n);del v[n],at[n]
        peak=max(peak,len(owned))
    assert not owned and len(v)==222
    for i in range(111):
        assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
        assert v[f'Y{i}']==(1<<(111+i))^((1<<i) if i in w['targets'] else 0) and at[f'Y{i}']==f'F{i}'
    return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
            'dirty_CLEAR':dirty,'peak_owners':peak,'all_222_endpoints':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);original=independent_replay(w);rounds=[]
    for _ in range(12):
        n=len(w['operations']);w,d=dead_pass(w);w,m=fuse_routes(w)
        rounds.append({'dead_code':d,'fused_moves':m,'operations_after':len(w['operations'])})
        if len(w['operations'])==n:break
    else:raise AssertionError('not stabilized')
    new=independent_replay(w)
    # Keep only authenticated geometry, endpoint target set and source provenance;
    # inherited milestones/stock metadata describe the old word, not this one.
    result_word={k:w[k] for k in ('source_path','source_sha256','charts','targets','operations')}
    result_word.update({'schema':'endpoint-reduced-native-word-v1',
                        'base_word_sha256':hashlib.sha256(raw).hexdigest(),
                        'scope':'Partial native endpoints only. Old history, source cuts, seed code and later source availability are not inherited.'})
    a.out.mkdir(parents=True,exist_ok=True)
    blob=(json.dumps(result_word,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(blob)
    report={'status':'PASS_ENDPOINT_REDUCTION_AND_EXACT_GEOMETRY',
            'base_word_sha256':hashlib.sha256(raw).hexdigest(),'word_sha256':hashlib.sha256(blob).hexdigest(),
            'before':original,'after':new,'rounds':rounds,'targets':w['targets'],
            'source_interface_changed':True,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('rounds','targets')}))


if __name__=='__main__':main()
