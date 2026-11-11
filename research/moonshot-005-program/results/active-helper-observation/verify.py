#!/usr/bin/env python3
"""Source-authentic historical observations; common endpoint repair stays open."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def add(a,b,c):
 z=a.copy()
 for i,v in b.items():
  t=z.get(i,F(0))+c*v
  if t:z[i]=t
  else:z.pop(i,None)
 return z
def ser(a):return {str(i):str(v) for i,v in sorted(a.items())}
def span(a):
 s={0}
 for v in a:s.update(x^v for x in tuple(s))
 return frozenset(s)
def source_check(w,items):
 pub=w['public'];N=pub+w['owned_fields'];P=w['program'];rows=[{i:F(1)} for i in range(pub)]+[{} for _ in range(w['owned_fields'])];sens=[{} for _ in range(N)];chart=dict(enumerate(w['initial']));events={x['event']:i for i,x in enumerate(items)};obs=collections.defaultdict(list);decoded=[{} for _ in items];beta=[F(0) for _ in items];paths={};actualcharts=[[] for _ in items];cutrows={};copyguards={};source_reads={}
 need(len(events)==len(items)==31,'31 distinct selected cuts')
 for i,x in enumerate(items):
  for t in x['historical_decoder']:obs[t['after_event']].append((i,t))
  y=x['receiver'];paths[y]=[w['initial'][y]]+[e[3] for e in P if e[0]=='MOVE' and e[1]==y]
  donorpath=[w['initial'][x['donor']]]+[e[3] for e in P if e[0]=='MOVE' and e[1]==x['donor']]
  need(x['source_chart'] in donorpath and x['donor']!=y,'actual donor route and distinct recipient')
 def observe(k):
  for i,t in obs[k]:
   r=t['role'];c=F(t['coefficient']);need(chart[r]==t['chart'],'actual exact source chart');decoded[i]=add(decoded[i],rows[r],c);beta[i]+=c*sens[r].get(i,F(0));actualcharts[i].append(chart[r]);source_reads[(k,r)]=rows[r].copy()
 observe(-1)
 for k,e in enumerate(P):
  if k in events:
   i=events[k];x=items[i];h=x['helper'];need(e[:2]==['MOVE',h] and e[2]==x['source_chart'],'actual loan source event');cutrows[i]=rows[h].copy();sens[h][i]=F(1)
  op,r=e[:2]
  if op=='ADD':rows[r]=add(rows[r],rows[e[2]],F(e[3]));sens[r]=add(sens[r],sens[e[2]],F(e[3]))
  elif op=='SCALE':rows[r]={i:F(e[2])*v for i,v in rows[r].items()};sens[r]={i:F(e[2])*v for i,v in sens[r].items()}
  elif op=='COPY':need(not rows[r],'reference COPY zero');copyguards[k]=sens[r].copy();rows[r]={i:F(e[3])*v for i,v in rows[e[2]].items()};sens[r]={i:F(e[3])*v for i,v in sens[e[2]].items()}
  elif op=='INIT':rows[r]={};sens[r]={};chart[r]=e[2]
  elif op=='CLEAR':rows[r]={};sens[r]={};chart.pop(r)
  elif op=='MOVE':need(chart[r]==e[2],'source MOVE');chart[r]=e[3]
  observe(k)
 summaries=[];responses=[]
 for i,x in enumerate(items):
  a={int(k):F(v) for k,v in x['hrow'].items()};need(decoded[i]==cutrows[i]==a,'all1480-input historical/helper identity');need(beta[i]==F(x['decoder_sensitivity']) and beta[i]!=0,'actual nonzero gain');g=F(x['gain']);need(g*beta[i]==1,'gain normalization');need(all(i not in z for z in copyguards.values()),'COPY perturbation guard');b={}
  for r,c in x['lambda_hub'].items():r=int(r);need(w['final'][r]==127,'actual hub recovery chart');b=add(b,rows[r],F(c))
  need(a==b,'full-input hub recovery');z={r:row[i] for r,row in enumerate(sens[:pub]) if i in row};off={r:v for r,v in z.items() if w['final'][r]!=127};need(ser(off)==x['offhub_suffix_rows'] and len(off)==x['offhub_suffix_support'] and len(z)==x['public_suffix_support'],'all endpoint response rows');responses.append(z)
  last=0;ordered=True
  need(set(actualcharts[i])<=set(paths[x['receiver']]),'every observation chart on actual receiver route')
  for f in actualcharts[i]:
   hits=[j for j in range(last,len(paths[x['receiver']])) if paths[x['receiver']][j]==f]
   if hits:last=hits[0]
   else:ordered=False
  need(ordered==x['strict_receiver_itinerary_order'],'receiver chronology');L=len(set(actualcharts[i]));need(L==x['stationary_accumulators_if_clock_waived'],'stationary accumulator count')
  summaries.append({'event':x['event'],'donor':x['donor'],'receiver':x['receiver'],'gain':str(g),'decoder_terms':len(x['historical_decoder']),'direct_accumulation_ordered':ordered,'stationary_accumulators':L,'offhub_residual_fields':len(off)})
 return rows[:pub],responses,summaries,source_reads
def build(w,selected):
 M=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));qm={i:1480+j for j,i in enumerate(M)};Q=qm[77];R=qm[189];ops=[];reservations=[];marks={};loan=selected['event'];bytime=collections.defaultdict(list)
 for t in selected['historical_decoder']:bytime[t['after_event']].append(t)
 def append(e):ops.append(e)
 def raw_move(k,e):reservations.append({'source_event':k,'physical_event':len(ops),'main_role':e[1]});append(['MOVE',qm[e[1]],e[2],e[3],False])
 for i in M:append(['ADD',qm[i],i,'-1',w['initial'][i]])
 for t in bytime[-1]:append(['ADD',R,t['role'],t['coefficient'],t['chart']])
 for k,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1] in qm and e[1]!=77:raw_move(k,e)
 for k,e in enumerate(w['program']):
  if k==loan:
   marks['loan_physical_event']=len(ops);append(['ADD',Q,287,'-1',71]);append(['ADD',287,Q,'1',71])
   for kk,ee in enumerate(w['program']):
    if ee[0]=='MOVE' and ee[1]==77:raw_move(kk,ee)
  f=e.copy();f[1]=f[1]+400 if f[1]>=1480 else f[1]
  if f[0] in ('ADD','COPY'):f[2]=f[2]+400 if f[2]>=1480 else f[2]
  append(f)
  for t in bytime[k]:append(['ADD',R,t['role']+400 if t['role']>=1480 else t['role'],t['coefficient'],t['chart']])
 need(len(reservations)==1710 and len({r['source_event'] for r in reservations})==1710,'each raw reservation exactly once')
 return {'status':'ACTUAL_1880_INPUT_OBSERVATION_CORE_WITH_OPEN_OFFHUB_REPAIR','source_sha256':PIN,'public':1880,'owned_fields':51,'initial':w['initial']+[w['initial'][i] for i in M],'difference_role_map':{str(i):v for i,v in qm.items()},'selected_source_event':loan,'selected_donor':77,'selected_receiver':189,'program':ops,'raw_reservations':reservations,'marks':marks,'final_recoupling_included':False},qm
def execute(w,meta,ops,state=None):
 pub=meta['public'];C=list(map(span,w['frames']));rows={i:{i:F(1)} for i in range(pub)} if state is None else {i:r.copy() for i,r in state[0].items()};chart=dict(enumerate(meta['initial'])) if state is None else state[1].copy();bill=collections.Counter();life=peak=0
 for e in ops:
  op,r=e[:2];need(0<=r<pub+meta['owned_fields'],'declared role');bill[op]+=1
  if op=='INIT':need(r>=pub and r not in chart,'owned INIT');chart[r]=e[2];rows[r]={};life+=1
  elif op=='CLEAR':need(r>=pub and chart.get(r)==e[2],'owned CLEAR');chart.pop(r);rows.pop(r)
  elif op=='MOVE':
   a,b,own=e[2:];need(chart.get(r)==a and type(own)is bool and own==(r>=pub),'typed MOVE');need(C[a]<C[b] or own and C[b]<C[a],'proper nested route');chart[r]=b
  elif op=='SCALE':need(chart.get(r)==e[3],'SCALE chart');rows[r]={i:F(e[2])*v for i,v in rows[r].items()}
  elif op in ('ADD','COPY'):
   s,c,f=e[2:];need(r!=s and chart.get(r)==chart.get(s)==f,'actual cochart arithmetic')
   if op=='COPY':need(not rows[r],'physical COPY destination zero')
   rows[r]=add(rows[r],rows[s],F(c))
  else:raise ValueError('unknown instruction')
  peak=max(peak,len(chart)-pub)
 return rows,chart,{'instructions':len(ops),'counts':dict(sorted(bill.items())),'owned_lifetimes':life,'peak_owned':peak,'final_live_owned':len(chart)-pub}
def run(source,packet,write):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));certificate=json.loads((packet/'OBSERVATIONS.json').read_text());items=certificate['observations'];need(certificate['source_sha256']==PIN,'observation source pin');W,Z,summaries,reads=source_check(w,items);pick=next(i for i,x in enumerate(items) if x['event']==29098 and x['donor']==77);sel=items[pick];need(sel['gain']=='1' and len(sel['historical_decoder'])==5,'selected five-term module');meta,qm=build(w,sel);path=packet/'OBSERVATION-WORD.json.gz';word=json.dumps(meta,sort_keys=True,separators=(',',':')).encode()
 if write:path.write_bytes(gzip.compress(word,compresslevel=9,mtime=0))
 else:need(gzip.decompress(path.read_bytes())==word,'entire literal word reconstructed')
 out,chart,bill=execute(w,meta,meta['program']);delta={qm[77]:F(1),77:F(-2)};z=Z[pick]
 for i in range(1480):need(out[i]==add(W[i],delta,z.get(i,F(0))) and chart[i]==w['final'][i],'full common source response')
 for i,r in qm.items():
  expected=delta if i==77 else {r:F(1),i:F(-1)}
  if i==189:expected=add(expected,{qm[77]:F(1),77:F(-1)},F(1))
  need(out[r]==expected and chart[r]==w['final'][i],'all400 actual raw endpoints')
 need(bill['instructions']==73378 and bill['counts']['ADD']==61587 and bill['counts']['MOVE']==8020 and bill['owned_lifetimes']==54 and bill['peak_owned']==43 and bill['final_live_owned']==0,'core full cost/storage')
 need(W[77]=={77:F(1)} and len(z)==431,'selected hub recovery/response');corr=[['ADD',i,qm[77],str(-v),127] for i,v in sorted(z.items()) if w['final'][i]==127];corr.append(['ADD',qm[77],77,'1',127]);normal,nchart,nbill=execute(w,meta,corr,(out,chart));off={i:v for i,v in z.items() if w['final'][i]!=127}
 need(len(corr)==372 and len(off)==60,'selected precise remaining repair')
 for i in range(1480):need(normal[i]==add(W[i],delta,off.get(i,F(0))),'hub normal form')
 need(normal[qm[77]]=={qm[77]:F(1),77:F(-1)},'donor restored');need(any(normal[i]!=W[i] for i in off),'not a complete common restoration')
 payload={'source_sha256':PIN,'program':corr,'remaining_offhub_response':ser(off),'remaining_error_field':'delta=q77-u77=v77-2u77','complete_common_restoration':False};cpath=packet/'HUB-CORRECTIONS.json';ctext=json.dumps(payload,indent=2,sort_keys=True)+'\n'
 if write:cpath.write_text(ctext)
 else:need(cpath.read_text()==ctext,'hub corrections reconstructed')
 negatives=[]
 wrong=add({int(k):F(v) for k,v in sel['hrow'].items()},reads[-1,953],F(8));need(wrong!={77:F(1)},'omitted initial helper-history term rejected');negatives.append('omitting initial -8u953 changes full source decoder by8u953')
 need(F(2)*F(sel['decoder_sensitivity'])!=1,'wrong gain rejected');negatives.append('doubling injection gain breaks normalized q observation')
 need(len(off)>0,'incomplete common restoration rejected');negatives.append('claiming full common restoration ignores60 nonzero offhub rows')
 bad=meta['raw_reservations']+[meta['raw_reservations'][0]];need(len(bad)!=len({r['source_event'] for r in bad}),'duplicate reservation rejected');negatives.append('duplicating a funded raw reservation is rejected')
 try:execute(w,meta,[['MOVE',qm[77],71,312,True]])
 except ValueError:negatives.append('false owned flag on public donor MOVE rejected')
 else:raise ValueError('accepted false ownership')
 return {'status':'PASS_31_SOURCE_OBSERVATIONS_AND_ACTUAL_1880_INPUT_CORE','source_sha256':PIN,'observation_certificate_sha256':hashlib.sha256((packet/'OBSERVATIONS.json').read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'distinct_individual_modules':31,'direct_chronological_modules':sum(x['direct_accumulation_ordered'] for x in summaries),'modules_with_stationary_lowering':31,'gain_histogram':dict(collections.Counter(x['gain'] for x in summaries)),'selected_donor':77,'selected_receiver':189,'selected_loan_event':29098,'physical_input_directions':1880,'core_bill':bill,'all_raw_reservations_used_once':1710,'source_public_response_support':431,'local_hub_corrections':len(corr),'remaining_offhub_response_fields':60,'core_includes_final_recoupling':False,'module_summaries':summaries,'negative_controls':negatives,'scope':'31 separate observation modules; one full1880-input observation core. Common endpoint repair is explicitly incomplete. No joint composition, compatible supplier, complete multiplication bound or new kappa.','new_complete_kappa':None}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--write-word',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.packet,a.write_word);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k!='module_summaries'},indent=2))
