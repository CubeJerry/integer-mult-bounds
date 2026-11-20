#!/usr/bin/env python3
"""Rebuild the true forward H/D and adjoint K/F transfer and verify raw original addresses."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
import gzip,importlib.util,json
from pathlib import Path
import numpy as np

def mod(p,name):
 s=importlib.util.spec_from_file_location(name,p);z=importlib.util.module_from_spec(s);s.loader.exec_module(z);return z

def req(x,msg):
 if not x:raise ValueError(msg)

def load(path,pin):
 raw=gzip.decompress(path.read_bytes());req(sha256(raw).hexdigest()==pin,'native '+path.name);return json.loads(raw)

def binary_rows(A,f):
 encoded=[]
 for row in A:
  work=[0]*6
  for j,c in enumerate(row):
   for t in range(6):
    v=int(f.MUL[c,1<<t]);ix=6*j+t
    for q in range(6):
     if v>>q&1:work[q]|=1<<ix
  encoded.extend(work)
 return encoded

def price(A,f):
 B=binary_rows(A,f);count=0
 for c in range(len(B)):
  t=next(u for u in range(c,len(B)) if B[u]>>c&1)
  if t!=c:B[c],B[t]=B[t],B[c];count+=3
  for t in range(len(B)):
   if t!=c and B[t]>>c&1:B[t]^=B[c];count+=1
 req(B==[1<<i for i in range(len(B))],'all six physical basis bits');return count

def extension(f,M,earliest=True):
 # Extend a row set by coordinate rows, in the exact requested wire order.
 n=M.shape[1];r=len(M);used=[];B=M.copy()
 req(f.eliminate(B)[0]==r,'independent before completing a physical word')
 if not earliest:
  # Lexicographic pivots of B, then its complementary coordinate rows.
  piv=[]
  for t in range(n):
   if f.eliminate(M[:,piv+[t]])[0]>len(piv):piv.append(t)
   if len(piv)==r:break
  return np.eye(n,dtype=np.uint8)[[t for t in range(n) if t not in piv]]
 for e in np.eye(n,dtype=np.uint8):
  C=np.vstack([B,e]);r2=f.eliminate(C)[0]
  if r2>r:used.append(e);B=C;r=r2
  if r==n:break
 return np.array(used,dtype=np.uint8)

def dword(n,W):
 f=n.f;ids=n.mid[120];m=sum(n.routes[r][0]=='X' for r in ids);req(len(ids)==36 and m==19,'native two-wave D120')
 cols=defaultdict(list);rows=defaultdict(list)
 for t,r in enumerate(ids):
  ph,_,_,h,_,k,_,_=n.routes[r]
  if h is not None:cols[h].append(t)
  if k is not None:rows[k].append(t)
 hs=sorted(cols);ks=sorted(rows)
 req(len(hs)==len(ks)==16 and all(len(cols[h])==2 for h in hs) and all(len(rows[k])==2 for k in ks),'genuine two-lane proper D labels')
 A=np.zeros((36,36),dtype=np.uint8)
 for b in range(2):A[np.ix_([rows[k][b] for k in ks],[cols[h][b] for h in hs])]=W
 hub=[t for t,r in enumerate(ids[:m]) if n.routes[r][5] is None]
 ground=[m+t for t,r in enumerate(ids[m:]) if n.routes[r][3] is None]
 req(len(hub)==len(ground)==4,'four true closures and four Ground inputs')
 A[hub,:m]=extension(f,A[[v for v in range(m) if v not in hub],:m]);good=[u for u in range(m,36) if u not in ground]
 A[m:,ground]=extension(f,A[m:,good].T).T
 req(f.eliminate(A)[0]==36 and not A[:m,m:].any(),'true causal D word')
 c=A[m:,:m];snapshot=6*sum(np.any(c,axis=0));bills={'E':8*price(A[:m,:m],f),'L':8*price(A[m:,m:],f),
 'cross':8*sum(int(u).bit_count() for u in binary_rows(c,f)),'snapshot_ADD_INIT_CLEAR':int(8*snapshot)}
 return A,bills

class KFacet:
 def __init__(self,n,base):
  self.n=n;self.f=n.f
  d=base/'bit-gf64-actual-k-atlas/author/output'
  self.K=load(d/'SPREAD-OWNERS.json.gz','513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0')
  raw=load(d/'TEMPLATES.json.gz','6691b46a45b253e1e48f073f2114aed0c817e786b7efe7dce3dfa440c01cc73d')
  for m in (9,36):
   U=[1<<t for t in range(6*m)]
   for a,b in raw[str(m)]:U[a]^=U[b]
   req(U==binary_rows(self.f.power_matrix(range(1,m+1),m).T,self.f),'genuine binary right template equals field adjoint V')

 def matrix(self,i,ids):
  n=self.n;f=n.f;keep=set(ids);response={};native=set(range(111));first=set([h for h in n.n.hlist[i] if n.n.early[i,h]==15][:12]);
  scales={49:2,97:2,53:1,77:1,93:1,8:1,82:1,58:1,106:4,31:1,105:1}
  for v,h in enumerate(n.n.hlist[i],1):
   hd=self.K[str(h)];C=Counter();duals={};data=[];quota=n.n.early[i,h]//15;size=len(n.n.H[h]&native)
   pow=f.power_matrix([v],16)[0];der=np.zeros(16,dtype=np.uint8);der[1::2]=pow[:-1:2]
   for ph,ins,outs in hd['stripes']:
    m=len(ins);stripe=C[ph,m];C[ph,m]+=1
    if m!=9:
     req(not set(ins)&keep,'D120 lies solely in marked K component');continue
    data.append((ins,outs))
    for t,r in enumerate(outs):
     rt=n.routes[r];M=np.zeros(96,dtype=np.uint8);destination=rt[7] if ph=='X' else rt[1];req(rt[5]==h and rt[0]==ph,'actual native K stripe')
     if destination==i:
      derivative=False;scale=1
      if size==3 and quota==2:ch=t%3+3*stripe;req(ph=='Y','fully late receiver')
      elif size==2 and quota==2:ch=t;req(ph=='Y' and t<6,'large true terminal')
      elif size==1:
       ch=t if t<6 else t-6;derivative=t>=6;scale=scales[i] if derivative else 1
      else:ch=t%3+(0 if ((h in first)==(ph=='Y')) else 3)
      M[16*ch:16*(ch+1)]=f.MUL[scale,der if derivative else pow]
     duals[r]=M
   for early,late in hd['early_cache_to_late']:
    if late in duals:
     req(early in duals and n.routes[early][0]=='X' and n.routes[late][0]=='Y','right cached shear of genuine same resolved component');duals[early]^=duals[late]
   for ins,outs in data:
    ix=[v for v,r in enumerate(ins) if r in keep]
    if ix:
     D=f.matmul(n.V[ix],np.vstack([duals[r]for r in outs]))
     for t,row in zip(ix,D):response[ins[t]]=row
  req(set(response)==keep,'all eight genuine D output holders reach selected K/F system')
  return np.vstack([response[r] for r in ids]).T

def evaluate(n,kf,f,raw,reference,retained):
 stars={int(k):v for k,v in raw['stars'].items()};n.cache.clear();n.early_rank.clear()
 def frame(j,h,t,q,half):
  v=stars[j];F=np.asarray(v['F'][str(h)],dtype=np.uint8);P=np.asarray(v['P'][str(h)],dtype=np.uint8)
  req(F.shape==(3,48) and P.shape==(6,6) and f.eliminate(P)[0]==6,'fixed six genuine frame inputs')
  B=f.matmul(P,np.kron(np.eye(2,dtype=np.uint8),F))
  return np.vstack([B,v['Q'][str(h)]]).astype(np.uint8) if q==3 else B
 n.frame=frame
 A,bill=dword(n,np.asarray(raw['W'],dtype=np.uint8));ids=n.mid[120];targets=raw['receivers'];U={int(i):np.asarray(x,dtype=np.uint8)for i,x in raw['U'].items()}
 native=set(range(111));is0=[i for i in range(111)if n.n.D[120]<=n.n.adj[i]];js=sorted(n.n.D[120]&native);req(set(js)==set(stars) and all(i!=80 for i in is0) and 10 not in js,'identity S028 rectangle')
 cuts=0;boundaries={};counts=Counter();untouched={};calib={};legal=0
 for j in js:
  T=n.rows(j);input_pos=[t for t,r in enumerate(ids)if r in T]
  for i in is0:
   op=[t for t,r in enumerate(ids) if n.routes[r][5] in n.n.hlist[i]]
   req(f.eliminate(A[np.ix_(op,input_pos)])[0]==8,'all native true D sections');legal+=1
  for i in n.n.adj[j]&native:
   ds,H,blocks=n.marked(i,j);cuts+=1
   if i not in targets:continue
   seq=[t for t,r in enumerate(ids) if n.routes[r][5] in n.n.hlist[i]];L=np.kron(np.eye(2,dtype=np.uint8),U[i]);off=np.vstack([M for d,M in blocks.items() if d!=120]);req(f.eliminate(off)[0]==88 and not f.matmul(off,L).any(),'precisely the eight isolated original inputs')
   dvec=f.matmul(A[np.ix_(seq,input_pos)],np.vstack([T[ids[t]] for t in input_pos]))
   val=f.matmul(dvec,L);req(f.eliminate(val)[0]==8,'complete D response on the labelled original coordinates')
   if i in boundaries:req(np.array_equal(val,boundaries[i][1]),'literal common response in same physical holder order')
   else:boundaries[i]=([ids[t] for t in seq],val)
   if j in n.c.donors and retained:
    if i in untouched:req(np.array_equal(dvec,untouched[i]),'unrestricted equality across the three retained H263 source stars')
    untouched[i]=dvec
   counts[i]+=1
 if retained:
  for j in n.c.donors:
   v=stars[j]
   for h in n.n.hlist[j]:
    expected=(np.eye(48,dtype=np.uint8)[3*n.c.ix[j]:3*(n.c.ix[j]+1)] if h==263 else np.asarray(reference['off_H'][str(n.c.point[j][h])],dtype=np.uint8))
    req(np.array_equal(v['F'][str(h)],expected),'retained every H263 and off-chart scalar quotient');
   req(np.array_equal(v['P']['263'],np.eye(6,dtype=np.uint8)),'original unframed H263 input')
 swaps={16*(3*t+b)+8*l+e:96*e+(3*l+b)*16+t for t in range(16)for b in range(3)for l in range(2)for e in range(8)}
 seen=set();cycles=Counter()
 for i in swaps:
  if i in seen:continue
  p=i;m=0
  while p not in seen:seen.add(p);m+=1;p=swaps[p]
  cycles[m]+=1
 cost_per_F=18*(768-sum(cycles.values())); req(cost_per_F==11880,'genuine original-address relabelling')
 for i,(rids,V) in boundaries.items():
  R=kf.matrix(i,rids);raw_img=f.matmul(R,V);U0=U[i];E=np.zeros((96,8),dtype=np.uint8)
  for half in range(2):
   for t in range(16):
    for b in range(3):E[(3*half+b)*16+t,4*half:4*half+4]=U0[3*t+b]
  def basis(M):return np.hstack([M,extension(f,M.T,False).T])
  XO=basis(raw_img);r,inv=f.eliminate(XO,np.eye(96,dtype=np.uint8));req(r==96,'actual output coordinates extend to a basis')
  C=f.matmul(basis(E),inv);req(f.eliminate(C)[0]==96 and np.array_equal(f.matmul(C,raw_img),E),'genuine terminal correction')
  # The two actual raw full-bank address orders differ. Verify every source basis
  # coefficient in the terminal physical bank after the paid permutation.
  for e in range(8):
   before=np.zeros((768,8),dtype=np.uint8);before[96*e:96*(e+1)]=f.matmul(C,raw_img)
   after=before[[swaps[u] for u in range(768)]];want=np.zeros_like(after)
   for half in range(2):
    for t in range(48):want[16*t+8*half+e,4*half:4*half+4]=U0[t]
   req(np.array_equal(after,want),'actual final physical identity on original addresses')
  calib[i]={'eight_copy_field_calibration_ADD':8*price(C,f),'raw_permutation_ADD':cost_per_F,
            'calibration_sha256':sha256(C.tobytes()).hexdigest(),'all_twelve_source_endpoint_fibres':counts[i]}
 return {'designated_original_subspace_fibres':sum(counts.values()),'field_dimension_on_full_true_bank':64,'native_donor_cuts':cuts,
         'local_D_native_sections':legal,'D_price':bill,'true_terminal_calibrations':calib,'raw_768_label_permutation_cycles':cycles,
         'raw_768_label_permutation_binary_cost_per_facet_each_direction':cost_per_F}

def main():
 p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--tables',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 for k in ('packing-review','field-review','middle-review','h263-coefficients'):p.add_argument('--'+k,type=Path)
 a=p.parse_args();base=a.repo/'research/moonshot-005-program/results';r=mod(a.packing_review or base/'bit-spread-overlap-source/review/check.py','reviews');f=mod(a.field_review or base/'bit-spread-h263-source/review/check.py','field');m=mod(a.middle_review or base/'bit-spread-isolated-middle-cut/review/check.py','middle')
 coeff=load(a.h263_coefficients or base/'bit-spread-h263-source/author/output/COEFFICIENTS.json.gz','66fe6820e16e2a1a221cc59656b6356087f92b685ff121ef174a67c7c4890a0e');n=m.NativeLeft(a.repo,r,f,coeff,{'frames':[],'gauges':[]},{});kf=KFacet(n,base);out={}
 for label,name,pin,keep in [('retained_H263','TABLES.json.gz','688380f3b2e65521d6abff2e9267b6460039325bfc60c5b05a4c5cffa052c5d8',True),('all_D120_receivers','ALL-RECEIVERS.json.gz','3d2fbd7fc6eb74e006d6910f812d6d1a7487cf47c59d75844e08b69c8dd98747',False)]:
  raw=(a.tables/name).read_bytes();req(sha256(raw).hexdigest()==pin,'actual fixture bytes');out[label]=evaluate(n,kf,f,json.loads(gzip.decompress(raw)),coeff['components']['3'],keep)
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print([(k,d['designated_original_subspace_fibres']) for k,d in out.items()])

if __name__=='__main__':main()
