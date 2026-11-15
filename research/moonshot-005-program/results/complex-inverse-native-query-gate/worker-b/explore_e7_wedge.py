import itertools,json
from pathlib import Path
import sympy as S
pts=list(range(1,8))
par=lambda n:n.bit_count()%2
roots=[];xs=[]
for a in pts:
 v=[0]*7;v[a-1]=2;roots.append(tuple(v));xs.append(0)
for x in pts:
 support=[a-1 for a in pts if par(x&a)]
 for bits in itertools.product((1,-1),repeat=3):
  v=[0]*7;v[support[0]]=1
  for j,b in zip(support[1:],bits):v[j]=b
  roots.append(tuple(v));xs.append(x)
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
comm=lambda a,b:int(abs(dot(a,b))==2)
options=[[r for r,x in zip(roots,xs) if x==1<<i] for i in range(3)]
chosen=None;labels=None
for pp in itertools.product(*options):
 if any(comm(pp[i],pp[j]) for i in range(3) for j in range(i)):continue
 zz=[sum(comm(r,p)<<i for i,p in enumerate(pp)) for r in roots]
 ll=[x|(z<<3) for x,z in zip(xs,zz)]
 if len(set(ll))<63:continue
 if all(comm(a,b)==(par((la&7)&(lb>>3))^par((la>>3)&(lb&7))) for a,la in zip(roots,ll) for b,lb in zip(roots,ll)):
  chosen=pp;labels=ll;break
assert chosen is not None
print('chosen',chosen,flush=True)
lookup={r:i for i,r in enumerate(roots)}
def canon(v):
 v=tuple(v)
 return tuple(-x for x in v) if next(x for x in v if x)<0 else v
reflection_controls=0
for v,lv in zip(roots,labels):
 R=S.Matrix(7,7,lambda i,j:(v[i]*v[j])/S.Integer(2)-(1 if i==j else 0))
 assert R.T*R==S.eye(7) and R.det()==1
 for w,lw in zip(roots,labels):
  z=canon(R*S.Matrix(w));actual=labels[lookup[z]]
  c=par((lv&7)&(lw>>3))^par((lv>>3)&(lw&7))
  assert actual==(lw^(lv if c else 0));reflection_controls+=1
triples=list(itertools.combinations(range(7),3))
line=[(pts[a]^pts[b]^pts[c])==0 for a,b,c in triples]
P=S.diag(*[1 if b else -1 for b in line])
g=S.eye(7);ranks=[]
for r in range(4):
 if r:
  v=chosen[r-1];g=S.Matrix(7,7,lambda i,j:v[i]*v[j]/S.Integer(2)-(1 if i==j else 0))*g
 W=S.Matrix(len(triples),len(triples),lambda i,j:g.extract(triples[i],triples[j]).det())
 ranks.append((W-P*W*P).rank())
 print('r',r,'rank',ranks[-1],flush=True)
out={'representation':'third exterior power of exact seven-dimensional root model','roots':63,'root_transvection_controls':reflection_controls,'chosen_isotropic_complement':[list(v) for v in chosen],'line_subspace_dimension':sum(line),'ranks':ranks,'query_target_32_margin':ranks[3]+ranks[2]-4*ranks[1]}
Path(__file__).with_name('E7-WEDGE-EXPLORATION.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
