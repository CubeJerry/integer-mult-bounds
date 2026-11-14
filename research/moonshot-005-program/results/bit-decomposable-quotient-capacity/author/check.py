#!/usr/bin/env python3
"""Exact all-width decomposable-capacity controls."""
import argparse,gzip,hashlib,itertools,json,random
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def basis(rows):
 b={};out=[]
 for row in rows:
  x=row
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;out.append(row);break
 return out
def brank(rows):return len(basis(rows))
def xor(xs):
 out=0
 for x in xs:out^=x
 return out
def mul(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return out
M=[[mul(a,b)for b in range(4)]for a in range(4)];INV={1:1,2:3,3:2}
def frank(rows):
 piv={}
 for raw in rows:
  r=list(raw)
  for p in sorted(piv):
   if r[p]:z=r[p];r=[x^M[z][y]for x,y in zip(r,piv[p])]
  if any(r):
   p=next(j for j,x in enumerate(r)if x);piv[p]=[M[INV[r[p]]][x]for x in r]
 return len(piv)
def inverse(A):
 n=len(A);R=[list(row)+[int(i==j)for j in range(n)]for i,row in enumerate(A)]
 for p in range(n):
  k=next(k for k in range(p,n)if R[k][p]);R[p],R[k]=R[k],R[p];z=INV[R[p][p]];R[p]=[M[z][x]for x in R[p]]
  for k in range(n):
   if k!=p and R[k][p]:z=R[k][p];R[k]=[x^M[z][y]for x,y in zip(R[k],R[p])]
 return [r[n:]for r in R]
def outer(m,v):return [M[x][y]for x in m for y in v]
def bouter(m,v,V):return sum(((m>>r)&1)*((v>>t)&1)<<(V*r+t)for r in range(V)for t in range(V))
def binary_circuits():
 V=3;I=sum(1<<(3*j+j)for j in range(3));records=[]
 for label,values in [('MDS',[1,2,4,7]),('non_MDS_distinct',[1,2,4,3])]:
  counts=Counter();cases=0
  for left in itertools.product(range(8),repeat=4):
   mats=[bouter(m,v,V)for m,v in zip(left,values)];active=[m for m in mats if m];r=brank(active)
   if brank(active+[I])==r:need(r==len(active),'near-width active independence');counts[len(active)]+=1
   cases+=1
  records.append({'V':3,'r':4,'value_family':label,'cases':cases,'identity_span_cases':dict(counts)})
 repeated=[bouter(m,v,3)for m,v in zip([1,1,2,4],[1,1,2,4])]
 need(brank(repeated)==3 and brank(repeated+[I])==3,'repeated-value independence counterexample')
 need([j for j,v in enumerate([1,1,2,4])if(v&2).bit_count()%2]==[2],'singleton projection')
 return records
def mds_f4():
 values=[(1,t,M[t][t])for t in range(4)]+[(0,0,1)]
 need(all(frank(rows)==3 for rows in itertools.combinations(values,3)),'MDS value family')
 inv=inverse(values[:3]);counts=Counter();I=[int(r==t)for r in range(3)for t in range(3)]
 columns=list(itertools.product(range(4),repeat=3));cases=0
 for a,b in itertools.product(columns,repeat=2):
  extras=[outer(a,values[3]),outer(b,values[4])];R=[[int(r==t)^extras[0][3*r+t]^extras[1][3*r+t]for t in range(3)]for r in range(3)]
  X=[[xor(M[R[r][k]][inv[k][t]]for k in range(3))for t in range(3)]for r in range(3)]
  left=[tuple(X[r][t]for r in range(3))for t in range(3)]+[a,b];mats=[outer(m,v)for m,v in zip(left,values)];active=[m for m in mats if any(m)]
  need([xor(m[j]for m in mats)for j in range(9)]==I,'exact right inverses');need(frank(active)==len(active),'MDS active independence');counts[len(active)]+=1;cases+=1
 need(cases==4096,'all MDS right inverses')
 vb=[(1,0),(0,1),(1,1),(1,2)];mb=[(1,0),(0,1),(3,2),(2,2)];mm=[outer(m,v)for m,v in zip(mb,vb)];I2=[1,0,0,1]
 need(all(frank(pair)==2 for pair in itertools.combinations(vb,2)),'boundary MDS')
 need([xor(m[j]for m in mm)for j in range(4)]==[0]*4 and frank(mm)==3 and frank(mm+[I2])==3,'strict MDS boundary')
 return {'field_order':4,'V':3,'r':5,'right_inverses':cases,'active_count_census':dict(counts),'values':values,'boundary_V2_r4':{'values':vb,'left_columns':mb,'coefficient_rank':3,'identity_in_span':True}}
def further_widths():
 out=[]
 for V in [2,3,4,8,17]:
  whole=(1<<V)-1;values=[1<<j for j in range(V)]+[whole]
  if V<=8:zs=range(1<<V)
  else:
   rng=random.Random(1701);zs=sorted({0,whole}|{1<<j for j in range(V)}|{(1<<j)-1 for j in range(1,V)}|{rng.randrange(1<<V)for _ in range(64)})
  I=sum(1<<(V*j+j)for j in range(V));count=0
  for z in zs:
   left=[(1<<j)^z for j in range(V)]+[z];mats=[bouter(m,v,V)for m,v in zip(left,values)];active=[m for m in mats if m]
   need(xor(mats)==I and brank(active)==len(active),'further-width right inverse');count+=1
  out.append({'V':V,'r':V+1,'right_inverses_checked':count,'exhaustive_right_inverse_family':V<=8,'saving_cap':17*(V+1)//V})
 return out
def native(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw));roots=[list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0]))for i in range(111)]
 K=[sum(int(i==j or sum(x*y for x,y in zip(r,s))==0)<<j for j,s in enumerate(roots))for i,r in enumerate(roots)];C=basis(K);need(len(C)==9,'canonical rank')
 ids=[7,24,25];common=K[7]&K[24]&K[25]
 for i in ids:common&=~(1<<i)
 T=[j for j in range(111)if common>>j&1];need(len(T)==36,'shared contacts');P=T[:-3];p=sum(1<<j for j in P);hs=[p^(1<<j)for j in T[-3:]];need(brank(C+hs+[p])==13,'four scalar modes')
 zero=[0]*4;coeff=[[[1,0,0,0],[0,0,0,1],zero],[[1,0,1,0],zero,[0,0,1,1]],[zero,[0,1,0,1],[1,1,0,0]]]
 old=[]
 for i,k in enumerate(K):
  mats=coeff[ids.index(i)]if i in ids else[zero,zero,zero]
  old.append([[(k if r==t else 0)^xor(h for h,m in zip(hs,mats)if m[2*r+t])for t in range(2)]for r in range(2)])
 scalar_savings=[]
 for a,h in enumerate(hs):
  F=[k^h if i in ids and any(coeff[ids.index(i)][a]) else k for i,k in enumerate(K)];ell=sum(int(f.bit_count()-1>36)+int(f.bit_count()-1>52)for f in F);need(ell==218 and brank(F+C)==10,'old scalar charge mode');scalar_savings.append(222-ell)
 F=[k^p if i in ids else k for i,k in enumerate(K)];ell=sum(int(f.bit_count()-1>36)+int(f.bit_count()-1>52)for f in F);need(ell==216 and brank(F+C)==10,'repeated scalar charge mode');extra_saving=222-ell
 result=[]
 for V in [2,3,4,8,17]:
  lift=lambda h,t:sum(((h>>j)&1)<<(V*j+t)for j in range(111));A=[];total=0;blockmask=(1<<V)-1
  for i,k in enumerate(K):
   rr=[lift(old[i][r][0],0)^lift(old[i][r][1],1)for r in range(2)]+[lift(k^p if i in ids else k,t)for t in range(2,V)]
   need(all(((row>>(V*i))&blockmask)==1<<r for r,row in enumerate(rr)),'all-width identity diagonal')
   support=sum(int(any((row>>(V*j))&blockmask for row in rr))<<j for j in range(111));need(support&~k==0,'all-width forbidden zeros');foreign=support.bit_count()-1
   need(foreign==(27 if i in ids else k.bit_count()-1),'actual block support');total+=int(foreign>36)+int(foreign>52);A+=rr
  CV=[lift(c,t)for c in C for t in range(V)];d=brank(A+CV)-9*V;charge=sum(scalar_savings)+(V-2)*extra_saving
  need(d==V+1 and total==216 and charge==V*(222-total),'native quotient and weighted charging')
  result.append({'V':V,'quotient_dimension':d,'ell':total,'scalar_envelope_dimension':3 if V==2 else 4,'indexed_scalar_charge_sum':charge,'actual_saving':6,'scalar_modes_are_dependent':V>=4})
 return {'shared_patch':P,'tips':T[-3:],'controls':result}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 out={'status':'PASS_DECOMPOSABLE_QUOTIENT_CAPACITY_CONTROLS','native_sha256':PIN,'binary_near_width_exhaustion':binary_circuits(),'MDS_F4':mds_f4(),'further_widths':further_widths(),'native_all_width_controls':native(a.native),'classification':'exact finite controls for all-field proofs; no physical source or new kappa','new_kappa':None}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'binary_cases':8192,'F4_MDS_right_inverses':4096,'native_widths':[2,3,4,8,17]}))
if __name__=='__main__':main()
