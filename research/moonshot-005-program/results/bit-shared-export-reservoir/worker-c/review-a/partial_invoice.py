#!/usr/bin/env python3
"""Independent directed completed-BIT movement comparison for a partial word."""
import argparse,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from check import need,nth_root,price

def add(*terms):
    out=Counter()
    for coefficient,profile in terms:
        for rank,count in profile.items():out[rank]+=coefficient*count
    return out

def moment(profile):
    scale=10**30;lo=hi=F(0)
    for rank,count in profile.items():
        exact=rank**199*scale**200;root=nth_root(exact,200)
        need(root**200<=exact<(root+1)**200,'exact integer root bound')
        a,b=F(root,scale),F(root if root**200==exact else root+1,scale)
        lo+=count*(a if count>=0 else b);hi+=count*(b if count>=0 else a)
    return lo,hi

def encode(interval):
    lo,hi=interval
    return {'lower':str(lo),'upper':str(hi),'approximate_decimal':str(float((lo+hi)/2))}

def check(profile):
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    H={2:1,4:25,6:1,8:410}
    P2=add((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
    T2=add((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
    cap=add((1,N),(-1,H),(F(1,36),T2),(F(-1,36),P2))
    simplified=add((F(37,6),{127:1}),(F(37,3),{1+7*j:1 for j in range(1,10)}),
                   (F(-37,3),{1:1}),(F(-37,3),{7*j:1 for j in range(1,9)}))
    need(all(cap[k]==simplified[k]for k in set(cap)|set(simplified)),'exact target-cap cancellation')
    room=moment(add((1,cap),(-1,profile)));controls=[]
    for m in range(2,22,2):
        margin=moment(add((F(m,2),T2),(F(-m,2),P2),(18*(m-1),N),(-18*(m-1),H),(-18*(m-1),profile)))
        controls.append({'m':m,'margin':encode(margin),'strictly_positive':margin[0]>0})
    first=next((row['m']for row in controls if row['strictly_positive']),None)
    return {'status':'PASS_EXACT_PARTIAL_MOVEMENT_COMPARISON','t':'199/200','profile':profile,
            'moment':price(profile),'target_cap':encode(moment(cap)),'limiting_room':encode(room),
            'finite_even_caller_controls':controls,'first_positive_even_m_in_tested_range':first,
            'all_larger_even_m_positive_by_linear_margin':room[0]>0 and first is not None,
            'scope':'Necessary movement inequality only. The word is partial; ordinary, compiler, ownership, precision, recursive compatibility and missing outputs are not certified.',
            'new_complete_kappa':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--result',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    data=json.loads(a.result.read_text());rows=data.get('receipts',data.get('variants'))
    name=next(name for name in rows if name in ['CLOSED-WORD.json','COUPLED-CLOSED-WORD.json'])
    profile={int(rank):count for rank,count in rows[name]['movement_profile'].items()}
    a.output.write_text(json.dumps(check(profile),indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
