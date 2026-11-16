#!/usr/bin/env python3
"""Exact source/family controls; universal claims are proved in PROOF.md."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,itertools,json,random,sys

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--catalogue',type=Path);args=ap.parse_args();here=Path(__file__).resolve().parent
 for dep in json.loads((here/'DEPENDENCIES.json').read_text())['sources']:
  assert hashlib.sha256((args.repo/dep['path']).read_bytes()).hexdigest()==dep['sha256'],dep['path']
 hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sp=importlib.util.spec_from_file_location('boolean_family_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 units=((1,0),(0,1),(-1,0),(0,-1))
 def ratio(x,y):return next((j for j,u in enumerate(units)if m.gm(u,y)==x),None)
 def table(M):
  p=[];q=[]
  for j in range(M.n):
   inds=[i for i in range(M.n)if M.a[i][j]!=(0,0)];assert len(inds)==1;i=inds[0];p.append(i)
   q.append(next(k for k,u in enumerate(units)if tuple(z*2**M.k for z in u)==M.a[i][j]))
  assert len(set(p))==M.n;return {'permutation':p,'phase_mod4':q}
 def normalizer(M,r,CC):
  n=M.n;groups={}
  for i,row in enumerate(M.a):groups.setdefault(tuple(j for j,z in enumerate(row)if z!=(0,0)),[]).append(i)
  assert len(groups)==n//2**r and all(len(a)==len(b)==2**r for a,b in groups.items())
  assert all(not(set(a)&set(b))for a,b in itertools.combinations(groups,2))
  C=m.eye(n)
  for j in range(r):C=C@CC[j]
  assert M.k==C.k
  rp=[None]*n;cp=[None]*n;lp=[None]*n;qq=[None]*n
  for block,(cols,rows) in enumerate(groups.items()):
   i0,j0=rows[0],cols[0];deph=[]
   for i in rows:
    bits=[]
    for j in cols:
     z=ratio(m.gm(M.a[i][j],M.a[i0][j0]),m.gm(M.a[i][j0],M.a[i0][j]));assert z in(0,2);bits.append(z//2)
    deph.append(sum(z<<k for k,z in enumerate(bits)))
   span={0:0};basis=[]
   for z in deph:
    if z not in span:
     b=len(basis);basis.append(z);span.update({x^z:y^(1<<b)for x,y in list(span.items())})
   assert len(basis)==r and set(deph)==set(span)
   rr=[span[z]for z in deph];cc=[sum(((basis[k]>>j)&1)<<k for k in range(r))for j in range(2**r)]
   assert sorted(rr)==sorted(cc)==list(range(2**r))
   for i,z in zip(rows,rr):rp[i]=z+(block<<r)
   for j,z in zip(cols,cc):cp[j]=z+(block<<r)
  for cols,rows in groups.items():
   i0,j0=rows[0],cols[0]
   for i in rows:lp[i]=ratio(M.a[i][j0],C.a[rp[i]][cp[j0]]);assert lp[i] is not None
   for j in cols:qq[j]=ratio(M.a[i0][j],m.gm(units[lp[i0]],C.a[rp[i0]][cp[j]]));assert qq[j] is not None
  p=[rp.index(i)for i in range(n)];q=[lp[p[j]]for j in range(n)];L=m.monomial(p,q);R=m.monomial(cp,qq)
  assert L@C@R==M;return L,R
 def data(d,mask):
  n=2**d;I=m.eye(n);XX=[m.monomial([x^(1<<j)for x in range(n)],[0]*n)for j in range(d)]
  CC=[m.M((I.scale((1,1))+z.scale((1,-1))).a,1).norm()for z in XX]
  p=[(x>>1)|((x&1)<<(d-1))for x in range(n)];P=m.monomial(p,[0]*n);f=[mask>>x&1 for x in range(n)];D=m.monomial(list(range(n)),[2*z for z in f]);S=D@P;A=CC[1]@S
  g=[f[x]^f[x^1]for x in range(n)];assert all(g[x]==g[x^1]for x in range(n));J=m.monomial([x^g[x]for x in range(n)],g);R=J@S.power(2)
  assert S.star()@CC[0]@R==A and CC[0]@CC[1]@R==A.power(2)
  L,Q=normalizer(A.power(3),3,CC)
  if d==3:
   anf=f[:]
   for bit in range(3):
    for x in range(8):
     if x>>bit&1:anf[x]^=anf[x^(1<<bit)]
   f0,la,lb,qab,lc,qac,qbc,eta=anf
   FF=[];GG=[];ll=[];qq=[]
   for x in range(8):
    a,b,c=(x>>j&1 for j in range(3));y=x^(2*((qab*a)^(eta*a*c)));z=x^(4*((qab*a)^((qbc^qac)*b)^(eta*a*b)));FF.append(y);GG.append(z)
    u,v,w=(y>>j&1 for j in range(3));rr=(la*u+(la+lc)*w+qac*u*w)%2
    cc=(f0+(lb+lc)*a+(la+lb+lc)*b+lb*c+(qbc+qac)*a*b+qab*b*c+qbc*a*c+eta*a*b*c)%2
    ll.append((x.bit_count()-y.bit_count()+2*rr)%4);qq.append((z.bit_count()-x.bit_count()+2*cc)%4)
   L=m.monomial(FF,ll);Q=m.monomial(GG,qq)
   assert L@CC[0]@CC[1]@CC[2]@Q==A.power(3)
  assert S.star()@S==R.star()@R==L.star()@L==Q.star()@Q==I
  return A,S,R,L,Q,CC,P,f,g
 counts={'finite':0,'infinite':0};Ts={};cat=[];saved={}
 for mask in range(256):
  A,S,R,L,Q,CC,P,f,g=data(3,mask);a3=A.power(3);delta=[(-1)**z for z in f];eps=[delta[1]*delta[2]*delta[4],delta[3]*delta[5]*delta[6]];T=delta[0]+delta[7]+3*sum(eps)
  tr=tuple(F(sum(a3.a[j][j][k]for j in range(8)),2**a3.k)for k in range(2));assert tr==(F(-T,4),F(T,4))
  odd=mask.bit_count()%2;det=(-1)**sum(f);assert det==(-1 if odd else 1)
  anf=f[:]
  for j in range(3):
   for x in range(8):
    if x>>j&1:anf[x]^=anf[x^(1<<j)]
  assert anf[7]==odd
  if odd:assert T%4==2 and T in(-6,-2,2,6);counts['infinite']+=1
  else:assert T%4==0;counts['finite']+=1
  Ts[T]=Ts.get(T,0)+1
  cat.append({'truth_table_mask':mask,'parity':odd,'order_class':'infinite_projective'if odd else'finite_Clifford','trace_bracket_T':T,'source_R':table(R),'cube_L':table(L),'cube_R':table(Q)})
  if mask in[0,1,37,128,255]:saved[mask]=(A,S,R,L,Q,CC)
 assert counts=={'finite':128,'infinite':128}
 widths=[]
 for mask,(A,S,R,L,Q,CC)in saved.items():
  V=2;av=A.tp(V);sv,rv,lv,qv=(z.tp(V)for z in[S,R,L,Q]);cs=[z.tp(V)for z in CC]
  assert sv.star()@cs[0]@rv==av and cs[0]@cs[1]@rv==av.power(2)
  assert lv@cs[0]@cs[1]@cs[2]@qv==av.power(3)
  assert av.power(2).scale((-1,0))!=A.power(2).scale((-1,0)).tp(V)
  widths.append({'mask':mask,'V':2,'dimension':64,'all_independent_columns':64})
 rng=random.Random(731);larger=[]
 for d in[4,5]:
  n=2**d;masks=[0,(1<<n)-1,1,1<<(n-1),sum(1<<x for x in range(n)if (x&7)==7),sum(1<<x for x in range(n)if x.bit_count()%2)]
  masks+=list(dict.fromkeys(rng.getrandbits(n)for _ in range(10)))
  for mask in masks:
   A,S,R,L,Q,CC,P,f,g=data(d,mask);larger.append({'d':d,'mask':mask,'source_and_cube':True})
 A,S,R,L,Q,CC=saved[128];base=CC[0]@CC[1]@CC[2]
 left=m.monomial([4,7,1,0,3,6,2,5],[1,3,0,2,2,1,0,3]);right=m.monomial([7,2,4,1,5,0,3,6],[0,1,1,3,2,0,3,2]);scramble=left@base@right
 l2,r2=normalizer(scramble,3,CC);assert l2@base@r2==scramble
 assert saved[0][0]!=A
 p=table(R)['permutation'];wrong=m.monomial(p,[0]*8);assert CC[0]@CC[1]@wrong!=A.power(2)
 assert m.monomial(table(L)['permutation'],[0]*8)@base@Q!=A.power(3)
 assert L@base@m.monomial(list(range(8)),table(Q)['phase_mod4'])!=A.power(3)
 bad=[list(row)for row in scramble.a];bad[0][0]=tuple(-z for z in bad[0][0]);bad=m.M(tuple(tuple(row)for row in bad),scramble.k)
 try:normalizer(bad,3,CC)
 except AssertionError:pass
 else:raise AssertionError('broken Hadamard control accepted')
 result={'status':'PASS_BOOLEAN_SIGNED_NATIVE_FAMILY','three_bit_tables':256,'order_classification':counts,'trace_bracket_distribution':{str(k):v for k,v in sorted(Ts.items())},'source_square_and_cube_normalizers':'exact complete entries for all256tables','width_two_controls':widths,'larger_dimension_controls':larger,'negative_controls':['source_sign_table','source_residual_phase','cube_left_phase','cube_right_permutation','tensor_exterior_minus','broken_Hadamard'],'universal_proof':'unique three-bit paths plus elementary Fano normalization; trace/determinant parity classification','scope':'exact source family and conditional physical interface; profitable caller unresolved; No new kappa'}
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
 if args.catalogue:args.catalogue.parent.mkdir(parents=True,exist_ok=True);args.catalogue.write_text(json.dumps({'convention':'input-indexed permutation and i-phase mod4','source_head':'A=C_bit1 D_mask P_cycle','entries':cat},indent=2)+'\n')
 print(json.dumps({k:result[k]for k in['status','three_bit_tables','order_classification','trace_bracket_distribution','scope']}))
if __name__=='__main__':main()
