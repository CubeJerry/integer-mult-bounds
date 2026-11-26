#!/usr/bin/env python3
"""Check CK, its macro FFT, each embedded chirp, and the final natural output order."""
from collections import Counter
from random import Random
import json


def phi(m): return 2*m//3
def add(a,b,mod): return [(x+y)%mod for x,y in zip(a,b,strict=True)]
def sub(a,b,mod): return [(x-y)%mod for x,y in zip(a,b,strict=True)]
def scale(a,x,mod): return [v*x%mod for v in a]


def reduced(coeffs,m,mod):
    # Independent monic long division by W^(2m/3)+W^(m/3)+1.
    n=phi(m); gap=m//3
    v=list(coeffs)+[0]*max(0,n-len(coeffs))
    for k in range(len(v)-1,n-1,-1):
        value=v[k]; v[k-n]-=value; v[k-gap]-=value
    return [x%mod for x in v[:n]]


def fold(coeffs,m,mod):
    full=[0]*m
    for j,x in enumerate(coeffs): full[j%m]=(full[j%m]+x)%mod
    n=phi(m); gap=m//3
    for j in range(gap):
        full[j]=(full[j]-full[n+j])%mod; full[gap+j]=(full[gap+j]-full[n+j])%mod
    return full[:n]


def shift(word,delta,m,mod):
    z=word+[0]*(m-len(word)); delta%=m
    return fold(z[-delta:]+z[:-delta] if delta else z,m,mod)


def guarded(a,b,mod):
    # Finite, independent elementary replacement for a real priced batch call.
    w=2*mod.bit_length()+min(len(a),len(b)).bit_length()+1
    x=sum(v<<(i*w) for i,v in enumerate(a)); y=sum(v<<(i*w) for i,v in enumerate(b)); p=x*y
    return [(p>>(k*w))%mod for k in range(len(a)+len(b)-1)]


def school(a,b,mod):
    ans=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): ans[i+j]+=x*y
    return [t%mod for t in ans]


def ring_product(a,b,m,mod):
    coeff=guarded(a,b,mod); ans=fold(coeff,m,mod)
    assert ans==reduced(coeff,m,mod)
    return ans


def chirp(words,L,mod,sign):
    p=phi(L); step=2*p-1; inv2=pow(2,-1,L); one=[1]+[0]*(p-1); f=[]; g=[]
    for j,x in enumerate(words):
        f.extend(shift(x,sign*inv2*j*j,L,mod)+[0]*(step-p))
        g.extend(shift(one,-sign*inv2*j*j,L,mod)+[0]*(step-p))
    raw=guarded(f,g,mod); rows=[[0]*p for _ in range(L)]
    for j in range(2*L-1):
        rows[j%L]=add(rows[j%L],fold(raw[j*step:(j+1)*step],L,mod),mod)
    return [shift(x,sign*inv2*i*i,L,mod) for i,x in enumerate(rows)]


def axes(fibres,L,m,mod,sign,stats,mutation):
    h=m//L; stats[(L,len(fibres)*h,L*(2*phi(L)-1))]+=1; outputs=[]
    for fibre in fibres:
        result=[[0]*phi(m) for _ in range(L)]
        for u in range(h):
            words=[word[u::h] for word in fibre]
            assert all(len(w)==phi(L) for w in words)
            changed=chirp(words,L,mod,sign)
            for k,w in enumerate(changed):
                lane=((u+1)%h if mutation=='wrong_lanes' else u)
                result[k][lane::h]=w
        outputs.append(result)
    return outputs


