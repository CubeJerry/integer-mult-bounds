#!/usr/bin/env python3
"""Exact source-gauge and all-eight-Pauli-sector controls; no synthesized caller."""
import argparse,hashlib,importlib.util,itertools,json,sys
from pathlib import Path
import walsh_group as w

def imp(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path(__file__).with_name('PAULI-SPLIT-RESULT.json'));ar=ap.parse_args()
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
 actual=hashlib.sha256(hp.read_bytes()).hexdigest();assert actual=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';m=imp('pauli_split_dyadic',hp)
 I=m.eye(8);Z=m.zero(8);S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);Si=S.star()
 X={v:m.monomial([x^v for x in range(8)],[0]*8) for v in range(8)}
 C={v:m.M((I.scale((1,1))+X[v].scale((1,-1))).a,1).norm() for v in range(1,8)}
 a=C[2]@S;L=m.block([[a,I],[Z,a]]);L0=m.block([[a,Z],[I,a]]);J=m.block([[Z,I],[I,Z]]);assert J@L0@J==L;gauges=0
 for u,v in itertools.permutations(range(1,8),2):
  t=next(t for t in range(1,8) if w.rank([t,u,v])==3);cols=(t,u,v)
  H=m.monomial([w.app(cols,x) for x in range(8)],[0]*8)
  left=m.diagonal([H,H@Si]);right=m.diagonal([Si@H.star(),H.star()]);target=m.block([[C[u],I],[Z,C[v]]])
  assert left@L@right==target
  gauges+=1
 prod=I
 for v in range(1,8):
  assert C[v]@C[v]==X[v]
  prod=prod@C[v]
 assert prod==I
 # Eight translation characters, 64 independent normalized phase characters.
 chars=[]
 for ell in range(8):
  roots=[(ell&v).bit_count()%2 for v in range(1,8)]
  assert sum(roots)%4==0
  for bits in itertools.product(range(2),repeat=6):
   signs=bits+(sum(bits)%2,)
   vals=tuple((r+2*b)%4 for r,b in zip(roots,signs))
   assert sum(vals)%4==0
   assert all((2*vals[v-1])%4==2*((ell&v).bit_count()%2) for v in range(1,8))
   chars.append(vals)
 assert len(set(chars))==512
 # BFS records exact generator expressions. Character values must be independent
 # of the path, including every generating edge for all 512 phase group elements.
 gens=[w.gaussian(v) for v in range(1,8)];expr={w.ONE:(0,)*7};queue=[w.ONE]
 for g in queue:
  for j,h in enumerate(gens):
   z=w.mul(g,h);e=list(expr[g]);e[j]=(e[j]+1)%4;e=tuple(e)
   if z not in expr:expr[z]=e;queue.append(z)
   else:
    diff=[(x-y)%4 for x,y in zip(e,expr[z])]
    assert all(sum(x*y for x,y in zip(diff,c))%4==0 for c in chars)
 assert len(expr)==512
 # Distinct ordinary translations and exact Gaussian rank distribution.
 ordinary=[g for g in expr if w.ordinary(g)];assert len(ordinary)==8
 hist={}
 for g in expr:hist[w.gaussian_rank(g)]=hist.get(w.gaussian_rank(g),0)+1
 assert hist=={0:8,1:56,2:224,3:224}
 # Literal tensor controls retain actual phases and no V=1 quotient.
 for V in [1,2]:
  Cv={v:C[v].tp(V) for v in range(1,8)};iv=m.eye(8**V);p=iv
  for v in range(1,8):p=p@Cv[v]
  assert p==iv
  assert Cv[1]@Cv[1]==X[1].tp(V)
 wrong=I
 for v in range(1,7):wrong=wrong@C[v]
 assert wrong!=I # Omitting the seventh actual phase is rejected.
 out={'status':'PASS_EXACT_SOURCE_GAUGES_AND_ALL_PAULI_SECTORS','actual_ordered_direction_gauges':gauges,'paid_lower_half_role_swaps':2,'phase_group_elements':512,'ordinary_translation_elements':8,'pauli_characters':8,'normalized_characters_per_sector':64,'all_phase_characters':512,'phase_character_edges_checked':512*7,'gaussian_rank_histogram':hist,'literal_tensor_widths':[1,2],'negative_controls':{'omitted_fano_factor_rejected':True,'actual_gaussian_square_is_translation_not_identity':C[1]@C[1]!=I},'source_helper_sha256':actual,'proof_sha256':hashlib.sha256(Path(__file__).with_name('PAULI-SPLIT-GAUGED-SOURCE.md').read_bytes()).hexdigest(),'scope':'Exact source identities and finite algebraic reduction only. No four-native word or supplier admission.','new_kappa':False}
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
