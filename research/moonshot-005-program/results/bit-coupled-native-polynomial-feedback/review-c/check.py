#!/usr/bin/env python3
"""Independent polynomial feedback audit. No author code imported.
Field/geometry arithmetic is copied from this reviewer's frozen checks.
"""
import argparse,gzip,hashlib,json
from collections import Counter
from pathlib import Path
import numpy as np

def need(condition,message):
 if not condition:raise AssertionError(message)
def xor(items):
 answer=0
 for value in items:answer^=int(value)
 return answer
def q(x):return ((x&(x>>1))&85).bit_count()&1
def b(x,y):return (x&(((y&85)<<1)|((y&170)>>1))).bit_count()&1
def span(items):
 out={0}
 for x in items:out|={y^x for y in tuple(out)}
 return out
def polynomial_product(x,y):
 value=xor(1<<(i+j)for i in range(6)if x>>i&1 for j in range(6)if y>>j&1)
 for d in range(10,5,-1):
  if value>>d&1:value^=67<<(d-6)
 return value
M=np.array([[polynomial_product(x,y)for y in range(64)]for x in range(64)],dtype=np.uint8)
INV=np.array([0]+[next(y for y in range(1,64)if M[x,y]==1)for x in range(1,64)],dtype=np.uint8)
def mm(A,B):
 A=np.asarray(A,dtype=np.uint8);B=np.asarray(B,dtype=np.uint8);need(A.ndim==B.ndim==2 and A.shape[1]==B.shape[0],'matrix dimensions')
 out=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
 for k in range(A.shape[1]):out^=M[A[:,k,None],B[k,None,:]]
 return out
def echelon(A):
 A=np.array(A,dtype=np.uint8,copy=True);pivots=[]
 for c in range(A.shape[1]):
  r=len(pivots);choices=np.flatnonzero(A[r:,c])
  if not len(choices):continue
  s=r+int(choices[-1]);A[[r,s]]=A[[s,r]];A[r,c:]=M[INV[A[r,c]],A[r,c:]]
  if r+1<len(A):A[r+1:,c:]^=M[A[r+1:,c,None],A[r,None,c:]]
  pivots.append(c)
  if len(pivots)==len(A):break
 return A,pivots
def rank(A):return len(echelon(A)[1])
def null(A):
 R,P=echelon(A);free=[c for c in range(R.shape[1])if c not in P];K=np.zeros((R.shape[1],len(free)),dtype=np.uint8);K[free]=np.eye(len(free),dtype=np.uint8)
 for r in range(len(P)-1,-1,-1):K[P[r]]=mm(R[r:r+1,P[r]+1:],K[P[r]+1:])[0]
 need(not np.any(mm(A,K)),'independently solved nullspace');return K
def invert(A):
 n=len(A);need(A.shape==(n,n),'square inverse');R,P=echelon(np.hstack([A,np.eye(n,dtype=np.uint8)]));need(P[:n]==list(range(n)),'invertible matrix');X=np.zeros((n,n),dtype=np.uint8)
 for r in range(n-1,-1,-1):X[r]=R[r,n:]^mm(R[r:r+1,r+1:n],X[r+1:])[0]
 need(np.array_equal(mm(A,X),np.eye(n,dtype=np.uint8)),'right inverse identity');return X
def power(x,e):
 out=1
 while e:
  if e&1:out=int(M[out,x])
  x=int(M[x,x]);e//=2
 return out
def qf(x):return power(x,9)^power(x,18)^power(x,36)
def roots_from_files(L,B):
 cols=B['lattice_basis_columns'];A=[[cols[j][i]for j in range(8)]for i in range(8)];basis=B['hyperbolic_basis_masks'];back={xor(basis[j]for j in range(8)if x>>j&1):x for x in range(256)};need(len(back)==256,'binary lattice coordinate isomorphism');roots=[]
 for root in L['root_table']:
  coords=[0]*8
  for i in range(7,-1,-1):coords[i],remainder=divmod(root[i]-sum(A[i][j]*coords[j]for j in range(i+1,8)),A[i][i]);need(remainder==0,'exact integral root coordinates')
  roots.append(back[sum((x&1)<<i for i,x in enumerate(coords))])
 need(len(roots)==len(set(roots))==120 and set(roots)=={x for x in range(256)if q(x)},'all120 actual anisotropic roots');return roots
