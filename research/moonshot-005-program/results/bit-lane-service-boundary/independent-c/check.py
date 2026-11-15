import json,itertools,hashlib,argparse
from pathlib import Path

def mm(A,B):return [sum(1<<j for j in range(len(B))if sum(((r>>k)&1)*((B[k]>>j)&1)for k in range(len(B)))%2)for r in A]
def lane(A,a,B,b,s):
 for t in range(s):
  temporary=A[a*s+t];B[b*s+t]^=temporary
p=argparse.ArgumentParser();p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();count=0
for V in [2,3,4]:
 for constants in itertools.product([0,1],repeat=3):
  R=[[x]*V for x in constants]
  for s in range(3):
   for t in range(3):
    if s!=t:assert len(set(x^y for x,y in zip(R[s],R[t])))==1;count+=1
  for i in range(3):
   for perm in itertools.permutations(range(V)):assert len(set(R[i][j]for j in perm))==1;count+=1
T=[1,2,8,4];P0=[1,2,0,0];P1=[0,0,4,8];E10=[0,0,1,2]
assert mm(T,T)==[1,2,4,8]and mm(T,P0)==mm(P0,T)and mm(T,P1)==mm(P1,T)
conjugate=mm(mm(T,E10),T);assert conjugate!=E10
distinct=same=0
for s in range(1,4):
 for bits in itertools.product([0,1],repeat=4*s):
  X=list(bits[:2*s]);Y=list(bits[2*s:])
  for left in range(2):
   for right in range(2):
    xx=X[:];yy=Y[:];lane(xx,left,yy,right,s)
    assert xx==X and all(yy[j]==Y[j]for j in range(2*s)if j//s!=right)
    assert all(yy[right*s+t]==Y[right*s+t]^X[left*s+t]for t in range(s))
    lane(xx,left,yy,right,s);assert yy==Y;distinct+=1
for s in range(1,5):
 for bits in itertools.product([0,1],repeat=2*s):
  for left,right in [(0,1),(1,0)]:
   X=list(bits);old=X[:];lane(X,left,X,right,s)
   assert X[left*s:(left+1)*s]==old[left*s:(left+1)*s]
   assert all(X[right*s+t]==old[right*s+t]^old[left*s+t]for t in range(s))
   lane(X,left,X,right,s);assert X==old;same+=1
r={'status':'PASS_INDEPENDENT_LANE_INTERFACE_CONTROLS','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'constant_record_generator_cases':count,'distinct_streaming_cases':distinct,'same_record_distinct_bank_cases':same,'projector_only_negative_control':{'T':T,'P0':P0,'P1':P1,'E10':E10,'T_E10_Tinv':conjugate},'scope':'Restricted grammar and conditional stream algebra only; no compiler admission.','new_complete_kappa':False}
a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'],count,distinct,same)
