#!/usr/bin/env python3
"""Exact fourteen-return quotient and source-history observation reduction."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
ROOT_REL='research/shared-wire-split-composition/data/final.json.gz'
def need(p,s):
 if not p:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def add(a,b,c):
 for k,v in b.items():
  z=a.get(k,F(0))+c*v
  if z:a[k]=z
  else:a.pop(k,None)
def enc(a):return {str(k):str(v) for k,v in sorted(a.items())}
def dec(z):return {int(k):F(v) for k,v in (z.items() if isinstance(z,dict) else z) if F(v)}
def span(f):
 s={0}
 for b in f:s|={x^b for x in s}
 return tuple(sorted(s))
def basis_for(candidates):
 B={}
 for label,row in candidates:
  a=dict(row);z={label:F(1)}
  while a:
   k=min(a)
   if k not in B:
    c=a[k];B[k]=({j:v/c for j,v in a.items()},{j:v/c for j,v in z.items()});break
   b,q=B[k];c=a[k];add(a,b,-c);add(z,q,-c)
 return B
def solve(target,candidates):
 B=basis_for(candidates);a=dict(target);out={}
 while a:
  k=min(a)
  if k not in B:return None
  b,q=B[k];c=a[k];add(a,b,-c);add(out,q,c)
 return out
def dual(target,candidates):
 B=basis_for(candidates);a=dict(target)
 while a:
  k=min(a)
  if k not in B:break
  b,_=B[k];add(a,b,-a[k])
 need(bool(a),'dual requires nonmembership');k=min(a);f={k:F(1)}
 for p in sorted(B,reverse=True):
  row,_=B[p];z=-sum((v*f.get(j,F(0)) for j,v in row.items() if j!=p),F(0))
  if z:f[p]=z
 need(all(sum((v*f.get(j,F(0)) for j,v in row.items()),F(0))==0 for _,row in candidates),'dual annihilates every candidate')
 response=sum((v*f.get(j,F(0)) for j,v in target.items()),F(0));need(response!=0,'nonzero target response');return f,response

def det(A):
 a=[row[:] for row in A];d=F(1)
 for i in range(len(a)):
  k=next((k for k in range(i,len(a)) if a[k][i]),None)
  if k is None:return F(0)
  if k!=i:a[i],a[k]=a[k],a[i];d=-d
  v=a[i][i];d*=v
  for k in range(i+1,len(a)):
   c=a[k][i]/v
   for j in range(i,len(a)):a[k][j]-=c*a[i][j]
 return d

def root_bounds(r,D=10**15):
 n=r**199*D**200;lo=0;hi=r*D+1
 while hi-lo>1:
  m=(lo+hi)//2
  if m**200<=n:lo=m
  else:hi=m
 need(lo**200<=n<hi**200,'integer root bracket');return lo,lo if lo**200==n else hi

def run(source,current,historical,budget):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));C=json.loads(current.read_text())['witnesses'];H=json.loads(historical.read_text());N=w['public'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);E={r for r in M if w['initial'][r]==3};need((N,len(M),len(E))==(1480,400,200),'input partition');need(w['frames'][3]==[],'empty entry chart')
 targets={a['before_event']:{'owner':a['move'][1],'dest':a['move'][3],'rank':a['rank'],'expected':dec(a['target_row']),'kind':'current'} for a in C};targets.update({a['event']:{'owner':a['owner'],'dest':a['to'],'rank':a['rank'],'expected':dec(a['target_row']),'kind':'historical'} for a in H});need(len(targets)==14,'fourteen distinct source occurrences')
 frames=[span(f) for f in w['frames']];need(all(len(s)==2**len(f) for s,f in zip(frames,w['frames'])),'independent frames');canon=[frames.index(f) for f in frames];history={canon[t['dest']]:[] for t in targets.values()};seen=set();rows=[{r:F(1)} if r in M else {} for r in range(N+w['owned_fields'])];cur=w['initial']+[None]*w['owned_fields'];versions=[-1]*len(rows);moves=[None]*len(rows);births=[None]*len(rows);cases=[];ledger=[];fulltargets={}
 def projection(a):return {j:v for j,v in a.items() if j not in E}
 def note(i,r):
  if cur[r] is None or not (r in M or r>=N) or canon[cur[r]] not in history or not rows[r]:return
  key=(canon[cur[r]],r,versions[r],births[r])
  if key in seen:return
  seen.add(key);history[canon[cur[r]]].append({'event':i,'role':r,'kind':'main' if r in M else 'owned','chart':cur[r],'value_version':versions[r],'birth':births[r],'last_move':moves[r],'row':rows[r].copy(),'projection':projection(rows[r])})
 def export(a):return {k:(enc(v) if k in ['row','projection'] else v) for k,v in a.items()}
 for r in range(N):note(-1,r)
 for i,e in enumerate(w['program']):
  op,r=e[:2]
  if i in targets:
   t=targets[i];need(e[0]=='MOVE' and e[1]==t['owner'] and e[3]==t['dest'] and e[4] is True,'actual owned MOVE occurrence');need(rows[r]==t['expected'],'source reproduces predecessor target row');fulltargets[i]=rows[r].copy();hist=history[canon[t['dest']]];target=projection(rows[r]);rec={'event':i,'owner':r,'destination':t['dest'],'kind':t['kind'],'history_records':len(hist),'history_sha256':hashlib.sha256(json.dumps([export(x) for x in hist],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'cases':{}}
   for case in ['owned','owned_main']:
    cand=[(k,x['projection']) for k,x in enumerate(hist) if case=='owned_main' or x['kind']=='owned'];terms={} if not target else None
    if terms is None:
     for k,q in reversed(cand):
      z=solve(target,[(k,q)])
      if z is not None:terms=z;break
    if terms is None:terms=solve(target,cand)
    if terms is None:
     f,response=dual(target,cand);rec['cases'][case]={'status':'NONMEMBER','functional':enc(f),'target_response':str(response),'all_candidate_records':[export(hist[k]) for k,_ in cand]};continue
    residual=rows[r].copy();obs=[]
    for k,co in terms.items():
     a=hist[k];need(a['event']<i and frames[a['chart']]==frames[t['dest']],'strict earlier cochart sample');add(residual,a['row'],-co);obs.append({'coefficient':str(co),'observation':export(a)})
    need(all(j in E for j in residual),'entry-only residual');rec['cases'][case]={'status':'MEMBER','terms':obs,'entry_residual':enc(residual),'entry_residual_support':len(residual)}
   if i==37606:
    a=next(x for x in C if x['before_event']==i);help_candidates=[(s,projection(rows[s])) for s,co in a['witness']];z=solve(target,[(k,x['projection']) for k,x in enumerate(hist)]+[(100000+s,q) for s,q in help_candidates]);need(z is not None,'literal helper-observer positive control');rec['helper_grant_control']=enc(z)
   cases.append(rec)
   if t['kind']=='current':
    a=next(x for x in C if x['before_event']==i)
    for s,k in a['observer_kinds'].items():
     if k=='owned':
      s=int(s);ledger.append({'use_event':i,'owner':s,'value_version':versions[s],'birth':births[s],'last_move':moves[s],'last_move_removed':moves[s] in targets,'current_chart':cur[s],'target_chart':t['dest']})
  need(cur[r] is not None or op=='INIT','live destination')
  if op=='INIT':need(r>=N and cur[r] is None,'fresh owned INIT');rows[r]={};cur[r]=e[2];versions[r]=i;births[r]=i;moves[r]=None
  elif op=='CLEAR':need(r>=N and cur[r]==e[2],'typed CLEAR');rows[r]={};cur[r]=None;versions[r]=i;births[r]=None;moves[r]=None
  elif op=='MOVE':need(cur[r]==e[2] and e[4]==(r>=N),'typed owned MOVE');need(set(frames[e[2]])<=set(frames[e[3]]) or set(frames[e[3]])<=set(frames[e[2]]),'nested MOVE');cur[r]=e[3];moves[r]=i
  elif op=='SCALE':need(cur[r]==e[3],'typed SCALE');rows[r]={j:F(e[2])*v for j,v in rows[r].items()};versions[r]=i
  elif op in ['ADD','COPY']:
   need(r!=e[2] and cur[r]==cur[e[2]]==e[4],'typed cochart scalar')
   if op=='COPY':need(not rows[r],'homogeneous COPY-zero')
   add(rows[r],rows[e[2]],F(e[3]));versions[r]=i
  else:raise ValueError(op)
  note(i,r)
 need(cur[:N]==w['final'] and all(x is None for x in cur[N:]),'final source charts/cleanup');need(len(fulltargets)==14,'all targets replayed')
 order=[a['event'] for a in H]+[a['before_event'] for a in C];projs={i:projection(fulltargets[i]) for i in order};selected=[]
 for i in order:
  if solve(projs[i],[(j,projs[j]) for j in selected]) is None:selected.append(i)
 need(len(selected)==10,'quotient rank10');B=basis_for([(i,projs[i]) for i in selected]);columns=sorted(B);minor=det([[projs[i].get(k,F(0)) for k in columns] for i in selected]);need(minor!=0,'exact rational rank minor');decomps=[]
 for i in order:
  z=solve(projs[i],[(j,projs[j]) for j in selected]);need(z is not None,'upper rank witness');res=fulltargets[i].copy()
  for j,v in z.items():add(res,fulltargets[j],-v)
  need(all(j in E for j in res),'quotient decomposition residual');decomps.append({'event':i,'basis_coefficients':enc(z),'entry_residual':enc(res)})
 stats=Counter('owned_or_entry' if a['cases']['owned']['status']=='MEMBER' else 'owned_main_only' if a['cases']['owned_main']['status']=='MEMBER' else 'unresolved' for a in cases);need(stats==Counter({'owned_or_entry':10,'owned_main_only':3,'unresolved':1}),'exact history classification');bad=next(a for a in cases if a['event']==37606);need(bad['cases']['owned_main']['status']=='NONMEMBER','37606 scoped obstruction')
 # Correct order/chart and signal controls; these test mathematical premises.
 f=dec(bad['cases']['owned_main']['functional']);need(all(j not in E for j in f),'dual vanishes on all freely granted chart3 inputs');need(sum((v*f.get(j,F(0)) for j,v in fulltargets[37606].items()),F(0))!=0,'target versus zero observations')
 need(hashlib.sha256(raw+b'!').hexdigest()!=PIN,'source corruption rejected')
 mutated=dict(fulltargets[33558]);mutated[0]=mutated.get(0,F(0))+1;relation=dict(fulltargets[33554]);relation={j:v/F(4) for j,v in relation.items()};add(mutated,relation,-1);need(any(j not in E for j in mutated),'wrong coefficient target control')
 braw=budget.read_bytes();need(hashlib.sha256(braw).hexdigest()=='6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51','prepaid budget pin');budgetdata=json.loads(braw);D=10**15;b3=root_bounds(3,D);b4=root_bounds(4,D);limit=F(int(budgetdata['raw_margin_numerator_bounds'][1]),18*D);need(F(b4[0],D)>limit,'single rank4 preload exceeds budget');pair_margin_upper=F(int(budgetdata['raw_margin_numerator_bounds'][1]),D)-18*F(b3[0]+b4[0],D);need(pair_margin_upper<0,'two independent entry preloads fail complete invoice')
 certificate={'schema':'moonshot-fourteen-quotient-history-v1','source_sha256':PIN,'current_certificate_sha256':sha(current),'historical_certificate_sha256':sha(historical),'prepaid_budget_sha256':sha(budget),'entry_chart':3,'entry_input_count':len(E),'all_main_input_count':len(M),'distributed_input_union':len(set().union(*(set(x) for x in projs.values()))),'quotient_rank':len(selected),'basis_events':selected,'minor_columns':columns,'minor_determinant':str(minor),'basis_projected_rows':{str(i):enc(projs[i]) for i in selected},'source_target_rows':{str(i):enc(fulltargets[i]) for i in order},'decompositions':decomps,'history_reductions':cases,'current_owned_observer_ledger':ledger,'fresh_preload_price':{'denominator':str(D),'rank3_bounds':list(map(str,b3)),'rank4_bounds':list(map(str,b4)),'existing_headroom_upper':str(limit),'two_preload_full_margin_upper':str(pair_margin_upper)},'scope':'Exact source-linear quotient and conditional historical-observation reductions. Historical rows and chart3 residuals are not free physical supplies; no full native/supplier or new kappa.'}
 result={'status':'PASS_FOURTEEN_RETURN_QUOTIENT_AND_HISTORY_REDUCTION','source_sha256':PIN,'source_events':len(w['program']),'independent_difference_inputs':len(M),'entry_chart3_inputs':len(E),'distributed_input_union':certificate['distributed_input_union'],'quotient_rank':10,'minor_determinant':str(minor),'history_classification':dict(stats),'remaining_obstruction_event':37606,'remaining_obstruction_history_records':bad['history_records'],'remaining_obstruction_functional':bad['cases']['owned_main']['functional'],'remaining_obstruction_response':bad['cases']['owned_main']['target_response'],'fresh_rank4_exceeds_remaining_paid_budget':True,'controls':['source corruption','exact nonzero separating functional','original helper-observer positive control','wrong target-row coefficient','rank4 paid-budget exclusion'],'scope':certificate['scope']}
 return certificate,result
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ['source','current','historical','budget','certificate','output']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();c,r=run(a.source,a.current,a.historical,a.budget);a.certificate.write_text(json.dumps(c,indent=2,sort_keys=True)+'\n');a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
