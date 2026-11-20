#!/usr/bin/env python3
"""Independent directed-decimal review of the split/trim product powers at the m=870 tariff."""
import argparse,gzip,hashlib,json,subprocess
from collections import Counter
from decimal import Decimal as D, Context, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from functools import cache
from pathlib import Path

LOW=Context(prec=85,rounding=ROUND_FLOOR);HIGH=Context(prec=85,rounding=ROUND_CEILING)
NATIVE='research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
TARGET='research/moonshot-005-program/results/bit-two-sided-covariant-target/author/output/RESULT.json'
BASE='914097a04bb93f730b805e9d4f036b46707c8675'

def need(v,m):
    if not v:raise ValueError(m)

def file(repo,pin,path):
    local=repo/path
    data=local.read_bytes() if local.is_file() else subprocess.check_output(['git','-C',str(repo),'show',BASE+':'+path])
    need(hashlib.sha256(data).hexdigest()==pin,'original physical source pin');return data

def product(a,b):return min(LOW.multiply(x,y)for x in a for y in b),max(HIGH.multiply(x,y)for x in a for y in b)
def exact(x):return D(x),D(x)
def quotient(a,b):return LOW.divide(a[0],b[1]),HIGH.divide(a[1],b[0])

@cache
def power(r,x):
    # Python Decimal's ln and exp are correctly rounded to nearest. Expanding
    # each by one adjacent representable number brackets its exact real value.
    l=LOW.ln(D(r));L=(LOW.next_minus(l),HIGH.next_plus(l));z=product(L,exact(x));u=LOW.exp(z[0]);v=HIGH.exp(z[1]);return LOW.next_minus(u),HIGH.next_plus(v)

def moment(hist,x):
    lo=hi=D(0)
    for r,count in sorted(hist.items(),reverse=True):
        a,b=product(exact(count),power(r,x));lo=LOW.add(lo,a);hi=HIGH.add(hi,b)
    return lo,hi

def build(repo):
    native=json.loads(gzip.decompress(file(repo,'51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78',NATIVE)))
    target=json.loads(file(repo,'4151df493670c7912ef613e8d6de490bcb2af9b1f95d9dc065e05594da2ef4c1',TARGET))
    need((target['bank'],target['retained_repair_rank'],target['return_rank'])==(3840,128,34688),'actual target bank')
    dims=lambda j:native['frames'][str(j)]['dim'];m=870;lanes=23040;P=Counter();T=Counter()
    for step in native['program']:
        if step[0]=='MOVE':P[abs(dims(step[2])-dims(step[3]))]+=18*lanes
    for i in range(222,659):T[dims(native['final'][i])-dims(native['start'][i])]+=18*lanes
    P[1]+=222*m*lanes;T[127]+=111*m*lanes
    for j in range(1,9):P[7*j]+=222*m*lanes
    for j in range(1,10):T[1+7*j]+=222*m*lanes
    for r,physical in ((1,4451*lanes//8),(2,7213*lanes//16),(4,24*lanes),(8,6*34688)):
        P[r]+=18*(m-1)*physical
    need((sum(P.values()),sum(r*z for r,z in P.items()),sum(T.values()))==(416127105216,1714004886528,42455715840),'integer lane profile')
    return P,T

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();P,T=build(a.repo);k=D('.0050000005');t=D(1)-k;total=moment(T,t);out={}
    for name,v,c,b,u,w,th,poly,H in [('short',88,31,32,D('.57'),D('1.02'),Q(109,110),234,109130000000000),('low_log',194,24,38,D('.34'),D('.66'),Q(7,8),36,15790000000000)]:
        ratio=[quotient(moment(P,t),total),quotient(moment(P,t+u),product(power(c,u),total)),quotient(product(power(b,w),moment(T,t-w)),total)]
        upper=[]
        for a0,b0 in ratio:
            lower=Q(a0)*10**15;higher=Q(b0)*10**15;need(lower.__ceil__()==higher.__ceil__(),'15-digit ceiling');upper.append(Q(higher.__ceil__(),10**15))
        a0,g,l=upper
        bill=lambda d:Q(1,1+d*(1-a0))+2*g**d+l**d
        direct=lambda d:a0**d+2*g**d+l**d
        need(bill(v)<1<=bill(v-1),'first power for stated rational bound')
        need(direct(v)<1<=direct(v-1),'direct exponential budget at both neighboring powers')
        num,den=th.numerator,th.denominator
        need(c**den<b**num and 2*c**(v*den)<=127**(v*num),'separation/ambient shrink')
        scale=power(127,k*v);need(th**poly<Q(t)/Q(scale[1]) and Q(scale[1])<2**poly,'polylog majorant')
        need(th**(poly-1)>=Q(t)/Q(scale[0]) or Q(scale[0])>=2**(poly-1),'preceding log power fails')
        unit=10**10;need(H%unit==0 and (H+1)**poly<2**(H//unit) and (H-unit+1)**poly>=2**(H//unit-1),'integer threshold grid')
        out[name]={'v':v,'v_minus_one_passes':False,'toleranced_15_digit_upper_ratios':[str(x)for x in upper],
                   'literal_direct_normalized_gap_lower':float(1-direct(v)),'literal_direct_previous_excess':float(direct(v-1)-1),
                   'bernoulli_gap_lower':float(1-bill(v)),'logarithm_power':poly,'threshold_log2':H}
    a.out.mkdir(exist_ok=True,parents=True);receipt={'integer_paid':P,'integer_target':T,'witnesses':out,'raw_saving':'0.0050000005','uniform_saving':'0.0050000004','ordinary_conditional_saving':'0.0050000002'};(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(out)
if __name__=='__main__':main()
