"""Independent high-pivot cut dimensions, dual identities and message decoding."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--envelope',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();E=json.loads(a.envelope.read_text());C=json.loads(a.certificate.read_text());w=json.loads(a.word.read_text());assert sha(a.word)==C['source_word_sha256'];assert sha(a.envelope)==C['envelope_result_sha256'];R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];assert sha(a.repo/w['source_path'])==C['native_source_sha256']
def basis(rows):
 b={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return b
rank=lambda rows:len(basis(rows))
def combo(rows,mask):
 assert mask>>len(rows)==0
 x=0
 for i,r in enumerate(rows):
  if(mask>>i)&1:x^=r
 return x
B=[int(x,16)for x in E['reconstructed_common_bank_rows_hex']]+[1<<j for g in E['private_groups']for j in g];closed=B+[1<<i for i in E['all_six_bank_case']['feedback_closure']]
K=[(1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)]
U=[[int(x,16)for x in rows]for rows in E['actual_remaining_filter_rows_hex']];assert U==[[int(x,16)for x in rows]for rows in C['bank_rows_hex']];assert rank(K)==9
out=[];duals=0;negative=0
for cert,S,want in zip(C['cases'],[B,closed],[[3,3,3,4],[2,2,2,3]]):
 assert rank(S)==cert['side_rank'];assert S==[int(x,16)for x in cert['side_rows_hex']];assert rank(S+K)-rank(S)==cert['canonical_quotient_dimension'];bounds=[]
 for j,d in enumerate(cert['cut_certificates']):
  T=S+[x for i,rows in enumerate(U)if i!=j for x in rows];delta=rank(T+K)-rank(T);bounds.append(delta);assert delta==want[j]==d['conditional_C9_dimension'];W=[K[i]for i in d['separated_canonical_indices']];ls=[int(x,16)for x in d['dual_hex']];assert len(W)==len(ls)==delta
  for k,l in enumerate(ls):
   assert all((x&l).bit_count()%2==0 for x in T)
   assert [(x&l).bit_count()%2 for x in W]==[int(i==k)for i in range(delta)];duals+=1
 M=[]
 for rows,masks,values in zip(U,cert['bank_message_original_row_masks'],cert['bank_messages_hex']):
  got=[combo(rows,int(x,16))for x in masks];assert got==[int(x,16)for x in values];M+=got
 assert len(M)==sum(want);assert rank(S+M+K)==rank(S+M)
 for k,c in zip(K,cert['all111_canonical_witnesses_hex']):assert combo(S+M,int(c,16))==k
 for j in range(len(M)):
  shorter=S+M[:j]+M[j+1:];assert rank(shorter+K)>rank(shorter);negative+=1
 out.append({'side_rank':rank(S),'canonical_gap':rank(S+K)-rank(S),'bank_cut_dimensions':bounds,'minimum_messages':len(M),'all111_decoders_checked':True})
r={'status':'PASS_INDEPENDENT_BANK_CUT_AND_NONLINEAR_CAPACITY_PREREQUISITES','certificate_sha256':sha(a.certificate),'envelope_sha256':sha(a.envelope),'cases':out,'independent_cut_dual_checks':duals,'single_message_deletion_controls':negative,'scope':'Independent algebra/certificate review on separately source-authenticated rows. Written finite-field counting proof extends fixed-side-information bank-separated lower bound to nonlinear encoders. No new feedback, routes, or kappa.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
