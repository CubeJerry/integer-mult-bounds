#!/usr/bin/env python3
"""Symbolic Boolean proof checks plus exact source-table and finite census controls."""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json,random,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());args=ap.parse_args();base=Path(__file__).parent
# Boolean polynomials are sets of squarefree monomial masks. Multiplication uses x²=x.
def add(*ps):
 out=set()
 for p in ps:out.symmetric_difference_update(p)
 return out
def mul(*ps):
 out={0}
 for p in ps:
  nxt=set()
  for x in out:
   for y in p:
    z=x|y
    if z in nxt:nxt.remove(z)
    else:nxt.add(z)
  out=nxt
 return out
vv={s:{1<<i}for i,s in enumerate('a b c d u v w z q r s p h k e'.split())};a,b,c,d,u,v,w,z,q,r,s,p,h,k,eta=[vv[n]for n in 'a b c d u v w z q r s p h k e'.split()]
E=add(mul(a,u),mul(b,v),mul(c,w),mul(d,z),mul(q,add(mul(b,u),mul(d,w),mul(a,z))),mul(r,add(mul(a,w),mul(b,z))),mul(s,b,w),mul(p,add(mul(a,d,w),mul(b,u,w),mul(a,b,z))),mul(h,add(mul(b,d,w),mul(b,u,z),mul(a,w,z))),mul(k,add(mul(a,b,w),mul(b,w,z))),mul(eta,add(mul(a,b,d,w),mul(a,b,w,z),mul(b,u,w,z))))
VV=[add(a,mul(q,b)),b,add(c,mul(q,d),mul(r,a),mul(s,b),mul(p,a,d),mul(h,b,d),mul(k,a,b),mul(eta,a,b,d)),add(d,mul(q,a),mul(r,b),mul(p,a,b))]
UU=[add(u,mul(h,w,z)),add(v,mul(p,u,w),mul(h,u,z),mul(add(k,mul(q,h),mul(eta,q)),w,z),mul(eta,u,w,z)),w,z]
normal=add(*(mul(x,y)for x,y in zip(UU,VV)),mul(eta,UU[2],UU[3],VV[0],VV[1]));assert E==normal
wrong=list(UU);wrong[1]=add(wrong[1],mul(eta,q,w,z));assert E!=add(*(mul(x,y)for x,y in zip(wrong,VV)),mul(eta,wrong[2],wrong[3],VV[0],VV[1]))
N=16;rot=lambda x,j:((x>>j)|((x&((1<<j)-1))<<(4-j)))if j else x
indices=[[[0]*4 for x in range(N)]for y in range(N)]
for y,x in itertools.product(range(N),repeat=2):
 cur=x
 for j in range(3,-1,-1):
  indices[y][x][j]=rot(cur,(4-j)%4);bit=(1-j)%4;cur=(cur&~(1<<bit))|(y&(1<<bit))
 assert cur==y
F=lambda f,y,x:sum((f>>t)&1 for t in indices[y][x])%2
base_rows=[sum(((x&y).bit_count()%2)<<x for x in range(N))for y in range(N)]
def rows(f):
 return [sum((((x&y).bit_count()%2)^F(f,y,x)^F(f,y,0)^F(f,0,x)^F(f,0,0))<<x for x in range(N))for y in range(N)]
def brank(xs):
 piv={}
 for x in xs:
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;break
 return len(piv)
def anf(f):
 co=[f>>x&1 for x in range(N)]
 for j in range(4):
  for x in range(N):
   if x>>j&1:co[x]^=co[x^(1<<j)]
 return co
def parameters(f):
 c=anf(f);return c[3],c[5]^c[10],c[6]^c[9]^c[12],c[7],c[11],c[13]^c[14],c[15]
def maps(f):
 q,r,s,p,h,k,e=parameters(f);vs=[];us=[]
 for x in range(N):
  a,b,c,d=[x>>j&1 for j in range(4)];vs.append((a^(q*b))+2*b+4*(c^(q*d)^(r*a)^(s*b)^(p*a*d)^(h*b*d)^(k*a*b)^(e*a*b*d))+8*(d^(q*a)^(r*b)^(p*a*b)))
  u,v,w,z=[x>>j&1 for j in range(4)];us.append((u^(h*w*z))+2*(v^(p*u*w)^(h*u*z)^((k^(q*h)^(e*q))*w*z)^(e*u*w*z))+4*w+8*z)
 assert sorted(vs)==list(range(N))and sorted(us)==list(range(N))
 return us,vs,e
