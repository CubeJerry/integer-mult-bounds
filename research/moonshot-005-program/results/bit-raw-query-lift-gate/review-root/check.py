#!/usr/bin/env python3
"""Independent native same-quotient/dual certificates and changed-D control."""
import argparse,hashlib,json,re
from pathlib import Path

def rank(rows):
 B={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in B:x^=B[p]
   else:B[p]=x;break
 return len(B)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def parity(a,b):return(a&b).bit_count()%2
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 nf=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(nf.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(nf.read_text())['native_roots'];assert hashlib.sha256(a.source.read_bytes()).hexdigest()=='4cea047c9f28a17c3379d3073a88b3a5d00e6e749214661c9d330a289824d060';w=json.loads(a.source.read_text())
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};R=[0]*8;k0=None
 for op in w['operations']:
  if op[0]=='INIT':vals[op[1]]=0
  elif op[0]=='ADD':
   x,y=op[1:]
   if x=='P0'and y=='Y0':assert k0 is None;k0=vals[x]
   if re.fullmatch(r'C\d+_\d+_[01]',x)and re.fullmatch(r'P[0-7]',y):R[int(y[1:])]^=vals[x]
   vals[y]^=vals[x]
  elif op[0]=='CLEAR':del vals[op[1]]
  elif op[0]=='MOVE':pass
  else:raise AssertionError(op)
 assert all(vals[f'X{i}']==1<<i for i in range(111));assert vals['Y0']==(1<<111)^1
 assert all(vals[f'Y{i}']==1<<(111+i)for i in range(1,111))
 cache={n:v for n,v in vals.items()if re.fullmatch(r'C\d+_\d+_[01]',n)};D=list(cache.values());mask=(1<<111)-1;assert len(D)==80 and all(x&~mask==0 for x in D)
 K=[sum(1<<j for j in range(111)if i==j or dot(roots[i],roots[j])==0)for i in range(111)];h=K[0]^K[4];W=[K[i]&sum(1<<j for j in range(111)if(h>>j&1)==(h>>i&1))for i in range(111)];A=D+W;B=[vals['P0'],k0,255]+R
 assert rank(D)==40 and rank(W)==15 and rank(A)==47 and rank(B)==11 and rank(D+B)==40
 cert=[]
 for i,j,support in [(8,11,[8,37,78]),(22,23,[22,33,61])]:
  z=sum(1<<b for b in support);dims=[]
  for v in [i,j]:
   local=sum(1<<b for b in range(111)if dot(roots[v],roots[b])==0);ad=rank(A)-rank([x&~local for x in A]);dd=rank(D)-rank([x&~local for x in D]);assert ad==dd;dims.append(ad);assert z&local==0
  assert rank(D+[W[i]^W[j]])==40 and all(parity(z,b)==0 for b in B) and parity(z,(1<<i)^(1<<j))==1
  assert parity(z,1<<i)==1 # granting the demanded point breaks this dual
  k_escape=[]
  for q in range(8):
   k=1<<q
   for n,row in cache.items():
    if n.startswith(f'C{q}_')and n.endswith('_0'):k^=row
   if parity(z,k):k_escape.append(q)
  cert.append({'receivers':[i,j],'intersection_dimensions':dims,'dual_support':support,'mixed_kernel_escape_axes':k_escape})
 assert cert[0]['intersection_dimensions']==[15,16] and cert[1]['intersection_dimensions']==[16,13]
 # Changed actual acquisition is outside the fixed-D gate.
 a0=sum(1<<i for i in [49,50,84,87,100,102]);a1=sum(1<<i for i in [18,20,70,72]);D2=D+[a0,a1];assert rank(D2)==42 and rank(D2+W)==48 and rank(D2+[W[14]^W[66]])==42
 assert rank(D2+[W[i]for i in[8,14,22,30,38,59]])==48
 out={'status':'PASS_ROOT_ARBITRARY_LIFT_DUALS','D_rank':40,'W_rank':15,'A_rank':47,'B_rank':11,'witnesses':cert,'changed_acquisition_control':{'D_rank':42,'W_intersection':9,'W_quotient':6},'scope':'Fixed spaces and all222 values independently rebuilt without author code; universal all-block section proof reviewed separately; no new kappa'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
