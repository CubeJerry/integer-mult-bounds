#!/usr/bin/env python3
"""Independent rational rectangular-cell identities and birth/termination limits."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s

def need(b,m):
 if not b:raise ValueError(m)
def columns(vs,n):return s.Matrix.hstack(*vs) if vs else s.zeros(n,0)
def main(a):
 need(hashlib.sha256(a.proof.read_bytes()).hexdigest()=='ded1bb828379cd5a589003bde38650bc110c6941e1e9f7b7c1a42da8417e270f','frozen proper-birth proof')
 cases=[s.Matrix([[1,1],[2,2],[0,0]]),s.Matrix([[0],[1]]),s.zeros(2,0),s.Matrix([[1,0,1,1],[0,1,1,2],[1,1,0,1],[2,1,1,3],[0,2,1,3],[3,0,2,2]]),s.zeros(4,4)]
 receipts=[]
 for M in cases:
  b,n=M.shape;_,piv=M.rref();r=len(piv);W=s.eye(n)[:,list(piv)] if piv else s.zeros(n,0);K=columns(M.nullspace(),n);nu=n-r;I=s.eye(n)
  V=W.row_join(K);need(V.det()!=0,'domain complement');Vi=V.inv();images=M*W;out=[images[:,j] for j in range(r)]
  for j in range(b):
   candidate=out+[s.eye(b)[:,j]]
   if columns(candidate,b).rank()>len(out):out=candidate
  O=columns(out,b);need(O.shape==(b,b) and O.det()!=0,'range complement');Oi=O.inv();R=W*Oi[:r,:];J=K;h=Vi[r:,:]
  need(R*M==I-J*h and M*J==s.zeros(b,nu) and h*J==s.eye(nu) and h*R==s.zeros(nu,b),'all rectangular inverse identities')
  N=s.Matrix(b,2,lambda i,j:(i+1)*(j+1));Pout=N.row_join(M);U=s.eye(n+2)[:2,:];Pin=s.eye(n+2)[2:,:]
  need(R*(Pout-N*U)+J*h*Pin==Pin,'full symbolic X/Y/input reconstruction')
  projection=s.eye(b)-M*R;need(projection*(Pout-N*U)==s.zeros(b,n+2),'actual image condition')
  need(projection*N[:,1]!=s.zeros(b,1) if r==0 and b else True,'birth-only independent Y cannot be dropped')
  if r<b:need(projection*O[:,r]!=s.zeros(b,1),'nonimage birth direction rejected')
  if nu:need(R*M*J==s.zeros(n,nu) and J!=s.zeros(n,nu),'kernel coordinate cannot be omitted')
  receipts.append({'shape':[b,n],'rank':r,'kernel_dimension':nu,'all_symbolic_columns':n+2})
 need(receipts[1]['kernel_dimension']==0,'newborn retains old packet despite zero old through diagonal')
 need(receipts[2]['kernel_dimension']==0,'birth-only cell has no incoming kernel coordinate')
 out=dict(status='PASS_INDEPENDENT_RATIONAL_PROPER_BIRTH_REVIEW',author_proof_sha256=hashlib.sha256(a.proof.read_bytes()).hexdigest(),author_code_imported=False,field_for_computational_controls='Q with exact symbolic matrices',cells=receipts,universal_proof='Independently reviewed complement decomposition and spatial induction; finite checks do not prove universal quantifiers.',scope='Descenders end at ground. Proper early terminations and direction reversals require separately stated normalization and actual route invoice.',new_kappa=None)
 a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'cells':len(cases)}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
