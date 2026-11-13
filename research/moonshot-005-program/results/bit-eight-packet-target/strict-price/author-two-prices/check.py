"""Exact nearby covered-exponent budgets via directed rational log/exp."""
import argparse,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit("Exact checks require Python without -O")
def integer_root(n,k):
 v=1<<((n.bit_length()+k-1)//k)
 while True:
  z=((k-1)*v+n//v**(k-1))//k
  if z>=v:break
  v=z
 while (v+1)**k<=n:v+=1
 while v**k>n:v-=1
 assert v**k<=n<(v+1)**k
 return v
def log_bounds(r,n=36):
 if r==1:return F(0),F(0)
 k=r.bit_length()-1;v=F(r,1<<k)
 def partial(z):
  s=sum((2*z**(2*j+1)/F(2*j+1) for j in range(n)),F(0));tail=2*z**(2*n+1)/F(2*n+1)/(1-z*z);return s,s+tail
 a,b=partial(F(1,3));c,d=partial((v-1)/(v+1));return k*a+c,k*b+d

def exp_negative_bounds(lo,hi):
 assert 0<=lo<=hi<1
 def poly(x,n):return sum(((-x)**j/F(math.factorial(j)) for j in range(n+1)),F(0))
 return poly(hi,5),poly(lo,4)
def main(a):
 raw=a.base_result.read_bytes();assert hashlib.sha256(raw).hexdigest()=='f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2';b=json.loads(raw)
 N,H,P2,T2=[{int(k):v for k,v in b[name].items()} for name in ['native_paid','helper_target','paired_paid','paired_target']];ranks=set(N)|set(H)|set(P2)|set(T2)|{1};grid=10**36;base={}
 for r in ranks:
  target=r**199*grid**200;z=integer_root(target,200);base[r]=(F(z,grid),F(z+int(z**200!=target),grid))
 critical=F(3112961,621875000);cases={'C0050001':F(50001,10**7),'one_stage_above_threshold':critical+F(1,10**10)};outcases={}
 for tag,C in cases.items():
  eps=C-F(1,200);assert eps>0;pw={}
  for r in ranks:
   l,u=log_bounds(r);el,eu=exp_negative_bounds(eps*l,eps*u);pl,pu=base[r][0]*el,base[r][1]*eu;qgrid=10**30
   pw[r]=(F(pl.numerator*qgrid//pl.denominator,qgrid),F((pu.numerator*qgrid+pu.denominator-1)//pu.denominator,qgrid))
  def bounds(profile):
   lo=hi=F(0)
   for r,n in profile.items():
    x,y=pw[r];lo+=n*(x if n>=0 else y);hi+=n*(y if n>=0 else x)
   return [lo,hi]
  def rec(pair):return {'lower':str(pair[0]),'upper':str(pair[1]),'decimal_for_display':[float(x) for x in pair]}
  assert bounds({r:T2.get(r,0)-P2.get(r,0) for r in ranks})[1]<0
  margins={}
  for m in [2,4,6,8]:
   profile={r:N.get(r,0)-H.get(r,0)+F(m,36*(m-1))*(T2.get(r,0)-P2.get(r,0))-(1618 if r==1 else 0) for r in ranks};margins[m]=rec(bounds(profile))
  assert F(margins[2]['upper'])<0 and F(margins[4]['upper'])<0<F(margins[6]['lower'])
  limit=bounds({r:N.get(r,0)-H.get(r,0)+F(T2.get(r,0)-P2.get(r,0),36)-(1618 if r==1 else 0) for r in ranks})
  outcases[tag]={'covered_C':str(C),'exponent_t':str(1-C),'above_requested_one_stage_threshold':C>critical,'first_profitable_even_m':6,'margins':margins,'limiting_margin':rec(limit)}
 out={'status':'PASS_EXACT_STRICT_COVERED_Q8_TARGET_BUDGETS','base_result_sha256':hashlib.sha256(raw).hexdigest(),'method':'Exact rational atanh-series log bounds and alternating exp bounds around199/200','outward_power_grid':'10^30','log_terms':36,'exp_lower_degree':5,'exp_upper_degree':4,'Q_profile':{1:1618},'cases':outcases,'one_stage_threshold_from_root':str(critical),'supplier_or_bootstrap_admitted':False,'scope':'Only conditional complete movement profiles at t=1-C. Actual covered saving, changed-atom rho, source completion, ordinary/physical compiler and bootstrap premises remain.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({tag:{'C':x['covered_C'],'m4':x['margins'][4]['decimal_for_display'],'m6':x['margins'][6]['decimal_for_display'],'limit':x['limiting_margin']['decimal_for_display']} for tag,x in outcases.items()},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base-result',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
