#!/usr/bin/env python3
"""Independent exact replay of SP's physical invariant sectors.

Uses SymPy on the actual one-special-letter permutation representation.
Does not import the author's checker and does not test a tape runtime.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

def permutation_matrix(p):
    n=len(p)
    a=sp.zeros(n,n)
    for i,j in enumerate(p):
        a[j,i]=1
    return a

def star(m,j):
    p=list(range(m+1))
    p[0],p[j]=p[j],p[0]
    return permutation_matrix(p)

def standard_coordinates(m):
    # Column 0 is all-ones; columns 1..m are e_j-e_0.
    columns=[sp.ones(m+1,1)]
    for j in range(1,m+1):
        v=sp.zeros(m+1,1)
        v[j],v[0]=1,-1
        columns.append(v)
    return sp.Matrix.hstack(*columns)

def main():
    counts={"physical_orbit_actions":0,"exact_mixed_products":0,
            "positive_sector_spectra":0,"seed_kernel_blocks":0,
            "address_phase_scope_controls":0,
            "field_kernel_blocks":0,"field_fixed_line_cases":0,
            "excluded_characteristic_controls":0}
    for m in range(2,8):
        n=m+1
        b=standard_coordinates(m)
        bi=b.inv()
        one=sp.ones(n,1)
        stars=[star(m,j) for j in range(1,n)]
        sm=sum(stars,sp.zeros(n,n))
        assert sm*one==m*one
        assert sm.eigenvals()=={sp.Integer(m):1,sp.Integer(m-1):m-1,sp.Integer(-1):1}
        counts["positive_sector_spectra"]+=1
        # Actual complete alphabet of four pair symbols, restricted to the
        # orbit with one distinguished symbol. No abstract oracle substitution.
        words=[tuple(1 if j==i else 0 for j in range(n)) for i in range(n)]
        for j,pj in enumerate(stars,1):
            for i,w in enumerate(words):
                out=list(w)
                out[0],out[j]=out[j],out[0]
                target=words.index(tuple(out))
                assert pj[target,i]==1
                counts["physical_orbit_actions"]+=1
        # The actual binary phase at the center breaks the trivial sector.
        phase=sp.diag(-1,*([1]*m))
        assert len(set(phase*one))==2
        assert any((bi*phase*b)[i,0]!=0 for i in range(1,n))
        counts["address_phase_scope_controls"]+=1

        # Dense, full-rank and singular row operations with changing controlled
        # permutations, expressed on the unabridged n-dimensional orbit.
        for rows in (1,2,3):
            full=sp.eye(rows*n)
            for stage in range(3):
                mixer=sp.Matrix(rows,rows,lambda i,j:
                    (stage+1)*(i+1)-2*j+(1 if i==j else 0))
                if stage==2 and rows==3:
                    mixer[rows-1,:]=sp.zeros(1,rows)
                controls=[stars[(r+stage)%m] for r in range(rows)]
                full=sp.diag(*controls)*sp.kronecker_product(mixer,sp.eye(n))*full
            change=sp.kronecker_product(sp.eye(rows),b)
            restricted=change.inv()*full*change
            triv=[r*n for r in range(rows)]
            std=[r*n+j for r in range(rows) for j in range(1,n)]
            assert restricted.extract(triv,std)==sp.zeros(rows,rows*m)
            assert restricted.extract(std,triv)==sp.zeros(rows*m,rows)
            o0=restricted.extract(triv,triv)
            o1=restricted.extract(std,std)
            assert o1.det()**2==o0.det()**(2*m)
            counts["exact_mixed_products"]+=1

    for r in range(2,6):
        m=2**r-1
        primes=(2,3,5,7,11,31)
        for p in primes:
            fixed_line_determinant=(m*pow(-1,m,p))%p
            assert bool(fixed_line_determinant)==bool(m%p)
            if m%p:
                counts["field_fixed_line_cases"]+=1
            else:
                counts["excluded_characteristic_controls"]+=1
        for t in range(1,2**r):
            signs=[-1 if (j&t).bit_count()%2 else 1 for j in range(1,m+1)]
            assert sum(signs)==-1
            neg=[i+1 for i,b in enumerate(signs) if b==-1]
            assert len(neg)-1==(m-1)//2
            # Direct action on every basis vector of this kernel:
            # negative leaf differences, not a determinant of an inferred block.
            for j in neg[:-1]:
                v=[0]*(m+1)
                v[j],v[neg[-1]]=1,-1
                image=[sum(s*v[i+1] for i,s in enumerate(signs))]
                image.extend(s*v[0]+(-1-s)*v[i+1] for i,s in enumerate(signs))
                assert not any(image)
            counts["seed_kernel_blocks"]+=1
            for p in primes:
                if m%p==0:
                    continue
                v=[0]*(m+1)
                v[neg[0]],v[neg[-1]]=1,-1
                assert any(z%p for z in v)
                image=[0]*(m+1)
                for j,s in enumerate(signs,1):
                    moved=v[:]
                    moved[0],moved[j]=moved[j],moved[0]
                    image=[(a+s*b)%p for a,b in zip(image,moved)]
                assert not any(image)
                counts["field_kernel_blocks"]+=1
        h=sp.Rational(m*(m-1),2)
        d=m*(m+1)
        assert h/d>=sp.Rational(1,4)
        assert 1/(sp.Integer(16)*(sp.Rational(3,2)*m)**3)==sp.Rational(1,54*m**3)

    here=Path(__file__).resolve().parent
    proof=here.parent/"route-a"/"square-product-star-obstruction.md"
    result={"status":"pass","implementation":"independent SymPy exact matrices",
            "counts":counts,
            "proof_sha256":hashlib.sha256(proof.read_bytes()).hexdigest(),
            "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "scope":"Finite algebra and sector applicability; no operator-norm sampling, tape execution or formalization."}
    (here/"square-product-independent-verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
