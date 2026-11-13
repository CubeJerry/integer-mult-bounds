"""Symbolic affine identities and independent small-family corroboration.
No matching solver, predecessor checker or current C search is imported.
Apache-2.0; prepared with substantial OpenAI Codex assistance.
"""
from itertools import permutations, product
from pathlib import Path
import json, argparse

H=((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))
def need(ok,message):
 if not ok:raise ValueError(message)
def dot(v,w):return sum(a*b for a,b in zip(v,w))
def image2(x):return tuple(dot(row,x) for row in H)
def norm2(x):return dot(x,x)
def error4(x,y):return sum((2*b-a)**2 for a,b in zip(image2(x),y))
def orbit(v):
 return {tuple(s[i]*p[i] for i in range(4)) for p in permutations(v)
         for s in product((-1,1),repeat=4) if s[0]*s[1]*s[2]*s[3]==1}
def nearest(x):
 h=image2(x);need(len({v%2 for v in h})==1,'Hadamard parity')
 if h[0]%2:return set(product(*[(v//2,v//2+1) for v in h]))
 b=tuple(v//2 for v in h);out={b}
 for i in range(4):
  for sign in (-1,1):out.add(tuple(v+sign*(i==j) for j,v in enumerate(b)))
 return out
def z_allowed(m,R0,R1):
 # sqrt(m)-sqrt(R1)<sqrt(R1)-sqrt(R0), sign-aware exact squaring.
 d=4*R1-m-R0
 return d>0 and 4*m*R0<d*d

# Affine coordinate (slope,constant); identities hold as polynomials in a.
Z=((1,1),(1,0),(1,0),(1,0))
X=((2,0),(0,1),(0,1),(0,1))
Y=((1,2),(1,0),(1,-1),(1,-1))
def affine_image(v):return tuple(tuple(sum(row[i]*v[i][j] for i in range(4)) for j in (0,1)) for row in H)
def norm_poly(v):return (sum(s*s for s,c in v),2*sum(s*c for s,c in v),sum(c*c for s,c in v))
def affine_error4(v,w):
 hv=affine_image(v)
 return norm_poly(tuple(tuple(2*w[i][j]-hv[i][j] for j in (0,1)) for i in range(4)))
def evaluate(v,a):return tuple(s*a+c for s,c in v)
def multiply(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)) for i in range(4))

def verify():
 need(multiply(H,H)==tuple(tuple(4*(i==j) for j in range(4)) for i in range(4)),'orthogonality')
 need(tuple(map(sum,zip(*H)))==(4,0,0,0),'D4 image sum')
 need(norm_poly(Z)==(4,2,1) and norm_poly(X)==(4,0,3) and norm_poly(Y)==(4,0,6),'symbolic norm identities')
 need(affine_error4(Z,X)==(0,0,4) and affine_error4(X,Y)==(0,0,4),'symbolic error-one identities')
 # Independent generator check corroborates the root-reflection proof.
 generators=[]
 for k in range(3):
  p=list(range(4));p[k],p[k+1]=p[k+1],p[k]
  generators.append(tuple(tuple(int(p[i]==j) for j in range(4)) for i in range(4)))
 generators.append(tuple(tuple((-1 if i<2 else 1)*(i==j) for j in range(4)) for i in range(4)))
 for A in generators:
  n=multiply(multiply(H,A),H);need(all(t%4==0 for row in n for t in row),'conjugate integrality')
  B=tuple(tuple(t//4 for t in row) for row in n)
  need(all(sum(t*t for t in row)==1 for row in B),'signed permutation rows')
  need(all(sum(B[i][j]**2 for i in range(4))==1 for j in range(4)),'signed permutation columns')
  signs=[next(t for t in row if t) for row in B]
  need(signs[0]*signs[1]*signs[2]*signs[3]==1,'even signs')
 records=[]
 for a in range(2,65):
  z=evaluate(Z,a);x=evaluate(X,a);y=evaluate(Y,a);R0=4*a*a+3;R1=4*a*a+2*a+1
  need(error4(z,x)==4 and error4(x,y)==4,'actual affine edge')
  Zs=orbit(z);Xs=orbit(x);Ys=orbit(y)
  need((len(Zs),len(Xs),len(Ys))==(32,32,96),'symbolic orbit counts')
  union=set();edges=0
  for point in Zs:
   ns=nearest(point);need(len(ns)==16 and all(error4(point,q)==4 for q in ns),'half-image completeness')
   allowed={q for q in ns if z_allowed(norm2(q),R0,R1)}
   need(len(allowed)==8,'eight strict Z corners');union.update(allowed);edges+=len(allowed)
  patterns={(tuple(sorted(map(abs,q))),0 if 0 in q else (1 if q[0]*q[1]*q[2]*q[3]>0 else -1)) for q in union}
  expected={((0,0,0,2*a),0),((0,0,1,2*a),0),((0,1,1,2*a),0),((1,1,1,2*a),1)}
  need(patterns==expected and len(union)==184 and Xs<=union,'complete Z neighborhood union')
  hits={q:0 for q in Ys}
  for point in Xs:
   candidates=nearest(point)&Ys;need(len(candidates)==3,'three Y corners per X')
   for q in candidates:hits[q]+=1
  need(set(hits.values())=={1},'each Y has one X neighbor')
  need(norm2(y)-norm2(x)==3 and norm2(z)-norm2(y)==2*a-5,'escape shell identities')
  need((norm2(y)<R1)==(a>=3),'strict beta escape threshold')
  if a in (2,3,4,8,16,64):records.append({'a':a,'R0':R0,'R1':R1,'Y_norm2':norm2(y),
    'Z_size':len(Zs),'Z_strict_edges':edges,'Z_union':len(union),'forced_X':len(Xs),
    'Y_shell':len(Ys),'strict_beta_escape':norm2(y)<R1})
 need(len(nearest((0,0,0,0)))==9,'integer-image nine candidates')
 need(norm2(evaluate(Y,2))>norm2(evaluate(Z,2)),'a2 negative control')
 wrong=list(evaluate(Y,3));wrong[0]+=1
 need(error4(evaluate(X,3),wrong)>4,'wrong neighbor control')
 need(affine_error4(Z,X)[2]==4,'strict-error-cap control')
 return {'marker':'PASS_PARAMETRIC_HALL_BOUNDARY_OBSTRUCTION','symbolic_identities':'Norms and both error-one edges checked as polynomial identities, not inferred from samples.',
  'corroborated_a_range':[2,64],'records':records,'generator_conjugations':4,
  'controls':['a2 second edge is not strict beta2','wrong upper neighbor exceeds error cap','both edges require inclusive error cap1','half-image neighborhood has16 corners, integer-image has9'],
  'scope':'No N subset B_(4a^2+3) satisfies N_beta_a(N union Z_a) subset N when a>=3; no general Hall or global1/2 impossibility claim.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args();r=verify()
 dest=Path(__file__).with_name('RESULT.json')
 if args.write:dest.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 else:need(json.loads(dest.read_text())==r,'receipt drift')
 print('PASS_PARAMETRIC_HALL_BOUNDARY_OBSTRUCTION: exact two-step escape; a>=3 ball-core containment impossible.')
