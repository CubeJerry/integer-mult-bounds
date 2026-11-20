"""A rank-eight physical H642 signal map from a common-annihilator-row degeneration."""
from pathlib import Path
import importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def build(repo):
 base=repo/'research/moonshot-005-program/results'
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','rank8_geometry');f,a,previous=g.context(repo)
 params=json.loads((base/'bit-coupled-native-geometric-cycle-source/component/output/PARAMETERS.json').read_text())['local']['642']
 chart,nodes,receivers,E,E2=g.geometry(f,a,params);N=previous.null_basis(E2.T,a).T
 literal=json.loads(Path(__file__).with_name('LITERAL-PROVIDER.json').read_text());m=np.array(literal['m'],dtype=np.uint8);n=np.array(literal['n'],dtype=np.uint8);p=np.array(literal['p'],dtype=np.uint8)
 need(all(m) and all(n) and all(m^n),'three nonzero coordinate weights')
 _,pc=g.rref(N,a);inv=g.inverse(N[:,pc],a);um=a.mm(m[pc][None,:],inv)[0];un=a.mm(n[pc][None,:],inv)[0]
 need(np.array_equal(a.mm(um[None,:],N)[0],m) and np.array_equal(a.mm(un[None,:],N)[0],n),'both rows belong to the quadratic annihilator')
 def basis(first):
  rows=[first]
  for row in np.eye(3,dtype=np.uint8):
   if a.rank(np.array(rows+[row],dtype=np.uint8))>len(rows):rows.append(row)
   if len(rows)==3:return np.array(rows,dtype=np.uint8)
  raise ValueError('nonzero first row')
 t=a.product[n,a.inverse[m]];B=[basis(um^un),basis(um),basis(un)]
 W=[a.mm(B[0],a.product[N,a.inverse[t^1]]),a.mm(B[1],N),a.mm(B[2],a.product[N,a.inverse[t]])]
 need(all(np.array_equal(X[0],m) for X in W) and a.rank(np.vstack(W))==7,'one common annihilator row and rank-seven stack')
 u=a.product[a.product[m,p],a.inverse[t^1]];v=a.product[a.product[m,p],a.inverse[t]]
 G=np.vstack([m,u,u^v]+[row for X in W for row in X[1:]])
 need(a.rank(G)==9,'finite normalised constraint matrix')
 Q=np.zeros((9,9),dtype=np.uint8);Q[1,[0,3]]=1;Q[2,[0,6]]=1
 for r,c in enumerate([1,2,4,5,7,8],3):Q[r,c]=1
 P=a.mm(g.inverse(G,a),Q);need(np.array_equal(P,np.array(literal['word'],dtype=np.uint8)) and a.rank(P)==8,'literal rank-eight physical provider')
 pencils={};geometric_fibres={};points={x:np.kron(a.vandermonde([nodes[x]],16),np.eye(3,dtype=np.uint8)) for x in chart.singular}
 for i,r in receivers.items():
  s=a.mm(E,np.array(r,dtype=np.uint8)[:,None])[:,0];V=a.product[s[:,None],E]
  D=[a.mm(W[0],a.product[t[:,None],V]),a.mm(W[1],a.product[t[:,None],V]),a.mm(W[2],V)]
  D[0][0]=a.mm(u[None,:],V)[0];D[1][0]=a.mm(a.product[m,p][None,:],V)[0];D[2][0]=a.mm(v[None,:],V)[0]
  need(all(np.array_equal(X,np.array(Y,dtype=np.uint8)) for X,Y in zip(D,literal['pencils'][str(i)])),'literal central pencils')
  pencils[i]=D
  xs=[x for x in chart.singular if not a.algebra.polar(x,a.masks[i])]
  K=previous.null_basis(np.vstack([points[x] for x in xs]),a)
  geometric_fibres[i]=a.product[g.power(nodes[a.masks[i]],2,a),K]
 joined=np.hstack(list(geometric_fibres.values()));_,pc=g.rref(joined,a);S=joined[:,pc];_,rr=g.rref(S.T,a);left=g.inverse(S[rr],a)
 need(S.shape==(48,18),'six-dimensional geometric core repeated three times');ann=previous.null_basis(S.T,a).T
 controls=[]
 for j in range(3):
  targets=np.hstack([pencils[i][j] for i in chart.views]);C=np.zeros((3,48),dtype=np.uint8);C[:,rr]=a.mm(targets[:,pc],left)
  C ^= a.mm(f.coefficients(f'rank8-H642-source-tail/{j}/0',(3,len(ann))),ann)
  need(all(np.array_equal(a.mm(C,K),pencils[i][j]) for i,K in geometric_fibres.items()),'complete source pencil extension');controls.append(C)
 maps={j:chart.maps(points,j,controls[s]) for s,j in enumerate(chart.donors)}
 return {'geometry':g,'family':f,'atlas':a,'previous':previous,'chart':chart,'nodes':nodes,'receivers':receivers,
  'E':E,'E2':E2,'N':N,'m':m,'n':n,'p':p,'t':t,'W':W,'u':u,'v':v,'G':G,'Q':Q,'Hword':P,
  'pencils':pencils,'fibres':geometric_fibres,'source_core':S,'maps':maps,'controls':controls}
