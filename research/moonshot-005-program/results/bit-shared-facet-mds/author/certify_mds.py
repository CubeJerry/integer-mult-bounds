import json,hashlib,itertools
from pathlib import Path
from field import mul,power,invert,binary_matrix,restore_adds
p=Path(__file__).parent;g=json.loads((p/'GEOMETRY.json').read_text());d=5;mod=37
assert all(mul(a,power(a,30,d,mod),d,mod)==1 for a in range(1,32))
D=[[power(t,r,d,mod)for t in range(28)]for r in range(16)];row=g['rows'][3];masks=[int(z['native_mask_hex'],16)for z in row['atlas']];U=0
for mask in masks:U|=mask
foreign=[j for j in range(111)if U>>j&1];sources=[];source_adds=0
for j in foreign:
 ids=[t for t,m in enumerate(masks)if m>>j&1];assert len(ids)==16;A=[[D[r][t]for t in ids]for r in range(16)];B=invert(A,d,mod)
 for r in range(16):
  for c in range(16):
   z=0
   for k in range(16):z^=mul(A[r][k],B[k][c],d,mod)
   assert z==int(r==c)
 ops=restore_adds(binary_matrix(B,d,mod));source_adds+=2*len(ops);sources.append({'source_role':j,'selected_charts':ids,'inverse_matrix':B,'binary_inverse_add_count':len(ops),'binary_inverse_add_list_sha256':hashlib.sha256(json.dumps(ops,separators=(',',':')).encode()).hexdigest()})
anchor=invert([[D[r][c]for c in range(16)]for r in range(16)],d,mod);anchor_adds=2*len(restore_adds(binary_matrix(anchor,d,mod)));decode_adds=sum(mul(D[r][t],1<<src,d,mod).bit_count()for t in range(16,28)for r in range(16)for src in range(5));multiplicities=[sum(t in s['selected_charts']for s in sources)for t in range(28)];aggregate_adds=2*5*sum(m-1 for m in multiplicities[16:]);anchor_adds_direct=5*sum(multiplicities[:16]);f=len(foreign);profile={1:5*(2*28-16),2:80*f-60,5:80*f,6:80,7:80*(221-f)}
repeated=[]
for r in g['rows']:
 ms=[int(a['native_mask_hex'],16)for a in r['atlas']];U=0
 for m in ms:U|=m
 hit=None
 for c in range(28):
  pairs=[(a,b)for a,b in itertools.combinations(range(28),2)if c not in[a,b]and(ms[a]|ms[b]|ms[c])==U]
  for A,B in itertools.combinations(pairs,2):
   if ms[A[0]]|ms[A[1]]|ms[B[0]]|ms[B[1]]==U:hit=[*A,*B,c];break
  if hit:break
 if hit:repeated.append({'receiver':r['receiver'],'chart_indices':hit,'colors':[1,1,2,2,3]})
r={'status':'PASS_GF32_MDS_AND_ONE_RECEIVER_ENCODING_CERTIFICATE','geometry_sha256':hashlib.sha256((p/'GEOMETRY.json').read_bytes()).hexdigest(),'field_degree':5,'field_modulus_binary':mod,'all31_nonzero_elements_have_verified_inverse':True,'b':16,'n':28,'decoder_matrix':D,'MDS_proof':'Any16 distinct evaluation nodes have nonzero Vandermonde determinant; nodes0..27 are distinct in GF32.','receiver':3,'source_count':len(foreign),'source_certificates':sources,'physical_binary_copies':80,'parametric_original_pivot_compilation_counts':{'INIT':0,'CLEAR':0,'ADD':source_adds+anchor_adds+decode_adds+aggregate_adds+anchor_adds_direct,'MOVE':sum(profile.values()),'source_encoding_and_inverse_ADD':source_adds,'aggregation_and_inverse_ADD':aggregate_adds,'Y_anchor_pre_and_postencoding_ADD':anchor_adds,'nonanchor_decoder_ADD':decode_adds,'direct_anchor_source_ADD':anchor_adds_direct,'chart_source_multiplicities':multiplicities,'movement_profile':profile},'scope':'Exact synthesis counts for the proved generic direct-Y-anchor/nonanchor-original-pivot construction. No huge80-copy literal word is emitted or claimed independently replayed.','binary_five_distinct_atlas_solutions':g['binary_five_covered'],'binary_five_repeated_chart_witnesses':repeated,'new_complete_kappa':False};(p/'MDS-CERTIFICATE.json').write_text(json.dumps(r,indent=2)+'\n');print('GF32 PASS',r['parametric_original_pivot_compilation_counts'],'binary5 repeat',len(repeated),flush=True)
