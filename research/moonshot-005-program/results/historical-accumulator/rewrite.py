"""Literal normalized difference-rail rewrite, conditional on physical rail supply.
Public helper differences enter as known zero; this is NOT a full all-column
native certificate or an admission of those helper fields under H4.
"""
import argparse,gzip,hashlib,json
from collections import defaultdict,Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE='research/shared-wire-split-composition/data/final.json.gz'
def default_source():
 for p in Path(__file__).resolve().parents:
  for b in (p,p/'moonshot'):
   if (b/SOURCE).is_file():return b/SOURCE
 return Path(SOURCE)
def default_certificate():
 here=Path(__file__).resolve().parent
 for p in (here/'WITNESSES.json',here.parent/'historical-owned'/'WITNESSES.json'):
  if p.is_file():return p
 return here/'WITNESSES.json' 
def need(c,m):
 if not c:raise ValueError(m)
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def span(a):
 s={0}
 for v in a:s|={x^v for x in s}
 return s
def build(w,cert):
 N=w['public']+w['owned_fields'];mapping={r:r for r in range(N)};after=defaultdict(list);returns={};acc={};initialized=set();program=[];rebindings=[]
 for j,c in enumerate(cert):
  z=N+j;acc[c['event']]=z;returns[c['event']]=c
  for term in c['witnesses']['all']:
   o=term['observation'];need(o['phase']=='after' and o['event']<c['event'],'chronological observation');after[o['event']].append((c,z,term))
 for k,e in enumerate(w['program']):
  op,r=e[:2]
  if op=='INIT':mapping[r]=r
  if k in returns:
   c=returns[k];z=acc[k];need(e==['MOVE',c['owner'],c['from'],c['to'],True],'owned return pin');need(z in initialized,'ready accumulator');old=mapping[r];at=len(program);program.append(['CLEAR',old,c['from']]);mapping[r]=z;rebindings.append({'physical_before_event':at,'event':k,'logical_owner':r,'old_physical_owner':old,'new_physical_owner':z,'destination':c['to']})
  else:
   x=e[:];x[1]=mapping[r]
   if op in ('ADD','COPY'):x[2]=mapping[e[2]]
   program.append(x)
  for c,z,t in after.get(k,()):
   o=t['observation'];need(o['chart']==c['to'],'stationary accumulator chart')
   if z not in initialized:program.append(['INIT',z,c['to']]);initialized.add(z)
   program.append(['ADD',z,mapping[o['role']],t['coefficient'],c['to']])
 return program,rebindings

