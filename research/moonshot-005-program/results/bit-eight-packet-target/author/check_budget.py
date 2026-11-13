"""Independent exact target-first eight-packet invoice."""
import argparse,collections,gzip,hashlib,json
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
def main(a):
 sp=a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';raw=sp.read_bytes();assert hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(raw));fr={int(k):v for k,v in s['frames'].items()}
 N=collections.Counter(abs(fr[e[3]]['dim']-fr[e[2]]['dim']) for e in s['program'] if e[0]=='MOVE');H=collections.Counter(fr[s['final'][i]]['dim']-fr[s['start'][i]]['dim'] for i in range(222,659))
 assert N=={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10} and H=={2:1,4:25,6:1,8:410}
 P2=collections.Counter({r:36*n for r,n in N.items()});P2[1]+=444
 for j in range(1,9):P2[7*j]+=444
 T2=collections.Counter({r:36*n for r,n in H.items()});T2[127]+=222
 for j in range(1,10):T2[1+7*j]+=444
 Q={1:111*7+111*7+8*8};assert Q[1]==1618
 ranks=set(N)|set(H)|set(P2)|set(T2)|{1,7,8};grid=10**36;pw={}
 for r in ranks:
  target=r**199*grid**200;z=integer_root(target,200);pw[r]=(F(z,grid),F(z+int(z**200!=target),grid))
 def bounds(profile):
  lo=hi=F(0)
  for r,n in profile.items():
   x,y=pw[r];lo+=n*(x if n>=0 else y);hi+=n*(y if n>=0 else x)
  return [lo,hi]
 def rec(pair):return {'lower':str(pair[0]),'upper':str(pair[1]),'decimal_for_display':[float(x) for x in pair]}
 cases={}
 for m in [2,4,6,8,16,32]:
  tm={r:m//2*T2.get(r,0)-18*(m-1)*H.get(r,0) for r in ranks};pm={r:m//2*P2.get(r,0)-18*(m-1)*N.get(r,0)+18*(m-1)*Q.get(r,0) for r in ranks};assert min(tm.values())>=0 and min(pm.values())>=0
  per=bounds({r:F(tm[r]-pm[r],18*(m-1)) for r in ranks});total=[x*18*(m-1) for x in per]
  cases[m]={'perrail_margin':rec(per),'complete_moment_margin':rec(total),'T':{r:n for r,n in tm.items() if n},'P':{r:n for r,n in pm.items() if n},'target_positions':sum(tm.values()),'paid_positions':sum(pm.values()),'integer_rank_surplus':sum(r*(tm[r]-pm[r]) for r in ranks)}
 assert F(cases[2]['perrail_margin']['upper'])<0 and F(cases[4]['perrail_margin']['upper'])<0<F(cases[6]['perrail_margin']['lower'])
 assert bounds({r:T2.get(r,0)-P2.get(r,0) for r in ranks})[1]<0
 assert cases[6]['target_positions']==20520 and cases[6]['paid_positions']==209286 and cases[6]['integer_rank_surplus']==4428
 limit=bounds({r:N.get(r,0)-H.get(r,0)+F(T2.get(r,0)-P2.get(r,0),36)-Q.get(r,0) for r in ranks});assert limit[0]>3 and limit[1]<4
 assert F(cases[6]['perrail_margin']['lower'])>1 and F(cases[6]['perrail_margin']['upper'])<2
 out={'status':'PASS_EXACT_CONDITIONAL_Q8_UNIT_PATH_TARGET_BUDGET','source_sha256':hashlib.sha256(raw).hexdigest(),'t':'199/200','native_paid':dict(N),'helper_target':dict(H),'paired_paid':dict(P2),'paired_target':dict(T2),'Q_target_paid':Q,'minimum_q8_unit_path_calls':1618,'fixed_even_cases':cases,'first_profitable_even_m':6,'limiting_perrail_margin':rec(limit),'m6_affordable_extra_unit_calls':1,'all_finite_m_affordable_extra_unit_calls_at_most':3,'scalar_historical_fitting_rank_required_at_least':10,'scalar_actual_historical_rank_required_at_least':10,'scalar_nullity_sum_required_at_least':2,'allV_unconditional_nullity_sum_required_at_least':'V','allV_rank10V_not_established':True,'complete_source_constructed':False,'scope':'Target-first conditional caller invoice. Causal source acquisition, all222 main endpoints, histories, chart maps, owned erasure, ordinarywork, compiler and foundations required; no initial eight forms granted.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'Q':Q,'m4':cases[4]['perrail_margin'],'m6':cases[6]['perrail_margin'],'limit':rec(limit)},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
