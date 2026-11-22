"""Exact protected source/D parameterization. Own GF64 arithmetic; no tangent import.
@CubeJerry with substantial OpenAI assistance. Apache-2.0. No supplier claim.
"""
from pathlib import Path
import argparse,gzip,hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=Path('research/moonshot-005-program/results')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def mul(x,y):
 z=0
 for _ in range(6):
  if y&1:z^=x
  y>>=1;x<<=1
  if x&64:x^=0x43
 return z
P=np.array([[mul(x,y)for y in range(64)]for x in range(64)],dtype=np.uint8)
INV=np.array([0]+[next(y for y in range(1,64)if P[x,y]==1)for x in range(1,64)],dtype=np.uint8)
def mm(A,B):
 need(A.ndim==B.ndim==2 and A.shape[1]==B.shape[0],'matrix shape')
 C=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
 for q in range(A.shape[1]):C^=P[A[:,q,None],B[None,q,:]]
 return C
def rref(A):
 A=A.copy();row=0;piv=[]
 for col in range(A.shape[1]):
  ix=np.flatnonzero(A[row:,col])
  if not len(ix):continue
  q=row+int(ix[0]);A[[row,q]]=A[[q,row]];A[row]=P[INV[A[row,col]],A[row]]
  fac=A[:,col].copy();fac[row]=0;A^=P[fac[:,None],A[row][None,:]];piv.append(col);row+=1
  if row==A.shape[0]:break
 return A,piv
def rank(A):return len(rref(A)[1])
def inverse(A):
 n,m=A.shape;need(n==m,'square inverse');B,piv=rref(np.hstack([A,np.eye(n,dtype=np.uint8)]));need(piv[:n]==list(range(n)),'singular inverse');return B[:,n:]
def solve(A,B):
 _,cols=rref(A);X=np.zeros((A.shape[1],B.shape[1]),dtype=np.uint8)
 if cols:
  C=A[:,cols];_,rows=rref(C.T);X[cols]=mm(inverse(C[rows]),B[rows])
 need(np.array_equal(mm(A,X),B),'linear solve');return X
def read(p):
 raw=p.read_bytes();return json.loads(gzip.decompress(raw)if p.suffix=='.gz'else raw)
def save(p,obj):
 raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode();p.write_bytes(gzip.compress(raw,mtime=0)if p.suffix=='.gz'else raw)
