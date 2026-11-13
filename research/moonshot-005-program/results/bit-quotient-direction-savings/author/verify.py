from pathlib import Path
import json,gzip,itertools,hashlib,time
from fractions import Fraction as F
import numpy as np
import argparse,collections
if not __debug__:raise SystemExit("Assertions are required; do not use python -O")
p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--output",type=Path,required=True);args=p.parse_args()
native=args.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';blob=native.read_bytes();assert hashlib.sha256(blob).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
s=json.loads(gzip.decompress(blob));roots=[]
for i in range(111):
 v=[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]];n=sum(x*x for x in v);v=[x*(2 if n==1 else 1) for x in v];assert all(x.denominator==1 for x in v);v=list(map(int,v));assert sum(x*x for x in v)==4;roots.append(v)
R=np.array(roots,dtype=np.int64);D=R@R.T;A=D//2;assert np.all(D%2==0);deg=(D==0).sum(axis=1)
# Every rank-three span has a triple basis from the actual source. Exact Gram determinants and membership, without numerical rank.
triples=np.array(list(itertools.combinations(range(111),3)));flats={};t0=time.time();independent=0
for start in range(0,len(triples),2048):
 ids=triples[start:start+2048];x=A[ids[:,0],ids[:,1]];y=A[ids[:,0],ids[:,2]];z=A[ids[:,1],ids[:,2]];det=8-2*(x*x+y*y+z*z)+2*x*y*z;assert np.all(det>=0);ok=det>0;ids=ids[ok];x=x[ok];y=y[ok];z=z[ok];det=det[ok];independent+=len(ids)
 d0=A[ids[:,0]];d1=A[ids[:,1]];d2=A[ids[:,2]]
 val=(4-z*z)[:,None]*d0*d0+(4-y*y)[:,None]*d1*d1+(4-x*x)[:,None]*d2*d2+2*(y*z-2*x)[:,None]*d0*d1+2*(x*z-2*y)[:,None]*d0*d2+2*(x*y-2*z)[:,None]*d1*d2
 membership=val==2*det[:,None]
 for ids0,m in zip(ids,membership):
  key=np.packbits(m).tobytes()
  if key not in flats:flats[key]=tuple(map(int,ids0))
rows=[]
for key,ids in flats.items():
 V=np.flatnonzero(np.unpackbits(np.frombuffer(key,dtype=np.uint8))[:111]).tolist()
 if len(V)<5:continue
 U=np.flatnonzero(np.all(D[:,ids]==0,axis=1)).tolist()
 for width in [5,6]:
  if width>len(V):continue
  potential=sum(int(deg[i])<=52+width for i in U)
  rows.append({'basis':ids,'flat':V,'width':width,'orthogonal_roots':U,'eligible_count':potential,'total_orthogonal':len(U)})
max3=max(r['eligible_count'] for r in rows)
# The r4,s4,j4 case: four mutually orthogonal roots. Enumerate actual 4-cliques and count low-degree common perpendiculars exactly.
ortho=D==0;best4=0;four=[];count4=0
for a in range(111):
 for b in range(a+1,111):
  if not ortho[a,b]:continue
  for c in range(b+1,111):
   if not (ortho[a,c] and ortho[b,c]):continue
   ds=np.flatnonzero(ortho[a]&ortho[b]&ortho[c]& (np.arange(111)>c))
   for d in ds:
    count4+=1;u=np.flatnonzero(ortho[a]&ortho[b]&ortho[c]&ortho[d]&(deg<=56)).tolist();gain=len(u)+8
    if gain>best4:best4=gain;four=[{'basis':[a,b,c,int(d)],'low_degree_orthogonal':u,'upper_gain':gain}]
    elif gain==best4:four.append({'basis':[a,b,c,int(d)],'low_degree_orthogonal':u,'upper_gain':gain})
# Independent finite parameter envelope and sharp fitting witness.
N={0:0,1:1,2:3,3:6,4:12,5:20,6:36,7:111,8:111}
hist=dict(sorted(collections.Counter(map(int,deg)).items()))
assert hist=={55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}
H=lambda cutoff:sum(v for k,v in hist.items() if k<=cutoff)
envelope=[]
for r in range(1,9):
 for width in range(r,N[r]+1):
  for j in range(min(r,width)+1):
   if width>j+N[r-j]:continue
   u=N[8-r];bound=min(u,H(52+width))+min(u,H(36+width))+2*j
   envelope.append([r,width,j,bound])
