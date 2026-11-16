#!/usr/bin/env python3
"""Exact ordinary-module left-inverse certificates; not a bounded ordinary-word search."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,itertools,json,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());args=ap.parse_args();base=Path(__file__).parent
hp=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
assert hashlib.sha256(hp.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
sp=importlib.util.spec_from_file_location('coset_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
I=m.eye(8);units=((1,0),(0,1),(-1,0),(0,-1));P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);X={b:m.monomial([x^b for x in range(8)],[0]*8)for b in[1,2,4]};C={b:m.M((I.scale((1,1))+X[b].scale((1,-1))).a,1).norm()for b in[1,2,4]}
def comb(*pairs):
 d={}
 for g,c in pairs:d[g]=d.get(g,0)+c
 return{g:c for g,c in d.items()if c}
def mm(A,B):
 out=[[{}for _ in range(len(B[0]))]for _ in range(len(A))]
 for i,j,k in itertools.product(range(len(A)),range(len(B[0])),range(len(B))):out[i][j]=add(out[i][j],prod(A[i][k],B[k][j]))
 return out
def ordinary(M):
 return M.k==0 and all(sum(z!=(0,0)for z in row)==1 for row in M.a)and all(sum(M.a[i][j]!=(0,0)for i in range(8))==1 for j in range(8))and all(z in units for row in M.a for z in row if z!=(0,0))
def add(x,y,fac=1):
 o=dict(x)
 for g,c in y.items():o[g]=o.get(g,0)+fac*c
 return{g:c for g,c in o.items()if c}
def prod(x,y):
 o={}
 for g,c in x.items():
  for h,d in y.items():
   z=g@h;o[z]=o.get(z,0)+c*d
 return{g:c for g,c in o.items()if c}
def inverseunit(x):
 if len(x)!=1:return None
 g,c=next(iter(x.items()));return{g.star():F(1)/c}
def coset_constraints(B):
 Frows=[];cosets=[]
 for row in B:
  reps=[];cons=[]
  for j,cell in enumerate(row):
   for g,c in cell.items():
    if ordinary(g):continue
    match=None
    for i,rep in enumerate(reps):
     h=rep.star()@g
     if ordinary(h):match=(i,h);break
    if match is None:match=(len(reps),I);reps.append(g);cons.append([{}for _ in range(3)])
    i,h=match;cons[i][j]=add(cons[i][j],{h:F(c)})
  Frows.extend(cons);cosets.extend(reps)
 return Frows,cosets

def eliminate(Frows):
 rows=[[dict(x)for x in row]for row in Frows];pivotcols=[];r=0
 for c in range(3):
  pivot=next((i for i in range(r,len(rows))if inverseunit(rows[i][c])is not None),None)
  if pivot is None:continue
  rows[r],rows[pivot]=rows[pivot],rows[r];iv=inverseunit(rows[r][c]);rows[r]=[prod(iv,x)for x in rows[r]]
  for i in range(len(rows)):
   if i==r or not rows[i][c]:continue
   factor=rows[i][c];rows[i]=[add(x,prod(factor,y),-1)for x,y in zip(rows[i],rows[r])]
  pivotcols.append(c);r+=1
  if r==3:break
 nonzero=sum(any(x for x in row)for row in rows[r:]);return rows,pivotcols,nonzero

def preimage(A,targets):
 ai=A.star();ai2=ai.power(2)
 KI=[[comb((ai,1)),comb((ai,1),(ai2,-1)),{}],[{},comb((ai,-1)),comb((I,1))],[comb((ai,1)),comb((ai2,-1)),{}]]
 DD=[[comb((targets[i],1))if i==j else{}for j in range(3)]for i in range(3)]
 B=mm(mm(KI,DD),KI);FR,cos=coset_constraints(B);red,pivs,left=eliminate(FR)
 return{'constraints':len(FR),'pivots':pivs,'residual_rows':left},(B,FR,red)


def table(g):
 assert ordinary(g)
 return{'permutation':[next(i for i in range(8)if g.a[i][j]!=(0,0))for j in range(8)],'phase_mod4':[units.index(next(g.a[i][j]for i in range(8)if g.a[i][j]!=(0,0)))for j in range(8)]}
def serial(mat):return[[[{'coefficient':str(c),**table(g)}for g,c in sorted(cell.items(),key=lambda z:z[0].a)]for cell in row]for row in mat]
def left_inverse(C):
 n=len(C);aug=[[dict(x)for x in row]+[{I:F(1)}if i==j else{}for j in range(n)]for i,row in enumerate(C)];trace=[]
 for c in range(3):
  pivot=next(i for i in range(c,n)if inverseunit(aug[i][c])is not None);aug[c],aug[pivot]=aug[pivot],aug[c]
  val=aug[c][c];iv=inverseunit(val);trace.append({'column':c,'selected_row':pivot,'pivot':[{'coefficient':str(z),**table(g)}for g,z in val.items()]});aug[c]=[prod(iv,x)for x in aug[c]]
  for i in range(n):
   if i==c or not aug[i][c]:continue
   fac=aug[i][c];aug[i]=[add(x,prod(fac,y),-1)for x,y in zip(aug[i],aug[c])]
 E=[row[3:]for row in aug[:3]]
 assert mm(E,C)==[[{I:F(1)}if i==j else{}for j in range(3)]for i in range(3)]
 return E,trace
cases=[]
for mask in[128,64,112,176]:
 A=C[2]@m.monomial(list(range(8)),[2*(mask>>x&1)for x in range(8)])@P
 for name,targets in[('literal',[A.power(3),A.power(2),A.power(2)]),('canonical',[C[1]@C[2]@C[4],C[1]@C[2],C[1]@C[2]])]:
  rep,detail=preimage(A,targets);B,FR,red=detail;E,tr=left_inverse(FR)
  assert rep['pivots']==[0,1,2]
  cases.append({'mask':mask,'endpoint':name,'ordinary_coset_equations':len(FR),'constraint_matrix':serial(FR),'left_inverse':serial(E),'elimination_trace':tr})
# Sharp boundary control: K^3=diag(a²,a²,a²) has nonzero ordinary preimage e_2.
negative=[]
for mask in[128,64,112,176]:
 A=C[2]@m.monomial(list(range(8)),[2*(mask>>x&1)for x in range(8)])@P
 report,detail=preimage(A,[A.power(2)]*3);FR=detail[1]
 assert all(not row[1]for row in FR) and len(report['pivots'])<3
 negative.append({'mask':mask,'rank222_middle_has_ordinary_kernel_column':1,'unit_pivots':report['pivots']})
# Width1 must not be promoted to a faithful tensor proof: O_1 contains every matrix unit.
for x,y in itertools.product(range(8),repeat=2):
 pp=list(range(8));pp[x],pp[y]=pp[y],pp[x];swap=m.monomial(pp,[0]*8);sg=m.monomial(list(range(8)),[2*int(j==y)for j in range(8)])
 proj=m.M((I+sg.scale((-1,0))).a,1).norm();unit=swap@proj
 assert unit.k==0 and sum(z!=(0,0)for row in unit.a for z in row)==1 and unit.a[x][y]==(1,0)
(base/'CERTIFICATES.json').write_text(json.dumps(cases,indent=2)+'\n')
result={'status':'PASS_EXACT_FIXED_BOUNDARY_RIGHT_COSET_LEFT_INVERSES','cases':len(cases),'equations':[x['ordinary_coset_equations']for x in cases],'left_inverse_identity':'E C=I_3 in the exact ordinary monomial group algebra, hence every tensor phase sector','scope':'Fixed two endpoints per source; arbitrary ordinary input vector; all sufficiently large faithful widths; not arbitrary endpoint gauges','negative_controls':negative,'width1_ordinary_matrix_units':64,'new_kappa':False};(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
