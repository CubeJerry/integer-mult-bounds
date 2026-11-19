#!/usr/bin/env python3
"""Root review: binary local identities, explicit fields and exact target prices.

No author implementation is imported. Binary elimination checks GF16 rank by
restriction of scalars; integer Newton roots independently enclose all prices.
"""
import argparse, hashlib, itertools, json
from fractions import Fraction as F
from functools import cache
from pathlib import Path

def rem(x,p):
    while x.bit_length()>=p.bit_length():x^=p<<(x.bit_length()-p.bit_length())
    return x

def pmul(x,y):
    z=0
    for k in range(y.bit_length()):
        if (y>>k)&1:z^=x<<k
    return z

def gcd(x,y):
    while y:x,y=y,rem(x,y)
    return x

def irreducible(p):
    n=p.bit_length()-1;x=2
    for k in range(1,n+1):
        x=rem(pmul(x,x),p)
        if k<=n//2 and gcd(x^2,p)!=1:return False
    return x==2

def fm(x,y):return rem(pmul(x,y),0x13)

def fp(x,k):
    z=1
    for _ in range(k):z=fm(z,x)
    return z

def binary(A):
    return [sum(((fm(v,1<<c)>>b)&1)<<(4*j+c) for j,v in enumerate(row) for c in range(4)) for row in A for b in range(4)]

def rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in piv:piv[p]=x;break
            x^=piv[p]
    return len(piv)

def local(author):
    word=json.loads((author/'output/LOCAL-WORD.json').read_text())
    summary=json.loads((author/'output/LOCAL-MODULES.json').read_text())
    V=[[fp(a,k) for k in range(9)] for a in range(1,10)]
    D=[[fp(a,k-1) if k%2 else 0 for k in range(9)] for a in range(1,10)]
    C=[[v if k>=3 else 0 for k,v in enumerate(row)] for row in D]
    assert word['V9']==V and word['partial_cross_C9']==C and word['singleton_derivative_D9']==D
    assert rank(binary(V))==36
    triples=0
    for T in itertools.combinations(range(9),3):
        for j in range(3):assert rank(binary([[V[t][k] for k in range(3*j,3*j+3)] for t in T]))==12
        large=[[V[t][k] for k in range(3,9)] for t in T]+[[C[t][k] for k in range(3,9)] for t in T]
        small=[[V[t][k] for k in range(3)]+[0]*3 for t in T]+[[0]*3+[V[t][k] for k in range(3)] for t in T]
        assert rank(binary(large))==rank(binary(small))==24
        assert rank(binary([V[t] for t in T]+[D[t] for t in T]))==24
        triples+=1
    gates=word['binary_V9_ADD_word'];rows=[1<<k for k in range(36)]
    for dst,src in gates:
        assert 0<=src<36 and 0<=dst<36 and src!=dst;rows[dst]^=rows[src]
    assert rows==binary(V) and len(gates)==525
    counts=[]
    for cross,columns in ((C,[3,5,7]),(D,[1,3,5,7])):
        active=[j for j in range(9) if any(r[j] for r in cross)];assert active==columns
        public=[1<<k for k in range(72)];owned={4*j+k:0 for j in columns for k in range(4)}
        adds=0
        for k in owned:owned[k]^=public[k];adds+=1
        for offset in (0,36):
            for dst,src in gates:public[offset+dst]^=public[offset+src];adds+=1
        for dst,row in enumerate(binary(cross)):
            for src in range(36):
                if row>>src&1:assert src in owned;public[36+dst]^=owned[src];adds+=1
        assert public==binary(V)+[u^(v<<36) for u,v in zip(binary(cross),binary(V))]
        clear=len(owned);owned.clear();assert not owned
        counts.append({'cache_INIT_and_dirty_CLEAR':clear,'ADD_without_chart_permutation':adds,'cross_ADD':sum(v.bit_count() for v in binary(cross))})
    assert counts[0]['cross_ADD']==219 and counts[1]['cross_ADD']==255
    # Each phase permutation has at most45 field positions: at most3*4 per
    # position, twice. This is a safe bound, including every input placement.
    permutation=2*45*4*3
    invoice={'full_plane':{'ADD':10*len(gates)+permutation,'INIT':0,'dirty_CLEAR':0,'extra_peak':0},
             'partial_plane':{'ADD':5*counts[0]['ADD_without_chart_permutation']+permutation,'INIT':60,'dirty_CLEAR':60,'extra_peak':60},
             'singleton_plane':{'ADD':5*counts[1]['ADD_without_chart_permutation']+permutation,'INIT':80,'dirty_CLEAR':80,'extra_peak':80}}
    assert invoice==summary['whole_H_local_invoices']
    assert rank(binary([[V[t][k] for k in range(3,9)] for t in (0,1,2)]+[[0]*6]*3))==12
    assert rank(binary([V[0],V[0],V[1],D[0],D[0],D[1]]))<24
    return {'triples':triples,'full_donor_minors':3*triples,'arbitrary_input_words':2,'local_invoices_degree4':invoice,'local_invoices_degree28':{k:{j:7*v for j,v in z.items()} for k,z in invoice.items()},'independent_representation':'binary restriction of scalars; no author code imported'}

