#!/usr/bin/env python3
"""Derivative collision with pinned independent geometry, binary controls,
and finite controls for the separate nonlinear-core proof."""
import argparse,gzip,hashlib,importlib.util,itertools,json
from pathlib import Path
import numpy as np

def need(ok,reason):
 if not ok:raise AssertionError(reason)
def xor(values):
 out=0
 for v in values:out^=int(v)
 return out
def brank(matrix):
 basis={}
 for row in np.asarray(matrix):
  v=sum(int(x)<<j for j,x in enumerate(row))
  while v:
   b=v.bit_length()-1
   if b in basis:v^=basis[b]
   else:basis[b]=v;break
 return len(basis)
def bm(A,B):return ((np.asarray(A,dtype=np.int64)@np.asarray(B,dtype=np.int64))&1).astype(np.uint8)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 repo=args.repo.resolve();here=Path(__file__).resolve().parent;base=repo/'research/moonshot-005-program/results'
 for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'pin '+name)
 spec=importlib.util.spec_from_file_location('independent_geometric_primitives',base/'bit-geometric-gauge-port-gate/review-c/check.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=a.root_coordinates(L,B)
 H=[set(x)for x in L['A2']];D=[set(x)for x in L['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not a.polar(x,y)}for j,x in enumerate(roots)]
 data=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text());parameters={int(j):{int(i):v for i,v in row.items()}for j,row in data['receiver_parameters'].items()}
 h=263;c=49;donors=[0,61,62];receivers=[i for i in range(111)if H[h]<=adj[i]]
 need(H[h]==set(donors)and data['H_nodes'][h]==c and len(receivers)==33 and 80 not in receivers and 10 not in donors,'literal identity-target H263')
 derivative=lambda v:a.power(v,8)^int(a.MUL[a.power(c,4),a.power(v,4)])
 reads={i:[derivative(parameters[j][i])for j in donors]for i in receivers};need(all(all(row)for row in reads.values()),'all readouts nonzero')
 audience=[i for i in receivers if D[108]<=adj[i]];need(5 in audience and 76 in audience and H[h]<=D[108],'shared actual D108')
 need(reads[5]==[30,18,12]and reads[76]==[38,18,52],'literal derivative collision')
 owners=set()
 for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
  phase,role,coordinate,plane,d,_,source,_=json.loads(line)
  if plane==h and d==108:
   need(phase=='X'and source==role and role in donors,'genuine shared-port owner');owners.update((role,coordinate,lane)for lane in range(8))
 need(len(owners)==16,'positive16-field native packet')
 values=[parameters[0][i]for i in receivers];_,basis=a.binary_map(values,values)
 coords={xor(basis[j]for j in range(6)if mask>>j&1):mask for mask in range(64)};need(len(coords)==64,'binary native basis')
 graph={v:{w for w in values if w!=v and v^w in values}for v in values};seen={values[0]};todo=list(seen)
 while todo:
  new=graph[todo.pop()]-seen;seen.update(new);todo.extend(new)
 need(len(seen)==33,'connected additive parameter graph')
 axis_cover=[]
 for axis in range(6):
  choices=[i for i in receivers if coords[parameters[0][i]]>>axis&1 and coords[parameters[0][i]].bit_count()>=2];need(choices,'each axis participates in mixed direction');i=choices[0]
  axis_cover.append({'axis':axis,'basis_receiver':receivers[values.index(basis[axis])],'mixed_receiver':i,'mixed_coordinates':coords[parameters[0][i]]})
 def scalar(t):return np.array([[int(a.MUL[t,1<<col])>>row&1 for col in range(6)]for row in range(6)],dtype=np.uint8)
 need(np.array_equal(scalar(30)^scalar(38),scalar(56))and brank(scalar(56))==6,'nonzero field scalar difference')
 need(np.array_equal(bm(scalar(18),scalar(int(a.INV[18]))),np.eye(6,dtype=np.uint8)),'denominator inverse')
 controls=[]
 for width in [1,2,15]:
  n=6*width;M=np.eye(n,dtype=np.uint8)
  for row in range(n):M[row]^=M[(row+1)%n]
  S=lambda t:np.kron(np.eye(width,dtype=np.uint8),scalar(t));need(brank(M)==n and np.any(bm(M,S(18))^bm(S(18),M)),'invertible genuinely noncommuting binary amplitude')
  R=S(int(a.INV[18]));C5=bm(bm(S(30),M),R);C76=bm(bm(S(38),M),R);factor=bm(bm(S(56),M),R)
  need(np.array_equal(C5^C76,factor)and brank(factor)==n,'uncommuted derivative factorization')
  W5=np.hstack([np.eye(n,dtype=np.uint8),C5]);W76=np.hstack([np.eye(n,dtype=np.uint8),C76]);need(brank(np.vstack([W5,W76]))==2*n and brank(np.vstack([W5,W5]))==n,'negative and positive common-row controls')
  controls.append({'quotient_width':width,'binary_amplitude_dimension':n,'difference_rank':n,'two_donor_union_rank':2*n,'noncommuting':True})
 # Exhaust all eight-point coordinate permutations for the mixed-direction
 # increment test. This supports, but does not replace, the abstract proof.
 affine=0
 for f in itertools.permutations(range(8)):
  if all((f[x^t]^f[x])==(f[t]^f[0])for x in range(8)for t in range(8)):affine+=1
 need(affine==8*7*6*4==1344,'all40320 finite coordinate permutations')
 bad=[1,0,2,3,4,5,6,7];need(any((bad[x^t]^bad[x])!=(bad[t]^bad[0])for x in range(8)for t in range(8)),'nonaffine mixed-direction control')
 # Preserve all three core parallel classes while deliberately violating
 # additivity on the whole ambient domain: the proof must stay cosetwise.
 swap=lambda x:((x&1)<<1)|((x>>1)&1)
 g=lambda x,y,z:(swap(x)if z else x,swap(y)if z else y,z)
 points=list(itertools.product(range(4),range(4),range(2)));need(len({g(*p)for p in points})==32,'global nonlinear control bijective')
 for x,y,z in points:
  old=g(x,y,z)
  for vx,vy in [(1,0),(0,1),(1,1)]:
   for t in range(4):
    new=g(x^(t if vx else 0),y^(t if vy else 0),z);delta=(old[0]^new[0],old[1]^new[1]);need(delta in{(s if vx else 0,s if vy else 0)for s in range(4)},'core coset partition control')
 need(g(1,0,1)!=tuple(x^y for x,y in zip(g(1,0,0),g(0,0,1))),'global additivity is not inferred')
 result={'status':'PASS_BINARY_GAP15_DERIVATIVE_COLLISION','H':h,'D':108,'receivers':[5,76],'derivative_rows':[reads[5],reads[76]],'difference_scalar':56,'common_denominator':18,'shared_port_fields_at_bank3840':16,'actual_D108_audience':audience,'parameter_graph_vertices':33,'parameter_graph_edges':sum(map(len,graph.values()))//2,'binary_parameter_basis':basis,'mixed_axis_cover':axis_cover,'noncommuting_binary_controls':controls,'nonlinear_core_control_permutations':40320,'affine_increment_permutations':affine,'globally_nonlinear_partition_preserving_control':True,'arbitrary_binary_linear_bank_gauges_excluded':True,'all_admissible_widths_and_finite_extensions':True,'nonlinear_upgrade_requires_separate_proof_review':True,'new_complete_kappa':False}
 args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],108,5,76,56,18,40320,1344,flush=True)

if __name__=='__main__':main()
