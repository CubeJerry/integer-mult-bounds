#!/usr/bin/env python3
"""Exact all-input tests of paired prefix/suffix transport with retained modes."""
from __future__ import annotations
import argparse, json, random
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)
def norm(x,p):return x%p if p else F(x)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def zero(n,m):return [[0]*m for _ in range(n)]
def add(A,B,p,c=1):return [[norm(x+c*y,p) for x,y in zip(a,b)] for a,b in zip(A,B)]
def mul(A,B,p):return [[norm(sum(x*y for x,y in zip(a,b)),p) for b in zip(*B)] for a in A]
def transpose(A):return list(map(list,zip(*A)))
def rank(A,p):
    A=[[norm(x,p) for x in row] for row in A];r=0
    for j in range(len(A[0]) if A else 0):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];v=A[r][j];iv=pow(int(v),-1,p) if p else 1/v
        A[r]=[norm(iv*x,p) for x in A[r]]
        for k in range(len(A)):
            if k!=r:
                v=A[k][j];A[k]=[norm(x-v*y,p) for x,y in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r

def simulate(P,Q,alpha,beta,V,p,mutant=None):
    k=len(P);nx=sum(len(A[0]) for A in P);ny=sum(len(A) for A in Q)
    n=2*nx+2*ny+2*V;I=eye(n);offset=0
    def bank(width):
        nonlocal offset
        answer=I[offset:offset+width];offset+=width;return answer
    x=[bank(len(A[0])) for A in P];b=[bank(len(A[0])) for A in P]
    y=[bank(len(A)) for A in Q];d=[bank(len(A)) for A in Q]
    ga=bank(V);gd=bank(V);need(offset==n,'all independent original inputs')
    b0=[[row[:] for row in B] for B in b]
    y0=[[row[:] for row in Y] for Y in y]
    source_cache=[mul(Pi,xi,p) for Pi,xi in zip(P,x)]
    R=[row[:] for row in gd]
    if mutant!='omit_preload':
        for Qi,di in zip(Q,d):R=add(R,mul(transpose(Qi),di,p),p)
    up=[]
    for s in range(k):
        up.extend([row[:] for row in R])
        if mutant=='reverse_read_after_subtraction':R=add(R,mul(transpose(Q[s]),d[s],p),p,-1)
        b[s]=add(b[s],mul(transpose(P[s]),R,p),p,-1)
        if mutant!='reverse_read_after_subtraction':R=add(R,mul(transpose(Q[s]),d[s],p),p,-1)
    up.extend([row[:] for row in R])
    for s in range(k):
        if mutant!='omit_Hub_compensation':b[s]=add(b[s],mul(transpose(P[s]),R,p),p)
        b[s]=add(b[s],mul(beta[s],R,p),p,-1)
    Fowner=[row[:] for row in ga]
    if mutant!='omit_forward_augmentation':
        for cache in source_cache:Fowner=add(Fowner,cache,p)
    down=[];output_cache=[None]*k
    for t in reversed(range(k)):
        down.extend([row[:] for row in Fowner])
        if mutant=='forward_capture_after_subtraction':Fowner=add(Fowner,source_cache[t],p,-1)
        output_cache[t]=[row[:] for row in Fowner]
        if mutant=='dirty_output_cache':output_cache[t]=add(output_cache[t],gd,p)
        if mutant not in ('forward_capture_after_subtraction','omit_source_shedding'):
            Fowner=add(Fowner,source_cache[t],p,-1)
    down.extend([row[:] for row in Fowner])
    for t in range(k):
        decoder=alpha[t] if mutant=='unchanged_mode_decoder' else add(alpha[t],Q[t],p,-1)
        y[t]=add(y[t],mul(decoder,Fowner,p),p)
        y[t]=add(y[t],mul(Q[t],output_cache[t],p),p)
    desired_y=[];desired_b=[]
    for t in range(k):
        row=add(y0[t],mul(alpha[t],ga,p),p)
        for s in range(t+1):row=add(row,mul(mul(Q[t],P[s],p),x[s],p),p)
        desired_y.append(row)
    for s in range(k):
        row=add(b0[s],mul(beta[s],gd,p),p,-1)
        for t in range(s,k):row=add(row,mul(transpose(mul(Q[t],P[s],p)),d[t],p),p,-1)
        desired_b.append(row)
    return {'correct':y==desired_y and b==desired_b and R==gd and Fowner==ga,
            'all_input_columns':n,'reverse_history_rank':rank(up,p),
            'forward_history_rank':rank(down,p),
            'expected_reverse_history_rank':V+sum(rank(A,p) for A in Q),
            'expected_forward_history_rank':V+sum(rank(A,p) for A in P)}

def main(args):
    rng=random.Random(14082026);cases=[]
    for p in (0,2,3,5,7):
        for k in (1,2,3,5):
            for V in (1,2,3):
                widths=[(1+s%2)*V for s in range(k)];heights=[(1+(s+1)%2)*V for s in range(k)]
                random_matrix=lambda n,m:[[rng.randrange(-2,3) for _ in range(m)] for _ in range(n)]
                P=[random_matrix(V,w) for w in widths];Q=[random_matrix(h,V) for h in heights]
                alpha=[random_matrix(h,V) for h in heights];beta=[random_matrix(w,V) for w in widths]
                if k==5:P[1]=zero(V,widths[1]);Q[3]=zero(heights[3],V)
                result=simulate(P,Q,alpha,beta,V,p)
                need(result['correct'],'exact chronological paired prefix identity')
                need(result['reverse_history_rank']==result['expected_reverse_history_rank'],'reverse changing histories are fully accounted')
                need(result['forward_history_rank']==result['expected_forward_history_rank'],'forward changing histories are fully accounted')
                cases.append({'field':'Q' if p==0 else p,'stations':k,'V':V,'singular_and_empty_stations':k==5,**result})
    P=[[[1,1]],[[1,-1]],[[1,2]]];Q=[[[1],[2]],[[2],[-1]],[[1],[1]]]
    alpha=[[[1],[0]],[[0],[1]],[[2],[1]]];beta=[[[1],[0]],[[0],[1]],[[1],[2]]]
    negative=[]
    for label in ['omit_preload','reverse_read_after_subtraction','omit_Hub_compensation','omit_forward_augmentation','forward_capture_after_subtraction','omit_source_shedding','unchanged_mode_decoder','dirty_output_cache']:
        need(not simulate(P,Q,alpha,beta,1,0,label)['correct'],'hypothesis-sensitive control '+label);negative.append(label)
    result={'status':'PASS_EXACT_PAIRED_PREFIX_SUFFIX_ALGEBRA','matrix_cases':len(cases),'cases':cases,'negative_controls':negative,
            'scope':'Finite exact tests on every input column, rectangular and singular maps, noncommuting blocks, arbitrary independent old mode payloads and actual changing boundary-history ranks. Universal source theorem is proved separately.'}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],len(cases),'cases',len(negative),'negative controls')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args())
