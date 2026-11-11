#!/usr/bin/env python3
"""Independent exact typed replay of paid entry-preloaded difference rail."""
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT='d46db515a5fead49b752b8d798472c883aff7698d7e5e948f0d4e336ec99054b'
def need(c,m):
 if not c:raise ValueError(m)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,Q(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in s}
 return frozenset(s)
def play(w,ops,extra,checks):
 p=w['public'];N=p+w['owned_fields']+extra;M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);rows=[{r:Q(1)} if r in M else {} for r in range(N)];cur=w['initial']+[None]*(N-p);active=set(range(p));spans=list(map(span,w['frames']));count=Counter();hist=Counter();ownedhist=Counter();owned=peak=life=0;check={a['physical_before_event']:a for a in checks}
 for i,e in enumerate(ops):
  if i in check:
   a=check[i];old,new=a['old_physical_owner'],a['new_physical_owner'];need(old in active and new in active and rows[old]==rows[new],'exact old/new400-input row at rebind');need(cur[new]==a['destination'],'new owner at target destination')
  op,r=e[:2];need(0<=r<N,'physical label range');count[op]+=1
  if op=='INIT':need(r>=p and r not in active and cur[r] is None,'owned INIT');rows[r]={};cur[r]=e[2];active.add(r);owned+=1;life+=1;peak=max(peak,owned)
  elif op=='CLEAR':need(r>=p and r in active and cur[r]==e[2],'owned CLEAR');active.remove(r);rows[r]={};cur[r]=None;owned-=1
  elif op=='MOVE':
   need(r in active and cur[r]==e[2],'MOVE current chart');need(type(e[4]) is bool and e[4]==(r>=p),'MOVE actual ownership');s,d=spans[e[2]],spans[e[3]];need(s<d if r<p else s<d or d<s,'strict comparable MOVE');rank=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));hist[rank]+=1
   if r>=p:ownedhist[rank]+=1
   cur[r]=e[3]
  elif op in ('ADD','COPY'):
   t=e[2];need(r!=t and r in active and t in active and cur[r]==cur[t]==e[4],'current typed cochart scalar input');a=Q(e[3]);need(a!=0,'nonzero ADD coefficient')
   if op=='COPY':need(not rows[r],'all400-input COPYzero')
   add(rows[r],rows[t],a)
  elif op=='SCALE':need(r in active and cur[r]==e[3] and Q(e[2])!=0,'current nonzero SCALE');rows[r]={j:v*Q(e[2]) for j,v in rows[r].items()}
  else:raise ValueError(op)
 return rows,cur,{'counts':dict(count),'move_histogram':dict(sorted(hist.items())),'owned_move_histogram':dict(sorted(ownedhist.items())),'declared_owned_labels':w['owned_fields']+extra,'peak_owned':peak,'owned_lifetimes':life,'final_live_owned':owned}
