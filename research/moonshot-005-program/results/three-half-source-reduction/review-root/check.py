#!/usr/bin/env python3
"""Independent ordered extraction, literal codec and tariff review."""
import argparse,collections,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def root(q):
 a=[i for i in range(9)if q>>i&1]
 if len(a)==3:return [2 if i in a else -1 for i in range(9)]
 need(len(a)==7,'native normal');u,v=[i for i in range(9)if i not in a];return [3*(int(i==u)-int(i==v))for i in range(9)]
def gram(q,r):return F(sum(x*y for x,y in zip(root(q),root(r))),18)
def pow_interval(r):
 scale=10**32;target=r**199*scale**200;a,b=0,r*scale+1
 while a+1<b:
  c=(a+b)//2
  if c**200<=target:a=c
  else:b=c
 need(a**200<=target<b**200,'integer root interval');return F(a,scale),F(b,scale)
def moment(terms):
 a=b=F(0)
 for r,c in terms.items():
  lo,hi=pow_interval(r);a+=c*(lo if c>=0 else hi);b+=c*(hi if c>=0 else lo)
 return a,b
def main(author,out):
 pins={'PROOF.md':'56df558dbeaa4994c025c8e2ac78074a61cd17ab143fd60d9358ef43232ec390','MANIFEST.json':'feaf2b06752af3172a19d108357c0999729b5749cd16351c3465b2056a5cc7e4','INTERFACE-PROGRAM.json':'bc0f2aade58bb2191349ee13492f2b660f6a3a97662fdfa9a56a34995b318e2e'}
 for n,h in pins.items():need(hashlib.sha256((author/n).read_bytes()).hexdigest()==h,'pin '+n)
 need(hashlib.sha256((HERE/'source/GEOMETRY.json').read_bytes()).hexdigest()=='e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6','geometry pin')
 sourcepins=json.loads((author/'SOURCES.json').read_text())['pins']
 for n,h in sourcepins.items():need(hashlib.sha256((author/n).read_bytes()).hexdigest()==h,'inherited source '+n)
 I=s.eye(3);Z=s.zeros(3);blk=lambda A,B,C,D:A.row_join(B).col_join(C.row_join(D))
 U=lambda A:blk(I,A,Z,I);L=lambda A:blk(I,Z,-A,I);diag=lambda A,B:blk(A,Z,Z,B)
 wrong_c=wrong_e=0
 for k in range(1,21):
  a=s.Matrix([[1,k,1],[0,1,k+1],[0,0,1]]);b=s.Matrix([[1,0,0],[k+1,1,0],[1,k+2,1]])
  f=s.Matrix([[1,1,0],[0,1,0],[k,0,1]]);D1=s.Matrix([[1,0,k],[1,1,0],[0,0,1]]);D2=s.Matrix([[1,k+1,0],[0,1,0],[1,0,1]]);D3=s.Matrix([[1,0,0],[0,1,k],[k+2,0,1]])
  need(a*b!=b*a and D1*a!=a*D1,'noncommuting controls')
  c=b.inv()*D1*a.inv()*D1.inv();e=f.inv()*D2*b.inv()*D2.inv()
  first=diag(D1,D1)*U(a);second=diag(D2,D2)*L(b);third=diag(D3,D3)*U(f)
  W=third*diag(I,e)*second*diag(c,I)*first
  exact=blk(Z,D3*D2*b.inv()*D1,-D3*f.inv()*D2*b.inv()*D1*a.inv(),Z)
  need(W==exact,'full six-column ordered extraction')
  badc=D1*b.inv()*a.inv()*D1.inv();bade=D2*f.inv()*b.inv()*D2.inv()
  wrong_c+=third*diag(I,e)*second*diag(badc,I)*first!=exact
  wrong_e+=third*diag(I,bade)*second*diag(c,I)*first!=exact
 need(wrong_c==wrong_e==20,'wrong orders rejected')
 g=json.loads((HERE/'source/GEOMETRY.json').read_text());q={int(k):v for k,v in g['normal_by_port'].items()};codec=json.loads((author/'R0-CODEC.json').read_text());ports=codec['ports'];n=len(ports);pos={h:i for i,h in enumerate(ports)}
 A=[[F(i==j)for j in range(n)]for i in range(n)];counts=collections.Counter()
 for op in codec['opcodes']:
  tag=op[0];counts[tag]+=1
  if tag=='ADD':_,i,j,c=op;c=F(c);A[i]=[x+c*y for x,y in zip(A[i],A[j])]
  elif tag=='SCALE':_,i,c=op;c=F(c);need(c!=0,'invertible scale');A[i]=[c*x for x in A[i]]
  elif tag=='SWAP':_,i,j=op;A[i],A[j]=A[j],A[i]
  else:raise ValueError('unadmitted codec operation')
 E=[[F(0)for _ in ports]for _ in ports]
 for cl in g['classes']:
  for h in cl['ports']:
   for j in cl['ports']:E[pos[h]][pos[j]]=F(h==j)-gram(q[h],q[j])
 need(A==E,'all12544 independent codec coefficients')
 need(dict(counts)=={'ADD':224,'SCALE':304,'SWAP':92},'literal codec invoice')
 program=json.loads((author/'INTERFACE-PROGRAM.json').read_text());need(program['productive_rank25_target_claimed']is False and program['query_calls']==program['idle_calls']==program['owned_or_zero_fields']==0,'honest caller scope')
 need(program['gaussian_child_profile']=={'2':336,'3':336,'5':336,'6':336},'complete paid profile')
 room=moment({25:224,2:-336,3:-336,5:-336,6:-336});gate=pow_interval(224)
 need(0<room[0]<room[1]<gate[0],'strict modular unitary exclusion')
 result={'status':'PASS_INDEPENDENT_THREE_HALF_CODED_CALLER_REVIEW','author_pins':pins,'source_pins':sourcepins,'noncommuting_3by3_instances':20,'independent_input_columns_per_instance':6,'wrong_c_orders_rejected':wrong_c,'wrong_e_orders_rejected':wrong_e,'actual_R0_codec_coefficients':n*n,'codec_counts':dict(counts),'paid_profile':program['gaussian_child_profile'],'optimistic_rank25_room':[str(x)for x in room],'one_modular_service_lower_bound':[str(x)for x in gate],'physical_route_scope':'Fresh-axis rename and exact inherited source/route identities reviewed; not a new independent replay of every signed native child.','universal_proof':'Direct ordered block elimination and four adjacent-Q reductions in REVIEW.md.','new_kappa':False,'sympy_version':s.__version__}
 out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'noncommuting_instances':20,'codec_coefficients':n*n}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=HERE.parent/'author');p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();main(a.author,a.output)
