#!/usr/bin/env python3
"""Separate exact SymPy source identities; universal coefficient proof separate."""
import json
from pathlib import Path
import sympy as s

def perm(n,f):return s.SparseMatrix(n,n,{(f(j),j):1 for j in range(n)})
def block(a,b,c,d):return a.row_join(b).col_join(c.row_join(d))
def tensor(a,v):
    z=s.eye(1)
    for _ in range(v):z=s.kronecker_product(z,a)
    return z
I=s.eye(8);xb=perm(8,lambda j:j^2)
cycle=perm(8,lambda j:((j&1)<<2)|((j&2)>>1)|((j&4)>>1))
A=((1+s.I)*I+(1-s.I)*xb)*cycle/2
P=s.diag(*[s.I**((j>>2)&1)for j in range(8)])
G=A.H*A.H;H=A.H*P*A.H;K=s.simplify(G.H*H);J=s.simplify(G*K.H)
assert K==s.simplify(A*P*A.H) and J==s.simplify(A.H*P.H*A.H)
def column_supports(m):return sorted(set(sum(s.simplify(m[i,j])!=0 for i in range(m.rows))for j in range(m.cols)))
assert [column_supports(x)for x in [G,H,K,J]]==[[4],[4],[2],[4]]
checks=[]
for v in [1,2]:
    a=tensor(A,v);p=tensor(P,v);g=tensor(G,v);h=tensor(H,v);d=8**v;i=s.eye(d);z=s.zeros(d)
    source=block(a.H,i,z,a.H);ordinary=block(i,p,z,i);query=block(a.H,z,z,i)
    assert s.simplify(query*ordinary*source-block(g,a.H+h,z,a.H))==s.zeros(2*d)
    checks.append({'width':v,'exact_first_query_identity':True,'full_input_roles':2})
# The claimed obstruction disappears without the ordinary phase twist.
assert s.simplify(G.H*G)==I
assert G.row_join(G)==G*I.row_join(I)
result={'status':'PASS_ROOT_INDEPENDENT_ROW_SEED','column_supports_G_H_K_J':[4,4,2,4],'corresponding_head_ranks':[2,2,1,2],'widths':checks,'negative_control_P_identity_admits_ordinary_factorization':True,'interpretation':'Finite exact identities plus separate faithful-algebra proof; no compiled caller or new kappa.'}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
