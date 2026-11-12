#!/usr/bin/env python3
"""Exact source tight-frame and full-rank correction identity."""
import json
from pathlib import Path
from fractions import Fraction as F
p=Path(__file__).resolve().parent;c=json.loads((p/'CERTIFICATE.json').read_text());A=c['rows'];n=len(A)
def need(x,s):
    if not x:raise ValueError(s)
AtA=[[sum(row[i]*row[j] for row in A) for j in range(8)] for i in range(8)];need(AtA==[[104*int(i==j) for j in range(8)] for i in range(8)],'104I tight-frame identity')
G=[[sum(x*y for x,y in zip(a,b)) for b in A] for a in A]
# C=G/8-I, and C^-1=G/96-I because G^2=104G.
C=[[F(G[i][j],8)-int(i==j) for j in range(n)] for i in range(n)];Inv=[[F(G[i][j],96)-int(i==j) for j in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):need(sum(C[i][k]*Inv[k][j] for k in range(n))==int(i==j),'literal correction inverse')
out={'status':'PASS_FULL_RANK_CORRECTION_OPERATOR','source_sha256':c['source_sha256'],'transpose_gram_diagonal':104,'transpose_gram_offdiagonal':0,'packet_gram_rank':8,'correction_operator':'C=AA^T/8-I','correction_rank':104,'exact_inverse':'C^-1=AA^T/96-I','eigenvalues':{'12':8,'-1':96},'determinant':'12^8','scope':'Algebraic aggregate dimension only; no104-call lower bound when receivers already have side information. The inverse is not claimed as a dyadic implementation.','new_complete_kappa':None};(p/'CORRECTION-RANK.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
