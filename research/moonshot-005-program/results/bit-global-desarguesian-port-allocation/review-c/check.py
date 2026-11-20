#!/usr/bin/env python3
"""Independent audit of the global marked-D certificate.

Pure Python integer arithmetic. No author or predecessor code is imported.
The native A2/D4 atlas is regenerated from the pinned quadratic coordinates;
endomorphisms use a row-major unknown matrix and least-pivot elimination;
maximal singular spaces are enumerated by unique binary RREF bases.
"""
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from itertools import combinations,product
from pathlib import Path

def require(x,s):
 if not x:raise AssertionError(s)
def foldxor(xs):
 x=0
 for y in xs:x^=y
 return x
def quad(x):return ((x&(x>>1))&0x55).bit_count()&1
def bilinear(x,y):return (x&(((y&0x55)<<1)|((y&0xaa)>>1))).bit_count()&1
def span(vs):
 A={0}
 for v in vs:A|={u^v for u in tuple(A)}
 return frozenset(A)
def rank_binary(rows):
 basis={}
 for r in rows:
  while r:
   j=(r&-r).bit_length()-1
   if j in basis:r^=basis[j]
   else:basis[j]=r;break
 return len(basis)
def independent(rows):
 basis={};answer=[]
 for original in rows:
  r=original
  while r:
   j=(r&-r).bit_length()-1
   if j in basis:r^=basis[j]
   else:basis[j]=r;answer.append(original);break
 return answer

