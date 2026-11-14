#!/usr/bin/env python3
"""Independent outward dyadic full-caller price for the actual parity source."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)
def main(a):
    raw=a.full.read_bytes();pin=hashlib.sha256(raw).hexdigest()
    need(pin=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','caller pin')
    f=json.loads(raw);r=json.loads(a.review.read_text());au=json.loads(a.author.read_text())
    need(r['status']=='PASS_INDEPENDENT_ACTUAL_PARITY_HALF_COMPILER','actual source review')
    T,P,N,H=({int(k):F(v) for k,v in f[i][j].items()} for i,j in [('invoice','T'),('invoice','P'),('native','paid'),('native','helpers')])
    Q={int(k):F(v) for k,v in r['bill']['moves'].items()}
    def add(*terms):
        d={}
        for c,p in terms:
            for k,v in p.items():d[k]=d.get(k,F(0))+c*v
        return {k:v for k,v in d.items() if v}
    S=add((F(1,18),T),(F(-1,18),P));B=add((1,S),(1,N),(-1,H),(-1,Q));grid=1<<160;cache={}
    def power(k):
        if k not in cache:
            nn=k**199*grid**200;lo,hi=0,k*grid+1
            while hi-lo>1:
                m=(lo+hi)//2
                if m**200<=nn:lo=m
                else:hi=m
            need(lo**200<=nn<hi**200,'outward root')
            cache[k]=F(lo,grid),F(hi,grid)
        return cache[k]
    def mom(p):
        lo=hi=F(0)
        for k,v in p.items():
            l,h=power(k);lo+=v*(l if v>0 else h);hi+=v*(h if v>0 else l)
        return lo,hi
    room=mom(B);pen=mom(add((-1,S)));need(room[0]>0 and pen[0]>0,'correct limiting sign and finite penalty')
    m=2
    while room[0]-pen[1]/(m-1)<=0:m+=1
    need(m==35 and room[1]-pen[0]/(m-2)<0,'strict first m35')
    for key,v in [('limiting_room',room),('finite_m_penalty',pen)]:
        l,h=map(F,au[key]);need(l<=v[0]<v[1]<=h,'independent tighter '+key)
    need(au['first_m_positive_certified']==m,'same multiplicity')
    one_extra=(room[0]-1,room[1]-1);need(one_extra[1]<0,'one extra unit move exceeds limiting room')
    out={'status':'PASS_INDEPENDENT_PARITY_FULL_CALLER_PRICE','word_sha256':r['word_sha256'],'full_sha256':pin,'grid':'2^-160','Q':{str(k):str(v) for k,v in Q.items()},'limiting_room':list(map(str,room)),'finite_m_penalty':list(map(str,pen)),'first_m':m,'at_m35':[str(room[0]-pen[1]/34),str(room[1]-pen[0]/34)],'at_m34':[str(room[0]-pen[1]/33),str(room[1]-pen[0]/33)],'one_additional_rank1_move_room':list(map(str,one_extra)),'scope':'Actual partial word movement invoice only. Any additional source operation must be explicitly repriced. No endpoints, strict supplier or foundational premise is inferred.','new_kappa':None}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'room':float(room[0]),'first_m':m,'one_extra_move':float(one_extra[1])}))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ['full','review','author','output']:p.add_argument('--'+n,type=Path,required=True)
    main(p.parse_args())
