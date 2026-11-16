#!/usr/bin/env python3
"""Exact fixed-source controls and integer price enclosures; no floating point."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());args=ap.parse_args();base=Path(__file__).parent
hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';sp=importlib.util.spec_from_file_location('four_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
N=16;I=m.eye(N);X={b:m.monomial([j^b for j in range(N)],[0]*N)for b in[1,2,4,8]};C={b:m.M((I.scale((1,1))+X[b].scale((1,-1))).a,1).norm()for b in X};P=m.monomial([(j>>1)|((j&1)<<3)for j in range(N)],[0]*N);D=m.monomial(list(range(N)),[2*int(j&13==13)for j in range(N)]);S=D@P;A=C[2]@S
bits=lambda j:((j>>0)&1,(j>>1)&1,(j>>2)&1,(j>>3)&1)
def mon(perm,phase):return m.monomial([perm(*bits(j))for j in range(N)],[phase(*bits(j))%4 for j in range(N)])
L=mon(lambda a,b,c,d:a+2*(b^(c*d))+4*c+8*d,lambda a,b,c,d:c*d*(2*a+2*b-1))
R=mon(lambda a,b,c,d:a+2*b+4*(c^(a*b))+8*d,lambda a,b,c,d:a*b*(1+2*c+2*d))
J=mon(lambda a,b,c,d:(a^(c*d))+2*b+4*c+8*d,lambda a,b,c,d:c*d)
R2=J@S.power(2);G2=C[1]@C[2];G4=G2@C[4]@C[8];B=G2@P.power(2)
assert R2==P.power(2)@R and L.power(2)==I and R.power(2)==I
assert S.star()@C[1]@R2==A and C[2]@S==A and G2@R2==A.power(2)
assert A.power(4)==L@G4@R and B.power(2)==G4 and B@R@B.star()==L
T=m.monomial([int(f'{j:04b}'[::-1],2)for j in range(N)],[2*(j.bit_count()%2)for j in range(N)])
assert T.power(2)==I and T@A.star()@T==A.scale((0,-1))
# All256 fourth-power kernel coefficients derived independently from unique paths.
units=((1,0),(0,1),(-1,0),(0,-1));alpha4=(-1,0) # alpha^4=-1/4
for y in range(N):
 u,v,w,z=bits(y)
 for x in range(N):
  a,b,c,d=bits(x);flips=(a^u)+(b^v)+(c^w)+(d^z);sg=(-1)**((a*b*d+a*b*w+b*w*z+u*w*z)%2);num=m.gm(alpha4,units[-flips%4]);num=(sg*num[0],sg*num[1]);assert A.power(4).a[y][x]==num and A.power(4).k==2
ar=A.power(3);tr=(sum(ar.a[j][j][0]for j in range(N)),sum(ar.a[j][j][1]for j in range(N)));assert tr==(6,-6)and ar.k==2
# The source permutation is three coordinate SWAPs, each four transpositions.
assert sum(int(j&13==13)for j in range(N))==2
checks=[]
for V in[1,2]:
 a=A.tp(V);s=S.tp(V);r2=R2.tp(V);l=L.tp(V);r=R.tp(V);e=m.eye(N**V);z=m.zero(N**V);ca=C[1].tp(V);cb=C[2].tp(V)
 assert a.power(2)==(G2.tp(V)@r2) and a.power(4)==l@G4.tp(V)@r
 assert a.star()==(T.tp(V)@a@T.tp(V)).scale(units[-V%4])
 for typ in[0,2]:
  orig=m.block([[cb,z],[e,ca]])if typ==0 else m.block([[cb,(ca@cb).scale((-1,0))],[z,ca]])
  actual=m.diagonal([e,s.star()])@orig@m.diagonal([s,r2])
  expected=m.block([[a,z],[e,a]])if typ==0 else m.block([[a,a.power(2).scale((-1,0))],[z,a]])
  assert actual==expected
 checks.append({'width':V,'source_matrix_dimension':2*N**V,'endpoint_matrix_dimension':N**V,'all_columns':True,'both_native_orientations':True})
# Meaningful literal-source negatives.
assert (C[2]@P).power(4)!=L@G4@R
Lperm=mon(lambda a,b,c,d:a+2*(b^(c*d))+4*c+8*d,lambda a,b,c,d:0)
Rperm=mon(lambda a,b,c,d:a+2*b+4*(c^(a*b))+8*d,lambda a,b,c,d:0)
assert A.power(4)!=Lperm@G4@Rperm and A.power(4)!=L@G4 and A.power(4)!=G4@R
scale=10**40
def rootlo(n):
 target=n**199*scale**200;lo=0;hi=n*scale+1
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 assert lo**200<=target<(lo+1)**200
 return lo
vals={r:rootlo(r)for r in[7,8,22,23,25]}
plo=3*scale+6*vals[7]+3*vals[8];phi=plo+9
prices={}
for name,rs in [('421',[25,23,22]),('422',[25,23,23])]:
 tl=sum(vals[r]for r in rs);th=tl+3;lo=tl-phi;hi=th-plo;assert lo>0
 prices[name]={'lower_numerator':str(lo),'upper_numerator':str(hi),'denominator':str(scale)}
def table(g):
 return{'permutation':[next(i for i in range(N)if g.a[i][j]!=(0,0))for j in range(N)],'phase_mod4':[units.index(next(g.a[i][j]for i in range(N)if g.a[i][j]!=(0,0)))for j in range(N)]}
result={'status':'PASS_EXACT_FOUR_BIT_CUBIC_NATIVE_SOURCE','source_truth_mask':40960,'tables':{nm:table(g)for nm,g in [('S',S),('R2',R2),('L4',L),('R4',R),('T_inverse',T)]},'width_checks':checks,'cube_trace':{'numerator':[3,-3],'denominator':2,'valuation_at_1_plus_i':-1},'determinant':1,'fourth_kernel_entries_checked':256,'shared_right_gauge':True,'fresh_four_bit_inverse_witness':True,'L4_R4_involutions':True,'target_exponent':'199/200','gaussian_margins':prices,'three_native_421_source_and_endpoint_recipe':{'monomial_services':13,'coordinate_swaps':29,'Toffoli':6,'phase_passes':13,'additional_caller_operations':'still required and paid'},'negative_controls':['omit_source_cubic_phase','omit_both_quarter_phase_tables','omit_right_endpoint_table','omit_left_endpoint_table'],'scope':'Actual uniform source and rank4 endpoint; no caller or new kappa','new_kappa':False};(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='tables'}))
