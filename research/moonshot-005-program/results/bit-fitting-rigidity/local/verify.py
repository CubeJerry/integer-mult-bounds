"""Exact canonical-fitting Jacobian and gauge-kernel certificate; no SAT."""
import argparse,gzip,hashlib,json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAME=[0,16,17,32,36,38,67,71]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def basis(rows):
 b={};chosen=[]
 for n,v in enumerate(rows):
  while v:
   j=v.bit_length()-1
   if j not in b:b[j]=v;chosen.append(n);break
   v^=b[j]
 return b,chosen
def main(a):
 from fractions import Fraction as F
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 s=json.loads(gzip.decompress(raw));charts={int(k):v for k,v in s['frames'].items()};r=[[F(x) for x in charts[s['start'][i]]['B'][0]] for i in range(111)]
 v=[]
 for rr in r:
  n=dot(rr,rr);assert n in (1,4);vv=[x*(2 if n==1 else 1) for x in rr];assert all(x.denominator==1 for x in vv);v.append(list(map(int,vv)))
 assert all(dot(x,x)==4 for x in v)
 K=[]
 for i in range(111):
  row=0
  for j in range(111):
   z=dot(v[i],v[j]);assert z%2==0;row|=(1^(z//2%2))<<j
  K.append(row)
 def bit(i,j):return K[i]>>j&1
 assert all(bit(i,j)==int(i==j) for i in FRAME for j in FRAME)
 at={i:j for j,i in enumerate(FRAME)};bb=[sum(bit(i,j)<<k for k,j in enumerate(FRAME)) for i in range(111)]
 p=next(i for i in range(111) if i not in at and bb[i].bit_count()%2==0)
 x=[bb[i]|((bit(i,p)^((bb[i]&bb[p]).bit_count()%2))<<8) for i in range(111)]
 assert p==1 and all(((x[i]&x[j]).bit_count()%2)==bit(i,j) for i in range(111) for j in range(111))
 vr={};labels=[]
 for i in range(111):
  if i in at:continue
  for j in range(9):
   if j<8 and not bit(i,FRAME[j]):continue
   for side in (0,1):vr[side,i,j]=len(labels);labels.append((side,i,j))
 def derivative(i,j):
  z=0
  for q in range(9):
   if x[j]>>q&1 and (0,i,q) in vr:z^=1<<vr[0,i,q]
   if x[i]>>q&1 and (1,j,q) in vr:z^=1<<vr[1,j,q]
  return z
 constraints=[(i,j) for i in range(111) for j in range(111) if i==j or not bit(i,j)]
 rows=[derivative(i,j) for i,j in constraints];eb,selected=basis(rows)
 assert len(labels)==1120 and len(rows)==5851 and len(eb)==1009
 pivots=sorted(eb);minor=[sum((rows[i]>>j&1)<<k for k,j in enumerate(pivots)) for i in selected]
 assert len(basis(minor)[0])==1009
 gauges=[]
 for t in range(112):
  z=0
  for n,(side,i,q) in enumerate(labels):
   own=int(t==i);coord=int(t==FRAME[q]) if q<8 else int(t==111)
   if x[i]>>q&1 and own^coord:z|=1<<n
  assert all(not((row&z).bit_count()%2) for row in rows);gauges.append(z)
 gb,gs=basis(gauges);assert len(gb)==111
 total=0
 for z in gauges:total^=z
 assert total==0
 reached={0}
 while True:
  nxt=reached|{j for i in reached for j in range(111) if i!=j and bit(i,j)}
  if nxt==reached:break
  reached=nxt
 assert len(reached)==111
 # A diagonal factor perturbation with a nonzero diagonal derivative violates the fitting equations.
 probe=next(1<<vr[0,i,q] for i in range(111) for q in range(9) if (0,i,q) in vr and x[i]>>q&1)
 assert any((row&probe).bit_count()%2 for row in rows)
 # Ordered noncommuting control over M2(F2[t]/t^3).
 def pmul(x,y):
  z=0
  for q in range(3):
   if x>>q&1:z^=y<<q
  return z&7
 def mmul(a,b):return tuple(pmul(a[i*2],b[j])^pmul(a[i*2+1],b[2+j]) for i in range(2) for j in range(2))
 one=(1,0,0,1);uu=(1,2,0,1);vv=(1,0,2,1)
 assert mmul(uu,uu)==mmul(vv,vv)==one and mmul(uu,vv)!=mmul(vv,uu)
 correct=mmul(mmul(mmul(uu,vv),vv),uu);wrong=mmul(mmul(mmul(vv,uu),vv),uu)
 assert correct==one and wrong!=one
 triangle=next((i,j,k) for i in range(111) for j in range(i+1,111) if bit(i,j) for k in range(j+1,111) if bit(j,k) and bit(k,i))
 out={'status':'PASS_EXACT_CANONICAL_BIT_JACOBIAN_GAUGE_KERNEL','source_sha256':SP,'field':'F2; exact ranks persist under every characteristic-two field extension','identity_frame_roles':FRAME,'canonical_extra_pivot_role':p,'canonical_factor_rows_9bit':x,'factor_variable_count':1120,'constraint_count':5851,'jacobian_rank':1009,'factor_kernel_dimension':111,'gauge_generator_count':112,'gauge_span_rank':111,'single_generator_relation':'All112 vertex/complement generators sum to0; this spans their relation space.','jacobian_nonsingular_minor_constraint_indices':selected,'jacobian_nonsingular_minor_variable_indices':pivots,'independent_gauge_generator_indices':gs,'fitting_matrix_tangent_dimension':110,'contact_graph_connected':True,'negative_controls':{'diagonal_changing_single_factor_perturbation_rejected':True,'noncommuting_vertex_order_control':{'actual_contact_triangle':triangle,'ring':'M2(F2[t]/t^3)','correct_cycle_is_identity':True,'reversed_order_cycle_fails':True,'wrong_cycle_entries_polynomial_bits':wrong}},'scope':'Canonical infinitesimal and nilpotent/formal neighbourhood only. Not global all-V rigidity or a complete correction construction.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','factor_variable_count','constraint_count','jacobian_rank','factor_kernel_dimension','gauge_span_rank','fitting_matrix_tangent_dimension']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
