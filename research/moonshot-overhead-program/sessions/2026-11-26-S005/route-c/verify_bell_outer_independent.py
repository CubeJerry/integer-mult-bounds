#!/usr/bin/env python3
"""Independent integer-numerator checks of Bell product/diagonal boundaries."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

def character(x,y): return 1-2*((x&y).bit_count()&1)
def transform(values):
    return [sum(character(i,j)*z for j,z in enumerate(values))
            for i in range(len(values))]
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    a,b=x
    c,d=y
    return (a*c-b*d,a*d+b*c-b*d)
def conj(x): return (x[0]-x[1],-x[1])

def main():
    counts={"product_coordinates":0,"diagonal_coordinates":0,
            "pointwise_rejection_controls":0,"cyclotomic_unitarity_controls":0,
            "endpoint_invoice_cases":0}
    for s in range(7):
        q=1<<s
        for seed in range(3):
            for u in range(q):
                fv=[(3*z+5*(z^u)+seed*z*(z^u)+seed)%11-5 for z in range(q)]
                gv=[(7*z+2*(z^u)+(seed+1)*z*(z^u)+2*seed)%13-6 for z in range(q)]
                dv=[(5*z+7*(z^u)+seed*z*(z^u)+1)%17-8 for z in range(q)]
                hv=[(3*v+seed*v*v+u)%19-9 for v in range(q)]
                ff,gg=transform(fv),transform(gv)
                pp=transform([a*b for a,b in zip(fv,gv)])
                kk=transform(dv)
                physical_h=transform(hv)
                actual_d=transform([d*h for d,h in zip(dv,physical_h)])
                for v in range(q):
                    assert q*pp[v]==sum(ff[w]*gg[v^w] for w in range(q))
                    assert actual_d[v]==sum(kk[w]*hv[v^w] for w in range(q))
                    counts["product_coordinates"]+=1
                    counts["diagonal_coordinates"]+=1
    assert [a*b for a,b in zip(transform([1,0]),transform([0,1]))]!=[0,0]
    counts["pointwise_rejection_controls"]+=1
    # Q(omega), omega^2+omega+1=0, represented literally as a+b*omega.
    alpha=(F(0),F(-1,2))
    beta=(F(1),F(1,2))
    assert alpha!=(0,0) and beta!=(0,0)
    assert add(mul(alpha,conj(alpha)),mul(beta,conj(beta)))==(1,0)
    assert add(mul(alpha,conj(beta)),mul(beta,conj(alpha)))==(0,0)
    counts["cyclotomic_unitarity_controls"]+=1
    for h in range(11):
        a=2*(1<<h)
        leaf=1<<h
        assert leaf==a//2
        bounded_bill=2*leaf-1
        assert a//2<=bounded_bill<=a
        linear_toll_bill=a*h+leaf
        assert linear_toll_bill==sum(a for _ in range(h))+leaf
        counts["endpoint_invoice_cases"]+=1
    here=Path(__file__).resolve().parent
    proof=here.parent/"route-b"/"bell-outer-boundary.md"
    report={"status":"pass","counts":counts,
            "proof_sha256":hashlib.sha256(proof.read_bytes()).hexdigest(),
            "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "scope":"Exact Bell boundary identities and the defined endpoint bill; no physical lower bound or new convolution algorithm."}
    (here/"bell-outer-independent-verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__": main()

