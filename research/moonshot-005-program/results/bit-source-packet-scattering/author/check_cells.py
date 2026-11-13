"""Independent exact interleaved scattering and singular exchange controls."""
import json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def add(A,B):return [[a^b for a,b in zip(r,s)] for r,s in zip(A,B)]
def mul(A,B):return [[sum(a*B[k][j] for k,a in enumerate(r))%2 for j in range(len(B[0]))] for r in A]
def inv(A):
 n=len(A);R=[r.copy()+[int(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  p=next(i for i in range(j,n) if R[i][j]);R[j],R[p]=R[p],R[j]
  for i in range(n):
   if i!=j and R[i][j]:R[i]=[x^y for x,y in zip(R[i],R[j])]
 return [r[n:] for r in R]
I=[[1,0],[0,1]];O=[[0,0],[0,0]];A=[[1,1],[0,1]];B=[[1,0],[1,1]];N=[[0,1],[0,0]];assert mul(A,B)!=mul(B,A)
x=[[1,0,0,0],[0,1,0,0]];p=[[0,0,1,0],[0,0,0,1]]
# A packet visits upper F and leaves a cache BEFORE X later arrives there.
cacheF=p;poutF=mul(B,p)
xoutL=add(x,mul(A,poutF));poutL=add(poutF,mul(N,xoutL));Z=mul(A,poutL)
xoutF=add(xoutL,mul(B,cacheF))
DF=B;DL=add(I,mul(N,A));D0=A
for d in [DF,DL,D0]:assert mul(d,inv(d))==I
# Low-to-high inverse elimination, retaining the required factor order.
pinLG=mul(inv(DL),inv(D0));pinLL=mul(mul(inv(DL),N),x)
xoutLG=mul(A,pinLG);xoutLL=add(x,mul(A,pinLL))
pinFG=mul(inv(DF),pinLG);pinFL=mul(inv(DF),pinLL)
xoutFG=add(xoutLG,mul(B,pinFG));xoutFL=add(xoutLL,mul(B,pinFL))
for actual,g,l in [(poutF,pinLG,pinLL),(xoutL,xoutLG,xoutLL),(p,pinFG,pinFL),(xoutF,xoutFG,xoutFL)]:
 assert actual==add(mul(g,Z),l)
 assert all(not row[j] for row in l for j in [2,3])
# Empty packet cells have the empty invertible through-map.
assert inv([])==[]
# Two ADDs preserve the full pair while erasing packet-through dependence.
xe=add(x,p);pe=add(p,xe);assert pe==x and add(xe,pe)==p
full=[I[i]+I[i] for i in range(2)]+[I[i]+O[i] for i in range(2)]
assert mul(full,inv(full))==[[int(i==j) for j in range(4)] for i in range(4)]
assert all(not v for row in O for v in row)
# The earlier p contains columns absent from terminal pe and local x.
assert any(v for row in p for v in row[2:]) and all(not v for row in pe+x for v in row[2:])
out={'status':'PASS_EXACT_SCATTERING_CONTROLS','field':'GF2','block_volume':2,'all_four_independent_columns_checked':True,'noncommuting_units':True,'packet_arrives_F_before_X':True,'zero_packet_cell_handled':True,'all_three_through_blocks_invertible':True,'all_normalized_local_parts_exclude_nonlocal_p_columns':True,'two_ADD_exchange_joint_invertible':True,'exchange_packet_through_rank':0,'singular_exchange_breaks_terminal_plus_local_normalization':True,'scope':'Concrete controls for the written all-V theorem, not a complete actual111-source replay.'}
pth=Path(__file__).resolve().parent;(pth/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
