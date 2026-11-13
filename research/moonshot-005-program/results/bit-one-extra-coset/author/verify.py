"""Exact primary-source finite premises for one-extra-coset gluing."""
import argparse,collections,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
def rank_selected(rows):
 basis={};sel=[]
 for ix,v in enumerate(rows):
  while v:
   p=v.bit_length()-1
   if p in basis:v^=basis[p]
   else:basis[p]=v;sel.append(ix);break
 return len(basis),sel
def rank(rows):return rank_selected(rows)[0]
def main(a):
 blob=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();pin=hashlib.sha256(blob).hexdigest();assert pin=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(blob));fr={int(k):v for k,v in s['frames'].items()};roots=[]
 for i in range(111):
  r=[F(x) for x in fr[s['start'][i]]['B'][0]];norm=sum(x*x for x in r);assert norm in [1,4];r=[int(x*(2 if norm==1 else 1)) for x in r];assert sum(x*x for x in r)==4;roots.append(r)
 K=[]
 for i,r in enumerate(roots):
  row=0
  for j,t in enumerate(roots):
   z=sum(x*y for x,y in zip(r,t));assert z%2==0;k=1^((z//2)%2);assert k==int(i==j or z==0);row|=k<<j
  K.append(row)
 assert rank(K)==9 and all(K[i]>>j&1==K[j]>>i&1 for i in range(111) for j in range(111))
 _,bp=rank_selected(K);basis=[K[i] for i in bp];assert len(basis)==9
 words={0:0}
 for k,r in enumerate(basis):words.update({v^r:m|(1<<k) for v,m in list(words.items())})
 assert len(words)==512 and min(v.bit_count() for v in words if v)==48
 normals=[words[r] for r in K];points=[sum(((r>>j)&1)<<k for k,r in enumerate(basis)) for j in range(111)]
 assert len(set(normals))==111 and all(normals) and rank(normals)==9
 assert all(((normals[i]&points[j]).bit_count()%2)==(K[i]>>j&1) for i in range(111) for j in range(111))
 full=(1<<111)-1;zero=[full^r for r in K];single=[]
 for i in range(111):
  ids=[j for j in range(111) if zero[i]>>j&1];r,sel=rank_selected([points[j] for j in ids]);assert r==8;single.append([i,[ids[k] for k in sel]])
 pairs=[];commonhist=collections.Counter();bestpair=None
 for i,j in itertools.combinations(range(111),2):
  assert rank([normals[i],normals[j]])==2
  mask=zero[i]&zero[j];ids=[l for l in range(111) if mask>>l&1]
  r,sel=rank_selected([points[l] for l in ids]);assert r==7;pairs.append([i,j,[ids[k] for k in sel]])
  common=(K[i]&K[j]).bit_count();commonhist[common]+=1
  if common==36 and bestpair is None:bestpair=(i,j)
 assert len(pairs)==6105 and max(commonhist)==36 and bestpair is not None
 # Coordinate exception and sharp non-coordinate witness, checked in the binary field.
 outside=[full^(K[i]^(1<<i)) for i in range(111)];restr=[{word&m for word in words} for m in outside]
 assert all(len(v)==512 for v in restr)
 coord=[]
 for j in range(111):
  avail=sum(1<<i for i in range(111) if ((1<<j)&outside[i]) in restr[i]);assert avail==K[j];coord.append(avail.bit_count())
 j,k=bestpair;h=(1<<j)|(1<<k);avail=[i for i in range(111) if (h&outside[i]) in restr[i]]
 assert len(avail)==36 and h not in words and all((h^(1<<l)) not in words for l in range(111))
 # Three dependent normals do not suffice for abstract pair-relation gluing.
 aa=[1,2,3];qq=[0,0,1]
 assert all(rank([aa[i],aa[j],qq[i]^qq[j]])==2 for i,j in itertools.combinations(range(3),2))
 assert not any(all((qq[i]^q) in [0,aa[i]] for i in range(3)) for q in range(4))
 cert={'source_sha256':pin,'basis_ports':bp,'basis_rows_hex':[hex(v) for v in basis],'feature_points':points,'coefficient_normals':normals,'single_zero_witnesses':single,'pair_zero_witnesses':pairs}
 a.output.mkdir(parents=True,exist_ok=True);cb=(json.dumps(cert,separators=(',',':'))+'\n').encode();(a.output/'SOURCE-CERTIFICATE.json.gz').write_bytes(gzip.compress(cb,mtime=0))
 out={'status':'PASS_EXACT_SOURCE_PREMISES_ONE_EXTRA_COSET_GLUING','source_sha256':pin,'code_dimension':9,'minimum_nonzero_binary_codeword_weight':48,'all111_nonzero_distinct_normals':True,'all111_single_zero_restriction_ranks':8,'all6105_pair_zero_intersection_ranks':7,'maximum_pair_closed_neighborhood_intersection':36,'pair_closed_intersection_histogram':dict(sorted(commonhist.items())),'coordinate_availability_sizes':coord,'all111_coordinate_availability_exact_closed_neighborhood':True,'sharp_noncoordinate_witness':{'h_support':[j,k],'availability':avail,'availability_count':36},'rank_two_three_normal_gluing_negative_control':True,'source_certificate_sha256':hashlib.sha256(cb).hexdigest(),'source_certificate_gzip_sha256':hashlib.sha256((a.output/'SOURCE-CERTIFICATE.json.gz').read_bytes()).hexdigest(),'scope':'Exact binary source ranks imply scalar characteristic-two extension-field theorem by the written gluing proof. Does not classify arbitrary rank10 spaces or entangled operator-valued extra mode.'}
 (a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','all111_single_zero_restriction_ranks','all6105_pair_zero_intersection_ranks','maximum_pair_closed_neighborhood_intersection','sharp_noncoordinate_witness']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
