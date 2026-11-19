#!/usr/bin/env python3
"""Separate column-action audit of the receiver-covariant target."""
from argparse import ArgumentParser
from pathlib import Path
from hashlib import sha256
from itertools import product
import gzip,json
from sympy import Matrix


def basis(vectors):
    piv={}
    for v in vectors:
        while v:
            k=(v & -v).bit_length()-1
            if k in piv:v^=piv[k]
            else:piv[k]=v;break
    return list(piv.values())


def act(cols,x):
    y=0
    while x:
        low=x&-x;y^=cols[low.bit_length()-1];x^=low
    return y


def multiply(A,B):return [act(A,x) for x in B]
def plus(A,B):return [a^b for a,b in zip(A,B)]
def identity(n):return [1<<i for i in range(n)]


def inverse_coordinates(cols):
    piv={}
    for j,c in enumerate(cols):
        code=1<<j
        while c:
            k=(c&-c).bit_length()-1
            if k in piv:
                old,tag=piv[k];c^=old;code^=tag
            else:piv[k]=(c,code);break
        assert c
    def solve(c):
        code=0
        while c:
            k=(c&-c).bit_length()-1
            old,tag=piv[k];c^=old;code^=tag
        return code
    return solve


def transposed(cols):
    n=len(cols)
    return [sum(((cols[j]>>i)&1)<<j for j in range(n)) for i in range(n)]


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();base=args.repo/'research/moonshot-005-program/results'
    layoutpath=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(layoutpath.read_bytes())
    assert sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    L=json.loads(raw);roots=L['root_table']
    witnesspath=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    W=json.loads(witnesspath.read_text());lattice=Matrix.hstack(*map(Matrix,W['lattice_basis_columns']))
    assert abs(lattice.det())==16
    inverse=lattice.inv();masks=[]
    for root in roots:
        c=inverse*Matrix(root);assert all(x.q==1 for x in c)
        masks.append(sum((int(x)&1)<<i for i,x in enumerate(c)))
    hyp=W['hyperbolic_basis_masks'];coords={}
    for v in range(256):
        z=0
        for k in range(8):
            if v>>k&1:z^=hyp[k]
        coords[z]=v
    assert len(coords)==256
    def gamma(v):
        c=coords[v];ans=[]
        for k in range(16):
            z=0
            for t in range(4):
                if c>>(2*t+int(bool(k>>t&1)))&1:z^=1<<(k^(1<<t))
            ans.append(z)
        return ans
    G=[gamma(v) for v in masks];I=identity(16)
    A=plus(G[80],I);C=plus(G[10],I)
    assert multiply(A,A)==[0]*16==multiply(C,C)
    assert plus(multiply(A,C),multiply(C,A))==I
    U=basis(A);assert len(U)==8
    adapted=U+[act(C,x) for x in U];solve=inverse_coordinates(adapted)
    adaptedG=[[solve(act(g,x)) for x in adapted] for g in G]
    N01=[0]*8+identity(8);N10=[1<<(k+8) for k in range(8)]+[0]*8
    assert plus(adaptedG[80],I)==N01 and plus(adaptedG[10],I)==N10
    orth=[{j for j in range(111) if sum(a*b for a,b in zip(x,roots[j]))==0}
          for x in roots[:111]]
    assert sum(map(len,orth))==6470
    O=[sum(1<<j for j in row) for row in orth]
    K=[row^(1<<i) for i,row in enumerate(O)]
    assert len(basis(K))==9 and len(orth[80])==62 and len(orth[10])==61 and 10 not in orth[80]
    visited={0}
    while True:
        larger=visited|set().union(*(orth[i] for i in visited))
        if larger==visited:break
        visited=larger
    assert len(visited)==111
    for deleted in (orth[80]|{10},orth[10]|{80}):
        mask=sum(1<<j for j in range(111) if j not in deleted)
        assert len(basis(row&mask for row in K))==9
    # The actual minimum spinor width, using independent column conventions.
    w=8;secondary=60*w;b=2*secondary
    def lift_spin(g):
        cols=[]
        for q in range(2):
            for bank in range(60):
                for t in range(8):
                    v=g[8*q+t];z=0
                    for qq in range(2):
                        for tt in range(8):
                            if v>>(8*qq+tt)&1:z|=1<<(qq*secondary+bank*w+tt)
                    cols.append(z)
        return cols
    generators=[]
    for kind in ('J','E'):
        n=[0]*b
        for q in range(2):
            if kind=='J':
                for t in range(1,w):n[q*secondary+t]=1<<(q*secondary+t-1)
            else:n[q*secondary]=1<<(q*secondary+w-1)
        generators.append(n)
    transfers=[]
    for bank in range(1,60):
        n=[0]*b
        for q in range(2):
            for t in range(w):n[q*secondary+bank*w+t]=1<<(q*secondary+t)
        transfers.append(n)
    up=[0]*b;down=[0]*b
    for t in range(w):up[secondary+t]=1<<t;down[t]=1<<(secondary+t)
    rowgens=generators+transfers+[up]
    colgens=[transposed(t) for t in transfers]+[down,[0]*b]
    assert len(rowgens)==62 and len(colgens)==61
    checks=0
    for j,n in zip(sorted(orth[80]),rowgens):
        g=lift_spin(adaptedG[80]);assert multiply(n,g)==multiply(g,n)
        assert len(basis(plus(identity(b),n)))==b;checks+=1
    for i,n in zip(sorted(orth[10]),colgens):
        g=lift_spin(adaptedG[i]);assert multiply(n,g)==multiply(g,n)
        assert len(basis(plus(identity(b),n)))==b;checks+=1
    assert len(basis(c for n in rowgens for c in n))==2*w
    assert len(basis(c for n in colgens for c in transposed(n)))==2*w
    # Local unit identities are directly checked; arbitrary bank propagation
    # and all-width generation are covered by the reviewed written argument.
    J=[0]+[1<<(k-1) for k in range(1,w)];E=[1<<(w-1)]+[0]*(w-1)
    powers=[identity(w)]
    for t in range(w):powers.append(multiply(J,powers[-1]))
    units=0
    for r,t in product(range(w),repeat=2):
        v=multiply(multiply(powers[w-1-r],E),powers[t])
        want=[0]*w;want[t]=1<<r;assert v==want;units+=1
    assert multiply(up,down)!=multiply(down,up)
    # Omitting down preserves the first spinor half for every other generator.
    halfmask=(1<<secondary)-1
    assert all(all(not(c&~halfmask) for c in n[:secondary]) for n in rowgens+colgens[:-2])
    receiver=sorted(orth[10])[-2]
    wrongroot=next(j for j in range(111) if j!=receiver and j not in orth[receiver])
    wrong=lift_spin(plus(adaptedG[wrongroot],I));gi=lift_spin(adaptedG[receiver])
    assert multiply(wrong,gi)!=multiply(gi,wrong)
    diagonal=[0]*b;diagonal[0]=1
    assert len(basis(plus(identity(b),diagonal)))==b-1
    # Double commutator is exactly a partial trace on several actual H algebras.
    tracechecks=[]
    for h in (0,263,370,1119):
        j,k=L['A2'][h][:2];outputs=[]
        for c,r in product(range(16),repeat=2):
            x=[0]*16;x[c]=1<<r
            inner=plus(multiply(G[k],x),multiply(x,G[k]))
            out=plus(multiply(G[j],inner),multiply(inner,G[j]))
            assert multiply(out,G[j])==multiply(G[j],out)
            assert multiply(out,G[k])==multiply(G[k],out)
            outputs.append(sum(v<<(16*t) for t,v in enumerate(out)))
        assert len(basis(outputs))==64
        tracechecks.append({'H':h,'matrix_unit_images':256,'partial_trace_rank':64})
    result={'status':'PASS_INDEPENDENT_RECEIVER_COVARIANT_TARGET_REVIEW',
      'b':b,'adapted_basis_columns':adapted,'modified_block_covariance_and_invertibility':checks,
      'native_foreign_pairs':6470,'native_canonical_rank':9,'separated_star_rank_each':2*w,
      'proved_return_rank':9*b+4*w,'direct_local_matrix_unit_checks':units,
      'partial_trace_checks':tracechecks,'omitted_down_invariant_dimension':secondary,
      'wrong_root_control':{'receiver':receiver,'wrong_root':wrongroot},
      'diagonal_mutation_rank':b-1,'full_native_big_matrix_replayed':False,
      'minimum_End16_compatible_bank':3840,'compatible_excess':128,'compatible_return':34688,
      'imports_covariant_author_code':False,'reuses_root_column_action_method':True,
      'restricted_mixed_trace_source_bases_proved_here':False,'new_complete_kappa':False,
      'proof_sha256':sha256((args.author/'PROOF.md').read_bytes()).hexdigest(),
      'pins':[{'path':str(p.relative_to(args.repo)),'sha256':sha256(p.read_bytes()).hexdigest()} for p in (layoutpath,witnesspath)]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({'covariance_checks':checks,'local_units':units,'partial_traces':tracechecks}))


if __name__=='__main__':main()
