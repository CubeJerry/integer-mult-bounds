import sympy as s
p=s.symbols('p',nonzero=True);ds=s.symbols('d1:4');I=s.eye(4)
def E(d,src,c):
 M=s.eye(4);M[d,src]=c;return M
def D(roles,v):
 M=s.eye(4)
 for r in roles:M[r,r]=v
 return M
B=s.Matrix([[0,0,1,0],[1,0,0,1],[0,1,1,0],[0,0,0,1]])
post=E(0,2,-1)
T2=E(2,0,-1);T3=E(3,1,-1)
H1=E(0,1,p);H2=T2.inv()*E(1,2,1/p)*T2;H3=T3.inv()*E(2,3,p)*T3
G1=D([0,1],ds[0])*H1
G2=T2.inv()*D([1,2],ds[1])*E(1,2,1/p)*T2
G3=T3.inv()*D([2,3],ds[2])*E(2,3,p)*T3
F=s.simplify(post*G3*G2*G1*B);F0=s.simplify(F.subs(dict.fromkeys(ds,1)))
print('head map',F0)
projs=[]
for d in ds:
 M=s.simplify(F.diff(d).subs(dict.fromkeys(ds,1))*F0.inv());projs.append(M)
 print('projector',d,M)
for i in range(3):
 for j in range(i):
  C=s.simplify(projs[i]*projs[j]-projs[j]*projs[i]);print('commutator',j+1,i+1,'at1rank',C.subs(p,1).rank(),'general',C)
