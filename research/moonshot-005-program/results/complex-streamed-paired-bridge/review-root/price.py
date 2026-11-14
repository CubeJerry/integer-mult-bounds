#!/usr/bin/env python3
"""Independent integer-root intervals from independently replayed profiles."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache

def need(ok,s):
    if not ok:raise ValueError(s)

def root(n,k):
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:break
        x=y
    while pow(x,k)>n:x-=1
    while pow(x+1,k)<=n:x+=1
    return x

@lru_cache(None)
def interval(r):
    D=10**30;n=pow(r,199)*pow(D,200);z=root(n,200)
    need(pow(z,200)<=n<pow(z+1,200),'directed integer-root bound')
    return F(z,D),F(z+1,D)

def add(*parts):
    out={}
    for c,h in parts:
        for k,v in h.items():out[int(k)]=out.get(int(k),F(0))+c*F(v)
    return {k:v for k,v in out.items()if v}

def moment(h):
    lo=hi=F(0)
    for r,c in h.items():
        a,b=interval(r)
        lo+=c*(a if c>0 else b);hi+=c*(b if c>0 else a)
    return lo,hi

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--package',type=Path,required=True)
    p.add_argument('--full',type=Path,required=True)
    p.add_argument('--review',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    raw=a.full.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','full caller pin')
    full=json.loads(raw);report=json.loads(a.review.read_text())
    slope=add((F(1,18),full['invoice']['T']),(F(-1,18),full['invoice']['P']))
    penalty=moment(add((-1,slope)));answers=[]
    for r in report['variants']:
        Q=add((1,r['raw']),(1,r['owned']))
        signed=add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']),(-1,Q))
        room=moment(signed)
        m=next(k for k in range(2,100)if room[0]-penalty[1]/(k-1)>0)
        if m>2:need(room[1]-penalty[0]/(m-2)<0,'first positive m exact')
        author=json.loads((a.package/r['mode'].replace('_','-')/'PRICE.json').read_text())
        old=list(map(F,author['limiting_room']))
        need(room[0]<=old[0]<=old[1]<=room[1],'author interval enclosed independently')
        need(m==author['first_positive_fixed_m'],'first m agrees')
        answers.append(dict(mode=r['mode'],limiting_interval=list(map(str,room)),limit_decimal=float(room[0]),first_positive_m=m,positive_margin=list(map(str,[room[0]-penalty[1]/(m-1),room[1]-penalty[0]/(m-1)]))))
    out=dict(status='PASS_INDEPENDENT_STREAMING_FULL_MOVEMENT_ACCOUNT',exponent='199/200',precision_decimal=30,penalty=list(map(str,penalty)),variants=answers,scope='Full signed movement invoice for actual partial source; missing completion/ordinary/physical admission not priced as zero.')
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],[(r['mode'],r['first_positive_m'])for r in answers])
if __name__=='__main__':main()
