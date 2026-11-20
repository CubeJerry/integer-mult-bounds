"""Reprice the m=870 profile using rational enclosures independent of the upstream tail tool."""
import argparse
from fractions import Fraction as Q
from functools import cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

GRID=10**38
def bound(x,y):
    return Q((x*GRID).__floor__(),GRID),Q((y*GRID).__ceil__(),GRID)

def mult(a,b):
    products=[x*y for x in a for y in b]
    return bound(min(products),max(products))

def div(a,b):
    assert b[0]>0
    return mult(a,(1/b[1],1/b[0]))

def inverse_exp_small(x):
    assert 0<=x<=1
    total=term=Q(1)
    for i in range(1,32):
        term=term*x/i
        total+=term
    nextterm=term*x/32
    return bound(total,total+nextterm/(1-x/33))

def exp_at(x):
    if x<0:
        low,high=exp_at(-x)
        return bound(1/high,1/low)
    count=0
    while x>Q(1,8):
        x/=2
        count+=1
    result=inverse_exp_small(x)
    for _ in range(count):result=mult(result,result)
    return result

def check(repo):
    comp=repo/'research/moonshot-005-program/results/bit-covariant-single-grade-budget/author/check.py'
    spec=importlib.util.spec_from_file_location('native_profile',comp)
    native=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    paid,target=native.histograms(native.ordered_profiles(repo),870)
    def counts(hist):
        q={r:Q(n)*23040 for r,n in hist.items()}
        assert all(n.denominator==1 and n>0 for n in q.values())
        return {r:int(n) for r,n in q.items()}
    P,T=counts(paid),counts(target);k=Q('0.0050000005');t=1-k
    @cache
    def power(r,exp):
        u,v=sorted(x*exp for x in native.log_int(r))
        return exp_at(u)[0],exp_at(v)[1]
    def moment(H,s):
        terms=[(n,power(r,s)) for r,n in H.items()]
        return bound(sum(n*a for n,(a,b) in terms),sum(n*b for n,(a,b) in terms))
    def ceil15(x):
        return Q((x*10**15).__ceil__(),10**15)
    source=json.loads((Path(__file__).parent/'output/CREDITED.json').read_bytes())
    result={}
    for name,v,c,b,u,w in [('short',88,31,32,Q(57,100),Q(102,100)),('low_log',194,24,38,Q(34,100),Q(66,100))]:
        S=source[name]['separation'];U=source[name]['uniform']
        assert set(P)==set(map(int,S['paid'])) and all(P[r]==S['paid'][str(r)] for r in P)
        assert set(T)==set(map(int,S['targets'])) and all(T[r]==S['targets'][str(r)] for r in T)
        assert min(P)>=1 and max(P)<max(T)==127 and 1<c<b<127 and u>=k and w>0
        mass=moment(T,t)
        ratios=[div(moment(P,t),mass),div(moment(P,t+u),mult(power(c,u),mass)),div(mult(power(b,w),moment(T,t-w)),mass)]
        upper=list(map(Q,S['rational_upper_limits']))
        assert all(ceil15(lo)==ceil15(hi)==z<1 for (lo,hi),z in zip(ratios,upper))
        alpha,gamma,lam=upper
        def budget(length):
            return 1/(1+length*(1-alpha))+2*gamma**length+lam**length
        assert budget(v)<1<=budget(v-1)
        theta=Q(U['theta']);p=U['logarithm_power'];H=U['H'];d=theta.denominator
        assert c**d<b**theta.numerator and 2*c**(d*v)<=127**(v*theta.numerator)
        scale=power(127,v*k)
        assert theta**p<t/scale[1] and scale[1]<2**p
        assert theta**(p-1)>=t/scale[0] or scale[0]>=2**(p-1)
        unit=10**10
        assert H%unit==0 and (H+1)**p < 2**(H//unit)
        assert (H-unit+1)**p >= 2**(H//unit-1)
        result[name]={'product_copies':v,'paid_base':c,'retained_base':b,'logarithmic_power':p,
            'uniform_saving':str(k-1/Q(unit)),'log2_carrier':H,
            'lower_gap_in_billionths':((1-budget(v))*10**9).__floor__(),
            'lower_gap_in_trillionths':((1-budget(v))*10**12).__floor__(),
            'previous_copy_count_fails_this_bound':True,'upper_ratios':list(map(str,upper))}
    # The numeric schedule printed for the other source words cannot simply be imposed at this target.
    foreign=div(moment(P,t+Q(11,50)),mult(power(10,Q(11,50)),moment(T,t)))
    assert foreign[0]>1
    result['original_7831_paid_tilt_fails_on_this_profile']=True
    result['physical_source_status']='conditional on the original full-word and supplier contracts'
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    v=check(a.repo)
    a.out.mkdir(exist_ok=True,parents=True)
    (a.out/'RESULT.json').write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
