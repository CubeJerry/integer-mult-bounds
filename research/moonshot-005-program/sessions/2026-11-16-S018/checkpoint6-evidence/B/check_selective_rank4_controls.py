#!/usr/bin/env python3
"""Literal source, cheap CNOT pullback and explicit rank-four gauges."""
from pathlib import Path
import argparse,itertools,json,hashlib
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();tidy=lambda M:M.applyfunc(s.expand);I=s.eye(16);P=s.zeros(16);Xb=s.zeros(16);sign=s.eye(16)
 for x in range(16):P[(x>>1)|((x&1)<<3),x]=1;Xb[x^2,x]=1;sign[x,x]=-1 if(x&13)==13 else 1
 A=tidy(((1+s.I)*I+(1-s.I)*Xb)*sign*P/2);A2=tidy(A*A);A3=tidy(A2*A)
 Rt=json.loads(Path(__file__).with_name('SQUARE-NORMALIZER-INDEPENDENT-REVIEW.json').read_text())['independent_R2_table'];R=s.zeros(16)
 for j,(i,e)in enumerate(Rt):R[i,j]=s.I**e
 roots=[1,s.I,-1,-s.I]
 def phase(z):return roots.index(s.expand(z))
 def table(M):return [(next(i for i in range(16)if M[i,j]!=0),phase(next(M[i,j]for i in range(16)if M[i,j]!=0)))for j in range(16)]
 C=s.Matrix(16,16,lambda i,j:-s.Rational(1,4)*(-s.I)**((int(i)^int(j)).bit_count()))
 def rank4_gauges(G):
  es=[[phase(4*G[i,j])for j in range(16)]for i in range(16)];rp=[es[i][0]for i in range(16)];cp=[(es[0][j]-es[0][0])%4 for j in range(16)];rows=[]
  for i in range(16):
   dd=[(es[i][j]-rp[i]-cp[j])%4 for j in range(16)]
   if any(x not in (0,2)for x in dd):return None
   rows.append(sum((x//2)<<j for j,x in enumerate(dd)))
  if len(set(rows))!=16 or any((x^y)not in rows for x,y in itertools.product(rows,repeat=2)):return None
  basis=[];span={0:0}
  for x in rows:
   if x not in span:
    bit=1<<len(basis);basis.append(x);span.update({y^x:code|bit for y,code in list(span.items())})
  assert len(basis)==4 and len(span)==16
  rid=[span[x]for x in rows];cid=[sum(((basis[k]>>j)&1)<<k for k in range(4))for j in range(16)];assert sorted(cid)==list(range(16))
  L=s.zeros(16);T=s.zeros(16)
  for i in range(16):L[i,rid[i]]=s.I**((2+rp[i]+rid[i].bit_count())%4)
  for j in range(16):T[cid[j],j]=s.I**((cp[j]+cid[j].bit_count())%4)
  assert tidy(L*C*T)==G
  return {'left':table(L),'right':table(T)}
 def gauges_even(G,rank):
  size=1<<rank;scale=1<<(rank//2);groups={}
  for row in range(16):groups.setdefault(tuple(j for j in range(16)if G[row,j]!=0),[]).append(row)
  assert len(groups)==16//size and all(len(cols)==len(rows)==size for cols,rows in groups.items())
  L=s.zeros(16);T=s.zeros(16);target=s.zeros(16)
  for block,(cols,rows)in enumerate(sorted(groups.items())):
   es=[[phase(scale*G[i,j])for j in cols]for i in rows];rp=[es[i][0]for i in range(size)];cp=[(es[0][j]-es[0][0])%4 for j in range(size)];masks=[]
   for i in range(size):
    dd=[(es[i][j]-rp[i]-cp[j])%4 for j in range(size)];assert all(z in(0,2)for z in dd);masks.append(sum((z//2)<<j for j,z in enumerate(dd)))
   basis=[];span={0:0}
   for z in masks:
    if z not in span:
     bit=1<<len(basis);basis.append(z);span.update({v^z:k|bit for v,k in list(span.items())})
   assert len(basis)==rank and set(masks)==set(span)
   rid=[span[z]for z in masks];cid=[sum(((basis[k]>>j)&1)<<k for k in range(rank))for j in range(size)];assert sorted(cid)==list(range(size))
   for i,row in enumerate(rows):L[row,block*size+rid[i]]=s.I**((rp[i]-rank//2+rid[i].bit_count())%4)
   for j,col in enumerate(cols):T[block*size+cid[j],col]=s.I**((cp[j]+cid[j].bit_count())%4)
   for i,j in itertools.product(range(size),repeat=2):target[block*size+i,block*size+j]=s.I**((rank//2-(i^j).bit_count())%4)/scale
  assert tidy(L*target*T)==G
  return {'left':table(L),'right':table(T),'canonical_rank':rank}
 active_swap=s.zeros(16)
 for x in range(16):active_swap[((x&1)<<1)|((x&2)>>1)|(x&12),x]=1
 J=tidy(R.conjugate().T*active_swap*R);cheapJ=s.zeros(16)
 for x in range(16):
  aa,bb,cc,dd=[(x>>j)&1 for j in range(4)];cheapJ[aa+2*bb+4*(dd^(aa*bb))+8*(cc^(aa*bb)),x]=1
 assert J==cheapJ and tidy(J*J)==I
 checks=[];Qm=[];perms=[(0,)+pm for pm in itertools.permutations((1,2,3))];expected=[(4,2),(4,4),(2,4),(4,4),(2,4),(4,2)]
 for sigma,ex in zip(perms,expected):
  B=s.zeros(16)
  for x in range(16):B[(x&3)+4*sigma[x>>2],x]=1
  Q=tidy(R.conjugate().T*B*R);Qm.append(Q);assert tidy(A2*Q)==tidy(B*A2)
  even=tidy(A3*Q*A);odd=tidy(A*J*A2*Q*A);rec={'sigma':sigma,'Q_table':table(Q),'even_first_rank':ex[0],'J_first_rank':ex[1],'even_gauges':gauges_even(even,ex[0]),'J_gauges':gauges_even(odd,ex[1])};checks.append(rec)
 for i,j in itertools.product(range(6),repeat=2):
  comp=tuple(perms[i][perms[j][k]]for k in range(4));assert tidy(Qm[i]*Qm[j])==Qm[perms.index(comp)]
 assert Qm[perms.index((0,2,1,3))]==active_swap
 rev=s.zeros(16)
 for x in range(16):
  aa,bb,cc,dd=[(x>>j)&1 for j in range(4)];rev[(aa^bb)+2*bb+4*(cc^bb)+8*dd,x]=s.I**(bb*(1+2*cc+2*dd))
 assert rev==Qm[perms.index((0,1,3,2))]and tidy(rev*rev)==I
 result={'status':'PASS_AUTHOR_SELECTIVE_RANK4_CONTROLS','scope':'All six actual GL2 spectator pullbacks, exact twelve Gaussian endpoint gauges and monomial recipes tensor to every positive width. These are rank4 source controls, not a three-bank421 caller.','controls':checks,'actual_S3_multiplication_table':True,'J_table':table(J),'generator_recipes_per_direction':{'J':{'coordinate_SWAP':1,'Toffoli':2,'phase_pass':0},'spectator_SWAP':{'coordinate_SWAP':1,'phase_pass':0},'reverse_CNOT':{'CNOT':2,'input_Z4_phase_pass':1}},'ordinary_inverse_and_prefix_norm':1,'generic_endpoint_monomial_recipe_bound':{'three_control_edges':105,'negative_control_X':630,'phase_pass':1},'source_R2_pin':hashlib.sha256(Path(__file__).with_name('SQUARE-NORMALIZER-INDEPENDENT-REVIEW.json').read_bytes()).hexdigest()}
 o.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
