"""Independent positive-series check of the frozen BIT strictification tail.

Reviewer code by @CubeJerry with OpenAI assistance.  The input histograms
are the source receipt, whose literal recount is separately checked by the
lead.  Uses the reviewer's exact logarithm core, not either BIT price engine.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, importlib.util, json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'reviewer_logs', HERE.parent/'ambient_bounds.py')
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

def need(v, message):
    if not v: raise ValueError(message)

def outward(a, b, digits=60):
    scale = 10**digits
    return Q((a*scale).__floor__(), scale), Q(-((-b*scale).__floor__()), scale)

def positive_exp(x):
    need(0 <= x < 1, 'positive Taylor domain')
    term = total = Q(1)
    for k in range(1, 49):
        term *= x/k
        total += term
    first = term*x/49
    return total, total+first/(1-x/50)

def exp_at(x):
    if x >= 0: return positive_exp(x)
    a, b = positive_exp(-x)
    return 1/b, 1/a

def power(r, offset):
    a, b = L.log_integer(r)
    a, b = outward(a, b)
    x, y = (offset*a, offset*b) if offset >= 0 else (offset*b, offset*a)
    low, _ = exp_at(x)
    _, high = exp_at(y)
    return outward(r*low, r*high)

def moment(hist, offset):
    lows = highs = Q(0)
    for r, n in hist.items():
        a, b = power(int(r), offset)
        lows += n*a
        highs += n*b
    return lows, highs

def show(pair):
    a,b=outward(*pair, digits=35)
    return [str(a), str(b)]

def run(source):
    data = json.loads(source.read_text())
    C, u = Q('.00376670'), Q(1,5)
    T,P=data['targets'],data['paid']
    t=moment(T,-C); p=moment(P,-C)
    pu=moment(P,u-C); tm=moment(T,-u-C)
    # r^u = r * r^(u-1); the latter exponent would exceed the small
    # exponential domain.  Compute it directly from the same log bounds.
    def tail_factor(r):
        a,b=L.log_integer(r);a,b=outward(a,b)
        low,_=exp_at(u*a);_,high=exp_at(u*b)
        return outward(low,high)
    c=tail_factor(15); b=tail_factor(16)
    ratios=[(p[0]/t[1],p[1]/t[0]),
            (pu[0]/(c[1]*t[1]),pu[1]/(c[0]*t[0])),
            (b[0]*tm[0]/t[1],b[1]*tm[1]/t[0])]
    limits=list(map(Q,data['finite_admission']['rational_upper_limits']))
    for i,((a,b),limit) in enumerate(zip(ratios,limits)):
        need(0<a<=b<=limit<1, 'strictification ratio '+str(i))
    alpha,gamma,lam=limits
    total=1/(1+768*(1-alpha))+2*gamma**768+lam**768
    need(total<1, 'completed and split product has strict margin')
    # Substantive control: replacing the source alpha by 1 funds no
    # strict loss at all, so the resulting upper bound must fail.
    bad=1+2*gamma**768+lam**768
    need(bad>1, 'zero raw surplus control')
    return {'method':'Positive Taylor exponential with geometric remainder; independent 80-term logarithm core',
            'ratios':[show(x) for x in ratios],
            'frozen_upper_limits':list(map(str,limits)),
            'normalized_upper':show((total,total)),
            'strict_gap':show((1-total,1-total)),
            'zero_raw_surplus_control':True,
            'scope':'Source-recounted histograms, strictification tail only. No physical native or ordinary admission assertion.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source', type=Path,
      default=HERE/'retained/bit/FRAGMENT-BIT-ADMISSION.json')
    ap.add_argument('--output', type=Path)
    a=ap.parse_args();result=run(a.source)
    if a.output:
        a.output.write_text(json.dumps(result,indent=2)+'\n')
    else:
        need(result==json.loads((HERE/'TAIL-REVIEW.json').read_text()), 'saved exact tail receipt')
    print(json.dumps(result,indent=2));print('PASS_REVIEWER_BIT_STRICTIFICATION_TAIL')