assert len(envelope)==569
critical=[row for row in envelope if row[3]>=17]
assert critical==[[3,5,0,20],[3,6,0,20],[4,4,3,18],[4,4,4,20]]
assert independent==220934 and len(flats)==74396 and len(rows)==11761
assert max3==17 and count4==90079 and best4==15
V=[0,2,38,41,42,45];U=np.flatnonzero(np.all(D[:,V]==0,axis=1)).tolist()
assert len(U)==20 and not set(U)&set(V)
K=(D==0).astype(np.uint8);np.fill_diagonal(K,1);fitting=K.copy()
for i in U:fitting[i,V]^=1
assert np.all(np.diag(fitting)==1) and np.all(fitting[K==0]==0)
foreign=fitting.sum(axis=1)-1
visits=(foreign>52).astype(np.int64)+(foreign>36).astype(np.int64)
assert int(visits.sum())==205
changed=int(np.count_nonzero(fitting!=K));assert changed==120

def bitrank(matrix):
 piv={}
 for row in matrix:
  v=sum(int(x)<<i for i,x in enumerate(row))
  while v:
   i=v.bit_length()-1
   if i in piv:v^=piv[i]
   else:piv[i]=v;break
 return len(piv)
assert bitrank(K)==9 and bitrank(fitting)==10
required=[]
for q,e in [(8,0),(8,1),(8,3),(9,0),(9,11)]:
 savings=111-q-e;directions=(savings+16)//17
 required.append({'q':q,'extra_arrivals':e,'required_savings':savings,'required_projective_quotient_directions':directions})
assert [r['required_projective_quotient_directions'] for r in required]==[7,6,6,6,6]
field_controls=[]
for order in [2,4]:
 directions=order+1;visits_lower=222-17*directions
 assert visits_lower>122 and visits_lower>131
 field_controls.append({'field_order':order,'maximum_directions_in_two_dimensional_quotient':directions,'minimum_required_visits':visits_lower,'q8_max_with_three_extras':122,'q9_max_with_eleven_extras':131})
# Existence is a genuine negative control for any proposed bound16.
assert 222-int(visits.sum())>16
out={'status':'PASS_EXACT_SOURCE_CENSUS_AND_SCALAR_QUOTIENT_SAVING_BOUND',
 'source_sha256':hashlib.sha256(blob).hexdigest(),
 'foreign_support_histogram':hist,'generic_parameter_cases':len(envelope),
 'generic_cases_requiring_refinement':critical,
 'independent_triple_count':independent,'rank3_flat_count':len(flats),
 'rank3_five_six_cases':len(rows),'rank3_maximum_eligible_gain':max3,
 'rank3_maximizers':[row for row in rows if row['eligible_count']==max3],
 'orthogonal4_count':count4,'orthogonal4_max_gain_bound':best4,
 'orthogonal4_maximizers':four,
 'sharp_fitting_witness':{'V':V,'U':U,'rank':bitrank(fitting),'changed_entries':changed,
 'foreign_weight_histogram':dict(sorted(collections.Counter(map(int,foreign)).items())),
 'required_visits_lower_bound':int(visits.sum()),'saved_visits':17,'physical_source_supplied':False},
 'direction_requirements':required,'two_extra_dimension_exclusions':field_controls,
 'negative_controls':{'claimed_bound16_disproved_by_explicit_fitting':True,
 'rank12_for_arbitrary_fittings_not_claimed':True,'extension_fields_larger_than4_not_excluded_by_dimension_count':True},
 'proof_scope':'Scalar all-characteristic-two-field saving17 per projective quotient direction; source-specific exhaustive real geometry; no-Y-feedback arrival interface. Dimension>=3 outside canonical code only over F2 and F4. Not arbitrary fitting-rank>=12 or a complete source.'}
args.output.mkdir(parents=True,exist_ok=True)
(args.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','independent_triple_count','rank3_flat_count','rank3_maximum_eligible_gain','orthogonal4_count','orthogonal4_max_gain_bound','sharp_fitting_witness','direction_requirements','two_extra_dimension_exclusions']},indent=2))
