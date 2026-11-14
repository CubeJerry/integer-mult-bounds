#!/usr/bin/env python3
"""Source support authentication and exact nonunitary row-union controls."""
import argparse,gzip,hashlib,itertools,json,random
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def root(q):
 s=[i for i in range(9)if q>>i&1]
 if len(s)==3:return [2 if i in s else -1 for i in range(9)]
 need(len(s)==7,'native root');a,b=[i for i in range(9)if i not in s];return [3*(int(i==a)-int(i==b))for i in range(9)]
def gram(q,r):return F(sum(x*y for x,y in zip(root(q),root(r))),18)
def mul(A,B):return [[sum(x*y for x,y in zip(row,col))for col in zip(*B)]for row in A]
def sp(A):return max((sum(x!=0 for x in row)for row in A),default=0)
def main(out):
 pins=json.loads((HERE/'SOURCE-PINS.json').read_text())
 for n,h in pins.items():need(hashlib.sha256((HERE/'source'/n).read_bytes()).hexdigest()==h,'source pin '+n)
 g=json.loads((HERE/'source/GEOMETRY.json').read_text());w=json.loads(gzip.decompress((HERE/'source/R0-WORD.json.gz').read_bytes()))
 q={int(h):z for h,z in g['normal_by_port'].items()};R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in w['logical_involution']['R_rows'].items()}
 need(len(q)==len(R)==112 and len(set(q.values()))==112,'112 actual distinct normals')
 checked=0
 for cl in g['classes']:
  for h in cl['ports']:
   expected={j:F(h==j)-gram(q[h],q[j])for j in cl['ports']};expected={j:c for j,c in expected.items()if c}
   need(R[h]==expected and len(expected)==4 and all(abs(c)==F(1,2)for c in expected.values()),'actual R row')
   for j in expected:
    shifts={0,q[h],q[j],q[h]^q[j]};need(len(shifts)==4,'physical block has four distinct translations')
    for V in (1,2,3):need(len(set(itertools.product(shifts,repeat=V)))==4**V,'finite tensor support control')
    checked+=1
 C=json.loads((HERE/'source/C-RESULT.json').read_text());hist={int(k):v for k,v in C['collision_codimension_histogram'].items()}
 need(sum(hist.values())==2688 and min(hist)==3,'authenticated affine collision premise')
 need(C['per_good_row_support']=='16*4^V','C support premise')
 good=[]
 for V in range(2,11):
  lo=1-F(24,2**(3*V));need(lo>0,'positive good-row fraction');good.append({'V':V,'fraction_lower':str(lo),'N_row_support':4**(V+1),'C_good_row_support':16*4**V,'one_query_support_before_ordinary':1+2**V})
 rng=random.Random(12014);tests=0
 for m,k,n in [(3,5,4),(8,8,8),(2,9,3),(1,4,1)]:
  for _ in range(30):
   A=[[rng.choice([0,0,0,-3,1,2])for _ in range(k)]for _ in range(m)];B=[[rng.choice([0,0,-2,1,4])for _ in range(n)]for _ in range(k)]
   need(sp(mul(A,B))<=sp(A)*sp(B),'row-union bound');tests+=1
 need(mul([[1,1]],[[1,-1],[-1,1]])==[[0,0]],'cancellation cannot enlarge support')
 need(sp(mul([[1000,1],[0,1]],[[1,1],[1,-1]]))==2,'unbounded coefficient control')
 linear=[]
 for V in range(1,8):
  n=2**V;A=[[int(i==j)for j in range(n)]for i in range(n)]
  for bit in range(V):
   B=[row[:]for row in A]
   for i in range(n):
    j=i^(1<<bit);B[i]=[A[i][x]+(1 if not(i>>bit&1)else -1)*A[j][x]for x in range(n)]
   A=B
  need(sp(A)==2**V,'linear ordinary branching builds exponential support');linear.append({'V':V,'ordinary_log_degree_allowance':V,'support':sp(A)})
 result={'status':'PASS_NONUNITARY_SUPPORT_DEPTH_CONTROLS','source_pins':pins,'actual_N_blocks_checked':checked,'N_support':'4^(V+1)','C_good_support':'16*4^V for V>=2','C_collision_codimension_histogram':hist,'finite_width_controls':good,'rectangular_nonunitary_product_controls':tests,'linear_ordinary_countercontrols':linear,'universal_proof':'Row-support union inequality in PROOF.md, not finite extrapolation.','scope':'Exact linear circuits; paid depth and ordinary branching only, no aggregate Gaussian-moment conclusion.','new_kappa':False}
 out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'blocks':checked,'matrix_controls':tests}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');main(p.parse_args().output)
