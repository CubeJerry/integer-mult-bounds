#!/usr/bin/env python3
"""Exact optimistic S8 point-feedback closure with short dual witnesses."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib

def rank(rows):
 B={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;break
 return len(B)
def solve(rows,v):
 B={}
 for k,r in enumerate(rows):
  c=1<<k
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p][0];c^=B[p][1]
   else:B[p]=(r,c);break
 c=0
 while v:
  p=v.bit_length()-1
  if p not in B:return None
  v^=B[p][0];c^=B[p][1]
 return c
def combine(rows,c):
 v=0
 for k,r in enumerate(rows):
  if c>>k&1:v^=r
 return v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();source='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=(a.repo/source).read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=[int((i!=72 and dot(R[72],r)!=0)^(dot([0,0,1,1,0,0,1,-1],r)!=0))for i,r in enumerate(R)];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)];indices=[1,3,4,6,73,74,77,78];S=[A[i]for i in indices];assert rank(S)==8 and rank(A)==15;initial=[1,6,73,75,77,79];expected=[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80];masks=[sum(1<<j for j in range(111)if dot(R[i],R[j])!=0)for i in range(111)]
 def fits(P):
  B=S+[1<<j for j in P];out=[]
  for i in range(111):
   c=solve([v&masks[i]for v in B],1<<i)
   if c is not None:
    v=combine(B,c);assert v&masks[i]==1<<i;out.append({'receiver':i,'source_coefficient_hex':hex(c),'fitting_row_hex':hex(v)})
  return out
 first=fits(initial);Z=[r['receiver']for r in first];assert Z==expected;final=fits(Z);assert[r['receiver']for r in final]==Z;assert rank(S+[1<<j for j in Z])==25
 cols=[sum(((s>>j)&1)<<k for k,s in enumerate(S))for j in range(111)];dual=[]
 for i in range(111):
  if i in Z:continue
  candidates=[j for j in range(111)if j!=i and j not in Z and masks[i]>>j&1];c=solve([cols[j]for j in candidates],cols[i]);assert c is not None;support=[i]+[j for k,j in enumerate(candidates)if c>>k&1];u=sum(1<<j for j in support);assert u>>i&1 and all(j not in Z and masks[i]>>j&1 for j in support);assert all((u&s).bit_count()%2==0 for s in S);assert len(support)<=9;dual.append({'receiver':i,'annihilator_support':support,'annihilator_hex':hex(u),'weight':len(support)})
 assert len(dual)==94
 for d in dual:
  i=d['receiver'];u=int(d['annihilator_hex'],16);assert((u^(1<<i))>>i&1)==0
  # The obstruction is deliberately bypassed by granting an unavailable raw input.
  assert solve(S+[1<<j for j in Z]+[1<<i],1<<i)is not None
 out={'status':'PASS_EXACT_S8_POINT_FEEDBACK_CLOSURE','source_path':source,'source_sha256':sha,'seed_native_indices':indices,'seed_rows_hex':[hex(s)for s in S],'initial_point_grants':initial,'first_round_ground_rank':rank(S+[1<<j for j in initial]),'first_round_fitting_witnesses':first,'closed_point_set':Z,'closed_ground_rank':25,'closed_fitting_witnesses':final,'excluded_receivers':94,'dual_witnesses':dual,'dual_weight_histogram':dict(Counter(d['weight']for d in dual)),'negative_and_scope_controls':['Every witness loses its required nonzero target pairing if its target coordinate is deleted.','Granting any excluded raw coordinate explicitly defeats its witness; that operation is outside completed-point feedback.'],'scope':'Arbitrary linear characteristic-two record algorithms whose global X information remains inside S8 plus raw coordinates of already completed outputs, with arbitrary proper raw source coordinates at each receiver and free point feedback. Nonpoint global innovations and genuinely nonlocal receiver information are excluded from this scoped model.','new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'closed',len(Z),'rank25','dual',len(dual),'weights',out['dual_weight_histogram'])
if __name__=='__main__':main()
