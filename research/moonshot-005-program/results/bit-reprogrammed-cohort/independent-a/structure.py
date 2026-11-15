import json,argparse,collections
from pathlib import Path
from check import rank,basis,contains,dimcap,xor
p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);a=p.parse_args();word=json.loads((a.package/'output/WORD.json').read_text());W=[int(x,16) for x in word['W_rows_hex']];h=int(word['W_pivot_h_hex'],16);runrows=[];expected=collections.Counter();sources=[];form_cost=0
for c in word['cohorts']:
 ss=c['sources'];sources+=ss;mat=c['local_matrix_rows'];piv=[c['carrier']]+c['donors'];assert len(mat)==len(ss) and rank(mat)==len(ss)
 assert len(piv)==len(c['runs'])==len(c['run_rows_hex'])
 for t,label in enumerate(ss):
  if label not in piv:assert mat[t]==1<<t
 for label,encoded in zip(piv,c['run_rows_hex']):
  p=ss.index(label);v=mat[p];assert v>>p&1
  assert all(not(v>>ss.index(other)&1) for other in piv if other!=label)
  z=sum(1<<ss[j] for j in range(len(ss)) if v>>j&1);assert z==int(encoded,16);runrows.append(z);form_cost+=2*(v.bit_count()-1)
 for i,j in c['restore_add_indices']:
  assert ss[j] in piv and ss[i] not in piv and mat[j]>>i&1;expected[(f'X{ss[i]}',f'X{ss[j]}')]+=2
assert sorted(sources)==list(range(111)) and len(runrows)==40 and rank(runrows)==40 and form_cost==142
actual=collections.Counter(tuple(op[1:]) for op in word['operations'] if op[0]=='ADD' and op[1].startswith('X') and op[2].startswith('X'));assert actual==expected and sum(actual.values())==142
raw=[v for n,(c,v) in word['expected'].items() if n.startswith('C')];assert rank(raw+runrows)==40
b0=[int(x,16) for x in word['reprogramming']['h0_W_basis_hex']];coeffs=word['reprogramming']['h0_target_coefficients'];U=[xor(b0[j] for j in range(7) if c>>j&1) for c in coeffs];assert rank(b0)==7 and rank(U)==5
assert [hex(x) for x in U]==word['reprogramming']['h0_target_rows_hex'];plane=word['reprogramming']['dual_plane'];assert rank(plane)==2 and all((a&c).bit_count()%2==0 for a in plane for c in coeffs)
W0=[W[i] for i in range(111) if not(h>>i&1)];W1=[W[i] for i in range(111) if h>>i&1];assert rank(W0)==7 and rank(W1)==8 and rank(b0+W0)==7
assert dimcap(raw,W0)==5 and dimcap(raw,W1)==4 and all(contains(raw,u) for u in U)
for c in word['cohorts']:
 if c['h_class']==0:
  mask=sum(1<<i for i in c['sources']);rr=[int(z,16) for z in c['run_rows_hex']];assert rank([u&mask for u in U])<=len(rr);assert all(contains(rr,u&mask) for u in U)
classes=collections.Counter()
for op in word['operations']:
 if op[0]!='ADD':continue
 a,b=op[1:]
 if a.startswith('X') and b.startswith('R'):kind='initial_point_captures'
 elif a.startswith('X') and b.startswith('X'):kind='cohort_formation_restoration'
 elif a.startswith('X') and b.startswith('C'):kind='source_cache_deposits'
 elif a.startswith('X') and b.startswith('P'):kind='actual_Hub_seed_reads'
 elif a.startswith('C') and b.startswith('P'):kind='packet_cache_reads'
 elif a.startswith('C') and b=='Y0':kind='Y0_local_corrections'
 else:kind='actual_mask_feedback'
 classes[kind]+=1
assert dict(classes)=={'initial_point_captures':111,'cohort_formation_restoration':142,'source_cache_deposits':112,'actual_Hub_seed_reads':349,'packet_cache_reads':80,'Y0_local_corrections':7,'actual_mask_feedback':4}
result={'status':'PASS_INDEPENDENT_SYSTEMATIC_SOURCE_STRUCTURE','cohort_count':len(word['cohorts']),'actual_run_count':40,'actual_run_rank':40,'cache_incidence_rank':40,'systematic_transform_and_inverse_ADDs':142,'actual_D_W0_intersection':5,'actual_D_W1_intersection':4,'ADD_decomposition':dict(classes)};(Path(__file__).parent/'output/STRUCTURE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
