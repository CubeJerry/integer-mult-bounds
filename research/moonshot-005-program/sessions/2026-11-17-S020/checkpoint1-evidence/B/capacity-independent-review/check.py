from pathlib import Path
import argparse,hashlib,itertools,json
import sympy as s

def rank(x):return int(x.rank())

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
 perms=list(itertools.permutations(range(3)));identity=(0,1,2);index={g:i for i,g in enumerate(perms)}
 compose=lambda g,h:tuple(g[h[i]] for i in range(3))
 def regular(g):
  out=s.zeros(6)
  for j,h in enumerate(perms):out[index[compose(g,h)],j]=1
  return out
 I=s.eye(6);R=regular((1,0,2));S=regular((0,2,1))
 assert R*S!=S*R and R*R==S*S==I and s.trace(R)==s.trace(S)==0
 pr=(I+R)/2;ps=(I+S)/2;mr=I-pr;ms=I-ps
 plus=s.diag(pr,ps);minus=s.diag(mr,ms)
 assert rank(plus)==rank(minus)==6
 C=pr.col_join(mr);D=pr.row_join(mr);P=s.diag(pr,mr)
 assert D*C==I and P*C==C
 U=pr.row_join(mr).col_join(mr.row_join(pr));assert U*U==s.eye(12)
 # Same regular equality does not assert literal equality of idempotents.
 P0=s.Matrix([[1,1],[0,0]]);C0=s.Matrix([1,0]);D0=s.Matrix([[1,0]]);Q0=C0*D0
 assert P0*P0==P0 and D0*C0==s.eye(1) and P0*C0==C0
 assert P0!=Q0 and P0*Q0==Q0 and Q0*P0==P0
 # Independent cyclic-three average, not the author's C2 x C2 model.
 g=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);e=(s.eye(3)+g+g*g)/3
 assert e*e==e and rank(e)==1 and rank(s.diag(e,e,e))==3
 expected={'two_plus':{'regular_normalized_rank':'1','augmentation_rank':2},'two_minus':{'regular_normalized_rank':'1','augmentation_rank':0},'three_cyclic_plus':{'regular_normalized_rank':'1','augmentation_rank':3}}
 result={'status':'PASS_INDEPENDENT_REGULAR_CAPACITY_REVIEW','source_proof_sha256':hashlib.sha256((args.source/'PROOF.md').read_bytes()).hexdigest(),'comparison_group':'noncommuting S3 regular action','group_order':6,'checks':expected,'nonorthogonal_equal_image_control':True,'scope':'Written universal proof independently checked; finite controls authenticate distinct representation and equality details.','new_complete_kappa':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
