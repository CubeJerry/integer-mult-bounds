from pathlib import Path
from fractions import Fraction as F
import argparse,gzip,hashlib,json
if not __debug__:raise RuntimeError('Run without -O')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rank(rows):
 b={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k in b:v^=b[k]
   else:b[k]=v;break
 return len(b)
def main(a):
 native=a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
 assert sha(native)=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(native.read_bytes()))
 target=a.repo/'research/moonshot-005-program/results/bit-fifteen-class-target/author/RESULT.json'
 assert sha(target)=='7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117';groups=json.loads(target.read_text())['groups'];assert groups[0]==list(range(8))
 roots=[]
 for i in range(111):
  r=tuple(F(x) for x in s['frames'][str(s['start'][i])]['B'][0]);n=sum(x*x for x in r);assert n in [1,4];roots.append(tuple(x*(2 if n==1 else 1) for x in r))
 dot=lambda r,t:sum(x*y for x,y in zip(r,t));supp=lambda r:sum(1<<j for j,x in enumerate(r) if x)
 K=[sum(1<<j for j in range(111) if i==j or dot(roots[i],roots[j])==0) for i in range(111)]
 U=[sum(1<<i for i in g) for g in groups];full=[c for c,g in enumerate(groups) if len(g)==8 and c!=0];short=[c for c,g in enumerate(groups) if len(g)<8];assert len(full)==8 and len(short)==6
 halves={}
 for c in full:
  halves[c]=[]
  for bit in [0,1]:
   selected=[i for i in groups[c] if ((K[0]>>i)&1)^bit];assert len(selected)==4
   supports={supp(roots[i]) for i in selected};assert len(supports)==1
   m=supports.pop();assert m.bit_count()==4
   assert all(dot(roots[i],roots[j])==(4 if i==j else 0) for i in selected for j in selected)
   halves[c].append(m)
  assert halves[c][0]^halves[c][1]==255
 for c in short:
  masks={supp(roots[i]) for i in groups[c]};assert len(masks)==2
  x,y=sorted(masks);assert x^y==255 and x.bit_count()==y.bit_count()==4
 proper=[];full_count=0;negative=0
 for bits in range(256):
  union=0;u=U[0]
  for j,c in enumerate(full):
   bit=(bits>>j)&1;union|=halves[c][bit]
   if bit:u^=U[c]
  if union==255:full_count+=1;continue
  assert union.bit_count()==7;j=((~union)&255).bit_length()-1
  for c in short:
   outside=[i for i in groups[c] if roots[i][j]];assert outside
   vals={(K[0]>>i)&1 for i in outside};assert len(vals)==1
   if vals.pop():u^=U[c]
  w=K[0]^u;assert w==K[j]^U[0] and all(not roots[i][j] for i in range(111) if (w>>i)&1)
  facet=s['frames'][str(s['final'][111+j])];assert facet['dim']==7 and all(F(row[j])==0 for row in facet['B'])
  for c in short:
   wrong=w^U[c];assert any(roots[i][j] for i in range(111) if (wrong>>i)&1);negative+=1
  proper.append({'full_class_choices':bits,'missing_coordinate':j,'row_hex':hex(w),'support_size':w.bit_count(),'actual_facet':s['final'][111+j],'support_real_rank':7})
 assert full_count==248 and len(proper)==8 and sorted(x['missing_coordinate'] for x in proper)==list(range(8))
 T=[U[c] for c in short];L=[K[j]^U[0] for j in range(8)]
 assert rank(U+[K[0]])==16 and rank(T)==6 and rank(L)==4 and rank(T+L)==10 and rank(U+T+L)==16
 out={'status':'PASS_EXACT_W0_PROPER_LOCALIZATION','source_sha256':sha(native),'target_result_sha256':sha(target),'full_noncoordinate_classes':full,'short_classes':short,'full_patterns':256,'patterns_spanning_Hub':248,'proper_nonclass_words':proper,'all65536_W0_words_covered_by_structural_cases':True,'local_span_rank':10,'U_intersection_local_span_rank':9,'W0_mod_all_proper_local_words_dimension':6,'required_target_quotient_rank':6,'negative_wrong_short_bit_cases':negative,'uncanceled_coordinate_class_spans_Hub':True,'scope':'Scalar F2 coefficient support only. Exactly eight nonclass W0 words have proper real support, at coordinate facets. Local-span quotient screen6 does not supply local values, physical q8 source or costs.'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','full_patterns','patterns_spanning_Hub','local_span_rank','W0_mod_all_proper_local_words_dimension','negative_wrong_short_bit_cases']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
