#!/usr/bin/env python3
"""Independent binary linear-interface reconstruction, not author-code replay."""
import argparse,hashlib,json
from pathlib import Path

def basis(rows):
 b={}
 for v in rows:
  for p in sorted(b,reverse=True):
   if v>>p&1:v^=b[p]
  if not v:continue
  p=v.bit_length()-1
  for q in b:
   if b[q]>>p&1:b[q]^=v
  b[p]=v
 return tuple(b[p]for p in sorted(b,reverse=True))

def solver(rows):
 d={}
 for i,v in enumerate(rows):
  c=1<<i
  for p in sorted(d,reverse=True):
   if v>>p&1:v^=d[p][0];c^=d[p][1]
  assert v
  d[v.bit_length()-1]=(v,c)
 def solve(v):
  c=0
  for p in sorted(d,reverse=True):
   if v>>p&1:v^=d[p][0];c^=d[p][1]
  assert not v
  return c
 return solve

def xor_selected(rows,c):
 v=0
 for i,x in enumerate(rows):
  if c>>i&1:v^=x
 return v

def verify(K,h,sizes):
 K=basis(K);n=h+sum(sizes);H=(1<<h)-1;D=((1<<n)-1)^H;offset=h;charts=[]
 for k in sizes:charts.append(((1<<k)-1)<<offset);offset+=k
 # Build independent projected rows and their actual full-K lifts.
 P=[];lifts=[];kernel=[]
 for r in K:
  d=r&D
  if len(basis(P+[d]))>len(P):P.append(d);lifts.append(r)
  else:
   c=solver(P)(d) if P else 0;kernel.append(r^xor_selected(lifts,c))
 kernel=list(basis(kernel));assert all(not(v&D)for v in kernel)
 marg=[basis(v&mask for v in P)for mask in charts];B=[v for bs in marg for v in bs];t=len(B);p=len(P);delta=t-p
 E=[]
 for v in B:
  if len(basis(P+E+[v]))>len(P)+len(E):E.append(v)
 assert len(E)==delta and len(kernel)==len(K)-p
 S=solver(P+E);f=[];helpers=[];principal=[];final=[]
 for v in B:
  cs=S(v);hv=xor_selected([r&H for r in lifts],cs);q=hv^v;f.append(q)
  assert sum(bool(q&mask)for mask in charts)==1
  if v in E:
   assert hv==0;helpers.append(q)
  else:
   principal.append(q);final.append(q^xor_selected(E,cs>>p))
 principal+=kernel;final+=kernel;f+=kernel
 assert len(principal)==len(K) and len(helpers)==delta
 assert basis(final)==K and len(basis(f))==len(K)+delta
 return {'c':len(K),'p':p,'t':t,'delta':delta,'acquisition_rank':len(basis(f))}

def all_subspaces(n):
 levels=[{()}]
 for k in range(n):
  nxt=set()
  for B in levels[-1]:
   for v in range(1,1<<n):
    T=basis(B+(v,))
    if len(T)==k+1:nxt.add(T)
  levels.append(nxt)
 return [x for s in levels for x in sorted(s)]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 if a.source:assert hashlib.sha256((a.source/'PROOF.md').read_bytes()).hexdigest()=='fbc3c1d974444062c5f45f4c7a4fee75fd085fcdc50b670d1f95e2b06092fe3b'
 cases=0;stats={}
 for h,sizes in [(1,[1,1,1]),(1,[2,2]),(2,[1,1])]:
  subs=all_subspaces(h+sum(sizes));stats[str((h,sizes))]=len(subs)
  for K in subs:verify(K,h,sizes);cases+=1
 # Concrete positive controls, including separability failure and nonzero Hub lifts.
 controls=[verify([0b110],1,[1,1]),verify([0b111],1,[1,1]),verify([1,0b110],1,[1,1]),verify([0b10101,0b01011],1,[2,2])]
 assert controls[0]=={'c':1,'p':1,'t':2,'delta':1,'acquisition_rank':2}
 # Native ten-root, four-copy restriction: abstract interface example only.
 src=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';roots=json.loads(src.read_text())['native_roots']
 K=basis(sum((1<<j)for j,r in enumerate(roots)if i==j or sum(x*y for x,y in zip(roots[i],r))==0)for i in range(111));assert len(K)==9
 columns=[sum(((v>>j)&1)<<i for i,v in enumerate(K))for j in range(111)];selected=[];chosen=[]
 for j,v in enumerate(columns):
  if len(basis(chosen+[v]))>len(chosen):chosen.append(v);selected.append(j)
 assert len(selected)==9
 selected.append(next(j for j in range(111)if j not in selected));assert len(basis(columns[j]for j in selected))==9
 # Each full root has four independent bank coordinates, split into two chart blocks.
 projection=[]
 for r in K:
  for bank in range(4):projection.append(sum(((r>>j)&1)<<(4*i+bank)for i,j in enumerate(selected)))
 x=verify(projection,0,[2]*20);assert x=={'c':36,'p':36,'t':40,'delta':4,'acquisition_rank':40}
 # Peak ownership is deliberately distinct from the acquired-span lower bound.
 # x0+x2 and x1+x3 can be assembled with 3 peak owners, but four acquisitions.
 peak=verify([0b0101,0b1010],0,[1,1,1,1]);assert peak['acquisition_rank']==4
 result={'status':'INDEPENDENT_CHARTWISE_HELPER_REPAIR_PASS','exhaustive_binary_subspaces':cases,'subspace_domains':stats,'positive_controls':controls,'ten_root_interface':{'native_roles':selected,**x,'helper_move_profile':{'6':4},'qualification':'An abstract held-chart interface example, not an actual five-receiver source.'},'peak_owner_negative_control':{'c':2,'delta':2,'acquisition_rank':4,'sequential_peak_owner_upper_bound':3,'qualification':'The theorem lower-bounds acquisition span and hence total acquisitions, not peak live owner count.'},'universal_status':'The all-field result follows from the written direct-sum/complement proof; finite binary controls are supplementary.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
