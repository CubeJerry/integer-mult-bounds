#!/usr/bin/env python3
"""Bounded exact endpoint-gauge synthesis over the full ordinary Sp6 parabolic."""
import argparse,importlib.util,itertools,json,pickle,random,sys,time
from fractions import Fraction as F
from pathlib import Path
import sympy as sy

def imp(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cases',type=int,default=32);ap.add_argument('--out',type=Path,default=Path(__file__).with_name('FULL-ENDPOINT-GAUGES.json'));ar=ap.parse_args();base=Path(__file__).parent;start=time.monotonic()
 import exploration_support as geo;lin=geo;ki=geo;dp=geo
 a=(12,33,16,32,8,18);ID=tuple(1<<i for i in range(6));aps=[ID]
 for _ in range(15):aps.append(geo.mul(a,aps[-1]))
 assert aps[15]==ID;aps=aps[:15]
 cache=base/'order15-parabolic-types.pkl'
 if cache.exists():data=pickle.loads(cache.read_bytes());types=data['types'];orbits=data['orbits']
 else:
  H=set()
  for B in itertools.product(range(1,8),repeat=3):
   if geo.rank(B)!=3:continue
   Bit=geo.tr3(geo.inv3(B))
   for bits in range(64):
    q=[(bits>>i)&1 for i in range(6)];C=(q[0]|q[3]<<1|q[4]<<2,q[3]|q[1]<<1|q[5]<<2,q[4]|q[5]<<1|q[2]<<2)
    H.add(tuple(geo.app(B,1<<i)|(geo.app(C,geo.app(B,1<<i))<<3)for i in range(3))+tuple(v<<3 for v in Bit))
  assert len(H)==10752;remaining=set(H);out={};orbits=0
  while remaining:
   h=min(remaining);gs={};order=[]
   for u,v in itertools.product(range(15),repeat=2):
    g=geo.mul(geo.mul(aps[u],h),aps[v])
    if g not in gs:gs[g]=len(order);order.append(g)
   hs=[g for g in order if g in H];remaining.difference_update(hs);orbits+=1
   indices=[tuple(gs[geo.mul(geo.mul(aps[u],hj),aps[v])]for u,v in itertools.product(range(15),repeat=2))for hj in hs];ordinary=tuple(g in H for g in order);key=(ordinary,tuple(indices))
   if key not in out:out[key]={'multiplicity':0,'ordinary':ordinary,'indices':indices,'representative':h,'heads':hs}
   out[key]['multiplicity']+=1
  types=list(out.values());assert sum(t['multiplicity']*len(t['indices'])for t in types)==10752;cache.write_bytes(pickle.dumps({'types':types,'orbits':orbits,'a':a}))
 print('types',len(types),'orbits',orbits,flush=True)
 def scalar(E):return [[{0:int(v)}if v else {}for v in row]for row in E]
 def inverse(kind):
  sg,cr,cs=[(1,0,1),(1,2,-1),(-1,-2,-1),(-1,0,1)][kind]
  return [[{-sg:1},{cr-2*sg:-cs},{}],[{},{-sg:1},{}],[{},{},{0:1}]]
 rng=random.Random(5151015);cases=[]
 for trial in range(ar.cases):
  while True:
   ss,tt=rng.choice([(1,0),(0,1),(1,1),(1,-1)]);E=[[rng.randrange(-1,2)for _ in range(3)]for _ in range(2)]+[[0,ss,tt]];Fmat=[[rng.randrange(-1,2),rng.randrange(-1,2),0],[rng.randrange(-1,2),rng.randrange(-1,2),tt],[rng.randrange(-1,2),rng.randrange(-1,2),-ss]]
   if sy.Matrix(E).det() and sy.Matrix(Fmat).det():break
  profile=[(0,0,0),(0,1,0),(1,0,0),(0,0,1),(0,3,0),(3,0,0),(0,0,3),(1,1,1)][trial%8];n2,n1,n0=[inverse(k)for k in profile];heads=(3 if trial%2==0 else 4,2,2);D=[[{heads[i]:1}if i==j else {}for j in range(3)]for i in range(3)];M=lin.mm(lin.mm(lin.mm(lin.mm(n2,scalar(E)),D),scalar(Fmat)),n0)
  augpiv={};augbasis=[];lifts=[];total_kernel=0
  for ti,t in enumerate(types):
   eq={};nh=len(t['indices'])
   for h in range(nh):
    for k,l in itertools.product(range(3),repeat=2):
     col=9*h+3*k+l
     for i,j in itertools.product(range(3),repeat=2):
      for u,c in M[i][k].items():
       for v,d in n1[l][j].items():
        g=t['indices'][h][(u%15)*15+(v%15)]
        if t['ordinary'][g]:continue
        row=eq.setdefault((i,j,g),{});row[col]=row.get(col,0)+c*d
   rows=[{k:v for k,v in row.items()if v}for row in eq.values()];rows=[r for r in rows if r];ab,free,piv=ki.augmentation_image(rows,9*nh);total_kernel+=(9*nh-len(piv))*t['multiplicity']
   for av,f in zip(ab,free):
    v={j:c for j,c in enumerate(av)if c};new=False
    while v:
     p=min(v);c=v[p]
     if p not in augpiv:augpiv[p]={j:x/c for j,x in v.items()};new=True;break
     for j,x in augpiv[p].items():
      val=v.get(j,F(0))-c*x
      if val:v[j]=val
      elif j in v:del v[j]
    if new:
     augbasis.append(av);lift=ki.lift_free(piv,{f:1});lifts.append({'type':ti,'entries':[{'head':t['heads'][c//9],'row':c%9//3,'column':c%3,'coefficient':str(v)}for c,v in sorted(lift.items())]})
  det=dp.determinant_polynomial(augbasis);ans={'trial':trial,'source_orientations':profile,'heads':heads,'left':E,'right':Fmat,'full_kernel_dimension':total_kernel,'augmentation_dimension':len(augbasis),'determinant_polynomial_nonzero':bool(det)};cases.append(ans);ar.out.write_text(json.dumps({'status':'BOUNDED_EXACT_FULL_ORDINARY_ENTANGLING_ENDPOINT_SCREEN','source_a':a,'ordinary_elements':10752,'double_cosets':orbits,'incidence_types':len(types),'cases':cases,'elapsed_seconds':time.monotonic()-start,'scope':'Each full-parabolic quotient screen is exact, but boundary choices are bounded. A unit augmentation still needs all other character blocks, actual phase lift and a physical ordinary circuit.'},indent=2)+'\n');print(json.dumps(ans),flush=True)
  if det:
   (base/'FULL-ENDPOINT-WITNESS.json').write_text(json.dumps({'case':ans,'augmentation_basis':[[str(c)for c in v]for v in augbasis],'lifts':lifts},indent=2)+'\n');break
if __name__=='__main__':main()
