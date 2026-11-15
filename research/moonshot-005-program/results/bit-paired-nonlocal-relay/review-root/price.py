#!/usr/bin/env python3
"""Independent exact root enclosures for the independently replayed profile."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
S=1<<180
def root(n):
    a,b=0,1<<((n.bit_length()+199)//200)
    while b-a>1:
        c=(a+b)//2
        if c**200<=n:a=c
        else:b=c
    return a
bounds={r:(F(root(r**199*S**200),S),F(root(r**199*S**200)+1,S))for r in range(1,128)}
def linear(profile):
    a=b=F(0)
    for r,c in profile.items():
        lo,hi=bounds[r]
        a+=c*(lo if c>=0 else hi);b+=c*(hi if c>=0 else lo)
    return a,b
def combine(*terms):
    z={}
    for p,c in terms:
        for r,v in p.items():z[r]=z.get(r,F(0))+c*v
    return{k:v for k,v in z.items()if v}
def encode(pair):
    out={'lower':str(pair[0]),'upper':str(pair[1])}
    for key,x,mode in [('decimal_lower',pair[0],ROUND_FLOOR),('decimal_upper',pair[1],ROUND_CEILING)]:
        with localcontext()as c:c.prec=60;c.rounding=mode;out[key]=str(Decimal(x.numerator)/Decimal(x.denominator))
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--review',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    review=json.loads(a.review.read_text());author=json.loads(a.author.read_text())['price']
    Q={int(r):v for r,v in review['CLOSED-WORD']['profile'].items()};assert Q=={1:159,2:26,3:128,4:70,5:2,7:105}
    paired={1:149,2:26,3:127,4:67,7:110};delta={1:10,3:1,4:3,5:2,7:-5}
    assert combine((paired,1),(delta,1))==Q
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    P2=combine((N,36),({1:444},1),({7*j:444 for j in range(1,9)},1))
    T2=combine((H,36),({127:222},1),({1+7*j:444 for j in range(1,10)},1))
    cap=combine((N,1),(H,-1),(T2,F(1,36)),(P2,F(-1,36)))
    quantities={'Q':linear(Q),'limiting_cap':linear(cap),'room':linear(combine((cap,1),(Q,-1))),
                'm2_margin':linear(combine((T2,1),(P2,-1),(N,18),(H,-18),(Q,-18)))}
    for n,(lo,hi) in quantities.items():
        assert lo<=F(author[n]['upper'])and F(author[n]['lower'])<=hi,(n,'nonoverlapping enclosure')
    assert quantities['room'][0]>0 and quantities['m2_margin'][0]>0
    # Omitting the actual nonlocal Y split would underprice a positive expense.
    ysplit=linear({4:1,3:1,7:-1});assert ysplit[0]>0
    out={'status':'PASS_INDEPENDENT_NONLOCAL_RELAY_INVOICE','exact_method':'integer200th roots at binary scale2^180','quantities':{n:encode(v)for n,v in quantities.items()},'profile_delta':delta,'unpriced_Y59_split_negative_control':encode(ysplit),'scope':'Actual source movement only; complete decoder and strict supplier not inferred.','new_complete_kappa':False}
    a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'Q':out['quantities']['Q']['decimal_lower'],'room':out['quantities']['room']['decimal_lower']}))
if __name__=='__main__':main()