def main(repo,out):
 for p,h in read(HERE/'SOURCE-PINS.json').items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 z=read(repo/BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');T=np.array(read(repo/BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz')['matrix'],dtype=np.uint8)
 L=np.array(z['common_frames'],dtype=np.uint8);need(L.shape==(96,32)and rank(L)==32,'commonframe')
 R=z['retained_receivers'];J=z['donors'];I={int(k):v for k,v in z['D_inputs'].items()};O={int(k):v for k,v in z['D_outputs'].items()};U=sorted(set(sum(O.values(),[])));B=[4,5,7,8]
 need(R==[6,9,48,73]and len(U)==22 and set(B)<=set(I[61]),'incidence')
 ss={(j,r):inverse(T[np.ix_(O[r],I[j])])for j in J for r in R};systems={};witnesses=[];source_free=0
 for key,v in sorted(z['systems'].items()):
  j,h=map(int,key.split('/'));F=np.array(v['old_protected_map'],dtype=np.uint8);C=np.array(v['H_observation_core'],dtype=np.uint8);X=np.array(v['input_generators'],dtype=np.uint8);N=np.array(v['relation_kernel'],dtype=np.uint8);maps=[np.array(x,dtype=np.uint8)for x in v['receiver_ingress_to_quotient_maps']]
  need(np.array_equal(X,np.hstack([C,L])),'input generators');need(not np.any(mm(X,N))and rank(N)==X.shape[1]-rank(X),'full relation kernel');need(rank(C)==C.shape[1],'H basis')
  for t,r in enumerate(R):need(np.array_equal(mm(F,L[:,8*t:8*t+8]),mm(maps[t],ss[j,r])),'old source image')
  special=[p for p in B if p in I[j]];V=np.zeros((32,4*len(special)),dtype=np.uint8)
  for t,r in enumerate(R):V[8*t:8*t+8,t*len(special):(t+1)*len(special)]=T[np.ix_(O[r],special)]
  W=mm(L,V);coeff=solve(C,W);dim=rank(C)+32-rank(X);need(rank(W)==W.shape[1]==dim,'exact intersection')
  free=6*(96-rank(X));source_free+=free;witnesses.append({'system':key,'special_inputs':special,'H_rank':rank(C),'generator_rank':rank(X),'intersection_dimension':dim,'L_coordinates':V.tolist(),'H_core_coordinates':coeff.tolist(),'source_extension_dimension':free});systems[j,h]={'F':F,'C':C,'X':X,'N':N,'maps':maps}
 parent=[]
 for j in J:
  hs=sorted(h for jj,h in systems if jj==j);need(len(hs)==4,'four H parents')
  for t,r in enumerate(R):
   M=np.vstack([systems[j,h]['maps'][t]for h in hs]);need(rank(M)==8,'parent stack');left=solve(M.T,np.eye(8,dtype=np.uint8)).T;parent.append({'donor':j,'receiver':r,'parents':hs,'left_inverse':left.tolist()})
 allowed=[(q,p)for q in range(35)for p in range(35)if q>=19 or p<19];frozen={(q,p)for q in U for p in B};free=[qp for qp in allowed if qp not in frozen]
 need(len(systems)==44 and len(allowed)==921 and len(frozen)==88 and len(free)==833 and source_free==13368,'dimensions')
 def inverse_sections(TT):
  ans={}
  for j in J:
   for r in R:
    S=TT[np.ix_(O[r],I[j])]
    if rank(S)!=8:return None
    ans[j,r]=inverse(S)
  return ans
 def failures(inv):
  ans=[]
  for(j,h),s in systems.items():
   Y=np.hstack([mm(s['F'],s['C'])]+[mm(M,inv[j,r])for M,r in zip(s['maps'],R)]);e=mm(Y,s['N'])
   if np.any(e):ans.append([j,h,rank(e)])
  return ans
 need(not failures(ss),'old positive');controls=[]
 for q,p in sorted(frozen):
  for t in range(1,64):
   TT=T.copy();TT[q,p]^=t;inv=inverse_sections(TT)
   if inv is None:continue
   bad=failures(inv);w=next((x for x in bad if x[0]==61),None);need(w is not None,'frozen mutation missed decisive donor');controls.append({'row':q,'column':p,'coefficient':t,'donor61_failure':w});break
  else:raise ValueError('missing nonsingular mutation')
 # A positive point with many simultaneous changes exercises the exact family.
 for seed in range(100):
  raw=hashlib.shake_256(('S033-affine-positive/'+str(seed)).encode()).digest(len(free));TT=T.copy()
  for(q,p),v in zip(free,raw):TT[q,p]^=v&63
  if rank(TT[:19,:19])<19 or rank(TT[19:,19:])<16:continue
  inv=inverse_sections(TT)
  if inv is None:continue
  need(not failures(inv),'dense positive');positive={'seed':seed,'changed_entries':int(np.count_nonzero(TT^T)),'D_matrix':TT.tolist()};break
 else:raise ValueError('positive not found')
 out.mkdir(parents=True,exist_ok=True);save(out/'CERTIFICATE.json.gz',{'intersections':witnesses,'parent_left_inverses':parent,'frozen_inputs':B,'output_union':U,'free_entries':free,'negative_controls':controls,'dense_positive':positive})
 result={'status':'PASS_EXACT_833_PARAMETER_LOCAL_D_FAMILY','local_systems':44,'decisive_donor':61,'decisive_parent_systems':4,'phase_legal_D_entries':921,'fixed_D_entries':88,'exact_D_dimension':833,'source_extension_dimension':13368,'exact_joint_local_dimension':14201,'frozen_entry_negative_controls':len(controls),'dense_positive_seed':positive['seed'],'dense_positive_changed_entries':positive['changed_entries'],'all_coefficient_extensions':True,'arbitrary_repeated_lane_block_matrices':True,'full_source_validity':False,'full_source_cost':False,'new_fifth_receiver':False,'fixed_K_rank_bound_proved_here':False,'new_complete_kappa':False};save(out/'RESULT.json',result);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);args=p.parse_args();main(args.repo.resolve(),args.out.resolve())
