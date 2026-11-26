"""Lift the published F16 Pascal word to an unramified ring modulo four."""
from functools import cache, reduce
from itertools import product, combinations
from pathlib import Path
import runpy
import json

gf=runpy.run_path(str(Path(__file__).with_name('verify-fibre-join.py')))
def red(x): return sum(((x >> (2*i))&1)<<i for i in range(4))
def lift(x): return sum(((x>>i)&1)<<(2*i) for i in range(4))
@cache
def add(x,y):
    return sum(((((x>>(2*i))&3)+((y>>(2*i))&3))%4)<<(2*i) for i in range(4))
@cache
def mul(x,y):
    v=[0]*7
    for i in range(4):
        for j in range(4): v[i+j]+=((x>>(2*i))&3)*((y>>(2*j))&3)
    for i in (6,5,4):
        v[i-4]-=v[i]
        v[i-3]-=v[i]
    return sum((v[i]%4)<<(2*i) for i in range(4))
def power(x,m):
    out=1
    while m:
        if m&1: out=mul(out,x)
        x=mul(x,x); m//=2
    return out
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def diag(v): return [[x if i==j else 0 for j in range(len(v))] for i,x in enumerate(v)]
def mm(A,B):
    return [[reduce(add,(mul(x,y) for x,y in zip(row,col)),0) for col in zip(*B)] for row in A]
def inverse(A):
    n=len(A); aug=[r+s for r,s in zip(A,eye(n))]
    for j in range(n):
        i=next(i for i in range(j,n) if red(aug[i][j]))
        aug[i],aug[j]=aug[j],aug[i]; u=power(aug[j][j],29)
        aug[j]=[mul(u,v) for v in aug[j]]
        for i in range(n):
            if i!=j:
                scale=mul(3,aug[i][j])
                aug[i]=[add(v,mul(scale,w)) for v,w in zip(aug[i],aug[j])]
    assert [r[:n] for r in aug]==eye(n)
    return [r[n:] for r in aug]
def embed(A,indices):
    M=eye(4)
    for i,u in enumerate(indices):
        for j,v in enumerate(indices): M[u][v]=A[i][j]
    return M
def prodm(word,n):
    A=eye(n)
    for B in word: A=mm(A,B)
    return A
def mapped(f,M): return [[f(x) for x in r] for r in M]
def flat(M): return [x for r in M for x in r]

w=next(x for x in range(256) if red(x)==6 and add(add(power(x,2),x),1)==0)
D=[[power(w,i*j) for j in range(3)] for i in range(3)]
J=[[1,0,0],[0,0,1],[0,1,0]]
rev=list(reversed(eye(4)))
ds=[[1,2,7],[1,5,6],[1,5,5]]
# Numerical factors from Jain, MobiusLean/Word.lean at 00ffede3d650d434ebba869cafab4d334edc6d4d.
factors=[
    ([[0,0,12],[0,4,0],[15,0,0]],ds[::-1],[[0,6,0],[0,0,1],[1,0,0]],(0,1,2)),
    ([[0,15,0],[2,0,0],[0,0,15]],ds,diag([1,12,10]),(0,2,3)),
    ([[0,15,0],[13,0,0],[0,0,15]],ds,diag([1,10,10]),(1,2,3))]
def naive_word():
    word=[rev]
    for M,entries,N,indices in factors:
        block=[mapped(lift,M)]
        for j in range(4):
            block.extend([D,diag([1,w,w]),D,J])
            if j<3: block.append(mapped(lift,diag(entries[j])))
        block.append(mapped(lift,N))
        word.extend(embed(A,indices) for A in block)
    return prodm(word+[rev],4)
def fm(x,y): return gf['mul'](x,y,0b10011)
def finv(x): return gf['power'](x,14,0b10011)
def basis_conjugates():
    pivots={}; basis=[]
    for triple in combinations(range(4),3):
        for shifts in product((1,w,power(w,2)),repeat=3):
            B=mm(embed(diag(shifts),triple),embed(D,triple)); C=inverse(B)
            idx=triple[0]
            mat=[[red(mul(B[i][idx],C[idx][j])) for j in range(4)] for i in range(4)]
            v=flat(mat)
            for k,h in sorted(pivots.items()):
                t=v[k]; v=[x^fm(t,y) for x,y in zip(v,h)]
            if not any(v): continue
            k=next(i for i,x in enumerate(v) if x); a=finv(v[k])
            pivots[k]=[fm(a,x) for x in v];basis.append((B,C,idx,flat(mat)))
            if len(basis)==16: return basis
    raise AssertionError('conjugates failed to span')
def solve(A,t):
    rows=[list(row)+[v] for row,v in zip(zip(*A),t)]
    for j in range(16):
        k=next(k for k in range(j,16) if rows[k][j])
        rows[k],rows[j]=rows[j],rows[k]; v=finv(rows[j][j])
        rows[j]=[fm(v,x) for x in rows[j]]
        for k in range(16):
            if k!=j:
                v=rows[k][j]; rows[k]=[x^fm(v,y) for x,y in zip(rows[k],rows[j])]
    return [r[-1] for r in rows]
def main():
    V=naive_word(); U=[[int((i&j)==i) for j in range(4)] for i in range(4)]
    assert mapped(red,V)==U
    A=mm(U,inverse(V)); I=eye(4); target=[]
    for i in range(4):
        for j in range(4):
            h=add(A[i][j],3*I[i][j]); assert red(h)==0
            target.append(red(h>>1))
    basis=basis_conjugates()
    coeffs=solve([g[-1] for g in basis],target); factors=[]
    for (B,C,k,_),t in zip(basis,coeffs):
        z=[1]*4; z[k]=add(1,mul(2,lift(t)))
        factors.append(prodm([B,diag(z),C],4))
    assert mm(prodm(factors,4),V)==U and V!=U
    print(json.dumps(dict(modulus_four_ring='(Z/4)[x]/(x^4+x+1)',cube_root=w,
                     Fourier_letters_before_correction=24,conjugate_basis_rank=len(basis),
                     correction_scalars_GF16=coeffs,naive_wrong_entries=sum(x!=y for x,y in zip(flat(V),flat(U))),
                     all_sixteen_ring_entries_exact=True),indent=2))
if __name__=='__main__': main()
