#!/usr/bin/env python3
"""Independent rational replay; no author modules. @CubeJerry, OpenAI assistance."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip,hashlib,json
from pathlib import Path
OLD='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c'
CORE='66815ff5d01f76f19e61b3f14cb12bf90ceef07c17801b6c681dacb628e19f12'
EXT='b32bffe0f86e12257ebb29f019b25b4c421d7ba31b8c260458937ac27a7b324c'
def need(c,m):
 if not c:raise ValueError(m)
def load(p,pin):
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'source pin');return json.loads(gzip.decompress(b))
def add(a,b,c=F(1)):
 out=a.copy()
 for k,v in b.items():
  z=out.get(k,F(0))+c*v
  if z:out[k]=z
  else:out.pop(k,None)
 return out
def combo(cs,rs):
 out={}
 for c,r in zip(cs,rs):out=add(out,r,c)
 return out
def det(a):
 a=[list(map(F,r))for r in a];d=F(1)
 for j in range(len(a)):
  k=next((i for i in range(j,len(a))if a[i][j]),None)
  if k is None:return F(0)
  if k!=j:a[j],a[k]=a[k],a[j];d=-d
  v=a[j][j];d*=v
  for i in range(j+1,len(a)):
   c=a[i][j]/v;a[i]=[x-c*y for x,y in zip(a[i],a[j])]
 return d
def rankp(a,p):
 a=[[x.numerator*pow(x.denominator,-1,p)%p for x in r]for r in a];n=0
 for j in range(len(a[0])):
  k=next((i for i in range(n,len(a))if a[i][j]),None)
  if k is None:continue
  a[n],a[k]=a[k],a[n];v=pow(a[n][j],-1,p);a[n]=[v*x%p for x in a[n]]
  for i in range(n+1,len(a)):
   c=a[i][j];a[i]=[(x-c*y)%p for x,y in zip(a[i],a[n])]
  n+=1
 return n
def smooth(n):
 n=abs(n)
 if not n:return False
 for p in(2,3,5):
  while n%p==0:n//=p
 return n==1
def replay(w):
 n=w['public'];rows={i:{i:F(1)}for i in range(n)};loc=dict(enumerate(w['initial']));spaces=[]
 for basis in w['frames']:
  s={0}
  for b in basis:s|={x^b for x in tuple(s)}
  need(len(s)==2**len(basis),'chart independence');spaces.append(s)
 bills=[Counter(),Counter()];ct=Counter();peak=dirty=height=0;l1=F(1)
 for e in w['program']:
  op,r=e[:2];ct[op]+=1
  if op=='INIT':
   need(r>=n and r not in rows,'fresh owner');rows[r]={};loc[r]=e[2];peak=max(peak,len(rows)-n)
  elif op=='CLEAR':
   need(r>=n and r in rows and loc[r]==e[2],'actual clear');dirty+=bool(rows[r]);del rows[r];del loc[r]
  elif op=='MOVE':
   _,r,a,b,own=e;need(loc[r]==a and own==(r>=n),'MOVE entrance');need(spaces[a]<spaces[b]or own and spaces[b]<spaces[a],'nested MOVE');bills[int(own)][abs(len(w['frames'][a])-len(w['frames'][b]))]+=1;loc[r]=b
  elif op in('ADD','COPY','SCALE'):
   need(loc[r]==e[-1],'destination cochart')
   if op=='SCALE':c=F(e[2]);rows[r]={i:c*x for i,x in rows[r].items()if c*x}
   else:
    need(r!=e[2]and loc[e[2]]==e[-1],'source cochart');c=F(e[3]);rows[r]=add(rows[r]if op=='ADD'else{},rows[e[2]],c)
   need(c and abs(c)+1<2**16 and smooth(c.denominator),'bounded smooth grammar');need(op!='SCALE'or smooth(c.numerator),'unit SCALE')
   for x in rows[r].values():
    need(x.denominator&(x.denominator-1)==0,'dyadic prefix');height=max(height,x.denominator.bit_length()-1)
   l1=max(l1,sum(map(abs,rows[r].values())))
  else:raise ValueError('unknown operation '+op)
 need(set(rows)==set(range(n)),'all owners ended')
 return rows,loc,{'events':sum(ct.values()),'operations':dict(ct),'public_moves':dict(bills[0]),'owned_moves':dict(bills[1]),'dirty_clears':dirty,'peak_owned':peak,'max_binary_height':height,'max_row_l1':str(l1)}
def root(v):
 if v.bit_count()==3:return[2 if v>>i&1 else-1 for i in range(9)]
 need(v.bit_count()==7,'root type');z=[i for i in range(9)if not(v>>i&1)];return[3*(int(i==z[0])-int(i==z[1]))for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def run(repo,package):
 old=load(repo/'research/moonshot-005-program/results/proper-chart-relay/author/20/WORD.json.gz',OLD)
 core=load(package/'WORD.json.gz',CORE);ext=load(package/'forward/WORD.json.gz',EXT)
 for key in('public','frames','initial','owned_fields','source_role_map'):need(old[key]==core[key]==ext[key],'unchanged '+key)
 need(core['program'][:432]==old['program'][:432]and core['program'][464:]==old['program'][432:],'literal32event insertion')
 rm={int(k):v for k,v in old['source_role_map'].items()};P=sorted(h for h in rm if h<112);S=old['relay']['unrestored_ports'];T=old['relay']['restored_ports'];H=sorted(S+T);U=set(P)-set(H)
 basis=[root(z)for z in old['relay']['ground_Gram_frame']]
 g={h:[F(dot(root(old['frames'][old['initial'][rm[h]]][0]),z),18)for z in basis]for h in P}
 u=list(map(F,('1','1/2','2','1/2','9/2','-3/2','1/2','-5/2')));v=list(map(F,('0','1','0','-1','1/2','1/2','-1/2','1/2')))
 need(dot(u,v)==0 and dot(u,u)==F(69,2)and dot(v,v)==3,'explicit wedge invariants')
 K=[[u[i]*v[j]-v[i]*u[j]for j in range(8)]for i in range(8)];L=[[F(i==j)+K[i][j]for j in range(8)]for i in range(8)]
 C=[[sum(g[h][i]*g[h][j]for h in S)for j in range(8)]for i in range(8)]
 A0=[[F(i==j)-C[i][j]for j in range(8)]for i in range(8)];A=[[F(i==j)-sum(L[i][k]*C[k][j]for k in range(8))for j in range(8)]for i in range(8)]
 need(det(A0)==24387048 and rankp(A0,127)==6,'old arithmetic kernel');need(det(A)==3200000000 and det(L)==F(209,2),'exact determinant and nonunit Lambda');need(rankp(K,127)==2,'wedge rank witness')
 need(all(dot(g[h],[dot(row,g[h])for row in K])==0 for h in P),'all104 diagonal equations')
 Br={h:208+j for j,h in enumerate(H)};Dr={h:304+j for j,h in enumerate(H)}
 q=[{Dr[h]:g[h][i]for h in H if g[h][i]}for i in range(8)];z=[combo(row,q)for row in L]
 residual={h:add({Dr[h]:F(-1)}if h in H else{},combo(g[h],z))for h in P};want={i:{i:F(1)}for i in range(400)}
 for h in U:want[rm[h]]=add(want[rm[h]],want[rm[h+112]],F(-1))
 perm={int(k):val for k,val in old['relay']['permutation'].items()}
 for h in H:
  want[Br[h]]=add(want[Br[h]],residual[h]);want[Dr[h]]={Dr[h]:F(1)}if h in T else residual[perm[h]]
 r,loc,bill=replay(core);need(r==want,'independent400column core endpoint')
 tail=core['program'][-208:];xm=[e for e in tail if e[1]<104];ym=[e for e in tail if 104<=e[1]<208];entrance=len(core['program'])-208
 need(ext['program'][:entrance]==core['program'][:entrance],'unchanged full prefix');need(ext['program'][entrance:entrance+104]==xm and ext['program'][-104:]==ym,'actual public tail reorder')
 service=ext['program'][entrance+104:-104];need(len(service)==350,'actual350event forward service')
 Gamma=[[dot(g[h],u)*dot(g[j],v)-dot(g[h],v)*dot(g[j],u)for j in P]for h in P];current=[want[rm[h]]for h in P]
 for h,cs in zip(P,Gamma):want[rm[h+112]]=add(want[rm[h+112]],combo(cs,current))
 rr,ll,bb=replay(ext);need(rr==want and ll==loc,'independent400column extended endpoint');need(bb['owned_moves']=={1:47,6:1,7:7,9:2},'owned invoice');need(bb['public_moves']=={1:96,2:20,5:20,7:76,8:304},'public invoice');need(bb['dirty_clears']==28 and bb['peak_owned']==15,'temporary lifetimes')
 bad=json.loads(json.dumps(ext));i=next(i for i in range(entrance+104,len(bad['program'])-104)if bad['program'][i][0]=='ADD');bad['program'][i][3]=str(2*F(bad['program'][i][3]));wrong,_,_=replay(bad);need(wrong!=want,'wrong capture control')
 return{'status':'PASS_INDEPENDENT_RANK_TWO_SOURCE_AND_FORWARD_REPLAY','pins':{'old':OLD,'core':CORE,'extended':EXT},'core':bill,'extended':bb,'input_columns_checked_each':400,'small_determinant':str(det(A)),'Lambda_determinant':str(det(L)),'old_residue_rank_mod127':6,'perturbation_rank':2,'remaining_D':76,'wrong_capture_control_rejected':True,'phase_scope':'Old MOVE phases inherited by literal identity; two new rank9 maps have separate pinned dual-engine evidence, not a new uniform compiler proof.','no_new_kappa':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repo,a.package);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
