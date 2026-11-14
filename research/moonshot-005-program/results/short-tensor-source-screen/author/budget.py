#!/usr/bin/env python3
"""Certified short-caller budgets. No floating-point gate or scientific imports."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,argparse,hashlib
HERE=Path(__file__).resolve().parent;DEN=10**45
def need(ok,msg):
    if not ok:raise ValueError(msg)
def root(z,k):
    x=1<<((z.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+z//x**(k-1))//k
        if y>=x:break
        x=y
    while x**k>z:x-=1
    while (x+1)**k<=z:x+=1
    need(x**k<=z<(x+1)**k,'exact integer root');return x
@lru_cache(None)
def p(r):
    if r in(0,1):return F(r),F(r)
    a=root(r**199*DEN**200,200);lo,hi=F(a,DEN),F(a+1,DEN)
    need(lo**200<=F(r)**199<hi**200,'power enclosure');return lo,hi
def add(*xs):return sum(x[0]for x in xs),sum(x[1]for x in xs)
def mul(c,x):
    c=F(c);return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def sub(x,y):return add(x,mul(-1,y))
def div(x,y):
    need(y[0]>0,'positive divisor');z=[a/b for a in x for b in y];return min(z),max(z)
def show(x):return dict(exact=[str(z)for z in x],decimal=[float(z)for z in x])
def moment(H):return add(*(mul(c,p(int(r)))for r,c in H.items()))
def wrap(b,a):return add(mul(2,p(1+2*a*b)),*(mul(4,p(1+j*b))for j in range(1,a+1)),mul(-4,p(1)),*(mul(-4,p(j*b))for j in range(1,a)))
def gap(a,r=14):return sub(wrap(17,a),add(mul(8*a,p(17)),mul(F(4*a*8,208),p(r))))
def main(out):
    G={a:gap(a)for a in range(1,10)};native={a:mul(F(1,2*a),G[a])for a in G}
    need(sub(G[4],G[3])[0]>0 and sub(G[5],G[4])[1]<0,'total room optimum a4')
    need(sub(native[3],native[2])[0]>0 and sub(native[4],native[3])[1]<0,'per-native room optimum a3')
    delta=sub(add(p(8),p(9)),p(17));rank16={a:gap(a,16)for a in(1,2,3,4)}
    need(rank16[2][1]<0 and sub(rank16[2],rank16[1])[0]>0 and sub(rank16[3],rank16[2])[1]<0,'rank16 maximum a2 negative')
    need(sub(native[3],mul(2,delta))[1]<0,'two complete station cohorts excluded globally')
    need(sub(G[3],mul(6,delta))[0]>0 and sub(G[4],mul(8,delta))[1]<0,'one station cohort differs by stage count')
    rowbirth={}
    for c in(16,17):
        stop=sub(add(p(c-1),p(18-c)),p(17));extra=sub(add(p(c-2),mul(104,stop)),p(16))
        need(extra[0]>0,'proper direct-original row gather loses at endpoint '+str(c))
        rowbirth[str(c)]=dict(public_stop_surcharge=show(stop),complete_row_excess_over_hub=show(extra))
    old=json.loads((HERE/'source/retained-FULL-RESULT.json').read_text());C=json.loads((HERE/'source/retained-caller.json').read_text())
    need(old['word_sha256']=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','retained native pin')
    need(len(C['types']['A']['ports'])==96 and len(C['types']['B']['ports'])==8,'actual A/B port counts')
    oldnet=sub(moment(old['native']['paid']),moment(old['native']['helpers']));conversion=add(mul(16,p(1)),mul(16,p(8)))
    h9={}
    for a in(3,4,9):
        raw=mul(104,wrap(8,a));full=sub(raw,mul(2*a,add(oldnet,conversion)));freequeries=sub(raw,mul(2*a,add(oldnet,mul(16,p(8)))))
        need(full[1]<0 and freequeries[1]<0,'retained h9 source rejected')
        h9[str(2*a)]=dict(complete_paid_conversion_gap=show(full),added_queries_granted_free_gap=show(freequeries),wrapper_moment=show(raw))
    saved=mul(F(1,2),sub(mul(2,delta),native[3]))
    R=dict(status='PASS_SHORT_TENSOR_SOURCE_SCREEN',t='199/200',
        rank14_total_gap={str(2*a):show(G[a])for a in G},rank14_spare_per_native_port={str(2*a):show(native[a])for a in G},
        total_gap_maximum_stages=8,spare_per_native_maximum_stages=6,
        tag9_stop_surcharge=show(delta),two_cohort_maximum_residual_per_native_port=show(sub(native[3],mul(2,delta))),
        maximum_uniform_station_visits_per_native=show(div(mul(208,native[3]),delta)),
        two_cohort_required_decoder_moment_reduction_per_plane=show(mul(208,saved)),
        hub_row_rank16_total_gap={str(2*a):show(v)for a,v in rank16.items()},direct_proper_row_birth=rowbirth,
        retained_h9_native_net=show(oldnet),retained_h9_actual_B_conversion=show(conversion),retained_h9=h9,
        scope='Caller and source-specific necessary budgets only. h18 row-family exclusions retain separate rows and nonnegative other net cost. No h18 native or new kappa.')
    out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(json.dumps({k:R[k]for k in('status','total_gap_maximum_stages','spare_per_native_maximum_stages','scope')},sort_keys=True))
if __name__=='__main__':
    q=argparse.ArgumentParser();q.add_argument('--out',type=Path,default=HERE/'BUDGET.json');a=q.parse_args();main(a.out)
