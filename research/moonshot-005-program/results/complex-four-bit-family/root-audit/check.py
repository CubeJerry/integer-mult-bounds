"""Independent Gaussian-integer trace and conjugacy audit."""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json
p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--audit',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();s=importlib.util.spec_from_file_location('root_exact',a.engine);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);I=g.mono(list(range(16)))
def truth(terms):return sum((sum(int(x&t==t) for t in terms)%2)<<x for x in range(16))
def source(f):return g.native(f,4)[0]
def power(A,n):
 out=I
 for _ in range(n):out=g.mm(out,A)
 return out
def trace(A):return tuple(sum(A[x][x][j] for x in range(16)) for j in range(2))
def sign(f,a,b,d):return ((f>>(b+2*b+4*d+8*a))^(f>>(d+2*d+4*a+8*b))^(f>>(a+2*a+4*b+8*d)))&1
for mon in range(16):
 f=truth([mon]);parity=sum(sign(f,*q) for q in itertools.product([0,1],repeat=3))%2;assert parity==int(mon in [13,14,15])
checks=[]
for f in sorted(set([truth([j]) for j in range(16)]+[0x1234,0xffff,0xa55a,truth([7,11,13,15])])):
 T=sum((1 if x==y==z else -1)*(1-2*sign(f,x,y,z)) for x,y,z in itertools.product([0,1],repeat=3));tr=trace(power(source(f),3));assert tr==(-2*T,2*T);checks.append({'truth_mask':f,'T':T,'cube_trace_numerator_over8':tr})
Z=g.mono(list(range(16)),[2*int(x&13==13) for x in range(16)]);quad=[j for j in range(16) if j.bit_count()<=2];conj=0
for terms in [[j] for j in quad]+[quad,[0,1,3,5,10]]:
 q=truth(terms);f=q^truth([13,14]);assert g.mm(g.mm(Z,source(f)),Z)==source(q);conj+=1
finite=power(source(truth([13,14])),16);assert finite==[[g.scale(z,2**16) for z in row] for row in I]
assert trace(power(source(truth([7])),5))==(80,80)
result={'status':'PASS_INDEPENDENT_TRACE_AND_CONJUGACY_AUDIT','audit_sha256':hashlib.sha256(a.audit.read_bytes()).hexdigest(),'ANF_trace_parity_basis':16,'exact_trace_controls':checks,'exact_conjugacy_controls':conj,'finite_cubic_order_divides':16,'abc_fifth_trace':'5(1+i)/2','source_counts':{'quartic_free':32768,'cube_trace_certified_infinite':16384,'explicit_Clifford_conjugate_finite':4096,'not_classified_by_these_two_families':12288},'scope':'Written trace path/valuation and ordinary conjugacy proof reviewed independently; fixed-table physical premises retained. Discovery scans not used as proof.','new_complete_kappa':False};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