def witt(V,Q):
 V=set(V);answer=[]
 while len(V)>1:
  polar=lambda x,y:Q(x)^Q(y)^Q(x^y)
  zeros=sorted(x for x in V if x and not Q(x))
  if zeros:e=zeros[0];f=next(x for x in zeros if polar(e,x))
  else:e=min(V-{0});f=min(V-{0,e})
  answer.extend((e,f));V={x for x in V if not polar(x,e)and not polar(x,f)}
 return answer
def random_rows(tag,rows,cols):
 return np.frombuffer(hashlib.shake_256(tag.encode('ascii')).digest(rows*cols),dtype=np.uint8).reshape(rows,cols)&63

def multiply_polynomials(a,b):
 out=np.zeros(len(a)+len(b)-1,dtype=np.uint8)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]^=M[x,y]
 return out
def annihilator(nodes):
 answer=np.array([1],dtype=np.uint8)
 for x in sorted(nodes):answer=multiply_polynomials(answer,np.array([x,1],dtype=np.uint8))
 return answer
def hasse(node,k):
 return np.array([[power(node,c-r)if c>=r and (c&r)==r else 0 for c in range(16*k)]for r in range(k)],dtype=np.uint8)
def fibre(off,k,mode):
 g=annihilator(off)
 if mode=='tensor':
  K=np.kron(g[:,None],np.eye(k,dtype=np.uint8));E=np.vstack([np.kron(np.array([[power(x,r)for r in range(16)]],dtype=np.uint8),np.eye(k,dtype=np.uint8))for x in sorted(off)])
 else:
  product=np.array([1],dtype=np.uint8)
  for _ in range(k):product=multiply_polynomials(product,g)
  K=np.zeros((16*k,k),dtype=np.uint8)
  for c in range(k):K[c:c+len(product),c]=product
  E=np.vstack([hasse(x,k)for x in sorted(off)])
 need(len(off)==15 and E.shape==(15*k,16*k)and rank(E)==15*k and rank(K)==k and not np.any(mm(E,K)),'full off-H polynomial kernel')
 central=hasse(49,k)if mode=='hermite'else np.kron(np.array([[power(49,r)for r in range(16)]],dtype=np.uint8),np.eye(k,dtype=np.uint8))
 need(rank(mm(central,K))==k,'complete16-node source view invertible');return K

SUPPORT={0,1,2,4,5,8,14}
GAPS={3,6,7,9,10,11,12,13,15}
def divide_linear(P,x):
 W=np.array(P,dtype=np.uint8,copy=True);out=np.zeros(len(P)-1,dtype=np.uint8)
 for d in range(len(P)-1,0,-1):out[d-1]=W[d];W[d]=0;W[d-1]^=M[x,out[d-1]]
 need(not np.any(W),'exact polynomial root division');return out
def feedback(j,seed):
 blocks=[]
 for slot in range(16):blocks.append(random_rows(f'native-polynomial-feedback/{j}/{seed}/{slot}',3,3)if slot in GAPS else np.zeros((3,3),dtype=np.uint8))
 blocks[3]=np.array([[0,1,0],[0,0,1],[1,0,0]],dtype=np.uint8);blocks[6]=np.diag(np.array([1,0,0],dtype=np.uint8));return np.hstack(blocks)
def source(node,V):
 k=len(V);ordinary=np.kron(np.array([[power(node,e)for e in range(16)]],dtype=np.uint8),np.eye(k,dtype=np.uint8));return ordinary^M[power(node,16)^1,V]
