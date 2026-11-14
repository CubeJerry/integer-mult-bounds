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
    for name in ['package','full','review','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();raw=a.full.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','complete caller byte pin')
    full=json.loads(raw);review=json.loads(a.review.read_text());author=json.loads((a.package/'output/PRICE.json').read_text())
    slope=add((F(1,18),full['invoice']['T']),(F(-1,18),full['invoice']['P']))
    penalty=moment(add((-1,slope)));need(penalty[0]>0,'strict finite-m penalty')
    seed=review['variants'][0]['seed_profile']
    seedroom=add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']),(-1,seed))
    checked=[]
    for k in range(2,9):
        delta=add((4*k*(k-1),{1:1}),(4*k,{9-k:1}),(-2*k,{8:1}),(-2*k,{3:1,5:1}),(2,{k:1}))
        added=moment(delta);room=moment(add((1,seedroom),(-1,delta)))
        old=author['family'][k-2]
        old_delta=list(map(F,old['increment']));old_room=list(map(F,old['limiting_margin']))
        need(added[0]<=old_delta[0]<=old_delta[1]<=added[1], 'independent increment encloses author')
        need(room[0]<=old_room[0]<=old_room[1]<=room[1], 'independent room encloses author')
        first=None
        if room[0]>0:
            first=next(m for m in range(2,1000)if room[0]>penalty[1]/(m-1))
            need(room[1]<penalty[0]/(first-2), 'exact preceding m fails')
        else:need(room[1]<0,'strict negative limiting margin')
        need(first==old['first_positive_fixed_m'],'first fixed m agrees exactly')
        if k in (2,4,8):
            replay=next(r for r in review['variants'] if r['size']==k)
            actual=add((1,replay['raw']),(1,replay['owned']))
            need(actual==add((1,seed),(1,delta)), 'formula agrees with independently replayed actual word')
        checked.append(dict(size=k,added_interval=list(map(str,added)),added_decimal=float(added[0]),limiting_room=list(map(str,room)),room_decimal=float(room[0]),first_positive_m=first,literal_source_reviewed=k in (2,4,8)))
    oracle=moment(add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']),(-1,{8:400})))
    lower=moment({8:24});gap=(oracle[0]-lower[1],oracle[1]-lower[0])
    need(gap[1]<0,'strict global fresh-disjoint-clique oracle exclusion')
    false_single_owner=moment({8:12})
    need(oracle[0]-false_single_owner[1]>0,'omitting reverse transport falsely passes oracle; paired tariff essential')
    wrong_k8=add((32,{1:1}),(-16,{8:1}),(-16,{3:1,5:1}),(2,{8:1}))
    need(moment(wrong_k8)[1]<moment(add((1,review['variants'][2]['raw']),(1,review['variants'][2]['owned']),(-1,seed)))[0], 'rank-one bucket overwrite undercharges actual word')
    out=dict(status='PASS_INDEPENDENT_CLIQUE_FULL_CALLER_INVOICES',precision_decimal=30,exponent='199/200',finite_m_penalty=list(map(str,penalty)),family=checked,global_screen=dict(oracle=list(map(str,oracle)),paired_lower=list(map(str,lower)),gap=list(map(str,gap))),negative_controls=['dropping paired reverse transport gives a false favorable oracle','overwriting coincident rank1 buckets undercharges k8'],scope='Actual partial words k2/k4/k8 and proved cyclic-family formula; scoped fresh disjoint-cohort exclusion. Foundational, ordinary and completion obligations remain; no new kappa.')
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()

