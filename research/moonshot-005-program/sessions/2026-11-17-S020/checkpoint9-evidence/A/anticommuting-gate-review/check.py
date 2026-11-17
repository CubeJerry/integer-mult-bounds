#!/usr/bin/env python3
"""Independent exact tensor-word review. Uses Sympy; imports no author engine."""
import argparse
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = 'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SOURCE_SHA = '1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
AUTHOR_PINS = {'check.py':'617349eba96f5a48e0df608a7ba281409fadd68582f43a930a1a5c5b60ebdeca', 'PROOF.md':'f15b8d8d7d77fac78df5e19cd88d2941214feafdd187f08d19ddb40f994da213', 'RESULT.json':'bc2bb4eef88292995177aa345bba63d662a70f1b8fb6ccd4e7ed49ec0789f45c'}

def clean(a):
    return s.ImmutableMatrix(a.applyfunc(s.expand))

@lru_cache(None)
def mm(a,b):
    return clean(a*b)

def table(n, dest, phase):
    a=s.zeros(2**n)
    for x in range(2**n):
        bits=[(x>>k)&1 for k in range(n)]
        a[dest(*bits),x]=s.I**(phase(*bits)%4)
    return s.ImmutableMatrix(a)

I4=s.ImmutableMatrix(s.eye(4)); I16=s.ImmutableMatrix(s.eye(16)); Z4=s.ImmutableMatrix(s.zeros(4))

# A dictionary is the literal expression sum_h coefficient[h] tensor h^(tensor W).
# Matrices are multiplied before grouping identical tail words. No linear
# dependence of physical width-one matrices is used to merge distinct words.
def term(c,h=I16):
    c=clean(c)
    return {} if c==Z4 else {h:c}

def add(*aa):
    out={}
    for a in aa:
        for h,c in a.items():
            out[h]=clean(out.get(h,Z4)+c)
    return {h:c for h,c in out.items() if c!=Z4}

def scale(a,q):
    return {h:clean(q*c) for h,c in a.items() if q!=0}

def mul(*aa):
    out=term(I4)
    for a in aa:
        nxt={}
        for h,c in out.items():
            for k,d in a.items():
                hk=mm(h,k); cd=mm(c,d)
                nxt[hk]=clean(nxt.get(hk,Z4)+cd)
        out={h:c for h,c in nxt.items() if c!=Z4}
    return out

one=term(I4)
def bmul(a,b):
    return [[add(*(mul(a[i][k],b[k][j]) for k in range(3))) for j in range(3)] for i in range(3)]

def padd(*aa):
    degrees=set().union(*(set(a) for a in aa))
    return {d:add(*(a.get(d,{}) for a in aa)) for d in degrees}

def pmul(a,b):
    out={}
    for d,x in a.items():
        for e,y in b.items():
            out[d+e]=add(out.get(d+e,{}),mul(x,y))
    return out

def pbmul(a,b):
    return [[padd(*(pmul(a[i][k],b[k][j]) for k in range(3))) for j in range(len(b[0]))] for i in range(3)]

def rot(i,j,h):
    out=[[one if a==b else {} for b in range(3)] for a in range(3)]
    ph=scale(add(one,h),s.Rational(1,2)); nh=scale(add(one,scale(h,-1)),s.Rational(1,2))
    out[i][i]=out[j][j]=ph; out[i][j]=scale(nh,-1); out[j][i]=nh
    return out

def support(a):
    return sorted(set(sum(x!=0 for x in a.row(i)) for i in range(a.rows)))

