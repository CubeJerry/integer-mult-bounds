#!/usr/bin/env python3
"""One exact full-ordinary four-native template in a necessary Sp6 quotient."""
import argparse,importlib.util,itertools,json,sys,time
from pathlib import Path

def imp(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--heads',default='4,4,4');ap.add_argument('--prefix',default='qii',choices=['qii','identity','cnot-shear','cz-shear','cnot-diag','cz-diag']);ap.add_argument('--out',type=Path,default=Path(__file__).with_name('FULL-PARABOLIC-FOUR.json'));ar=ap.parse_args();base=Path(__file__).parent;start=time.monotonic()
 import exploration_support as geo;lin=geo;ki=geo;dp=geo
 ID=tuple(1<<i for i in range(6));a=(12,33,16,32,8,18);aps=[ID]
 for _ in range(15):aps.append(geo.mul(a,aps[-1]))
 assert aps[15]==ID;aps=aps[:15];ai=aps[-1];ai2=aps[-2];Cb=(1,2,4,8,18,32);S=geo.mul(Cb,a);h=tuple(next(v for v in range(64)if geo.app(S,v)==1<<i)for i in range(6));s=S;si=h
 def e(g,c=1):return {g:c}
 def add(A,B):
  C=A.copy()
  for g,c in B.items():C[g]=C.get(g,0)+c
  return {g:c for g,c in C.items()if c}
 def mm(A,B):
  C=[[{}for _ in range(3)]for _ in range(3)]
  for i,j,k in itertools.product(range(3),repeat=3):
   for g,c in A[i][k].items():
    for h,d in B[k][j].items():
     z=geo.mul(g,h);C[i][j][z]=C[i][j].get(z,0)+c*d
  return [[{g:c for g,c in A.items()if c}for A in row]for row in C]
 def eye():return [[e(ID)if i==j else {}for j in range(3)]for i in range(3)]
 K=[[e(ID),{},add(e(a),e(ID,-1))],[e(a),{},e(a,-1)],[e(ID),e(ID),e(ID,-1)]];Ki=[[e(ai),add(e(ai),e(ai2,-1)),{}],[{},e(ai,-1),e(ID)],[e(ai),e(ai2,-1),{}]]
 Q=[[add(e(ID),e(s,-1)),add(e(h),e(ID)),e(ID)],[e(s),{},{}],[e(ID),e(h),e(ID)]];Qi=[[{},e(si),{}],[e(ID),e(ID),e(ID,-1)],[e(h,-1),add(e(si,-1),e(h,-1)),add(e(ID),e(h))]]
 if ar.prefix!='qii':
  Q=eye();Qi=eye()
  if ar.prefix!='identity':
   if ar.prefix.startswith('cz'):hg=(33,2,12,8,16,32)
   else:
    PP=(1,2,5);PPI=geo.tr3(geo.inv3(PP));hg=tuple(PP)+tuple(v<<3 for v in PPI)
   assert geo.mul(hg,hg)==ID
   if ar.prefix.endswith('shear'):Q[0][1]=e(hg);Qi[0][1]=e(hg,-1)
   else:Q[0][0]=e(hg);Qi[0][0]=e(hg)
 assert mm(K,Ki)==eye() and mm(Q,Qi)==eye() and mm(Qi,Q)==eye()
 H=set()
 for B in itertools.product(range(1,8),repeat=3):
  if geo.rank(B)!=3:continue
  Bit=geo.tr3(geo.inv3(B))
  for bits in range(64):
   q=[(bits>>i)&1 for i in range(6)];C=(q[0]|q[3]<<1|q[4]<<2,q[3]|q[1]<<1|q[5]<<2,q[4]|q[5]<<1|q[2]<<2);H.add(tuple(geo.app(B,1<<i)|(geo.app(C,geo.app(B,1<<i))<<3)for i in range(3))+tuple(v<<3 for v in Bit))
 assert len(H)==10752;cat=sorted(H);exps=tuple(map(int,ar.heads.split(',')));D=[[e(aps[exps[i]])if i==j else {}for j in range(3)]for i in range(3)];M=mm(mm(mm(mm(Ki,Qi),Ki),D),Ki);eq={}
 for idx,g in enumerate(cat):
  cache={}
  for k,l in itertools.product(range(3),repeat=2):
   col=9*idx+3*k+l
   for i,j in itertools.product(range(3),repeat=2):
    for u,c in M[i][k].items():
     for v,d in Ki[l][j].items():
      key=(u,v)
      if key not in cache:cache[key]=geo.mul(geo.mul(u,g),v)
      z=cache[key]
      if z not in H:
       row=eq.setdefault((i,j,z),{});row[col]=row.get(col,0)+c*d
  if idx%2000==0:print('heads',idx,'equations',len(eq),'elapsed',time.monotonic()-start,flush=True)
 rows=[{k:v for k,v in row.items()if v}for row in eq.values()];del eq;rows=[r for r in rows if r];print('linear_elimination',len(rows),flush=True)
 ab,free,piv=ki.augmentation_image(rows,9*len(cat));det=dp.determinant_polynomial(ab);out={'status':'EXACT_FULL_PARABOLIC_FOUR_NATIVE_TEMPLATE','target_exponents':exps,'source_a':a,'fixed_prefix':ar.prefix,'ordinary_elements':len(cat),'unknowns':9*len(cat),'equations':len(rows),'kernel_dimension':9*len(cat)-len(piv),'augmentation_dimension':len(ab),'augmentation_determinant_nonzero':bool(det),'augmentation_basis':[[str(c)for c in v]for v in ab],'elapsed_seconds':time.monotonic()-start,'scope':'Necessary quotient only; fixed prefix and endpoint gauge, arbitrary full ordinary unknown interstage. No universal caller impossibility and no phase-exact lift.'}
 if det:
  out['lifts']=[[{'head':cat[c//9],'row':c%9//3,'column':c%3,'coefficient':str(v)}for c,v in sorted(ki.lift_free(piv,{f:1}).items())]for f in free]
 ar.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in['lifts','augmentation_basis']}))
if __name__=='__main__':main()