def replay(w,ops,extra,checks=()):
 p=w['public'];N=p+w['owned_fields']+extra;M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);rows=[{r:F(1)} if r in M else {} for r in range(N)];cur=w['initial'][:]+[None]*(N-p);live=set(range(p));counts=Counter();hist=Counter();peak=life=0;spans=list(map(span,w['frames']))
 check_at={x['physical_before_event']:x for x in checks}
 for k,e in enumerate(ops):
  if k in check_at:
   c=check_at[k];need(rows[c['old_physical_owner']]==rows[c['new_physical_owner']],'exact accumulator return row');need(cur[c['new_physical_owner']]==c['destination'],'accumulator current destination')
  op,r=e[:2];need(0<=r<N,'physical owner');counts[op]+=1
  if op=='INIT':need(r>=p and r not in live,'owned init');live.add(r);cur[r]=e[2];rows[r]={};life+=1
  elif op=='CLEAR':need(r>=p and r in live and cur[r]==e[2],'owned clear');live.remove(r);cur[r]=None;rows[r]={}
  elif op=='MOVE':
   need(r in live and cur[r]==e[2] and type(e[4]) is bool and e[4]==(r>=p),'typed MOVE');a,b=spans[e[2]],spans[e[3]];need(a<b or r>=p and b<a,'nested MOVE');cur[r]=e[3];hist[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
  elif op in ('ADD','COPY'):
   s=e[2];need(r!=s and r in live and s in live and cur[r]==cur[s]==e[4],'actual cochart ADD');c=F(e[3]);need(c!=0,'nonzero coefficient')
   if op=='COPY':need(not rows[r],'zero COPY')
   add(rows[r],rows[s],c)
  elif op=='SCALE':need(r in live and cur[r]==e[3] and F(e[2]),'SCALE');rows[r]={j:v*F(e[2]) for j,v in rows[r].items()}
  else:raise ValueError(op)
  peak=max(peak,len(live)-p)
 return rows,cur,{'counts':dict(counts),'move_histogram':dict(sorted(hist.items())),'peak_owned':peak,'owned_lifetimes':life,'final_live_owned':len(live)-p}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=default_source());ap.add_argument('--certificate',type=Path,default=default_certificate());ap.add_argument('--output',type=Path);ap.add_argument('--transcript',type=Path);a=ap.parse_args();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source SHA');w=json.loads(gzip.decompress(raw));cert=json.loads(a.certificate.read_text());ops,rebind=build(w,cert);rows,cur,bill=replay(w,ops,len(cert),rebind);base,bcur,bbill=replay(w,w['program'],0);need(rows[:w['public']]==base[:w['public']] and cur[:w['public']]==bcur[:w['public']],'all public difference endpoints');need(not bill['final_live_owned'],'all owned retired')
 diff=Counter(bill['counts']);diff.subtract(bbill['counts']);saved=Counter(bbill['move_histogram']);saved.subtract(bill['move_histogram']);need(dict(+saved)=={2:3,5:1},'four exact MOVE savings');need(diff['ADD']==9 and diff['INIT']==4 and diff['CLEAR']==4 and diff['MOVE']==-4 and all(v==0 for k,v in diff.items() if k not in ('ADD','INIT','CLEAR','MOVE')),'exact scalar lifecycle increment')
 # Each mutated future version must be independently rejected by geometry or rows.
 controls=[]
 for name in ('wrong_historical_coefficient','wrong_accumulator_chart','omit_rebinding'):
  c=json.loads(json.dumps(cert))
  if name=='wrong_historical_coefficient':c[0]['witnesses']['all'][0]['coefficient']='4'
  elif name=='wrong_accumulator_chart':c[0]['witnesses']['all'][0]['observation']['chart']=3
  try:
   bad,_=build(w,c)
   if name=='omit_rebinding':
    idx=next(i for i,e in enumerate(bad) if e[0]=='CLEAR' and e[1]==cert[0]['owner'] and e[2]==cert[0]['from']);bad[idx]=['MOVE',cert[0]['owner'],cert[0]['from'],cert[0]['to'],True]
   b,bc,bi=replay(w,bad,len(c));need(b[:w['public']]==base[:w['public']] and not bi['final_live_owned'],'mutated final effect')
  except ValueError as ex:controls.append({'name':name,'rejected':str(ex)})
  else:raise ValueError('negative control accepted '+name)
 t={'schema':'moonshot-historical-accumulator-difference-rail-v1','source_sha256':PIN,'public':w['public'],'owned_fields':w['owned_fields']+len(cert),'initial':w['initial'],'frames':w['frames'],'main_roles':sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])),'initial_helper_differences':'zero, conditional supplied physical rail','program':ops,'rebindings':rebind};payload=(json.dumps(t,sort_keys=True,separators=(',',':'))+'\n').encode();result={'status':'PASS_CONDITIONAL_LITERAL_DIFFERENCE_RAIL','source_sha256':PIN,'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'public_difference_rows_checked':w['public'],'independent_main_difference_inputs':400,'baseline':bbill,'rewritten':bill,'saved_MOVE_histogram':dict(+saved),'operation_changes':dict(diff),'rebindings':rebind,'negative_controls':controls,'scope':'Conditional complete difference-rail rewrite only. All helper difference availability, the full shared native, source control/precision and five assumptions remain explicit. No new kappa.'}
 if a.transcript:a.transcript.write_bytes(gzip.compress(payload,mtime=0))
 if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
