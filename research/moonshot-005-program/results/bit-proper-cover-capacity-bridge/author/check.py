#!/usr/bin/env python3
"""Exact native and abstract controls; the universal bridge is separate."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def rank(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def mul(a,b,modulus):
 top=1<<(modulus.bit_length()-1);out=0
 while b:
  if b&1:out^=a
  a<<=1;b>>=1
  if a&top:a^=modulus
 return out
def power(a,n,m):
 out=1
 while n:
  if n&1:out=mul(out,a,m)
  a=mul(a,a,m);n>>=1
 return out
def f32rank(rows):
 a=[list(r) for r in rows];k=0
 for c in range(len(a[0]) if a else 0):
  p=next((j for j in range(k,len(a)) if a[j][c]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];v=power(a[k][c],30,37);a[k]=[mul(x,v,37) for x in a[k]]
  for j in range(k+1,len(a)):
   if a[j][c]:v=a[j][c];a[j]=[x^mul(v,y,37) for x,y in zip(a[j],a[k])]
  k+=1
 return k
def xor(xs):
 a=0
 for x in xs:a^=x
 return a
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw));R=[]
 for i in range(111):
  r=list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0]));scale=(2 if sum(x*x for x in r)==1 else 1)*(1 if next(x for x in r if x)>0 else -1)
  rr=[x*scale for x in r];need(all(x.denominator==1 for x in rr),'integer roots');R.append(list(map(int,rr)))
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
 K=[sum(int(i==j or dot(i,j)==0)<<j for j in range(111)) for i in range(111)]
 support=lambda r:tuple(i for i,x in enumerate(r) if x)
 patterns=sorted({support(r) for r in R if len(support(r))==4});pairs=[(S,tuple(j for j in range(8) if j not in S)) for S in patterns if S<tuple(j for j in range(8) if j not in S)]
 classes=[[] for _ in range(15)]
 for i,r in enumerate(R):
  S=support(r);c=0 if len(S)==1 else 1+2*next(j for j,p in enumerate(pairs) if S in p)+sum(x<0 for x in r)%2;classes[c].append(i)
 selected=[1,2];need(all(len(classes[c])==7 for c in selected),'native seven-class boundary')
 U=[sum(1<<j for j in classes[c]) for c in selected];which={i:k for k,c in enumerate(selected) for i in classes[c]}
 F=[U[which[i]] if i in which else k for i,k in enumerate(K)]
 need(all(f>>i&1 and f&~K[i]==0 for i,f in enumerate(F)),'two-class scalar fitting')
 need(rank(K)==9 and rank(K+F)==11,'actual scalar quotient2')
 need(all(all(dot(i,j)==0 for i,j in itertools.combinations(classes[c],2)) for c in selected),'orthogonal proper foreign supports')
 boundary=[]
 for V in [1,2,3,4,8]:
  lift=lambda r,t:sum(((r>>j)&1)<<(V*j+t) for j in range(111))
  cv=[lift(k,t) for k in K for t in range(V)];av=[lift(f,t) for f in F for t in range(V)];d=rank(cv+av)-9*V
  need(d==2*V,'actual tensor boundary quotient2V');boundary.append({'V':V,'quotient_dimension':d,'chi':194,'physical_source':False})
 vectors=[(1,0),(0,1),(1,1)]
 need(all(any((u[0]*l[0]+u[1]*l[1])%2==0 for u in vectors) for l in itertools.product(range(2),repeat=2)),'no binary functional avoids all three hyperplanes')
 need(all(u[0]^mul(2,u[1],7) for u in vectors),'extension-field common functional')
 need(all(power(x,31,37)==1 for x in range(1,32)),'all nonzero GF32 elements invertible')
 polynomial=[1]
 for root in range(16):
  nxt=[0]*(len(polynomial)+1)
  for j,c in enumerate(polynomial):nxt[j]^=mul(root,c,37);nxt[j+1]^=c
  polynomial=nxt
 zero_set=[x for x in range(28) if xor(mul(c,power(x,j,37),37) for j,c in enumerate(polynomial))==0]
 need(zero_set==list(range(16)),'exact sixteen-membership abstract vector')
 normals=[[power(x,j,37) for j in range(17)] for x in range(28)]
 need(f32rank(normals)==17 and all(f32rank([normals[(s+j)%28] for j in range(17)])==17 for s in range(28)),'Vandermonde rank controls')
 thresholds=[{'V':V,'necessary_MDS_r':(7*V+3)//4,'inside_r_less_than_2V':(7*V+3)//4<2*V} for V in range(2,18)]
 need(next(x for x in thresholds if x['inside_r_less_than_2V'])['V']==4,'first MDS arithmetic width4')
 need(16*5//3==26 and 17*5//3==28 and 16*7//4==28,'old/new MDS threshold distinction')
 out={'status':'PASS_PROPER_COVER_CAPACITY_BRIDGE_CONTROLS','native_sha256':PIN,'two_class_boundary':boundary,
      'base_field_functional_failure_control':True,'abstract_density_sharpness':{'field_order':32,'V':16,'d':17,'unit_weight_rows':28,'point_capacity':16,'explicit_zero_set':zero_set,'native_fitting':False},
      'MDS_thresholds':thresholds,'former_MDS_V3_r5':{'maximum_chi_saving':26,'minimum_chi':196},
      'next_arithmetic_V4_r7':{'maximum_chi_saving':28,'construction_supplied':False},
      'strict_incidence_threshold_control':'16 identical unit-weight V-subspaces in dimensionV satisfy the pointwise premise; S>16 is essential abstractly',
      'classification':'exact controls supplement the universal projection and inherited structural proofs; no new kappa','new_kappa':None}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','former_MDS_V3_r5','next_arithmetic_V4_r7']}))
if __name__=='__main__':main()
