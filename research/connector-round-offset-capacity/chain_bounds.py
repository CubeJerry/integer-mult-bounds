"""Exact finite arithmetic corroborating CHAIN_COVER.md; no real logarithms.

@CubeJerry with OpenAI Codex assistance. Apache-2.0.
"""
from math import comb


def require(ok, message):
    if not ok:
        raise ValueError(message)


def capacity(c):
    require(type(c) is int and c >= 2, 'characteristic')
    D=c.bit_length()-1
    b,w=1,1
    while True:
        nxt=2*w if b%2 else w*(b+1)//(b//2+1)
        if D*nxt>c:
            break
        b,w=b+1,nxt
    return D,b,c//(D+1),w


def check_bounds():
    for b in range(1,2049):
        w=comb(b,b//2)
        require(w*w*b <= 1<<(2*b), 'upper binomial estimate')
        require(16*b*w*w >= 1<<(2*b), 'lower binomial estimate')
    for c in range(2,16385):
        D,b,B,w=capacity(c)
        require(w==comb(b,b//2), 'central binomial recurrence')
        require(D*w<=c<D*comb(b+1,(b+1)//2), 'maximal feasible width')
        require(B*(D+1)<=c, 'concatenation budget')
        old_b=(c//D+1).bit_length()-1
        require(b>=old_b, 'refinement cannot lose source capacity')
    table=[]
    for e in (4,8,16,32,64,128,1024,4096):
        c=1<<e;D,b,B,w=capacity(c)
        require(D*w<=c<D*comb(b+1,(b+1)//2), 'large exact budget')
        table.append({'log2_c':e,'groups':D,'width':b,'ratio_ppm':10**6*D*b*B//(c*e)})
    return {'binomial_cases':2048,'capacity_integers':16383,'table':table}
