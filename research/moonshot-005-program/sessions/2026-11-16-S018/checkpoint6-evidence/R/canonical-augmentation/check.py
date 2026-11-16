#!/usr/bin/env python3
"""Independent canonical source-span and actual eight-receiver transcript audit."""
import argparse,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from review_leaf_capacity import chart_basis,echelon
from price import moment,encode,invoice
raw=a.word.read_bytes();w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];stats=independent_replay(w);v,at=trace(w)[0][w['carrier_interface_before_operation']];C={n:chart_basis(c)for n,c in w['charts'].items()};S=set(w['targets']);U=set(range(111))-S;assert len(S)==48 and len(U)==63;sm=sum(1<<i for i in S)
local=[sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)];canon=[((1<<i)^local[i])&~sm for i in range(111)];ids=[4,74,78,15,35,13,1,2,0]
def basis(rows):
 b={}
 for j,z in enumerate(rows):
  cf=1<<j
  while z:
   k=z.bit_length()-1
   if k in b:r,c=b[k];z^=r;cf^=c
   else:b[k]=(z,cf);break
 return b
def coef(rows,z):
 b=basis(rows);cf=0
 while z:
  k=z.bit_length()-1
  assert k in b,('missing canonical row',hex(z));r,c=b[k];z^=r;cf^=c
 return cf
originals={f'{c}{i}'for c in 'XY'for i in range(111)};owners=set(v)-originals
chosen=[]
for i in ids:
 candidates=sorted(n for n in owners if v[n]==canon[i]and at[n]=='M1');assert candidates,('missing actual M1 canonical mode',i);chosen.append(candidates[0])
rows=[v[n]for n in chosen];assert len(basis(rows))==len(basis(canon))==9
coefficients=[]
for i,r in enumerate(canon):
 cf=coef(rows,r);z=0
 for j,x in enumerate(rows):
  if cf>>j&1:z^=x
 assert z==r;coefficients.append({'receiver':i,'selected_mode_indices':[j for j in range(9)if cf>>j&1]})
groups=[v[n]for n in owners if n.startswith('ASC_GROUP_')];assert len(groups)==7 and len(basis(groups))==7 and len(basis(groups+canon))==13
for i in U:
 assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
 assert any(v[n]==1<<i and at[n]==f'L{i}'for n in owners)
for i in S:assert v[f'X{i}']==1<<i and at[f'X{i}']==f'L{i}'
J=[5,35,90,93,96,97,109,110];assert set(J)<=U
assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in J for j in J)
mask=sum(1<<i for i in J);access=[];memo={}
def sub(x,y):
 key=(x,y)
 if key not in memo:memo[key]=len(echelon(C[x]+C[y])[0])==len(C[y])
 return memo[key]
for i in J:
 for n in sorted(v):
  if v[n]&mask and sub(at[n],f'F{i}'):access.append({'receiver':i,'field':n})
assert not access
cut=w['carrier_interface_before_operation'];suffix=w['operations'][cut:]
assert all(op[0]=='CLEAR'or(op[0]=='MOVE'and op[1]in originals)for op in suffix)
counts={n:0 for n in originals}
for op in suffix:
 if op[0]=='MOVE':counts[op[1]]+=1
assert max(counts.values())<=1
q=moment(stats['movement_profile']);limit=invoice(stats['movement_profile'])['limiting_allowance'];from fractions import Fraction
allow=(Fraction(limit['lower_fraction']),Fraction(limit['upper_fraction']))
floor=(q[0]+8,q[1]+8);assert floor[0]>allow[1]
direct=moment({7:222,1:48,3:9});directfloor=(direct[0]+8,direct[1]+8);assert directfloor[0]>allow[1]
report={'status':'PASS_ROOT_CANONICAL9_SOURCE_AND_EIGHT_DESCENT_GATE','word_sha256':hashlib.sha256(raw).hexdigest(),'native_source_sha256':w['source_sha256'],'actual_native_all222':stats,'cut':cut,'selected_actual_M1_fields':dict(zip(ids,chosen)),'canonical_rows_mod_actual_known48_rank':9,'group_rank':7,'group_plus_canonical_rank':13,'canonical_extension_dimension_over_group_space':6,'all111_canonical_row_coefficients':coefficients,'actual_unknown_native_caches':63,'raw_known_originals_native':48,'actual_J8_no_access_witness':J,'all_initial_field_access_edges':access,'whole_word_moment':encode(q),'frozen_cut_completion_movement_floor':encode(floor),'excess_over_allowance':encode((floor[0]-allow[1],floor[1]-allow[0])),'direct_source_class_without_group_detours':{'profile':{'7':222,'1':48,'3':9},'source_moment':encode(direct),'with_eight_descents':encode(directfloor),'excess_over_allowance':encode((directfloor[0]-allow[1],directfloor[1]-allow[0]))},'scope':'Full canonical quotient source at M1 is actual; free global distribution plus geometric raw side information yields ideal all111 equations, not physical decoder chains. Exactly6 extra dimensions is only for containing the prescribed canonical envelope over the7-group space. The initial-chart theorem forces8 future owned descents at this fixed cut. The direct-source comparison requires48 actual unit ground acquisitions,9 full Hub-to-M1 rank3 deliveries and the same J8 zero-access cut premise; no universal supplier lower bound.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status']);print('actual floor',encode(floor)['lower'],'direct floor',encode(directfloor)['lower'],'direct excess',report['direct_source_class_without_group_detours']['excess_over_allowance']['lower'])
