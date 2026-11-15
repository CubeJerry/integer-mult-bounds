#!/usr/bin/env python3
"""Exact finite geometry and negative controls for the dihedral shadow.

No exploratory search module or cached orbit classification is imported.
"""
import argparse, hashlib, importlib.util, itertools, json, sys, time
from collections import Counter
from pathlib import Path
import sympy as s

ID=tuple(1<<i for i in range(6))
def app(A,v):
    z=0
    for j,c in enumerate(A):
        if (v>>j)&1:z^=c
    return z
def mul(A,B):return tuple(app(A,c) for c in B)
def gf_rank(vs):
    piv={}
    for v in vs:
        while v:
            j=v.bit_length()-1
            if j not in piv:piv[j]=v;break
            v^=piv[j]
    return len(piv)
def span(bs):
    ans={0}
    for b in bs:ans|={x^b for x in tuple(ans)}
    return tuple(sorted(ans))
def tr(A):return tuple(sum(((A[j]>>i)&1)<<j for j in range(3)) for i in range(3))
def inv3(A):return tuple(next(v for v in range(8) if app(A,v)==1<<i) for i in range(3))
def omega(v,w):return (((v&7)&(w>>3)).bit_count()+((w&7)&(v>>3)).bit_count())%2
def symplectic(A):return all(omega(A[i],A[j])==omega(1<<i,1<<j) for i,j in itertools.product(range(6),repeat=2))
def distance(i,j,n=6):return min((i-j)%n,(j-i)%n)
def perm_matrix(p):
    M=s.zeros(len(p))
    for j,i in enumerate(p):M[i,j]=1
    return M

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path(__file__).parent/'RESULT.json');ar=ap.parse_args();base=Path(__file__).parent;start=time.monotonic()
    dep=json.loads((base/'DEPENDENCIES.json').read_text())
    for d in dep['sources']:assert hashlib.sha256((ar.repo/d['path']).read_bytes()).hexdigest()==d['sha256']
    hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
    sp=importlib.util.spec_from_file_location('shadow_actual_source',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
    I=m.eye(8);Xb=m.monomial([j^2 for j in range(8)],[0]*8)
    Cb=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm();S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=Cb@S
    paulis={}
    for x,z in itertools.product(range(8),repeat=2):paulis[x|(z<<3)]=m.monomial([j^x for j in range(8)],[2*((j&z).bit_count()%2) for j in range(8)])
    cols=[]
    for j in range(6):
        P=A@paulis[1<<j]@A.star()
        matches=[v for v,Q in paulis.items() if any(P==Q.scale(c) for c in ((1,0),(-1,0),(0,1),(0,-1)))]
        assert len(matches)==1;cols.append(matches[0])
    a=tuple(cols);assert symplectic(a)
    powers=[ID]
    for _ in range(6):powers.append(mul(a,powers[-1]))
    assert powers[6]==ID
    ranks=[gf_rank([v&7 for v in p[3:]]) for p in powers[:6]]
    assert ranks==[0,1,2,3,2,1]
    lag=[span(p[3:]) for p in powers[:6]];assert len(set(lag))==6
    for i,j in itertools.product(range(6),repeat=2):
        inter=len(set(lag[i])&set(lag[j]));assert 3-(inter.bit_length()-1)==distance(i,j)
    # Enumerate every partial cycle map fixing zero, not merely those from H.
    partial_encodings=0;partial_maps=set()
    for choices in itertools.product((None,0,1),repeat=5):
        f={0:0}
        for j,c in enumerate(choices,1):
            if c is not None:f[j]=j if c==0 else (-j)%6
        if len(set(f.values()))!=len(f):continue
        if any(distance(i,j)!=distance(fi,fj) for i,fi in f.items() for j,fj in f.items()):continue
        assert any(all(fj==(eps*j)%6 for j,fj in f.items()) for eps in (1,-1))
        partial_encodings+=1;partial_maps.add(tuple(sorted(f.items())))
    assert partial_encodings==93 and len(partial_maps)==62
    bad={0:0,1:1,2:4};assert distance(1,2)!=distance(bad[1],bad[2])
    H=set()
    for B in itertools.product(range(1,8),repeat=3):
        if gf_rank(B)!=3:continue
        Bit=tr(inv3(B))
        for bits in range(64):
            q=[(bits>>i)&1 for i in range(6)]
            C=(q[0]|(q[3]<<1)|(q[4]<<2),q[3]|(q[1]<<1)|(q[5]<<2),q[4]|(q[5]<<1)|(q[2]<<2))
            h=tuple(app(B,1<<i)|(app(C,app(B,1<<i))<<3) for i in range(3))+tuple(v<<3 for v in Bit)
            assert symplectic(h);H.add(h)
    assert len(H)==10752
    choices={};partial_census=Counter()
    for h in H:
        f={}
        for j,L in enumerate(lag):
            image=tuple(sorted(app(h,v) for v in L))
            if image in lag:f[j]=lag.index(image)
        epss=[e for e in (1,-1) if all(fj==(e*j)%6 for j,fj in f.items())]
        assert epss;choices[h]=epss[0];partial_census[len(f),tuple(epss)]+=1
    # Entire cyclic-double-coset cover meeting H: well-defined T and covariance.
    remain=set(H);orbits=0;basis_elements=0;ordinary_count=0;orbit_census=Counter()
    while remain:
        h=min(remain);eps=choices[h];e=0 if eps==1 else 1;table={}
        for u,v in itertools.product(range(6),repeat=2):
            g=mul(mul(powers[u],h),powers[v]);value=((u+eps*v)%6,e)
            if g in table:assert table[g]==value
            else:table[g]=value
        hs=set(table)&H;assert hs
        for g,(k,ee) in table.items():
            assert table[mul(a,g)]==((k+1)%6,ee)
            assert table[mul(g,a)]==((k+eps)%6,ee)
            if g in H:assert k==0
        remain.difference_update(hs);orbits+=1;basis_elements+=len(table);ordinary_count+=len(hs);orbit_census[len(table),len(hs),eps]+=1
    assert ordinary_count==10752
    # Auxiliary dihedral representation: the reflection shift matters.
    X=perm_matrix([(j+1)%6 for j in range(6)])
    T=perm_matrix([(2-j)%6 for j in range(6)])
    P=s.diag(1,1,1,-1,-1,-1)
    assert X**6==s.eye(6) and T*T==s.eye(6) and T*X*T==X.inv()
    assert T*P==P*T
    geometric=perm_matrix([(-j)%6 for j in range(6)])
    assert geometric*P!=P*geometric
    deltas=[]
    for k in range(6):
        d=(X**k-P*X**k*P).rank();assert d==2*distance(0,k);deltas.append(d)
    Y=P*X*P;Z=s.zeros(6);II=s.eye(6)
    native=[]
    for name,cross0,cross1 in [('L',II,II),('U',-X**2,-Y**2)]:
        N=s.BlockMatrix([[X,cross0],[Z,X]]).as_explicit();M=s.BlockMatrix([[Y,cross1],[Z,Y]]).as_explicit()
        assert (N-M).rank()==4 and (N.inv()-M.inv()).rank()==4
        native.append({'orientation':name,'forward_difference_rank':4,'inverse_difference_rank':4})
    assert sum(deltas[k] for k in (3,2,2))==14>12
    # A shadow's augmentation may be a unit before its other character is.
    Rp=s.eye(2);Rm=s.diag(1,0)
    assert (Rp+Rm).det()!=0 and (Rp-Rm).det()==0
    lam=2;assert (Rp+lam*Rm).det()!=0 and (Rp-lam*Rm).det()!=0
    # A nontrivial physical central character cannot be discarded at that width.
    assert s.I!=1 and s.I**4==1
    out={'status':'PASS_EXACT_TWO_INTERSTAGE_DIHEDRAL_SHADOW_CONTROLS',
         'proof_sha256':hashlib.sha256((base/'PROOF.md').read_bytes()).hexdigest(),
         'actual_source_symplectic_columns':list(a),'source_cycle_gaussian_ranks':ranks,
         'partial_cycle_encodings_checked':partial_encodings,
         'distinct_partial_cycle_maps_checked':len(partial_maps),'ordinary_stabilizer_elements':len(H),
         'partial_cycle_census':[{'domain_size':k[0],'allowed_orientations':k[1],'count':v} for k,v in sorted(partial_census.items())],
         'cyclic_double_cosets_meeting_ordinary':orbits,'covered_group_basis_elements':basis_elements,
         'ordinary_basis_elements_covered_once':ordinary_count,'bimodule_covariance_checked':True,
         'dihedral_power_difference_ranks':deltas,'native_difference_checks':native,
         'unit_deformation_negative_and_positive_controls':True,
         'negative_controls':['wrong reflection fails sign-potential agreement','nonisometric partial map rejected','augmentation alone need not make both ordinary character blocks units','nontrivial central phase cannot be quotiented before a compatible width is chosen'],
         'scope':'Finite geometry diagnostics plus universal written group-algebra proof. This does not construct a caller, justify arbitrary ordinary endpoint gauges, or improve kappa.'}
    ar.out.parent.mkdir(parents=True,exist_ok=True);ar.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));print(json.dumps({'verification_elapsed_seconds':time.monotonic()-start}))

if __name__=='__main__':main()
