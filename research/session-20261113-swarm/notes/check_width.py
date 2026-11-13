from fractions import Fraction as Q
from itertools import product
import json

Z=(Q(0),Q(0))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,n):return(a[0]*n,a[1]*n)
def c_axis(x,axis,inverse=False):
    out=list(x);u=(Q(1,2),Q(-1 if inverse else 1,2));v=(Q(1,2),Q(1 if inverse else -1,2));bit=1<<axis
    for i in range(len(x)):
        if not(i&bit):
            a,b=x[i],x[i|bit];out[i]=add(mul(u,a),mul(v,b));out[i|bit]=add(mul(v,a),mul(u,b))
    return out
def partial(x,axes,inverse=False):
    for a in axes:x=c_axis(x,a,inverse)
    return x
def norm(x):return max(abs(c) for v in x for c in v)
def integral(x):return all(c.denominator==1 for v in x for c in v)
def require(v,msg):
    if not v:raise AssertionError(msg)
counts={'sharp_cuts':0,'prefix_bound_checks':0,'scale_checks':0,'negative_controls':0}
for f in range(1,11):
    for j in range(f+1):
        d=min(j,f-j);active=list(range(d))+list(range(j,j+d));mask=sum(1<<a for a in active)
        z=[(Q(1<<((d+1)//2)) if i&mask==0 else Q(0),Q(0)) for i in range(1<<f)]
        x=partial(z,list(range(j)),True);y=partial(x,list(range(f)))
        require(integral(x) and integral(y),'witness endpoint integrality')
        require(norm(x)==norm(y)==1,'witness endpoint sizes')
        require(partial(x,list(range(j)))==z,'witness prefix')
        require(norm(z)==1<<((d+1)//2),'sharp norm factor')
        counts['sharp_cuts']+=1
        k=(f+2)//4;scaled=[scale(a,1<<k) for a in x]
        for a in range(f+1):
            prefix=partial(scaled,list(range(a)))
            require(integral(prefix),'endpoint scale clears')
            require(norm(prefix)<=(1<<(k+(min(a,f-a)+1)//2)),'endpoint range bound')
            counts['prefix_bound_checks']+=1
        if j==f//2:
            require(norm(partial(scaled,list(range(j))))==1<<(2*k),'global sharp range')
            if k:
                require(norm(partial(scaled,list(range(j))))>(1<<(2*k))-1,'one fewer signed bit fails')
                counts['negative_controls']+=1
# Paired-coordinate sharp denominator inputs from credited PR7468.
for f in range(2,11):
    j=f//2;d=j;k=(f+2)//4
    x=[(Q(int(all(((i>>a)&1)==((i>>(j+a))&1) for a in range(d)))),Q(0)) for i in range(1<<f)]
    y=partial(x,list(range(f)));require(integral(y),'paired endpoint')
    for j0 in range(f+1):
        z=partial([scale(v,1<<k) for v in x],list(range(j0)));require(integral(z),'all scaled prefixes');counts['scale_checks']+=1
    too_small=partial([scale(v,1<<(k-1)) for v in x],list(range(j)))
    require(not integral(too_small),'insufficient binary scale detected');counts['negative_controls']+=1
# One-endpoint range premise is insufficient for a middle-cut bound.
z=[(Q(4),Q(0))]+[Z]*15
x=partial(z,[0,1,2],True);p=partial(x,[0,1,2]);y=partial(x,[0,1,2,3])
require(integral(x) and integral(y) and norm(x)==1 and norm(y)==2 and norm(p)>2,'missing final norm failure');counts['negative_controls']+=1
print(json.dumps({'status':'PASS_ENDPOINT_COMPONENT_WIDTH_CANDIDATE','scope':'finite corroboration, mathematical proof separate','counts':counts},sort_keys=True))
