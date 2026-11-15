#!/usr/bin/env python3
"""Exact phase-aware source controls; all-width proof is separate."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

SCALE=10**30

def interval(r,p=199,q=200):
 n=pow(r,p)*pow(SCALE,q);lo=SCALE;hi=r*SCALE
 while lo+1<hi:
  mid=(lo+hi)//2
  if pow(mid,q)<=n:lo=mid
  else:hi=mid
 return (lo,lo) if pow(lo,q)==n else (lo,hi)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--out',type=Path,default=Path(__file__).with_name('RESULT.json'));ar=ap.parse_args();base=Path(__file__).parent
 deps=json.loads((base/'DEPENDENCIES.json').read_text())
 for d in deps['sources']:assert hashlib.sha256((ar.repo/d['path']).read_bytes()).hexdigest()==d['sha256']
 hp=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sp=importlib.util.spec_from_file_location('order9_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);Z=m.zero(8);X={v:m.monomial([j^v for j in range(8)],[0]*8)for v in [1,2,4]}
 C={v:m.M((I.scale((1,1))+X[v].scale((1,-1))).a,1).norm()for v in [1,2,4]}
 P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);D=m.monomial(list(range(8)),[(j>>1)&1 for j in range(8)]);S=D@P
 L=(C[2]@D).scale((0,1));B=L@P;assert L.power(3)==I;assert L.power(2)+L+I==Z;assert L.power(2)==(D@L@D).scale((0,1))
 assert P.power(3)==I and S@C[2]@S.star()==C[1]
 assert C[1].star()@S@C[2]@S==S.power(2)
 G1=S.scale((0,1));G2=S.power(2).scale((-1,0));H2=S.star().scale((0,-1))
 ranks=[m.gaussian_rank(B.power(k))for k in range(10)];assert ranks==[0,1,2,3,3,3,3,2,1,0]
 assert B.power(9)==I and all(B.power(k)!=I for k in range(1,9))
 trace=[]
 for k in range(9):
  A=B.power(k);tr=(sum(A.a[j][j][0]for j in range(8)),sum(A.a[j][j][1]for j in range(8)),A.k);assert tr[1]==0 and tr[0]==(8 if k==0 else -1)*(2**tr[2]);trace.append(8 if k==0 else -1)
 bridge=B.power(-4)@D@B.power(3);assert bridge==S.star().scale((0,-1)) and m.gaussian_rank(bridge)==0
 assert B.power(4)==(D@B.power(3)@S).scale((0,1))
 widths=[]
 for v in [1,2]:
  g1,g2,h2,b,ca,cb=(A.tp(v)for A in [G1,G2,H2,B,C[1],C[2]]);iv=m.eye(8**v)
  assert cb@g1==b and h2@g1==iv and h2@ca@g2==b and ca@cb@g2==b.power(2)
  assert b.power(-4)@D.tp(v)@b.power(3)==bridge.tp(v)
  # Actual all-column halves; no zero-input restriction is used.
  z=m.zero(8**v);nativeL=m.block([[cb,z],[iv,ca]]);nativeU=m.block([[cb,(ca@cb).scale((-1,0))],[z,ca]])
  before=m.diagonal([g1,g2]);after=m.diagonal([iv,h2])
  l=after@nativeL@before;u=after@nativeU@before
  assert l==m.block([[b,z],[iv,b]]) and u==m.block([[b,b.power(2).scale((-1,0))],[z,b]])
  li=m.block([[b.power(-1),z],[b.power(-2).scale((-1,0)),b.power(-1)]])
  ui=m.block([[b.power(-1),iv],[z,b.power(-1)]])
  assert l@li==m.eye(2*8**v) and u@ui==m.eye(2*8**v)
  assert m.gaussian_rank(b.power(3))==3*v
  widths.append(v)
 # The V=1 nontrivial-character relation cannot be silently tensor-lifted.
 s1=Z
 for k in range(9):s1=s1+B.power(k)
 assert s1==Z
 b2=B.tp(2);s2=m.zero(64)
 for k in range(9):s2=s2+b2.power(k)
 assert s2!=m.zero(64) and s2@s2==s2.scale((9,0))
 assert sum(s2.a[j][j][0]for j in range(64))==72*2**s2.k
 # Physical phase negative controls.
 raw=C[2]@S;assert raw.power(9)==I.scale((0,-1)) and raw.power(9)!=I
 assert B.tp(2)!=(C[2].tp(2)@S.tp(2)).scale((0,1))
 old=C[2]@P;assert m.gaussian_rank(old.power(4))==2 and m.gaussian_rank(B.power(4))==3
 assert B.power(2).scale((-1,0)).tp(2)!=B.tp(2).power(2).scale((-1,0))
 # Exact native/common-body invoice, including all rank-seven idles.
 cases=[]
 for heads in [(3,2,2),(3,3,3),(2,2,2)]:
  target={21+h:heads.count(h)for h in set(heads)};price={1:3,7:6,8:3};tab={r:interval(r)for r in set(target)|set(price)}
  lo=sum(c*tab[r][0]for r,c in target.items())-sum(c*tab[r][1]for r,c in price.items());hi=sum(c*tab[r][1]for r,c in target.items())-sum(c*tab[r][0]for r,c in price.items())
  cases.append({'heads':heads,'natives':3,'roles':3,'rank7_idles':3,'target':target,'price':price,'margin_numerators':[str(lo),str(hi)],'denominator':str(SCALE),'strict_positive':lo>0})
 assert cases[0]['margin_numerators']==['561007339600891538672434298712','561007339600891538672434298724'] and cases[1]['strict_positive'] and not cases[2]['strict_positive']
 tables={}
 for name,A in [('G1',G1),('G2',G2),('H2',H2),('D',D),('bridge',bridge)]:
  assert A.k==0;per=[];ph=[]
  for j in range(8):
   nz=[(i,A.a[i][j])for i in range(8)if A.a[i][j]!=(0,0)];assert len(nz)==1;per.append(nz[0][0]);ph.append([(1,0),(0,1),(-1,0),(0,-1)].index(nz[0][1]))
  tables[name]={'permutation':per,'phase_exponents_mod4':ph}
 out={'status':'PASS_EXACT_ORDER_NINE_SOURCE_AND_NONDIHEDRAL_TRANSPORT','source_dependencies':deps,'proof_sha256':hashlib.sha256((base/'PROOF.md').read_bytes()).hexdigest(),'power_gaussian_ranks':ranks,'power_traces':trace,'all_input_column_tensor_widths':widths,'actual_native_inverses_checked':True,'ordinary_monomial_tables':tables,'cyclic_faithfulness_for_all_V_at_least':2,'width2_cyclic_projector_rank':8,'ordinary_power_transport':[3,4],'complete_optimistic_movement_budgets':cases,'ordinary_extra_services_per_half':{'head_permutations':3,'unit_phase_passes':3,'new_gaussian_calls':0,'new_owners':0},'spectator_volume_multiplier':'2^V','negative_controls':['omitted normalization phase changes ninth power to -iI','width-independent i fails at V=2','omitted local phase loses rank-three fourth power','tensoring the native cross minus fails at even width','one-column cyclic sum identity fails at V=2'],'scope':'Exact source and uniform tensor construction; no caller, supplier admission or new kappa. The source-independent rank gates remain applicable.'}
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'power_gaussian_ranks':ranks,'proof_sha256':out['proof_sha256'],'budgets':cases}))
if __name__=='__main__':main()
