#!/usr/bin/env python3
"""Exact finite controls for the written non-Clifford two-native theorem."""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());args=ap.parse_args();base=Path(__file__).parent
hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91';sp=importlib.util.spec_from_file_location('tn_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
I=m.eye(8);Z=m.zero(8);units=((1,0),(0,1),(-1,0),(0,-1));Xb=m.monomial([x^2 for x in range(8)],[0]*8);Cb=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm();P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);Zb=m.monomial(list(range(8)),[2*((x>>1)&1)for x in range(8)]);Db=m.monomial(list(range(8)),[(x>>1)&1 for x in range(8)])
def ordinary(g):return g.k==0 and all(sum(z!=(0,0)for z in row)==1 for row in g.a)and all(sum(g.a[i][j]!=(0,0)for i in range(8))==1 for j in range(8))and all(z in units for row in g.a for z in row if z!=(0,0))
def canon(g):
 gs=[g.scale(u)for u in units];j=min(range(4),key=lambda j:gs[j].a);return gs[j],(-j)%4
# Formal group-ring coefficients are Gaussian integers; phases depend on width residue.
def collect(xs,V):
 out={}
 for g,c in xs:
  u,ph=canon(g);c=m.gm(c,units[ph*V%4]);out[u]=m.ga(out.get(u,(0,0)),c)
 return{u:c for u,c in out.items()if c!=(0,0)}
def eq(xs,ys,V):return collect(xs,V)==collect(ys,V)
def add(*xs):return sum((list(x)for x in xs),[])
def neg(xs):return[(g,(-c[0],-c[1]))for g,c in xs]
def prod(xs,ys):return[(g@h,m.gm(c,d))for g,c in xs for h,d in ys]
def one(g):return[(g,(1,0))]
def filt(xs,pred):return[(g,c)for g,c in xs if pred(g)]
def evaluation(xs,V=1):
 r=m.zero(8**V)
 for g,c in xs:r=r+g.tp(V).scale(c)
 return r
heads=[]
for mask in[128,64,112,176]:
 S=m.monomial(list(range(8)),[2*(mask>>x&1)for x in range(8)])@P;A=Cb@S;heads.append((mask,A,S));assert all(sum(z!=(0,0)for z in row)==4 for row in A.power(2).a)
count=0;ordinary_collisions=0;physical=0
for (ma,a,sa),(mb,b,sb),inverse_b in itertools.product(heads,heads,[False,True]):
 if inverse_b:b=b.star()
 HS=[I,P,sa,sa.star(),Zb,Db,sa.star()@Zb,sa.star()@Db]
 for k in range(8):
  h1,h2,h3,h4=[HS[(k+j*3)%8]for j in range(4)]
  u=add(one(h3),one(h1@h2@h3));v=one(h1@h4);w=one(h2@h3);z=one(h4)
  aub=prod(prod(one(a),u),one(b));awb=prod(prod(one(a),w),one(b));azb=prod(prod(one(a),z),one(b));ub=prod(u,one(b));vb=prod(v,one(b))
  bottom_left=add(ub,awb);bottom_right=add(neg(prod(u,one(b.power(2)))),neg(prod(awb,one(b))),vb,azb)
  cos=lambda g:ordinary(g@b.star())
  assert not any(cos(a@h@b)for h in HS)
  for V in range(4):
   assert eq(filt(bottom_left,cos),ub,V)
   assert eq(filt(bottom_left,ordinary),filt(awb,ordinary),V)
   assert eq(filt(bottom_right,cos),add(vb,neg(prod(filt(awb,ordinary),one(b)))),V)
  ordinary_collisions+=sum(ordinary(a@h@b)for h in HS)
  # Exact physical expansion on every fixture, both cross signs.
  pp=m.block([[evaluation(u),evaluation(v)],[evaluation(w),evaluation(z)]])
  n0=m.block([[a,Z],[I,a]])
  for sg in[1,-1]:
   n2=m.block([[b,b.power(2).scale((sg,0))],[Z,b]])
   expected=m.block([[evaluation(aub),evaluation(add(prod(prod(one(a),u),one(b.power(2).scale((sg,0)))) ,prod(prod(one(a),v),one(b))))],[evaluation(bottom_left),evaluation(add(prod(u,one(b.power(2).scale((sg,0)))),prod(awb,one(b.scale((sg,0)))),vb,azb))]])
   assert n0@pp@n2==expected;physical+=1
  count+=1
# Sharp total head four control; ordinary-endpoint and singular-middle controls.
controls=[]
for mask,a,s in heads:
 plus=m.block([[a,a.power(2)],[Z,a]]);minus=m.block([[a,a.power(2).scale((-1,0))],[Z,a]])
 assert minus@plus==m.diagonal([a.power(2),a.power(2)])
 swap=m.block([[Z,I],[I,Z]]);lower=m.block([[a,Z],[I,a]]);bi=a.star();upper_inv_head=m.block([[bi,bi.power(2).scale((-1,0))],[Z,bi]])
 assert lower@swap@upper_inv_head==swap
 singular=m.diagonal([Z,I]);n2=m.block([[a,a.power(2).scale((-1,0))],[Z,a]])
 assert lower@singular@n2==m.diagonal([Z,a.power(2)])
 controls.append({'mask':mask,'sharp_head_profile':[2,2],'ordinary_endpoint_if_rank_hypothesis_removed':True,'singular_middle_leaves_zero_owner':True})
assert ordinary_collisions>0
result={'status':'PASS_EXACT_NONCLIFFORD_TWO_NATIVE_CONTROLS','ordinary_middle_fixtures':count,'width_phase_residues_checked':4,'coset_projection_identities_per_fixture':3,'physical_signed_block_expansions':physical,'observed_ordinary_collisions':ordinary_collisions,'sharp_and_negative_controls':controls,'universal_claim':'Written finite-word separation plus support/coset/rank proof, not inferred from finite fixtures','extension':'No finite nonordinary Clifford group or invariant2-adic lattice required','new_kappa':False};(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
