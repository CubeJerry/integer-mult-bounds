#!/usr/bin/env python3
import importlib.util,sys,json
from pathlib import Path
h=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('row_seed_exact',h/'check.py');m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
i=m.eye(8);xb=m.monomial([j^2 for j in range(8)],[0]*8);cb=m.M((i.scale((1,1))+xb.scale((1,-1))).a,1).norm();S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=cb@S;P=m.monomial(list(range(8)),[(j>>2)&1 for j in range(8)])
G=A.power(-2);H=A.star()@P@A.star();K=G.star()@H;J=G@K.star()
assert K==A@P@A.star() and J==A.star()@P.star()@A.star()
assert [m.gaussian_rank(x) for x in (G,H,K,J)]==[2,2,1,2]
rows=[]
for v in (1,2):
 a=A.tp(v);iv=m.eye(a.n);z=m.zero(a.n);p=P.tp(v);g=G.tp(v);hh=H.tp(v)
 L=m.block([[a.star(),iv],[z,a.star()]]);D=m.block([[iv,p],[z,iv]]);Q=m.diagonal([a.star(),iv])
 assert Q@D@L==m.block([[g,a.star()+hh],[z,a.star()]])
 rows.append({'width':v,'exact_seed_word':True,'ranks_per_column':[m.gaussian_rank(x.tp(v))//v for x in (G,H,K,J)]})
assert G.star()@G==i
out={'status':'PASS_EXACT_ROW_SEED','widths':rows,'negative_control':'P=I has ordinary relative identity and row factorization G(I,I)','scope':'finite coefficient controls, universal source/preimage arguments separate','new_kappa':False};(h/'ROW-SEED-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
