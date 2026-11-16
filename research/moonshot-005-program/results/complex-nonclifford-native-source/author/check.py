#!/usr/bin/env python3
"""Author exact controls; universal proof in PROOF.md."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,itertools,json,sys

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);args=ap.parse_args();here=Path(__file__).resolve().parent
 for dep in json.loads((here/'DEPENDENCIES.json').read_text())['sources']:
  assert hashlib.sha256((args.repo/dep['path']).read_bytes()).hexdigest()==dep['sha256'],dep['path']
 hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sp=importlib.util.spec_from_file_location('nc_source_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 tables={
  'S':([0,4,1,5,2,6,3,7],[0,0,0,0,0,0,0,2]),
  'J':([0,1,2,3,4,5,7,6],[0,0,0,0,0,0,1,1]),
  'R':([0,2,4,7,1,3,5,6],[0,0,0,1,0,0,0,1]),
  'L3':([0,1,2,3,4,7,6,5],[0,0,0,0,0,3,0,1]),
  'R3':([0,1,2,7,4,5,6,3],[0,0,0,1,0,0,0,1])}
 mon={n:m.monomial(*pq)for n,pq in tables.items()};I=m.eye(8)
 X={bit:m.monomial([j^bit for j in range(8)],[0]*8)for bit in[1,2,4]}
 C={bit:m.M((I.scale((1,1))+X[bit].scale((1,-1))).a,1).norm()for bit in[1,2,4]}
 P=m.monomial(tables['S'][0],[0]*8);D=m.monomial(list(range(8)),tables['S'][1]);S,R,L3,R3=map(mon.get,['S','R','L3','R3']);A=C[2]@S
 CZ=m.monomial(list(range(8)),[2*((j>>1)&1)*((j>>2)&1)for j in range(8)])
 assert D@P==S and D@P==P@D and S.power(2)==P.power(2)
 assert S@X[2]@S.star()==X[1]@CZ
 assert R==mon['J']@S.power(2)==C[1].star()@S@C[2]@S
 assert A.power(2)==C[1]@C[2]@R
 assert A.power(3)==L3@C[1]@C[2]@C[4]@R3
 assert A.power(3)==C[2]@D@C[1]@D@C[4]@D
 a3=A.power(3);tr=(F(sum(a3.a[j][j][0]for j in range(8)),2**a3.k),F(sum(a3.a[j][j][1]for j in range(8)),2**a3.k))
 assert tr==(F(-3,2),F(3,2));alpha3=(-1,1)
 for j in range(8):
  expected=tuple(z*(-1 if j==7 else 1)for z in alpha3)
  assert tuple(F(z,2**a3.k)for z in a3.a[j][j])==tuple(F(z,4)for z in expected)
 units=((1,0),(0,1),(-1,0),(0,-1))
 for x,y in itertools.product(range(8),repeat=2):
  a,b,c=(x>>j&1 for j in range(3));u,v,w=(y>>j&1 for j in range(3));dist=(u^a)+(v^b)+(w^c);sign=(a*b*c+a*b*w+u*b*w)%2
  z=m.gm(alpha3,units[(-dist+2*sign)%4]);assert tuple(F(z0,4)for z0 in z)==tuple(F(z0,2**a3.k)for z0 in a3.a[y][x])
 parity=sum(tables['S'][0][i]>tables['S'][0][j]for i in range(8)for j in range(i+1,8))%2
 assert parity==0 and sum(tables['S'][1])%4==2
 widths=[]
 for V in[1,2]:
  av=A.tp(V);sv,rv,l3v,r3v=(z.tp(V)for z in[S,R,L3,R3]);iv=m.eye(8**V)
  cav,cbv,ccv=(C[bit].tp(V)for bit in[1,2,4])
  assert cbv@sv==av and sv.star()@cav@rv==av
  assert cav@cbv@rv==av.power(2)
  assert av.power(3)==l3v@cav@cbv@ccv@r3v
  for z in[sv,rv,l3v,r3v]:assert z.star()@z==z@z.star()==iv
  assert av.power(2)@rv.star()==cav@cbv
  assert l3v.star()@av.power(3)@r3v.star()==cav@cbv@ccv
  assert av.power(3)!=av.power(2)
  if V==2:
   assert av.power(2).scale((-1,0))!=A.power(2).scale((-1,0)).tp(V)
   perm=[];phase=[];p,q=tables['S']
   for j in range(64):lo=j%8;hi=j//8;perm.append(p[hi]*8+p[lo]);phase.append(q[lo])
   assert m.monomial(perm,phase)!=sv
  widths.append({'V':V,'dimension':8**V,'all_independent_columns':8**V,'source_identities':True,'square_and_cube_wrappers':True})
 def matchings(xs):
  if not xs:yield [];return
  x=xs[0]
  for j in range(1,len(xs)):
   y=xs[j]
   for rest in matchings(xs[1:j]+xs[j+1:]):yield [(x,y)]+rest
 total=admitted=0
 for pairs in matchings(list(range(8))):
  for phases in itertools.product(range(4),repeat=4):
   p=[0]*8;qq=[0]*8
   for (x,y),q in zip(pairs,phases):p[x]=y;p[y]=x;qq[x]=q;qq[y]=(-q)%4
   criterion=all(p[x]==x^1 and qq[x]%2==0 for x in range(8));ismono=True
   for x in range(8):
    col={};c=units[qq[x]]
    for y,z in[(x,(1,0)),(p[x]^1,c),(x^1,(0,1)),(p[x],(c[1],-c[0]))]:col[y]=m.ga(col.get(y,(0,0)),z)
    nz=[z for z in col.values()if z!=(0,0)]
    ismono&=len(nz)==1 and sum(t*t for t in nz[0])==4
   assert criterion==ismono
   total+=1;admitted+=ismono
 assert(total,admitted)==(26880,16)
 assert C[2]@P!=A
 assert C[1]@C[2]@P.power(2)!=A.power(2)
 assert m.monomial(tables['L3'][0],[0]*8)@C[1]@C[2]@C[4]@R3!=A.power(3)
 assert L3@C[1]@C[2]@C[4]@m.monomial(list(range(8)),tables['R3'][1])!=A.power(3)
 odos=[]
 for V in range(1,5):
  digits=[0]*V;sums=[0]*len(tables);updates=0;qs=[q for p,q in tables.values()]
  for j in range(8**V):
   for k,q in enumerate(qs):assert sums[k]%4==sum(q[j//8**i%8]for i in range(V))%4
   if j==8**V-1:break
   i=0
   while True:
    old=digits[i];new=(old+1)%8;digits[i]=new
    for k,q in enumerate(qs):sums[k]=(sums[k]-q[old]+q[new])%4
    updates+=1
    if new:break
    i+=1
  assert updates*7<=8*8**V;odos.append({'V':V,'coordinates':8**V,'digit_updates':updates})
 result={'status':'PASS_NONCLIFFORD_SOURCE_ALGEBRA','gaussian_whole_job_ranks':[1,2,3],'tables':{n:{'permutation':p,'phase_mod4':q}for n,(p,q)in tables.items()},'trace_A_cubed':['-3/2','3/2'],'det_A':-1,'projective_order':'infinite by trace/determinant proof','invariant_lattice_at_2':'excluded by negative trace valuation','width_controls':widths,'monomial_involution_census':{'tested':total,'admitted':admitted},'phase_odometer_controls':odos,'negative_controls':['omit_CCZ','omit_source_Toffoli','omit_cube_left_phase','omit_cube_right_Toffoli','square_for_cube','tensor_exterior_minus','drop_second_column_phase'],'physical_status':'nonlinear permutation service requires separately proved admission','caller_status':'profitable retained-role caller unresolved','kappa_status':'No new kappa'}
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in['status','trace_A_cubed','det_A','monomial_involution_census','width_controls','kappa_status']}))
if __name__=='__main__':main()
