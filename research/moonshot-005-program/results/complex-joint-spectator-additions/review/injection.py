#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import json
import sympy as sp
from sympy import QQ_I as E
from check import dm,block,matrix_action,swaporder,require


def run():
 pts=list(product(range(2),repeat=4));I=dm(sp.eye(16));Z=I*E.zero;half=E(1,0)/E(2,0)
 sw=lambda x,y:matrix_action(pts,lambda p:(swaporder(p,x,y),1));r=matrix_action(pts,lambda v:((v[1],v[2],v[3],v[0]),(-1)**(v[0]*v[1]*v[3])))
 xb=matrix_action(pts,lambda v:((v[0],v[1]^1,v[2],v[3]),1));a=(I*E(1,1)+xb*E(1,-1))*half*r;ai=dm(a.to_Matrix().H);s=sw(2,3);s2=sw(0,1)
 L=block([[a,Z,Z],[I,a,Z],[Z,Z,I]]);U=block([[a,-a**2,Z],[Z,a,Z],[Z,Z,I]])
 Oi=block([[I,Z,Z],[-I,I,Z],[-I,I,I]])
 seen=Counter();m=a.to_Matrix()
 for j,k in combinations(range(16),2):
  cpair=tuple(i for i in range(4) if pts[j][i]!=pts[k][i])==(2,)
  for phase in [1,sp.I,-1,-sp.I]:
   vec=m[:,j]+m[:,k]*phase;supp=[r for r in range(16) if sp.expand(vec[r])!=0]
   require(len(supp)<=2 if cpair else len(supp)==4,'source pair collapse criterion')
   if len(supp)==2:
    f,g=(pts[i] for i in supp);require(tuple(i for i in range(4) if f[i]!=g[i])==(1,),'output b pair')
   seen[('c' if cpair else 'other')+str(len(supp))]+=1
 Q=block([[I,s,sw(0,3)],[Z,I,sw(1,2)],[Z,Z,I]]);cases=[]
 for sign in (-1,1):
  S=s*E(sign,0);P=(I+S)*half;N=I-P;P2=(I+s2*E(sign,0))*half;N2=I-P2
  C=block([[P,Z,-N],[P,I,-N],[N,Z,P]])
  for name,t in [('zero',Z),('permutation',sw(0,2)),('singular noncommuting',(I-sw(0,1))*sw(1,3))]:
   K=block([[I,Z,Z],[Z,I,Z],[Z,t,I]]);Ephys=L*C*K*U;M=Oi*Ephys
   require(block([[(t-N)*ai+t*ai**2,-t*ai,P]])*Ephys==block([[Z,Z,I]]),'inverse row times physical matrix')
   require(block([[-I,I,I]])*Ephys==block([[a,S*t*a,S]]),'physical forward probe')
   require(block([[Z,P,Z]])*M==block([[P*a,Z,Z]]),'gauged left probe')
   cols=[]
   for j in range(3):
    coeff=lambda i:Q.extract(list(range(16*i,16*i+16)),list(range(16*j,16*j+16)))
    p,z,w=(coeff(i) for i in range(3));x=P*a*p-N*t*a*z;u=a*p+S*t*a*z;y=P2*z;z2=N2*z
    cols.append(block([[a*x-a**3*y-a*N*w],[x+a**2*z2-N*w],[u+S*w]]))
   require(M*Q==cols[0].hstack(*cols[1:]),'all D columns')
   if name.startswith('singular'):
    require(0<t.rank()<16 and a*t!=t*a,'genuinely singular and noncommuting')
    require(block([[(t-N)*ai,-t*ai,P]])*Ephys!=block([[Z,Z,I]]),'omitted inverse-quadratic term')
   cases.append([sign,name,t.rank()])
 return {'status':'PASS_INDEPENDENT_SINGLE_INJECTION','coupled_case_ranks':cases,'relative_fourth_root_phase_pair_checks':dict(sorted(seen.items())),
         'negative_controls':['singular noncommuting t','omitted inverse-quadratic term rejects','non-c source pair has four outputs even after relative phase']}
if __name__=='__main__':
 p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run();a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
