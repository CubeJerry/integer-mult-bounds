#!/usr/bin/env python3
"""Independent finite controls for the separately reviewed all-field cell proof."""
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,itertools,json
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col))%2 for col in zip(*b)] for row in a]
def plus(a,b):return [[x^y for x,y in zip(r,s)] for r,s in zip(a,b)]
def mv(a,v):return tuple(sum(x*y for x,y in zip(row,v))%2 for row in a)
def inverse(a):
 n=len(a);z=[row[:]+ident(n)[i] for i,row in enumerate(a)]
 for j in range(n):
  k=next(i for i in range(j,n) if z[i][j]);z[j],z[k]=z[k],z[j]
  for i in range(n):
   if i!=j and z[i][j]:z[i]=[x^y for x,y in zip(z[i],z[j])]
 return [r[n:] for r in z]
def reduce_both(a):
 n=len(a);d=[r[:] for r in a];u=ident(n);v=ident(n);rank=0
 for k in range(n):
  pos=next(((i,j) for i in range(k,n) for j in range(k,n) if d[i][j]),None)
  if pos is None:break
  i,j=pos;d[k],d[i]=d[i],d[k];u[k],u[i]=u[i],u[k]
  for z in (d,v):
   for row in z:row[k],row[j]=row[j],row[k]
  for i in range(n):
   if i!=k and d[i][k]:d[i]=[x^y for x,y in zip(d[i],d[k])];u[i]=[x^y for x,y in zip(u[i],u[k])]
  for j in range(n):
   if j!=k and d[k][j]:
    for z in (d,v):
     for row in z:row[j]^=row[k]
  rank+=1
 assert mm(mm(u,a),v)==d==[[int(i==j and i<rank) for j in range(n)] for i in range(n)]
 return rank,u,v,d
def rank_rows(rows):
 basis={}
 for a in rows:
  while a:
   j=a.bit_length()-1
   if j in basis:a^=basis[j]
   else:basis[j]=a;break
 return len(basis)
def main(a):
 pins={str(p.relative_to(a.package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [a.package/'PROOF.md',a.package/'next/PROOF.md']}
 distribution=Counter();incompatible=missing=0;cases=0;vectors=list(itertools.product((0,1),repeat=3));I=ident(3)
 for mask in range(512):
  D=[[mask>>(3*i+j)&1 for j in range(3)] for i in range(3)]
  r,U,V,E=reduce_both(D);distribution[r]+=1
  R=mm(mm(V,E),U);J=[row[r:] for row in V];h=inverse(V)[r:]
  assert mm(mm(D,R),D)==D and mm(mm(R,D),R)==R
  if r<3:
   assert mm(D,J)==[[0]*(3-r) for _ in range(3)] and mm(h,J)==ident(3-r)
   assert plus(mm(R,D),mm(J,h))==I and mm(h,R)==[[0]*3 for _ in range(3-r)]
  else:assert mm(R,D)==I
  image={mv(D,v) for v in vectors};compat=plus(I,mm(D,R))
  for w in vectors:
   ok=not any(mv(compat,w));assert ok==(w in image)
   if not ok:assert mv(D,mv(R,w))!=w;incompatible+=1
  for p in vectors:
   w=mv(D,p);t=mv(h,p) if h else ()
   restored=tuple(x^y for x,y in zip(mv(R,w),mv(J,t) if t else (0,0,0)))
   assert restored==p;cases+=1
   if any(t):assert mv(R,w)!=p;missing+=1
 raw=a.bus.read_bytes();word=json.loads(gzip.decompress(raw));rows={i:1<<i for i in range(222)};packet=222;hist=[];ground=None
 for e in word['program']:
  if e[0]=='INIT':rows[e[1]]=0
  elif e[0]=='ADD':rows[e[1]]^=rows[e[2]]
  elif e[0]=='CLEAR':del rows[e[1]]
  elif e[0]=='MOVE' and e[1]==packet:
   dim=word['frames'][str(e[3])]['dim']
   if dim:hist.append(rows[packet])
   else:ground=rows[packet]
 assert len(hist)==7 and hist==[1<<i for i in range(7,0,-1)] and ground==1
 assert rank_rows([ground]+hist)==8
 first=1;cache=first;later=first^cache;assert later==0 and rank_rows([later])<rank_rows([first])
 out={'status':'PASS_INDEPENDENT_SCATTERING_PARAMETERIZATION_CONTROLS_AND_BUS_RANK','proof_pins':pins,'method':'Two-sided binary row/column elimination, not author generalized-inverse construction; written universal proof reviewed separately.','all_binary_3_by_3_through_matrices':512,'rank_distribution':dict(sorted(distribution.items())),'actual_input_reconstruction_cases':cases,'incompatible_output_controls_rejected':incompatible,'omitted_kernel_controls_rejected':missing,'actual_bus_word_sha256':hashlib.sha256(raw).hexdigest(),'actual_bus_ground_and_historical_modes':[ground]+hist,'actual_bus_historical_rank':8,'late_zero_terminal_control_rejected':True,'scope':'Finite controls only; separate root review proves all-field/all-V algebra and poset induction. Actual111-target endpoint remains open; q>=2 is necessary only.'}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','rank_distribution','actual_input_reconstruction_cases','incompatible_output_controls_rejected','omitted_kernel_controls_rejected','actual_bus_historical_rank']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);p.add_argument('--bus',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