def fourier(words,m,mod,sign,stats,mutation=None):
    n=len(words); lv=0; j=n
    while j>1: lv+=1; j//=3
    a=3**(lv//2); b=n//a
    assert a>=3 and b<=3*a
    first=axes([[words[j0+a*j1] for j1 in range(b)] for j0 in range(a)],b,m,mod,sign,stats,mutation)
    middle=[[shift(first[j0][k1],0 if mutation=='drop_twiddle' else sign*(m//n)*j0*k1,m,mod)
             for j0 in range(a)] for k1 in range(b)]
    second=axes(middle,a,m,mod,sign,stats,mutation)
    return [second[k1][k0] for k0 in range(a) for k1 in range(b)]


def direct_fourier(words,m,mod,sign):
    n=len(words); out=[]
    for k in range(n):
        coeff=[0]*(2*m)
        for j,word in enumerate(words):
            exponent=sign*(m//n)*k*j%m
            for i,val in enumerate(word): coeff[exponent+i]+=val
        out.append(reduced(coeff,m,mod))
    return out


def ck(a,b,mod,stats):
    size=len(a); assert len(b)==size
    Q=1; M=3
    while phi(M)<=2*size-2: Q+=1; M*=3
    assert Q>=6
    m=3**(Q//2+1); n=M//m; d=phi(m)
    a=a+[0]*(phi(M)-size); b=b+[0]*(phi(M)-size)
    outer_a=[a[j::n] for j in range(n)]; outer_b=[b[j::n] for j in range(n)]
    def cyclic(twisted):
        power=m//(3*n) if twisted else 0
        vals=[]
        for src in (outer_a,outer_b):
            pre=[shift(w,j*power,m,mod) for j,w in enumerate(src)]
            vals.append(fourier(pre,m,mod,1,stats))
        point=[ring_product(x,y,m,mod) for x,y in zip(*vals)]
        z=fourier(point,m,mod,-1,stats)
        return [scale(shift(w,-j*power,m,mod),pow(n,-1,mod),mod) for j,w in enumerate(z)]
    u,v=cyclic(False),cyclic(True); rows=[]
    for j in range(n):
        diff=sub(v[j],u[j],mod)
        high=scale(sub(shift(diff,2*m//3,m,mod),diff,mod),pow(3,-1,mod),mod)
        low=sub(u[j],high,mod)
        rows.append(add(low,shift(high,1,m,mod),mod))
    out=[rows[j][i] for i in range(d) for j in range(n)]
    assert not any(out[2*size-1:])
    return out[:2*size-1], (M,m,n)


def main():
    rng=Random(202608021); stats=Counter(); dfts=[]; products=[]; integers=[]
    for m,n,H in ((27,9,1),(81,9,3),(81,27,4),(243,27,8)):
        mod=1<<H; words=[[rng.randrange(mod) for _ in range(phi(m))] for _ in range(n)]
        mistakes={}
        for sign in (-1,1):
            oracle=direct_fourier(words,m,mod,sign)
            assert fourier(words,m,mod,sign,stats)==oracle
            if sign==1:
                for bad in ('drop_twiddle','wrong_lanes'):
                    mutated=fourier(words,m,mod,sign,Counter(),bad)
                    mistakes[bad]=sum(v!=w for a,b in zip(oracle,mutated) for v,w in zip(a,b))
                    assert mistakes[bad]
        dfts.append({'m':m,'n':n,'H':H,'direct_DFT_coefficients_both_signs':2*n*phi(m),'wrong_coefficients':mistakes})
    for s,H in ((120,1),(320,3),(930,8),(326,16)):
        mod=1<<H
        a=[rng.randrange(mod) for _ in range(s)]; b=[rng.randrange(mod) for _ in range(s)]
        got,shape=ck(a,b,mod,stats)
        assert got==school(a,b,mod)
        products.append({'s':s,'H':H,'M_m_n':shape,'ordinary_coefficients':len(got)})
    for N in (1000,3072):
        w=(N+1).bit_length(); s=(N+w-1)//w; H=2*w+s.bit_length()+1
        x=rng.getrandbits(N); y=rng.getrandbits(N); cut=(1<<w)-1
        a=[(x>>(i*w))&cut for i in range(s)]; b=[(y>>(i*w))&cut for i in range(s)]
        z,_=ck(a,b,1<<H,stats); carry=0; result=0
        for j,coeff in enumerate(z):
            carry+=coeff;result|=(carry&cut)<<(j*w);carry>>=w
        result|=carry<<(len(z)*w); assert result==x*y
        integers.append({'N_bits':N,'w':w,'s':s,'H':H,'returned_product_bits':result.bit_length()})
    print(json.dumps({'macro_direction_checks':dfts,'full_ring_products':products,'integer_products':integers,
                      'packet_shapes':[{'macro_radix':k[0],'independent_jobs':k[1],
                                        'ordinary_RH_operand_length':k[2],'invocations':n} for k,n in sorted(stats.items())]},indent=2))


if __name__=='__main__': main()
