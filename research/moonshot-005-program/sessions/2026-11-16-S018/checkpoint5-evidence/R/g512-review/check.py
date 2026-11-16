#!/usr/bin/env python3
"""Independent complete G512 source-class audit in bounded Gaussian integers."""
import argparse,hashlib,json,itertools
from collections import Counter,deque
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser()
for key in ['repo','proof','out']:p.add_argument('--'+key,type=Path,required=True)
o=p.parse_args();N=16
class M:
 def __init__(self,r,i=None,k=0):
  self.r=np.array(r,dtype=np.int64);self.i=np.zeros((N,N),dtype=np.int64)if i is None else np.array(i,dtype=np.int64);self.k=k
  while self.k and np.all(self.r%2==0)and np.all(self.i%2==0):self.r//=2;self.i//=2;self.k-=1
 def __matmul__(self,b):
  ar=max(int(np.max(np.abs(self.r))),int(np.max(np.abs(self.i))));br=max(int(np.max(np.abs(b.r))),int(np.max(np.abs(b.i))))
  assert 2*N*ar*br<2**62
  return M(self.r@b.r-self.i@b.i,self.r@b.i+self.i@b.r,self.k+b.k)
 def adj(self):return M(self.r.T,-self.i.T,self.k)
 def key(self):return(self.k,self.r.tobytes(),self.i.tobytes())
 def eq(self,b):return self.key()==b.key()
 def pow(self,n):
  a=self;v=I
  for _ in range(n):v=v@a
  return v
def mono(g):
 r=np.zeros((N,N),dtype=np.int64);i=r.copy()
 for c,(dst,ph)in enumerate(zip(*g)):
  r[dst,c]=[1,0,-1,0][ph];i[dst,c]=[0,1,0,-1][ph]
 return M(r,i)
def extract(A):
 assert A.k==0;dst=[];phase=[]
 for j in range(N):
  ix=np.flatnonzero((A.r[:,j]!=0)|(A.i[:,j]!=0));assert len(ix)==1;x=int(ix[0]);z=(int(A.r[x,j]),int(A.i[x,j]));assert z in [(1,0),(0,1),(-1,0),(0,-1)];dst.append(x);phase.append([(1,0),(0,1),(-1,0),(0,-1)].index(z))
 assert len(set(dst))==N
 return(tuple(dst),tuple(phase))
def gp(g,h):return(tuple(g[0][h[0][j]]for j in range(N)),tuple((h[1][j]+g[1][h[0][j]])%4 for j in range(N)))
ident=(tuple(range(N)),(0,)*N);I=mono(ident)
def group(gs):
 seen={ident};q=deque([ident])
 while q:
  x=q.popleft()
  for g in gs:
   z=gp(g,x)
   if z not in seen:seen.add(z);q.append(z)
 return seen
X=mono((tuple(j^2 for j in range(N)),(0,)*N));P=mono((tuple((j>>1)|((j&1)<<3)for j in range(N)),(0,)*N))
D=mono((tuple(range(N)),tuple(2*((j&1)*((j>>2)&1)*((j>>3)&1))for j in range(N))))
A=M(I.r+X.r,I.r-X.r,1)@D@P;Ai=A.adj();assert(A@Ai).eq(I)
A2=A@A;A3=A2@A;Ai2=Ai@Ai
Da=mono((tuple(range(N)),tuple(j&1 for j in range(N))));Db=mono((tuple(range(N)),tuple((j>>1)&1 for j in range(N))))
Ha=Ai2@Da.pow(2)@A2;Hb=Ai2@Db.pow(2)@A2
dst=[];ph=[]
for j in range(N):
 a,b,c,d=[(j>>k)&1 for k in range(4)];dst.append((c^(a*b))+2*d+4*a+8*b);ph.append((a*b+2*a*b*(c+d))%4)
