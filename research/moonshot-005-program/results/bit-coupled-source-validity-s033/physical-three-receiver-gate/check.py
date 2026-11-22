"""Exact three-receiver geometry gate and abstract sharpness controls.

No construction executable is imported. @CubeJerry, OpenAI assistance,
Apache-2.0. Abstract models do not claim native supplier attainment.
"""
from pathlib import Path
import argparse,json,gzip,hashlib,numpy as np

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&64:a^=67
 return c
P=np.array([[mul(a,b)for b in range(64)]for a in range(64)],dtype=np.uint8);INV=np.zeros(64,dtype=np.uint8)
for a in range(1,64):INV[a]=next(b for b in range(1,64)if P[a,b]==1)
def rr(A):
 A=np.array(A,dtype=np.uint8,copy=True);p=[]
 for c in range(A.shape[1]):
  q=len(p);ii=np.flatnonzero(A[q:,c])
  if not len(ii):continue
  k=q+int(ii[-1]);A[[q,k]]=A[[k,q]];A[q]=P[INV[A[q,c]],A[q]];v=A[:,c].copy();v[q]=0;A^=P[v[:,None],A[q,None,:]];p.append(c)
  if len(p)==len(A):break
 return A,p
def rank(A):return len(rr(A)[1])
def mm(A,B):
 C=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
 for k in range(A.shape[1]):C^=P[A[:,k,None],B[k,None,:]]
 return C
def need(v,msg):
 if not v:raise ValueError(msg)
def null(A):
 R,p=rr(A);f=[j for j in range(A.shape[1])if j not in p];N=np.zeros((A.shape[1],len(f)),dtype=np.uint8);N[f]=np.eye(len(f),dtype=np.uint8)
 for i,j in enumerate(p):N[j]=R[i,f]
 need(not np.any(mm(A,N)),'nullspace');return N
