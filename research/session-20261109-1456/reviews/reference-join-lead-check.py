"""Independent small rational audit of the reference/ideal join; not a native replay.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from fractions import Fraction as F
from itertools import product
import json

def need(x, message):
    if not x: raise ValueError(message)
def ceil_log(x):
    k=0
    while F(2)**k<x:k+=1
    while F(2)**(k-1)>=x:k-=1
    return k
def inverse2(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]
def augment(a):return [list(row)+[F(0)] for row in a]+[[F(0),F(0),F(1)]]
def tensor(a,b):return [[x*y for x in rowa for y in rowb] for rowa in a for rowb in b]
def norm(a):return max(sum(map(abs,row)) for row in a)
def scaled(a,s):return [[x*s for x in row] for row in a]
def diff(a,b):return [[x-y for x,y in zip(ra,rb)] for ra,rb in zip(a,b)]
def left_diag(a):return [[x*[F(1),F(3,2),F(1)][i] for x in row] for i,row in enumerate(a)]
axes=[]
for a,b in product(range(1,5),range(1,4)):
    u,v=F(1,2**a),F(1,2**(a+b));e=v/16
    n=[[F(1),u],[v,F(1)]];h=[[F(1),u-e],[v+e,F(1)]]
    delta=1-u-e;ni=inverse2(n);hi=inverse2(h)
    need(norm(diff(h,n))==e,'exact perturbation')
    need(norm(ni)<=1/(delta+e) and norm(hi)<=1/delta,'inverse bounds')
    need(norm(diff(hi,ni))<=e/(delta*(delta+e)),'resolvent')
    axes.append((left_diag(augment(hi)),left_diag(augment(ni)),delta,e,ceil_log(1/delta)))
count=0
for x,y in product(axes,repeat=2):
    U=x[4]+y[4];V=2;K=2*U+V+8
    h=scaled(tensor(x[0],y[0]),F(2)**(-K));n=scaled(tensor(x[1],y[1]),F(2)**(-K))
    mu=F(2)**(V-K)/(x[2]*y[2]);c=F(2)**(U+V-K)
    xi=mu*(x[3]/(x[2]+x[3])+y[3]/(y[2]+y[3]))
    need(norm(h)<=mu<=c<=1 and norm(n)<=mu,'complete augmented group contraction')
    need(norm(diff(h,n))<=xi,'complete tensor defect')
    need(mu*2*F(2)**U<=F(2)**42,'normalizer slack gate')
    count+=1
budgets=0
for p,R0,g,z,W in product([2,3,73],[1,2,10],[1,2,7],[3,10,60],[0,3]):
    delta=F(1,8*p*p);u=ceil_log(1/delta);l=ceil_log(F(p));U=g*u;V=g*(2*l+8);K=g*100*l
    mu=F(2)**(V-K)/delta**g;c=F(2)**(U+V-K);eta=F(2)**(-z)
    t=max(1,z+2-U);s=z+2;Ri=2*R0;Q=2**21*p
    E=s+ceil_log(F(8*(Ri+1)*Q*Q));epsilon=F(2)**(-E)
    xi=mu*g*epsilon/(delta+epsilon)
    L=g*F((2*W+1)*2*R0+2)/delta;q=z+ceil_log(max(F(8),2*L));eA=(3*R0+2)*F(2)**(-q)
    need(R0*epsilon<=F(2)**(-s-46)/(p*p),'source radius cancellation')
    need(R0*xi<=mu*g*F(2)**(-t-42),'reference target allocation')
    need(eA<=F(3,4)*eta and c*eta+eA+R0*xi<=2*eta,'same original output budget')
    budgets+=1
p=3;R0=2**60;Ri=1;s=5;Q=2**21*p;E=s+ceil_log(F(8*(Ri+1)*Q*Q))
need(R0*F(2)**(-E)>F(2)**(-s-46)/(p*p),'underdeclared source radius must fail cancellation')
print(json.dumps(dict(status='PASS_INDEPENDENT_RATIONAL_JOIN',two_axis_with_holes_cases=count,exact_budget_cases=budgets,controls=['underdeclared source radius violates cancellation'],scope='Finite rational audit plus lead proof review, not source-native replay or universal proof by testing'),sort_keys=True))
