"""Independent active-window contact enumeration and reverse dirty dual check."""
import argparse,gzip,hashlib,json
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,s):
 if not b:raise ValueError(s)
def run(source,author):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));ops=w['program'];M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);end=len(ops);nexttouch={};seen={};future={};depart={}
 for i in range(end-1,-1,-1):
  e=ops[i];roles={e[1]}|({e[2]} if e[0] in ('ADD','COPY') else set())
  for r in roles:nexttouch[i,r]=seen.get(r,end);seen[r]=i
  if e[0]=='MOVE' and e[1] in M:
   need((e[1],e[3]) not in future,'unique arrival');future[e[1],e[3]]=i;depart[e[1],e[2]]=i
 cohorts=defaultdict(set)
 for r in M:cohorts[w['initial'][r]].add(r)
 active=defaultdict(list);windows=[]
 for i,e in enumerate(ops):
  if e[0]!='MOVE':continue
  r,a,b=e[1:4]
  if r in M:
   for win in active[b]:
    if win['start']<i<win['close']:win['receivers'].add(r)
   cohorts[a].remove(r);cohorts[b].add(r)
  else:
   deadline=nexttouch[i,r]
   for q in sorted(cohorts[a]):
    close=future.get((q,b),end)
    if i<close<deadline:
     win={'start':i,'close':close,'helper_next_use':deadline,'helper':r,'donor':q,'from':a,'to':b,'receivers':set(cohorts[b])};windows.append(win);active[b].append(win)
 loans=[];contacts=[];critical=[]
 for win in windows:
  rec={k:v for k,v in win.items() if k!='receivers'};loans.append(rec)
  for r in sorted(win['receivers']):
   leave=depart.get((r,win['to']),end);early=leave<win['close'];need(r!=win['donor'],'distinct recipient')
   if early:need(win['from']==3 and w['initial'][r]==w['initial'][win['donor']]==3,'critical initial cochart')
   x={'loan_start':win['start'],'donor':win['donor'],'recipient':r,'recipient_departure':leave,'donor_return':win['close'],'direct_ADD_after_source_event':-1 if early else win['close'],'direct_frame':3 if early else win['to']};contacts.append(x)
   if early:critical.append(x)
 audit=json.loads((author/'RAW-CONTACT-AUDIT.json').read_text());digest=hashlib.sha256(json.dumps({'loans':loans,'contacts':contacts},sort_keys=True,separators=(',',':')).encode()).hexdigest();need(digest==audit['all_contact_witnesses_sha256'],'every contact record independently agrees');need(critical==audit['critical_witnesses'],'all61 critical witnesses')
 def backwards(r):
  row={r:F(1)}
  for e in reversed(ops[:28048]):
   op,d=e[:2];v=row.get(d,0)
   if not v:continue
   if op=='ADD':
    s=e[2];row[s]=row.get(s,0)+F(e[3])*v
    if not row[s]:del row[s]
   elif op=='COPY':
    del row[d];s=e[2];row[s]=row.get(s,0)+F(e[3])*v
    if not row[s]:del row[s]
   elif op=='SCALE':row[d]*=F(e[2])
   elif op in ('INIT','CLEAR'):del row[d]
  return row
 dirty={r:str(backwards(r).get(1477,F(0))) for r in (449,977,1206,1427)};need(dirty=={449:'1',977:'0',1206:'0',1427:'0'},'independent reverse dirty dual');need(1477 not in M,'arbitrary helper input');need(not any(e[0]=='MOVE' and e[3]==3 for e in ops),'no zero-chart arrivals')
 return {'status':'PASS_INDEPENDENT_CONTACT_CENSUS_AND_REVERSE_DIRTY_DUAL','native_sha256':PIN,'quiet_windows':len(loans),'recipient_contacts':len(contacts),'critical_contacts':len(critical),'all_contact_witnesses_sha256':digest,'dirty1477_reverse_coefficients':{str(k):v for k,v in dirty.items()},'method':'Forward active-window/cohort contact enumeration versus author interval method; reverse rational source adjoints versus author one-column forward replay. All exact records agree.','scope':'Individual raw shears in the fixed single-MOVE quiet family are replaceable contacts. Does not commute an interdependent coded circuit or prove supplier feasibility.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source,a.author_root);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
