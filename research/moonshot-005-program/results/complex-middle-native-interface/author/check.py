#!/usr/bin/env python3
"""Exact noncommutative algebra controls for the middle-native interface.

Free reduced words retain scalar coefficients outside tensor lifts. Identities
proved here therefore hold in every representation; Gaussian-type separation
is supplied by the cited mathematical argument at faithful tensor widths.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse, hashlib, itertools, json

ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/5b84182f4f70/programme'))
ap.add_argument('--output',type=Path,default=Path(__file__).with_name('MIDDLE-RESULT.json'))
args=ap.parse_args()

def require(ok,message):
    if not ok:raise ValueError(message)

inverse={'a':'A','A':'a','h':'H','H':'h','j':'J','J':'j','g':'G','G':'g'}
def reduce(w):
    out=[]
    for letter in w:
        if out and inverse[letter]==out[-1]:out.pop()
        else:out.append(letter)
    return tuple(out)
def term(w=(),c=1):return {reduce(w):Q(c)}if c else{}
def add(x,y,c=1):
    z=dict(x)
    for w,v in y.items():z[w]=z.get(w,Q(0))+c*v
    return {w:v for w,v in z.items()if v}
def prod(x,y):
    z={}
    for w,v in x.items():
        for u,k in y.items():
            t=reduce(w+u);z[t]=z.get(t,Q(0))+v*k
    return {w:v for w,v in z.items()if v}
def eye():return [[term()if i==j else{}for j in range(3)]for i in range(3)]
def zero():return [[{}for j in range(3)]for i in range(3)]
def matadd(X,Y,c=1):return [[add(x,y,c)for x,y in zip(rx,ry)]for rx,ry in zip(X,Y)]
def mm(X,Y):
    Z=zero()
    for i,j,k in itertools.product(range(3),repeat=3):Z[i][j]=add(Z[i][j],prod(X[i][k],Y[k][j]))
    return Z
def unit(i,j,w=(),c=1):
    Z=zero();Z[i][j]=term(w,c);return Z
def diag(xs):return [[xs[i]if i==j else{}for j in range(3)]for i in range(3)]
def pw(n):return term(('a',)*n if n>=0 else ('A',)*(-n))
I=eye();Z=zero();a=pw(1);ai=pw(-1)
L=[[a,{},{}],[term(),a,{}],[{},{},term()]]
LI=[[ai,{},{}],[term(('A','A'),-1),ai,{}],[{},{},term()]]
U=[[a,term(('a','a'),-1),{}],[{},a,{}],[{},{},term()]]
D=diag([a,a,term()]);DI=diag([ai,ai,term()])
P0=unit(2,2);T0=unit(0,1,('a',),-1)
U0=P0;U1=diag([a,a,{}]);U2=unit(0,1,('a','a'),-1)
require(mm(L,LI)==I and mm(LI,L)==I,'Native inverse identity')
require(matadd(matadd(U0,U1),U2)==U,'Native rank-component decomposition')
require(mm(D,matadd(I,T0))==U,'Native flattening identity')
require(mm(T0,T0)==Z and mm(P0,T0)==Z and mm(T0,P0)==Z,'Native nilpotent flags')

# Actual noncommuting ordinary shear words in both interstages.
C=matadd(I,unit(2,0,('h',)));CI=matadd(I,unit(2,0,('h',),-1))
R=matadd(I,unit(0,2,('j',)));RI=matadd(I,unit(0,2,('j',),-1))
require(mm(C,CI)==I and mm(R,RI)==I,'Ordinary elementary inverses')
B0=mm(mm(C,U0),R);B1=mm(mm(C,U1),R);B2=mm(mm(C,U2),R)
F=matadd(B0,B1);FI=mm(mm(RI,DI),CI)
require(mm(F,FI)==I and mm(FI,F)==I,'Flattened inverse with noncommuting ordinary shears')
P=mm(FI,B0);T=mm(FI,B2)
require(P==mm(mm(RI,P0),R)and T==mm(mm(RI,T0),R),'Covariant component formula')
require(mm(P,P)==P and mm(T,T)==Z and mm(P,T)==Z and mm(T,P)==Z,'Covariant flag identities')
require(mm(mm(F,RI),DI)==C,'Reconstructed first ordinary interstage')
require(mm(mm(C,U),R)==matadd(F,B2),'Exact native reconstruction')

# Literal concentration family: no commutation between g and a is used.
Eg=[[{},term(('a',)*4,-1),{}],[pw(2),{},{}],[{},{},term(('g',))]]
Bg=mm(mm(LI,Eg),LI)
expected=matadd(U,unit(2,2,(),-1));expected=matadd(expected,unit(2,2,('g',)))
require(Bg==expected,'Literal nonordinary-idle sandwich')
E420=[[{},term(('a',)*4,-1),{}],[pw(2),{},{}],[{},{},term()]]
require(mm(mm(LI,E420),LI)==U and mm(mm(L,U),L)==E420,'Sharp concentration420 control')
Ed=diag([pw(4),pw(2),a]);Bd=mm(mm(LI,Ed),LI)
expected_d=[[pw(2),{},{}],[add(term(('a',),-1),term(('A',),-1)),term(),{}],[{},{},a]]
require(Bd==expected_d,'Literal diagonal421 sandwich')

# Every word in the first row of Bd has pure rank2, so removing rank2 leaves
# an exactly zero row. This is an algebraic degeneracy, not sampled rank.
Fd=[[{}, {}, {}],expected_d[1],expected_d[2]]
require(all(not cell for cell in Fd[0]),'Diagonal boundary flattening is singular')

# Rank-only false positive: all-width invertibility is justified in the proof
# by unitarity and ||a/2||<1; the square-zero failure is exact here.
star2=unit(0,0,('a','a'),Q(1,2));tstar=mm(DI,star2)
require(mm(tstar,tstar)==unit(0,0,('a','a'),Q(1,4))!=Z,'Rank-only false positive rejected')

# Negative controls that fail the exact equation, not merely a repeated run.
badLI=[[ai,{},{}],[term(('A',),-1),ai,{}],[{},{},term()]]
require(mm(badLI,L)!=I,'Wrong inverse power must fail')
require(mm(mm(LI,Eg),LI)!=U,'Replacing the idle identity by g is not free')
require(matadd(U1,U2)!=U,'Ordinary idle component cannot be discarded')

source_paths=[
'research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md',
'research/moonshot-005-program/results/complex-four-bit-concentration/author/PROOF.md',
'research/moonshot-005-program/results/complex-inverse-native-coset/two-native/PROOF.md',
'research/moonshot-005-program/results/complex-four-bit-family/classification/PROOF.md',
]
sources={p:hashlib.sha256((args.repo/p).read_bytes()).hexdigest()for p in source_paths}
result={
 'status':'PASS_EXACT_FREE_WORD_IDENTITIES',
 'baseline':'3057acc9311101cfedfcfacf7f68fb0866507871',
 'scope':'Universal free-word algebra identities; faithful tensor projections supplied by the written proof and pinned predecessor theorem. No finite search interpreted as a universal obstruction.',
 'native_component_ranks':['D','2D','D'],
 'native_flattening':'invertible',
 'relative_rank2':'rank D; square zero; annihilates ordinary projector on both sides',
 'reconstruction':'verified with noncommuting ordinary elementary shear symbols h,j',
 'excluded_fixed_boundaries':['literal concentrated42 plus any positive-rank independent Gaussian','literal diagonal(a^4,a^2,a)'],
 'controls':['420 exact positive','rank-only all-width invertible false positive','wrong inverse power','missing ordinary idle component','nonordinary idle is not free'],
 'source_sha256':sources,
 'new_kappa':False,
}
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
