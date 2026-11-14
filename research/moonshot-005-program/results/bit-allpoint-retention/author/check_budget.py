#!/usr/bin/env python3
"""Exact rational-root movement screen and known ordinary ledger; no decoder."""
import argparse,gzip,hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
S=10**40

def root_floor(n,k):
    if n==0:return 0
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:break
        x=y
    while pow(x,k)>n:x-=1
    while pow(x+1,k)<=n:x+=1
    return x

cache={}
def power(r):
    if r not in cache:
        n=pow(r,199)*pow(S,200);z=root_floor(n,200)
        if not(pow(z,200)<=n<pow(z+1,200)):raise ValueError('integer root enclosure')
        cache[r]=(F(z,S),F(z+1,S))
    return cache[r]

def combine(*terms):
    d=Counter()
    for a,p in terms:
        for r,c in p.items():d[r]+=F(a)*c
    return {r:c for r,c in d.items() if c}

def moment(p):
    lo=hi=F(0)
    for r,c in p.items():
        a,b=power(r)
        if c>=0:lo+=c*a;hi+=c*b
        else:lo+=c*b;hi+=c*a
    return lo,hi

def decimal(x):
    with localcontext() as c:
        c.prec=55
        return str(Decimal(x.numerator)/Decimal(x.denominator))

def record(pair):
    return {'lower_rational':str(pair[0]),'upper_rational':str(pair[1]),
            'lower_decimal':decimal(pair[0]),'upper_decimal':decimal(pair[1])}

def main(a):
    raw=a.native.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('source pin')
    native=json.loads(gzip.decompress(raw));frames=native['frames']
    N=Counter(abs(frames[str(op[2])]['dim']-frames[str(op[3])]['dim']) for op in native['program'] if op[0]=='MOVE')
    if N!=Counter({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}):raise ValueError('native movement profile')
    H={2:1,4:25,6:1,8:410}
    P2=combine((36,N),(444,{1:1}), (444,{7*j:1 for j in range(1,9)}))
    T2=combine((36,H),(222,{127:1}), (444,{1+7*j:1 for j in range(1,10)}))
    M2=combine((1,T2),(-1,P2));Binf=combine((1,N),(-1,H),(F(1,36),M2))
    cert=json.loads(a.certificate.read_text());X=Counter({7:8})
    for g in cert['groups']:
        size=len(g['indices']);X[size-1]+=size;X[8-size]+=size
    if X!=Counter({1:4,2:15,3:84,4:84,5:15,6:4,7:8}):raise ValueError('actual group capture profile')
    profiles={
        'literal_unit_q9':{1:1626},
        'coalesced_X_unit_Y_packet_q9':combine((1,X),(849,{1:1})),
        'ideal_capture_q9':combine((1,X),(111,{7:1}),(9,{8:1})),
        'ideal_capture_q10':combine((1,X),(111,{7:1}),(10,{8:1}))}
    screens={}
    for name,Q in profiles.items():
        limit=combine((1,Binf),(-1,Q));cases={};first=None
        for m in range(2,66,2):
            gap=moment(combine((1,limit),(F(1,36*(m-1)),M2)))
            if gap[0]>0 and first is None:first=m
            if m<=20 or m in(32,64):cases[str(m)]=record(gap)
        screens[name]={'profile':{str(r):str(c)for r,c in sorted(Q.items())},
                      'Q_moment':record(moment(Q)),'limiting_margin':record(moment(limit)),
                      'first_profitable_even_m_at_most64':first,'fixed_m_margins':cases}
    if screens['literal_unit_q9']['first_profitable_even_m_at_most64'] is not None:raise ValueError('literal unit word incorrectly admitted')
    if screens['coalesced_X_unit_Y_packet_q9']['first_profitable_even_m_at_most64']!=16:raise ValueError('first even multiplicity')
    pr=json.loads(a.receipt.read_text())
    if pr['prefix_receipt']['counts']!={'INIT':117,'ADD':496,'MOVE':680,'CLEAR':3}:raise ValueError('prefix invoice')
    if pr['closed_preconditioner_receipt']['counts']!={'INIT':117,'ADD':571,'MOVE':1578,'CLEAR':117}:raise ValueError('closed invoice')
    native_counts=Counter(op[0] for op in native['program'])
    out={'status':'PASS_EXACT_CONDITIONAL_POINT_PREFIX_BUDGET_NOT_A_DECODER',
         'native_sha256':PIN,'t':'199/200','integer_scale':str(S),
         'limiting_allowance':record(moment(Binf)),
         'finite_m_correction_numerator':record(moment(combine((F(1,36),M2)))),
         'original_X_capture_profile':dict(sorted(X.items())),
         'original_X_capture_moment':record(moment(X)),
         'conditional_profiles':screens,
         'ordinary_invoice':{'prefix_ADD':496,'prefix_INIT':117,'prefix_CLEAR':3,'prefix_live_owned':114,'prefix_peak_owned':115,
             'known_closing_restore_ADD':75,'closed_preconditioner_ADD':571,
             'prospective_q9_completed_Q_ADD':'571 + A_dec, unless decoder replaces rather than supplements the75 Hub restoration ADDs',
             'prospective_q9_completed_Q_INIT_CLEAR_each':'123 + L_dec; all114 retained caches must actually be retired',
             'shared_source_ADD':'30789 + (m-1)*(444 + A_Q)',
             'shared_source_owned_lifetimes':'237 + (m-1)*L_Q',
             'shared_source_sequential_peak':'max(237, peak(Q))',
             'native_actual_counts':dict(native_counts)},
         'premises':['All111 Y endpoints completed and all original X restored by an actual source word.',
             'Each proposed MOVE coalescing has no intervening read/write of that field and preserves nested monotonicity.',
             'Every extra decoder route, new owned lifetime, nonzero erasure and cocharted operation is paid.',
             'Fixed even multiplicity uses the retained caller and unchanged rank/target accounting.',
             'All-volume physical/compiler, cover/tail, strict supplier, ordinary BIT, complex supplier and foundational assumptions remain.'],
         'complete_source':False,'new_kappa':False}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'limiting_allowance':out['limiting_allowance']['lower_decimal'],
                     'first_even':{k:v['first_profitable_even_m_at_most64']for k,v in screens.items()},
                     'X_moment':out['original_X_capture_moment']['lower_decimal']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
