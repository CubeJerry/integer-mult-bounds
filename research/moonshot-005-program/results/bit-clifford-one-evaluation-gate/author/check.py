#!/usr/bin/env python3
"""Exact native Clifford word envelope and its retained return-budget gate."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json,random

LAYOUT_PIN='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
def need(x,label):
 if not x:raise ValueError(label)
def rank(rows):
 piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p not in piv:piv[p]=x;break
   x^=piv[p]
 return len(piv)
def mm(A,B):
 out=[]
 for x in A:
  z=0
  while x:
   low=x&-x;z^=B[low.bit_length()-1];x^=low
  out.append(z)
 return out
def flatten(A):return sum(row<<(16*i)for i,row in enumerate(A))
def action(A,x):return sum(((row&x).bit_count()%2)<<i for i,row in enumerate(A))
def inv_rational(A):
 n=len(A);a=[[Q(x)for x in row]+[Q(i==j)for j in range(n)]for i,row in enumerate(A)]
 determinant=Q(1)
 for c in range(n):
  k=next(k for k in range(c,n)if a[k][c])
  if k!=c:a[c],a[k]=a[k],a[c];determinant=-determinant
  d=a[c][c];determinant*=d;a[c]=[x/d for x in a[c]]
  for k in range(n):
   if k!=c and a[k][c]:
    m=a[k][c];a[k]=[x-m*y for x,y in zip(a[k],a[c])]
 return [row[n:]for row in a],determinant

def main():
 ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 programme=a.repo/'research/moonshot-005-program'
 layout_path=programme/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
 raw=gzip.decompress(layout_path.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_PIN,'native layout pin')
 layout=json.loads(raw);roots=layout['root_table'];planes=list(map(set,layout['A2']))
 basis_path=Path(__file__).with_name('BASIS.json');cert=json.loads(basis_path.read_text());cols=cert['lattice_basis_columns']
 basis=[[cols[j][i]for j in range(8)]for i in range(8)];inverse,det=inv_rational(basis);need(abs(det)==16,'lattice determinant')
 G=[[sum(x*y for x,y in zip(cols[i],cols[j]))for j in range(8)]for i in range(8)]
 need(all(x%2==0 for row in G for x in row)and all(G[i][i]%4==0 for i in range(8)),'integral even Gram')
 _,gramdet=inv_rational([[Q(x,2)for x in row]for row in G]);need(gramdet==1,'unimodular scaled Gram')
 qdiag=[(G[i][i]//4)%2 for i in range(8)];beta=[[G[i][j]//2%2 for j in range(8)]for i in range(8)]
 need(rank([sum(x<<j for j,x in enumerate(row))for row in beta])==8,'nondegenerate polar form')
 def q(v):return (sum(qdiag[i]for i in range(8)if v>>i&1)+sum(beta[i][j]for i in range(8)for j in range(i)if v>>i&1 and v>>j&1))%2
 def bil(v,w):return sum(beta[i][j]for i in range(8)for j in range(8)if v>>i&1 and w>>j&1)%2
 masks=[]
 for root in roots:
  coords=[sum(c*x for c,x in zip(row,root))for row in inverse];need(all(c.denominator==1 for c in coords),'root lattice coordinates')
  masks.append(sum((int(c)%2)<<i for i,c in enumerate(coords)))
 need(len(set(masks))==120 and all(q(v)==1 for v in masks),'all nonsingular native roots')
 need(sum(q(v)for v in range(256))==120,'plus quadratic type')
 hyp=cert['hyperbolic_basis_masks'];need(rank(hyp)==8,'hyperbolic basis independence')
 need(all(q(v)==0 for v in hyp),'singular hyperbolic basis vectors')
 need(all(bil(hyp[i],hyp[j])==int(i//2==j//2 and i!=j)for i in range(8)for j in range(8)),'hyperbolic pairings')
 lookup={}
 for v in range(256):
  mask=0
  for k in range(8):
   if v>>k&1:mask^=hyp[k]
  lookup[mask]=v
 I=[1<<i for i in range(16)];primitive=[]
 for k in range(4):
  create=[0]*16;erase=[0]*16
  for j in range(16):
   if j>>k&1:erase[j^(1<<k)]^=1<<j
   else:create[j|(1<<k)]^=1<<j
  primitive.extend([create,erase])
 def gamma(v):
  rows=[0]*16
  for k in range(8):
   if lookup[v]>>k&1:rows=[x^y for x,y in zip(rows,primitive[k])]
  return rows
 gs=[gamma(v)for v in range(256)]
 for v in range(256):need(mm(gs[v],gs[v])==[q(v)*x for x in I],'all gamma squares')
 for v in range(256):
  for w in range(256):need([x^y for x,y in zip(mm(gs[v],gs[w]),mm(gs[w],gs[v]))]==[bil(v,w)*x for x in I],'all Clifford pair identities')
 rootg=[gs[v]for v in masks]
 adj=[{j for j,y in enumerate(roots)if i!=j and sum(x*z for x,z in zip(root,y))==0}for i,root in enumerate(roots)]
 need(all((j in adj[i])==(bil(masks[i],masks[j])==0)for i in range(120)for j in range(i)),'real and binary orthogonality')
 local={}
 for h,H in enumerate(planes):
  j,k=sorted(H)[:2];need(bil(masks[j],masks[k])==1,'A2 anisotropic generators')
  basisH=[I,rootg[j],rootg[k],mm(rootg[j],rootg[k])]
  need(rank(list(map(flatten,basisH)))==4,'full local Clifford algebra dimension')
  local[h]=basisH
 hist=Counter();critical=None
 for i in range(111):
  for j in sorted(adj[i]&set(range(111))):
   visible=[h for h,H in enumerate(planes)if j in H and H<=adj[i]]
   need(len(visible)==16,'sixteen actual source planes')
   matrices=[M for h in visible for M in local[h]]
   dim=rank(list(map(flatten,matrices)));need(dim==14,'actual local-word envelope dimension')
   hist[dim]+=1
   if(i,j)==(5,77):critical=(visible,matrices)
 need(hist=={14:6470}and critical is not None,'complete native envelope census')
 frame=[9,30,37,46,52,77,92,101]
 need(all(v not in adj[u]for u,v in combinations(frame,2)),'critical frame noncontacts')
 edge_roles={}
 for j in range(111):
  e=tuple(k for k,v in enumerate(frame)if v in adj[j])
  if len(e)==2:need(e not in edge_roles,'unique frame edges');edge_roles[e]=j
 C=range(7);need(all(e in edge_roles for e in combinations(C,2)),'critical K7')
 need(edge_roles[0,5]==5 and frame[5]==77,'actual critical pair')
 for e,j in edge_roles.items():
  for f,k in edge_roles.items():
   if j!=k and set(e)&set(f):need(k not in adj[j],'shared endpoint zeros')
 # Direct evaluation controls include arbitrary binary vectors and an
 # explicit two-vector escape. They are not the proof of the bound.
 mats=critical[1];rng=random.Random(271119);vectors=[1<<i for i in range(16)]+[rng.randrange(1,1<<16)for _ in range(128)]
 ranks=[rank([action(M,v)for M in mats])for v in vectors];need(max(ranks)<=14,'one-vector information bound')
 escape=None
 for v,w in combinations(vectors,2):
  union=[action(M,v)for M in mats]+[action(M,w)for M in mats]
  if rank(union)==16:escape=[v,w];break
 need(escape is not None,'two-vector hypothesis escape')
 # Exact native return gate dependencies and strict rational comparison.
 movement_path=programme/'results/bit-near-minimum-foreign-rank/author/output/RATIONAL-MOVEMENT.json'
 near_proof=programme/'results/bit-near-minimum-foreign-rank/author/PROOF.md'
 return_proof=programme/'results/bit-replacement-return-bank/author/PROOF.md'
 movement=json.loads(movement_path.read_text());room_upper=Q(movement['room_interval'][1])
 need(room_upper<Q(279,1000),'retained limiting room bound')
 need(Q(movement['finite_budget_offset_numerator_T2_minus_P2'][1])<0,'strict finite-budget correction')
 need(8**199>7**200 and Q(7,24)>Q(279,1000),'exact movement obstruction')
 need(Q(7,24)-Q(279,1000)==Q(19,1500),'rational separation margin')
 pins=[{'path':str(p.relative_to(a.repo)),'sha256':sha256(p.read_bytes()).hexdigest()}for p in [layout_path,movement_path,near_proof,return_proof]]
 result={'status':'PASS_NATIVE_CLIFFORD_ONE_VECTOR_SOURCE_GATE','field':'every finite characteristic-two field',
         'source_domain':'End(F^16)^r, one donor/copy evaluation vector, local Clifford right words',
         'lattice_determinant':16,'gamma_square_checks':256,'gamma_pair_checks':65536,
         'A2_algebras_checked':1120,'native_foreign_envelope_histogram':dict(hist),
         'critical_pair':[5,77],'critical_frame':frame,'critical_visible_planes':critical[0],
         'one_vector_sample_rank_histogram':dict(Counter(ranks)),'two_vector_full_span_control':escape,
         'source_rank_fraction':'7/8','required_return_excess_fraction':'1/24',
         'new_irreducible_target_excess_fraction':'1/30','strict_rational_movement_gap':'19/1500',
         'examples':[{'b':3840,'required_excess':160,'irreducible_target_excess':128},
                     {'b':11520,'required_excess':480,'strict_retained_allowance_upper':405}],
         'allows_noncommuting_coefficients':True,'general_clifford_sources_excluded':False,
         'new_complete_kappa':False,'source_pins':pins,'basis_sha256':sha256(basis_path.read_bytes()).hexdigest()}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(result['status']);print(json.dumps({k:result[k]for k in ['native_foreign_envelope_histogram','one_vector_sample_rank_histogram','two_vector_full_span_control','required_return_excess_fraction']},sort_keys=True))
if __name__=='__main__':main()
