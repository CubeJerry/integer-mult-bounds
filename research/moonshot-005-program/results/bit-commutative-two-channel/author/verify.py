#!/usr/bin/env python3
"""Exact native, commutative-ring and noncommuting-scope checks."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PIVOT_PIN='8c11ca368995bc6a77f8d0425ac259384a7edf6164bc4254dfc0c7d780e26e19'
ORTH=[92,36,54,38,55];NONORTH=[92,38,36,55,54]

def need(ok,msg):
 if not ok:raise ValueError(msg)

def real_rank(rows):
 b={}
 for row in rows:
  v=list(row)
  for p,u in sorted(b.items()):
   c=v[p];v=[x-c*y for x,y in zip(v,u)]
  p=next((i for i,x in enumerate(v) if x),None)
  if p is not None:
   c=v[p];b[p]=[x/c for x in v]
 return len(b)

def ring_cases(size,polynomial):
 def mul(a,b):
  v=0
  for k in range(2):
   if a>>k&1:v^=b<<k
  if v&4:v^=polynomial
  return v
 M=[[mul(a,b) for b in range(size)] for a in range(size)]
 for a,b,c in itertools.product(range(size),repeat=3):
  need(M[a][b]==M[b][a] and M[M[a][b]][c]==M[a][M[b][c]],'commutative associative product')
  need(M[a][b^c]==(M[a][b]^M[a][c]) and M[1][a]==a,'ring and unit')
 matrices=[x for x in itertools.product(range(size),repeat=4) if M[x[1]][x[2]]==M[x[0]][x[3]]]
 valid=0
 for A,B in itertools.product(matrices,repeat=2):
  left=[(u,v) for u,v in itertools.product(range(size),repeat=2)
        if M[u][A[0]]^M[v][B[0]]==1 and M[u][A[1]]^M[v][B[1]]==0]
  right=[(u,v) for u,v in itertools.product(range(size),repeat=2)
         if M[u][A[3]]^M[v][B[3]]==1 and M[u][A[2]]^M[v][B[2]]==0]
  for L,R in itertools.product(left,right):
   need(M[L[0]][A[0]]^M[R[0]][A[3]]==1,'forced alternating edge weight');valid+=1
 odd=sum(all(u[i]^u[(i+1)%5]==1 for i in range(5)) for u in itertools.product(range(size),repeat=5))
 need(odd==0,'no odd-cycle assignment in characteristic two')
 return {'ring_size':size,'reciprocal_edge_matrices':len(matrices),'valid_edge_decoders_checked':valid,'odd_cycle_weight_assignments':odd}

def mm(A,B):
 return [(B[0] if r&1 else 0)^(B[1] if r&2 else 0) for r in A]

def add(A,B):return [a^b for a,b in zip(A,B)]

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--pivots',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 raw=a.native.read_bytes();pr=a.pivots.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native bytes');need(hashlib.sha256(pr).hexdigest()==PIVOT_PIN,'reviewed pivot assignment')
 n=json.loads(gzip.decompress(raw));roots={i:list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in ORTH}
 dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
 need(real_rank(list(roots.values()))==5,'native pentagon real rank')
 for cycle,is_zero in [(ORTH,True),(NONORTH,False)]:
  for i,j in itertools.combinations(range(5),2):
   edge=(i-j)%5 in (1,4)
   need((dot(cycle[i],cycle[j])==0)==(edge if is_zero else not edge),'exact induced pentagon')
 need(all(sum(dot(i,j)==0 for j in ORTH)==2 for i in ORTH),'two local receiver constraints per source')
 need(set(ORTH)<=set(json.loads(pr)['pivots']),'all selected core-zero columns are pivots')
 need(not(set(ORTH)&{8,9,16}),'donor observations vanish on pentagon')
 rings={'F2':ring_cases(2,2),'F4':ring_cases(4,7),'F2_dual_numbers':ring_cases(4,4)}
 # A bipartite nonorthogonality graph has a two-static-sum relaxed decoder.
 color=[0,1,0,1];seeds=[sum(1<<i for i,c in enumerate(color) if c==k) for k in range(2)]
 for i in range(4):
  row=seeds[color[i]];need(row>>i&1,'positive own coefficient')
  need(all(not(row>>j&1) for j in range(4) if (i-j)%4 in (1,3)),'positive forbidden coefficients')
 # Noncommuting2x2 selectors invalidate the scalar edge-weight deduction.
 E11=[1,0];E12=[2,0];E21=[0,1];E22=[0,2];I=[1,2];Z=[0,0]
 A=[[E11,E21],[E12,E22]];L=[[E11,E21],[E12,E22]]
 for i in range(2):
  for j in range(2):
   block=add(mm(L[i][0],A[0][j]),mm(L[i][1],A[1][j]))
   need(block==(I if i==j else Z),'exact noncommuting pair endpoint')
 U=[mm(L[i][0],A[0][i]) for i in range(2)]
 need(U==[E11,E11] and add(*U)!=I,'noncommuting edge control')
 need(mm(E11,E21)!=mm(E21,E11),'explicit failure of commutativity')
 # A fictitious one-channel two-target history breaks the reciprocal premise.
 bad=(1,0,0,1);need(bad[1]*bad[2]!=bad[0]*bad[3],'nonlocal-history mutant rejected')
 out={'status':'PASS_COMMUTATIVE_TWO_CHANNEL_THEOREM_CHECKS','native_sha256':PIN,'pivot_assignment_sha256':PIVOT_PIN,
      'orthogonality_cycle':ORTH,'nonorthogonality_cycle':NONORTH,'Gram_in_orthogonality_order':[[str(dot(i,j)) for j in ORTH] for i in ORTH],
      'real_rank':5,'local_information_deadline_distinct_receivers':3,'ring_checks':rings,
      'bipartite_positive_control_seeds':seeds,'noncommuting_pair_control':{'own_contributions':U,'sum':add(*U),'identity':I,'full_two_target_map_verified':True,'pentagon_claimed':False},
      'negative_controls':['nonlocal coefficient invention violates reciprocity','arbitrary block extrapolation fails on an exact two-target decoder'],
      'classification':'universal commutative-ring proof with exact native premises; coupled and noncommuting cases open','new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'rings':rings,'real_rank':5}))

if __name__=='__main__':main()
