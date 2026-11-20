#!/usr/bin/env python3
"""Independent directed log/exp review; imports no author price implementation."""
import argparse
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from collections import Counter
import gzip,json,hashlib
Q=10**85

def require(x,s):
    if not x: raise ValueError(s)
def floor(x): return x.numerator//x.denominator
def ceil(x): return -((-x.numerator)//x.denominator)
@lru_cache(None)
def log_bounds(n):
    e=n.bit_length()-1
    u=F(n,2**e)
    def unit(a):
        z=(a-1)/(a+1);p=z;s=F(0)
        for k in range(100):
            s+=2*p/(2*k+1);p*=z*z
        return s,s+2*p/(201*(1-z*z))
    l2,u2=unit(F(2));l,u=unit(u)
    return floor((e*l2+l)*Q),ceil((e*u2+u)*Q)
@lru_cache(None)
def power(n,k):
    """Enclose n**(1-k) by log series followed by alternating exp."""
    if not k:return F(n),F(n)
    l,u=log_bounds(n);a=floor(k*l);b=ceil(k*u)
    require(0<=a<=b<Q,'alternating-series range')
    sl=su=Q;tl=tu=Q
    for j in range(1,101):
        tl=tl*a//(Q*j);tu=-(-tu*b//(Q*j))
        if j%2:sl-=tu;su-=tl
        else:sl+=tl;su+=tu
    remainder=-(-tu*b//(101*Q))
    return F(n*(sl-remainder),Q),F(n*su,Q)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(c,x):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])
def moment(h,k):
    r=(F(0),F(0))
    for n,c in h.items():r=add(r,mul(c,power(int(n),k)))
    return r
def hist(*rows):
    z=Counter()
    for m,h in rows:
        for r,c in h.items():z[int(r)]+=m*F(c)
    return z
def show(z):return [str(float(x)) for x in z]
def sign(z):
    require(z[0]>0 or z[1]<0,'strict sign');return 1 if z[0]>0 else -1
def wrapper(a):
    z=Counter({14*a+1:2,1:-4})
    for j in range(1,a+1):z[7*j+1]+=4
    for j in range(1,a):z[7*j]-=4
    return z

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    package=Path(__file__).resolve().parents[1];base=package.parent
    pins=json.loads((package/'SOURCES.json').read_text())['files']
    for path,h in pins.items():require(hashlib.sha256((base/path).read_bytes()).hexdigest()==h,'input pin')
    z=json.load(open(base/'bit-covariant-rebalanced-cutoffs/grade14/sources/BIT.json'))['native']
    delta=hist((1,z['native_targets']),(-1,z['native_paid']))
    B=hist((36,delta),(111,wrapper(9)))
    require(B==hist((1,z['targets']),(-1,z['paid'])),'complete binary invoice')
    signs=[]
    for s in ['.003879928046154','.003879928046155']:
        signs.append(sign(moment(B,F(s))))
    require(signs==[1,-1],'binary crossing')
    ku=F('.003879928046155')
    arm_signs=[sign(moment(hist((a,wrapper(a+1)),(-a-1,wrapper(a))),ku)) for a in (8,9)]
    require(arm_signs==[1,-1],'all-arm concavity endpoint')
    trials={}
    for s,a in [('.004',9),('.0043',8),('.0045',8),('.005',7)]:
        k=F(s);g=moment(hist((4*a,delta),(111,wrapper(a))),k)
        require(sign(g)==-1,'source deficit')
        require(sign(moment(hist((a-1,wrapper(a)),(-a,wrapper(a-1))),k))==1,'preceding arm')
        require(sign(moment(hist((a,wrapper(a+1)),(-a-1,wrapper(a))),k))==-1,'following arm')
        trials[s]=show(mul(F(-1,4*a),g))
    app=json.loads(gzip.decompress((base/'complex-native-contested-restoration/author/sources/DOUBLE-APPLICATION.json.gz').read_bytes()))['application']['invoice']
    C=hist((1,app['targets']),(-1,app['paid']))
    require([sign(moment(C,F(s))) for s in ['.00388013644474','.00388013644475']]==[1,-1],'complex crossing')
    derivative_upper=F(0)
    for r,n in C.items():
        l,u=log_bounds(r)
        if n>0: derivative_upper-=n*power(r,F(1,32))[0]*F(l,Q)
        else: derivative_upper-=n*r*F(u,Q)
    require(derivative_upper < -790000,'whole-range complex derivative')
    OldN={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};OldH={2:1,4:25,6:1,8:410}
    Og=hist((36,OldH),(-36,OldN),(111,wrapper(9)))
    L=hist((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}))
    for j in range(1,9):L[7*j+1]+=F(37,3);L[7*j]-=F(37,3)
    Q0={1:F(4451,8),2:F(7213,16),4:F(24)}
    def gap(k,q,m=None):
        h=hist((1,L),(-1,Q0),(-q,{8:1}))
        if m is not None:h=hist((1,h),(F(1,36*(m-1)),Og))
        return moment(h,k)
    caps={}
    for s,q,m in [('.0043',36875,870),('.005',34688,870)]:
        require(sign(gap(F(s),F(q,3840),m))==1,'integer cap passes')
        require(sign(gap(F(s),F(q+1,3840),m))==-1,'next integer fails')
        caps[s]=q
    require(sign(gap(F('.0043'),F(9),2))==-1,'ideal floor fails at two copies')
    receipt=json.load(open(package/'RESULT.json'))
    for name,ratio in [('any_missing_direction',F(29,3)),('regular_missing_direction_continuum',F(68,7)),('regular_missing_direction_bank3840',F(37303,3840)),('ideal_nine_bank',F(9))]:
        for label,m in [('infinite_m',None),('m2',2),('m870',870)]:
            lo,hi=receipt['balanced_source_return_gates']['missing_direction_kappa_ceilings'][name][label]
            require(sign(gap(F(lo),ratio,m))==1 and sign(gap(F(hi),ratio,m))==-1,'independent threshold '+name+'/'+label)
    require(gap(F(0),F(629,48))==(0,0),'limiting zero-saving price')
    require(gap(F(0),F(55,3),2)==(0,0),'finite zero-saving credit')
    require(sign(gap(F('.0043'),F(29,3)))==-1,'missing donor fails significant target')
    # Positive changed-source control cannot be confused with a cutoff change.
    g=moment(hist((32,delta),(111,wrapper(8))),F('.0043'))
    require(g[0]+160>0,'five-unit actual-profile change would matter')
    args.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_INDEPENDENT_LOG_EXP_PRICE_REVIEW','powers':'rational logarithm enclosure and fixed-grid alternating exponential; no author power imports','binary_endpoint_signs':signs,'all_arm_neighbor_signs':arm_signs,'per_native_required_gains_diagnostic':trials,'strict_integer_return_caps':caps,'reviewed_thresholds':12,'new_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
