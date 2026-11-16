"""Discovery: exact projective-word rank filter with nonlinear ordinary gauges."""
from pathlib import Path
import importlib.util,sys,itertools,json,random,time
from functools import lru_cache
repo=Path('/workspace/scratch/6e036830f982/programme');hp=repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py';sp=importlib.util.spec_from_file_location('nc_search_exact',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
I=m.eye(8);X={b:m.monomial([j^b for j in range(8)],[0]*8)for b in(1,2,4)};C={b:m.M((I.scale((1,1))+X[b].scale((1,-1))).a,1).norm()for b in(1,2,4)}
P=m.monomial([0,4,1,5,2,6,3,7],[0]*8);D=m.monomial(list(range(8)),[0]*7+[2]);A=C[2]@D@P
units=((1,0),(0,1),(-1,0),(0,-1))
@lru_cache(None)
def mul(a,b):return a@b
@lru_cache(None)
def canon(g):
 vals=[g.scale(u)for u in units];j=min(range(4),key=lambda j:vals[j].a);return vals[j],(-j)%4
@lru_cache(None)
def kind(g):
 groups={}
 for i,row in enumerate(g.a):
  supp=tuple(j for j,z in enumerate(row)if z!=(0,0));groups.setdefault(supp,[]).append(i)
 sizes={len(s)for s in groups}
 if len(sizes)!=1:return -1
 sz=next(iter(sizes));r=sz.bit_length()-1
 if sz!=2**r or len(groups)!=8//sz or any(len(s)!=len(rows)for s,rows in groups.items()):return -1
 if any(len(set(s)&set(t))for s,t in itertools.combinations(groups,2)):return -1
 target=I
 for b in range(r):target=target@C[1<<b]
 if g.k!=target.k:return -1
 mags={z[0]*z[0]+z[1]*z[1]for row in g.a for z in row if z!=(0,0)}
 expmags={z[0]*z[0]+z[1]*z[1]for row in target.a for z in row if z!=(0,0)}
 if mags!=expmags:return -1
 for cols,rows in groups.items():
  x0,y0=rows[0],cols[0];d=[]
  for x in rows:
   mask=0
   for j,y in enumerate(cols):
    num=m.gm(g.a[x][y],g.a[x0][y0]);den=m.gm(g.a[x][y0],g.a[x0][y])
    if num==den:pass
    elif num==tuple(-z for z in den):mask|=1<<j
    else:return -1
   d.append(mask)
  span={0};nb=0
  for z in d:
   if z not in span:span|={x^z for x in list(span)};nb+=1
  if nb!=r or set(d)!=span:return -1
 return r

def comb(*pairs):
 d={}
 for g,c in pairs:d[g]=d.get(g,0)+c
 return{g:c for g,c in d.items()if c}
def mm(X,Y):
 out=[[{}for _ in range(3)]for _ in range(3)]
 for i,j,k in itertools.product(range(3),repeat=3):
  for a,c in X[i][k].items():
   for b,e in Y[k][j].items():
    g=mul(a,b);out[i][j][g]=out[i][j].get(g,0)+c*e
 return[[{g:c for g,c in z.items()if c}for z in row]for row in out]
K=[[comb((I,1)),{},comb((A,1),(I,-1))],[comb((A,1)),{},comb((A,-1))],[comb((I,1)),comb((I,1)),comb((I,-1))]]
p=1000003

def null(rows,n):
 piv={}
 for row in rows:
  row=[x%p for x in row]
  for i in sorted(piv):
   x=row[i]
   if x:row=[(a-x*b)%p for a,b in zip(row,piv[i])]
  j=next((j for j,x in enumerate(row)if x),None)
  if j is None:continue
  z=pow(row[j],-1,p);row=[x*z%p for x in row]
  for i,old in list(piv.items()):
   x=old[j]
   if x:piv[i]=[(a-x*b)%p for a,b in zip(old,row)]
  piv[j]=row
  if len(piv)==n:return []
 out=[]
 for j in range(n):
  if j in piv:continue
  v=[0]*n;v[j]=1
  for i,r in piv.items():v[i]=-r[j]%p
  out.append(v)
 return out

def det(a):return(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))%p

def constraints(B,HS):
 nvar=9*len(HS);out={}
 for r,c,i,j,e in itertools.product(range(3),range(3),range(3),range(3),range(len(HS))):
  idx=(i*3+j)*len(HS)+e
  for a,x in B[r][i].items():
   for b,y in K[j][c].items():
    g,phase=canon(mul(mul(a,HS[e]),b));key=(r,c,g)
    if key not in out:out[key]=[0]*nvar
    out[key][idx]+=x*y # Necessary width0mod4 filter; exact phases kept in input keys.
 return out

if __name__=='__main__':
 start=time.time();rng=random.Random(20261115);count={};candidates=[];scopes=0
 for mask in range(1,128):
  h=m.monomial(list(range(8)),[0]+[2*((mask>>(j-1))&1)for j in range(1,8)]);k=A.star()@h@A
  assert kind(k)==0 and k.power(2)==I
  for u,v in itertools.combinations(range(3),2):
   Q=[[comb((I,2))if i==j else{}for j in range(3)]for i in range(3)];Q[u][u]=Q[v][v]=comb((I,1),(h,1));Q[u][v]=Q[v][u]=comb((I,1),(h,-1))
   B=mm(mm(K,Q),K);rows=constraints(B,[I,k])
   for rr in itertools.product((2,3),repeat=3):
    if sum(rr)<=6:continue
    mat=[row for (r,c,g),row in rows.items()if kind(g)!=rr[r]];ns=null(mat,18);scopes+=1;count[len(ns)]=count.get(len(ns),0)+1
    if not ns:continue
    for trial in range(8):
     co=[rng.randrange(p)for _ in ns];vec=[sum(z*u[j]for z,u in zip(co,ns))%p for j in range(18)]
     if all(det([[sum((sgn**e)*vec[(i*3+j)*2+e]for e in range(2))%p for j in range(3)]for i in range(3)])for sgn in(1,-1)):
      candidate={'mask':mask,'pair':[u,v],'ranks':rr,'null_dim':len(ns),'vector':vec};candidates.append(candidate);print('CANDIDATE',candidate,flush=True);break
  if mask%8==0:print('progress',mask,'scopes',scopes,'nulls',count,'candidates',len(candidates),'secs',round(time.time()-start,2),flush=True)
 result={'scope':'finite exact projective-word filter at width0mod4 followed by modular necessary constraints; not a proof','scopes':scopes,'null_counts':count,'candidates':candidates,'seconds':time.time()-start}
 Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print('DONE',result,flush=True)
