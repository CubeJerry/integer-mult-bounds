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
    for n in ['package','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=(a.package/'dependencies/FULL-RESULT.json').read_bytes();need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','full caller pin');full=json.loads(raw)
    old=json.loads((a.package/'output/PRICE.json').read_text());slope=add((F(1,18),full['invoice']['T']),(F(-1,18),full['invoice']['P']));penalty=moment(add((-1,slope)))
    Q={1:120,2:112,3:88,5:200,8:216};room_profile=add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']),(-1,Q));room=moment(room_profile)
    def encloses(got,expected):
        x,y=map(F,expected);need(got[0]<=x<=y<=got[1],'author enclosure contained independently')
    encloses(room,old['seed_limiting_room']);encloses(penalty,old['finite_m_penalty_coefficient']);need(penalty[0]>0,'fixed-m penalty strictly positive')
    profiles=[{1:79,7:79,8:-78},{1:79,7:80,8:-79},{1:88,7:88,8:-88},{1:96,2:120,3:304,5:96,8:-216},{1:96,2:216,3:400,8:-216}];answers=[]
    for i,profile in enumerate(profiles):
        e=old['scenarios'][i];need({int(k):v for k,v in e['new_minus_seed_profile'].items()}==profile,'independently derived scenario profile');inc=moment(profile);margin=moment(add((1,room_profile),(-1,profile)));encloses(inc,e['increment']);encloses(margin,e['limiting_margin'])
        first=next((m for m in range(2,101)if margin[0]-penalty[1]/(m-1)>0),None)
        need(first==e['first_positive_fixed_m_for_this_screen'],'screen first m');need(first is not None or margin[1]<0,'strict all-m rejection')
        if first and first>2:need(margin[1]-penalty[0]/(first-2)<0,'minimal first m')
        answers.append(dict(name=e['name'],increment=list(map(str,inc)),limiting_margin=list(map(str,margin)),first_positive_m=first))
    stop=moment({1:1,7:1,8:-1});refund=moment({1:1,2:1,3:-1});encloses(stop,old['raw_rank8_facet_stop_increment']);encloses(refund,old['refund_per_deleted_raw_pivot_1plus2_to3']);need(stop[0]>0 and refund[0]>0,'positive tariffs')
    deficit=moment(add((1,profiles[0]),(-1,room_profile)));need(deficit[0]>26*refund[1]and deficit[1]<27*refund[0],'exact27-refund arithmetic boundary')
    out=dict(status='PASS_INDEPENDENT_SCOPED_GLOBAL_PREFIX_PRICE',exponent='199/200',seed_room=list(map(str,room)),penalty=list(map(str,penalty)),rank8_deficit=list(map(str,deficit)),minimum_arithmetic_refunds=27,scenarios=answers,scope='Conditional route screens only; no acquisition or refunds constructed; paired and non-MOVE obligations remain.')
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
