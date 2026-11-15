from pathlib import Path
import json
import sympy as s
z,p,j=s.symbols('z p j');out=[]
for sig in [-1,1]:
 for eps in [-1,1]:
  for e,d in [(z**2,z**3),(z**3,z**2)]:
   a=z**sig;b=a*(z**eps-1)
   f=s.rem(s.expand(z**10*((d-a)**2*(d-1)+(e-d)*(p*(d-a)*(d-1)+b*j*(d-1)+(1-p)*(d-a)**2))),z**5-1,z)
   coeff=[s.expand(f).coeff(z,k) for k in range(5)]
   A=s.Matrix([[x.coeff(p),x.coeff(j)] for x in coeff]);c=s.Matrix([x.subs({p:0,j:0}) for x in coeff])
   if A.rank()==A.row_join(c).rank():raise ValueError('obstruction not proved')
   dual=next(v for v in A.T.nullspace() if (v.T*c)[0])
   out.append({'sigma':sig,'epsilon':eps,'e':str(e),'d':str(d),'polynomial':str(f),'dual':[str(x) for x in dual],'residual':str((dual.T*c)[0])})
r={'status':'PASS_INDEPENDENT_C5_ONE_NATIVE_SPECIAL_CASE','sympy_version':s.__version__,'cases':out,'no_new_kappa':True}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(out))
