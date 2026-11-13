"""Exact primary-source canonical code and punctured row distances."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 s=json.loads(gzip.decompress(raw));fr={int(k):v for k,v in s['frames'].items()};r=[[F(x) for x in fr[s['start'][i]]['B'][0]] for i in range(111)];v=[]
 for rr in r:
  n=dot(rr,rr);assert n in(1,4);vv=[x*(2 if n==1 else 1) for x in rr];assert all(x.denominator==1 for x in vv);v.append(list(map(int,vv)))
 K=[]
 for i in range(111):
  row=0
  for j in range(111):
   z=dot(v[i],v[j]);assert z%2==0 and bool(i==j or z==0)==bool(1^(z//2%2));row|=int(i==j or z==0)<<j
  K.append(row)
 basis={};selected=[];rows=[]
 for i,old in enumerate(K):
  z=old
  while z:
   q=z.bit_length()-1
   if q not in basis:basis[q]=z;selected.append(i);rows.append(old);break
   z^=basis[q]
 assert len(rows)==9
 words=[]
 for m in range(1,512):
  z=0
  for q in range(9):
   if m>>q&1:z^=rows[q]
  words.append(z)
 assert len(set(words))==511 and min(z.bit_count() for z in words)==48
 cert=[]
 for i in range(111):
  candidates=[((z&~K[i]).bit_count(),m,z) for m,z in enumerate(words,1) if not(z>>i&1)];assert len(candidates)==255
  w,m,z=min(candidates);assert w>=18;cert.append({'role':i,'minimum_noncontact_weight_with_diagonal_zero':w,'attaining_basis_mask':m,'attaining_word_hex':hex(z)})
 assert min(c['minimum_noncontact_weight_with_diagonal_zero'] for c in cert)==18
 assert min((z&~K[0]).bit_count() for z in words)==0 and K[0] in words
 out={'status':'PASS_EXACT_PUNCTURED_CODE_DISTANCE18','source_sha256':SP,'canonical_code_dimension':9,'binary_basis_source_roles':selected,'binary_basis_rows_hex':list(map(hex,rows)),'nonzero_words_checked':511,'minimum_nonzero_code_weight':48,'per_receiver':cert,'minimum_diagonal_zero_noncontact_weight':18,'restriction_distance_histogram':dict(sorted(collections.Counter(c['minimum_noncontact_weight_with_diagonal_zero'] for c in cert).items())),'negative_controls':{'removing_diagonal_zero_condition_gives_noncontact_weight0':True},'scope':'Finite source code facts only; arbitrary-field/block/timing theorem is PROOF.md. Canonical/gauge row code retained; singular-Schur codes and mutable outside-code payloads not covered.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CODE-CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','canonical_code_dimension','minimum_nonzero_code_weight','minimum_diagonal_zero_noncontact_weight','restriction_distance_histogram']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