def read(p):return json.loads(gzip.decompress(p.read_bytes()))if p.suffix=='.gz'else json.loads(p.read_text())
def save(p,v):
 raw=(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode();p.write_bytes(gzip.compress(raw,mtime=0)if p.suffix=='.gz'else raw)
def main(repo,out,candidates):
 source=repo/'research/moonshot-005-program/results/bit-simultaneous-d1509-s032/output/READOUTS.json.gz';z=read(source);first=next(iter(z.values()));O={r:first[str(r)]['D_outputs']for r in[48,73,95]};ins={int(j):next(iter(v.values()))['D_inputs']for j,v in z.items()}
 for j,vs in z.items():
  for r,x in vs.items():
   need(x['D_inputs']==ins[int(j)],'donor labels')
   if int(r)in O:need(x['D_outputs']==O[int(r)],'receiver labels')
 V=sorted(set(sum(ins.values(),[])));missing=sorted(set(range(35))-set(V));U=sorted(set(sum(O.values(),[])));common=[10,30]
 need(len(V)==32 and missing==[24,29,33]and len(U)==20,'native/physical union')
 need(all(sorted(set(O[a])&set(O[b]))==common for a,b in[(48,73),(48,95),(73,95)]),'actual shared rows')
 records=[];models={};eye=np.eye(32,dtype=np.uint8)
 for d in range(2,6):
  a=d-2;n=5-d;s=16-d;T=np.zeros((35,35),dtype=np.uint8)
  def row(r,c,u=None):
   T[r,V[c]]=1
   if u is not None:T[r,missing[u]]=1
  for k,r in enumerate(common):row(r,k)
  r48=[r for r in O[48]if r not in common];r73=[r for r in O[73]if r not in common];r95=[r for r in O[95]if r not in common]
  for k,r in enumerate(r48):row(r,2+k)
  for k,r in enumerate(r73):row(r,2+k,k)if k<a else row(r,8+k-a)
  overlap=list(range(2,2+min(a,n)))+list(range(2+a,2+a+max(0,n-a)))
  for k,r in enumerate(r95):row(r,overlap[k],a+k)if k<n else row(r,s+k-n)
  for k,r in enumerate(sorted(set(range(35))-set(U))):row(r,17+k)
  H=eye[:d];M=T[np.ix_(O[95],V)];A=np.vstack([H,M]);N=null(A);Z=np.zeros((35,40),dtype=np.uint8);Z[np.ix_(V,range(N.shape[1]))]=N;B0=np.zeros((35,4),dtype=np.uint8);B0[V]=M[:4].T;S=np.vstack([T[np.ix_(O[r],V)]for r in[48,73]]);e=rank(H)+rank(M)-rank(A)
  need(rank(T)==35 and rank(T[U])==20 and rank(T[np.ix_(U,V)])==17,'sharp physical projection')
  need(rank(M)==8 and rank(T[np.ix_(O[48],V)])==rank(T[np.ix_(O[73],V)])==8 and 16-rank(S)==d,'rowspaces')
  need(e==min(d,7-d)and rank(Z)==32-(d+8-e),'sharp refined gate')
  need(not np.any(mm(T[O[95]],Z))and not np.any(mm(H,Z[V]))and rank(mm(T[O[95]],B0))==4,'common actual readout')
  for k in range(10):need(rank(B0^Z[:,4*k:4*k+4])==4,'injective donor images')
  records.append({'d':d,'e':e,'actual_rows_outside_overlap':8-e,'annihilator_dimension':32-rank(Z),'contrast_rank':rank(Z),'full_word_rank':35,'native_triple_union_rank':17});models[d]={'T':T.tolist(),'Z':Z.tolist(),'B61':B0.tolist(),'overlap_rows':H.tolist()}
  if d==5:T5,H5,M5=T,H,M
 N=null(M5);Z=np.zeros((35,40),dtype=np.uint8);Z[np.ix_(V,range(N.shape[1]))]=N
 need(rank(T5)==35 and rank(Z)==24 and not np.any(mm(T5[O[95]],Z))and rank(mm(H5,Z[V]))==3,'overlap-annihilator premise essential')
 bad=T5.copy()
 for r,c in zip([r for r in O[95]if r not in common],[2,3,4,11,12,13]):bad[r]=0;bad[r,V[c]]=1
 badM=bad[np.ix_(O[95],V)];need(rank(badM)==8 and rank(np.vstack([H5,badM]))==8 and rank(bad)<35,'full-word premise essential')
 actual=[];pins={str(source.relative_to(repo)):hashlib.sha256(source.read_bytes()).hexdigest()}
 for p in candidates:
  T=np.array(read(p)['D_matrix'],dtype=np.uint8);S=np.vstack([T[np.ix_(O[r],V)]for r in[48,73]]);d=16-rank(S);need(rank(T)==35 and rank(T[np.ix_(U,V)])>=17,'candidate row geometry');actual.append({'candidate':str(p),'d':d,'native_triple_union_rank':rank(T[np.ix_(U,V)]),'conditional_contrast_upper':32-(d+8-min(d,7-d))});pins[str(p.relative_to(repo))if p.is_relative_to(repo)else str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
 result={'status':'PASS_PHYSICAL_THREE_RECEIVER_REFINED_GATE','actual_outputs':O,'shared_rows':common,'triple_union':U,'native_columns':V,'unused_columns':missing,'sharp_abstract_models':records,'premise_controls':{'without_I_subset_AnnZ':{'full_word_rank':35,'contrast_rank':24,'actual95_contrast_rank':0,'I_contrast_rank':3},'without_full_word_invertibility':{'full_word_rank':rank(bad),'actual95_rank':8,'annihilator_dimension':8,'native_triple_union_rank':rank(bad[np.ix_(U,V)])}},'candidate_geometry':actual,'native_family_attainment_claimed':False,'new_complete_kappa':False};out.mkdir(parents=True,exist_ok=True);save(out/'RESULT.json',result);save(out/'ABSTRACT-MODELS.json.gz',models);save(out/'SOURCE-PINS.json',pins);print(result['status'],[(r['d'],r['contrast_rank'])for r in records],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);p.add_argument('--candidate',type=Path,action='append',default=[]);q=p.parse_args();main(q.repo.resolve(),q.out.resolve(),[x.resolve()for x in q.candidate])
