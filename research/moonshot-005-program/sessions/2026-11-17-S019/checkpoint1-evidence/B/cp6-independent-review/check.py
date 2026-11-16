#!/usr/bin/env python3
"""Independent literal reconstruction; no S018 B or R executable imports."""
from pathlib import Path
import importlib.util,sys,json,hashlib,argparse
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--evidence',type=Path);ap.add_argument('--out',type=Path);args=ap.parse_args()
ROOT=args.repo.resolve()
OLD=args.evidence.resolve() if args.evidence else ROOT/'research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint6-evidence'
engine=ROOT/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
spec=importlib.util.spec_from_file_location('retained_gaussian_arithmetic',engine);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
I=m.eye(16);Z=m.zero(16)
def minus(X):return X.scale((-1,0))
def half(X):return m.M(X.a,X.k+1).norm()
def table(dest,phase):return m.monomial([dest(*[(x>>j)&1 for j in range(4)]) for x in range(16)],[phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
rot=table(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
X=m.monomial([x^2 for x in range(16)],[0]*16)
A=half(I.scale((1,1))+X.scale((1,-1)))@rot
F=table(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*a)
S=table(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
R2=table(lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
J=R2.star()@S@R2
H=A.power(-2)@F@A.power(2);Fh=A@F@A.star();Fb=A.star()@H@A
Kd=A@J@A.power(2)@S@A.power(-3)
Ktable=table(lambda a,b,c,d:a+2*(b^(a*d))+4*(c^(a*d))+8*d,lambda a,b,c,d:2*a*d)
assert Kd==Ktable
for x in (F,H,Fh,Fb,J,S,Kd):assert x@x==I
assert Kd@Fh==Fh@Kd and J@F==F@J and S@H==H@S
B2=A.power(3)@S@A
assert A@J@A.power(3)==Kd@B2
assert B2@Fb==Fh@B2 and A.power(4)@Fb==Fh@A.power(4)
# Multiplicative source identities tensor exactly. Apply projectors afterward.
def route(G):
 p=half(I+G);n=half(I+minus(G))
 return m.block([[n,p,Z],[p,n,Z],[Z,Z,I]])
Cp=m.diagonal([I,J,I])@route(F)
Qp=m.diagonal([I,S,I])@route(H)@m.diagonal([I,S.star(),I])
O=route(Fh)@m.diagonal([I,Kd.star(),I])
Rp=route(Fb)
P=half(I+F);Pm=half(I+minus(F))
K=m.block([[A@Pm@A,Z,Z],[A@J@P@A,Z,Z],[Z,Z,Z]])
assert K.star()@K==m.diagonal([I,Z,Z])
OK=O@K
assert all(z==m.Z for row in OK.a[16:] for z in row)
Pi=O.star()@m.diagonal([I,Z,Z])@O
assert Pi@Pi==Pi and Pi@K==K
# Direct quartic prefix: first column of C and middle row of Q.
def quartic(Q):
 q10=m.M(tuple(tuple(Q.a[16+i][j]for j in range(16))for i in range(16)),Q.k).norm()
 q11=m.M(tuple(tuple(Q.a[16+i][16+j]for j in range(16))for i in range(16)),Q.k).norm()
 q12=m.M(tuple(tuple(Q.a[16+i][32+j]for j in range(16))for i in range(16)),Q.k).norm()
 left=[A@Pm@A@A,A@J@P@A@A,Z]
 right=[q10@A,q11@A,q12]
 return m.block([[minus(x@y)for y in right]for x in left])
t4=quartic(Qp);exp=m.block([[Z,minus(A.power(4)),Z],[Z,Z,Z],[Z,Z,Z]])
assert O@t4@Rp==exp
Qi=m.diagonal([I,S,I])@route(H.scale((0,1)))@m.diagonal([I,S.star(),I])
Tinv=I+Fb.scale((0,-1));Uinv=I+Fb.scale((0,1));Ri=m.diagonal([Tinv,Uinv,I])@route(Fb)
assert O@quartic(Qi)@Ri==m.block([[minus(B2),minus(A.power(4)),Z],[Z,Z,Z],[Z,Z,Z]])
# Ordinary rank-D projector does not by itself mean free one-bank module.
# Abstract O=Q x Q, Pi=diag(e+,e+,0) has physical rankD for balanced reps,
# but component ranks(2,0) differ from one-bank(1,1).
module_counterexample={'coefficient_algebra':'Q x Q','rank_one_bank_by_simple_component':[1,1],'rank_Pi_by_simple_component':[2,0],'balanced_representation_physical_rank_matches':True}
# External-i parity distinction in the +1 involution sector.
assert (1+1j)/2 !=0 and (1+(1j)**2)/2==0
files=[OLD/'B/PURE-PREFIX-IMAGE-GATE-v3.md',OLD/'B/INVERSE-CUT-SUPPORT-GATE-v2.md',OLD/'B/ALIGNED-SELECTIVE-COMPONENT-v1.md',OLD/'B/RESIDUE-SELECTIVE-COMPONENT-v1.md',OLD/'B/FINAL-COST-SCOPE.md',OLD/'R/pure-prefix-review/REVIEW.md',OLD/'R/pure-prefix-review/RESULT.json',OLD/'R/residue-review/REVIEW.md',OLD/'R/residue-review/RESULT.json',engine]
result={'status':'PASS_INDEPENDENT_CP6_COMPLEX_LOGIC_AND_LITERAL_CONTROLS','source_byte_sha256':{('cp6/'+str(p.relative_to(OLD)) if p.is_relative_to(OLD) else str(p.relative_to(ROOT))):hashlib.sha256(p.read_bytes()).hexdigest()for p in files},'literal_identities':12,'all_width_reason':'Tensor only exact multiplicative identities; then use collective involution algebra with exterior scalars. Fixed-catalogue gate rests on proof, not this finite control.','positive_scope':'Exact aligned quartic and residue components only; no421 caller','wording_note':module_counterexample,'source_and_coefficients':'Exact bounded Gaussian integers/dyadic denominator arithmetic; no cp6 author or root executable imports','not_replayed':'Existing full ordinary primitive invoice counts/negative controls remain independently reviewed cp6 receipts; not claimed freshly replayed here.'}
(args.out or Path(__file__).with_name('RESULT.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
