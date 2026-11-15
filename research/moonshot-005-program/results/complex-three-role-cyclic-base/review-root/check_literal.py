#!/usr/bin/env python3
"""Independent Laurent identities and coset-coordinate certificate."""
from pathlib import Path
import json
import sympy as s

a=s.symbols('a', nonzero=True)
K=s.Matrix([[1,0,a-1],[a,0,-a],[1,1,-1]])
Ki=s.Matrix([[a**-1,a**-1-a**-2,0],[0,-a**-1,1],[a**-1,-a**-2,0]])
B=s.Matrix([[a,a-2+a**-1,a-1],[a,0,-a],[a,a-1+a**-1,-1]])
def zero(M):return all(s.expand(v)==0 for v in M)
assert zero(K*Ki-s.eye(3)) and zero(Ki*K-s.eye(3))
assert zero(Ki*s.diag(a**3,a**2,a**2)*Ki-B)
assert K[:,1]==s.Matrix([0,0,1])
# Coefficients of the distinct nonordinary right coset spans aO and a^-1 O.
C=s.Matrix([[1,0,-1],[1,1,0],[0,1,0]])
assert C.det()==-1
u,v,w=s.symbols('u v w')
assert C*s.Matrix([u,v,w])==s.Matrix([u-w,u+v,v])
# When a^2=-I, distinct-coset premise fails and (0,I,0) has ordinary image.
col=B[:,1].xreplace({a**-1:-a})
assert col==s.Matrix([-2,0,-1])
out={'status':'PASS_ROOT_LITERAL_TWO_INTERSTAGE_GATE','universal_laurent_identities':True,'coefficient_constraint_determinant':-1,'ordinary_second_column_of_K':True,'negative_control_ordinary_square_merges_cosets':True,'scope':'Formal identity and three-coset proof certificate; inherited faithful phase and actual a-square premises retained; arbitrary endpoint gauges outside scope','new_complete_kappa':False}
Path(__file__).with_name('LITERAL-RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
