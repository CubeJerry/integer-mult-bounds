#!/usr/bin/env python3
"""Independent projected-space census and nontrivial two-wave field replay."""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from itertools import combinations,product
from pathlib import Path
import json

def need(v,label):
 if not v:raise ValueError(label)
def span(vectors,p,n):
 out={(0,)*n}
 for v in vectors:out={tuple((x[i]+c*v[i])%p for i in range(n))for x in out for c in range(p)}
 return frozenset(out)
def dim(S,p):
 n=len(S);r=0
 while n>1:need(n%p==0,'space size');n//=p;r+=1
 return r
def ternary_spaces():
 Z=span([],3,2);V=span([(1,0),(0,1)],3,2)
 lines={span([v],3,2)for v in V if v!=(0,0)}
 return [Z]+sorted(lines,key=lambda s:sorted(s))+[V]
def determinant3(rows):
 a,b,c=rows
 return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%3
def projected_census():
 spaces=ternary_spaces();need(len(spaces)==6,'ternary projected spaces');cases=positive=trials=0
 for U in product(spaces,repeat=3):
  condition=all(dim(span(set().union(*(U[i]for i in S)),3,2),3)+1>=len(S)
                for k in range(1,4)for S in combinations(range(3),k))
  choices=[[(x,y,z)for x,y in V for z in range(3)]for V in U]
  found=False
  for rows in product(*choices):
   trials+=1
   if determinant3(rows):found=True;break
  need(found==condition,'late subset criterion versus actual full determinant')
  cases+=1;positive+=found
 # Full projected span is not a substitute for subset conditions.
 Z=spaces[0];full=spaces[-1]
 need(dim(span(Z|Z|full,3,2),3)==2,'total span control')
 need(dim(span(Z|Z,3,2),3)+1<2,'proper subset obstruction')
 return {'lists':cases,'positive':positive,'actual_row_triples_examined':trials,'total_span_only_rejected':True}
def mul(a,b):
 out=0
 while b:
  if b&1:out^=a
  b>>=1;a<<=1
  if a&8:a^=0b1011
 return out
def inv(a):
 return next(b for b in range(1,8)if mul(a,b)==1)
def matvec(A,x):return [mul(row[0],x[0])^mul(row[1],x[1])for row in A]
def invert2(A):
 det=mul(A[0][0],A[1][1])^mul(A[0][1],A[1][0]);need(det!=0,'invertible actual phase')
 z=inv(det);return [[mul(z,A[1][1]),mul(z,A[0][1])],[mul(z,A[1][0]),mul(z,A[0][0])]]
def field_replay():
 need(all(mul(x,inv(x))==1 for x in range(1,8)),'GF8 inverses')
 early=[[1,2],[2,1]];late=[[1,2],[1,3]];cross=[[4,1],[2,4]]
 e_inv=invert2(early);l_inv=invert2(late);cases=0
 for u0,u1,v,y0,ybirth in product(range(8),repeat=5):
  snapshot=[u0,u1]
  ex=matvec(early,snapshot)
  need(matvec(e_inv,ex)==snapshot,'early continuing plus genuine closure restore')
  owners=[y0^v,ybirth]
  pure=matvec(late,owners);shift=matvec(cross,snapshot)
  actual=[x^y for x,y in zip(pure,shift)]
  recovered=matvec(l_inv,[x^y for x,y in zip(actual,shift)])
  need(recovered==owners,'arbitrary original late owners restored')
  proper=[v^shift[0],v^shift[1]]
  baseline=matvec(late,[y0,ybirth])
  need(actual==[x^y for x,y in zip(proper,baseline)],'all original baseline columns explicit')
  # The two rank-two saturated demands share the actual one early slot.
  target1=[u0^mul(2,u1),v^mul(4,u0)^u1]
  target2=[u0^mul(2,u1),v^mul(2,u0)^mul(4,u1)]
  need([ex[0],proper[0]]==target1 and [ex[0],proper[1]]==target2,'both saturated targets')
  cases+=1
 # Every scalar multiplication expands to a fixed three-bit binary map.
 binary=[]
 for coefficient in range(8):
  rows=[sum(((mul(coefficient,1<<k)>>bit)&1)<<k for k in range(3))for bit in range(3)]
  for x in range(8):need(sum(((row&x).bit_count()%2)<<bit for bit,row in enumerate(rows))==mul(coefficient,x),'binary field multiplication')
  binary.append(rows)
 rejected=0
 for bad in [[[1,0],[1,0]],[[1,0],[2,0]]]:
  try:invert2(bad)
  except ValueError:rejected+=1
 need(rejected==2,'duplicate early row and omitted birth column rejected')
 return {'states':cases,'field_polynomial':'x^3+x+1','early':early,'late':late,'cross':cross,
         'early_inverse':e_inv,'late_inverse':l_inv,'binary_scalar_maps_checked':64,
         'actual_local_snapshot_binary_records':6,'new_MOVE':0,'phase_rank_faults_rejected':rejected}
def main():
 ap=ArgumentParser();ap.add_argument('--author',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
 result={'status':'PASS_INDEPENDENT_PAID_D_PHASE_REVIEW','author_code_imported':False,'projected_space_census':projected_census(),
         'actual_two_wave_replay':field_replay(),'scope':'local D stage conditional on supplied full-product source/demand interface; no full native code'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 pins={str(p.relative_to(a.author)):sha256(p.read_bytes()).hexdigest()for p in [a.author/'PROOF.md',a.author/'check.py',a.author/'output/RESULT.json']}
 (a.out/'REVIEW-PINS.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n');print(result['status']);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
