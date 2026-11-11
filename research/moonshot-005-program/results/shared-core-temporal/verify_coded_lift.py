#!/usr/bin/env python3
"""Exact positive/alias/zero-target controls for the conditional coded interface."""
from fractions import Fraction as F
import itertools,json

def need(p,m):
 if not p:raise ValueError(m)
weights=[F(-1),F(0),F(1,2),F(1),F(2)]
scalars=[F(-2),F(-1,2),F(1),F(3)]
cases=0;bad_defects=0
for ld,ls,c in itertools.product(weights,weights,scalars):
 for ud,vd,us,vs in itertools.product([F(-2),F(0),F(3)],repeat=4):
  zd=ld*ud+(1-ld)*vd;zs=ls*us+(1-ls)*vs;t=us-vs
  target=ld*(ud+c*us)+(1-ld)*(vd+c*vs)
  coded=zd+c*zs+c*(ld-ls)*t
  need(coded==target,'coded/coded identity')
  need(zd+c*ld*us+c*(1-ld)*vs==target,'coded/main identity')
  gotu=ud+c*zs+c*(1-ls)*t;gotv=vd+c*zs-c*ls*t
  need((gotu,gotv)==(ud+c*us,vd+c*vs),'main/coded identity')
  for new in weights:
   need(zd+(new-ld)*(ud-vd)==new*ud+(1-new)*vd,'weight change')
  bad_defects+=(zd+c*zs!=target)
  cases+=1
need(bad_defects>0,'omitted mismatch defect must fail')
# The representation delta=old(a)+b aliases a destination. Snapshot it first.
a,b,v,z=F(1),F(2),F(7),F(5);delta=a+b;lam=F(1,2)
a_good=a+z+(1-lam)*delta;v_good=v+z-lam*delta
need((a_good,v_good)==(F(15,2),F(21,2)),'snapshot alias oracle')
a_bad=a+z+(1-lam)*(a+b);v_bad=v+z-lam*(a_bad+b)
need((a_bad,v_bad)!=(a_good,v_good),'stale source expression mutation')
# Coded zero does not imply both virtual destinations zero.
u,v,lam=F(1),F(-1),F(1,2)
need(lam*u+(1-lam)*v==0 and (u!=0 or v!=0),'COPY zero guard distinction')
# Dirty shared helpers preserve their independent input at either boundary.
for h,lam in itertools.product([F(-3),F(0),F(7)],weights):
 need(lam*h+(1-lam)*h==h,'arbitrary helper boundary')
# Cauchy equality does not license an ordinary cross-chart update.
def cochart_snapshot(observations,destination_frame):
 return all(frame==destination_frame for _,frame in observations)
need(cochart_snapshot([(1,'A'),(2,'A')],'A'),'cochart positive control')
need(not cochart_snapshot([(1,'A'),(2,'B')],'A'),'cross-chart negative control')
print(json.dumps({'status':'PASS_CODED_LIFT_LOCAL_IDENTITIES','rational_add_cases':cases,'omitted_defect_failures':bad_defects,'snapshot_alias_good':[str(a_good),str(v_good)],'snapshot_alias_bad':[str(a_bad),str(v_bad)],'controls':['omitted unequal-weight defect','destination alias without snapshot','coded-zero versus both-zero COPY','cross-chart observation'], 'scope':'Local algebra and failure controls only; no all-events observation certificate, chronology, physical invoice or new kappa.'},indent=2))
