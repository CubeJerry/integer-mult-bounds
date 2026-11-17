from pathlib import Path
import argparse,hashlib,itertools,json
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();G=list(itertools.permutations(range(3)));ix={g:i for i,g in enumerate(G)}
def product(g,h):return tuple(g[h[k]]for k in range(3))
def parity(g):return sum(g[i]>g[j]for i in range(3)for j in range(i+1,3))%2
def left(g):
 A=s.zeros(6)
 for j,h in enumerate(G):A[ix[product(g,h)],j]=1
 return A
S=left((1,0,2));R=left((2,1,0));I=s.eye(6);Z=s.zeros(6);results=[]
for eps in [1,-1]:
 Ps=(I+eps*S)/2;Ms=I-Ps;Pr=(I+eps*R)/2;Mr=I-Pr;Sig=sum((eps**parity(g)*left(g)for g in G),s.zeros(6))/6;W=Ps-Sig
 assert Sig*Sig==Sig and Ps*Sig==Sig and W*W==W and W.rank()==2
 count=0;total_dim=0
 for cm in range(64):
  C=s.diag(*[(cm>>j)&1 for j in range(6)])
  if S*C!=C*S:continue
  for em in range(64):
   if cm&em:continue
   E=s.diag(*[(em>>j)&1 for j in range(6)])
   if R*E!=E*R:continue
   A=s.Matrix.vstack((I-C)*s.Matrix.hstack(Pr,Mr),(I-C)*s.Matrix.hstack(Z,Ms),(I-E)*s.Matrix.hstack(Z,Ps));ker=A.nullspace();assert all(W*v[6:12,0]==s.zeros(6,1)for v in ker)
   count+=1;total_dim+=len(ker)
 assert count==18
 results.append({'sign':eps,'support_patterns':count,'summed_nullspace_dimensions':total_dim,'regular_orbit_W_rank':2})
ranks=[]
for V in [1,2,3,4,8]:
 q=2**V;W=q*q*(q*q-1)//3
 for eps in [1,-1]:
  p=(q**4+eps*q**3)//2;sig=(q**4+3*eps*q**3+2*q*q)//6;assert p-sig==W>0
  ranks.append({'V':V,'sign':eps,'W':W,'character_sector':sig})
report={'status':'PASS_SIGNED_S3_COLUMN_LEMMA','exact_regular_orbit_controls':results,'total_patterns':36,'collective_rank_controls':ranks,'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'scope':'Both signs in same rank1-isolating two-bank family; genuine three-bank negative-spectator coupling outside.'}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
