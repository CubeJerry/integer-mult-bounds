#!/usr/bin/env python3
from itertools import product
from pathlib import Path
from argparse import ArgumentParser
import json,sympy as sp
from sympy import QQ_I as E
from check import dm,block,matrix_action,swaporder,require


def run():
 points=list(product(range(2),repeat=4));eye=dm(sp.eye(16));zero=eye*E.zero;half=E(1,0)/E(2,0)
 sw=lambda i,j:matrix_action(points,lambda p:(swaporder(p,i,j),1));r=matrix_action(points,lambda p:((p[1],p[2],p[3],p[0]),(-1)**(p[0]*p[1]*p[3])))
 xb=matrix_action(points,lambda p:((p[0],p[1]^1,p[2],p[3]),1));a=(eye*E(1,1)+xb*E(1,-1))*half*r
 def case(I,Z,A,S,t0,t1,bench):
  Ai=dm(A.to_Matrix().H);P=(I+S)*half;N=I-P;L=block([[A,Z,Z],[I,A,Z],[Z,Z,I]]);U=block([[A,-A**2,Z],[Z,A,Z],[Z,Z,I]])
  C=block([[P,Z,-N],[P,I,-N],[N,Z,P]]);J=block([[I,Z,Z],[Z,I,Z],[t0,t1,I]]);O=block([[I,Z,Z],[I,I,Z],[Z,-I,I]]);Oi=block([[I,Z,Z],[-I,I,Z],[-I,I,I]])
  H=N*(I+t0);J0=P-N*t0;Eph=L*C*J*U;M=Oi*Eph
  require(block([[(t1-t0*P-N)*Ai+t1*Ai**2,-t1*Ai,P-t0*N]])*Eph==block([[Z,Z,I]]),'two-injection inverse row')
  require(block([[Z,P,Z]])*M==block([[P*A,Z,Z]]),'gauged row invariant')
  require((t0*P+N)*N==N and not N.is_zero_matrix,'quartic contradiction on minus eigenspace')
  Q=block([[I,t0,I],[Z,I,t1],[Z,Z,I]]);cols=[];n=I.shape[0]
  for j in range(3):
   p,z,w=(Q.extract(list(range(n*i,n*i+n)),list(range(n*j,n*j+n))) for i in range(3));v=t0*A*p+t1*A*z;x=P*A*p-N*v;u=A*p+S*v
   cols.append(block([[A*x-A*J0*A**2*z-A*N*w],[x+H*A**2*z-N*w],[u-S*t0*A**2*z+S*w]]))
  require(M*Q==cols[0].hstack(*cols[1:]),'all base input blocks')
  if bench:
   P2=Ai**2*P*A**2;Q0=block([[I,Z,Z],[Z,Z,I],[Z,I,Z]]);full=M*Q0*L
   corner=block([[-(I-t0)*A**3*P2],[N*(I+t0)*A**2],[-S*t0*A**2]])
   require(full.extract(list(range(3*n)),list(range(2*n,3*n)))==corner,'prefix-flip benchmark all 32 third-bank columns')
   require((-S*t0*A**2).rank()==n and ((I-t0)*A**3*P2).rank()==n//2,'benchmark ranks')
   plus=(I+t0)*half;minus=I-plus;out=block([[minus,plus,Z],[plus,minus,N*(I+t0)],[Z,Z,-S*t0]])
   output=O*out;endpoint=block([[A**3,Z,Z],[Z,A**2,Z],[Z,Z,A**2]]);inc=block([[I,Z,-(I-t0)*P2],[Z,I,Z],[Z,Z,I]])
   require((output*endpoint*inc).extract(list(range(3*n)),list(range(2*n,3*n)))==O*corner,'actual proposed endpoint third column')
   require(output.rank()==3*n and inc.rank()==3*n and output*endpoint*inc!=O*full,'other two columns fail in invertible completed units')
 for sign in [-1,1]:case(eye,zero,a,sw(2,3)*E(sign,0),sw(0,1)-eye,sw(1,3)+sw(0,2),False)
 I=block([[eye,zero],[zero,eye]]);Z=I*E.zero;A=block([[a,zero],[zero,a]]);S=block([[sw(2,3),zero],[zero,-sw(2,3)]]);flip=block([[zero,eye],[eye,zero]])
 require(S*flip==-flip*S,'genuine fixed sign flip');case(I,Z,A,S,flip,Z,True)
 return {'status':'PASS_INDEPENDENT_JOINT_SPECTATOR_ADDS','joint_noncommuting_singular_probes':2,'benchmark_prefix_sectors_simultaneous':True,'benchmark_columns':32,'benchmark_cubic_rank':16,'benchmark_quadratic_rank':32,'negative_controls':['positive N restriction prevents t0P+N=0','same real units fail full-column-set equality']}
if __name__=='__main__':
 p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run();a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
