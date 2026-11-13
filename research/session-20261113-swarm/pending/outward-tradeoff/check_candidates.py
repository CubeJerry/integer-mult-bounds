"""Separate direct certificate checks; no matching/search code is imported."""
from itertools import product
from math import isqrt
from pathlib import Path
import json

P=Path(__file__).resolve().parent


def need(ok,why):
    if not ok:
        raise ValueError(why)


def n2(x):
    return sum(z*z for z in x)


def hx(x):
    a,b,c,d=x
    return (a+b+c+d,a-b+c-d,a+b-c-d,a-b-c+d)


def interval(n):
    scale=1<<128
    a=isqrt(n*scale*scale)
    return a,a+int(a*a!=n*scale*scale)


def growth(a,b,strict=False):
    if a<=b:
        return True
    if (a,b)==(21,19):
        return not strict
    al,au=interval(a);bl,bu=interval(b)
    pl,pu=interval(21);ql,qu=interval(19)
    if au-bl<pl-qu:
        return True
    if al-bu>pu-ql:
        return False
    raise ValueError('unseparated radical comparison')


def ball(radius):
    pairs={}
    for a,b in product(range(-radius,radius+1),repeat=2):
        pairs.setdefault(a*a+b*b,[]).append((a,b))
    return {x+y for r,xx in pairs.items() for s,yy in pairs.items() if r+s<=radius*radius for x in xx for y in yy}


def targets(x):
    z=hx(x)
    choices=[[(a+k)//2 for k in range(-2,3) if (a+k)%2==0] for a in z]
    return {y for y in product(*choices) if n2(y)+n2(x)-sum(a*b for a,b in zip(z,y))<=1}


def main():
    x=json.loads((P/'R5-OPTIMUM.json').read_text())
    rows=[(tuple(a),tuple(b)) for a,b in x['matching']]
    domain=ball(5)
    need(len(rows)==len(domain)==3121,'complete radius-five cardinality')
    need({a for a,b in rows}==domain and len({b for a,b in rows})==len(rows),'complete finite injection')
    attaining=0
    for a,b in rows:
        z=hx(a)
        need(n2(b)+n2(a)-sum(u*v for u,v in zip(z,b))<=1,'dot-product exact error')
        need(growth(n2(b),n2(a)),'upper threshold')
        attaining+=(n2(b),n2(a))==(21,19)
    need(attaining>0,'actual attained finite optimum candidate')
    hs={tuple(a) for a in x['hall']['input_set']}
    expected={tuple(a) for a in x['hall']['output_neighbors']}
    need(hs<=domain and len(hs)==len(x['hall']['input_set']),'Hall inputs unique and in domain')
    actual=set()
    for a in hs:
        actual.update(b for b in targets(a) if growth(n2(b),n2(a),True))
    need(actual==expected,'complete strict-threshold neighbor census')
    need(len(actual)<len(hs),'strict Hall deficit')
    y=json.loads((P/'R3.json').read_text())
    small=[(tuple(a),tuple(b)) for a,b in y['matching']]
    need({a for a,b in small}==ball(3) and len({b for a,b in small})==425,'radius-three injection')
    for a,b in small:
        need(n2(b)<=n2(a) or (n2(b),n2(a))==(10,9),'radius-three exact growth bound')
        need(n2(b)+n2(a)-sum(u*v for u,v in zip(hx(a),b))<=1,'radius-three exact error')
    print(json.dumps({'marker':'PASS_DIRECT_FINITE_OUTWARD_CERTIFICATES',
                      'radius5_inputs':len(domain),'attaining_edges':attaining,
                      'radius5_optimum':'sqrt(21)-sqrt(19)',
                      'strict_Hall_inputs':len(hs),'strict_Hall_neighbors':len(actual),
                      'radius3_inputs':425,'radius3_optimum':'sqrt(10)-3',
                      'scope':'finite injection optima only; radius-five lower bound also necessary for any global bijection with error<=1'},indent=2))


if __name__=='__main__':
    main()
