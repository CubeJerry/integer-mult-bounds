"""Exact generalized-inverse and compatibility controls over GF2."""
import itertools,json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def add(A,B):return [[a^b for a,b in zip(r,s)] for r,s in zip(A,B)]
def mul(A,B):return [[sum(a*B[k][j] for k,a in enumerate(r))%2 for j in range(len(B[0]))] for r in A]
def rank(A):
 b={}
 for row in A:
  r=sum(v<<j for j,v in enumerate(row))
  while r:
   p=r.bit_length()-1
   if p in b:r^=b[p]
   else:b[p]=r;break
 return len(b)
I=[[1,0],[0,1]];Z=[[0,0],[0,0]]
matrices=[[[a,b],[c,d]] for a,b,c,d in itertools.product([0,1],repeat=4)]
Pin=[[1,0,0,1],[0,1,1,0]];Xin=[[0,1,0,1],[1,0,1,1]];C=[[1,1],[1,0]]
counts={0:0,1:0,2:0};bad_compat=missing_kernel=0
for D in matrices:
 R=next(R for R in matrices if mul(mul(D,R),D)==D and mul(mul(R,D),R)==R)
 H=add(I,mul(R,D));nu=2-rank(D);counts[nu]+=1
 assert mul(H,H)==H and mul(D,H)==Z and rank(H)==nu
 assert mul(R,D)==add(I,H) and mul(mul(D,R),mul(D,R))==mul(D,R)
 W=mul(D,Pin);Pout=add(mul(C,Xin),W);compat=add(I,mul(D,R))
 assert mul(compat,W)==[[0]*4 for _ in range(2)]
 recovered=add(mul(R,add(Pout,mul(C,Xin))),mul(H,Pin));assert recovered==Pin
 # Factor H into a kernel-basis injection J and coordinates h.
 if nu==1:
  h=[next(row for row in H if any(row))];J=[[int(row==h[0])] for row in H]
  assert mul(J,h)==H and mul(h,J)==[[1]] and mul(h,R)==[[0,0]] and mul(D,J)==[[0],[0]]
 elif nu==2:assert H==I and R==Z
 else:assert H==Z
 if nu:
  assert mul(R,W)!=Pin;missing_kernel+=1
  v=next([[a],[b]] for a,b in itertools.product([0,1],repeat=2) if mul(compat,[[a],[b]])!=[[0],[0]])
  assert mul(D,mul(R,v))!=v;bad_compat+=1
# Ground cancellation: later pre-CLEAR values can lose all arriving modes.
arrival=Pin;cache=arrival;terminal=add(arrival,cache);assert terminal==[[0]*4 for _ in range(2)] and rank(arrival)==2
out={'status':'PASS_ALL16_BINARY_TWO_BY_TWO_THROUGH_BLOCKS','block_volume':2,'all_four_original_columns_checked':True,'nullity_counts':counts,'missing_kernel_coordinate_controls_rejected':missing_kernel,'incompatible_output_controls_rejected':bad_compat,'ground_cache_cancellation_loses_preCLEAR_modes':True,'first_arrival_ground_modes_retain_all_ground_history':True,'scope':'Exact local parameterization controls and zero-boundary countercontrol; general theorem and source geometry are proved/dependent separately.'}
p=Path(__file__).resolve().parent;(p/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
