"""Independent rational fixed-point log/exp bounds; standard library only."""
from fractions import Fraction as F
from functools import lru_cache
S=10**60
def need(ok,msg):
    if not ok:raise ValueError(msg)
def ceil(a,b=1):return -((-a)//b)
def exact(x):
    x=F(x);return x.numerator*S//x.denominator,ceil(x.numerator*S,x.denominator)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[1],a[1]-b[0]
def mul(a,b):
    v=[a[i]*b[j] for i in (0,1) for j in (0,1)]
    return min(v)//S,ceil(max(v),S)
def scale(a,x):return mul(a,exact(x))
def div(a,b):
    need(a[0]>=0 and b[0]>0,'positive division')
    return a[0]*S//b[1],ceil(a[1]*S,b[0])
def series_log(y):
    need(0<=y<=F(1,3),'log range')
    lo=hi=0;p=y
    for j in range(100):
        q=2*p/F(2*j+1);lo+=q.numerator*S//q.denominator;hi+=ceil(q.numerator*S,q.denominator);p*=y*y
    tail=2*p/(201*(1-y*y))
    return lo,hi+ceil(tail.numerator*S,tail.denominator)
@lru_cache(None)
def log(n):
    need(type(n) is int and n>0,'positive integer log')
    k=n.bit_length()-1;r=series_log(F(n-2**k,n+2**k));l2=series_log(F(1,3))
    return r[0]+k*l2[0],r[1]+k*l2[1]
def exp(a):
    need(0<=a[0]<=a[1]<=8*S,'exp range')
    lo=hi=S;total=(S,S)
    for j in range(1,101):
        lo=lo*a[0]//(S*j);hi=ceil(hi*a[1],S*j);total=add(total,(lo,hi))
    nxt=ceil(hi*a[1],S*101);tail=ceil(nxt*S*102,S*102-a[1])
    return total[0],total[1]+tail
@lru_cache(None)
def power(r,q):return exp(scale(log(r),q))
def moment(hist,q):
    a=(0,0)
    for r,n in hist.items():a=add(a,scale(power(r,q),n))
    return a
def report(a):return {'lower':str(F(a[0],S)),'upper':str(F(a[1],S)),'midpoint':float(F(sum(a),2*S))}
