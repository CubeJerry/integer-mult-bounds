"""Exact finite controls for the written arbitrary-Y normalization proof."""
from pathlib import Path
import argparse,collections,gzip,hashlib,itertools,json
from fractions import Fraction as F
if not __debug__:raise SystemExit('Exact checks require Python without -O')
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def act(rows,v):return sum(((r&v).bit_count()%2)<<j for j,r in enumerate(rows))
def form(rows,forms):
 out=[]
 for r in rows:
  v=0
  for j,f in enumerate(forms):
   if r>>j&1:v^=f
  out.append(v)
 return out
MATS=list(itertools.product(range(4),repeat=2))
def inverse_data(D):
 R=next(R for R in MATS if all(act(D,act(R,act(D,p)))==act(D,p) and act(R,act(D,act(R,p)))==act(R,p) for p in range(4)))
 basis=[];space={0}
 for p in range(1,4):
  if not act(D,p) and p not in space:basis.append(p);space|={z^p for z in list(space)}
 J=lambda t:__import__('functools').reduce(int.__xor__,(p for j,p in enumerate(basis) if t>>j&1),0)
 h=next(h for h in itertools.product(range(4),repeat=len(basis)) if all(act(h,J(t))==t for t in range(1<<len(basis))) and all(act(h,act(R,p))==0 for p in range(4)))
 assert all(act(R,act(D,p))==p^J(act(h,p)) for p in range(4))
 assert all(act(D,J(t))==0 for t in range(1<<len(basis)))
 return R,basis,h,J

def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==NATIVE;s=json.loads(gzip.decompress(raw));frames={int(k):v for k,v in s['frames'].items()};start=s['start'];end=s['final']
 assert len(set(end[111:222]))==111
 assert all(len(frames[start[i]]['B'])==1 and len(frames[end[i]]['B'])==8 for i in range(111))
 assert all(len(frames[start[111+i]]['B'])==0 and len(frames[end[111+i]]['B'])==7 for i in range(111))
 normals=[]
 for i in range(111):
  r=[F(x) for x in frames[start[i]]['B'][0]];normals.append(r)
  assert sum(x*x for x in r)>0
  assert all(sum(F(x)*y for x,y in zip(row,r))==0 for row in frames[end[111+i]]['B'])
 cells=values=symbolic=omit_fail=order_fail=outside_images=0;rank_hist=collections.Counter()
 for D in MATS:
  R,kbasis,h,J=inverse_data(D);rank_hist[2-len(kbasis)]+=1
  for v in range(4):
   if v not in {act(D,p) for p in range(4)}:
    assert v^act(D,act(R,v));outside_images+=1
  for C,A,B in itertools.product(MATS,repeat=3):
   cells+=1
   for u,p in itertools.product(range(4),repeat=2):
    pout=act(C,u)^act(D,p);T=act(h,p);recover=act(R,pout^act(C,u))^J(T)
    assert recover==p and (pout^act(C,u))^act(D,act(R,pout^act(C,u)))==0
    assert act(A,u)^act(B,recover)==act(A,u)^act(B,p)
    values+=1
    if act(R,pout^act(C,u))!=p:omit_fail+=1
    wrong=act(R,pout)^act(C,act(R,u))^J(T)
    if wrong!=p:order_fail+=1
   # Independent original forms: nonlocal x0,x1; local x2; nuisance y0,y1.
   U=[1<<2,1<<3];Pin=[(1<<0)^(1<<3),(1<<1)^(1<<4)]
   Pout=[x^y for x,y in zip(form(C,U),form(D,Pin))];T=form(h,Pin)
   recovered=[x^y for x,y in zip(form(R,[x^y for x,y in zip(Pout,form(C,U))]),form(tuple(sum(((p>>j)&1)<<i for i,p in enumerate(kbasis)) for j in range(2)),T))]
   assert recovered==Pin
   actual=[x^y for x,y in zip(form(A,U),form(B,Pin))]
   global_part=form(B,form(R,Pout));kernel_part=form(B,form(tuple(sum(((p>>j)&1)<<i for i,p in enumerate(kbasis)) for j in range(2)),T))
   remainder=[x^y^z for x,y,z in zip(actual,global_part,kernel_part)]
   assert all((v&3)==0 for v in remainder) # no nonlocal x columns
   projected=[v&7 for v in remainder];assert all(v in [0,4] for v in projected)
   symbolic+=1
 assert cells==65536 and values==1048576 and symbolic==65536 and omit_fail>0 and order_fail>0 and outside_images>0
 # Y/packet swap: D=0, actual historical kernel oldP is essential.
 oldP=(1<<0)^(1<<1);oldY=1<<3;newP=oldY;newY=oldP
 assert (newP&7)==0 and (newY&7)==oldP
 # At0 a retained generated cache may cancel P before CLEAR; first arrival is essential.
 ground_first=(1<<0)^(1<<3);cache=ground_first;preclear=ground_first^cache
 assert preclear==0 and (cache&7)==1 and (ground_first&7)==1
 deps=['results/bit-source-packet-scattering/author/PROOF.md','results/bit-source-packet-scattering/ADMISSION.md','results/bit-monotone-arrival-gate/PROOF.md','results/bit-binary-four-quotients/ADMISSION.md','results/bit-binary-four-quotients/review/REVIEW.md','results/bit-eight-packet-target/strict-price/ADMISSION.md','results/bit-minimum-rank-nine/ADMISSION.md']
 base=a.repo/'research/moonshot-005-program';pins={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in deps}
 result={'status':'PASS_FINITE_CONTROLS_Y_NUISANCE_NORMALIZATION','native_sha256':NATIVE,'dependency_pins':pins,'source_roles':{'X_ascending_line_to_Hub':111,'Y_ascending_zero_to_distinct_facets':111},'through_rank_histogram':dict(rank_hist),'all_four_by_four_binary_cells':cells,'actual_input_reconstructions':values,'mixed_X_Y_symbolic_locality_checks':symbolic,'omitted_kernel_failures':omit_fail,'wrong_noncommuting_order_failures':order_fail,'out_of_image_vectors_rejected':outside_images,'Y_swap_terminal_X_projection_zero_but_kernel_essential':True,'first_ground_boundary_control':True,'universal_proof':'Written poset/cell induction; finite tests are not its substitute.','scope':'Arbitrary cocharted originalY feedback with fixed monotone carriers; generated ascending copies require paid facetarrival accounting. No complete q8 source or newkappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='dependency_pins'},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
