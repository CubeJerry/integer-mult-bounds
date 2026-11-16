from pathlib import Path
import json,itertools
ROOT=Path('/workspace/scratch/6e036830f982')
D=json.loads((ROOT/'work-c/private-bank-envelope/output/RESULT.json').read_text())
B=[int(x,16)for x in D['reconstructed_common_bank_rows_hex']]+[1<<j for g in D['private_groups']for j in g]
E=B+[1<<i for i in D['all_six_bank_case']['feedback_closure']]
R=json.loads((ROOT/'programme/research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_text())['native_roots']
K=[(1<<i)^sum(1<<j for j in range(111)if sum(a*b for a,b in zip(R[i],R[j]))==0)for i in range(111)]
UU=[[int(x,16)for x in g]for g in D['actual_remaining_filter_rows_hex']]
def basis(rows):
 d={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in d:x^=d[j]
   else:d[j]=x;break
 return d
def rem(b,x):
 for j in sorted(b,reverse=True):
  if x>>j&1:x^=b[j]
 return x
def solver(rows):
 piv={};kernel=[]
 for i,x in enumerate(rows):
  co=1<<i
  while x:
   j=x.bit_length()-1
   if j in piv:y,z=piv[j];x^=y;co^=z
   else:piv[j]=(x,co);break
  if not x:kernel.append(co)
 def solve(x):
  co=0
  while x:
   j=x.bit_length()-1
   if j not in piv:return None
   y,z=piv[j];x^=y;co^=z
  return co
 return solve,kernel
def xor_select(rows,mask):
 out=0
 for i,x in enumerate(rows):
  if mask>>i&1:out^=x
 return out
outs=[]
for model,BB in [('rank80',B),('rank88_feedback',E)]:
 bb=basis(BB);U=[];selected=[];offsets=[0]
 for rows in UU:
  inds=[];vv=[]
  for i,r in enumerate(rows):
   x=rem(bb,r)
   if rem(basis(vv),x):vv.append(x);inds.append(i)
  U.append(vv);selected.append(inds);offsets.append(offsets[-1]+len(vv))
 KK=[];kindices=[]
 for i,k in enumerate(K):
  r=rem(bb,k)
  if rem(basis(KK),r):KK.append(r);kindices.append(i)
 solve,ker=solver(sum(U,[]));particular=[solve(k)for k in KK];assert all(z is not None for z in particular)
 profiles={};best=None;bestcases=[]
 for coeffs in itertools.product(range(1<<len(ker)),repeat=len(KK)):
  lifted=[z^xor_select(ker,co)for z,co in zip(particular,coeffs)]
  blocks=[[(z>>offsets[i])&((1<<len(U[i]))-1)for z in lifted]for i in range(4)]
  ranks=tuple(len(basis(block))for block in blocks);cost=sum(ranks);profiles[ranks]=profiles.get(ranks,0)+1
  if best is None or cost<best:best=cost;bestcases=[]
  if cost==best:bestcases.append({'kernel_coefficients':coeffs,'lifts_hex':[hex(z)for z in lifted],'bank_ranks':ranks,'messages_basis_masks':[[hex(v)for v in basis(block).values()]for block in blocks]})
 out={'model':model,'side_rank':len(bb),'bank_dimensions':list(map(len,U)),'bank_original_row_indices':selected,'bank_offsets':offsets,'canonical_quotient_dimension':len(KK),'canonical_original_indices':kindices,'canonical_quotient_rows_hex':[hex(k)for k in KK],'joint_bank_dimension':len(basis(sum(U,[]))),'kernel_basis_hex':[hex(z)for z in ker],'particular_lifts_hex':[hex(z)for z in particular],'sections_examined':2**(len(KK)*len(ker)),'minimum_total_messages_binary':best,'best_sections':bestcases,'profile_census':{str(k):v for k,v in profiles.items()}}
 outs.append(out);print(model,'dims',out['bank_dimensions'],'K',len(KK),'ker',len(ker),'min',best,'profiles',list(profiles),'best',bestcases[:1],flush=True)
Path(__file__).with_name('PROBE.json').write_text(json.dumps(outs,indent=2)+'\n')
