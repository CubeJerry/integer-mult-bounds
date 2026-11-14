#!/usr/bin/env python3
"""Independent full-word differentiation of the three-half padding control."""
import argparse, hashlib, itertools, json
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
pa=argparse.ArgumentParser();pa.add_argument('--author',type=Path,default=HERE/'source');pa.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=pa.parse_args()
pins={'PROOF.md':'41d8bce94bd0998e5dce43c9667ad24d55e809fa91f68fb30037666df4f135d1','MANIFEST.json':'ced1c9319c04bb9ebcdcbcb23a4e4a155193abc32e99dd6a5d75988486b3e486'}
for n,h in pins.items():
 if hashlib.sha256((a.author/n).read_bytes()).hexdigest()!=h:raise ValueError('pin '+n)
def need(x,m):
 if not x:raise ValueError(m)
def red(M):return M.applyfunc(s.cancel)
def E(i,j,c):
 M=s.eye(4);M[i,j]=c;return M
p,u,w=s.symbols('p u w',nonzero=True);d=s.symbols('d1 d2 d3')
B=s.Matrix([[0,0,1,0],[1,0,0,1],[0,1,1,0],[0,0,0,1]])
T2=E(2,0,-1);T3=E(3,1,-1);K=E(2,3,-p);J=E(0,2,-1)
expected=[s.Matrix([[1,0,0,p*(1-w)],[0,u,(u-1)/p,0],[0,0,1,0],[0,0,0,w]]),s.Matrix([[1,0,0,p*(1-w)],[0,1,0,0],[u-1,0,u,p*(u-1)],[0,0,0,w]]),s.Matrix([[u,0,u-1,p*(u-1)],[0,w,0,0],[0,p*(1-w),1,0],[0,w-1,0,1]])]
active=[(0,1),(1,2),(2,3)];idle=[(2,3),(0,3),(0,1)]
allD=[]
for k in range(3):
 D=[s.eye(4) for _ in range(3)];vals=[0]*4
 for r in active[k]:vals[r]=1
 vals[idle[k][0]]=u;vals[idle[k][1]]=w
 D[k]=s.diag(*[1+(d[k]-1)*z for z in vals])
 F=K*J*T3.inv()*D[2]*E(2,3,p)*T3*T2.inv()*D[1]*E(1,2,1/p)*T2*D[0]*E(0,1,p)*B
 F0=red(F.subs({z:1 for z in d}));need(F0==s.diag(p,1/p,1,1),'complete head word')
 Pi=red(F.diff(d[k]).subs({z:1 for z in d})*F0.inv());need(red(Pi-expected[k])==s.zeros(4),'independent derivative')
 allD.append(Pi)
accepted=[];witnesses=[]
for bits in itertools.product((0,1),repeat=6):
 P=[M.subs({u:bits[2*k],w:bits[2*k+1]}) for k,M in enumerate(allD)]
 diffs=[red(M.subs(p,1)-M.subs(p,-1)) for M in P]
 if all(M==s.zeros(4) for M in diffs):accepted.append(list(bits))
 else:
  k=next(k for k,M in enumerate(diffs)if M!=s.zeros(4));i,j=next((i,j)for i in range(4)for j in range(4)if diffs[k][i,j]);witnesses.append({'bits':list(bits),'stage':k+1,'entry':[i,j],'difference':str(diffs[k][i,j])})
need(accepted==[[1]*6] and len(witnesses)==63,'complete padding classification')
z=s.Matrix(s.symbols('a b c e'));v=B*z
v=d[0]*E(0,1,p)*v
v=T2.inv()*(d[1]*E(1,2,1/p)*(T2*v))
v=T3.inv()*(d[2]*E(2,3,p)*(T3*v))
v=red(K*J*v);need(red(v-d[0]*d[1]*d[2]*s.diag(p,1/p,1,1)*z)==s.zeros(4,1),'four independent endpoints')
r={'status':'PASS_INDEPENDENT_COMPLETE_WORD_DERIVATIVES','proof_pins':pins,'all_three_closed_projectors_rederived':True,'accepted':accepted,'rejected_witnesses':witnesses,'arbitrary_original_inputs_checked':4,'no_author_verifier_import':True,'scope':'Formal common-P/even ordinary role algebra with legitimate p=plusminus1 evaluations only; actual physical matching is unproved.','new_kappa':False,'sympy_version':s.__version__}
a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':r['status'],'accepted':accepted,'rejected':len(witnesses)}))
