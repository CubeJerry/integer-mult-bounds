#!/usr/bin/env python3
"""Independent exact negative control; not a supplier or a universal search."""
import json
from pathlib import Path
import sympy as s

def perm(n, f):
    return s.SparseMatrix(n,n,{(f(j),j):1 for j in range(n)})
def tensor(a,v):
    z=s.eye(1)
    for _ in range(v): z=s.kronecker_product(z,a)
    return s.SparseMatrix(z)
def swap(j,a,b):
    return j ^ (((j>>a ^ j>>b)&1)*((1<<a)|(1<<b)))
def block(a,b,c,d): return a.row_join(b).col_join(c.row_join(d))

I=s.eye(8)
X={a:perm(8,lambda j,a=a:j^(1<<a)) for a in range(3)}
Z={a:s.diag(*[(-1)**((j>>a)&1) for j in range(8)]) for a in range(3)}
S=perm(8,lambda j:((j&1)<<2)|((j&2)>>1)|((j&4)>>1))
A=((1+s.I)*I+(1-s.I)*X[1])*S/2
assert A*Z[0]==Z[2]*A and A*Z[1]==Z[0]*A
assert A**2*Z[1]==Z[2]*A**2
rows=[]
for v in (1,2):
    d=8**v; ident=s.eye(d); zero=s.zeros(d)
    a=tensor(A,v); a2=a*a
    ebp=(ident+tensor(Z[1],v))/2; ebm=ident-ebp
    ecp=(ident+tensor(Z[2],v))/2; ecm=ident-ecp
    # Only the first physical column is flipped. This is valid at even v.
    first_a=s.kronecker_product(X[0],s.eye(8**(v-1)))
    first_c=s.kronecker_product(X[2],s.eye(8**(v-1)))
    hp=first_a*tensor(perm(8,lambda j:swap(j,0,1)),v)
    h=first_c*tensor(perm(8,lambda j:swap(j,0,2)),v)
    ol=block(ecp,ecm*h,ecm,ecp*h)
    ore=block(hp*ebp,hp*ebm,ebm,ebp)
    native=block(a,-a2,zero,a)
    out=ol*native*ore
    assert ol*ol.H==s.eye(2*d) and ore.H*ore==s.eye(2*d)
    assert out[:d,:d]==zero and out[d:,d:]==zero
    assert ebm.rank()==d//2
    # Omitting the required sign flip destroys the zero-corner identity.
    bad_hp=tensor(perm(8,lambda j:swap(j,0,1)),v)
    bad=ecp*a*bad_hp*ebp-ecp*a2*ebm+ecm*h*a*ebm
    assert bad!=zero
    rows.append({'width':v,'field_dimension':d,'ordinary_boundaries_unitary':True,
                 'both_diagonal_corners_zero':True,'k2_rank':d//2,
                 'omitted_flip_rejected':True})
result={'status':'PASS_EXACT_MARKED_PROJECTOR_NEGATIVE_CONTROL',
        'widths':rows,'all_width_statement':'proved separately by Pauli conjugation',
        'interpretation':'A zero native compression can have nonzero unimodular boundaries. Its singular k2 cannot satisfy the full-rank pure-E3 endpoint requirement.',
        'new_kappa':False}
Path(__file__).with_name('PROJECTOR-CONTROL.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
