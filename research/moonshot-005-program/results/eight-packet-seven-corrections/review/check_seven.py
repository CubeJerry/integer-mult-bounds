#!/usr/bin/env python3
"""Independent joint five-controller and actual seven-term E8 word review."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import gzip,hashlib,json,importlib.util,time
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'worker-coupling/eight-packet-seven-corrections';BUDGET=BASE/'worker-budget/initial-line-controllers';OUT=Path(__file__).resolve().parent
WPIN='3cb2c8ef4b3f3d4c85703d3d737d4a2f570f380916d91fa0f00d8c3a768900cb';RPIN='cc668ed7c65c0b94f3095aba788e5911ca599aed043df78655f8f46ad0de05ce';PROOF='5bda343cc9e6f15b0d2ea3488afb80ac52da40a6bcb50efa8da844d26fd9819f';CPIN='bcc2bf5e5297dd3b81c24789e8b06035cc72466ce860be150fe9f6a24b297486';IPIN='cb8fcd6f9851645d0af11ded11734e0c19e0aea821b40b24ce23ac6efd95e086'
def need(a,b):
 if not a:raise ValueError(b)
def axpy(a,b,c):
 for k,v in b.items():
  v=a.get(k,F(0))+c*v
  if v:a[k]=v
  else:a.pop(k,None)
def rank(rows):
 basis={}
 for row in rows:
  row=row.copy()
  for p in sorted(basis):
   if p in row:axpy(row,basis[p],-row[p])
  if row:
   p=min(row);c=row[p];basis[p]={k:v/c for k,v in row.items()}
 return len(basis)
def own_helpers():
 p=BASE/'worker-review/eight-packet-one-correction/check_composition.py';need(hashlib.sha256(p.read_bytes()).hexdigest()=='a089410089d0c57549379cc51c3dd09829b3cc9f0ee209d3e0ab2d53462aa473','own independent E8 review pin')
 spec=importlib.util.spec_from_file_location('review_e8_helpers',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m,m.import_own_channel_checker()

def check_all_baselines(source,relations):
 timed=defaultdict(list);adj={};start=time.monotonic()
 for i,r in enumerate(relations):
  for t in r['arrival_terms']:timed[t['after_event']].append((t['role'],i,F(t['coefficient'])))
 scalars={}
 for event in range(len(source['program'])-1,-1,-1):
  op=source['program'][event];kind,j=op[:2]
  for role,i,c in timed.get(event,[]):axpy(adj.setdefault(role,{}),{i:c},F(1))
  if kind in ('ADD','COPY'):
   c=scalars.setdefault(op[3],F(op[3]));axpy(adj.setdefault(op[2],{}),adj.get(j,{}),c)
   if kind=='COPY':adj[j]={}
  elif kind=='SCALE':
   c=scalars.setdefault(op[2],F(op[2]));adj[j]={i:c*v for i,v in adj.get(j,{}).items() if c*v}
  elif kind in ('INIT','CLEAR'):adj[j]={}
  elif kind!='MOVE':raise ValueError(kind)
  if event%20000==0:print('FULL_NULL_ADJOINT',event,'seconds',round(time.monotonic()-start,2),flush=True)
 for i,r in enumerate(relations):
  for t in r['initial_terms']:
   need(source['initial'][t['role']]==t['chart'],'actual initial chart in full null identity')
   axpy(adj.setdefault(t['role'],{}),{i:F(t['coefficient'])},F(1))
 need(all(not row for row in adj.values()),'all1486 full-input null identities')

def check_complete_interface(source,relations,helper):
 cert=gzip.decompress((BASE/'worker-review/owned-history/CERTIFICATE.json.gz').read_bytes())
 need(hashlib.sha256(cert).hexdigest()=='a6e6efe3e4e1df2f2f62d47796f089470bbec168a6dd5c28a2217d9b63ba5611','independent original-history rank certificate')
 old={r['receiver']:r for r in json.loads(cert)['receivers']}
 first={};canon=[first.setdefault(frozenset(s),i) for i,s in enumerate(helper.spaces(source))]
 byreceiver=defaultdict(list)
 for r in relations:byreceiver[r['receiver']].append(r)
 need(set(byreceiver)==set(old) and len(relations)==1486,'all104 complete null families')
 for receiver,rows in byreceiver.items():
  route={canon[source['initial'][receiver]]}|{canon[o[3]] for o in source['program'] if o[0]=='MOVE' and o[1]==receiver}
  known={j for j,c in enumerate(source['initial']) if canon[c] in route}
  arrivals={e for e,o in enumerate(source['program']) if o[0]=='MOVE' and canon[o[3]] in route}
  matrix=[]
  for r in rows:
   v={}
   for t in r['arrival_terms']:
    e=t['after_event'];o=source['program'][e]
    need(e in arrivals and o[1]==t['role'] and o[3]==t['chart'],'actual granted arrival in full null family')
    v[e]=v.get(e,F(0))+F(t['coefficient'])
   for t in r['initial_terms']:need(t['role'] in known,'actual initially granted common input')
   matrix.append({k:v for k,v in v.items() if v})
  previous=old[receiver]
  need(len(known)==previous['initial_count'] and len(arrivals)==previous['arrivals'],'same independently reviewed observation interface')
  need(len(rows)==rank(matrix)==len(arrivals)-previous['common_rank'],'complete independent original common null basis')

def joint_pulse(source,certificate,relations):
 donors=certificate['donor_order'];scaling={int(d):F(c) for d,c in certificate['weighted_partial_E8_construction']['donor_control_scalings'].items()}
 controls=defaultdict(list)
 for family in certificate['families']:
  d=family['donor'];need(family['chart']==source['initial'][d],'actual donor initial controller chart')
  for control in family['controls']:controls[control['before_event']].append(dict(control,donor=d,coefficient=F(control['coefficient'])*scaling[d]))
 needed={t['after_event'] for r in relations for t in r['arrival_terms']};state={j:{} for j in range(source['public'])};loc=dict(enumerate(source['initial']));observed={};guards=[]
 for e,op in enumerate(source['program']):
  kind,j=op[:2]
  for ctl in controls.get(e,[]):
   need(loc[ctl['role']]==ctl['chart']==source['initial'][ctl['donor']],'exact current controller chart')
   axpy(state[ctl['role']],{ctl['donor']:ctl['coefficient']},F(1))
  if kind=='INIT':state[j]={};loc[j]=op[2]
  elif kind=='CLEAR':del state[j],loc[j]
  elif kind=='SCALE':state[j]={d:F(op[2])*v for d,v in state[j].items() if F(op[2])*v}
  elif kind in ('ADD','COPY'):
   if kind=='COPY':need(not state[j],'all five COPY responses vanish');guards.append(e)
   axpy(state[j],state[op[2]],F(op[3]))
  elif kind=='MOVE':need(loc[j]==op[2],'native location trace');loc[j]=op[3]
  else:raise ValueError(kind)
  if e in needed:observed[e]=state[j].copy()
 Z={j:row for j,row in state.items() if row};need(all(j<1480 and source['final'][j]==127 for j in Z),'joint debt entirely at actual hub')
 for family in certificate['families']:
  d=family['donor'];want={int(j):F(v)*scaling[d] for j,v in family['hub_response'].items()}
  need({j:row[d] for j,row in Z.items() if row.get(d)}==want,'independent full donor endpoint response')
 gain={}
 for r in relations:
  value={}
  for t in r['arrival_terms']:axpy(value,observed[t['after_event']],F(t['coefficient']))
  gain[r['receiver'],r['relation']]=value
 want={(r['receiver'],r['relation']):{d:F(v)*scaling[d] for d,v in zip(donors,r['row']) if F(v)} for r in certificate['all_receiver_null_response_rows']}
 need({key:v for key,v in gain.items() if v}==want,'all1486 actual five-column null responses')
 need(rank(list(gain.values()))==4 and all(row.get(37,F(0))==row.get(47,F(0)) for row in gain.values()),'joint signal rank4 and inseparable37/47 aggregate')
 return donors,controls,Z,gain,guards

def main():
 mod,helper=own_helpers();source=mod.read_source();start_time=time.monotonic()
 b=(PACK/'INPUT-CONTROLLERS.json').read_bytes();need(b==(BUDGET/'CERTIFICATE.json').read_bytes() and hashlib.sha256(b).hexdigest()==CPIN,'frozen five-controller certificate');certificate=json.loads(b)
 b=gzip.decompress((BUDGET/'INPUT.json.gz').read_bytes());need(hashlib.sha256(b).hexdigest()==IPIN,'full history input pin');inputs=json.loads(b);relations=inputs['history']['complete_null_relations']
 need(certificate['source_sha256']==inputs['source_sha256']==mod.SPIN,'same authenticated native')
 b=gzip.decompress((PACK/'INPUT-PREFIX.json.gz').read_bytes());need(hashlib.sha256(b).hexdigest()==mod.PPIN,'retained prefix pin');prefix=json.loads(b)
 need(b==gzip.decompress((REPO/'research/moonshot-005-program/results/eight-packet-prefix/PREFIX.json.gz').read_bytes()),'exact published prefix')
 b=gzip.decompress((PACK/'WORD.json.gz').read_bytes());need(hashlib.sha256(b).hexdigest()==WPIN,'composed word pin');word=json.loads(b)
 b=(PACK/'RESULT.json').read_bytes();need(hashlib.sha256(b).hexdigest()==RPIN,'frozen result pin');report=json.loads(b)
 need(hashlib.sha256((PACK/'PROOF.md').read_bytes()).hexdigest()==PROOF,'frozen proof pin')
 check_complete_interface(source,relations,helper);check_all_baselines(source,relations)
 donors,controls,Z,gains,guards=joint_pulse(source,certificate,relations)
 raw,expected,G,c=mod.prefix_map(source,prefix);xs=source['live'];decoders=certificate['weighted_partial_E8_construction']['decoders'];allrelations={(r['receiver'],r['relation']):r for r in relations}
 correction={};initial_terms=0;arrival_terms=0
 for dec in decoders:
  full=allrelations[dec['receiver'],dec['relation']]
  need(dec['initial_terms']==full['initial_terms'] and dec['arrival_terms']==full['arrival_terms'],'selected actual history identity')
  multiplier=F(dec['decoder_scale'])*c[dec['receiver']-112]
  correction[dec['receiver']]={d:multiplier*v for d,v in gains[dec['receiver'],dec['relation']].items()}
  initial_terms+=len(dec['initial_terms']);arrival_terms+=len(dec['arrival_terms'])
 need(correction[172]=={37:F(-1,4),47:F(-1,4)} and rank(list(correction.values()))==4,'actual weighted aggregate at receiver172')
 need({str(r):[[d,str(v)] for d,v in sorted(row.items())] for r,row in correction.items()}==word['corrections'],'all recorded actual correction rows')
 need(len(Z)==350 and sum(map(len,Z.values()))==1014,'full joint hub repair census')
 ops=word['program'];pp=prefix['program'];pmap={int(e):pos for e,pos in word['prefix_event_to_physical'].items()};nmap=word['native_event_to_physical'];marks=word['marks'];caches={int(d):role for d,role in word['donor_caches'].items()}
 need(word['source_sha256']==mod.SPIN and word['prefix_decompressed_sha256']==mod.PPIN and word['controller_certificate_sha256']==CPIN,'word input bindings')
 need(word['private_role_map']==prefix['difference_role_map'] and word['initial']==prefix['initial'] and word['public']==1880 and word['owned_fields']==57,'actual complete field interface')
 need(caches=={d:1932+i for i,d in enumerate(donors)},'distinct stationary cache labels')
 covered=set()
 def claim(pos,wanted):
  need(pos not in covered and 0<=pos<len(ops) and ops[pos]==wanted,'exact word coverage at '+str(pos));covered.add(pos)
 need(set(pmap)==set(range(2362)) and len(set(pmap.values()))==2362,'prefix instructions once')
 for e,pos in pmap.items():claim(pos,pp[e])
 need(len(nmap)==71261 and nmap==sorted(set(nmap)),'unchanged ordered full native')
 rename=lambda r:r+400 if r>=1480 else r
 for e,pos in enumerate(nmap):
  op=list(source['program'][e]);op[1]=rename(op[1])
  if op[0] in ('ADD','COPY'):op[2]=rename(op[2])
  claim(pos,op)
 need(nmap[0]==marks['common_starts'] and nmap[-1]+1==marks['common_finished'],'actual native boundaries')
 need([pmap[e] for e in range(400)]==list(range(400)),'all actual differences precede caches')
 scalar_positions=[pmap[e] for e,o in enumerate(pp) if o[0]!='MOVE'];need(scalar_positions==sorted(scalar_positions) and max(scalar_positions)<marks['common_starts'],'prefix arithmetic order and early completion')
 for i,d in enumerate(donors):
  claim(400+2*i,['INIT',caches[d],source['initial'][d]]);claim(401+2*i,['ADD',caches[d],raw[d],'1',source['initial'][d]])
 need(marks['cache_acquisitions']==400,'cache acquisition cut')
 original={e:o for e,o in enumerate(source['program']) if o[0]=='MOVE' and o[1] in raw};reservations=word['raw_reservations'];rmap={r['source_event']:r for r in reservations};pr={r['source_event']:r for r in prefix['reservations']}
 need(len(rmap)==len(reservations)==len(original)==1710 and set(rmap)==set(original) and len(pr)==890,'all raw reservations exactly once')
 actual_routes=defaultdict(list);delayed=[]
 for r in sorted(reservations,key=lambda r:r['physical_event']):
  e=r['source_event'];o=original[e];pos=r['physical_event'];actual_routes[o[1]].append(e)
  need(r['role']==o[1] and ops[pos]==['MOVE',raw[o[1]],o[2],o[3],False],'exact original raw leg')
  if e in pr:
   pe=pr[e]['physical_event'];need(r['prefix_event']==pe and pmap[pe]==pos,'prefix reservation preserved')
   if pos>marks['common_starts']:delayed.append(e)
  else:
   need(r.get('prefix_event') is None and pos<marks['common_starts'],'remaining820 routes completed before native')
   claim(pos,['MOVE',raw[o[1]],o[2],o[3],False])
 for role,events in actual_routes.items():need(events==sorted(e for e,o in original.items() if o[1]==role),'every carrier retains original route order')
 need(len(delayed)==9,'nine original receiver suffix reservations delayed causally')
 need({p for p,o in enumerate(ops) if o[0]=='MOVE' and 1480<=o[1]<1880}=={r['physical_event'] for r in reservations},'no additional raw MOVE')
 offset=0
 for dec in decoders:
  receiver=dec['receiver'];multiplier=F(dec['decoder_scale'])*c[receiver-112]
  for t in dec['initial_terms']:
   need(source['initial'][t['role']]==t['chart']==3,'actual initial cochart decoder term')
   claim(marks['initial_decoders']+offset,['ADD',raw[receiver],t['role'],str(multiplier*F(t['coefficient'])),3]);offset+=1
  need(all(pmap[e]<marks['initial_decoders'] for e,o in enumerate(pp) if o[0] in ('ADD','SCALE','COPY') and o[1]==raw[receiver]),'normalizations and packet mixtures precede common-noise accumulation')
 need(offset==initial_terms==164 and marks['initial_decoders']+offset<marks['common_starts'],'all initial terms before native')
 last_control={d:max(e for e,ctls in controls.items() if any(t['donor']==d for t in ctls)) for d in donors};control_positions={}
 for e,ctls in controls.items():
  for ctl in ctls:
   d=ctl['donor'];pos=marks['control_'+str(d)+'_'+str(e)];control_positions[e]=min(control_positions.get(e,pos),pos)
   claim(pos,['ADD',ctl['role'],caches[d],str(ctl['coefficient']),ctl['chart']])
   need((nmap[e-1] if e else -1)<pos<nmap[e],'exact controller source cut')
   if e==last_control[d]:claim(pos+1,['CLEAR',caches[d],ctl['chart']]);need(pos+1<nmap[e],'cache cleared only after last actual use')
 for dec in decoders:
  receiver=dec['receiver'];multiplier=F(dec['decoder_scale'])*c[receiver-112];reads=[]
  for t in dec['arrival_terms']:
   e=t['after_event'];pos=marks['observation_'+str(receiver)+'_'+str(e)];reads.append(pos)
   claim(pos,['ADD',raw[receiver],t['role'],str(multiplier*F(t['coefficient'])),t['chart']])
   need(nmap[e]<pos<(control_positions.get(e+1,nmap[e+1]) if e+1<len(nmap) else len(ops)),'actual post-arrival version before next-source change')
  completed=marks['receiver_corrected_'+str(receiver)]
  need(completed>max(reads) and all(raw[receiver] not in (op[1:3] if op[0] in ('ADD','COPY') else op[1:2]) for op in ops[max(reads)+1:completed]),'decoder completion marker follows its last read without an intervening own-field change')
 repair_start=marks['common_finished'];repair_ops=Counter(tuple(['ADD',r,raw[d],str(-v),127]) for r,row in Z.items() for d,v in row.items())
 actual_repairs=ops[repair_start:repair_start+1014];need(Counter(map(tuple,actual_repairs))==repair_ops,'every exact hub correction coefficient present')
 for pos,op in enumerate(actual_repairs,repair_start):claim(pos,op)
 need(marks['common_restored']==repair_start+1014,'all hub debt repaired before recoupling')
 for offset,r in enumerate(sorted(raw)):claim(marks['common_restored']+offset,['ADD',raw[r],r,'1',source['final'][r]])
 need(covered==set(range(len(ops))),'complete literal word has no omitted or extra instruction')
 counts,ranks,peak=helper.typed_walk(source,word)
 need(dict(counts)==report['bill']['opcode_counts'] and {str(k):v for k,v in ranks.items()}==report['bill']['move_rank_histogram'] and peak==43,'fresh full physical invoice')
 native=Counter(o[0] for o in source['program']);pc=Counter(o[0] for o in pp);opcodes=['ADD','SCALE','MOVE','INIT','CLEAR','COPY']
 extras={o:pc[o]-(400 if o=='ADD' else 890 if o=='MOVE' else 0) for o in opcodes};baseline=native+Counter({'ADD':800,'MOVE':1710})+Counter(extras)
 increment={o:counts[o]-baseline[o] for o in opcodes};need(increment==report['increment_beyond_common_raw_boundaries_and_E8']=={'ADD':1207,'SCALE':0,'MOVE':0,'INIT':5,'CLEAR':5,'COPY':0},'complete seven-term incremental cost')
 need(initial_terms+arrival_terms==178 and sum(map(len,controls.values()))==10 and 178+10+1014+5==1207,'all new additions accounted')
 corrected={r:row.copy() for r,row in expected.items()};changed=[]
 for receiver,row in correction.items():
  for d,value in row.items():
   need(d!=receiver-112 and expected[receiver].get(d)==-value,'correction cancels the actual weighted Gram coefficient')
   changed.append((receiver,d))
  axpy(corrected[receiver],row,F(1))
 need(len(changed)==7 and all(d not in corrected[r] for r,d in changed),'seven designated coefficients vanish')
 actual_changes={(r,d) for r in raw for d in set(expected[r])|set(corrected[r]) if expected[r].get(d,F(0))!=corrected[r].get(d,F(0))}
 need(actual_changes==set(changed),'no other raw coefficient changes')
 remaining={}
 for i,x in enumerate(xs):remaining[x+112]=sum(d!=x and corrected[x+112].get(d,F(0))!=0 for d in xs)
 need(sum(remaining.values())==4985 and min(remaining.values())>0,'all4985 other offdiagonal terms remain and no receiver complete')
 need({str(r):remaining[r] for r in correction}==report['remaining_at_selected_receivers'],'selected receiver residual census')
 inverse=0
 for r in raw:
  if r-112 in c:
   x=r-112;i=xs.index(x);row={d:v/c[x] for d,v in corrected[r].items()}
   for j,d in enumerate(xs):
    if G[i][j]:axpy(row,corrected[d],-F(G[i][j],8))
   for d,v in correction.get(r,{}).items():axpy(row,corrected[d],-v/c[x])
  else:row=corrected[r].copy()
  need(row=={r:F(1)},'explicit inverse of complete400-coordinate private map');inverse+=1
 need(rank(list(gains.values())+[{37:F(1)}])==5,'unavailable individual q37 direction is outside rank4 history span')
 mutants=[]
 for d in donors:
  altered=json.loads(json.dumps(certificate));next(f for f in altered['families'] if f['donor']==d)['controls'].pop(0)
  failure=None
  try:joint_pulse(source,altered,relations)
  except ValueError as e:failure=str(e)
  need(failure is not None,'deleted-control mutant rejected');mutants.append({'donor':d,'failure':failure})
 affected=sorted({r for (r,k),row in gains.items() if row});need(len(affected)==6,'other98 original null interfaces have zero response')
 result={'status':'PASS_INDEPENDENT_FIVE_CONTROLLER_SEVEN_CORRECTION_WORD','source_sha256':mod.SPIN,'prefix_payload_sha256':mod.PPIN,'controller_certificate_sha256':CPIN,'all_history_input_payload_sha256':IPIN,'word_payload_sha256':WPIN,'author_result_sha256':RPIN,'reviewed_proof_sha256':PROOF,'full_input_null_identities_checked':len(relations),'complete_receiver_null_families':104,'joint_all1486_history_rank':4,'joint_donor37_and47_columns_equal':True,'nonzero_history_receivers':affected,'zero_history_receivers':98,'source_controls':sum(map(len,controls.values())),'source_COPY_guards':guards,'hub_endpoint_support':len(Z),'hub_scalar_repairs':sum(map(len,Z.values())),'weighted_corrections':{str(r):{str(d):str(v) for d,v in sorted(row.items())} for r,row in correction.items()},'prefix_ops_retained_once':len(pmap),'native_ops_retained_in_order':len(nmap),'raw_reservations_once':len(rmap),'prefix_raw_reservations_once':len(pr),'other_raw_reservations':len(rmap)-len(pr),'delayed_prefix_raw_reservations':sorted(delayed),'stationary_cache_lifetimes':len(caches),'extra_cache_MOVEs':0,'initial_decoder_terms':initial_terms,'arrival_decoder_terms':arrival_terms,'instructions':len(ops),'opcode_counts':dict(counts),'MOVE_histogram':{str(k):v for k,v in sorted(ranks.items())},'peak_owned':peak,'increment_beyond_complete_E8_baseline':increment,'common_rows_restored':1480,'private_inverse_rows':inverse,'corrected_terms':7,'all_other_coefficients_unchanged':True,'remaining_terms':sum(remaining.values()),'completed_first_receivers':0,'negative_controls':{'individual_q37_target_increases_history_rank_to':5,'delete_first_control':mutants},'scope':'Independent simultaneous full1480-input null adjoints and five-column source replay, source-derived E8 prefix algebra, complete literal word/physical audit, and universal1880-input composition proof with explicit400-row inverse. Baseline history ranks reuse the prior independently checked immutable-source certificate. No dense1880 native replay, author verifier imports, full supplier or new kappa.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,indent=2));print('ELAPSED',round(time.monotonic()-start_time,2),flush=True)
if __name__=='__main__':main()