R2=mono((tuple(dst),tuple(ph)))
Ba=mono((tuple(((j&1)<<1)|((j&2)>>1)|(j&12)for j in range(N)),(0,)*N))
J=R2.adj()@Ba@R2;Jg=extract(J)
core=mono((tuple((j&3)+4*(0,3,2,1)[j>>2]for j in range(N)),(0,)*N))
Qc=R2.adj()@core@R2;CZ=mono((tuple(range(N)),tuple(2*int((j&3)==3)for j in range(N))))
gens=[extract(T)for T in [Ha,Hb,Da,Db,CZ,Qc]];H=group(gens);G=group(gens+[Jg]);assert len(H)==256 and len(G)==512
assert H.isdisjoint({gp(g,Jg)for g in H})and H|{gp(g,Jg)for g in H}==G
assert len({(g[0],tuple((x-g[1][0])%4 for x in g[1]))for g in G})==512
def gaussian_rank(T):
 supports={}
 for r in range(N):
  cols=tuple(j for j in range(N)if T.r[r,j]or T.i[r,j]);supports.setdefault(cols,[]).append(r)
 sizes={len(c)for c in supports};assert len(sizes)==1;size=next(iter(sizes));rank=size.bit_length()-1
 assert size==1<<rank and len(supports)==N//size
 seen=set()
 for cols,rows in supports.items():
  assert len(rows)==size and not(seen&set(cols));seen.update(cols)
  vals=[];r0=rows[0];c0=cols[0]
  for r in rows:
   bits=0
   for k,c in enumerate(cols):
    x,y=int(T.r[r,c]),int(T.i[r,c]);assert x*x+y*y==1<<(2*T.k-rank)
    ar,ai=int(T.r[r0,c0]),int(T.i[r0,c0]);br,bi=int(T.r[r,c0]),int(T.i[r,c0]);cr,ci=int(T.r[r0,c]),int(T.i[r0,c])
    left=(x*ar-y*ai,x*ai+y*ar);right=(br*cr-bi*ci,br*ci+bi*cr)
    assert left==right or left==(-right[0],-right[1])
    if left!=right:bits|=1<<k
   vals.append(bits)
  span={0}
  for row in vals:
   if row not in span:span|={x^row for x in list(span)}
  assert set(vals)==span and len(span)==1<<rank
 return rank
even=Counter();odd=Counter();max_integer=0
for g in sorted(G):
 T=mono(g);extract(A2@T@Ai2)
 if g in H:extract(A@T@Ai)
 E=A3@T@A;O=A@J@A2@T@A
 even[gaussian_rank(E)]+=1;odd[gaussian_rank(O)]+=1
 max_integer=max(max_integer,int(np.max(np.abs(E.r))),int(np.max(np.abs(E.i))),int(np.max(np.abs(O.r))),int(np.max(np.abs(O.i))))
assert even=={4:512}and odd=={2:256,3:256}
prefix=[gaussian_rank(A@J@A),gaussian_rank(A@J@A2),gaussian_rank(A@J@Ai)];assert prefix==[2,3,2]
revcore=mono((tuple((j&3)+4*(0,1,3,2)[j>>2]for j in range(N)),(0,)*N));rev=R2.adj()@revcore@R2
escapes=[]
for name,T,want in [('spectator_swap',Ba,[2,4]),('reverse_CNOT',rev,[4,4])]:
 assert extract(T)not in G;extract(A2@T@Ai2);ranks=[gaussian_rank(A3@T@A),gaussian_rank(A@J@A2@T@A)];assert ranks==want
 escapes.append({'name':name,'outside_G512':True,'square_transport_monomial':True,'even_and_J_channel_ranks':ranks})
Pth=o.repo/'research/moonshot-005-program';deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-clean-first-column-exclusion/ADMISSION.md']
result={'status':'PASS_ROOT_COMPLETE_G512_COEFFICIENT_GATE_REVIEW','proof_sha256':hashlib.sha256(o.proof.read_bytes()).hexdigest(),'independent_arithmetic':'Separate Gaussian-integer matrices with power-of-two denominator; every integer product bounded before int64 multiplication, no modular samples or float tolerance.','actual_group_order':512,'clean_forward_subgroup_order':256,'exact_no_projective_duplicates':True,'complete_square_transport':True,'complete_clean_H_transport':True,'even_four_source_ranks':dict(even),'J_four_source_ranks':dict(odd),'J_prefix_ranks':prefix,'maximum_final_integer_coefficient':max_integer,'ordinary_coset_separation':'A² h hprime^-1 A^-2 is monomial; multiplying nonmonomial A J A^-1 cannot yield a monomial. Closed group and literal J inverse certify the entire finite-word premise.','ordinary_retraction_justification':'The ordinary coefficient algebra is a fixed finite-dimensional unital monomial algebra; ambient-invertible transition B has its inverse in that algebra. No physical free inverse is claimed.','surviving_escape_controls':escapes,'dependency_pins':{p:hashlib.sha256((Pth/p).read_bytes()).hexdigest()for p in deps},'scope':'Universal component-image/coset/inverse-cut proof independently read. Finite enumeration exhausts the explicitly defined512 group only; it is not failed caller search. No statement excludes the1536 enlargement or arbitrary ordinary first interfaces; no supplier or kappa.'}
o.out.parent.mkdir(parents=True,exist_ok=True);o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
