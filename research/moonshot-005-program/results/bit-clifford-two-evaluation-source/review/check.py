#!/usr/bin/env python3
"""Independent exact binary-expansion review of two-evaluation visibility."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from collections import Counter
import argparse,gzip,json,random,time

BASE=Path(__file__).resolve().parents[2]
REPO=BASE/'integer-mult-bounds'
def basis(rows):
 p={};out=[]
 for row in rows:
  x=row
  while x:
   k=x.bit_length()-1
   if k in p:x^=p[k]
   else:p[k]=x;out.append(row);break
 return out
def rank(rows):return len(basis(rows))
def add(A,B):return [x^y for x,y in zip(A,B)]
def mm(A,B):
 out=[]
 for x in A:
  z=0
  while x:
   l=x&-x;z^=B[l.bit_length()-1];x^=l
  out.append(z)
 return out
def action(A,x):return sum(((a&x).bit_count()%2)<<i for i,a in enumerate(A))
def inv(A):
 n=len(A);a=[[Fraction(x)for x in row]+[Fraction(i==j)for j in range(n)]for i,row in enumerate(A)]
 for c in range(n):
  k=next(k for k in range(c,n)if a[k][c]);a[c],a[k]=a[k],a[c]
  d=a[c][c];a[c]=[x/d for x in a[c]]
  for k in range(n):
   if k!=c and a[k][c]:
    m=a[k][c];a[k]=[x-m*y for x,y in zip(a[k],a[c])]
 return [r[n:]for r in a]
def geometry(repo=REPO,basis_path=BASE/'worker-C/clifford-evaluation-gate/author/BASIS.json'):
 layout=json.loads(gzip.decompress((repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
 cert=json.loads(basis_path.read_text())
 cols=cert['lattice_basis_columns'];ib=inv([[cols[j][i]for j in range(8)]for i in range(8)])
 hyp=cert['hyperbolic_basis_masks'];lookup={}
 for v in range(256):
  z=0
  for k in range(8):
   if v>>k&1:z^=hyp[k]
  lookup[z]=v
 prim=[]
 for k in range(4):
  C=[0]*16;D=[0]*16
  for j in range(16):
   if j>>k&1:D[j^(1<<k)]^=1<<j
   else:C[j|(1<<k)]^=1<<j
  prim.extend([C,D])
 gamma=[];masks=[]
 for root in layout['root_table']:
  cs=[sum(a*x for a,x in zip(row,root))for row in ib];assert all(c.denominator==1 for c in cs)
  v=sum((int(c)%2)<<i for i,c in enumerate(cs));masks.append(v);g=[0]*16
  for k in range(8):
   if lookup[v]>>k&1:g=add(g,prim[k])
  gamma.append(g)
 return layout,gamma,masks

def field_mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  a<<=1
  if a&16:a^=19
  b>>=1
 return c
def field_action(A,v):
 out=[]
 for row in A:
  z=0
  for k in range(16):
   if row>>k&1:z^=v[k]
  out.append(z)
 return out
def expanded_rank(vectors):
 return rank(sum(field_mul(c,x)<<(4*i)for i,x in enumerate(v))for v in vectors for c in [1,2,4,8])
def main():
 from hashlib import sha256
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=REPO);ap.add_argument('--basis',type=Path,default=BASE/'worker-C/clifford-evaluation-gate/author/BASIS.json');a=ap.parse_args()
 witness_path=a.author/'output/WITNESS.json';witness=json.loads(witness_path.read_text())
 assert witness['q']==16 and witness['polynomial']==19
 for x in range(1,16):assert sum(field_mul(x,y)==1 for y in range(1,16))==1
 layout,gamma,masks=geometry(a.repo,a.basis);roots=layout['root_table'];planes=list(map(set,layout['A2']));I=[1<<i for i in range(16)]
 local=[];binary=[];one_binary=[]
 for H in planes:
  j,k=sorted(H)[:2];mats=[I,gamma[j],gamma[k],mm(gamma[j],gamma[k])];local.append(mats)
  vb=[field_action(M,witness['v'])for M in mats];wb=[field_action(M,witness['w'])for M in mats]
  expand=lambda vs:[sum(field_mul(c,x)<<(4*i)for i,x in enumerate(v))for v in vs for c in [1,2,4,8]]
  binary.append(basis(expand(vb+wb)));one_binary.append(basis(expand(vb)))
 hist=Counter();one_hist=Counter();first=None;tested=0
 for i in range(111):
  adj={j for j in range(120)if i!=j and sum(x*y for x,y in zip(roots[i],roots[j]))==0}
  for j in sorted(adj&set(range(111))):
   visible=[h for h,H in enumerate(planes)if j in H and H<=adj];assert len(visible)==16
   r=rank(x for h in visible for x in binary[h]);assert r==64;hist[r]+=1
   r1=rank(x for h in visible for x in one_binary[h]);assert r1<=56;one_hist[r1]+=1
   if first is None:first={'pair':[i,j],'actual_H':visible,'binary_rank':r,'one_vector_rank':r1}
   tested+=1
 assert tested==6470
 source=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
 raw=gzip.decompress(source.read_bytes());assert sha256(raw).hexdigest()==witness['layout_sha256']
 result={'status':'PASS_INDEPENDENT_TWO_EVALUATION_VISIBILITY','binary_ranks':dict(hist),'one_vector_negative_control_ranks':dict(one_hist),'first_actual_plane_witness':first,'author_rank_code_imported':False,'actual_H_words_used':True,'field_scalar_expansion':'four binary columns for every GF16 vector','scope':'visibility only; no quotient compression, H/D code or new kappa','pins':[{'path':str(p),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [witness_path,a.author/'search.py',a.basis,source]]}
 labelled=[('author/output/WITNESS.json',witness_path),('author/search.py',a.author/'search.py'),('BASIS.json',a.basis),('native/bit-all111-tight-port-atlas/LAYOUT.json.gz',source)]
 result['pins']=[{'path':label,'sha256':sha256(p.read_bytes()).hexdigest()}for label,p in labelled]
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status']);print(json.dumps({k:result[k]for k in ['binary_ranks','one_vector_negative_control_ranks']},sort_keys=True))
if __name__=='__main__':main()

