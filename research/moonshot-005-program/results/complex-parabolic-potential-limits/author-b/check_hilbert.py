#!/usr/bin/env python3
"""Independently check Worker C's radial Hilbert identity from B's complete spaces."""
from pathlib import Path
import argparse,json

def apply(cols,v):
 ans=0
 for j in range(6):
  if v&(1<<j):ans^=cols[j]
 return ans
ap=argparse.ArgumentParser();ap.add_argument('--spaces',default='LAGRANGIANS.json');ap.add_argument('--out',default='HILBERT-RESULT.json');a=ap.parse_args()
s=json.loads(Path(a.spaces).read_text());Ls=[tuple(L) for L in s['lagrangians']];idx={L:i for i,L in enumerate(Ls)};ds=s['distance'];Ns=[]
for g in s['rank_representatives']:
 N=[[0]*4 for _ in range(4)]
 for i,L in enumerate(Ls):
  M=tuple(sorted(apply(g,v) for v in L));N[ds[i]][ds[idx[M]]]+=1
 assert N==list(map(list,zip(*N))) and list(map(sum,N))==[1,14,56,64];Ns.append(N)
N1=[[0,1,0,0],[1,1,12,0],[0,12,12,32],[0,0,32,32]];N2=[[0,0,1,0],[0,3,3,8],[1,3,28,24],[0,8,24,32]]
assert Ns[1]==N1 and Ns[2]==N2
Q=[[[int(i==j)*[1,14,56,64][i]-N[i][j] for j in range(4)] for i in range(4)] for N in Ns]
u=[1,-3,2,0];v=[0,1,-3,2]
assert all(3*Q[1][i][j]-2*Q[2][i][j]==u[i]*u[j]+8*v[i]*v[j] for i in range(4) for j in range(4))
f=[7,3,1,0];q=[sum(f[i]*Qk[i][j]*f[j] for i in range(4) for j in range(4)) for Qk in Q]
assert q[1:3]==[96,144]
# Negative controls: constants have zero displacement; a unit orbit indicator need not meet the sharp ratio.
assert all(sum(map(sum,Qk))==0 for Qk in Q)
assert Q[1][0][0]==Q[2][0][0]==1
out={'status':'PASS','method':'B complete unordered-isotropic-triple certificate; independent transition and quadratic-form derivation; no C code imports','N1':N1,'N2':N2,'identity':'3q1-2q2=||v0-3v1+2v2||^2+8||v1-3v2+2v3||^2','sharp_values':f,'sharp_q1_q2':[96,144],'constant_control':'q1=q2=0','scope':'H-radial Hilbert-valued function displacement in the135-Lagrangian representation only'}
Path(a.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
