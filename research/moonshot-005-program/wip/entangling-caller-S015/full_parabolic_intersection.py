#!/usr/bin/env python3
"""Exact complete Sp6 parabolic intersection, a necessary all-width quotient."""
import argparse,importlib.util,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path

def imp(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m

def app(A,v):
 z=0
 for j,c in enumerate(A):
  if v>>j&1:z^=c
 return z

def mul(A,B):return tuple(app(A,c)for c in B)
def rank(vs):
 p={}
 for v in vs:
  while v:
   j=v.bit_length()-1
   if j not in p:p[j]=v;break
   v^=p[j]
 return len(p)
def inv3(B):return tuple(next(v for v in range(8)if app(B,v)==1<<i)for i in range(3))
def tr3(B):return tuple(sum(((B[j]>>i)&1)<<j for j in range(3))for i in range(3))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--heads',default='4,2,2');ap.add_argument('--out',type=Path,default=Path(__file__).with_name('PARABOLIC-INTERSECTION.json'));ar=ap.parse_args();base=Path(__file__).parent;start=time.monotonic()
 m=imp('parabolic_actual',ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py');import exploration_support as lin;ki=lin;dp=lin
 I=m.eye(8);Xb=m.monomial([j^2 for j in range(8)],[0]*8);Cb=m.M((I.scale((1,1))+Xb.scale((1,-1))).a,1).norm();P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);D=m.monomial(list(range(8)),[(((x>>1)&1)+2*(x&1)*((x>>2)&1))%4 for x in range(8)]);A=Cb@D@P
 paulis={x|(z<<3):m.monomial([j^x for j in range(8)],[2*((j&z).bit_count()%2)for j in range(8)])for x,z in itertools.product(range(8),repeat=2)}
 a=[]
 for j in range(6):
  Q=A@paulis[1<<j]@A.star();hits=[v for v,R in paulis.items()if any(Q==R.scale(c)for c in[(1,0),(0,1),(-1,0),(0,-1)])];assert len(hits)==1;a.append(hits[0])
 a=tuple(a);ID=tuple(1<<j for j in range(6));aps=[ID]
 for _ in range(15):aps.append(mul(a,aps[-1]))
 assert aps[15]==ID and all(g!=ID for g in aps[1:15]);aps=aps[:15]
 H=set()
 for B in itertools.product(range(1,8),repeat=3):
  if rank(B)!=3:continue
  Bit=tr3(inv3(B))
  for bits in range(64):
   q=[(bits>>i)&1 for i in range(6)];C=(q[0]|q[3]<<1|q[4]<<2,q[3]|q[1]<<1|q[5]<<2,q[4]|q[5]<<1|q[2]<<2)
   H.add(tuple(app(B,1<<i)|(app(C,app(B,1<<i))<<3)for i in range(3))+tuple(v<<3 for v in Bit))
 assert len(H)==10752
 exps=tuple(map(int,ar.heads.split(',')));Ki=[[{-1:1},{-2:-1,-1:1},{}],[{}, {-1:-1},{0:1}],[{-1:1},{-2:-1},{}]];Dpoly=[[{exps[i]:1}if i==j else {}for j in range(3)]for i in range(3)];M=lin.mm(lin.mm(Ki,Dpoly),Ki)
 remaining=set(H);blocks=[];augpiv={};augbasis=[];lifts=[];processed=0;orbit_hist={};det={}
 while remaining:
  h=min(remaining);orbit=set()
  for u in range(15):
   ah=mul(aps[u],h)
   for v in range(15):orbit.add(mul(ah,aps[v]))
  hs=sorted(orbit&H);remaining.difference_update(hs);processed+=len(hs);orbit_hist[len(hs)]=orbit_hist.get(len(hs),0)+1;eq={};cache={}
  for idx,g in enumerate(hs):
   for k,l in itertools.product(range(3),repeat=2):
    col=9*idx+3*k+l
    for i,j in itertools.product(range(3),repeat=2):
     for u,c in M[i][k].items():
      for v,d in Ki[l][j].items():
       key=(u,idx,v)
       if key not in cache:cache[key]=mul(mul(aps[u%15],g),aps[v%15])
       z=cache[key]
       if z not in H:
        row=eq.setdefault((i,j,z),{});row[col]=row.get(col,0)+c*d
  rows=[{k:v for k,v in row.items()if v}for row in eq.values()];rows=[r for r in rows if r];ab,free,piv=ki.augmentation_image(rows,9*len(hs));bd={'head_representative':h,'ordinary_members':len(hs),'kernel_dimension':9*len(hs)-len(piv),'augmentation_dimension':len(ab)};blocks.append(bd)
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
    augbasis.append(av);lift=ki.lift_free(piv,{f:1});lifts.append([{'head':hs[c//9],'row':c%9//3,'column':c%3,'coefficient':str(v)}for c,v in sorted(lift.items())]);det=dp.determinant_polynomial(augbasis)
  if len(blocks)%1000==0 or det:print(json.dumps({'processed':processed,'blocks':len(blocks),'augmentation_dimension':len(augbasis),'det_nonzero':bool(det),'elapsed_seconds':time.monotonic()-start}),flush=True)
  if det:break
 out={'status':'EXACT_FULL_SYMPLECTIC_PARABOLIC_NECESSARY_INTERSECTION','actual_source_symplectic_columns':a,'target_exponents':exps,'ordinary_group_size':len(H),'ordinary_members_processed':processed,'all_ordinary_processed':not remaining,'cyclic_double_coset_blocks':len(blocks),'orbit_histogram':orbit_hist,'augmentation_dimension':len(augbasis),'augmentation_determinant_polynomial_nonzero':bool(det),'augmentation_basis':[[str(c)for c in v]for v in augbasis],'lifted_basis':lifts,'blocks':blocks,'elapsed_seconds':time.monotonic()-start,'scope':'Exact Sp6 quotient necessary for all-width callers after legitimate centre/Pauli reduction. An augmentation unit is not a full group-algebra unit, physical word or all-width construction.'}
 ar.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in['blocks','lifted_basis','augmentation_basis']}))
if __name__=='__main__':main()
