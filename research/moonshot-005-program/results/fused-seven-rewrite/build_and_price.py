#!/usr/bin/env python3
"""Fuse two adjacent owned-return rewrites while preserving the seven-MOVE price."""
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

def run(source, invoice, certificate, seven_result, transcript):
 raw=source.read_bytes();need(hashbytes(raw)==PIN,'native pin')
 ir=invoice.read_bytes();need(hashbytes(ir)==INVOICE,'invoice pin')
 cr=certificate.read_bytes();need(hashbytes(cr)=='7b915321a6e9afc2a83fd79f95e0c9605d28dc578d69d4b0700ee6fd37f739b9','current certificate pin')
 sr=seven_result.read_bytes();need(hashbytes(sr)=='4d56a788e3eb78032d8f9e7a91583af20b8593940ed275bf7a867bb525e98217','seven result pin')
 w=json.loads(gzip.decompress(raw));C=json.loads(cr);s7=json.loads(sr)
 allten={a['before_event']:a for a in C['witnesses']}
 seven={i:a for i,a in allten.items() if i not in RETAIN}
 plain={i:a for i,a in seven.items() if i not in {40094,40096}}
 need(len(seven)==7 and len(plain)==5,'seven source MOVEs in six modules')
 n=w['public'];M=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 need(len(M)==400,'400 independent main differences')
 baseline,basecur,basebill,targets=replay(w,w['program'],M,capture=seven)
 original_block=[['MOVE',1512,597,1031,True],['ADD',1512,1362,'-1',1031],
                 ['MOVE',1512,1031,591,True],['SCALE',1512,'-1/2',591],
                 ['ADD',901,1512,'1',591],['CLEAR',1512,591]]
 need(w['program'][40094:40100]==original_block,'exact unobserved intermediate block')
 for t,a in seven.items():
  need(targets[t]=={int(j):F(v) for j,v in a['target_row']},'replayed target row')
 need(seven[40096]['witness']==[[133,'1/2'],[901,'2']],'terminal two-observer identity')
 operations=[];checks={};modules=[];terms=Counter();observer_records=[]
 for t,e in enumerate(w['program']):
  if 40095<=t<40100:continue
  if t==40094:
   start=len(operations)
   block=[['CLEAR',1512,597],['INIT',1512,591],['ADD',1512,133,'-1/4',591],
          ['ADD',1512,901,'-1',591],['ADD',901,1512,'1',591],['CLEAR',1512,591]]
   operations.extend(block)
   checks[start+4]={'owner':1512,'target':{j:-v/2 for j,v in targets[40096].items()}}
   modules.append({'source_interval':[40094,40100],'source_moves':[40094,40096],
                   'output_cut':len(operations),'macro_start_cut':start,
                   'observer_identity_event':40096,'witness':[[133,'-1/4'],[901,'-1']],
                   'effect':'delta901_after=-delta133_before/4; owned1512 retired'})
   for h in [133,901]:
    terms[seven[40096]['observer_kinds'][str(h)]]+=1
    observer_records.append({'module':40094,'identity_event':40096,'observer':h,
       'chart':591,'last_value_event':seven[40096]['observer_last_value_events'][str(h)]})
   continue
  if t not in plain:operations.append(e);continue
  a=plain[t];need(e==a['move'],'current source MOVE match')
  r,old,dest=e[1:4];start=len(operations)
  operations.extend([['CLEAR',r,old],['INIT',r,dest]])
  for h,c in a['witness']:
   operations.append(['ADD',r,h,c,dest]);terms[a['observer_kinds'][str(h)]]+=1
   observer_records.append({'module':t,'identity_event':t,'observer':h,'chart':dest,
                           'last_value_event':a['observer_last_value_events'][str(h)]})
  checks[len(operations)]={'owner':r,'target':targets[t]}
  modules.append({'source_interval':[t,t+1],'source_moves':[t],'output_cut':len(operations),
                  'macro_start_cut':start,'observer_identity_event':t,'witness':a['witness']})
 out,outcur,outbill,_=replay(w,operations,M,checks=checks)
 need(out[:n]==baseline[:n] and outcur==basecur,'all1480 public endpoint rows')
 need(len(operations)==71286,'fused exact instruction count')
 need(terms==Counter({'main':4,'helper':16,'owned':2}),'22 observer terms')
 changes={k:outbill['counts'].get(k,0)-basebill['counts'].get(k,0) for k in set(basebill['counts'])|set(outbill['counts'])}
 need(changes=={'ADD':21,'MOVE':-7,'INIT':6,'CLEAR':6,'SCALE':-1,'COPY':0},'full operation delta')
 need((outbill['declared_owned_labels'],outbill['owned_lifetimes'],outbill['peak_live_owned'])==(51,60,43),'owned census')
 controls=[]
 def reject(label,word,control_checks=checks,extra=None):
  try:replay(w,word,M,checks=control_checks,extra_helper=extra)
  except ValueError as ex:controls.append({'mutation':label,'rejection':str(ex)});return
  raise ValueError('negative control accepted '+label)
 fuse=next(a for a in modules if a['source_interval']==[40094,40100]);start=fuse['macro_start_cut']
 bad=[e[:] for e in operations];bad[start+2][3]='-1/2';reject('wrong_fused_coefficient',bad)
 bad=[e[:] for e in operations];bad[start+1][2]=1031;reject('wrong_fused_destination',bad)
 bad=[e[:] for e in operations];bad[start+3][3]='1';reject('wrong_endpoint_cancellation_sign',bad)
 _,_,_,dirty=replay(w,w['program'],M,capture=seven,extra_helper=400)
 dirty_checks={}
 for a in modules:
  t=a['observer_identity_event']
  if t==40096:dirty_checks[a['macro_start_cut']+4]={'owner':1512,'target':{j:-v/2 for j,v in dirty[t].items()}}
  else:dirty_checks[a['output_cut']]={'owner':plain[t]['move'][1],'target':dirty[t]}
 reject('independent_helper400_difference_outside_domain',operations,dirty_checks,400)
 z=json.loads(ir);T=Counter({int(k):v for k,v in z['T4'].items()});P4=Counter({int(k):v for k,v in z['P4'].items()})
 O=Counter();S=Counter()
 for t,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1]>=n:
   r=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));O[r]+=1
   if t in seven:S[r]+=1
 P=Counter(P4)
 for r in set(O)|set(S):P[r]+=18*(O[r]-S[r])
 need(S==Counter({1:4,3:1,4:1,6:1}),'same saved MOVE profile')
 need(dict(sorted(P.items()))=={int(k):v for k,v in s7['new_P'].items()},'same complete paid invoice')
 need(dict(sorted(T.items()))=={int(k):v for k,v in s7['new_T'].items()},'same complete target invoice')
 D=10**15;lower=upper=0
 for r in set(T)|set(P):
  c=T[r]-P[r];lo,hi=enclose(r,D);lower+=c*(lo if c>=0 else hi);upper+=c*(hi if c>=0 else lo)
 need([str(lower),str(upper)]==s7['raw_margin_numerator_bounds'] and lower>0,'same exact positive margin')
 payload={'schema':'moonshot-fused-seven-reference-v1','source_sha256':PIN,'public':n,
          'owned_fields':w['owned_fields'],'initial':w['initial'],'final':w['final'],'frames':w['frames'],
          'main_roles':sorted(M),'program':operations,'modules':modules,
          'scope':'Homogeneous reference difference rail; actual22 observers and shared supplier remain premises.'}
 pr=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode()
 transcript.write_bytes(gzip.compress(pr,mtime=0))
 return {'status':'PASS_FUSED_SEVEN_REFERENCE_AND_UNCHANGED_CONDITIONAL_PRICE','source_sha256':PIN,
         'current_certificate_sha256':hashbytes(cr),'invoice_sha256':INVOICE,'seven_result_sha256':hashbytes(sr),
         'transcript_payload_sha256':hashbytes(pr),'original_instructions':len(w['program']),
         'physical_instructions':len(operations),'independent_q_inputs':400,'public_endpoint_rows_checked':1480,
         'source_moves_removed':sorted(seven),'replacement_modules':len(modules),'fused_source_interval':[40094,40100],
         'fused_endpoint_identity':'delta901_after=-delta133_before/4','observer_terms':22,
         'observer_terms_by_kind':dict(terms),'observation_versions':observer_records,
         'removed_observers_at40094':[695,1336,1362,1502],
         'baseline_reference':basebill,'rewritten_reference':outbill,'operation_changes':changes,
         'new_T':dict(sorted(T.items())),'new_P':dict(sorted(P.items())),
         'saved_owned_histogram':dict(sorted(S.items())),'paid_count':sum(P.values()),'target_count':sum(T.values()),
         'rank_surplus':sum(r*(T[r]-P[r]) for r in set(T)|set(P)),
         'denominator':str(D),'raw_margin_numerator_bounds':[str(lower),str(upper)],
         'additional_per_native_headroom':{'numerator_bounds':[str(lower),str(upper)],'denominator':str(18*D),
                                         'positive_rank_arrival_ceiling':3},
         'negative_controls':controls,
         'scope':'Six conditional modules remove the same seven owned difference MOVEs, with22 observer terms. '
                 'No unpriced cross-chart transport is added: the unobserved intermediate owned state is omitted. '
                 'Full physical observer acquisition, joint native and global supplier assumptions remain open. No new kappa.'}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['source','invoice','certificate','seven_result','transcript','output']:
  p.add_argument('--'+name.replace('_','-'),dest=name,type=Path,required=True)
 a=p.parse_args();r=run(a.source,a.invoice,a.certificate,a.seven_result,a.transcript)
 a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k not in ['new_T','new_P','baseline_reference','rewritten_reference','observation_versions']},sort_keys=True,indent=2))