def singular_spaces(dimension):
 # Each binary subspace has one reduced row-echelon basis, with its pivot
 # coordinates in increasing order. Filter row domains and pairwise polarities.
 spaces=set()
 for pivots in combinations(range(8),dimension):
  P=set(pivots);domains=[]
  for pivot in pivots:
   free=[j for j in range(pivot+1,8)if j not in P]
   domains.append([v for z in range(1<<len(free))if not quad(v:=(1<<pivot)|foldxor(1<<j for k,j in enumerate(free)if z>>k&1))])
  def extend(rows):
   if len(rows)==dimension:spaces.add(span(rows));return
   for v in domains[len(rows)]:
    if all(not bilinear(v,w)for w in rows):extend(rows+[v])
  extend([])
 return spaces

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 base=a.repo/'research/moonshot-005-program/results';package=base/'bit-global-desarguesian-port-allocation';pins=json.loads((package/'SOURCE-PINS.json').read_text())['files']
 for name,digest in pins.items():require(hashlib.sha256((a.repo/name).read_bytes()).hexdigest()==digest,'pinned data '+name)
 lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json';wp=package/'author/WITNESS.json.gz';oldp=base/'bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz';cp=base/'bit-coupled-native-geometric-h-source/component/output/PARAMETERS.json';cm=base/'bit-coupled-native-geometric-h-source/component/MANIFEST.json'
 manifest=json.loads(cm.read_text());require(hashlib.sha256(cp.read_bytes()).hexdigest()==manifest['files']['output/PARAMETERS.json'],'actual H263 component parameter pin')
 L=json.loads(gzip.decompress(lp.read_bytes()));B=json.loads(bp.read_text());W=json.loads(gzip.decompress(wp.read_bytes()));old=json.loads(gzip.decompress(oldp.read_bytes()));component=json.loads(cp.read_text())
 cols=B['lattice_basis_columns'];A=[[cols[j][i]for j in range(8)]for i in range(8)];require(all(A[i][j]==0 for i in range(8)for j in range(i)),'independently triangular lattice basis')
 masks=B['hyperbolic_basis_masks'];to_lattice={x:foldxor(masks[j]for j in range(8)if x>>j&1)for x in range(256)};require(len(set(to_lattice.values()))==256,'binary coordinate isomorphism');from_lattice={v:k for k,v in to_lattice.items()}
 # Independently verify the quadratic form against the actual integer lattice.
 for x,m in to_lattice.items():
  v=[sum(cols[j][i]for j in range(8)if m>>j&1)for i in range(8)];norm=sum(z*z for z in v);require(norm%4==0 and norm//4%2==quad(x),'physical norm /4 quadratic convention')
 roots=[]
 for root in L['root_table']:
  coord=[0]*8
  for i in range(7,-1,-1):
   numerator=root[i]-sum(A[i][j]*coord[j]for j in range(i+1,8));coord[i],rem=divmod(numerator,A[i][i]);require(rem==0,'integral lattice back-substitution')
  require([sum(A[i][j]*coord[j]for j in range(8))for i in range(8)]==root,'exact root reconstruction')
  roots.append(from_lattice[sum((z&1)<<j for j,z in enumerate(coord))])
 nonsingular={x for x in range(256)if quad(x)};require(len(roots)==len(set(roots))==120 and set(roots)==nonsingular,'all literal nonsingular root coordinates')
 H=[frozenset(roots[j]for j in ids)for ids in L['A2']];D=[frozenset(roots[j]for j in ids)for ids in L['D4']]
 require(len(H)==len(set(H))==1120 and len(D)==len(set(D))==3150,'distinct native chart rosters')
 actual_H={frozenset((x,y,x^y))for x,y in combinations(sorted(nonsingular),2)if bilinear(x,y)};require(set(H)==actual_H,'regenerated complete anisotropic-plane atlas')
 singular={x for x in range(1,256)if not quad(x)};lines={frozenset((0,x,y,x^y))for x,y in combinations(sorted(singular),2)if not bilinear(x,y)};require(len(lines)==1575,'all singular radical lines')
 # For each radical line, its perpendicular has two connected components of
 # nonsingular vectors under B(x,y)=1. They are the two actual D4 root sets.
 regenerated=set();by_rad={}
 for radical in lines:
  r,s=sorted(radical-{0})[:2];points={x for x in nonsingular if not bilinear(x,r)and not bilinear(x,s)};require(len(points)==24,'radical-perpendicular nonsingular census')
  seed=min(points);left={seed};pending=[seed]
  while pending:
   x=pending.pop();new={y for y in points-left if bilinear(x,y)};left|=new;pending.extend(new)
  right=points-left;require(len(left)==len(right)==12,'two D4 components per radical')
  for ds in (frozenset(left),frozenset(right)):
   require(span(ds)==radical|ds,'exact four-space and radical');require(all(not bilinear(x,y)for x in radical for y in ds),'singular radical annihilates D4');regenerated.add(ds)
  by_rad[radical]=(frozenset(left),frozenset(right))
 require(regenerated==set(D),'regenerated complete D4 atlas')
 Dindex={ds:i for i,ds in enumerate(D)};Hindex={hs:i for i,hs in enumerate(H)};radicals=[None]*3150;dual=[None]*3150;perps=[None]*3150
 for radical,(left,right)in by_rad.items():
  i,j=Dindex[left],Dindex[right];radicals[i]=radicals[j]=radical;dual[i]=j;dual[j]=i;perps[i]=radical|right;perps[j]=radical|left
 for d,ds in enumerate(D):require(perps[d]==frozenset(x for x in range(256)if all(not bilinear(x,y)for y in ds)),'exact perpendicular chart')
 supplied=L['dual_D4'];require((supplied if isinstance(supplied,list)else[supplied[str(i)]for i in range(3150)])==dual,'literal native perpendicular table')
 selected_list=W['selected_D'];require(selected_list==sorted(set(selected_list))and len(selected_list)==630 and all(type(i)is int and 0<=i<3150 for i in selected_list),'canonical marked-D list');selected=set(selected_list)
 require(all((d in selected)==(dual[d]in selected)for d in range(3150)),'all3150 perpendicular covariance checks')
 marked_lines={radicals[d]for d in selected};require(len(marked_lines)==315,'two D labels per marked radical')
 ports=[[]for _ in H];parents=[[]for _ in D]
 for d,ds in enumerate(D):
  local={frozenset((x,y,x^y))for x,y in combinations(sorted(ds),2)if bilinear(x,y)};require(len(local)==16 and local<=actual_H,'sixteen actual H flags at D')
  for hs in local:h=Hindex[hs];ports[h].append(d);parents[d].append(h)
 profiles=0
 for d,hs in enumerate(parents):
  for v in D[d]:require(sum(v in H[h]for h in hs)==4,'four parent flags per D donor');profiles+=1
 require(profiles==37800,'all actual D-donor profiles')
 local_structures=W['local_structures'];require(len(local_structures)==1120,'one local field structure per actual H')
 dimensions=Counter();point_count=views=native_views=0;selected_by_H=[];all_orbit_checks=0;conjugate_checks=0
 for h,hs in enumerate(H):
  hp=frozenset(x for x in range(256)if all(not bilinear(x,y)for y in hs));require(len(hp)==64,'six-dimensional actual H perpendicular')
  chosen=sorted(selected&set(ports[h]));require(len(ports[h])==45 and len(chosen)==9,'all45/9 port quotas');selected_by_H.append(chosen)
  zero_points={x for x in hp if x and not quad(x)};reservation=Counter(x for d in chosen for x in radicals[d]if x);require(len(zero_points)==27 and reservation==Counter({x:1 for x in zero_points}),'all27 point reservations');point_count+=27
  local=local_structures[h];require(local['H']==h,'literal local structure index');basis=local['coordinate_basis'];require(len(basis)==6 and all(type(x)is int and 0<x<256 for x in basis)and span(basis)==hp,'literal local coordinate isomorphism')
  back=[foldxor(basis[j]for j in range(6)if x>>j&1)for x in range(64)];forward={v:x for x,v in enumerate(back)};packed=local['J'];require(type(packed)is int and 0<=packed<(1<<36),'operator encoding bounds');columns=[(packed>>(6*c))&63 for c in range(6)]
  image=[foldxor(columns[c]for c in range(6)if x>>c&1)for x in range(64)];require(len(set(image))==64,'field operator is invertible')
  require(all(image[image[x]]^image[x]^x==0 for x in range(64)),'irreducible quadratic relation on every vector');require(all(quad(back[image[x]])==quad(back[x])for x in range(64)),'actual quadratic preservation')
  local_lines={frozenset(forward[x]for x in radicals[d])for d in chosen};equations=[]
  for line in local_lines:
   r,s=sorted(line-{0})[:2];ann=independent(x for x in range(64)if not(x&r).bit_count()%2 and not(x&s).bit_count()%2);require(len(ann)==4,'line annihilator dimension')
   for v in (r,s):
    for z in ann:equations.append(foldxor(v<<(6*row)for row in range(6)if z>>row&1))
  matrix=foldxor(1<<(6*r+c)for r in range(6)for c in range(6)if columns[c]>>r&1);identity=foldxor(1<<(7*r)for r in range(6))
  require(all(not(e&matrix).bit_count()%2 and not(e&identity).bit_count()%2 for e in equations),'row-major invariant-endomorphism constraints');dimension=36-rank_binary(equations);dimensions[dimension]+=1;require(dimension==2 and matrix not in(0,identity),'exact endomorphism field dimension')
  # Directly reconstruct all21 F4-orbit lines. The nine singular lines must
  # coincide with the marked ports; this certifies Desarguesian structure.
  orbits={frozenset((0,x,image[x],image[image[x]]))for x in range(1,64)};require(len(orbits)==21 and all(len(o)==4 for o in orbits),'complete21-line Desarguesian spread');require(Counter(x for o in orbits for x in o if x)==Counter({x:1 for x in range(1,64)}),'all63 nonzero vectors partitioned')
  singular_orbits={o for o in orbits if all(not quad(back[x])for x in o)};require(singular_orbits==local_lines and len(singular_orbits)==9,'marked nine equal all singular F4 lines');all_orbit_checks+=21
  squared=[image[image[x]]for x in range(64)];require(all(squared[squared[x]]^squared[x]^x==0 for x in range(64))and{frozenset((0,x,squared[x],squared[squared[x]]))for x in range(1,64)}==orbits,'positive conjugate field generator');conjugate_checks+=1
  for i,x in enumerate(roots):
   if x not in hp:continue
   visible=[d for d in ports[h]if x in perps[d]];require(len(visible)==15 and len(selected&set(visible))==3,'every actual receiver three/twelve split');views+=1;native_views+=i<111
 require(point_count==30240 and views==40320 and native_views==37296,'complete point and receiver quantifiers')
 require(component['H']==263 and selected_by_H[263]==component['ports']==[110,132,720,810,1509,1735,1994,2621,2836],'actual new H263 component port binding')
 counts=[];four_spaces=None
 for d in range(1,5):
  spaces_d=singular_spaces(d);counts.append(len(spaces_d))
  if d==2:require(spaces_d==lines,'independent RREF radical-line enumeration')
  if d==4:four_spaces=spaces_d
 require(counts==[135,1575,2025,270],'complete RREF singular Grassmannians')
 histogram=Counter()
 for Z in four_spaces:
  contained={line for line in lines if line<=Z};require(len(contained)==35,'all35 lines of every maximal singular space');histogram[len(contained&marked_lines)]+=1
 require(histogram=={0:72,7:135,15:63},'no orthogonal-spread inducing space')
 changed=len(selected^set(old['selected_D']));require(changed==840,'literal old/new marking difference')
 # Adversarial controls distinguish covariance, quotas and field structure.
 flipped=selected^{selected_list[0]};broken_single=sum(len(flipped&set(ps))!=9 for ps in ports);require(broken_single==16,'single-D mutation breaks exactly16 H quotas')
 first=selected_list[0];flipped_pair=selected^{first,dual[first]};require(all((d in flipped_pair)==(dual[d]in flipped_pair)for d in range(3150)),'dual-pair mutation preserves covariance');broken_pair=sum(len(flipped_pair&set(ps))!=9 for ps in ports);require(broken_pair==32,'dual-pair mutation still breaks32 H quotas')
 require(any((x^x^x)!=0 for x in range(64)),'identity operator fails irreducible field relation despite line and q preservation')
 result={'status':'PASS_INDEPENDENT_GLOBAL_DESARGUESIAN_PORT_ALLOCATION','no_author_or_predecessor_code_imported':True,'native_A2_atlas_regenerated':1120,'native_D4_atlas_regenerated':3150,'physical_quadratic_norm_checks':256,'marked_D':630,'marked_radical_lines':315,'all_H':1120,'point_reservations':point_count,'receiver_views':views,'native_receiver_views':native_views,'D_donor_profiles':profiles,'perpendicular_covariance_checks':3150,'local_endomorphism_dimension_histogram':dict(dimensions),'complete_F4_orbit_lines_checked':all_orbit_checks,'conjugate_generator_controls':conjugate_checks,'singular_subspace_counts_RREF':counts,'maximal_singular_four_space_marked_line_histogram':dict(histogram),'changed_from_old_marking':changed,'H263_actual_component_ports':selected_by_H[263],'negative_controls':{'single_D_broken_H':broken_single,'dual_pair_broken_H':broken_pair,'identity_operator_rejected':True},'witness_sha256':hashlib.sha256(wp.read_bytes()).hexdigest(),'witness_payload_sha256':hashlib.sha256(gzip.decompress(wp.read_bytes())).hexdigest(),'source_files':{str(f.relative_to(a.repo)):hashlib.sha256(f.read_bytes()).hexdigest()for f in[lp,bp,wp,oldp,cp,cm]},'source_word_certified':False,'common_middle_word_certified':False,'complete_kappa_claimed':False}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],1120,630,30240,40320,flush=True)

if __name__=='__main__':main()
