#!/usr/bin/env python3
import argparse, hashlib, itertools, json
from pathlib import Path
import sympy as s

base=Path(__file__).parent
ap=argparse.ArgumentParser()
ap.add_argument('--proof',type=Path,default=base.parents[1]/'root/two-interstage-reduction/PROOF.md')
ap.add_argument('--out',type=Path,default=base/'RESULT.json')
ar=ap.parse_args()
source=ar.proof
assert hashlib.sha256(source.read_bytes()).hexdigest()=='6ac2c14721f0e43a24c88281cb9ae0683c6d4c2ed8176614645f569ac1fc77a4'
chars=list(itertools.product((1,-1),repeat=2))
t=s.symbols('t')
# R=I+t*x*e12+t*y*e23 is an ordinary triangular unit at every character.
blocks=[]
for x,y in chars:
    R=s.Matrix([[1,t*x,0],[0,1,t*y],[0,0,1]])
    assert R.det()==1
    Ri=s.Matrix([[1,-t*x,t*t*x*y],[0,1,-t*y],[0,0,1]])
    assert R*Ri==s.eye(3) and Ri*R==s.eye(3)
    blocks.append((R,Ri))
# Fourier inversion reconstructs the coefficient of each group element.
coeff=[]
for i,j in itertools.product((0,1),repeat=2):
    coeff.append(s.simplify(sum((x**i*y**j*Ri for (x,y),(_,Ri) in zip(chars,blocks)),s.zeros(3))/4))
assert coeff[0]==s.eye(3)
assert coeff[1]==s.Matrix([[0,0,0],[0,0,-t],[0,0,0]])
assert coeff[2]==s.Matrix([[0,-t,0],[0,0,0],[0,0,0]])
assert coeff[3]==s.Matrix([[0,0,t*t],[0,0,0],[0,0,0]])
u,v=s.symbols('u v')
for x,y in chars:
    bad=s.Matrix([[u,v*x,0],[v*y,u,0],[0,0,0]])
    assert bad.det()==0
out={'status':'PASS_INDEPENDENT_ABELIAN_UNIT_CRITERION_CONTROLS',
     'reviewed_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'characters':len(chars),'positive_symbolic_unit':True,
     'inverse_fourier_reconstruction':True,'identically_singular_negative_control':True,
     'scope':'Diagnostic examples plus independent written proof review; no multiplication caller or new kappa.'}
ar.out.parent.mkdir(parents=True,exist_ok=True)
ar.out.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
