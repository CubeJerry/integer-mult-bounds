#!/usr/bin/env python3
"""Independent native-rank, message-count and integer-price checks."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

def rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in piv:piv[p]=x;break
            x^=piv[p]
    return len(piv)

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(c,a):return (c*a[0],c*a[1]) if c>=0 else (c*a[1],c*a[0])
def enc(a):
    with localcontext() as c:
        c.prec=60
        return {'rational':[str(x) for x in a],'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in a]}

def prices():
    den=10**55;cache={}
    def power(r):
        if r not in cache:
            target=r**199*den**200
            with localcontext() as ctx:
                ctx.prec=85
                z=int(Decimal(r)**(Decimal(199)/200)*den)
            while z**200>target:z-=1
            while (z+1)**200<=target:z+=1
            assert z**200<=target<(z+1)**200
            cache[r]=(F(z,den),F(z if z**200==target else z+1,den))
        return cache[r]
    def moment(dic):
        v=(F(0),F(0))
        for r,c in dic.items():v=add(v,scale(F(c),power(r)))
        return v
    n=moment({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10})
    h=moment({2:1,4:25,6:1,8:410})
    p2=add(scale(36,n),moment({1:444,**{7*j:444 for j in range(1,9)}}))
    t2=add(scale(36,h),moment({127:222,**{1+7*j:444 for j in range(1,10)}}))
    q=moment({1:F(4451,8),2:F(7213,16),4:24,8:9})
    limit=add(add(scale(F(1,36),add(t2,scale(-1,p2))),n),scale(-1,h))
    room=add(limit,scale(-1,q));p8=power(8)
    threshold=(5760*room[0]/p8[1],5760*room[1]/p8[0])
    assert 202<threshold[0]<=threshold[1]<203
    rows=[]
    for r,expected in [(0,46),(1,46),(70,70),(100,90),(200,3854),(202,27218),(203,None),(5690,None)]:
        qr=add(q,scale(F(r,5760),p8))
        slope=scale(18,add(limit,scale(-1,qr)))
        constant=scale(-18,add(add(n,scale(-1,h)),scale(-1,qr)))
        delta=lambda m:add(scale(m,slope),constant)
        if expected:
            assert slope[0]>0 and delta(expected)[0]>0 and delta(expected-2)[1]<0
        else:assert slope[1]<0 and delta(2)[1]<0
        rows.append({'r':r,'first_even_m':expected,'limiting_room':enc(scale(F(1,18),slope)),
                     'first_passing_gap':enc(delta(expected)) if expected else None,
                     'last_failing_gap':enc(delta(expected-2)) if expected else None})
    return {'base_room':enc(room),'rank_threshold':enc(threshold),'exact_200th_power_brackets':len(cache),'cases':rows}

def native(repo):
    path=repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    raw=path.read_bytes()
    assert sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(raw)['native_roots'];n=len(roots)
    o=[sum(1<<j for j,v in enumerate(roots) if sum(x*y for x,y in zip(u,v))==0) for u in roots]
    h=[v^(1<<i) for i,v in enumerate(o)]
    assert n==111 and rank(h)==9
    restrictions=[rank([r&(((1<<n)-1)^o[i]) for r in h]) for i in range(n)]
    assert restrictions==[9]*111
    assert (o[0]>>1)&1
    assert rank([o[0],1])==2
    assert rank(h+[o[0],1])-rank(h)==1
    return {'source_sha256':sha256(raw).hexdigest(),'canonical_rank':9,
            'outside_ranks':restrictions,'native_reuse_control_defect_rank':2,'native_reuse_control_quotient_rank':1}

def fibres():
    count=0
    for n in range(1,5):
        for h in range(1<<n):
            for a in range(1<<n):
                for b in range(1<<n):
                    groups={}
                    for x in range(1<<n):
                        hx=(h&x).bit_count()%2
                        y=(a&x).bit_count()%2+2*((b&x).bit_count()%2)
                        groups.setdefault(hx,set()).add(y)
                    assert set(map(len,groups.values()))=={2**(rank([h,a,b])-rank([h]))}
                    count+=1
    return {'exact_map_cases':count,'all_fibre_sizes_equal_two_to_quotient_rank':True}

def word_control():
    def multiply(a,b):
        out=[]
        for row in a:
            v=0
            for j,r in enumerate(b):
                if (row>>j)&1:v^=r
            out.append(v)
        return out
    ident=[1<<i for i in range(8)]
    canonical=[sum(1<<(2*j+a) for j in range(4)) for i in range(4) for a in range(2)]
    target=[u^v for u,v in zip(ident,canonical)]
    defect=[0]*8;defect[1]=1<<2
    proper=[u^v for u,v in zip(target,defect)]
    late=[(1<<(i+1))-1 for i in range(8)]
    inv=[1]+[(1<<i)|(1<<(i-1)) for i in range(1,8)]
    assert multiply(late,inv)==ident==multiply(inv,late)
    ground_x=multiply(inv,[u^v for u,v in zip(canonical,defect)])
    assert [u^v for u,v in zip(multiply(late,ground_x),proper)]==ident
    assert multiply(late,inv)==ident
    omitted=multiply(inv,canonical)
    assert [u^v for u,v in zip(multiply(late,omitted),proper)]!=ident
    assert late!=ident
    assert rank(canonical+defect)-rank(canonical)==1
    for i in range(4):
        for j in range(4):
            if i!=j:assert rank([(proper[2*i+a]>>(2*j))&3 for a in range(2)])==2
    return {'all_original_X_and_Y_columns':16,'quotient_rank':1,'all_foreign_blocks_invertible':True,
            'omitted_syndrome_rejected':True,'omitted_late_inverse_rejected':True,
            'scope':'Algebraic interface control, not a native balanced code'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    result={'native':native(a.repo),'fibre_counts':fibres(),'word_control':word_control(),'prices':prices(),
            'scope':'Independent checks supplement written proof review. No balanced coefficient assignment or supplier.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS independent ground-repair ranks, exact fibres and price inequalities')
if __name__=='__main__':main()
