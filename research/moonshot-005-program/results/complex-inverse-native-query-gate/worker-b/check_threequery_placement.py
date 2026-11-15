#!/usr/bin/env python3
"""Exact finite controls for the complementary-corner argument."""
import json
from pathlib import Path
import sympy as S
I=S.eye(2);O=S.zeros(2);P=S.diag(1,0);Q=I-P
X=S.Matrix([[0,1],[1,0]]);J=S.Matrix([[1,1],[0,1]])
def block(a,b,c,d):return a.row_join(b).col_join(c.row_join(d))
checks=0
for K in (I,X,J):
 for U0 in (O,P,Q,J):
  for V0 in (O,P,Q,X):
   U=U0.col_join(I);V=V0.row_join(I);B=U*V;A=block(K,O,O,O);W=A+B
   assert B.rank()==2 and W.rank()==4
   assert W[2:4,2:4].det()!=0
   checks+=1
# If the rank cap is discarded, the zero opposite corner is compatible with invertibility.
W=block(O,I,I,O);A=S.zeros(4);B=W
assert W.rank()==4 and B.rank()==4 and W[2:4,2:4]==O
# If invertibility is discarded, rank-cap and zero-corner hypotheses can coexist.
B=block(I,O,O,O);W=B
assert B.rank()==2 and W.rank()==2 and W[2:4,2:4]==O
out={'status':'PASS_COMPLEMENTARY_CORNER_CONTROLS','exact_rank_d_examples':checks,'field_dimension':2,'zero_divisors_in_ordinary_blocks':True,'negative_controls':{'removing_rank_cap_allows_invertible_zero_corner':True,'removing_independence_allows_rank_d_zero_corner':True},'proof':'THREE-QUERY-PLACEMENT-GATE.md','scope':'finite controls of linear-algebra implication; universal caller proof is written separately','new_kappa':False}
Path(__file__).with_name('THREE-QUERY-PLACEMENT-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
