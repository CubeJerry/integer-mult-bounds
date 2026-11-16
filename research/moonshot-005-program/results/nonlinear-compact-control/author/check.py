#!/usr/bin/env python3
"""Exact source/parameter linkage; independent modular replay is separate."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
here=Path(__file__).resolve().parent
deps=json.loads((here/'DEPENDENCIES.json').read_text())
for s in deps['canonical_sources']:
 assert hashlib.sha256((here/s['retained_copy']).read_bytes()).hexdigest()==s['sha256']
# Algebraic four-term identity and all four omission controls.
omission=[0]*4
for u,v,x,z in itertools.product(range(2),repeat=4):
 terms=[u*v,(u^x)*v,(u^x)*(v^z),u*(v^z)]
 assert (sum(terms)%2)==x*z
 for j in range(4):omission[j]+=((sum(terms)-terms[j])%2!=x*z)
assert all(omission)
assert 4*4+4*2==24 and 4*4+4==20
# Rigorous guard inequalities at powers-of-two boundaries and interiors.
ps=set(range(1,257))|{2**k+s for k in range(9,25) for s in [-1,0,1]}
guard_cases=0
for p in sorted(ps):
 l=(p-1).bit_length();G=4*l+6
 for extra in [0,1,7,37]:
  K=G+4*l+10+extra
  delta=F(p*3,2**G)+F(p*8,2**(K-G))
  assert delta<=F(7,128*p**3)
  guard_cases+=1
# Reservation is an exact ceiling bound, before fallback/strict exponent use.
reservation_cases=0
for d in range(1,129):
 for G in [1,2,6,14,38,70]:
  H=d*G
  for K in [1,2,7,31,H,H+1,4*H+1]:
   qF=(3*H+K-1)//K;qB=(H+K-1)//K
   assert qF*K>=3*H and qB*K>=H
   assert qF+qB<=F(4*H,K)+2
   for f in [1,d//2+1,d]:assert (f-1)*G<=H
   reservation_cases+=1
def swap(x,a,b):
 if ((x>>a)^(x>>b))&1:x^=(1<<a)|(1<<b)
 return x
def lowered(x,a,b,c,undo=True):
 last=max(a,b,c);q=swap(x,a,last);mapping={a:last,last:a} if a!=last else {a:a}
 bb=mapping.get(b,b);cc=mapping.get(c,c)
 assert bb<last and cc<last
 q^=(((q>>bb)&1)*((q>>cc)&1))<<last
 return swap(q,a,last) if undo else q
highest_cases=bad_inverse=0
for d in range(3,9):
 for a in range(d):
  for b,c in itertools.combinations([j for j in range(d) if j!=a],2):
   for x in range(1<<d):
    expect=x^((((x>>b)&1)*((x>>c)&1))<<a)
    actual=lowered(x,a,b,c);assert actual==expect
    assert lowered(actual,a,b,c)==x
    if a!=max(a,b,c):bad_inverse+=lowered(x,a,b,c,False)!=expect
    highest_cases+=1
assert bad_inverse
phase_cases=0;phase_controls=0
table=[(2*(j&1)*((j>>1)&1)*((j>>2)&1)+((j>>1)&1))%4 for j in range(8)]
for f in range(1,5):
 for columns in itertools.product(range(8),repeat=f):
  phase=(f+sum(table[j] for j in columns))%4
  literal=0
  for j in columns:literal=(literal+1+table[j])%4
  assert phase==literal
  phase_controls+=(1+sum(table[j] for j in columns))%4!=literal
  phase_cases+=1
assert phase_controls
result={'status':'PASS_NONLINEAR_COMPACT_PARAMETER_LINKAGE','proof_sha256':hashlib.sha256((here/'PROOF.md').read_bytes()).hexdigest(),
 'canonical_source_pins_verified':len(deps['canonical_sources']),
 'dirty_gray_identity_cases':16,'four_omission_witness_counts':omission,
 'low_selected_compact_swaps':24,'low_selected_controlled_rotations':20,
 'guard_cases':guard_cases,'proved_bad_fraction':'7/(128*p^3)',
 'reservation_cases':reservation_cases,'reservation_floor_bits':{'front':'3*d*G','back':'d*G'},
 'highest_bit_lowering_cases':highest_cases,'omitted_inverse_swap_failures':bad_inverse,
 'phase_lift_cases':phase_cases,'unlifted_absolute_phase_failures':phase_controls,
 'universal_status':'conditional proof in PROOF.md; finite checks supplement it',
 'complete_modular_replay':'separate independent-c package','new_complete_kappa':False}
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
