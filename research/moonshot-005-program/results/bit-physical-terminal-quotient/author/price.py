"""Rational enclosures from exact integer 200th roots at price 1/200."""
from collections import Counter
from functools import cache
from fractions import Fraction as F

@cache
def power(k):
    scale=10**14; target=(k**199)*(scale**200);lo=0;hi=k*scale+1
    while hi-lo>1:
        m=(hi+lo)//2
        if m**200<=target:lo=m
        else:hi=m
    return F(lo,scale),F(hi,scale)

def caps():
    native={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    helpers={2:1,4:25,6:1,8:410}
    base={1:F(4451,8),2:F(7213,16),4:24,8:9}
    result={}
    for label,m,offset in [('870',870,1),('limit',1,0)]:
        x=Counter({r:18*offset*n for r,n in helpers.items()})
        for r,n in native.items():x[r]-=18*offset*n
        x[1]-=222*m;x[127]+=111*m
        for j in range(1,9):x[7*j]-=222*m
        for j in range(1,10):x[1+7*j]+=222*m
        for r,n in base.items():x[r]-=18*(m-offset)*n
        low=sum(n*power(r)[n<0] for r,n in x.items())
        high=sum(n*power(r)[n>0] for r,n in x.items())
        ans=(3840*low/(18*(m-offset)*power(8)[1]),3840*high/(18*(m-offset)*power(8)[0]))
        result[label]=[str(v) for v in ans]
    return result

if __name__=='__main__':
    for k,v in caps().items():print(k,[float(F(w)) for w in v])
