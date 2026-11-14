#!/usr/bin/env python3
"""Independent rational occurrence-cell and repeated-boundary controls."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
def need(b,m):
 if not b:raise ValueError(m)
def cols(vs,n):return s.Matrix.hstack(*vs) if vs else s.zeros(n,0)
def main(a):
 pin='4a354728308afa0d6f6926f5c64cfc8f7e13640ad9e54fb3930ebeba9de2c0a6'
 need(hashlib.sha256(a.proof.read_bytes()).hexdigest()==pin,'frozen universal route proof')
 A=s.Matrix([[1,1],[0,1]]);B=s.Matrix([[1,0],[1,1]]);P=s.diag(1,0)
 need(A*B!=B*A,'genuine noncommuting blocks')
 loop=P.row_join(s.zeros(2,2)).col_join((B*A).row_join(B))
 cases=[('proper_termination',s.zeros(0,4)),('two_inputs_one_exit',A.row_join(B)),('same_lifetime_repeated_boundary',loop),('turn_birth_only',s.zeros(2,0)),('new_output_retains_old_input',s.zeros(2,2).col_join(A))]
 receipts=[];controls=[]
 for name,M in cases:
  b,n=M.shape;r=M.rank();nu=n-r
  # Domain and image complements use exact rational column spaces, independently
  # of the author's binary row-reduction implementation.
  _,piv=M.rref();W=s.eye(n)[:,list(piv)] if piv else s.zeros(n,0)
  J=cols(M.nullspace(),n);D=W.row_join(J);need(D.det()!=0,'domain direct sum');Di=D.inv()
  image=[(M*W)[:,j] for j in range(r)]
  for j in range(b):
   trial=image+[s.eye(b)[:,j]]
   if cols(trial,b).rank()>len(image):image=trial
  C=cols(image,b);need(C.shape==(b,b) and C.det()!=0,'image complement');R=W*C.inv()[:r,:];h=Di[r:,:]
  need(R*M==s.eye(n)-J*h and M*J==s.zeros(b,nu),'rectangular reconstruction')
  need(h*J==s.eye(nu) and h*R==s.zeros(nu,b),'normalized kernel')
  N=s.Matrix(b,3,lambda i,j:(i+1)**(j+1));U=s.eye(n+3)[:3,:];Pin=s.eye(n+3)[3:,:]
  Pout=N*U+M*Pin;T=h*Pin
  need(R*(Pout-N*U)+J*T==Pin,'all symbolic history columns')
  need((s.eye(b)-M*R)*(Pout-N*U)==s.zeros(b,n+3),'actual image constraints')
  if nu:
   need(J*T!=s.zeros(n,n+3),'discarded kernel changes actual histories');controls.append(name+':omitted_kernel_rejected')
  if b-r:
   q=C[:,r];need((s.eye(b)-M*R)*q!=s.zeros(b,1),'nonimage birth rejected');controls.append(name+':free_birth_rejected')
  receipts.append(dict(name=name,shape=[b,n],rank=r,kernel_dimension=nu,symbolic_columns=n+3))
 # A single physical owned record travels Hub->ground->Hub->ground. Its actual
 # input rows are x0 then x1, and arbitrary Y rows survive in two receivers.
 V=2;I=s.eye(8);x0=I[:2,:];x1=I[2:4,:];y0=I[4:6,:];y1=I[6:,:]
 G=x0.col_join(x1);actual=[x0,x1,y0+x0,y1+x1]
 need(G.rank()==2*V,'two visits really carry independent modes')
 need((y0+x0).col_join(x1).col_join(y0).col_join(y1).rank()>x1.col_join(y0).col_join(y1).rank(),'last-arrival-only control')
 need((y1+x1).col_join(x0).col_join(y0).col_join(y1).rank()>x0.col_join(y0).col_join(y1).rank(),'first-arrival-only control')
 need((y0+x0).col_join(G).rank()>G.rank(),'unknown Y cannot be silently omitted')
 controls+=['collapse_ground_occurrences_to_first_rejected','collapse_ground_occurrences_to_last_rejected','arbitrary_Y_erasure_rejected']
 out=dict(status='PASS_INDEPENDENT_RATIONAL_OWNED_ROUTE_CELLS',proof_sha256=pin,author_code_imported=False,field='Q; exact symbolic independent columns',cells=receipts,negative_controls=controls,repeated_ground_example=dict(width=V,one_owned_lifetime=True,downward_occurrences=2,history_x_rank=2*V),universal_review='Reviewed occurrence-indexed rectangular cells, spatial induction, facet-MOVE injectivity and target-wide normalized monotonicity separately. Finite controls do not supply universal quantifiers.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(status=out['status'],cells=len(cases),controls=len(controls))))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
