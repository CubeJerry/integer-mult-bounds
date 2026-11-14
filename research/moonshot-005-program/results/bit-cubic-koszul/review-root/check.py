#!/usr/bin/env python3
"""Independent native cubic construction and exterior-complex certificate."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
 if not c:raise ValueError(m)
def basis(words):
 out={}
 for w in words:
  while w:
   p=w.bit_length()-1
   if p in out:w^=out[p]
   else:out[p]=w;break
 return out
def rem(w,b):
 for p in sorted(b,reverse=True):
  if w>>p&1:w^=b[p]
 return w
def short(words,mask,N):
 piv={};out=[]
 for full in words:
  bad=full&(((1<<N)-1)^mask);r=full
  while bad:
   p=bad.bit_length()-1
   if p in piv:
    b,f=piv[p];bad^=b;r^=f
   else:piv[p]=(bad,r);break
  else:out.append(r)
 return basis(out)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def run(repo):
 raw=(repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw))
 roots=[list(map(F,w['frames'][str(w['start'][i])]['B'][0]))for i in range(111)]
 K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(roots))for i,r in enumerate(roots)];N=111;allbits=(1<<N)-1
 polar=[r^allbits for r in K];chosen=(0,1,2,4,8,14,30,59)
 gram=[sum(((polar[i]>>j)&1)<<k for k,j in enumerate(chosen))for i in chosen]
 need(gram==[224,208,176,112,238,221,187,119],'independent coordinate basis')
 inverse={sum(((g&x).bit_count()%2)<<k for k,g in enumerate(gram)):x for x in range(256)};need(len(inverse)==256,'nondegenerate polar form')
 coords=[inverse[sum(((polar[i]>>j)&1)<<k for k,i in enumerate(chosen))]for j in range(N)]
 def bil(a,b):return sum(((a>>j)&1)*((gram[j]&b).bit_count()%2)for j in range(8))%2
 def q(a):return (a.bit_count()+sum(((a>>i)&1)*((a>>j)&1)*((gram[i]>>j)&1)for i,j in itertools.combinations(range(8),2)))%2
 need(len(set(coords))==111 and all(q(a)for a in coords),'native quadric points')
 need(all(bil(a,b)==int(i!=j and dot(roots[i],roots[j])!=0)for i,a in enumerate(coords)for j,b in enumerate(coords)),'literal real/polar pairs')
 full=[a for a in range(256)if q(a)];need(len(full)==120,'full quadric')
 def monomials(d,points):
  return[sum(int(a&m==m)<<j for j,a in enumerate(points))for r in range(d+1)for S in itertools.combinations(range(8),r)for m in [sum(1<<i for i in S)]]
 full2=basis(monomials(2,full));full3=basis(monomials(3,full));Q2=basis(monomials(2,coords));Q3=basis(monomials(3,coords))
 need(len(full2)==len(Q2)==36 and len(full3)==len(Q3)==84,'ranks and injective puncturing')
 need(all((a&b).bit_count()%2==0 for a in full2.values()for b in full3.values()),'full dual pairing')
 # Construct the local modes afresh in a different source coordinate basis.
 sizes=Counter();locals_=[]
 for i,a in enumerate(coords):
  e=next(x for x in range(1,256)if q(x)==0 and bil(a,x));H=[e,a^e]
  for _ in range(3):
   available=[x for x in range(1,256)if all(not bil(x,h)for h in H)]
   e=next(x for x in available if not q(x));f=next(x for x in available if not q(x)and bil(e,x));H.extend((e,f))
  need(len(basis(H))==8 and all(not q(h)for h in H),'hyperbolic basis')
  need(all(bil(H[j],H[k])==int(j//2==k//2 and j!=k)for j in range(8)for k in range(8)),'hyperbolic Gram')
  def trans(x):return sum(bil(x,H[j^1])<<j for j in range(8))
  need(trans(a)==3 and all(q(x)==sum((trans(x)>>(2*j)&1)*(trans(x)>>(2*j+1)&1)for j in range(4))%2 for x in range(256)),'quadratic basis identity')
  modes=[]
  for bits in itertools.product((0,1),repeat=3):
   mask=sum(1<<(2*j+2+b)for j,b in enumerate(bits));support=[x for x in full if not(trans(x)&mask)]
   need(len(support)==8 and a in support and all(not bil(x,y)for x,y in itertools.combinations(support,2)),'explicit full eight-clique')
   mode=sum(int(x in support)<<j for j,x in enumerate(coords));sizes[mode.bit_count()]+=1
   need(mode>>i&1 and not(mode&~K[i])and rem(mode,Q3)==0,'native own-one cubic')
   modes.append(mode)
  products=basis(K[i]&v for v in Q2.values());local=short(Q3.values(),K[i],N)
  need(len(products)==28 and len(local)==36,'local dimensions')
  need(len(basis(list(products.values())+modes))==36 and all(rem(v,local)==0 for v in modes),'independent constructive local decomposition')
  need(len(basis(list(products.values())+modes[:-1]))==35,'omit-one-mode negative control')
  locals_.append(local)
 # Independently certify d squared zero and the finite middle-degree dimensions.
 complexes={}
 for m in(3,4):
  data=[];ranks={}
  for r in range(2*m+1):
   dom=[sum(1<<i for i in S)for S in itertools.combinations(range(2*m),r)];cod=[sum(1<<i for i in S)for S in itertools.combinations(range(2*m),r+2)]if r+2<=2*m else[];idx={v:j for j,v in enumerate(cod)}
   images=[]
   for v in dom:
    image=0
    for j in range(m):
     pair=3<<(2*j)
     if not(v&pair):image^=1<<idx[v|pair]
    images.append(image)
   rank=len(basis(images));cohom=len(dom)-rank-ranks.get(r-2,0);need(cohom==(2**m if r==m else 0),'middle cohomology')
   ranks[r]=rank;data.append({'degree':r,'rank':rank,'cohomology':cohom})
  complexes[str(m)]=data
 return{'status':'PASS_INDEPENDENT_NATIVE_CUBIC_CONSTRUCTION','source_sha256':PIN,'independent_coordinate_basis':chosen,'global_ranks':{'Q2':36,'Q3':84},'full_duality_verified':True,'all_receiver_local_dimensions':{'product':28,'cubic':36,'explicit_new_modes':8},'native_explicit_mode_size_histogram':dict(sorted(sizes.items())),'omit_one_mode_control_rank':35,'exterior_complexes':complexes,'physical_source':False,'no_new_kappa':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repo);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
