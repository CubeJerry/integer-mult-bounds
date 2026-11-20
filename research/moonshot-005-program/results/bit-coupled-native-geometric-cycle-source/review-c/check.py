#!/usr/bin/env python3
"""Independent literal-coefficient audit of the four-centre width-three cycle.
No author/predecessor imports, source constructor, core injection, or saved fibre
is used. Fibres are solved directly from the literal off-centre source maps.
GF64 uses carryless polynomial convolution; nullspaces use forward elimination
and back substitution. H words are rebuilt from the geometric parameters.
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

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();base=args.repo/'research/moonshot-005-program/results';package=base/'bit-coupled-native-geometric-cycle-source';here=Path(__file__).resolve().parent
 for path,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest()==digest,'pinned source '+path)
 component=package/'component';manifest=json.loads((component/'MANIFEST.json').read_text())
 for path,digest in manifest['files'].items():need(hashlib.sha256((component/path).read_bytes()).hexdigest()==digest,'frozen component '+path)
 L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=roots_from_files(L,B);H=[set(P)for P in L['A2']];D=[set(P)for P in L['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not b(x,y)}for j,x in enumerate(roots)];need(all(len(A)==63 for A in adj),'all63 receiver neighbours')
 prm=json.loads((component/'output/PARAMETERS.json').read_text());saved=json.loads((component/'output/COEFFICIENTS.json').read_text());maps={int(j):{int(h):np.array(F,dtype=np.uint8)for h,F in table.items()}for j,table in saved.items()};centres=prm['centres'];need(centres==[263,642,135,44],'closed cycle centres');need([sorted(H[h])for h in centres]==[[0,61,62],[45,61,100],[25,45,47],[0,25,26]],'actual closed cycle incidence');need(set(maps)==set.union(*(H[h]for h in centres)),'all eight literal donors')
 quota=Counter()
 for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
  kind,owner,_,plane,_,_,source,_=json.loads(line)
  if kind=='X'and plane is not None:need(owner==source,'genuine initial owner');quota[owner,plane]+=1
 need(Counter(quota.values())=={15:2675,30:422,45:11},'actual native early slot quotas')
 all_cuts=native_cuts=0;cut_counts={};early_matrices={};row_hashes={}
 for j,table in maps.items():
  need(set(table)=={h for h,P in enumerate(H)if j in P}and len(table)==28,'one literal complete source bank per donor')
  need(all(F.shape==(3,48)and np.all(F<64)and rank(F)==3 for F in table.values()),'28 genuine width-three quotients')
  count=0
  for i in sorted(adj[j]):
   visible=sorted(h for h in table if H[h]<=adj[i]);need(len(visible)==16,'actual16 quotient view');A=np.vstack([table[h]for h in visible]);need(rank(A)==48,'every geometric source determinant');count+=1;native_cuts+=i<111
  all_cuts+=count;cut_counts[j]=count
  # The first incident centre fixes the recorded SHAKE labels, not source data.
  label=f'{next(h for h in centres if j in H[h])}/3/';rows=[]
  for h,F in sorted(table.items()):
   k=quota[j,h]//15;need(k in(1,2,3),'actual positive quota');seed=prm['early'][str(j)]
   if k>=2:
    rows.append(np.block([[F,np.zeros_like(F)],[np.zeros_like(F),F]]))
    if k==3:rows.append(random_rows(f'extra/{label}{j}/{h}/{seed}',3,96))
   elif h in centres:rows.append(np.hstack([F,np.zeros_like(F)]))
   else:
    change=random_rows(f'early/{label}{j}/{h}/{seed}',3,6);need(rank(change)==3,'early quotient rows extend to local frame');rows.append(np.hstack([mm(change[:,:3],F),mm(change[:,3:],F)]))
  early=np.vstack(rows);need(early.shape==(96,96)and rank(early)==96,'all eight actual early bases');early_matrices[j]=early.tolist();row_hashes[j]=hashlib.sha256(early.tobytes()).hexdigest()
 need(all_cuts==504 and native_cuts==468,'complete source cut quantifiers')
 fieldq=[qf(x)for x in range(64)];need(set(fieldq)=={0,1}and fieldq.count(0)==28,'GF64 minus norm');target=witt(range(64),qf);fibres={};Hwords={};fibre_counts={};union_hist=Counter();decisions={};readout_mutation_detected=False
 for h in centres:
  prm_h=prm['local'][str(h)];donors=sorted(H[h]);a0,b0=(roots[j]for j in donors[:2]);space={x for x in range(256)if not b(x,a0)and not b(x,b0)};source=witt(space,q);nodes={xor(source[k]for k in range(6)if mask>>k&1):xor(target[k]for k in range(6)if mask>>k&1)for mask in range(64)};need(len(nodes)==64 and all(q(x)==qf(y)for x,y in nodes.items()),'actual local quadratic isometry')
  basis=prm_h['F4_basis'];omega=prm_h['omega'];need(int(M[omega,omega])^omega==1,'literal F4 generator');coordinates={xor(basis[k]for k in range(6)if mask>>k&1):tuple(((mask>>(2*k))&1)^(omega if (mask>>(2*k+1))&1 else 0)for k in range(3))for mask in range(64)};need(len(coordinates)==64 and all(qf(x)==xor(power(t,3)for t in r)for x,r in coordinates.items()),'all64 Hermitian values');reverse={r:x for x,r in coordinates.items()};rotation={x:reverse[tuple(int(M[omega,t])for t in r)]for x,r in coordinates.items()}
  local_ports=[];radicals={}
  for d,P in enumerate(D):
   if not H[h]<=P:continue
   V=span(roots[j]for j in P);rad=sorted(x for x in V if x and all(not b(x,y)for y in V));need(len(rad)==3,'literal D radical')
   marked=all(rotation[nodes[x]]in{nodes[y]for y in rad}for x in rad)
   decisions.setdefault(d,set()).add(marked)
   if marked:local_ports.append(d);radicals[d]=rad
  need(local_ports==prm_h['ports']and len(local_ports)==9,'nine actual Desarguesian D exits');E1=np.array([[int(M[t,t])for t in coordinates[nodes[radicals[d][0]]]]for d in local_ports],dtype=np.uint8);E2=np.array([[int(M[x,x]),int(M[y,y]),int(M[z,z]),int(M[x,y]),int(M[x,z]),int(M[y,z])]for x,y,z in E1],dtype=np.uint8);need(rank(E1)==3 and rank(E2)==6,'evaluation row ranks')
  aa,bb=np.asarray(prm_h['weights'],dtype=np.uint8);need(np.all(aa)and np.all(bb)and np.all(aa^bb),'three nonzero quadratic weights');W=[null(M[c[:,None],E2].T).T for c in(aa^bb,bb,aa)];need(all(w.shape==(3,9)for w in W),'three canonical annihilator blocks');T=np.vstack(W);HW=invert(T);need(rank(HW)==9,'actual H word invertible');Hwords[h]=HW.tolist();views=[i for i in range(120)if H[h]<=adj[i]];need(len(views)==36,'all centre receivers');fibres[h]={}
  for i in views:
   visible=[p for p,d in enumerate(local_ports)if D[d]<=adj[i]];need(len(visible)==3,'three actual receiver exit ports');ev=mm(E1,np.array(coordinates[nodes[roots[i]]],dtype=np.uint8)[:,None])[:,0];need(set(visible)==set(np.flatnonzero(ev==0)),'literal visible ports equal three zero evaluations');kernel=None;images=[]
   for t,j in enumerate(donors):
    off=[p for p in sorted(maps[j])if p!=h and H[p]<=adj[i]];need(len(off)==15,'fifteen off-centre quotient maps');A=np.vstack([maps[j][p]for p in off]);K=null(A);need(K.shape==(48,3),'whole original-coordinate inverse fibre')
    if kernel is None:kernel=K
    else:need(np.array_equal(K,kernel),'three exactly equal complete canonical kernels')
    images.append(mm(mm(HW[np.ix_(visible,range(3*t,3*t+3))],maps[j][h]),kernel))
   need(rank(images[0])==3 and np.array_equal(images[0],images[1])and np.array_equal(images[0],images[2]),'same injective actual H port readout on whole fibre');fibres[h][i]=kernel.tolist()
   if not readout_mutation_detected:
    changed=HW.copy();changed[visible[0],0]^=1;bad=mm(mm(changed[np.ix_(visible,range(3))],maps[donors[0]][h]),kernel);readout_mutation_detected=not np.array_equal(bad,images[1])
  fibre_counts[h]={'geometric':len(views),'native':sum(i<111 for i in views)}
  point_flags={}
  for j in donors:
   point_flags[j]={}
   for p,P in enumerate(H):
    if j not in P or p==h:continue
    projected={roots[t]^(a0 if b(roots[t],b0)else 0)^(b0 if b(roots[t],a0)else 0)for t in P-{j}};need(len(projected)==1,'actual off-centre singular point');point=projected.pop();need(point and not q(point),'nonzero singular point');point_flags[j][point]=p
   need(len(point_flags[j])==27,'all27 point flags')
  need(len(set.intersection(*(set(v)for v in point_flags.values())))==27,'same point geometry')
  for point in point_flags[donors[0]]:
   for r,s in((0,1),(0,2),(1,2)):
    j,k=donors[r],donors[s];value=rank(np.vstack([maps[j][point_flags[j][point]],maps[k][point_flags[k][point]]]));union_hist[value]+=1;need(value==6,'complete quotient kernels differ despite common inverse fibres')
 need(all(len(v)==1 for v in decisions.values()),'selected-centre allocation agrees at shared D exits');need(union_hist=={6:324},'all324 distinct point-kernel comparisons');need(readout_mutation_detected,'one-entry H word mutation is detected')
 nonrs=json.loads((component/'output/NON-RS-WITNESSES.json').read_text());need(set(map(int,nonrs))==set(maps),'all8 non-RS witnesses')
 for j,w in nonrs.items():
  Ps=w['planes'];need(len(Ps)==len(set(Ps))==16 and set(Ps)<=set(maps[int(j)]),'sixteen valid source observations');need(rank(np.vstack([maps[int(j)][h]for h in Ps]))==w['rank']==47,'invariant failure of16-wise RS bijection')
 first=min(adj[0]&set(range(111)));A=np.vstack([maps[0][h]for h in sorted(maps[0])if H[h]<=adj[first]]);A[:3]=0;need(rank(A)==45,'one deleted real quotient negative control');phases={h:sum(quota[j,h]for j in H[h])for h in centres};need(phases=={263:90,642:90,135:45,44:45},'actual early phase totals');need(all(10 not in H[h]and not H[h]<=adj[80]for h in centres),'protected centres avoid both perturbed stars')
 result={'status':'PASS_INDEPENDENT_LITERAL_CLOSED_CYCLE_COMPONENT','no_author_or_predecessor_imports':True,'no_source_constructor_or_core_fibres_used':True,'source_dimension':48,'quotient_width':3,'donors':sorted(maps),'centres':centres,'source_geometric_cuts':all_cuts,'source_native_cuts':native_cuts,'source_cuts_per_donor':cut_counts,'common_fibres':fibre_counts,'geometric_common_fibres':sum(v['geometric']for v in fibre_counts.values()),'native_common_fibres':sum(v['native']for v in fibre_counts.values()),'actual_early_bases':8,'early_basis_dimension':96,'early_basis_sha256':row_hashes,'actual_H_early_slots':phases,'off_centre_pair_union_rank_histogram':dict(union_hist),'non_RS_sources':8,'reconstructed_H_words':4,'consistent_shared_D_component_allocation':True,'negative_controls':{'one_source_quotient_deleted_rank':45,'one_H_word_entry_mutation_detected':True},'standalone_global_extension_proved':False,'complete_physical_word_proved':False,'new_complete_kappa':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(args.out/'HWORDS.json').write_text(json.dumps(Hwords,sort_keys=True,separators=(',',':'))+'\n');(args.out/'EARLY-BASES.json.gz').write_bytes(gzip.compress(json.dumps(early_matrices,sort_keys=True,separators=(',',':')).encode(),mtime=0));(args.out/'FIBRES.json.gz').write_bytes(gzip.compress(json.dumps(fibres,sort_keys=True,separators=(',',':')).encode(),mtime=0));print(result['status'],all_cuts,144,135,8,flush=True)

if __name__=='__main__':main()
