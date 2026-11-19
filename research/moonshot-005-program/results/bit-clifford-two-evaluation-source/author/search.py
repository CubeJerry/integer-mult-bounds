#!/usr/bin/env python3
"""Bounded exact search for a common two-vector Clifford visibility witness."""
from argparse import ArgumentParser
from pathlib import Path
from collections import Counter
import gzip,hashlib,json,random
import numpy as np
from sympy import Matrix

def binary_basis(vs):
 p={}
 for v in vs:
  while v:
   k=(v&-v).bit_length()-1
   if k not in p:p[k]=v;break
   v^=p[k]
 return list(p.values())

def gf_tables(q,poly):
 def mul(a,b):
  c=0
  while b:
   if b&1:c^=a
   a<<=1
   if a&q:a^=poly
   b>>=1
  return c
 tab=np.array([[mul(a,b) for b in range(q)] for a in range(q)],dtype=np.uint8)
 inv=np.zeros(q,dtype=np.uint8)
 for a in range(1,q):
  ks=np.flatnonzero(tab[a]==1);assert len(ks)==1;inv[a]=ks[0]
 return tab,inv

def ranks(a,tab,inv):
 a=a.copy();batch,m,n=a.shape;r=np.zeros(batch,dtype=np.int16);rows=np.arange(m)[None,:]
 for c in range(n):
  eligible=(rows>=r[:,None])&(a[:,:,c]!=0);chosen=eligible.argmax(axis=1)
  ids=np.flatnonzero(eligible.any(axis=1))
  if not len(ids):continue
  rr=r[ids];kk=chosen[ids];tmp=a[ids,rr,:].copy();a[ids,rr,:]=a[ids,kk,:];a[ids,kk,:]=tmp
  a[ids,rr,:]=tab[inv[a[ids,rr,c]][:,None],a[ids,rr,:]]
  factors=a[ids,:,c].copy();factors[np.arange(len(ids)),rr]=0
  a[ids]^=tab[factors[:,:,None],a[ids,rr,:][:,None,:]];r[ids]+=1
  if np.all(r==m):break
 return r

def main():
 ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
 ap.add_argument('--basis',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
 args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
 source=args.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
 raw=gzip.decompress(source.read_bytes());assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
 layout=json.loads(raw);roots=layout['root_table'];cert=json.loads(args.basis.read_text())
 basis=Matrix.hstack(*map(Matrix,cert['lattice_basis_columns']));assert abs(basis.det())==16
 gram=basis.T*basis/2;inverse=basis.inv();masks=[]
 for root in roots:
  v=inverse*Matrix(root);assert all(x.q==1 for x in v)
  masks.append(sum((int(x)&1)<<i for i,x in enumerate(v)))
 polar=[sum((int(gram[i,j])&1)<<j for j in range(8)) for i in range(8)]
 def bil(v,w):return sum((polar[i]&w).bit_count() for i in range(8) if v>>i&1)&1
 hyp=cert['hyperbolic_basis_masks'];coords={}
 for c in range(256):
  v=0
  for k in range(8):
   if c>>k&1:v^=hyp[k]
  coords[v]=c
 assert len(coords)==256
 gamma=np.zeros((256,16,16),dtype=np.uint8)
 for v,c in coords.items():
  for s in range(16):
   for k in range(4):
    if c>>(2*k+int(bool(s>>k&1)))&1:gamma[v,s^(1<<k),s]^=1
 pairs=[];envs=[]
 for i in range(111):
  wb=binary_basis(v for v in range(256) if bil(masks[i],v)==0);assert len(wb)==7
  for j in range(111):
   if j==i or sum(x*y for x,y in zip(roots[i],roots[j])):continue
   assert bil(masks[i],masks[j])==0
   env=np.concatenate([gamma[wb],(gamma[masks[j]][None,:,:]@gamma[wb])&1],axis=0)
   pairs.append([i,j]);envs.append(env)
 envs=np.array(envs,dtype=np.uint8);assert len(pairs)==6470
 trials=[];rng=random.Random(2711192026)
 for q,poly in [(16,0x13),(32,0x25),(64,0x43),(128,0x83)]:
  tab,inv=gf_tables(q,poly)
  for attempt in range(3):
   v=np.array([rng.randrange(q) for _ in range(16)],dtype=np.uint8)
   w=np.array([rng.randrange(q) for _ in range(16)],dtype=np.uint8)
   a=np.zeros((6470,16,28),dtype=np.uint8)
   for k in range(16):
    a[:,:,:14]^=(envs[:,:,:,k]*v[k]).transpose(0,2,1)
    a[:,:,14:]^=(envs[:,:,:,k]*w[k]).transpose(0,2,1)
   rr=ranks(a,tab,inv);hist=dict(sorted(Counter(map(int,rr)).items()))
   trial={'q':q,'attempt':attempt,'histogram':hist};trials.append(trial);print(json.dumps(trial),flush=True)
   if np.all(rr==16):
    result={'status':'FOUND_COMMON_TWO_EVALUATION_WITNESS','q':q,'polynomial':poly,'v':list(map(int,v)),'w':list(map(int,w)),'pairs':6470,'all_ranks':16,'same_vectors_for_every_donor':True,'trials':trials,'layout_sha256':hashlib.sha256(raw).hexdigest()}
    (args.out/'WITNESS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');return
 (args.out/'SEARCH.json').write_text(json.dumps(trials,indent=2)+'\n');print('NO_WITNESS_IN_BOUNDED_SEARCH')

if __name__=='__main__':main()
