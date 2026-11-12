#!/usr/bin/env python3
"""Finite exact coverage for the separately proved all-field lifting theorem."""
import argparse,itertools,json
from fractions import Fraction as Q
from pathlib import Path

def need(b,m):
 if not b:raise ValueError(m)

def rank_mod(A,p):
 A=[list(r) for r in A];m=len(A);n=len(A[0]) if m else 0;k=0
 for j in range(n):
  i=next((i for i in range(k,m) if A[i][j]%p),None)
  if i is None:continue
  A[k],A[i]=A[i],A[k];c=pow(A[k][j]%p,-1,p);A[k]=[c*x%p for x in A[k]]
  for i in range(m):
   if i!=k:
    c=A[i][j]%p;A[i]=[(x-c*y)%p for x,y in zip(A[i],A[k])]
  k+=1
  if k==m:break
 return k

def matrices(m,n,p):
 for xs in itertools.product(range(p),repeat=m*n):yield tuple(tuple(xs[i*n:(i+1)*n]) for i in range(m))

def mm_mod(A,V,p):return tuple(tuple(sum(x*y for x,y in zip(row,col))%p for col in zip(*V)) for row in A)

def criterion(A,B,p):
 r=len(A[0]);d=len(B[0]);q=rank_mod(A,p);qb=rank_mod(B,p)
 return rank_mod([a+b for a,b in zip(A,B)],p)==q and d-qb<=r-q

def inverse(A):
 n=len(A);M=[[Q(v) for v in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
 for j in range(n):
  i=next(i for i in range(j,n) if M[i][j]);M[j],M[i]=M[i],M[j];c=M[j][j];M[j]=[v/c for v in M[j]]
  for i in range(n):
   if i!=j:
    c=M[i][j];M[i]=[v-c*w for v,w in zip(M[i],M[j])]
 return [row[n:] for row in M]

def mm(A,B):return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in zip(*B)] for row in A]

def rational_source():
 A=[[Q(-1,2)]*8,[Q(v,2) for v in [-1,-1,-1,-1,1,1,1,1]],[Q(v,2) for v in [-1,-1,1,1,-1,-1,1,1]],[Q(v,2) for v in [-1,1,-1,1,1,-1,1,-1]]]
 R=[[row[5],row[6]] for row in A];Z=[[Q(1),Q(-1)],[Q(1),Q(1)]];T=inverse(Z);B=mm(R,Z)
 need(T==[[Q(1,2),Q(1,2)],[Q(-1,2),Q(1,2)]],'actual T');need(all(row[7]==-row[4]+b[0] and row[3]==row[0]+b[1] for row,b in zip(A,B)),'actual two branch relations')
 dual=[list(c) for c in zip(*Z)];dual_inv=[list(c) for c in zip(*T)];I=[[Q(i==j) for j in range(2)] for i in range(2)];need(mm(Z,T)==I and mm(dual_inv,dual)==I,'actual inverse pair')
 return {'old_shared_columns':[[str(v) for v in row] for row in R],'requested_columns':[[str(v) for v in row] for row in B],'forward_change':[[str(v) for v in row] for row in T],'dual_change':[[str(v) for v in row] for row in dual],'minimum_added_paired_slots':0}

def main(out):
 coverage=[];checks=0
 for p,m,r in [(2,1,1),(2,2,1),(2,2,2),(2,2,3),(3,1,2),(3,2,2)]:
  for d in range(1,r+2):
   lifts=[V for V in matrices(r,d,p) if rank_mod(V,p)==d];count=0
   for A in matrices(m,r,p):
    actual={mm_mod(A,V,p) for V in lifts}
    for B in matrices(m,d,p):
     need((B in actual)==criterion(A,B,p),f'gate mismatch p={p},m={m},r={r},d={d},A={A},B={B}');count+=1
   coverage.append({'p':p,'m':m,'r':r,'d':d,'independent_lifts_enumerated_per_A':len(lifts),'A_B_pairs':count});checks+=count
 A=((1,0),(0,1));dup=((1,1),(0,0));A1=((1,0,0),(0,1,0));triple=((1,1,1),(0,0,0));A2=((1,0,0,0),(0,1,0,0));plusminus=((1,-1),(1,1));outside=((0,),(1,))
 controls={'two_equal_columns_need_one_kernel_slot':not criterion(A,dup,5) and criterion(A1,dup,5),'three_equal_columns_need_two_kernel_slots':not criterion(A1,triple,5) and criterion(A2,triple,5),'image_mismatch_not_repaired_by_nullity':not criterion(((1,0),(0,0)),outside,5),'characteristic_two_plusminus_not_invertible':not criterion(A,plusminus,2),'odd_characteristic_plusminus_valid':all(criterion(A,plusminus,p) for p in [3,5,7,11])}
 need(all(controls.values()),'negative controls');result={'status':'PASS_INVERTIBLE_COLUMN_REALIZATION_GATE','classification':'finite computational verification of a separately proved all-field algebraic criterion','coverage':coverage,'total_A_B_pairs':checks,'negative_controls':controls,'source_two_branch_instance':rational_source(),'minimum_slot_formula':'max(0,d-rank(B)-nullity(A)); only if im(B) subset im(A)','not_a_physical_admission_or_kappa_certificate':True};out.mkdir(parents=True,exist_ok=True);(out/'CHECK.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],checks)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
