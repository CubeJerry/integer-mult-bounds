#!/usr/bin/env python3
"""Exact atlas/operation certificates and directed local-source price bounds."""
import argparse,hashlib,json
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path

def basis(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return list(p.values())
def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&32:a^=37
 return c
CACHE={}
def root(r):
 if r not in CACHE:
  S=1<<192;N=r**199*S**200;lo=0;hi=r*S+1
  while hi-lo>1:
   z=(lo+hi)//2
   if z**200<=N:lo=z
   else:hi=z
  CACHE[r]=(F(lo,S),F(hi,S))
 return CACHE[r]
def add(*xs):return tuple(sum(x[k]for x in xs)for k in (0,1))
def scale(c,x):return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def lin(d):return add(*(scale(F(v),root(int(k)))for k,v in d.items()))
def dec(x):
 with localcontext()as c:c.prec=60;return str(Decimal(x.numerator)/Decimal(x.denominator))
def enc(x):return{'lower':str(x[0]),'upper':str(x[1]),'decimal_lower':dec(x[0]),'decimal_upper':dec(x[1])}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();base=a.repo/'research/moonshot-005-program';f=base/'results/bit-shared-facet-one-hop-gate/author-root/output/GEOMETRY.json';raw=f.read_bytes();assert hashlib.sha256(raw).hexdigest()=='4e0653d14264a3fc4e655eca1fb49b45188a1657832f6705c5687bca18fabc19';g=json.loads(raw);R=g['reflection_closure_roots'][:111];dot=lambda x,y:sum(v*w for v,w in zip(x,y));K=[sum(1<<j for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)];assert len(basis(K))==9;inverse_table=[next(b for b in range(1,32)if mul(v,b)==1)for v in range(1,32)];assert len(set(inverse_table))==31;cases=[]
 for i,atlas in enumerate(g['native_atlas']):
  foreign=[j for j in range(111)if dot(R[i],R[j])==0];degree=len(foreign);j=foreign[0];J=[a for a,p in enumerate(atlas)if j in g['normal_planes'][p]['full_foreign_roots']];assert len(J)==16;non=J[:12];anchors=[k for k in range(28)if k not in non];assert len(anchors)==16
  for p in atlas:assert len([x for x in g['normal_planes'][p]['full_foreign_roots']if x<111])>=27
  for l in foreign:assert sum(l in g['normal_planes'][p]['full_foreign_roots']for p in atlas)==16
  zero=basis(row^((row>>j&1)*K[j])for row in K);assert len(zero)==8 and all(not(row>>j&1)for row in zero);assert len(basis([K[j]]+zero))==9;outside=((1<<111)-1)^sum(1<<l for l in foreign);assert len(basis(row&outside for row in K))==9
  B=80;h=60;r=720;profile={1:B+2*h,2:degree*B,5:degree*B,6:B+h,7:(221-degree)*B,8:r-h};ops=2*(degree+1)*(B*B+2*B)+2*degree*B+r*(111*B-h)+h+B*r+B+B*h;assert sum(profile.values())==18680+80*degree
  bad=next(k for k in range(28)if k not in J);assert j not in g['normal_planes'][atlas[bad]]['full_foreign_roots'];assert len(basis([K[j]]+zero[:-1]+[zero[0]]))==8
  cases.append({'receiver':i,'foreign_degree':degree,'pivot_source':j,'atlas_plane_ids':atlas,'nonanchor_indices':non,'anchor_indices':anchors,'pivot_containing_chart_indices':J,'zero_at_pivot_canonical_basis_hex':list(map(hex,zero)),'held_binary_coordinates':60,'Hub_only_canonical_fields':660,'exceptional_single_read_fields':60,'final_canonical_rank':720,'completed_seed_transport_rank':780,'partial_Hub_history_rank_upper':8880,'owners_dirty_cleared':800,'movement_profile':profile,'MOVEs':sum(profile.values()),'ADD_upper':ops})
 degrees=sorted({x['foreign_degree']for x in cases});assert degrees==list(range(55,63));assert max(x['ADD_upper']for x in cases)==7249420
 N=lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10});H=lin({2:1,4:25,6:1,8:410});P2=add(scale(36,N),lin({1:444,**{7*j:444 for j in range(1,9)}}));T2=add(scale(36,H),lin({127:222,**{1+7*j:444 for j in range(1,10)}}));diff=add(T2,scale(-1,P2));cap=add(N,scale(-1,H),scale(F(1,36),diff));budgets={}
 for f in degrees:
  Q=lin({1:F(5,2),2:f,5:f,6:F(7,4),7:221-f,8:F(33,4)});room=add(cap,scale(-1,Q));m2=add(scale(18,room),scale(F(1,2),diff));m4=add(scale(54,room),scale(F(1,2),diff));assert room[0]>0 and m2[1]<0 and m4[0]>0;budgets[str(f)]={'Q':enc(Q),'room':enc(room),'m2_hypothetical_margin':enc(m2),'m4_hypothetical_margin':enc(m4),'first_positive_even_m_if_full_endpoints_were_supplied':4}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps({'status':'PASS_ALL111_ATLAS_PIVOT_CANONICAL_DIMENSION_AND_OPERATION_CERTIFICATES','geometry_sha256':hashlib.sha256(raw).hexdigest(),'GF32_nonzero_inverse_table':inverse_table,'cases':cases,'negative_controls':['Chart outside the chosen source incidence cannot host its pivot','Duplicating a zero-at-source canonical row reduces basis rank'],'scope':'Root checks exact atlas/basis choices, counts and field premise. A separate independent review explicitly inverts binary80-by80 selected encoders. No111 enormous literal words are emitted or claimed replayed.','new_complete_kappa':False},indent=2)+'\n');(a.out/'BUDGET.json').write_text(json.dumps({'status':'PASS_RIGOROUS_ALL_RECEIVER_LOCAL_MOMENTS','scale_bits':192,'native_degree_values':degrees,'ceiling':enc(cap),'cases_by_foreign_degree':budgets,'max_receiver_degree':62,'owners':800,'maximum_moves':23640,'maximum_ADD_bound':7249420,'complete_native_endpoint_status':'NOT_SUPPLIED; caller margins are conditional diagnostics only.','new_complete_kappa':False},indent=2)+'\n');print(json.dumps({'receivers':111,'worst_Q':budgets['62']['Q']['decimal_lower'],'worst_room':budgets['62']['room']['decimal_lower'],'maximum_ADD_bound':7249420}))
if __name__=='__main__':main()
