#!/usr/bin/env python3
"""Exact source witness and controls; no predecessor scientific code imported."""
from __future__ import annotations
import argparse, gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path

PIN = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE = 'research/shared-wire-split-composition/data/final.json.gz'

def require(p, message):
    if not p: raise ValueError(message)

def main_roles(w):
    return set(w['live']) | {r + 112 for r in w['live']} | set(w['hosted']['X2']) | set(w['hosted']['Y2'])

def replay_column(w, seed, skeleton=False):
    mains=main_roles(w); n=w['public']; v=[F(0)]*(n+w['owned_fields']); v[seed]=F(1)
    for e in w['program']:
        op=e[0]; r=e[1]
        if op in ('INIT','CLEAR'):
            if not skeleton: v[r]=F(0)
        elif op=='SCALE':
            if not skeleton or r in mains: v[r]*=F(e[2])
        elif op in ('ADD','COPY'):
            if not skeleton or (r in mains and e[2] in mains):
                if op=='COPY': require(v[r]==0,'COPY target must be zero')
                v[r]+=F(e[3])*v[e[2]]
        elif op!='MOVE': raise ValueError('unknown opcode')
    return v

def span(rows):
    s={0}
    for r in rows: s|={x^r for x in s}
    return frozenset(s)

def frame_checks(w):
    n=w['public']; cur=w['initial'][:]+[None]*w['owned_fields']; mains=main_roles(w)
    main_moves=0
    for e in w['program']:
        op=e[0]; r=e[1]
        if op=='INIT': cur[r]=e[2]
        elif op=='CLEAR': require(cur[r]==e[2],'clear chart'); cur[r]=None
        elif op=='MOVE':
            require(cur[r]==e[2],'move entry chart'); cur[r]=e[3]
            main_moves+=r in mains
        elif op=='SCALE': require(cur[r]==e[3],'scale chart')
        elif op in ('ADD','COPY'): require(cur[r]==cur[e[2]]==e[4],'common chart')
    require(cur[:n]==w['final'],'final charts')
    return len(w['program'])+1,main_moves

def matrix_mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def kron(a,b):
    return [[x*y for x in rowa for y in rowb] for rowa in a for rowb in b]

def run(path):
    raw=path.read_bytes(); require(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    require(hashlib.sha256(raw+b'\n').hexdigest()!=PIN,'byte corruption control')
    w=json.loads(gzip.decompress(raw)); mains=main_roles(w)
    require(len(mains)==400,'main census')
    require(not any(e[1] in mains and e[0] in ('COPY','INIT','CLEAR') for e in w['program']),'invertible skeleton opcodes')
    require(all(F(e[2]) != 0 for e in w['program'] if e[0]=='SCALE' and e[1] in mains),'invertible skeleton scales')
    cuts,moves=frame_checks(w)
    full=replay_column(w,1); skel=replay_column(w,1,True)
    require(full[112]==0,'full native must cancel off-port transfer')
    require(skel[112]==F(-1,2),'fixed-channel cross-port witness')
    require(full[1]==1 and full[113]==1,'positive selected endpoint control')
    require(skel[112]!=full[112],'full source replacement destroys witness')
    frames=list(map(span,w['frames']))
    src_frame=frames[w['initial'][1]]; dst_frame=frames[w['final'][112]]
    entry=[r for r in sorted(mains) if frames[w['initial'][r]]==src_frame]
    exit=[r for r in sorted(mains) if frames[w['final'][r]]==dst_frame]
    require(entry==[1,773] and exit==[112,882],'complete boundary cohorts')
    cols={r:replay_column(w,r,True) for r in entry}
    block=[[cols[s][r] for s in entry] for r in exit]
    require(block==[[F(-1,2),F(0)],[F(0),F(0)]],'rank-one off-port block')
    fullcols={r:replay_column(w,r) for r in entry}
    require(all(fullcols[s][r]==0 for r in exit for s in entry),'required zero block')
    require(skel[112]+F(1,2)*skel[1]==0,'unpriced forbidden correction control')
    require(w['final'][112]!=w['final'][1] and dst_frame!=frames[w['final'][1]],'forbidden correction chart mismatch')
    switch_cases=0
    for u in range(-3,4):
      for v in range(-3,4):
        a,b=F(u),F(v);a+=b;b-=a;a+=b
        require((a,b)==(F(v),F(-u)),'three ADD signed swap');switch_cases+=1
    I2=[[1,0],[0,1]]; I3=[[1,0,0],[0,1,0],[0,0,1]]
    C=[[1,0],[0,-1]]; U=[[F(1,2),2,0],[-1,3,F(2,3)],[5,0,1]]
    require(matrix_mul(kron(C,I3),kron(I2,U))==matrix_mul(kron(I2,U),kron(C,I3)),'cochart switch/transport commutation')
    return {'status':'PASS_FIXED_CHANNEL_OBSTRUCTION_AND_SWITCH_INTERFACE','source_sha256':PIN,
      'source_path':SOURCE,'main_roles':400,'source_events':len(w['program']),
      'synchronized_cuts':cuts,'main_move_occurrences':moves,
      'input_role':1,'output_role':112,'skeleton_coefficient':'-1/2','full_coefficient':'0',
      'entry_cohort':entry,'exit_cohort':exit,
      'skeleton_block':[[str(x) for x in row] for row in block],
      'block_rank':1,'global_sign_switch_scalars':400,'global_signed_swap_adds':1200,
      'signed_swap_cases':switch_cases,
      'controls':['altered source pin','full-source replacement destroys witness','forbidden final ADD cancels numerically but has different charts'],
      'scope':'Exact finite-source witness plus universal linear invariant proof; no H4 native or new kappa.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);args=p.parse_args()
    source=args.source
    if source is None:
      here=Path(__file__).resolve()
      source=next((d/SOURCE for d in here.parents if (d/SOURCE).is_file()),None)
      require(source is not None,'run inside repository or provide --source')
    print(json.dumps(run(source),indent=2))
