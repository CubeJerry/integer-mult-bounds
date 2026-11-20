#!/usr/bin/env python3
"""Independent owner binding, polynomial lift, exact transvection replay and bill."""
from pathlib import Path
from array import array
from hashlib import sha256
import gzip,json,sys,time
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[3]
PACKAGE=HERE.parent
EARLY=PACKAGE.parent/'output/EARLY.json.gz'
ROUTES=BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
HRECEIPT=PACKAGE.parent/'root-physical/output/RESULT.json'
claimed=json.loads((PACKAGE/'author/output/RESULT.json').read_text())
early=json.loads(gzip.decompress(EARLY.read_bytes()))
owner_h={j:{}for j in [0,45,61,62,100]}
for line in gzip.decompress(ROUTES.read_bytes()).splitlines():
 phase,j,x,h,d,k,source,target=json.loads(line)
 if phase=='X'and j in owner_h:
  assert j==source and x not in owner_h[j]
  owner_h[j][x]=h
# Polynomial long division; no call to an author field-arithmetic routine.
def remainder(poly,mod):
 while poly.bit_length()>=mod.bit_length():poly^=mod<<(poly.bit_length()-mod.bit_length())
 return poly
assert all(remainder(67,d) for degree in range(1,4) for d in range(1<<degree,1<<(degree+1)))
monomial=[[remainder(a<<k,67)for k in range(6)]for a in range(64)]
pattern=[[sum(((monomial[a][k]>>b)&1)<<k for k in range(6))for b in range(6)]for a in range(64)]
receipts=[];started=time.time()
for j in owner_h:
 labels=early['full'][str(j)]['row_owners'];matrix=early['full'][str(j)]['matrix']
 assert len(labels)==len(matrix)==480 and set(owner_h[j])==set(range(480))
 by_owner={}
 for label,row in zip(labels,matrix):
  h,x=label
  assert x not in by_owner and owner_h[j][x]==h and len(row)==480 and all(isinstance(v,int)and 0<=v<64 for v in row)
  by_owner[x]=row
 assert set(by_owner)==set(range(480))
 ordered=[by_owner[x]for x in range(480)]
 digest_matrix=sha256(bytes(v for row in ordered for v in row)).hexdigest()
 binary=[]
 for row in ordered:
  acc=[0]*6
  for y,a in enumerate(row):
   for b in range(6):acc[b]|=pattern[a][b]<<(6*y)
  binary.extend(acc)
 n=2880;work=list(binary);operations=array('H');swaps=0
 for column in range(n):
  pivot=next(r for r in range(column,n)if(work[r]>>column)&1)
  if pivot!=column:
   swaps+=1
   for target,source in [(column,pivot),(pivot,column),(column,pivot)]:
    assert target!=source
    work[target]^=work[source];operations.extend([target,source])
  to_clear=[r for r,value in enumerate(work)if r!=column and(value>>column)&1]
  for r in to_clear:work[r]^=work[column];operations.extend([r,column])
 identity=[1<<r for r in range(n)];assert work==identity
 replay=identity.copy()
 for i in reversed(range(0,len(operations),2)):
  target,source=operations[i:i+2];assert target!=source and target<n and source<n;replay[target]^=replay[source]
 assert replay==binary
 for i in range(0,len(operations),2):replay[operations[i]]^=replay[operations[i+1]]
 assert replay==identity
 if sys.byteorder!='little':operations.byteswap()
 word_sha=sha256(operations.tobytes()).hexdigest();count=len(operations)//2
 expected=next(r for r in claimed['sources']if r['donor']==j)
 assert digest_matrix==expected['field_matrix_row_major_sha256']
 assert word_sha==expected['binary_elimination_word_u16le_sha256']
 assert count==expected['ADDs_per_direction']and swaps==expected['three_ADD_swaps']
 receipts.append({'donor':j,'field_matrix_sha256':digest_matrix,'elimination_word_sha256':word_sha,'ADDs_per_direction':count,'paid_three_ADD_swaps':swaps,'all_bits_forward_inverse_replayed':True})
 print('INDEPENDENT_SOURCE_PASS',j,count,swaps,round(time.time()-started,2),flush=True)
h=json.loads(HRECEIPT.read_text());assert h['pair_ADD_total']==1509520 and h['paid_field_exports']==16
source_sum=16*sum(r['ADDs_per_direction']for r in receipts)
assert source_sum==191000864 and source_sum+h['pair_ADD_total']==192510384
out={'status':'PASS_INDEPENDENT_ACTUAL_SOURCE_COMPILATION','field_polynomial':67,'irreducibility_checked_by_all_degree_at_most_three_divisors':True,'actual_owner_row_permutation_compiled':True,'sources':receipts,'source_forward_inverse_ADD_total':source_sum,'known_source_and_two_H_ADD_total':source_sum+h['pair_ADD_total'],'H_exports':16,'H_export_gap':6,'binary_INIT_MOVE_CLEAR_each':96,'global_transport_precondition_not_proved':True,'gross_bill_only':True,'new_kappa':False,'input_sha256':{str(p.relative_to(BASE)):sha256(p.read_bytes()).hexdigest()for p in [EARLY,ROUTES,HRECEIPT,PACKAGE/'PROOF.md',PACKAGE/'author/check.py',PACKAGE/'author/output/RESULT.json']}}
(HERE/'output').mkdir(exist_ok=True);(HERE/'output/RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],source_sum,source_sum+h['pair_ADD_total'],flush=True)
