#!/usr/bin/env python3
"""Independent complete CK input/output and two macroradix DFTs over Z/(2^precision)."""
from collections import Counter
from random import Random
import json


def ordinary(u,v,precision):
    """Guarded nonnegative integer product, followed by coefficientwise reduction."""
    if not u or not v:
        return []
    guard=2*precision+min(len(u),len(v)).bit_length()
    z=sum(x<<(guard*i) for i,x in enumerate(u))*sum(x<<(guard*i) for i,x in enumerate(v))
    mask=(1<<precision)-1
    return [(z>>(guard*i))&mask for i in range(len(u)+len(v)-1)]


def red(poly,order,mask):
    third=order//3
    p=2*third
    a=poly+[0]*max(0,p-len(poly))
    for i in range(len(a)-1,p-1,-1):
        a[i-p]-=a[i]
        a[i-third]-=a[i]
    return [x&mask for x in a[:p]]


def shift(poly,offset,order,mask):
    width=order//3
    offset%=order
    zp=poly+[0]*(order-len(poly))
    zp=zp[-offset:]+zp[:-offset] if offset else zp
    return [(zp[i]-zp[2*width+i%width])&mask for i in range(2*width)]


def chirp(words,length,sign,precision,counts):
    p=2*(length//3)
    stride=2*p-1
    mask=(1<<precision)-1
    two=pow(2,-1,length)
    arr=[]
    kernel=[]
    for j,word in enumerate(words):
        assert len(word)==p
        phase=sign*two*j*j
        arr+=shift(word,phase,length,mask)+[0]*(stride-p)
        kernel+=shift([1],-phase,length,mask)+[0]*(stride-p)
    raw=ordinary(arr,kernel,precision)
    out=[[0]*p for _ in range(length)]
    for j in range(2*length-1):
        part=red(raw[j*stride:(j+1)*stride],length,mask)
        out[j%length]=[(a+b)&mask for a,b in zip(out[j%length],part,strict=True)]
    counts["ordinary_macro_packet_products"]+=1
    return [shift(word,sign*two*i*i,length,mask) for i,word in enumerate(out)]


def small_dft(words,order,sign,precision,counts):
    length=len(words)
    lanes=order//length
    p=2*(order//3)
    out=[[None]*p for _ in range(length)]
    for u in range(lanes):
        packet=[word[u::lanes] for word in words]
        results=chirp(packet,length,sign,precision,counts)
        for j,row in enumerate(results):
            out[j][u::lanes]=row
    assert all(None not in word for word in out)
    return out


def macro(words,order,sign,precision,counts,skip_twiddle=False):
    mask=(1<<precision)-1
    n=len(words)
    A=1
    while 9*A*A<=n:
        A*=3
    B=n//A
    assert A>=3 and B in (A,3*A)
    tmp=[[None]*A for _ in range(B)]
    for j0 in range(A):
        rows=small_dft([words[j0+A*j1] for j1 in range(B)],order,sign,precision,counts)
        for k1,row in enumerate(rows):
            tmp[k1][j0]=row if skip_twiddle else shift(row,sign*(order//n)*j0*k1,order,mask)
    out=[None]*n
    for k1,packet in enumerate(tmp):
        for k0,row in enumerate(small_dft(packet,order,sign,precision,counts)):
            out[k1+B*k0]=row
    return out


def direct_finite_dft(words,order,sign,mask):
    n=len(words)
    result=[]
    for k in range(n):
        rolled=[shift(word,sign*(order//n)*j*k,order,mask) for j,word in enumerate(words)]
        result.append([sum(column)&mask for column in zip(*rolled,strict=True)])
    return result


def cyclic(a,b,m,H,counts):
    mask=(1<<H)-1
    n=len(a)
    f=macro(a,m,1,H,counts)
    g=macro(b,m,1,H,counts)
    point=[red(ordinary(x,y,H),m,mask) for x,y in zip(f,g,strict=True)]
    counts["true_pointwise_products"]+=len(point)
    raw=macro(point,m,-1,H,counts)
    scale=pow(n,-1,1<<H)
    return [[(z*scale)&mask for z in word] for word in raw]


def ck(f,g,n,m,H,counts):
    pm=2*(m//3)
    size=n*pm
    mask=(1<<H)-1
    def reshape(values):
        raw=values+[0]*(size-len(values))
        return [raw[j::n] for j in range(n)]
    a,b=reshape(f),reshape(g)
    untwisted=cyclic(a,b,m,H,counts)
    power=m//(3*n)
    av=[shift(z,j*power,m,mask) for j,z in enumerate(a)]
    bv=[shift(z,j*power,m,mask) for j,z in enumerate(b)]
    second=cyclic(av,bv,m,H,counts)
    inv3=pow(3,-1,1<<H)
    result=[None]*size
    for j,(u,tw) in enumerate(zip(untwisted,second,strict=True)):
        v=shift(tw,-j*power,m,mask)
        diff=[(y-x)&mask for x,y in zip(u,v,strict=True)]
        up=shift(diff,2*(m//3),m,mask)
        high=[((x-y)*inv3)&mask for x,y in zip(up,diff,strict=True)]
        high_y=shift(high,1,m,mask)
        result[j::n]=[(z+x-y)&mask for z,x,y in zip(u,high_y,high,strict=True)]
    expected=ordinary(f,g,H)
    assert result==expected+[0]*(size-len(expected))
    counts["ordinary_CK_coefficients_including_zero_padding"]+=len(result)
    counts["full_two_operand_CK_products"]+=1


def main():
    rng=Random(0xC07A4)
    cases=[]
    total=Counter()
    for n,m,H in [(9,27,1),(9,81,2),(27,81,2),(27,243,5),(81,243,3)]:
        counts=Counter()
        p=2*(m//3)
        mask=(1<<H)-1
        words=[[rng.randrange(mask+1) for _ in range(p)] for _ in range(n)]
        expected=direct_finite_dft(words,m,1,mask)
        forward=macro(words,m,1,H,counts)
        assert forward==expected
        assert macro(words,m,-1,H,counts)==direct_finite_dft(words,m,-1,mask)
        wrong=macro(words,m,1,H,Counter(),skip_twiddle=True)
        counts["wrong_omitted_twiddle_symbols"]=sum(x!=y for a,b in zip(wrong,expected,strict=True) for x,y in zip(a,b,strict=True))
        assert counts["wrong_omitted_twiddle_symbols"]>0
        counts["direct_DFT_symbols_compared"]=2*n*p
        top=(n*p)//2
        left=[rng.randrange(mask+1) for _ in range(top)]
        right=[rng.randrange(mask+1) for _ in range(top)]
        ck(left,right,n,m,H,counts)
        cases.append({"n":n,"m":m,"H":H,"counts":dict(sorted(counts.items()))})
        total.update(counts)
    print(json.dumps({"seed":"0xc07a4","cases":cases,"totals":dict(sorted(total.items()))},indent=2))


if __name__=="__main__":
    main()
