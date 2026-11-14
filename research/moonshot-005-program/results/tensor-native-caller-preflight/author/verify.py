#!/usr/bin/env python3
"""Exact rational preflight for a pinned caller invoice; no scientific imports.

All exponent evaluations enclose x^(199/200) by certified integer roots.
The universal stage/geometry conclusions use the inequalities in PROOF.md;
finite evaluations alone are not those theorems.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEN = 10**45
T = F(199, 200)

def need(test, msg):
    if not test:
        raise ValueError(msg)

def root_floor(z, k):
    need(z >= 0 and k >= 1, 'integer-root domain')
    if z < 2:
        return z
    x = 1 << ((z.bit_length()+k-1)//k)
    while True:
        y = ((k-1)*x + z//pow(x,k-1))//k
        if y >= x:
            break
        x = y
    while pow(x,k) > z:
        x -= 1
    while pow(x+1,k) <= z:
        x += 1
    need(pow(x,k) <= z < pow(x+1,k), 'integer-root certificate')
    return x

@lru_cache(None)
def power(r):
    need(isinstance(r,int) and r >= 0, 'nonnegative integer rank')
    if r == 0:
        return F(0), F(0)
    if r == 1:
        return F(1), F(1)
    z=pow(r,199)*pow(DEN,200)
    a=root_floor(z,200)
    lo,hi=F(a,DEN),F(a+1,DEN)
    need(lo**200 <= F(r)**199 < hi**200, 'outward power enclosure')
    return lo,hi

def add(*intervals):
    return sum(x[0] for x in intervals),sum(x[1] for x in intervals)

def mul(q,x):
    q=F(q)
    return (q*x[0],q*x[1]) if q>=0 else (q*x[1],q*x[0])

def sub(x,y):
    return add(x,mul(-1,y))

def div(x,y):
    need(y[0]>0,'positive denominator interval')
    p=[a/b for a in x for b in y]
    return min(p),max(p)

def show(x):
    return {'exact':[str(a) for a in x], 'decimal':[float(a) for a in x]}

def rho(rows,rank,n):
    return mul(F(rows,n),power(rank))

def gap(b,a,owned=(F(0),F(0)),queries=4):
    """Per-port upper bound, 2a stages, two private row planes."""
    terms=[mul(2,power(1+2*a*b)),mul(-queries,power(1)),
           mul(-8*a,power(b)),mul(-4*a,owned)]
    terms += [mul(4,power(1+j*b)) for j in range(1,a+1)]
    terms += [mul(-4,power(j*b)) for j in range(1,a)]
    return add(*terms)

def invoice(b,a,n,rows=0,rank=0):
    t=Counter({1+2*a*b:2*n})
    p=Counter({1:4*n,b:8*a*n})
    for j in range(1,a+1): t[1+j*b]+=4*n
    for j in range(1,a): p[j*b]+=4*n
    if rows: p[rank]+=4*a*rows
    return dict(T=dict(sorted(t.items())),P=dict(sorted(p.items())))

def moment(hist):
    return add(*(mul(c,power(int(r))) for r,c in hist.items()))

def source_caller():
    c=json.loads((HERE/'source/caller.json').read_text())
    need(c['stages']==18,'pinned caller has eighteen stages')
    need(sum(e[0]=='J' for e in c['events'])==18,'eighteen native events')
    out={}
    for ty,d in c['types'].items():
        targets=Counter()
        for dg in d['diagonal']:
            need(dg[0]%2==1 and dg[1]==0,'one positive head per target')
            targets[sum(dg[2:])]+=1
        expected=Counter({18:2})
        expected.update({j:4 for j in range(1,10)})
        need(targets==expected,'exact per-port target body masks')
        idles=Counter();queries=0
        for e in c['events']:
            if e[0]!=ty: continue
            if e[1]=='QUERY':queries+=1
            if e[1]=='IDLE_ONE':
                need(len(set(e[3]))==len(e[3]),'idle distinct complete stage blocks')
                idles[len(e[3])]+=1
        want=Counter({j:4 for j in range(1,9)})
        if ty=='B':want[1]+=36
        need(idles==want and queries==4,'exact per-port wrapper inventory')
        fields=4 if ty=='A' else 2
        # At every body rank b, missing main routes and extra B idles cancel.
        need(18*fields+idles[1]==76,'type A/B raw-body route cancellation')
        out[ty]=dict(ports=len(d['ports']),native_main_fields=fields,
                     target_body_counts=dict(sorted(targets.items())),
                     idle_body_counts=dict(sorted(idles.items())),queries=queries)
    return out

def main(output):
    pins=json.loads((HERE/'source/PINS.json').read_text())
    for p in pins:
        need(hashlib.sha256((HERE/'source'/p['file']).read_bytes()).hexdigest()==p['sha256'],
             'source pin '+p['file'])
    caller=source_caller()
    cases={}
    for name,h,n,rows,rk in [
        ('complex_square',81,104**2,64,49),
        ('bit_square_hub_packets',64,111**2,81,64),
        ('complex_cube_free_control',729,104**3,0,0),
        ('bit_cube_free_control',512,111**3,0,0),
    ]:
        b=h-1; rc=rho(rows,rk,n) if rows else (F(0),F(0))
        entries={}
        for a in (1,2,3,9):
            free=gap(b,a);full=gap(b,a,rc)
            inv=invoice(b,a,n,rows,rk)
            direct=mul(F(1,n),sub(moment(inv['T']),moment(inv['P'])))
            need(max(full[0],direct[0])<=min(full[1],direct[1]),'independent histogram agreement')
            entries[str(2*a)]=dict(free_decoder_gap_per_port=show(free),
                row_model_gap_per_port=show(full),
                maximum_owned_moment_density=show(mul(F(1,4*a),free)),
                maximum_productive_rank=1+2*a*b,ambient_cap=h+2*a*b)
        need(gap(b,1,rc)[1]<0,'two-stage row-model rejection')
        need(sub(gap(b,2,rc),gap(b,1,rc))[1]<0,'negative first stage increment')
        cases[name]=dict(h=h,ports=n,rows_per_plane=rows,price_per_row=rk,
                         owned_moment_per_port=show(rc),stages=entries)
    cx=rho(64,49,10816)
    need(gap(80,1)[0]>0,'free decoder at two stages stays open')
    need(gap(80,2)[1]<0,'four stages fail even with free decoder')
    need(sub(gap(80,2),gap(80,1))[1]<0,'free-decoder sequence decreasing after two stages')
    need(gap(63,2)[0]>0 and gap(63,3)[1]<0 and sub(gap(63,3),gap(63,2))[1]<0,'BIT free-decoder exact stage boundary')
    need(gap(728,1)[1]<-2 and gap(511,1)[1]<-2,'all higher tensor powers start below g0')
    need(gap(36,9)[0]>0 and gap(37,9)[1]<0,'sharp integer fixed-18 free-body threshold')
    need(gap(134,1)[0]>0 and gap(135,1)[1]<0,'sharp integer two-stage free-body threshold')
    # Scoped relaxed controls, deliberately not supplier certificates.
    basecx=gap(8,9,rho(8,7,104));basebit=gap(7,9,rho(9,8,111))
    need(basecx[0]>0 and basebit[0]>0,'existing small geometries not ruled out by relaxation')
    need(gap(80,1,cx,queries=0)[0]>0,'omitting required queries falsely flips the sign')
    cap=mul(F(1,4),gap(80,1)); retained=div(cap,cx)
    currentfree=gap(80,9);currentfull=gap(80,9,cx)
    controls={
        'original_complex_relaxation':show(basecx),
        'original_bit_relaxation':show(basebit),
        'complex_two_stage_queries_omitted_false_positive':show(gap(80,1,cx,queries=0)),
        'complex_two_stage_free_decoder_positive':show(gap(80,1)),
        'complex_four_stage_free_decoder_negative':show(gap(80,2)),
        'fixed18_b36_positive':show(gap(36,9)),
        'fixed18_b37_negative':show(gap(37,9)),
        'two_stage_b134_positive':show(gap(134,1)),
        'two_stage_b135_negative':show(gap(135,1)),
    }
    rescue=dict(
        two_stage_maximum_decoder_moment_per_plane=show(mul(10816,cap)),
        two_stage_maximum_density=show(cap),
        two_stage_current_decoder_moment_per_plane=show(mul(10816,cx)),
        two_stage_maximum_retained_fraction=show(retained),
        two_stage_required_reduction_fraction=show(sub((F(1),F(1)),retained)),
        fixed18_minimum_caller_gain_if_decoder_free=show(mul(-10816,currentfree)),
        fixed18_minimum_total_gain_with_tensor_rows=show(mul(-10816,currentfull)),
        fixed18_decoder_elimination_gain=show(mul(36*10816,cx)),
    )
    report=dict(status='PASS_SCOPED_TENSOR_NATIVE_PREFLIGHT',target_kappa='1/200',
        exponent=str(T),source_caller=caller,cases=cases,rescue=rescue,controls=controls,
        universal_proof='PROOF.md: concavity in a, strict monotonicity in b, and normalized moment monotonicity',
        scope='Fixed pinned eighteen-stage caller is source-bound; all-even-stage conclusions are conditional on its explicitly stated invoice family. No actual higher-label native is claimed, and no arbitrary-caller or shared-ascent impossibility is claimed.',
        kappa_status='No new kappa; both strict suppliers and all five foundations remain open.',
        power_certificates=power.cache_info().currsize)
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':report['status'],'out':str(output),'cases':len(cases),'source_types':list(caller),'negative_controls':len(controls)},sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();main(a.output)
