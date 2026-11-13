"""Independent rational-source BIT fitting and odd-frame review; no author imports."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAMES=[[0,16,17,32,36,38,67,71],[0,16,17,32,36,39,68,72],[0,16,17,36,37,63,71,72],[0,16,17,36,38,39,62,63],[1,8,9,30,37,46,73,77],[1,8,9,30,37,47,74,78],[1,8,9,36,37,65,73,74],[1,8,9,37,46,47,64,65],[36,37,62,64,67,68,77,78]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def binary_rank(rows):
 b={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j not in b:b[j]=v;break
   v^=b[j]
 return len(b)
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 s=json.loads(gzip.decompress(raw));charts={int(k):v for k,v in s['frames'].items()}
 roots=[[F(t) for t in charts[s['start'][i]]['B'][0]] for i in range(111)]
 norms=[dot(r,r) for r in roots];assert set(norms)<={F(1),F(4)}
 v=[[t*(2 if n==1 else 1) for t in r] for r,n in zip(roots,norms)]
 assert all(dot(r,r)==4 and all(t.denominator==1 for t in r) for r in v)
 v=[[int(t) for t in r] for r in v];assert len(set(map(tuple,v)))==111
 K=[];B=[];contacts=0
 for i in range(111):
  kk=bb=0
  for j in range(111):
   z=dot(v[i],v[j]);assert z%2==0
   b=(z//2)%2;k=b^1
   bb|=b<<j;kk|=k<<j
   if i==j:assert k==1
   if i!=j:
    contact=all(dot(roots[i],[F(t) for t in ar])==0 for ar in charts[s['final'][111+j]]['A'])
    assert contact==(z==0) and bool(k)==contact
    contacts+=contact
  B.append(bb);K.append(kk)
 assert binary_rank(B)==8 and binary_rank(K)==9
 def check(fs):
  if len(fs)%2!=1:return False
  ct=collections.Counter()
  for ff in fs:
   if len(ff)!=8 or len(set(ff))!=8 or any(not 0<=i<111 for i in ff):return False
   if any((K[i]>>j&1)!=int(i==j) for i in ff for j in ff):return False
   ct.update(ff)
  return all(n%2==0 for n in ct.values())
 assert len(FRAMES)==9 and check(FRAMES)
 counts=collections.Counter(i for f in FRAMES for i in f)
 assert sum(counts.values())==72
 bad=[f.copy() for f in FRAMES];bad[0][0]=bad[0][1];assert not check(bad)
 assert not check(FRAMES[:-1])
 assert all(dot(v[i],v[j])!=0 for f in FRAMES for i in f for j in f if i!=j)
 out={'status':'PASS_INDEPENDENT_ACTUAL_BIT_NINE_FRAME_FITTING_REVIEW','source_sha256':SP,'roots':111,'native_raw_norm_histogram':{str(k):n for k,n in collections.Counter(norms).items()},'integral_doubled_norm':4,'rank_B_GF2':8,'rank_K_GF2':9,'offdiagonal_contact_checks':111*110,'offdiagonal_contacts':contacts,'fitting_ones':sum(x.bit_count() for x in K),'fitting_rows_hex':[hex(x) for x in K],'frames':FRAMES,'q':9,'ordered_identity_block_checks':576,'distinct_used_roots':len(counts),'multiplicities':dict(sorted(counts.items())),'multiplicity_histogram':dict(sorted(collections.Counter(counts.values()).items())),'all_V_theorem':'Every fitting has rank >=9V over every characteristic-two field; K tensor I_V attains9V.','negative_controls':{'repeated_vertex_rejected':True,'even_collection_rejected':True},'scope':'Actual111 BIT rational-chart native contact graph. Distinct from complex96/104 characteristic-two obstruction; no complete rail or physical claim.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','rank_B_GF2','rank_K_GF2','offdiagonal_contacts','distinct_used_roots','multiplicity_histogram']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