def floor_root(n,k):
    if n<2:return n
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//(x**(k-1)))//k
        if y>=x:break
        x=y
    while (x+1)**k<=n:x+=1
    while x**k>n:x-=1
    assert x**k<=n<(x+1)**k
    return x

@cache
def radical(n):
    scale=10**30;N=n**199*scale**200;r=floor_root(N,200)
    return F(r,scale),F(r if r**200==N else r+1,scale)

def lin(*terms):
    p={}
    for c,vec in terms:
        for n,v in vec.items():p[n]=p.get(n,F(0))+c*v
    return p

def interval(vec):
    lo=hi=F(0)
    for n,c in vec.items():
        a,b=radical(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi

def budget(bank,author):
    report=json.loads((author/'output/BUDGET.json').read_text())
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    P=lin((36,N),(1,{1:444}),*((1,{7*k:444}) for k in range(1,9)))
    T=lin((36,H),(1,{127:222}),*((1,{1+7*k:444}) for k in range(1,10)))
    Q={1:F(4451,8),2:F(7213,16),4:F(24),8:F(9)}
    limit=lin((F(1,36),T),(-F(1,36),P),(1,N),(-1,H));room=interval(lin((1,limit),(-1,Q)))
    eighth=radical(8);cap=(bank*room[0]/eighth[1],bank*room[1]/eighth[0])
    ceiling=16 if bank==480 else 67;assert ceiling<cap[0]<=cap[1]<ceiling+1
    expected={0:46,8:86,15:404,16:870,17:None} if bank==480 else {0:46,31:84,62:552,63:676,67:6750,68:None}
    for r,m in expected.items():
        profile=lin((1,Q),(F(r,bank),{8:1}));slack=interval(lin((1,limit),(-1,profile)))
        if m is None:assert slack[1]<0;continue
        assert slack[0]>0
        def gap(k):return interval(lin((F(k,2),T),(-F(k,2),P),(-18*(k-1),H),(18*(k-1),N),(-18*(k-1),profile)))
        assert gap(m)[0]>0 and gap(m-2)[1]<0
    for w,z in report['invoices'].items():
        w=int(w);M=111*bank*w;C=9*bank*w
        assert z['M']==M and z['C']==C and z['ADD']==17*M*M+50*M+111*C
        assert z['INIT']==z['dirty_CLEAR']==5*M+C and z['peak_public_and_auxiliary']==7*M+C
        assert z['MOVE']=={'1':bank*4451//8*w,'2':bank*7213//16*w,'4':24*bank*w,'8':9*bank*w}
    return {'bank':bank,'excess_integer_limit':ceiling,'threshold_interval':list(map(str,cap)),'first_even_m':expected,'every_reported_ordinary_invoice_checked':True,'radical_scale':10**30}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author480',type=Path,required=True);ap.add_argument('--author1920',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    fields={hex(p):irreducible(p) for p in (0x13,0x83,0x2000009,0x8000027,0x10000003)};assert all(fields.values())
    assert not irreducible(0x15)
    assert 10*(6470+222)*480<2**25 and 10*(6470+222)*1920<2**27
    assert 10*(6470*3323+111*1426+222*1920)==220843360<2**28
    result={'status':'PASS_INDEPENDENT_FIELDS_LOCAL_WORDS_AND_BUDGETS','irreducible_moduli':fields,'GF16_degree28_tower_coprime_degrees':[4,7],
            'local':local(a.author480),'budget480':budget(480,a.author480),'budget1920':budget(1920,a.author1920),
            'fixed_left_H_rank_only_completion_reviewed':True,'fixed_right_K_completion_claimed':False,'complete_native_endpoint':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'FIELD-BUDGET.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])

if __name__=='__main__':main()
