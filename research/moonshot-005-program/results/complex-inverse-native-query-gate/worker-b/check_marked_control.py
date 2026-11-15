#!/usr/bin/env python3
import importlib.util,sys,json
from pathlib import Path
h=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('marked_review_exact',h/'check.py');m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
i=m.eye(8);X={a:m.monomial([j^(1<<a) for j in range(8)],[0]*8) for a in range(3)};Z={a:m.monomial(list(range(8)),[2*((j>>a)&1) for j in range(8)]) for a in range(3)}
Cb=m.M((i.scale((1,1))+X[1].scale((1,-1))).a,1).norm();S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=Cb@S
def swap(a,b):return m.monomial([j^((((j>>a)^(j>>b))&1)*((1<<a)|(1<<b))) for j in range(8)],[0]*8)
def half(a):return m.M(a.a,a.k+1).norm()
assert A@Z[0]==Z[2]@A and A@Z[1]==Z[0]@A and A.power(2)@Z[1]==Z[2]@A.power(2)
rows=[]
for v in (1,2):
 av=A.tp(v);iv=m.eye(av.n);z=m.zero(av.n);ebp=half(iv+Z[1].tp(v));ebm=iv+ebp.scale((-1,0));ecp=half(iv+Z[2].tp(v));ecm=iv+ecp.scale((-1,0))
 hp=X[0].tensor(m.eye(8**(v-1)))@swap(0,1).tp(v);hh=X[2].tensor(m.eye(8**(v-1)))@swap(0,2).tp(v)
 corner=ecp@av@hp@ebp+(ecp@av.power(2)@ebm).scale((-1,0))+ecm@hh@av@ebm
 assert corner==z
 ol=m.block([[ecp,ecm@hh],[ecm,ecp@hh]]);orr=m.block([[hp@ebp,hp@ebm],[ebm,ebp]])
 assert ol@ol.star()==m.eye(2*av.n) and orr.star()@orr==m.eye(2*av.n)
 colhp=X[0].tp(v)@swap(0,1).tp(v);colh=X[2].tp(v)@swap(0,2).tp(v)
 colcorner=ecp@av@colhp@ebp+(ecp@av.power(2)@ebm).scale((-1,0))+ecm@colh@av@ebm
 assert (colcorner==z)==(v%2==1)
 rows.append({'width':v,'marked_corner_zero':True,'ordinary_boundaries_unitary':True,'collective_flip_corner_zero':v%2==1})
out={'status':'PASS_INDEPENDENT_MARKED_CONTROL','implementation':'integer Gaussian-dyadic matrices; does not import root SymPy checker','rows':rows,'phase_control':'collective flip fails at even width; marked first-column flip succeeds','new_kappa':False};(h/'MARKED-CONTROL-REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
