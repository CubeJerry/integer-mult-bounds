#!/usr/bin/env python3
"""Formal whole-interface identities and independent literal source controls."""
from pathlib import Path
import argparse,hashlib,json
from check_triangular_first_interstage import add,mul,neg,atom,mm
from review_square_normalizer import mm as imat,adj,tm,mt

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--square-package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);o=ap.parse_args()
 one,zero={():1},{}
 def prod(*xs):
  z=one
  for x in xs:z=mul(z,x)
  return z
 def clean(p):
  out={}
  for word,c in p.items():
   w=list(word);i=0
   while i+1<len(w):
    if w[i]=='a' and w[i+1]in('s','t'):w[i:i+2]=[w[i+1]+'hat','a']
    i+=1
   w=tuple(w);out[w]=out.get(w,0)+c
  return {w:c for w,c in out.items()if c}
 def degree(p,n):return {w:c for w,c in p.items()if w.count('a')==n}
 a,s,b,c,t,d,e,u,f,g=map(atom,('a','s','b','c','t','d','e','u','f','g'));a2=prod(a,a);a3=prod(a,a,a)
 L=[[a,zero,zero],[one,a,zero],[zero,zero,one]];U=[[a,neg(a2),zero],[zero,a,zero],[zero,zero,one]];C=[[s,b,c],[t,d,e],[u,f,g]];Q=[[atom(f'q{i}{j}')for j in range(3)]for i in range(3)]
 V=[atom('shat'),atom('that'),zero];W=[zero,s,u];Z=[prod(a,b,a),add(prod(b,a),prod(a,d,a)),prod(f,a)];F=[prod(a,c),add(c,prod(a,e)),g]
 P=[[clean(x)for x in row]for row in mm(mm(L,C),U)];expected=[[add(prod(V[r],a2),prod(W[r],a)),add(neg(prod(V[r],a3)),neg(prod(W[r],a2)),Z[r]),F[r]]for r in range(3)];assert P==expected
 E=mm(mm(P,Q),L)
 assert [[degree(E[r][j],4)for j in range(3)]for r in range(3)]==[[neg(prod(V[r],a3,Q[1][0],a)),neg(prod(V[r],a3,Q[1][1],a)),zero]for r in range(3)]
 assert [degree(E[r][2],3)for r in range(3)]==[neg(prod(V[r],a3,Q[1][2]))for r in range(3)]
 Qr=[[Q[0][0],Q[0][1],zero],[Q[1][0],Q[1][1],zero],[Q[2][0],Q[2][1],Q[2][2]]];Cr=[[s,b,zero],[t,d,e],[u,f,zero]];Pr=[[clean(x)for x in row]for row in mm(mm(L,Cr),U)];Er=mm(mm(Pr,Qr),L)
 assert [Er[r][2]for r in range(3)]==[zero,prod(a,e,Q[2][2]),zero]
 assert [degree(Er[2][j],3)for j in (0,1)]==[neg(prod(u,a2,Q[1][j],a))for j in (0,1)]
 Cru=[[s,b,zero],[t,d,e],[zero,f,zero]];Pru=[[clean(x)for x in row]for row in mm(mm(L,Cru),U)];Eru=mm(mm(Pru,Qr),L)
 assert Eru[2][0]==add(prod(f,a,Q[1][0],a),prod(f,a,Q[1][1]))
 Qr[1][1]=zero;Efinal=mm(mm(Pru,Qr),L)
 assert [degree(Efinal[r][1],3)for r in range(3)]==[prod(V[r],a2,Q[0][1],a)for r in range(3)]
 # Independent Gaussian-integer numerator arithmetic, literal source phase abd.
 A=[[(0,0)for _ in range(16)]for _ in range(16)];S=[[(0,0)for _ in range(16)]for _ in range(16)]
 for x in range(16):
  y=(x>>1)|((x&1)<<3);sgn=-1 if(x&11)==11 else 1;A[y][x]=(sgn,sgn);A[y^2][x]=(sgn,-sgn);S[y][x]=(sgn,0)
 A2=imat(A,A);A3=imat(A2,A);rootdata=json.loads((o.square_package/'RESULT.json').read_text());checks=[]
 for ex in rootdata['all24_fibre_permutation_controls']:
  J=[tuple(z)for z in ex['literal_Q_table']];JM=tm(J);B=mt(imat(imat(A2,JM),adj(A2)),16);assert B is not None
  assert all((J[x][0]&3)==ex['sigma'][x&3]for x in range(16))
  assert imat(imat(A2,JM),A)==imat(tm(B),A3)
  word=imat(imat(A,JM),A);supports=[sum(word[y][x]!=(0,0)for y in range(16))for x in range(16)];assert supports==[4]*16
  assert all(re*re+im*im==4 for row in word for re,im in row if(re,im)!=(0,0))
  checks.append({'sigma':ex['sigma'],'exact_four_path_support':True,'all_amplitude_moduli_one_half':True,'literal_square_transport':True})
 assert len(checks)==24
 Db=tm([(x,(x>>1)&1)for x in range(16)]);H=imat(adj(S),Db);assert mt(H,1)is not None
 hword=imat(imat(A,H),A);hsupport=sorted({sum(hword[y][x]!=(0,0)for y in range(16))for x in range(16)});assert hsupport==[2]
 assert mt(imat(imat(A2,H),adj(A2)),16)is None
 clean_controls=[]
 for name,T in [('identity',tm([(x,0)for x in range(16)])),('quarter_D_b',Db),('quartic_sign',tm([(x,2*int(x==15))for x in range(16)]))]:
  assert mt(imat(imat(A,T),adj(A)),4)is not None;clean_controls.append(name)
 deps=['results/complex-four-bit-cubic-source/author/PROOF.md','results/complex-boolean-sign-family/author/PROOF.md','results/complex-inverse-native-coset/two-native/PROOF.md'];prog=o.repo/'research/moonshot-005-program';proof=Path(__file__).with_name('CLEAN-FIRST-COLUMN-SQUARE-GATE.md')
 result={'status':'PASS_AUTHOR_CLEAN_FIRST_COLUMN_WHOLE_SQUARE_ALGEBRA_GATE','scope':'Universal faithful-width proof uses exact component-image directness; checker covers ordered polynomial identities and literal finite source controls, not an enumeration proof.','formal_checks':['clean-forward LCU column factorization','only degree4 terms carried by V','only degree3 last-column term -V a³q12','last-column normal form','bottom-row two degree3 terms','bottom-row after u=0','final degree3 column after q11=0'],'source_square_controls':checks,'clean_forward_source_controls':clean_controls,'outside_square_hypothesis_control':{'clock':'S^-1 D_b','ordinary_unit':True,'A_h_A_column_supports':hsupport,'A2_h_Aminus2_not_monomial':True,'not_a_positive_caller':True},'required_necessary_normal_form':{'C02_C22_Q02_Q12':'zero','C00_C12_Q22':'units','Q_active_corner':'unit'},'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'square_proof_sha256':hashlib.sha256((o.square_package/'PROOF.md').read_bytes()).hexdigest(),'source_pins':{d:hashlib.sha256((prog/d).read_bytes()).hexdigest()for d in deps}}
 o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['proof_sha256'])
if __name__=='__main__':main()
