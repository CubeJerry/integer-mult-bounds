#!/usr/bin/env python3
"""Exact complete three-head symplectic gauge census plus actual source controls."""
import argparse,hashlib,importlib.util,itertools,json,sys
from collections import Counter
from pathlib import Path

def app(cols,x):
 z=0
 for j,c in enumerate(cols):
  if x>>j&1:z^=c
 return z

def rk(vs):
 p={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j not in p:p[j]=v;break
   v^=p[j]
 return len(p)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path(__file__).with_name('SOURCE-ADMISSION-RESULT.json'));ar=ap.parse_args();base=Path(__file__).parent
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';sp=importlib.util.spec_from_file_location('admission_actual',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);Xa=m.monomial([x^1 for x in range(8)],[0]*8);Xb=m.monomial([x^2 for x in range(8)],[0]*8);Ca=m.M((I.scale((1,1))+Xa.scale((1,-1))).a,1).norm();Cb=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm();Za=m.monomial(list(range(8)),[2*(x&1)for x in range(8)])
 counts=Counter();admitted=negative_sign=0
 for P in itertools.product(range(1,8),repeat=3):
  if rk(P)!=3:continue
  for bits in range(64):
   d=[(bits>>j)&1 for j in range(6)];C=(d[0]|d[3]<<1|d[4]<<2,d[3]|d[1]<<1|d[5]<<2,d[4]|d[5]<<1|d[2]<<2)
   v=P[1];w=app(C,v);wa=w&1
   # Matrix (4) is expressed by its three column bitmasks.
   Bcols=[]
   for j in range(3):Bcols.append((1 if j==0 else 0)^(v if v>>j&1 else 0)^(1 if wa and(v>>j&1)else 0))
   expected=rk(Bcols);assert expected==(0 if v==1 and not wa else(1 if v==1 else 2));counts[expected]+=1
   perm=[app(P,x)for x in range(8)];ph=[]
   for y in perm:ph.append((sum(d[j]*((y>>j)&1)for j in range(3))+2*(d[3]*(y&1)*((y>>1)&1)+d[4]*(y&1)*((y>>2)&1)+d[5]*((y>>1)&1)*((y>>2)&1)))%4)
   S=m.monomial(perm,ph);R=Ca.star()@S@Cb@S;assert m.gaussian_rank(R)==expected
   if expected:continue
   for epsilon in[1,-1]:
    T=S if epsilon==1 else Za@S;f=[((x&w).bit_count()%2)^(epsilon==-1)for x in range(8)];J=m.monomial([x^f[x]for x in range(8)],f);R=Ca.star()@T@Cb@T;A=Cb@T
    assert R==J@T.power(2) and m.gaussian_rank(A)==1 and m.gaussian_rank(A.power(2))==2
    assert T.star()@Ca@R==A and Ca@Cb@R==A.power(2)
    if epsilon==1:admitted+=1
    else:negative_sign+=1
 assert counts=={0:768,1:768,2:9216} and admitted==negative_sign==768
 out={'status':'PASS_COMPLETE_THREE_HEAD_MONOMIAL_SOURCE_ADMISSION','symplectic_ordinary_gauges':sum(counts.values()),'residual_gaussian_rank_histogram':dict(counts),'actual_positive_sign_admitted_gauges':admitted,'actual_negative_sign_admitted_gauges':negative_sign,'every_admitted_head_ranks':[1,2],'source_phase_and_all_column_coefficients_checked':True,'proof_sha256':hashlib.sha256((base/'MONOMIAL-SOURCE-ADMISSION.md').read_bytes()).hexdigest(),'scope':'Exact finite source census supplements universal criterion for every fixed d. No caller, supplier or new kappa.'}
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
