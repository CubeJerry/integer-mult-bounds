import json
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
from argparse import ArgumentParser
POWERS={}
def bracket(n):
    if n not in POWERS:
        scale=10**36
        with localcontext() as ctx:
            ctx.prec=90;v=int(Decimal(n)**(Decimal(199)/200)*scale)
        exact=n**199*scale**200
        assert v**200<=exact<(v+1)**200
        POWERS[n]=(F(v,scale),F(v+1,scale))
    return POWERS[n]
def value(profile):
    lo=hi=F(0)
    for n,c in profile.items():
        a,b=bracket(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi
def linear(*terms):
    out={}
    for scale,p in terms:
        for n,c in p.items():out[n]=out.get(n,F(0))+scale*c
    return out
def main():
    ap=ArgumentParser();ap.add_argument('--out',required=True,type=Path);args=ap.parse_args()
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    P2=linear((36,N),(1,{1:444}),(1,{7*j:444 for j in range(1,9)}))
    T2=linear((36,H),(1,{127:222}),(1,{1+7*j:444 for j in range(1,10)}))
    Q={1:F(4451,8),2:F(7213,16),4:24,8:F(271,30)}
    allowance={127:F(37,6),64:F(74,6),1:-F(74,6)}
    for j in range(1,9):
        allowance[1+7*j]=allowance.get(1+7*j,0)+F(74,6);allowance[7*j]=allowance.get(7*j,0)-F(74,6)
    room=value(linear((1,allowance),(-1,Q)));assert room[0]>0
    gaps={}
    for m in [2,868,870]:
        gaps[m]=value(linear((F(m,2),T2),(-F(m,2),P2),(18*(m-1),N),(-18*(m-1),H),(-18*(m-1),Q)))
    assert gaps[2][1]<0 and gaps[868][1]<0 and gaps[870][0]>0
    base_room=value(linear((1,allowance),(-1,{1:F(4451,8),2:F(7213,16),4:24,8:9})))
    assert base_room[1]<F(279,1000)<F(7,16)
    out={'status':'PASS_INDEPENDENT_TARGET_MOVEMENT','room':[str(x) for x in room],'finite_gaps':{str(m):[str(x) for x in v] for m,v in gaps.items()},'base_room':[str(x) for x in base_room],'first_even_m':870,'precision_decimal_places':36,'power_intervals':{str(n):[str(x) for x in v] for n,v in POWERS.items()},'author_code_or_enclosures_imported':False,'whole_caller_admitted':False}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'BUDGET.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'],float(room[0]),float(gaps[868][1]),float(gaps[870][0]))
if __name__=='__main__':main()
