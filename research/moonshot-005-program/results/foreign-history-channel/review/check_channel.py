#!/usr/bin/env python3
"""Independent adjoint/pulse proof and typed-word audit of the q47 -> q172 channel."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,hashlib,json
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'worker-coupling/foreign-history-channel';OUT=Path(__file__).resolve().parent
PINS={'source':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','word':'290d246a9de8f0355263ca2f4bcf1a90db6305058c4c7c414eb9e8c155d8df0c','certificate':'546ca7bf0ab8a958c7269d94143f3ec315e12e96eddbebed129b435ac59239e6','report':'4a031837c7edf8a72b712f88f3519573085fa239bc1ccb9fc2e28667dac01add','proof':'deb84343a691fdc5116ac73d64158b3e6ca8baa0be402e6a9fe3489c74a33ccc'}
def need(v,m):
 if not v:raise ValueError(m)
def clean(row):return {k:v for k,v in row.items() if v}
def baseline_relation(source,rel,late=False):
 adj={};timed={}
 for term in rel['arrival_terms']:
  e=term['after_event']+(1 if late and term['role']==1197 else 0)
  timed.setdefault(e,[]).append(term)
 for e in range(len(source['program'])-1,-1,-1):
  op=source['program'][e];kind,j=op[:2]
  for t in timed.get(e,[]):adj[t['role']]=adj.get(t['role'],F(0))+F(t['coefficient'])
  if kind in ('ADD','COPY'):
   adj[op[2]]=adj.get(op[2],F(0))+F(op[3])*adj.get(j,F(0))
   if kind=='COPY':adj.pop(j,None)
  elif kind=='SCALE':adj[j]=adj.get(j,F(0))*F(op[2])
  elif kind in ('INIT','CLEAR'):adj.pop(j,None)
  elif kind!='MOVE':raise ValueError(kind)
 for t in rel['initial_terms']:adj[t['role']]=adj.get(t['role'],F(0))+F(t['coefficient'])
 return clean(adj)
def pulse(source,rel):
 v={};guards=[];observations={};live=set(range(source['public']));arrival_cuts={t['after_event']:t for t in rel['arrival_terms']}
 for e,op in enumerate(source['program']):
  kind,j=op[:2]
  if e==31460:v[j]=v.get(j,F(0))+1
  if kind=='INIT':live.add(j);v[j]=F(0)
  elif kind=='CLEAR':live.remove(j);v.pop(j,None)
  elif kind=='SCALE':v[j]=v.get(j,F(0))*F(op[2])
  elif kind in ('ADD','COPY'):
   if kind=='COPY':guards.append({'event':e,'response':str(v.get(j,F(0)))});need(not v.get(j),'pulse preserves COPY guard')
   v[j]=v.get(j,F(0))+F(op[3])*v.get(op[2],F(0))
  elif kind!='MOVE':raise ValueError(kind)
  if e in arrival_cuts:
   t=arrival_cuts[e];need(op[0]=='MOVE' and op[1]==t['role'] and op[3]==t['chart'],'actual arrival version')
   observations[e]=v.get(t['role'],F(0))
 z=clean(v);need(all(j<1480 and source['final'][j]==127 for j in z),'all pulse debts are actual hub endpoints')
 gain=sum(F(t['coefficient'])*observations[t['after_event']] for t in rel['arrival_terms'])
 return z,gain,guards,observations

def spaces(source):
 out=[]
 for frame in source['frames']:
  s={0}
  for v in frame:s.update([x^v for x in s.copy()])
  out.append(s)
 return out

def typed_walk(source,word):
 loc=dict(enumerate(word['initial']));sub=spaces(source);counts=Counter();ranks=Counter();peak=0
 for e,op in enumerate(word['program']):
  kind,j=op[:2];counts[kind]+=1
  need(0<=j<word['public']+word['owned_fields'],'target namespace')
  if kind=='INIT':need(j>=1880 and j not in loc,'fresh owned INIT');loc[j]=op[2]
  elif kind=='CLEAR':need(j>=1880 and loc.get(j)==op[2],'actual owned CLEAR');del loc[j]
  elif kind=='MOVE':
   a,b,owned=op[2:];need(loc.get(j)==a and type(owned)is bool and owned==(j>=1880),'MOVE location/ownership')
   need(sub[a]<sub[b] or owned and sub[b]<sub[a],'proper nested transport')
   ranks[abs(len(source['frames'][a])-len(source['frames'][b]))]+=1;loc[j]=b
  elif kind in ('ADD','COPY'):
   k,c,chart=op[2:];need(j!=k and loc.get(j)==loc.get(k)==chart,'physical cochart arithmetic at '+str(e));F(c)
  elif kind=='SCALE':need(loc.get(j)==op[3] and F(op[2]),'cochart invertible SCALE')
  else:raise ValueError(kind)
  peak=max(peak,len(loc)-1880)
 need(set(loc)==set(range(1880)),'all owned lifetimes retired')
 for j in range(1480):need(loc[j]==source['final'][j],'common endpoint chart')
 for j,k in word['private_role_map'].items():need(loc[k]==source['final'][int(j)],'private endpoint chart')
 return counts,ranks,peak

def literal_structure(source,word,rel,z):
 main=sorted(set(source['live'])|{i+112 for i in source['live']}|set(source['hosted']['X2'])|set(source['hosted']['Y2']))
 raw={j:1480+i for i,j in enumerate(main)}
 need(len(main)==400 and {str(j):k for j,k in raw.items()}==word['private_role_map'],'actual complete main bank')
 need(word['initial']==source['initial']+[source['initial'][j] for j in main],'all 1880 initial locations')
 need(word['public']==1880 and word['owned_fields']==source['owned_fields'],'unchanged owned namespace')
 ops=word['program'];reservations=word['raw_reservations'];by_position={r['physical_event']:r for r in reservations}
 originals={i:o for i,o in enumerate(source['program']) if o[0]=='MOVE' and o[1] in raw}
 need(len(reservations)==len(by_position)==len(originals)==1710,'one record for each raw reservation')
 need({r['source_event'] for r in reservations}==set(originals),'all source raw reservations exactly once')
 for pos,r in by_position.items():
  op=originals[r['source_event']];need(r['role']==op[1] and ops[pos]==['MOVE',raw[op[1]],op[2],op[3],False],'literal mapped raw MOVE')
 need({i for i,o in enumerate(ops) if o[0]=='MOVE' and 1480<=o[1]<1880}==set(by_position),'no unpriced or unreported raw MOVE')
 cursor=0;positions={};marks={}
 def expect(op):
  nonlocal cursor
  while cursor in by_position:cursor+=1
  need(cursor<len(ops) and ops[cursor]==op,'literal word at '+str(cursor))
  pos=cursor;cursor+=1;return pos
 for j in main:expect(['ADD',raw[j],j,'-1',source['initial'][j]])
 for t in rel['initial_terms']:
  need(source['initial'][t['role']]==t['chart']==3,'real initial common term');expect(['ADD',raw[172],t['role'],str(-F(t['coefficient'])),3])
 arrival={t['after_event']:t for t in rel['arrival_terms']}
 rename=lambda j:j+400 if j>=1480 else j
 for e,op in enumerate(source['program']):
  if e==31460:marks['control']=expect(['ADD',1193,raw[47],'1',43])
  mapped=list(op);mapped[1]=rename(mapped[1])
  if mapped[0] in ('ADD','COPY'):mapped[2]=rename(mapped[2])
  positions[e]=expect(mapped)
  if e in arrival:
   t=arrival[e];marks['observation_'+str(e)]=expect(['ADD',raw[172],t['role'],str(-F(t['coefficient'])),t['chart']])
   if e==36811:marks['receiver_decoded']=cursor
 marks['common_finished']=cursor
 for j,c in sorted(z.items()):expect(['ADD',j,raw[47],str(-c),127])
 marks['common_restored']=cursor
 for j in main:expect(['ADD',raw[j],j,'1',source['final'][j]])
 need(cursor==len(ops) and marks==word['marks'],'no additional word instructions and exact milestones')
 return raw,positions,by_position

def main():
 raw=(REPO/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS['source'],'source pin');source=json.loads(gzip.decompress(raw))
 payload=gzip.decompress((PACK/'WORD.json.gz').read_bytes());need(hashlib.sha256(payload).hexdigest()==PINS['word'],'word payload pin');word=json.loads(payload)
 data={}
 for label,name in [('certificate','INPUT-CERTIFICATE.json'),('report','RESULT.json'),('proof','PROOF.md')]:
  b=(PACK/name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[label],'frozen '+label)
  if label!='proof':data[label]=json.loads(b)
 cert,author=data['certificate'],data['report'];rel=cert['candidate_channels'][0]['best_relation']
 need(word['source_sha256']==cert['source_sha256']==PINS['source'],'word and candidate refer to authenticated source')
 need(source['program'][31460]==['MOVE',1193,43,502,False],'actual injection source cut')
 need(len(rel['initial_terms'])==107 and len(rel['arrival_terms'])==2 and rel['receiver']==172,'declared decoder interface')
 need(not baseline_relation(source,rel),'independent full1480-input adjoint proves baseline relation')
 z,gain,guards,observed=pulse(source,rel)
 need(gain==-1 and len(z)==33 and {str(j):str(c) for j,c in z.items()}==cert['full_endpoint_response'],'independent pulse and hub response')
 need(guards==cert['COPY_guard_response'],'actual source COPY response')
 rawmap,positions,reservations=literal_structure(source,word,rel,z)
 counts,ranks,peak=typed_walk(source,word)
 need(dict(counts)==author['bill']['opcode_counts'] and {str(k):v for k,v in ranks.items()}==author['bill']['move_rank_histogram'] and peak==author['bill']['peak_owned']==43,'independent physical invoice')
 baseline=Counter(o[0] for o in source['program'])+Counter({'ADD':800,'MOVE':1710})
 delta={op:counts[op]-baseline[op] for op in ['ADD','SCALE','MOVE','INIT','CLEAR','COPY']}
 need(delta=={'ADD':143,'SCALE':0,'MOVE':0,'INIT':0,'CLEAR':0,'COPY':0},'all additional operation counts')
 # Authenticate the previously reviewed pure-payload grant, with receiver rows and donor columns.
 b=gzip.decompress((REPO/'research/moonshot-005-program/results/endpoint-side-information/EXPANDED.json.gz').read_bytes())
 need(hashlib.sha256(b).hexdigest()=='0df1ceb9babf6931572f7aa558ec8fadfe9ca2966540ca0d92a06a9d1b157864','expanded pure-payload grant pin')
 S=json.loads(b)['variants']['main_reuse_retimed47']['matrix'];xs=source['live']
 need(sum(map(sum,S))==1746 and S[xs.index(172-112)][xs.index(47)]==0,'actual candidate is outside the reviewed pure-payload grant')
 # Decoder, timing and physical-access controls.
 missing=dict(rel);missing['initial_terms']=rel['initial_terms'][1:];missing_row=baseline_relation(source,missing)
 need(missing_row=={34:F(-1)},'omitted-initial-term control')
 late_row=baseline_relation(source,rel,late=True);need(late_row,'one-event-late read must fail baseline identity')
 original_early=next(pos for pos,r in reservations.items() if r['role']==172 and r['source_event']==36809)
 mutated=list(word['program']);moved=mutated.pop(original_early);mutated.insert(positions[36809],moved)
 physical_failure=None
 try:typed_walk(source,dict(word,program=mutated))
 except ValueError as e:physical_failure=str(e)
 need(physical_failure and 'cochart' in physical_failure,'delayed receiver MOVE must fail actual observation access')
 need(z[3]==F(-1,4),'omitted-hub-repair residual')
 result={'status':'PASS_INDEPENDENT_FOREIGN_HISTORY_WORD_COMPOSITION','pins':PINS,'independent_baseline_method':'Exact backward adjoint of two arrival terms on all1480 common inputs','baseline_initial_terms':len(rel['initial_terms']),'timed_arrival_responses':{str(e):str(c) for e,c in observed.items()},'pulse_gain':str(gain),'hub_response_support':len(z),'offhub_response_support':0,'COPY_guard':guards,'instructions':len(word['program']),'opcode_counts':dict(counts),'move_rank_histogram':{str(k):v for k,v in sorted(ranks.items())},'peak_owned':peak,'increment':delta,'all400_boundary_pairs':True,'raw_reservations_once':len(reservations),'outside_pure_payload_S':True,'universal_endpoint_map':'common=Tu; private_i=(Tu)_i+q_i+1[i=172]q47, with q_i=v_i-u_i','negative_controls':{'omitted_initial_baseline_residual':{'34':'-1'},'late_read_baseline_residual_support':len(late_row),'late_read_first_residual':[min(late_row),str(late_row[min(late_row)])],'delayed_raw_MOVE':physical_failure,'omitted_hub_repair_at3':'-q47/4','wrong_decoder_sign':'-2q47'},'scope':'Independent exact compositional proof on all1880 independent inputs using the reviewed native baseline, plus literal instruction and physical type audit. Does not rerun the author full1880-column baseline replay. One cross-coordinate shear; no complete private native, supplier, composition or new kappa.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
