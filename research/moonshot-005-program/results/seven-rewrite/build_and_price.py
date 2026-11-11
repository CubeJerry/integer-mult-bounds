#!/usr/bin/env python3
"""Seven current replacements, exact reference word and complete conditional price."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
PREPAID='6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51'
RETAIN={33272,33281,37606}
def need(p,s):
 if not p:raise ValueError(s)
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def encode(a):return {str(j):str(v) for j,v in sorted(a.items())}
def span(f):
 s={0}
 for b in f:s|={x^b for x in s}
 return frozenset(s)
def replay(w,program,M,checks=None,extra_helper=None,capture=None):
 n=w['public'];rows=[{i:F(1)} if i in M or i==extra_helper else {} for i in range(n+w['owned_fields'])];cur=w['initial']+[None]*w['owned_fields'];frames=list(map(span,w['frames']));counts=Counter();moves=Counter();active=peak=lifetimes=0;snapshots={}
 for k,e in enumerate(program):
  if capture and k in capture:snapshots[k]=rows[e[1]].copy()
  op,r=e[:2];counts[op]+=1
  if op=='INIT':need(r>=n and cur[r] is None,'INIT fresh owned');cur[r]=e[2];rows[r]={};active+=1;lifetimes+=1;peak=max(peak,active)
  elif op=='CLEAR':need(r>=n and cur[r]==e[2],'CLEAR ownership/chart');rows[r]={};cur[r]=None;active-=1
  elif op=='MOVE':
   need(cur[r]==e[2] and e[4]==(r>=n),'MOVE actual chart/owner');a,b=frames[e[2]],frames[e[3]];need(a<=b or b<=a,'MOVE nested spans');rank=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));moves[rank]+=1;cur[r]=e[3]
  elif op=='SCALE':need(cur[r]==e[3] and F(e[2])!=0,'SCALE chart');rows[r]={j:F(e[2])*v for j,v in rows[r].items()}
  elif op in ['ADD','COPY']:
   need(r!=e[2] and cur[r] is not None and frames[cur[r]]==frames[cur[e[2]]]==frames[e[4]],'live cochart scalar')
   if op=='COPY':need(not rows[r],'COPY zero in declared input domain')
   add(rows[r],rows[e[2]],F(e[3]))
  else:raise ValueError(op)
  if checks and k+1 in checks:
   q=checks[k+1];need(rows[q['owner']]==q['target'],'exact reconstructed replacement row')
 need(cur[:n]==w['final'] and all(x is None for x in cur[n:]) and active==0,'final charts and cleanup')
 return rows,cur,{'counts':dict(sorted(counts.items())),'MOVE_histogram':dict(sorted(moves.items())),'declared_owned_labels':w['owned_fields'],'owned_lifetimes':lifetimes,'peak_live_owned':peak,'final_live_owned':active},snapshots

def enclose(r,D=10**15):
 n=r**199*D**200;lo=0;hi=r*D+1
 while hi-lo>1:
  x=(lo+hi)//2
  if x**200<=n:lo=x
  else:hi=x
 need(lo**200<=n<hi**200,'exact integer power bracket');return lo,lo if lo**200==n else hi

def run(source,invoice,certificate,prepaid,transcript):
 raw=source.read_bytes();need(hashbytes(raw)==PIN,'native pin');ir=invoice.read_bytes();need(hashbytes(ir)==INVOICE,'invoice pin');pr=prepaid.read_bytes();need(hashbytes(pr)==PREPAID,'prepaid reference pin');w=json.loads(gzip.decompress(raw));C=json.loads(certificate.read_text());need(C['source_sha256']==PIN,'certificate source pin');allten={x['before_event']:x for x in C['witnesses']};need(RETAIN<=set(allten) and len(allten)==10,'source ten/retained three');seven={i:x for i,x in allten.items() if i not in RETAIN};need(len(seven)==7,'seven active rewrites');n=w['public'];M=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(len(M)==400,'400 difference inputs')
 baseline,basecur,basebill,targetrows=replay(w,w['program'],M,capture=seven)
 operations=[];rewrites=[];checks={};newADDs=0;terms_by_kind=Counter()
 for i,e in enumerate(w['program']):
  if i not in seven:operations.append(e);continue
  a=seven[i];need(e==a['move'] and e[0]=='MOVE' and e[1]>=n and e[4] is True,'source replacement MOVE');r,old,dest=e[1:4];need(targetrows[i]=={int(j):F(v) for j,v in a['target_row']},'replayed target certificate');start=len(operations);operations.extend([['CLEAR',r,old],['INIT',r,dest]])
  for observer,coefficient in a['witness']:
   need(observer!=r,'observation distinct from retired owner');operations.append(['ADD',r,observer,coefficient,dest]);newADDs+=1;terms_by_kind[a['observer_kinds'][str(observer)]]+=1
  end=len(operations);checks[end]={'owner':r,'target':targetrows[i]};rewrites.append({'source_event':i,'owner':r,'source_chart':old,'destination_chart':dest,'macro_start_cut':start,'macro_end_cut':end,'witness':a['witness'],'target_row':encode(targetrows[i])})
 out,outcur,outbill,_=replay(w,operations,M,checks=checks);need(out[:n]==baseline[:n] and outcur==basecur,'all1480 public difference endpoints');need(newADDs==26 and sum(terms_by_kind.values())==26,'26 current observer terms');changes={k:outbill['counts'].get(k,0)-basebill['counts'].get(k,0) for k in set(basebill['counts'])|set(outbill['counts'])};need(changes=={'ADD':26,'MOVE':-7,'INIT':7,'CLEAR':7,'SCALE':0,'COPY':0},'complete operation delta');need((outbill['declared_owned_labels'],outbill['peak_live_owned'],outbill['owned_lifetimes'])==(51,43,61),'actual ownership census');need(len(operations)==71294,'actual instruction count')
 controls=[]
 def reject(label,mutant,extra=None,control_checks=None):
  try:replay(w,mutant,M,checks=checks if control_checks is None else control_checks,extra_helper=extra)
  except ValueError as ex:controls.append({'mutation':label,'rejection':str(ex)});return
  raise ValueError('negative control accepted '+label)
 bad=[e[:] for e in operations];j=rewrites[0]['macro_start_cut']+2;bad[j][3]=str(F(bad[j][3])+1);reject('wrong_reconstruction_coefficient',bad)
 bad=[e[:] for e in operations];j=rewrites[0]['macro_start_cut']+1;bad[j][2]=rewrites[0]['source_chart'];reject('wrong_reinitialization_chart',bad)
 # The first selected ordinary equality has a nonzero entering-helper400 residual.
 need(400 not in M,'control is an entering helper');_,_,_,dirty_targets=replay(w,w['program'],M,extra_helper=400,capture=seven);dirty_checks={a['macro_end_cut']:{'owner':a['owner'],'target':dirty_targets[a['source_event']]} for a in rewrites};reject('independent_helper400_difference_not_admitted',operations,extra=400,control_checks=dirty_checks)
 z=json.loads(ir);T=Counter({int(k):v for k,v in z['T4'].items()});P4=Counter({int(k):v for k,v in z['P4'].items()});O=Counter();S=Counter();retained=Counter()
 for i,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1]>=n:
   rank=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));O[rank]+=1
   if i in seven:S[rank]+=1
   if i in RETAIN:retained[rank]+=1
 need(O==Counter({1:20,2:9,3:2,4:13,5:2,6:1}) and S==Counter({1:4,3:1,4:1,6:1}) and retained==Counter({1:2,2:1}),'source-owned profiles')
 P=Counter(P4)
 for r in set(O)|set(S):P[r]+=18*(O[r]-S[r])
 pre=json.loads(pr);Ppre=Counter({int(k):v for k,v in pre['new_P'].items()});D=10**15;powers={r:enclose(r,D) for r in set(T)|set(P)|set(Ppre)}
 def moment(profile):
  low=high=0
  for r,c in profile.items():
   a,b=powers[r];low+=c*(a if c>=0 else b);high+=c*(b if c>=0 else a)
  return [low,high]
 margin=moment({r:T[r]-P[r] for r in set(T)|set(P)});premium=moment({r:P[r]-Ppre[r] for r in set(P)|set(Ppre)});need(margin[0]>0 and F(margin[1],18*D)<F(3889495420926,10**12),'strict positive target headroom');need(premium[0]>0,'seven profile is slightly more expensive in paid moment');need(sum(P.values())==153144 and sum(T.values())==27344,'whole position counts');surplus=sum(r*T[r] for r in T)-sum(r*P[r] for r in P);need(surplus==3346,'same rank surplus')
 pre_retain3_upper=int(pre['raw_margin_numerator_bounds'][1])-18*(2*D+powers[2][0]);need(pre_retain3_upper<0,'prepaid14 cannot retain all three additional source MOVEs');paid_delta={r:(P[r]-Ppre[r])//18 for r in set(P)|set(Ppre) if P[r]!=Ppre[r]};need(all((P[r]-Ppre[r])%18==0 for r in set(P)|set(Ppre)),'integral native comparison');need(sum(r*v for r,v in paid_delta.items())==0,'comparison same rank sum')
 payload={'schema':'moonshot-seven-current-reference-word-v1','source_sha256':PIN,'public':n,'owned_fields':w['owned_fields'],'initial':w['initial'],'final':w['final'],'frames':w['frames'],'main_roles':sorted(M),'program':operations,'rewrites':rewrites,'scope':'Conditional homogeneous difference reference rail; shared helper and owned difference supplies remain obligations.'};rawpayload=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode();transcript.write_bytes(gzip.compress(rawpayload,mtime=0))
 return {'status':'PASS_SEVEN_CURRENT_REFERENCE_REWRITE_AND_CONDITIONAL_PRICE','source_sha256':PIN,'invoice_sha256':INVOICE,'current_certificate_sha256':hashbytes(certificate.read_bytes()),'prepaid_budget_sha256':PREPAID,'transcript_payload_sha256':hashbytes(rawpayload),'source_events':len(w['program']),'physical_instructions':len(operations),'all_main_difference_inputs':400,'public_endpoint_rows_checked':1480,'rewritten_events':sorted(seven),'retained_current_events':sorted(RETAIN),'all_historical_returns_retained':[28141,33554,34467,37597],'remaining_observer_terms':26,'remaining_observer_kind_terms':dict(terms_by_kind),'baseline_reference':basebill,'rewritten_reference':outbill,'operation_changes':changes,'owned_source_histogram':dict(O),'saved_histogram':dict(S),'retained_three_histogram':dict(retained),'new_T':dict(sorted(T.items())),'new_P':dict(sorted(P.items())),'paid_count':sum(P.values()),'target_count':sum(T.values()),'rank_surplus':surplus,'denominator':str(D),'raw_margin_numerator_bounds':list(map(str,margin)),'additional_per_native_headroom':{'numerator_bounds':list(map(str,margin)),'denominator':str(18*D),'positive_rank_arrival_ceiling':3},'extra_paid_moment_vs_prepaid14_numerator_bounds':list(map(str,premium)),'extra_paid_moment_vs_prepaid14_denominator':str(18*D),'per_native_histogram_difference_from_prepaid14':dict(sorted(paid_delta.items())),'prepaid14_retain_three_full_margin_upper_numerator':str(pre_retain3_upper),'negative_controls':controls,'scope':'Seven exact conditional current-row replacements plus a complete provisional paid invoice. The26 actual observer terms, full shared native, ordinary/compiler/precision/owned services and compatible BIT remain unresolved; no dominance theorem and no new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ['source','invoice','certificate','prepaid','transcript','output']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();r=run(a.source,a.invoice,a.certificate,a.prepaid,a.transcript);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['new_T','new_P','baseline_reference','rewritten_reference']},indent=2,sort_keys=True))
