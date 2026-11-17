#!/usr/bin/env python3
"""Exact source/coset and rank-six witness for one specified C-prime column."""
import argparse,hashlib,importlib.util,json,sys,itertools
from fractions import Fraction as F
from pathlib import Path
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'

def run(repo,out):
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('cprime_envelope_exact',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 def sc(x,re,im=0):
  re,im=F(re),F(im);den=max(re.denominator,im.denominator);assert den&(den-1)==0
  y=x.scale((int(re*den),int(im*den)));return m.M(y.a,y.k+den.bit_length()-1).norm()
 def tab(n,dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(n)]) for x in range(1<<n)],[phase(*[(x>>k)&1 for k in range(n)])%4 for x in range(1<<n)])
 h=lambda x:sc(x,F(1,2));i4=m.eye(4);i16=m.eye(16)
 rr=tab(4,lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);xb=m.monomial([x^2 for x in range(16)],[0]*16)
 a0=h(i16.scale((1,1))+xb.scale((1,-1)))@rr
 r2=tab(4,lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
 s2=tab(4,lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0);s1=tab(4,lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0);s=tab(4,lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
 j0=r2.star()@s2@r2;k0=a0@j0@s@a0.star();assert m.gaussian_rank(k0)==0 and a0@j0==k0@a0@s
 zs=tab(2,lambda s,t:s+2*t,lambda s,t:2*s);zt=tab(2,lambda s,t:s+2*t,lambda s,t:2*t);xt=tab(2,lambda s,t:s+2*(t^1),lambda s,t:0)
 I=m.eye(64);Z=m.zero(64);a=i4.tensor(a0);S=zs.tensor(s);S1=zs.tensor(s1);S2=zs.tensor(s2);T=zt.tensor(i16);R=xt.tensor(i16);J=i4.tensor(j0);K=zs.tensor(k0)
 P=h(I+T);N=I+sc(P,-1);U=h(I+R);V=I+sc(U,-1);As=h(I+S);Bs=I+sc(As,-1);A2=h(I+S2);B2=I+sc(A2,-1);H=sc(T+R,F(1,2),F(1,2))
 assert a.star()@S@a==S1 and a.power(-2)@S@a.power(2)==S2 and a@J==K@a@S
 p=U@B2;z=R@H@U@A2;w=V;D0=P+sc(N@V,-1);D1=P+N@V
 c00=P@As+sc(N@V@Bs,-1);c01=sc(P@Bs+N@V@As,-1);c10=J@U@Bs;c11=J@U@As;c20=N@As+P@V@Bs
 assert c00@a@a@z==c10@a@a@z==Z and c20@a@a@z==a@a@z
 direct=[a@c00@a@p+a@c01@a@z,a@c10@a@p+a@c11@a@z,sc(a@a@z,-1)]
 formula=[h(D0@a@a@(p+S1@z)+D1@a@a@(S1@p+sc(z,-1))),h(K@U@a@a@(sc((I+sc(S1,-1))@p,-1)+(I+S1)@z)),sc(a@a@z,-1)]
 assert direct==formula
 u=a0@a0;heads=[u,u@s1,u@s1@s2];assert u@s2==s@u
 ratios=[]
 for i,j in itertools.combinations(range(3),2):
  q=heads[i]@heads[j].star();assert m.gaussian_rank(q)!=0
  ratios.append({'pair':[i,j],'relative_gaussian_rank':m.gaussian_rank(q),'relative_sha256':hashlib.sha256(repr(q).encode()).hexdigest()})
 assert all(m.gaussian_rank(x)==2 for x in heads)
 # Reconstruct every coefficient in (2) before merging the u and u*s2 cosets.
 pp=h(i4+zt);nn=i4+sc(pp,-1);uu=h(i4+xt);bb=xt@sc(zt+xt,F(1,2),F(1,2))@uu;d0=pp+sc(nn@(i4+sc(uu,-1)),-1);d1=pp+nn@(i4+sc(uu,-1))
 cs=[
  [sc(d0@uu+sc(d1@bb,-1),F(1,4)),sc(d0@uu@zs+d1@bb@zs,F(-1,4)),sc(d0@zs@bb+d1@zs@uu,F(1,4)),sc(d0@bb+sc(d1@uu,-1),F(1,4))],
  [sc(zs@uu@(bb+sc(uu,-1)),F(1,4)),sc(uu@(bb+uu),F(1,4)),sc(uu@(uu+bb),F(1,4)),sc(zs@uu@(bb+sc(uu,-1)),F(1,4))],
  [sc(bb,F(-1,2)),sc(bb@zs,F(-1,2)),m.zero(4),m.zero(4)]
 ]
 words=[u,u@s2,u@s1,u@s1@s2]
 for r in range(3):
  val=m.zero(64)
  for cf,g in zip(cs[r],words):val=val+cf.tensor(k0@g if r==1 else g)
  assert val==direct[r]
 def take(q,rows,cols):return m.M(tuple(tuple(q.a[i][j] for j in cols) for i in rows),q.k).norm()
 def det3(q):
  v=(0,0)
  for perm in itertools.permutations(range(3)):
   z=(1,0)
   for i,j in enumerate(perm):z=m.gm(z,q.a[i][j])
   sg=-1 if sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2 else 1
   v=m.ga(v,(sg*z[0],sg*z[1]))
  return F(v[0],1<<(3*q.k)),F(v[1],1<<(3*q.k))
 epsblocks=[[cs[r][0]+cs[r][1],cs[r][2],cs[r][3]] for r in range(3)];envelope=m.block(epsblocks)
 witness=[]
 for sig,inds,rows,want in [(1,[0,2],[0,1,5],(F(0),F(1,64))),(-1,[1,3],[0,1,2],(F(1,128),F(1,128)))]:
  sectors=[[take(x,inds,inds) for x in row] for row in epsblocks];mr=m.block(sectors)
  assert all(mr.a[r][2*c]==mr.a[r][2*c+1] for r in range(6) for c in range(3))
  minor=take(mr,rows,[0,2,4]);value=det3(minor);assert value==want
  witness.append({'sigma_sign':sig,'rank':3,'minor_rows':rows,'minor_columns':[0,2,4],'minor_determinant':[str(x) for x in value],'minor_numerator':minor.a,'minor_denominator_power_of_two':minor.k})
 # Sigma summands really decouple: no cross-sign coefficient is silently omitted.
 assert all(x.a[i][j]==(0,0) for row in epsblocks for x in row for i in range(4) for j in range(4) if (i-j)%2)
 result={'status':'PASS_FIXED_CPRIME_COLUMN_ENVELOPE_GATE','scope':'one specified cancelling column; fixed finite prefix-matrix/collective tail catalogue; no universal Cprime gate','prefix_dimension':4,'ordinary_quadratic_encoder_capacity':4,'exact_coset_envelope_rank':6,'source_coset_count':3,'coset_controls':ratios,'sigma_witnesses':witness,'exact_quadratic_column_identity':True,'all_four_source_word_coefficients_reconstructed':True,'positive_interface_preserved':True,'new_kappa':False}
 out.mkdir(parents=True,exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 manifest={'engine':ENGINE,'engine_sha256':SHA,'files':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json']}};(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],'rank6 > capacity4',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.repo,a.out)
