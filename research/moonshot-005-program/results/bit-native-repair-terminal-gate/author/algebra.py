#!/usr/bin/env python3
"""Exact native correction algebra and masked rank repair exploration."""
import argparse,hashlib,json,itertools
from pathlib import Path
SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
PIN='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'

def rref(rows,n):
 a=list(rows);piv=[];k=0
 for j in range(n):
  p=next((i for i in range(k,len(a))if a[i]>>j&1),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k]
  for i in range(len(a)):
   if i!=k and a[i]>>j&1:a[i]^=a[k]
  piv.append(j);k+=1
 return a[:k],piv

def kernel(rows,n):
 a,piv=rref(rows,n);return [sum(((a[k]>>j)&1)<<p for k,p in enumerate(piv))^(1<<j)for j in range(n)if j not in piv]

def product(a,b):
 out=[]
 for x in a:
  z=0
  while x:
   p=(x&-x).bit_length()-1;z^=b[p];x&=x-1
  out.append(z)
 return out

def coords(x):return [i for i in range(x.bit_length())if x>>i&1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
 raw=(args.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;R=json.loads(raw)['native_roots'];n=len(R)
 N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
 K=[x^(1<<i)for i,x in enumerate(N)];kern=kernel(N,n);U=[sum(((N[i]>>j)&1)<<(j-8)for j in range(8,n))for i in range(8,n)];ukern=kernel(U,n-8)
 NN=product(N,N);KK=product(K,K)
 out={'source_pin':PIN,'native_rank':len(rref(N,n)[0]),'canonical_rank':len(rref(K,n)[0]),'N_kernel_supports':list(map(coords,kern)),
      'unknown_rank':len(rref(U,n-8)[0]),'unknown_kernel_supports':[[i+8 for i in coords(z)]for z in ukern],
      'K2_rank':len(rref(KK,n)[0]),'N2_plus_I_rank':len(rref([x^(1<<i)for i,x in enumerate(NN)],n)[0]),
      'K_kernel_part':[[hex(x)for x in kern]],'N_rows':list(map(hex,N)),'unknown_N_rows':list(map(hex,U))}
 # Rank3 native-supported corrections which repair N to invertibility:
 # pick row/column triples with nonsingular kernel projections and legal
 # native pair edges, then check the complete modified N.
 sig=[sum(((z>>i)&1)<<k for k,z in enumerate(kern))for i in range(n)]
 repairs=[]
 for ii in itertools.combinations(range(n),3):
  if len(rref([sig[i]for i in ii],3)[0])!=3:continue
  for jj in itertools.product(*[[j for j in range(n)if N[i]>>j&1 and sig[j]]for i in ii]):
   if len(set(jj))!=3 or len(rref([sig[j]for j in jj],3)[0])!=3:continue
   M=N[:]
   for i,j in zip(ii,jj):M[i]^=1<<j
   if len(rref(M,n)[0])==n:
    repairs.append({'removed_native_edges':list(map(list,zip(ii,jj))),'rank':n,'row_kernel_signatures':[sig[i]for i in ii],'column_kernel_signatures':[sig[j]for j in jj]});break
  if repairs:break
 out['first_native_mask_rank3_repair']=repairs
 args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if not k.endswith('_rows')},indent=2))
if __name__=='__main__':main()
