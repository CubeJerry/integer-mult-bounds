#!/usr/bin/env python3
"""Independent original-coordinate Hermite intertwiner obstruction.
Arithmetic/geometry is copied from this reviewer's frozen independent cycle
review. No author/predecessor code is imported. Intertwiners are assembled in
all48 polynomial coordinates, without the author's36-coordinate compression.
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

def equations(targets,relations,k,s):
 d=targets[0].shape[0];nrel=relations.shape[1];E=np.zeros((d*nrel,len(targets)*k*k),dtype=np.uint8)
 for i,A0 in enumerate(targets):
  A=A0.copy()
  for _ in range(s):A=M[A,A]
  for a in range(k):
   for c in range(k):E[:,i*k*k+a*k+c]=M[A[:,a,None],relations[i*k+c,None,:]].reshape(-1)
 return E

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();base=args.repo/'research/moonshot-005-program/results';here=Path(__file__).resolve().parent;package=here.parent
 for path,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest()==digest,'pinned source '+path)
 author=package/'author-b'
 for path,digest in json.loads((author/'MANIFEST.json').read_text())['files'].items():need(hashlib.sha256((author/path).read_bytes()).hexdigest()==digest,'frozen author binding '+path)
 L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=roots_from_files(L,B);H=[set(P)for P in L['A2']];D=[set(P)for P in L['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not b(x,y)}for j,x in enumerate(roots)];data=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text());nodes=data['H_nodes'];params={int(j):{int(i):v for i,v in z.items()}for j,z in data['receiver_parameters'].items()};h=263;donors=sorted(H[h]);need(donors==[0,61,62]and nodes[h]==49,'actual H263 and common node');receivers=[i for i in range(111)if H[h]<=adj[i]];need(len(receivers)==33 and 80 not in receivers and 10 not in donors,'33 actual identity-target receivers')
 stars={j:[p for p,P in enumerate(H)if j in P]for j in donors};need(all(len(ps)==28 and len({nodes[p]for p in ps})==28 for ps in stars.values()),'actual donor stars use28 distinct shared nodes');off={};parameters=[];intersections=Counter();visible_counts=Counter()
 for i in receivers:
  off[i]={}
  for j in donors:
   vis=[p for p in stars[j]if H[p]<=adj[i]];need(len(vis)==16 and h in vis,'actual tight source view');off[i][j]={nodes[p]for p in vis if p!=h};need(len(off[i][j])==15 and nodes[h]not in off[i][j],'fifteen distinct off-H nodes');visible_counts[j]+=1
  intersections[len(off[i][0]&off[i][61])]+=1;parameters.append([i,params[0][i],params[61][i],params[62][i]]);need(params[0][i]^params[61][i]==params[62][i]and len({params[j][i]for j in donors})==3,'bilinear triple relation')
 need(intersections=={9:33},'all off-H intersections contain9 nodes')
 exits={};quota=Counter()
 for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
  phase,role,coordinate,plane,d,_,source,_=json.loads(line)
  if plane==h:
   need(phase=='X'and source==role and role in donors,'fully early genuine H263 owners');quota[role]+=1;exits.setdefault(d,set()).update((role,coordinate,lane)for lane in range(8))
 need(len(exits)==45 and set(map(len,exits.values()))=={16}and quota=={0:30,61:30,62:30},'actual full H263 early invoice');need(all(sum(len(slots)for d,slots in exits.items()if D[d]<=adj[i])==240 for i in receivers),'actual240-field shared H cut')
 cases=[];proof_records=[];allf={}
 for mode,k in [('tensor',1),('tensor',3),('hermite',2),('hermite',3)]:
  KS=[[fibre(off[i][j],k,mode)for i in receivers]for j in donors];joint=np.hstack(KS[0]);r=rank(joint);need(rank(np.hstack(KS[1]))==r and rank(np.hstack(KS[0]+KS[1]))==r,'two actual receiver families span the same core');relations=null(joint);need(relations.shape==(33*k,33*k-r),'all exact original-coordinate kernel relations');pair=Counter(rank(np.hstack([KS[0][i],KS[1][i]]))for i in range(33));triple=Counter(rank(np.hstack([KS[j][i]for j in range(3)]))for i in range(33));srange=range(6)if(mode,k)==('hermite',3)else range(1);nullities=[]
  for s in srange:
   E=equations(KS[1],relations,k,s);erank=rank(E);nullities.append(E.shape[1]-erank)
   if(mode,k)==('hermite',3):
    need(E.shape==(3024,297)and erank==297,'all six original-coordinate intertwiner systems full column rank');_,rows=echelon(E.T);minor=E[rows];need(minor.shape==(297,297)and rank(minor)==297,'independent invertible square minor');proof_records.append({'relative_Frobenius':s,'original_coordinate_equation_shape':list(E.shape),'rank':erank,'equation_sha256':hashlib.sha256(E.tobytes()).hexdigest(),'independent_minor_rows':rows,'minor_sha256':hashlib.sha256(minor.tobytes()).hexdigest()})
  if(mode,k)!=('hermite',3):
   E=equations(KS[1],relations,k,0);solutions=null(E);best=0;witness=None
   for trial in range(32):
    coeff=np.array([(trial+1)*(z+1)%64 for z in range(solutions.shape[1])],dtype=np.uint8)[:,None];v=mm(solutions,coeff)[:,0];blocks=v.reshape(33,k,k);images=np.hstack([mm(KS[1][i],blocks[i])for i in range(33)]);need(not np.any(mm(images,relations)),'control map respects every source relation');mr=rank(images)
    if mr>best:best=mr;witness=v.tolist()
    if best==r:break
   need(best==r,'positive intertwiner achieves full core rank')
  else:best=0;witness=None;allf={'donor0':{i:K.tolist()for i,K in zip(receivers,KS[0])},'donor61':{i:K.tolist()for i,K in zip(receivers,KS[1])},'relations':relations.tolist()}
  expected={('tensor',1):(6,1,2,2),('tensor',3):(18,9,6,6),('hermite',2):(12,4,4,4),('hermite',3):(36,0,6,9)}[mode,k];need(r==expected[0]and nullities[0]==expected[1]and pair=={expected[2]:33}and triple=={expected[3]:33},'all exact positive and negative rank profiles');cases.append({'mode':mode,'width':k,'source_fibre_span':r,'pair_union_ranks':dict(pair),'triple_union_ranks':dict(triple),'intertwiner_nullities':nullities,'positive_control_core_map_rank':best,'positive_control_coefficients':witness})
 # Verify the Hermite12 decomposition in literal polynomial coordinates.
 decomposition_checks=0
 for i in receivers:
  for j in(0,61):
   K3=fibre(off[i][j],3,'hermite');K12=fibre(off[i][j],12,'hermite');Frob=M[M[K3,K3],M[K3,K3]]
   for residue in range(4):
    need(np.array_equal(K12[residue::4,residue::4],Frob),'four Frobenius-square Hermite3 blocks');need(all(not np.any(K12[r::4,residue::4])for r in range(4)if r!=residue),'separate residue classes in Hermite12');decomposition_checks+=1
 # A duplicated selected equation cannot remain a square full-rank certificate.
 bad=minor.copy();bad[-1]=bad[-2];need(rank(bad)==296,'rank certificate detects duplicate row')
 result={'status':'PASS_INDEPENDENT_HERMITE3_BINARY_INTERTWINER_OBSTRUCTION','no_author_or_predecessor_imports':True,'original_polynomial_coordinates_used':48,'author_compressed_core_not_used':True,'H':263,'common_node':49,'donors_compared':[0,61],'native_identity_receivers':receivers,'off_node_intersection_histogram':dict(intersections),'actual_H_cut_GF64_fields':240,'actual_early_donor_quotas':dict(quota),'intertwiner_equation_shape':[3024,297],'all_six_intertwiner_ranks':[297]*6,'Hermite12_residue_block_checks':decomposition_checks,'experiments':cases,'duplicate_minor_row_control_rank':296,'arbitrary_binary_linear_bank_gauges_excluded':True,'all_finite_extensions_and_positive_repetitions':True,'arbitrary_nonlinear_gauges_excluded':False,'changed_quotient_families_excluded':False,'complete_kappa_claimed':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(args.out/'MINORS.json').write_text(json.dumps(proof_records,sort_keys=True,indent=2)+'\n');(args.out/'FIBRES-AND-RELATIONS.json.gz').write_bytes(gzip.compress(json.dumps(allf,sort_keys=True,separators=(',',':')).encode(),mtime=0));print(result['status'],3024,297,6,33,decomposition_checks,flush=True)

if __name__=='__main__':main()
