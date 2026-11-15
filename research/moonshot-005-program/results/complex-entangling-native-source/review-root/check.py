#!/usr/bin/env python3
"""Independent exact Gaussian-integer columns for actual ordinary gauges."""
import argparse,collections,itertools,json
from pathlib import Path
UNIT=[(1,0),(0,1),(-1,0),(0,-1)]
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def conj(a):return(a[0],-a[1])
def scale(a,n):return(a[0]*n,a[1]*n)
def rank(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def pmul(M,x):
 z=0
 for j in range(3):
  if x>>j&1:z^=M[j]
 return z
def phase(q,x):
 bits=[x>>i&1 for i in range(3)];e=sum((q>>i&1)*bits[i]for i in range(3))
 for k,(i,j)in enumerate([(0,1),(0,2),(1,2)],3):e+=2*(q>>k&1)*bits[i]*bits[j]
 return UNIT[e%4]
def calculate(perm,phi):
 ea,eb=1,2;alpha=(1,1);beta=(1,-1);ca=conj(alpha);cb=conj(beta);R=[];A2=[]
 for x in range(8):
  r={};s={};y=perm[x]
  for t,first in [(y,alpha),(y^eb,beta)]:
   z=perm[t];f=mul(phi[x],mul(first,phi[t]))
   for dst,c in [(z,ca),(z^ea,cb)]:r[dst]=add(r.get(dst,(0,0)),mul(c,f))
   for dst,c in [(z,alpha),(z^eb,beta)]:s[dst]=add(s.get(dst,(0,0)),mul(c,f))
  R.append({k:v for k,v in r.items()if v!=(0,0)});A2.append({k:v for k,v in s.items()if v!=(0,0)})
 eta={perm[x]:mul(phi[x^eb],conj(phi[x]))for x in range(8)};v=perm[0]^perm[eb];pred=v==ea and all(z in [UNIT[0],UNIT[2]]for z in eta.values());sizes={len(x)for x in R};assert len(sizes)==1 and next(iter(sizes))in [1,2,4];rr={1:0,2:1,4:2}[next(iter(sizes))];assert pred==(rr==0)
 if pred:
  assert all(eta[y]==eta[y^ea]for y in range(8))
  for x,row in enumerate(R):
   y=perm[perm[x]];f=0 if eta[y]==UNIT[0]else 1;want=scale(mul(phi[x],mul(phi[perm[x]],UNIT[f])),4);assert row=={y^(f*ea):want}
  assert all(len(row)==4 for row in A2)
 return rr,v,eta,R
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();hist=collections.Counter();admitted=[];negative={};count=0;matrices=[M for M in itertools.product(range(1,8),repeat=3)if rank(M)==3];assert len(matrices)==168
 for M,q in itertools.product(matrices,range(64)):
  perm=[pmul(M,x)for x in range(8)];phi=[phase(q,x)for x in range(8)];r,v,eta,R=calculate(perm,phi);hist[r]+=1;count+=1
  if r==0:
   admitted.append({'columns':list(M),'phase_bits':q,'epsilon':1 if eta[0]==UNIT[0]else -1,'z_mask':sum((eta[1<<j]!=eta[0])<<j for j in range(3))})
   if any(z==UNIT[2]for z in eta.values())and'omit_controlled_gauge'not in negative:
    wrong=[{perm[perm[x]]:scale(mul(phi[x],phi[perm[x]]),4)}for x in range(8)];assert R!=wrong;negative['omit_controlled_gauge']={'columns':list(M),'phase_bits':q,'rejected':True}
  elif r==1 and'phase_on_control_axis'not in negative:negative['phase_on_control_axis']={'columns':list(M),'phase_bits':q,'actual_residual_rank':r}
  elif r==2 and'wrong_x_direction'not in negative:negative['wrong_x_direction']={'columns':list(M),'phase_bits':q,'actual_residual_rank':r}
 assert dict(hist)=={0:768,1:768,2:9216};assert len(admitted)==768
 witness=next(z for z in admitted if z['z_mask']);M=tuple(witness['columns']);q=witness['phase_bits'];phase_controls=0
 for translation,zmask,g in itertools.product(range(8),range(8),range(4)):
  perm=[pmul(M,x)^translation for x in range(8)];phi=[mul(phase(q,x),UNIT[(2*((zmask&x).bit_count()%2)+g)%4])for x in range(8)];r,_,_,_=calculate(perm,phi);assert r==0;phase_controls+=1
 ranks=[0,1,2,3,3,2,3,3,3,3,2,3,3,2,1];cut={0,1,2};h=[sum((j in cut)!=((j+k)%15 in cut)for j in range(15))//2 for k in range(15)];assert h==[min(k,15-k,3)for k in range(15)]and all(x>=y for x,y in zip(h,ranks));assert{(2-j)%15 for j in cut}==cut
 a.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_INDEPENDENT_ACTUAL_MONOMIAL_ADMISSION_AND_C15_MAJORANT','method':'Exact Gaussian-integer four-term column evaluation; no symplectic source-admission formula or author helper imported.','ordinary_linear_maps':168,'phase_lifts':64,'gauges_checked':count,'residual_gaussian_rank_histogram':dict(sorted(hist.items())),'admitted':admitted,'pauli_centre_controls':phase_controls,'negative_controls':negative,'c15_actual_ranks':ranks,'c15_cut_majorant':h,'c15_strict_majorant_indices':[i for i in range(15)if h[i]>ranks[i]],'scope':'General iff proved separately; finite controls authenticate actual phases and all d3 symplectic gauges. Scalar C15 native-only conservation, not full ordinary entangling conservation.','new_complete_kappa':False};(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','gauges_checked','residual_gaussian_rank_histogram','pauli_centre_controls','c15_strict_majorant_indices']}))
if __name__=='__main__':main()
