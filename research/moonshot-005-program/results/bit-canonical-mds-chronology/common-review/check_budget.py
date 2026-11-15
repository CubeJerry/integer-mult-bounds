#!/usr/bin/env python3
"""Independent decimal-denominator intervals for the complete partial invoice."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import argparse
import hashlib
import json

S=10**40
def root(n):
    lo=0;hi=1<<((n.bit_length()+199)//200)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=n:lo=mid
        else:hi=mid
    assert lo**200<=n<hi**200
    return lo

P={r:(F(root(r**199*S**200),S),F(root(r**199*S**200)+1,S)) for r in range(1,128)}
def scale(c,x):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])
def add(*xs):return tuple(sum(x[k] for x in xs) for k in (0,1))
def lin(d):return add(*[scale(F(c),P[r]) for r,c in d.items()])
def record(x):
    with localcontext() as c:
        c.prec=60
        return {'lower_fraction':str(x[0]),'upper_fraction':str(x[1]),
                'lower_decimal':str(Decimal(x[0].numerator)/Decimal(x[0].denominator)),
                'upper_decimal':str(Decimal(x[1].numerator)/Decimal(x[1].denominator))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args()
    author=json.loads((a.source/'PRICE.json').read_text())
    physical={1:16,2:228,3:36,5:268,6:4,7:652}
    normalized={r:F(v,4) for r,v in physical.items()}
    assert normalized=={1:F(4),2:F(57),3:F(9),5:F(67),6:F(1),7:F(163)}
    q=lin(normalized)
    N=lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10})
    H=lin({2:1,4:25,6:1,8:410})
    p2=add(scale(36,N),lin({1:444,**{7*j:444 for j in range(1,9)}}))
    t2=add(scale(36,H),lin({127:222,**{1+7*j:444 for j in range(1,10)}}))
    delta=add(t2,scale(-1,p2))
    allowance=add(N,scale(-1,H),scale(F(1,36),delta))
    room=add(allowance,scale(-1,q))
    for name, ours in [('moment',q),('limiting_allowance',allowance),('limiting_room',room)]:
        other=author[name]
        assert ours[0]<=F(other['upper_fraction']) and F(other['lower_fraction'])<=ours[1]
    m2=add(scale(18,room),scale(F(1,2),delta))
    m4=add(scale(54,room),scale(F(1,2),delta))
    assert m2[1]<0<m4[0] and room[0]>0
    old=scale(F(1,4),lin({1:12,2:228,5:232,6:4,7:652}))
    overhead=lin({1:1,3:9,5:9})
    assert add(old,overhead)[0]<=q[1] and q[0]<=add(old,overhead)[1]
    result={'status':'INDEPENDENT_COMPLETE_PARTIAL_MOVEMENT_INVOICE_PASS',
            'author_price_sha256':hashlib.sha256((a.source/'PRICE.json').read_bytes()).hexdigest(),
            'method':'decimal denominator10^40; exact integer200th roots; independent of author binary denominator',
            'physical_profile':physical,'physical_copies':4,'moment':record(q),
            'allowance':record(allowance),'room':record(room),'m2_margin':record(m2),
            'm4_margin':record(m4),'first_positive_even_m':4,
            'all_later_even_m_positive_by_affine_slope':True,
            'proper_patch_premium_per_copy':record(overhead),
            'scope':'Only the actual partial-source movement comparison. All44owners/4181ADD remain; no complete all-port supplier or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'BUDGET-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status']);print(result['moment']['lower_decimal']);print(result['room']['lower_decimal'])

if __name__=='__main__':main()