def run(repo,author,out):
    assert hashlib.sha256((repo/SOURCE).read_bytes()).hexdigest()==SOURCE_SHA
    for name,sha in AUTHOR_PINS.items():
        assert hashlib.sha256((author/name).read_bytes()).hexdigest()==sha
    rr=table(4,lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
    xb=table(4,lambda a,b,c,d:a+2*(b^1)+4*c+8*d,lambda *x:0)
    a0=mm(clean(((1+s.I)*I16+(1-s.I)*xb)/2),rr)
    r2=table(4,lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
    s2=table(4,lambda a,b,c,d:b+2*a+4*c+8*d,lambda *x:0)
    s1=table(4,lambda a,b,c,d:d+2*b+4*c+8*a,lambda *x:0)
    ss=table(4,lambda a,b,c,d:a+2*b+4*d+8*c,lambda *x:0)
    j0=mm(mm(r2.adjoint(),s2),r2); k0=mm(mm(mm(a0,j0),ss),a0.adjoint())
    assert mm(a0.adjoint(),a0)==I16 and mm(k0.adjoint(),k0)==I16
    assert support(k0)==[1] and set(k0)-{0}<={1,-1,s.I,-s.I}
    assert mm(a0,j0)==mm(mm(k0,a0),ss)
    assert mm(mm(a0.adjoint(),ss),a0)==s1
    u=mm(a0,a0)
    assert mm(mm(u.adjoint(),ss),u)==s2 and mm(u,s2)==mm(ss,u)
    zs=table(2,lambda x,t:x+2*t,lambda x,t:2*x)
    tt=table(2,lambda x,t:x+2*t,lambda x,t:2*t)
    rrpre=table(2,lambda x,t:x+2*(t^1),lambda *x:0)
    S=term(zs,ss); S1=term(zs,s1); S2=term(zs,s2)
    T=term(tt); R=term(rrpre); A=term(I4,a0); J=term(I4,j0)
    P=scale(add(one,T),s.Rational(1,2)); N=add(one,scale(P,-1))
    U=scale(add(one,R),s.Rational(1,2)); V=add(one,scale(U,-1))
    H=scale(add(T,R),(1+s.I)/2)
    p=scale(mul(U,add(one,scale(S2,-1))),s.Rational(1,2))
    z=scale(mul(R,H,U,add(one,S2)),s.Rational(1,2)); w=V
    diag=[[one,{},{}],[{},J,{}],[{},{},one]]
    C=bmul(bmul(bmul(diag,rot(0,2,T)),rot(1,2,R)),rot(0,1,S))
    # Reconstruct from the literal native quadratic paths, retaining the paths
    # that must cancel before any simplification or tail-coset merging.
    c00,c01=C[0][0],C[0][1]; c10,c11=C[1][0],C[1][1]
    c20=C[2][0]
    assert mul(c00,A,A,z)=={} and mul(c10,A,A,z)=={}
    assert mul(c20,A,A,z)==mul(A,A,z)
    assert mul(C[0][2],w)=={} and mul(C[2][2],w)=={}
    f2=[add(mul(A,c00,A,p),mul(A,c01,A,z)),
        add(mul(A,c10,A,p),scale(mul(c00,A,A,z),-1),mul(A,c11,A,z)),
        scale(mul(c20,A,A,z),-1)]
    # Independent extraction from the entire native L Cprime U last column.
    L=[[{1:A},{},{}],[{0:one},{1:A},{}],[{},{},{0:one}]]
    UN=[[{1:A},{2:scale(mul(A,A),-1)},{}],[{},{1:A},{}],[{},{},{0:one}]]
    Cp=[[{0:x} for x in row] for row in C]
    last=pbmul(pbmul(pbmul(L,Cp),UN),[[{0:p}],[{0:z}],[{0:w}]])
    assert [r[0].get(2,{}) for r in last]==f2
    assert all(not r[0].get(d,{}) for r in last for d in [0,3])
    assert all(support(h)==[2**d] for r in last for d in [1,2] for h in r[0].get(d,{}))
    words=[u,mm(u,s2),mm(u,s1),mm(mm(u,s1),s2)]
    assert len(set(words))==4
    coeff=[]
    for r,row in enumerate(f2):
        ww=[mm(k0,h) if r==1 else h for h in words]
        assert set(row)<=set(ww), ('unexpected literal word',r,len(row))
        coeff.append([row.get(h,Z4) for h in ww])
    blocks=[[clean(row[0]+row[1]),row[2],row[3]] for row in coeff]
    envelope=s.BlockMatrix(blocks).as_explicit()
    assert all(c[i,j]==0 for row in blocks for c in row for i in range(4) for j in range(4) if i%2!=j%2)
    controls=[]
    heads=[words[0],words[2],words[3]]
    assert all(support(h)==[4] for h in heads)
    for i,j in itertools.combinations(range(3),2):
        relative=mm(heads[i],heads[j].adjoint())
        assert support(relative)==[4]
        controls.append({'heads':[i,j],'relative_row_nonzeros':4,'not_projectively_monomial':True})
    sectors=[]
    for sign,ix,rows,want in [(1,[0,2],[0,1,5],s.I/64),(-1,[1,3],[0,1,2],(1+s.I)/128)]:
        mat=s.BlockMatrix([[b.extract(ix,ix) for b in row] for row in blocks]).as_explicit()
        assert all(mat[:,2*j]==mat[:,2*j+1] for j in range(3))
        minor=mat.extract(rows,[0,2,4]); value=s.expand(minor.det())
        assert value==want and mat.rank()==3
        sectors.append({'sigma_sign':sign,'rank':3,'rows':rows,'columns':[0,2,4],'determinant':str(value),'minor':[[str(minor[i,j]) for j in range(3)] for i in range(3)]})
    assert envelope.rank()==6
    author_result=json.loads((author/'RESULT.json').read_text())
    assert author_result['exact_coset_envelope_rank']==6 and author_result['ordinary_quadratic_encoder_capacity']==4
    result={'status':'PASS_INDEPENDENT_FIXED_COLUMN_ENVELOPE_REVIEW','author_proof_accepted_with_stated_scope':True,
      'method':'Independent Sympy exact tensor-word algebra; literal rotation product; no author imports; no width-one linear-dependence merging',
      'full_native_source_degree_extraction':True,'ordinary_and_cubic_terms_cancel_as_tensor_words':True,
      'literal_quadratic_word_counts':[len(x) for x in f2],'quadratic_coefficients':[[[[str(c[i,j]) for j in range(4)] for i in range(4)] for c in row] for row in coeff],
      'coset_controls':controls,'sectors':sectors,'prefix_dimension':4,'envelope_rank':6,'actual_endpoint_projector_capacity':4,
      'source_sha256':SOURCE_SHA,'author_pins':AUTHOR_PINS,
      'scope':'Specified cancelling last column, and its invertible ordinary right basis changes; fixed finite prefix-matrix/collective root-four tail catalogue, uniform arbitrarily large W divisible by four. No arbitrary-column or universal Cprime exclusion.',
      'new_kappa':False,'source_word_invalidated':False}
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'], 'exact rank 6 > ordinary encoder capacity 4')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,default=HERE/'output');args=ap.parse_args();run(args.repo,args.author,args.out)
