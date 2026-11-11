#!/usr/bin/env python3
"""Independent dyadic, exact-power-check audit of the prepaid full profile."""
import argparse,gzip,hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
def need(p,s):
    if not p:raise ValueError(s)
def enclosure(r):
    D=2**80;N=r**199*D**200
    with localcontext() as c:
        c.prec=90;a=int(Decimal(r)**(Decimal(199)/200)*D)
    while a**200>N:a-=1
    while (a+1)**200<=N:a+=1
    need(a**200<=N<(a+1)**200,'exact200thpower enclosure')
    return F(a,D),F(a if a**200==N else a+1,D)
def run(source,invoice,current,historical,author):
    raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin')
    w=json.loads(gzip.decompress(raw));ir=invoice.read_bytes();need(hashlib.sha256(ir).hexdigest()=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248','invoice pin');z=json.loads(ir)
    def rank(i):
        e=w['program'][i];need(e[0]=='MOVE' and e[1]>=w['public'] and e[4] is True,'owned source occurrence');return abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))
    old=Counter(rank(i) for i,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]>=w['public'])
    c=json.loads(current.read_text());h=json.loads(historical.read_text());events=[q['before_event'] for q in c['witnesses']]+[q['event'] for q in h]
    need(len(events)==len(set(events))==14,'distinct14');saved=Counter(rank(i) for i in events);preload=Counter(len(w['frames'][q['to']]) for q in h);need(w['frames'][3]==[],'empty entry chart')
    need(saved==Counter({1:6,2:4,3:1,4:1,5:1,6:1}) and preload==Counter({3:3,6:1}),'source profiles')
    T=Counter({int(k):v for k,v in z['T4'].items()});P=Counter({int(k):v for k,v in z['P4'].items()})
    for r in set(old)|set(saved)|set(preload):P[r]+=18*(old[r]-saved[r]+preload[r])
    powers={r:enclosure(r) for r in set(T)|set(P)}
    def moment(profile):
        lo=hi=F(0)
        for r,n in profile.items():
            a,b=powers[r];lo+=n*(a if n>=0 else b);hi+=n*(b if n>=0 else a)
        return lo,hi
    margin=moment({r:T[r]-P[r] for r in set(T)|set(P)});need(F(3)<margin[0]/18<=margin[1]/18<F(4),'strict3arrival ceiling')
    a=json.loads(author.read_text());need(P==Counter({int(k):v for k,v in a['new_P'].items()}),'independent complete paid histogram')
    recorded=[F(int(x),10**15) for x in a['raw_margin_numerator_bounds']];need(recorded[0]<=margin[0]<=margin[1]<=recorded[1],'dyadic interval inside author enclosure')
    extra=moment({2:-3,5:-1,3:3,6:1});need(extra[0]>0,'positive premium over10skip baseline')
    need(sum(P.values())==153090 and sum(T.values())==27344,'complete position census');surplus=sum(r*T[r] for r in T)-sum(r*P[r] for r in P);need(surplus==3346,'rank surplus')
    return {'status':'PASS_INDEPENDENT_PREPAID_PROFILE','source_sha256':hashlib.sha256(raw).hexdigest(),'author_budget_sha256':hashlib.sha256(author.read_bytes()).hexdigest(),'dyadic_denominator':str(2**80),'margin_bounds':[str(x) for x in margin],'per_native_headroom_bounds':[str(x/18) for x in margin],'positive_net_premium_bounds':[str(x) for x in extra],'paid_count':sum(P.values()),'targets':sum(T.values()),'rank_surplus':surplus,'additional_rank_one_ceiling':3,'scope':'Exact conditional profile only; current/owned physical observations, complete shared native and all ordinary/precision/compiler tariffs remain premises.'}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for s in ('source','invoice','current','historical','author'):p.add_argument('--'+s,type=Path,required=True)
    p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.invoice,a.current,a.historical,a.author);t=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(t)
    print(t,end='')