def updated_kernel(poly,node,V):
 k=len(V);g=divide_linear(poly,node);c=poly[:16].copy();c[0]^=1;K=np.kron(g[:,None],np.eye(k,dtype=np.uint8));C=np.kron(c[:,None],np.eye(k,dtype=np.uint8));return K^mm(C,mm(V,K))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();base=args.repo/'research/moonshot-005-program/results';here=Path(__file__).resolve().parent;author=here.parent/'author'
 for path,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest()==digest,'pinned source '+path)
 for path,digest in json.loads((author/'MANIFEST.json').read_text())['files'].items():need(hashlib.sha256((author/path).read_bytes()).hexdigest()==digest,'frozen author '+path)
 L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=roots_from_files(L,B);H=[set(P)for P in L['A2']];adj=[{i for i,y in enumerate(roots)if i!=j and not b(x,y)}for j,x in enumerate(roots)];nodes=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text());node=nodes['H_nodes'];params={int(j):{int(i):v for i,v in z.items()}for j,z in nodes['receiver_parameters'].items()};prm=json.loads((author/'output/PARAMETERS.json').read_text());witness=json.loads((author/'output/NON-RS-WITNESSES.json').read_text());claimed=json.loads((author/'output/RESULT.json').read_text());need(prm['k']==3,'literal width-three examples')
 Q=[x for x in range(64)if not qf(x)];need(len(Q)==28 and qf(1)==1 and all(power(x,16)^1 for x in Q),'nonvanishing h at all28 nodes');blocks={v:{x for x in Q if qf(x^v)==1}for v in range(1,64)};need(all(len(s)==16 for s in blocks.values()),'all63 actual field blocks');polys={v:annihilator(xs)for v,xs in blocks.items()};need(set.union(*(set(np.flatnonzero(P[:16]))for P in polys.values()))==SUPPORT,'all lower polynomial support positions')
 for v,P in polys.items():
  LP=np.zeros(17,dtype=np.uint8)
  for e,p in[(8,1),(16,2),(14,4),(5,4),(1,8),(2,16),(4,32)]:LP[e]^=power(v,p)
  LP[0]^=qf(v)^1;need(np.array_equal(M[power(v,2),P],LP),'complete coefficient identity v²P=L+q(v)+1')
 scalar_hist=Counter();linear_map_checks=0;pair_data={}
 for a in Q:
  for bnode in Q:
   if a==bnode:continue
   vs=[v for v,xs in blocks.items()if a in xs and bnode in xs];need(len(vs)==20,'all pairwise view intersections');K=[];C=[]
   for v in vs:
    c=polys[v][:16].copy();c[0]^=1;K.append(M[power(v,2),divide_linear(polys[v],a)]);C.append(M[power(v,2),c]);need(qf(v^(a^bnode))^qf(v)^qf(a^bnode)==0,'common views lie in a binary hyperplane')
   KK=np.array(K).T;CC=np.array(C).T;ranks=(rank(KK),rank(CC),rank(np.hstack([KK,CC])));need(ranks==(5,5,10),'exact scalar5+5 envelope');scalar_hist[str(ranks)]+=1;pair_data[a,bnode]=vs
   def linear_extensions(v):
    Lp=np.zeros(17,dtype=np.uint8)
    for e,p in[(8,1),(16,2),(14,4),(5,4),(1,8),(2,16),(4,32)]:Lp[e]^=power(v,p)
    Lpa=xor(int(M[x,power(a,e)])for e,x in enumerate(Lp));Lp[0]^=Lpa;g=divide_linear(Lp,a);cor=Lp.copy();cor[16]^=power(v,2);cor[0]^=power(v,2);need(not cor[16],'degree16 cancellation in correction');return g,cor[:16]
   basis=[linear_extensions(1<<t)for t in range(6)]
   for v in vs:
    a1,a2=linear_extensions(v);z1=np.zeros(16,np.uint8);z2=z1.copy()
    for t in range(6):
     if v>>t&1:z1^=basis[t][0];z2^=basis[t][1]
    need(np.array_equal(a1,z1)and np.array_equal(a2,z2),'actual restrictions of binary-linear parameter maps');linear_map_checks+=1
 quota=Counter()
 for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
  phase,role,coordinate,h,d,_,owner,_=json.loads(line)
  if phase=='X'and h is not None:need(owner==role,'genuine original early owner');quota[role,h]+=1
 need(Counter(quota.values())=={15:2675,30:422,45:11},'literal native quota census');singletons={j for(j,h),r in quota.items()if r==45};donors=sorted(set(range(111))-singletons);need(donors==prm['ordinary_donors']and len(donors)==100 and set(map(int,witness))==set(donors),'all100 ordinary source witnesses')
 all_maps={};feedbacks={};early_hash={};source_hash={};source_cuts=native_cuts=nilpotent_checks=0;nonrs_hist=Counter()
 for j in donors:
  V=feedback(j,prm['feedback_seed']);need(rank(V)==3,'literal full-row feedback');feedbacks[j]=V;star=[h for h,P in enumerate(H)if j in P];maps={h:source(node[h],V)for h in star};all_maps[j]=maps;need(len(maps)==28 and all(rank(F)==3 for F in maps.values()),'all literal quotient maps')
  source_hash[j]=hashlib.sha256(b''.join(maps[h].tobytes()for h in sorted(maps))).hexdigest();need(source_hash[j]==claimed['source_coefficient_sha256'][str(j)],'independently reconstructed coefficient bytes')
  for i in sorted(adj[j]):
   visible=sorted(h for h in star if H[h]<=adj[i]);v=params[j][i];need(len(visible)==16 and {node[h]for h in visible}==blocks[v],'actual native view equals shared field block');c=polys[v][:16].copy();c[0]^=1;C=np.kron(c[:,None],np.eye(3,dtype=np.uint8));need(not np.any(mm(V,C)),'literal zero-support product V C')
   A=np.vstack([maps[h]for h in visible]);old=np.kron(np.array([[power(node[h],e)for e in range(16)]for h in visible],dtype=np.uint8),np.eye(3,dtype=np.uint8));N=mm(C,V);need(not np.any(mm(N,N))and np.array_equal(mm(A,np.eye(48,dtype=np.uint8)^N),old),'literal square-zero inverse identity');need(rank(A)==48,'every actual geometric source cut');source_cuts+=1;native_cuts+=i<111;nilpotent_checks+=1
  spec=prm['early'][str(j)];h0=spec['chart'];need(j in H[h0]and max(H[h0])<111,'literal actual early chart label');rows=[]
  for h,F in sorted(maps.items()):
   r=quota[j,h]//15;need(r in(1,2),'ordinary donor early quota')
   if r==2:rows.append(np.block([[F,np.zeros_like(F)],[np.zeros_like(F),F]]))
   elif h==h0:rows.append(np.hstack([F,np.zeros_like(F)]))
   else:
    G=random_rows(f"early/{h0}/3/{j}/{h}/{spec['seed']}",3,6);need(rank(G)==3,'extendible local early quotient frame');rows.append(np.hstack([mm(G[:,:3],F),mm(G[:,3:],F)]))
  early=np.vstack(rows);need(early.shape==(96,96)and rank(early)==96,'all100 actual early bases');early_hash[j]=hashlib.sha256(early.tobytes()).hexdigest()
  hs=witness[str(j)]['planes'];need(len(set(hs))==len(hs)==16 and set(hs)<=set(maps),'valid16-plane non-RS witness');rr=rank(np.vstack([maps[h]for h in hs]));need(rr==witness[str(j)]['rank']and rr<48,'non-RS information invariant');nonrs_hist[rr]+=1
 need(source_cuts==6300 and native_cuts==5828 and nilpotent_checks==6300,'complete actual finite source quantifiers')
 V=feedbacks[0];P=V[:,9:12];E=V[:,18:21];powers=[np.eye(3,dtype=np.uint8),P,mm(P,P)];words=np.array([mm(mm(a,E),b).reshape(-1)for a in powers for b in powers]);need(rank(words)==9 and np.any(mm(P,E)^mm(E,P)),'noncommuting full matrix algebra')
 actual_hist=Counter();exact_visible_subtractions=0
 for(a,bnode),vs in pair_data.items():
  K=np.hstack([updated_kernel(polys[v],a,V)for v in vs]);need(not np.any(mm(source(bnode,V),K)),'visible other quotient annihilates every new fibre');rr=rank(K);need(rr==27,'all756 actual ranks attain9k');actual_hist[rr]+=1
  v=vs[0];c=polys[v][:16].copy();c[0]^=1;C=np.kron(c[:,None],np.eye(3,dtype=np.uint8));need(np.array_equal(mm(source(bnode,V),C),M[power(bnode,16)^1,np.eye(3,dtype=np.uint8)]),'surjective k-dimensional visible restriction');exact_visible_subtractions+=1
 first=min(adj[0]&set(range(111)));v=params[0][first];bad=V.copy();need(polys[v][14]!=0,'unsupported slot coefficient nonzero');bad[:,42:45]=M[INV[polys[v][14]],np.eye(3,dtype=np.uint8)];badcut=np.vstack([source(node[h],bad)for h in sorted(all_maps[0])if H[h]<=adj[first]]);need(rank(badcut)==45,'outside-support feedback loses three source dimensions')
 H263=263;common_hist=Counter()
 for i in range(111):
  if not H[H263]<=adj[i]:continue
  obs=[np.vstack([F for h,F in all_maps[j].items()if h!=H263 and H[h]<=adj[i]])for j in(0,61)];need(rank(obs[0])==rank(obs[1])==45,'two complete off-H kernels');rr=rank(np.vstack(obs));need(rr==48,'zero common inverse fibre in displayed coordinates');common_hist[rr]+=1
 need(common_hist=={48:33},'all33 native H263 ungauged failures')
 width_checks={}
 for k in(1,2,4,5):
  VV=np.hstack([random_rows(f'independent-feedback-width/{k}/{s}',k,k)if s in GAPS else np.zeros((k,k),dtype=np.uint8)for s in range(16)]);count=0
  for v in(1,2,7,19,63):
   c=polys[v][:16].copy();c[0]^=1;C=np.kron(c[:,None],np.eye(k,dtype=np.uint8));N=mm(C,VV);need(not np.any(mm(VV,C))and not np.any(mm(N,N)),'independent noncommuting width example');need(np.array_equal(mm(np.eye(16*k,dtype=np.uint8)^N,np.eye(16*k,dtype=np.uint8)^N),np.eye(16*k,dtype=np.uint8)),'square-zero inverse at another width');count+=1
  width_checks[k]=count
 v=1;c=polys[v][:16].copy();c[0]^=1;k=3;C=np.kron(c[:,None],np.eye(k,dtype=np.uint8));W=feedback(0,0).copy();slot=next(t for t in SUPPORT if c[t])
 for scalar in range(2,64):
  W[:,3*slot:3*slot+3]=M[int(M[scalar,INV[c[slot]]]),P];small=np.eye(3,dtype=np.uint8)^mm(W,C)
  if rank(small)==3:break
 need(np.any(mm(W,C)),'conditional example is outside gap family');N=mm(C,W);inverse=np.eye(48,dtype=np.uint8)^mm(C,mm(invert(small),W));need(np.array_equal(mm(np.eye(48,dtype=np.uint8)^N,inverse),np.eye(48,dtype=np.uint8)),'ordered conditional Woodbury inverse')
 result={'status':'PASS_INDEPENDENT_UNIVERSAL_POLYNOMIAL_FEEDBACK','universal_positive_k_and_finite_extensions_reviewed':True,'unconditional_gap_blocks':sorted(GAPS),'conditional_all16_blocks_reviewed':True,'universal_propagation_bound':'9k','saturation_threshold':'15k','scalar_pair_envelopes':dict(scalar_hist),'binary_linear_parameter_checks':linear_map_checks,'ordinary_donors':donors,'geometric_source_cuts':source_cuts,'native_source_cuts':native_cuts,'literal_inverse_checks':nilpotent_checks,'actual_early_basis_count':100,'early_basis_dimension':96,'early_basis_sha256':early_hash,'non_RS_rank_histogram':dict(nonrs_hist),'source_coefficients_sha256':source_hash,'copy_axis_algebra_dimension':9,'donor0_propagation_ranks':dict(actual_hist),'visible_k_subtraction_checks':exact_visible_subtractions,'other_width_examples':width_checks,'conditional_inverse_example':True,'negative_controls':{'unsupported_slot_rank':45,'ungauged_H263_union_ranks':dict(common_hist)},'F_linear_gauges_preserve_F_rank':True,'nonlinear_gauges_preserve_partition_join_nonsaturation_only':True,'singleton_source_replacements':False,'complete_physical_word':False,'common_H_word':False,'new_complete_kappa':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],756,6300,5828,100,9,flush=True)

if __name__=='__main__':main()
