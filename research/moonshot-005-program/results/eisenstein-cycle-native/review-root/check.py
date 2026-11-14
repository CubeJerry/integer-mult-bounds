#!/usr/bin/env python3
"""Independent full120 geometry, source and cubic-cross verifier."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='bca2056d98d0759d0c7c61104122160d13e12f099bea0cbe2de4169f9b3eac93'
def need(c,m):
 if not c:raise ValueError(m)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mm(a,b):return[[dot(r,c)for c in zip(*b)]for r in a]
def eye(n):return[[F(i==j)for j in range(n)]for i in range(n)]
def root(v):
 if v.bit_count()==3:return[2 if v>>i&1 else -1 for i in range(9)]
 need(v.bit_count()==7,'root type');z=[i for i in range(9)if not(v>>i&1)];return[3*(int(i==z[0])-int(i==z[1]))for i in range(9)]
def span(vs):
 out={0}
 for v in vs:out|={x^v for x in tuple(out)}
 return out
def add(a,b,c):
 out=a.copy()
 for j,x in b.items():
  y=out.get(j,0)+c*x
  if y:out[j]=y
  else:out.pop(j,None)
 return out
def run(package):
 raw=(package/'WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'word pin');w=json.loads(gzip.decompress(raw));sym=json.loads((package/'SYMMETRY.json').read_text())
 normals=[v for v in range(512)if v.bit_count()in(3,7)];need(normals==w['normals']and w['public']==480 and w['owned_fields']==0,'full120 interface')
 T=[47,482,62,458,59,488,213,405,341]
 def image(x):return sum(((r&x).bit_count()%2)<<i for i,r in enumerate(T))
 need(T==sym['binary_rows'],'binary T');cols=[image(1<<i)for i in range(9)]
 need(all(c.bit_count()==5 for c in cols)and all((a&b).bit_count()%2==int(i==j)for i,a in enumerate(cols)for j,b in enumerate(cols)),'orthogonal weight-five columns')
 need(all(image(image(image(x)))==x and image(image(x))^image(x)^x==(511 if x.bit_count()%2 else 0)for x in range(512)),'global cubic identity')
 need(all((image(x).bit_count()-x.bit_count())%4==0 for x in range(512)),'ordinary T commutes Fourier phase')
 pi=[normals.index(image(v))for v in normals];need(pi==w['permutation'],'all ports')
 need(all(pi[pi[pi[i]]]==i and pi[i]!=i and normals[i]^normals[pi[i]]^normals[pi[pi[i]]]==511 for i in range(120)),'forty three-cycles')
 need(all((normals[i]&normals[pi[i]]).bit_count()%2==0 for i in range(120)),'actual line/facet contact')
 # Independent nine-coordinate real construction, without author frame matrices.
 planes=((7,11),(28,44),(49,50),(127,191));E=eye(9)
 for a,b in planes:
  ra,rb=root(a),root(b);need(abs(dot(ra,rb))==9,'A2 angle')
  for v in(ra,rb):E=mm(E,[[F(i==j)-F(v[i]*v[j],9)for j in range(9)]for i in range(9)])
 need(all(dot(root(a),root(b))==0 for i,P in enumerate(planes)for Q in planes[i+1:]for a in P for b in Q),'orthogonal A2 planes')
 E2=mm(E,E);need(mm(E,[list(r)for r in zip(*E)])==eye(9),'real orthogonality')
 need(all(E2[i][j]+E[i][j]+int(i==j)==F(1,3)for i in range(9)for j in range(9)),'real minimal polynomial')
 for v in normals:
  actual=[dot(row,root(v))for row in E];desired=root(image(v));need(actual==desired or actual==[-x for x in desired],'real/binary symmetry compatibility')
 spaces=[span(f)for f in w['frames']];need(all(len(s)==2**len(f)for s,f in zip(spaces,w['frames'])),'independent frames')
 rows=[{i:1}for i in range(480)];loc=w['initial'][:];bill=Counter();ops=Counter();max_l1=1
 for e in w['program']:
  op,r=e[:2];ops[op]+=1
  if op=='MOVE':
   _,r,a,b,own=e;need(not own and loc[r]==a and spaces[a]<spaces[b],'actual public ascent');loc[r]=b;bill[len(w['frames'][b])-len(w['frames'][a])]+=1
  elif op=='ADD':
   _,r,s,c,a=e;c=int(c);need(c in(-1,1)and loc[r]==loc[s]==a and r!=s,'integer cochart ADD');rows[r]=add(rows[r],rows[s],c);max_l1=max(max_l1,sum(map(abs,rows[r].values())))
  else:raise ValueError('unexpected owner/operation')
 inv=[pi.index(i)for i in range(120)]
 for h in range(120):
  need(rows[h]=={h:1}and rows[120+h]=={120+h:1,pi[h]:1},'forward endpoint')
  need(rows[240+h]=={240+h:1,360+inv[h]:-1}and rows[360+h]=={360+h:1},'reverse endpoint')
  need(loc[h]==loc[240+h]==1 and loc[120+h]==loc[360+h]==122+h,'final charts')
 need(bill=={1:240,7:240,8:240}and ops=={'MOVE':720,'ADD':240}and max_l1==2,'complete invoice')
 for e in reversed(w['program']):
  if e[0]=='MOVE':
   _,r,a,b,own=e;need(loc[r]==b and spaces[a]<spaces[b],'inverse entrance');loc[r]=a
  else:
   _,r,s,c,a=e;need(loc[r]==loc[s]==a,'inverse cochart');rows[r]=add(rows[r],rows[s],-int(c))
 need(loc==w['initial']and all(row=={i:1}for i,row in enumerate(rows)),'inverse restores480columns')
 def nphase(h,z,p):return(z.bit_count()-(normals[h]&z).bit_count()%2-(normals[p[h]]&z).bit_count()%2)%4
 for h in range(120):
  orbit=[h,pi[h],pi[pi[h]]]
  for z in range(512):need((sum(nphase(i,z,pi)for i in orbit)-z.bit_count())%4==0,'exact cross cubic phase')
 bad=pi[:];bad[0],bad[1]=bad[1],bad[0]
 witness=next((h,z)for h in range(120)for z in range(512)if bad[bad[bad[h]]]!=h or(sum(nphase(i,z,bad)for i in(h,bad[h],bad[bad[h]]))-z.bit_count())%4)
 return{'status':'PASS_INDEPENDENT_FULL120_NATIVE_AND_CUBIC_CROSS','word_sha256':PIN,'symmetry_sha256':hashlib.sha256((package/'SYMMETRY.json').read_bytes()).hexdigest(),'real_A2_planes':planes,'binary_T_rows':T,'ports':120,'arbitrary_input_columns':480,'events':960,'moves':dict(bill),'owned':0,'integer_prefix_l1_bound':max_l1,'literal_inverse_verified':True,'character_checks':120*512,'bad_permutation_control':witness,'whole_native_cube_claimed':False,'no_new_kappa':True}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.package);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
