"""Exact robust-projector witnesses for the incomparable nine-packet gate."""
import argparse,gzip,hashlib,itertools,json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CP='9ec15dbf981c3a238b0c4687a717d5a3f32dc730099b29eb47b66b430f27983c'
B=[5,56,69,100,65,77,96,103]
BASES=[[0,1,2,4,5,6,7,8,9,10,11,12,13,15,16,18,20,22,23,24,25,26,27,28,29,31,32,33,37,42,44,48,51,53,54,57],[35,36,41,43,45,46,49,50,55,56,58,59,62,63,64,65,66,67,68,69,70,72,73,74,77,78,79,80,81,85,86,87,88,89,90,91]]
def root(n):
 t=[i for i in range(9) if n>>i&1]
 if len(t)==3:return [2 if i in t else -1 for i in range(9)]
 assert len(t)==7;z=[i for i in range(9) if i not in t]
 return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def detmod(rows,p=65537):
 a=[[x%p for x in row] for row in rows];d=1
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]),None)
  if k is None:return 0
  if k!=j:a[j],a[k]=a[k],a[j];d=-d
  v=a[j][j];d=d*v%p;q=pow(v,-1,p);a[j]=[x*q%p for x in a[j]]
  for k in range(j+1,len(a)):
   v=a[k][j];a[k]=[(x-v*y)%p for x,y in zip(a[k],a[j])]
 return d%p
def main(a):
 raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 cr=a.cap_certificate.read_bytes();assert hashlib.sha256(cr).hexdigest()==CP;cap=json.loads(cr);assert cap['source_pin']==SP
 caps={int(r):v for r,v in cap['rank_caps'].items()};assert caps=={1:1,2:2,3:4,4:8,5:16,6:24,7:35};caps[8]=96
 s=json.loads(gzip.decompress(raw));H=[s['live'][i] for i in s['hosted']['Dports']];R={h:root(s['frames'][s['initial'][h]][0]) for h in H}
 assert len(H)==96 and set(BASES[0]).isdisjoint(BASES[1]) and all(len(set(b))==36 and set(b)<=set(H) for b in BASES)
 assert all(dot(R[i],R[j])==18*int(i==j) for i in B for j in B)
 G={h:[dot(R[h],R[b])//9 for b in B] for h in H};assert all(dot(R[h],R[b])%9==0 for h in H for b in B)
 S={h:[G[h][p]*G[h][q] for p in range(8) for q in range(p,8)] for h in H}
 ds=[detmod([S[h] for h in b]) for b in BASES];assert all(ds)
 bad=[S[h] for h in BASES[0]];bad[0]=bad[1];assert detmod(bad)==0
 triples=[]
 for rs in itertools.combinations_with_replacement(range(1,9),3):
  if sum(rs)>17 or rs==(1,8,8):continue
  bound=min(caps[rs[i]]+caps[rs[j]] for i,j in itertools.combinations(range(3),2));triples.append((bound,rs));assert bound<42
 assert max(x[0] for x in triples)==40
 pairs=[(caps[r]+caps[t],r,t) for r in range(1,8) for t in range(1,8) if r+t<=8];assert max(x[0] for x in pairs)==36
 out={'status':'PASS_TWO_DISJOINT_PROJECTOR_BASES_AND_EXACT_NINE_PROFILES','source_sha256':SP,'cap_dependency_sha256':CP,'prime_for_integer_minor_certificate':65537,'source_coordinate_scale':'2*g_i in fixed orthogonal B8 basis; projector rows use upper-triangular products','gram_basis_roles':B,'two_disjoint_projector_bases':BASES,'projector_minor_determinants_mod65537':ds,'consequence':'Deleting ANY one of96 source projectors still leaves rank36 overQ and every characteristic-zero field.','z6_profiles_checked_except_1_8_8':len(triples),'maximum_smallest_pair_population_bound':max(triples),'z7_pair_population_bound':max(pairs),'negative_controls':{'duplicate_projector_row_has_zero_minor':True},'scope':'Exact finite premises for EXACTLY9 informative fresh packets; comparable and incomparable proof dependencies explicit; at-most9 optimum asserted only at t199/200 with admitted fresh8 raw-refinement optimum.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','projector_minor_determinants_mod65537','z6_profiles_checked_except_1_8_8','maximum_smallest_pair_population_bound','z7_pair_population_bound']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--cap-certificate',type=Path,default=Path(__file__).with_name('CAP-CERTIFICATE.json'));main(p.parse_args())