def run(source,certificate,transcript,receipt):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));rawcert=certificate.read_bytes();need(hashlib.sha256(rawcert).hexdigest()==CERT,'independently reviewed historical certificate');C=json.loads(rawcert);payload=gzip.decompress(transcript.read_bytes());t=json.loads(payload);p=w['public'];N=p+w['owned_fields'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(t['source_sha256']==PIN and t['public']==p and t['owned_fields']==55 and t['initial']==w['initial'] and t['frames']==w['frames'] and set(t['main_roles'])==M,'physical interface');need(w['frames'][3]==[],'entry empty chart')
 expected=[];forms=[];after=defaultdict(list);targets={};mapping={r:r for r in range(N)};rebind=[]
 for j,a in enumerate(C):
  z=N+j;row={};helpers=[];owned=[]
  for term in a['witnesses']['all']:
   o=term['observation'];need(o['phase']=='after' and o['event']<a['event'] and o['chart']==a['to'],'pinned earlier observation')
   if o['kind']=='helper':
    need(all(int(k) in M and w['initial'][int(k)]==3 for k in o['row']),'every helper row uses only initial empty-chart main inputs');add(row,{int(k):Q(v) for k,v in o['row'].items()},Q(term['coefficient']));helpers.append(o['role'])
   else:need(o['kind']=='owned','four residual owned samples');owned.append(o['role']);after[o['event']].append((z,o['role'],term['coefficient'],a['to']))
  expected.append(['INIT',z,3]);expected.extend(['ADD',z,r,str(c),3] for r,c in sorted(row.items()));expected.append(['MOVE',z,3,a['to'],True]);targets[a['event']]=(a,z)
  forms.append({'target_event':a['event'],'support':len(row),'helper_roles':helpers,'remaining_owned_roles':owned,'destination':a['to'],'rank':len(w['frames'][a['to']]),'row':{str(r):str(c) for r,c in sorted(row.items())},'coefficient_l1':str(sum(map(abs,row.values()),Q(0)))})
 prelude=len(expected);union_inputs={int(r) for f in forms for r in f['row']};need(len(union_inputs)==92 and all(Q(v).denominator==1 and abs(Q(v))<=2 for f in forms for v in f['row'].values()),'exact92-input integer preloader coefficient bound')
 for k,e in enumerate(w['program']):
  op,r=e[:2]
  if op=='INIT':mapping[r]=r
  if k in targets:
   a,z=targets[k];need(e==['MOVE',a['owner'],a['from'],a['to'],True],'literal removed route');old=mapping[r];rebind.append({'physical_before_event':len(expected),'event':k,'logical_owner':r,'old_physical_owner':old,'new_physical_owner':z,'destination':a['to']});expected.append(['CLEAR',old,a['from']]);mapping[r]=z
  else:
   out=e[:];out[1]=mapping[r]
   if op in ('ADD','COPY'):out[2]=mapping[e[2]]
   expected.append(out)
  expected.extend(['ADD',z,mapping[r0],co,f] for z,r0,co,f in after.get(k,[]))
 need(expected==t['program'],'independent reconstruction of every physical instruction');need(t['prelude_instructions']==prelude==189 and t['rebindings']==rebind,'all source/physical boundary pins');need([a['support'] for a in forms]==[44,44,44,49],'exact helper-entry form supports')
 for rec,f in zip(t['preloads'],forms):need(rec['row']==[[int(r),c] for r,c in f['row'].items()] and rec['rank']==f['rank'] and rec['destination']==f['destination'],'author preload row invoice')
 rows,cur,bill=play(w,t['program'],4,rebind);ref,rf,baseline=play(w,w['program'],0,[]);need(rows[:p]==ref[:p] and cur[:p]==rf[:p],'all1480 public endpoints on all400 inputs');need(bill['final_live_owned']==0,'all owned retired')
 changes=Counter(bill['counts']);changes.subtract(baseline['counts']);need(changes['ADD']==185 and changes['INIT']==changes['CLEAR']==4 and changes['MOVE']==0 and all(v==0 for k,v in changes.items() if k not in ('ADD','INIT','CLEAR','MOVE')),'complete operation changes');need((bill['declared_owned_labels'],bill['peak_owned'],bill['owned_lifetimes'])==(55,44,58),'full label/peak/lifetime invoice')
 actual=Counter(baseline['move_histogram']);actual.subtract({2:3,5:1});actual.update({3:3,6:1});need(dict(actual)==bill['move_histogram'],'four charged preloads and four removed arrivals')
 a=json.loads(receipt.read_text());need(a['transcript_payload_sha256']==hashlib.sha256(payload).hexdigest() and a['rewritten']['counts']==bill['counts'] and a['rewritten']['move_histogram']=={str(k):v for k,v in bill['move_histogram'].items()},'author exact result')
 controls=[]
 for name in ('wrong_entry_coefficient','wrong_preload_ownership','stale_role_after_rebinding'):
  bad=[e[:] for e in t['program']]
  if name=='wrong_entry_coefficient':bad[1][3]=str(-Q(bad[1][3]))
  elif name=='wrong_preload_ownership':next(e for e in bad[:prelude] if e[0]=='MOVE')[4]=False
  else:
   c=rebind[0];start=c['physical_before_event']+1;old,new=c['old_physical_owner'],c['new_physical_owner'];e=next(e for e in bad[start:] if e[1]==new or e[0] in ('ADD','COPY') and e[2]==new)
   if e[1]==new:e[1]=old
   else:e[2]=old
  try:br,bc,bb=play(w,bad,4,rebind);need(br[:p]==ref[:p] and bb['final_live_owned']==0,'mutated endpoints/cleanup')
  except ValueError as ex:controls.append({'mutation':name,'rejection':str(ex)})
  else:raise ValueError('mutation accepted '+name)
 return {'status':'PASS_INDEPENDENT_ENTRY_PRELOADED_DIFFERENCE_RAIL','source_sha256':PIN,'certificate_sha256':CERT,'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'physical_instructions':len(t['program']),'independent_difference_inputs':400,'public_endpoint_rows':p,'prelude_instructions':prelude,'entry_ADDs':181,'distinct_entry_q_inputs':len(union_inputs),'entry_coefficient_maximum_absolute_value':2,'later_owned_observation_ADDs':4,'later_helper_observation_reads':0,'charged_preload_MOVE_histogram':{3:3,6:1},'removed_owned_MOVE_histogram':{2:3,5:1},'forms':forms,'baseline':baseline,'rewritten':bill,'operation_changes':dict(changes),'negative_controls':controls,'scope':'Five historical helper observations physically discharged by four charged preloads. Four later owned difference observations and full reference difference-rail supply remain conditional; no complete H4 native or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--transcript',type=Path,required=True);p.add_argument('--author-result',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.certificate,a.transcript,a.author_result);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k not in ('forms','baseline','rewritten')},indent=2,sort_keys=True))