# Verify the cross table on the complete16-monomial ANF basis.
def evalpoly(poly,bits):return sum(int(mask&bits==mask)for mask in poly)%2
basis_checked=0
for term in range(N):
 f=sum(int(x&term==term)<<x for x in range(N));par=parameters(f);rr=rows(f)
 for y,x in itertools.product(range(N),repeat=2):
  assign=x+(y<<4)+sum(t<<(8+j)for j,t in enumerate(par));assert evalpoly(E,assign)==(rr[y]>>x&1)
 basis_checked+=1
hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';sp=importlib.util.spec_from_file_location('class_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
I=m.eye(N);xb=m.monomial([x^2 for x in range(N)],[0]*N);Cb=m.M((I.scale((1,1))+xb.scale((1,-1))).a,1).norm();P=m.monomial([rot(x,1)for x in range(N)],[0]*N);units=[(1,0),(0,1),(-1,0),(0,-1)]
def canonical(e):
 ar=[]
 for y in range(N):
  row=[]
  for x in range(N):
   sg=(-1)**(e*((y>>2)&1)*((y>>3)&1)*(x&1)*((x>>1)&1));t=units[-(x^y).bit_count()%4];row.append((-sg*t[0],-sg*t[1]))
  ar.append(tuple(row))
 return m.M(tuple(ar),2)
WW=[canonical(e)for e in[0,1]];assert all(g@g.star()==I for g in WW)
controls=[]
for par in itertools.product(range(2),repeat=7):
 mons=[3,5,6,7,11,13,15];f=sum((sum(c*int(x&t==t)for c,t in zip(par,mons))%2)<<x for x in range(N));controls.append(f)
rng=random.Random(20261116);controls+=rng.sample(range(65536),32)
for f in controls:
 uu,vv,e=maps(f);inv=[uu.index(j)for j in range(N)];L=m.monomial(inv,[(j.bit_count()-inv[j].bit_count()+2*F(f,inv[j],0))%4 for j in range(N)]);R=m.monomial(vv,[(vv[x].bit_count()-x.bit_count()+2*F(f,0,x)+2*F(f,0,0))%4 for x in range(N)]);A=Cb@m.monomial(list(range(N)),[2*(f>>x&1)for x in range(N)])@P
 assert A.power(4)==L@WW[e]@R
 assert brank(rows(f))==4+e
# Reference changes preserve the claimed invariant.
refchecks=0;tensor=[]
for e in[0,1]:
 rr=[sum((((x&y).bit_count()%2)^(e*((y>>2)&1)*((y>>3)&1)*(x&1)*((x>>1)&1)))<<x for x in range(N))for y in range(N)];assert brank(rr)==4+e
 for ri,ci in itertools.product(range(N),repeat=2):
  changed=[]
  for row in rr:
   z=row^rr[ri];changed.append(z^((2**N-1)if z>>ci&1 else 0))
  assert brank(changed)==4+e;refchecks+=1
 rr2=[sum((((r1>>x1)&1)^((r2>>x2)&1))<<(16*x1+x2)for x1,x2 in itertools.product(range(N),repeat=2))for r1,r2 in itertools.product(rr,repeat=2)];assert brank(rr2)==2*(4+e);tensor.append({'eta':e,'width2_rank':brank(rr2)})
# Reproduce the finite census efficiently by Gray-code updates; this is supplementary.
contrib=[]
for z in range(N):contrib.append([a^b for a,b in zip(rows(1<<z),base_rows)])
rr=list(base_rows);last=0;counts={}
for t in range(65536):
 f=t^(t>>1)
 if t:
  pos=(f^last).bit_length()-1;rr=[a^b for a,b in zip(rr,contrib[pos])]
 last=f;key=(f.bit_count()%2,brank(rr));counts[key]=counts.get(key,0)+1
assert counts=={(0,4):32768,(1,5):32768}
result={'status':'PASS_ANALYTIC_FOUR_BIT_FOURTH_POWER_CLASSIFICATION','symbolic_boolean_variables':15,'symbolic_normal_form_identity':True,'missing_eta_q_row_correction_rejected':True,'ANF_basis_monomials_checked':basis_checked,'effective_parameter_cases':128,'additional_full_table_controls':32,'actual_phase_exact_A4_normalizers_checked':len(controls),'reference_changes_checked':refchecks,'tensor_rank_controls':tensor,'finite_census':{str(k):v for k,v in counts.items()},'proof_status':'Universal written Boolean kernel/permutation/invariant proof; finite census kept separate','new_kappa':False};(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
