#!/usr/bin/env python3
"""Eliminate unread owned lifetimes after exact current reconstructions."""
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
   need(r!=e[2] and cur[r] is not None and cur[e[2]] is not None and frames[cur[r]]==frames[cur[e[2]]]==frames[e[4]],'live cochart scalar')
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

CURRENT='7b915321a6e9afc2a83fd79f95e0c9605d28dc578d69d4b0700ee6fd37f739b9'

def owned_lifetimes(records, public):
 live={};finished=[]
 for i,z in enumerate(records):
  e=z['instruction'];op,r=e[:2]
  if op=='INIT':
   need(r>=public and r not in live,'fresh lifetime')
   live[r]={'owner':r,'birth':i,'writes':[],'external_reads':[]}
  if r>=public:
   need(r in live,'owned write inside lifetime');live[r]['writes'].append(i)
  if op in ('ADD','COPY') and e[2]>=public:
   need(e[2] in live and e[2]!=r,'live distinct external owned read')
   live[e[2]]['external_reads'].append(i)
  if op=='CLEAR':
   life=live.pop(r);life['death']=i;finished.append(life)
 need(not live,'all lifetimes close')
 return finished

def eliminate(records, public):
 rounds=[]
 while True:
  dead=[x for x in owned_lifetimes(records,public) if not x['external_reads']]
  if not dead:break
  deletion={i for life in dead for i in life['writes']}
  rounds.append([{'owner':x['owner'],'birth':records[x['birth']],
                  'death':records[x['death']],'external_read_count':0,
                  'deleted_operations':[records[i] for i in x['writes']]} for x in dead])
  records=[z for i,z in enumerate(records) if i not in deletion]
 return records,rounds

def publicly_live_lifetimes(records, public):
 # Mark backwards from every public use, including whole owned-only SCCs.
 live={};dependencies={};roots=set()
 for i,z in enumerate(records):
  e=z['instruction'];op,r=e[:2]
  if op=='INIT':live[r]=i;dependencies[i]=set()
  if op in ('ADD','COPY') and e[2]>=public:
   source=live[e[2]]
   if r<public:roots.add(source)
   else:dependencies[live[r]].add(source)
  if op=='CLEAR':live.pop(r)
 marked=set(roots);pending=list(roots)
 while pending:
  for source in dependencies[pending.pop()]:
   if source not in marked:marked.add(source);pending.append(source)
 return set(dependencies),marked

def make_records(w, witnesses, selected, preload):
 records=[];preloads={};public=w['public'];next_role=public+w['owned_fields']
 def emit(source,kind,e):records.append({'source_event':source,'kind':kind,'instruction':e})
 if preload:
  for t in (33272,33281):
   a=witnesses[t];h=next_role;next_role+=1;preloads[t]=h
   emit(-1,'preload_init',['INIT',h,3])
   for q,c in a['target_row']:
    need(w['initial'][q]==3,'preload raw q starts at chart3')
    emit(-1,'preload_input',['ADD',h,q,c,3])
   emit(-1,'preload_move',['MOVE',h,3,a['move'][3],True])
 for t,e in enumerate(w['program']):
  if t not in selected:emit(t,'source',e);continue
  a=witnesses[t];need(e==a['move'],'source occurrence match');r,old,dest=e[1:4]
  emit(t,'macro_clear',['CLEAR',r,old]);emit(t,'macro_init',['INIT',r,dest])
  if t in preloads:
   h=preloads[t];emit(t,'preload_observation',['ADD',r,h,'1',dest])
   emit(t,'preload_clear',['CLEAR',h,dest])
  else:
   for h,c in a['witness']:emit(t,'external_observation',['ADD',r,h,c,dest])
 newword=dict(w);newword['owned_fields']=next_role-public
 return records,newword,preloads

def bill(T,P4,owned):
 P=Counter(P4)
 for r,c in owned.items():P[r]+=18*c
 D=10**15;lower=upper=0
 for r in set(T)|set(P):
  c=T[r]-P[r];lo,hi=enclose(r,D);lower+=c*(lo if c>=0 else hi);upper+=c*(hi if c>=0 else lo)
 need(lower>0,'strict positive full paid margin')
 return {'new_T':dict(sorted(T.items())),'new_P':dict(sorted(P.items())),
         'target_count':sum(T.values()),'paid_count':sum(P.values()),
         'rank_surplus':sum(r*(T[r]-P[r]) for r in set(T)|set(P)),
         'denominator':str(D),'raw_margin_numerator_bounds':[str(lower),str(upper)],
         'additional_per_native_headroom':{'numerator_bounds':[str(lower),str(upper)],
           'denominator':str(18*D),'positive_rank_arrival_ceiling':upper//(18*D)}}

def run(source, invoice, certificate, outdir):
 raw=source.read_bytes();need(hashbytes(raw)==PIN,'source pin');ir=invoice.read_bytes();need(hashbytes(ir)==INVOICE,'invoice pin')
 cr=certificate.read_bytes();need(hashbytes(cr)==CURRENT,'current certificate pin')
 w=json.loads(gzip.decompress(raw));C=json.loads(cr);W={a['before_event']:a for a in C['witnesses']}
 M=set(w['live'])|{q+112 for q in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 need(len(M)==400 and len(W)==10,'input and current identity census')
 baseline,basecur,basebill,targets=replay(w,w['program'],M,capture=W)
 for t,a in W.items():need(targets[t]=={int(q):F(v) for q,v in a['target_row']},'all ten targets freshly replayed')
 original_owned=Counter();source_owned_events=[]
 for t,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1]>=w['public']:
   source_owned_events.append(t);original_owned[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
 need(original_owned==Counter({1:20,2:9,3:2,4:13,5:2,6:1}),'47 original owned routes')
 z=json.loads(ir);T=Counter({int(k):v for k,v in z['T4'].items()});P4=Counter({int(k):v for k,v in z['P4'].items()})
 base_records=[{'source_event':t,'kind':'source','instruction':e} for t,e in enumerate(w['program'])]
 base_pruned,base_rounds=eliminate(base_records,w['public'])
 need(len(base_rounds)==1 and len(base_rounds[0])==1,'one already unread original lifetime')
 need(not any(z['instruction'][0]=='MOVE' for x in base_rounds[0] for z in x['deleted_operations']),'baseline deletion saves no route')
 configurations=[('seven',set(W)-{33272,33281,37606},False),
                 ('eight',set(W)-{33272,33281},False),('ten',set(W),False),('ten_preloaded',set(W),True)]
 expected={'seven':(71208,22,12,[8,3,3]),'eight':(71201,26,14,[9,3,3]),
           'ten':(71194,28,16,[11,3,3]),'ten_preloaded':(71296,26,16,[11,3,3])}
 results={};evidence={};cached={}
 dirty_baseline,_,_,_=replay(w,w['program'],M,extra_helper=400)
 for name,selected,preload in configurations:
  records,ww,preloads=make_records(w,W,selected,preload)
  # Before deleting anything, certify every replacement at its exact local cut.
  full_checks={};last={}
  for k,z in enumerate(records):
   if z['kind'] in ('external_observation','preload_observation'):last[z['source_event']]=k+1
  for t,cut in last.items():full_checks[cut]={'owner':W[t]['move'][1],'target':targets[t]}
  expanded,expandedcur,_,_=replay(ww,[z['instruction'] for z in records],M,checks=full_checks)
  need(expanded[:w['public']]==baseline[:w['public']],'expanded macros preserve all endpoints')
  kept,rounds=eliminate(records,w['public']);program=[z['instruction'] for z in kept]
  output,outcur,counts,_=replay(ww,program,M)
  need(output[:w['public']]==baseline[:w['public']] and outcur[:w['public']]==basecur[:w['public']],
       'pruned word preserves all1480 public rows and charts')
  need(all(x['external_reads'] for x in owned_lifetimes(kept,w['public'])),'maximal unread-lifetime fixed point')
  all_lives,publicly_live=publicly_live_lifetimes(kept,w['public'])
  need(all_lives==publicly_live,'no unobserved owned-only SCC survives')
  original_lives,originally_live=publicly_live_lifetimes(records,w['public'])
  need(len(original_lives)-len(originally_live)==sum(len(a) for a in rounds),
       'zero-read waves equal full backward owned-lifetime closure')
  kept_source={z['source_event'] for z in kept if z['kind']=='source'}
  removed=[t for t in source_owned_events if t not in kept_source]
  saved=Counter(abs(len(w['frames'][w['program'][t][2]])-len(w['frames'][w['program'][t][3]])) for t in removed)
  owned=Counter(abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])) for e in program if e[0]=='MOVE' and e[1]>=w['public'])
  external=[z for z in kept if z['kind']=='external_observation']
  kind_counts=Counter(W[z['source_event']]['observer_kinds'][str(z['instruction'][2])] for z in external)
  paid=bill(T,P4,owned)
  public_moves_before=[e for e in w['program'] if e[0]=='MOVE' and e[1]<w['public']]
  public_moves_after=[e for e in program if e[0]=='MOVE' and e[1]<w['public']]
  need(public_moves_before==public_moves_after,'all public moves retained in order')
  ex=expected[name];need((len(program),len(external),len(removed),[len(a) for a in rounds])==ex,'variant source census')
  controls=[]
  bad=[e[:] for e in program];index=next(i for i,z in enumerate(kept) if z['kind']=='external_observation')
  bad[index][3]=str(F(bad[index][3])+1)
  altered,_,_,_=replay(ww,bad,M)
  need(altered[:w['public']]!=baseline[:w['public']],'wrong live observation must change endpoints')
  controls.append('changed surviving observation coefficient changes public endpoint')
  dirty,_,_,_=replay(ww,program,M,extra_helper=400)
  mismatch=sum(a!=b for a,b in zip(dirty[:w['public']],dirty_baseline[:w['public']]))
  need(mismatch>0,'independent helper400 outside admitted domain')
  controls.append({'independent_helper400_endpoint_mismatches':mismatch})
  live=next(life for life in owned_lifetimes(kept,w['public']) if life['external_reads'])
  bad=[z['instruction'] for i,z in enumerate(kept) if i not in set(live['writes'])]
  rejected=False
  try:replay(ww,bad,M)
  except (ValueError,TypeError):rejected=True
  need(rejected,'removing an externally read lifetime must fail')
  controls.append('removing an externally read lifetime rejected')
  if preload:
   need(Counter({3:1,4:1})==Counter(abs(len(w['frames'][z['instruction'][2]])-len(w['frames'][z['instruction'][3]]))
         for z in kept if z['kind']=='preload_move'),'actual rank3/rank4 entry moves')
   need(sum(z['kind']=='preload_input' for z in kept)==96,'96 raw entry summands')
   bad=[e[:] for e in program];j=next(i for i,z in enumerate(kept) if z['kind']=='preload_input');bad[j][2]=0
   rejected=False
   try:replay(ww,bad,M)
   except ValueError:rejected=True
   need(rejected,'noncochart raw preload input rejected');controls.append('raw q0 preload violates chart3 input contract')
  payload={'schema':'moonshot-owned-lifetime-elimination-v1','variant':name,'source_sha256':PIN,
           'public':w['public'],'owned_fields':ww['owned_fields'],'initial':w['initial'],'final':w['final'],
           'frames':w['frames'],'main_roles':sorted(M),'program':program,
           'source_map':[[z['source_event'],z['kind']] for z in kept],
           'scope':'Exact400-input homogeneous difference reference, not1880-input shared native.'}
  encoded=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode()
  outdir.mkdir(parents=True,exist_ok=True);(outdir/(name+'.json.gz')).write_bytes(gzip.compress(encoded,mtime=0))
  changes={k:counts['counts'].get(k,0)-basebill['counts'].get(k,0) for k in set(counts['counts'])|set(basebill['counts'])}
  results[name]={'selected_current_events':sorted(selected),'reference_instructions':len(program),
    'removed_original_owned_moves':removed,'saved_owned_histogram':dict(sorted(saved.items())),
    'retained_and_added_owned_histogram':dict(sorted(owned.items())),
    'deletion_round_lifetimes':[len(a) for a in rounds],'external_observer_terms':len(external),
    'retained_lifetimes_reaching_public_uses':len(publicly_live),'dead_owned_SCCs_remaining':0,
    'external_observer_kinds':dict(kind_counts),'external_observer_versions':[
      {'event':z['source_event'],'observer':z['instruction'][2],
       'last_value_event':W[z['source_event']]['observer_last_value_events'][str(z['instruction'][2])],
       'chart':z['instruction'][4]} for z in external],
    'internal_preload_observations':sum(z['kind']=='preload_observation' for z in kept),
    'preload_input_ADDs':sum(z['kind']=='preload_input' for z in kept),
    'actual_reference':counts,'operation_changes':changes,'transcript_payload_sha256':hashbytes(encoded),
    'negative_controls':controls,**paid}
  evidence[name]={'selected_current_events':sorted(selected),'preload_roles':preloads,
                 'deletion_rounds':rounds,'surviving_lifetimes':[
      {'owner':life['owner'],'birth':kept[life['birth']], 'death':kept[life['death']],
       'external_read_sites':[kept[i] for i in life['external_reads']]} for life in owned_lifetimes(kept,w['public'])]}
  cached[name]=owned
  print(json.dumps({'variant':name,'instructions':len(program),'removed_owned_moves':len(removed),
                    'external_observers':len(external),'headroom':paid['additional_per_native_headroom'],
                    'peak_owned':counts['peak_live_owned']},sort_keys=True),flush=True)
 # At equal26 external observation terms, eight has a better paid moment than optional preloaded ten.
 diff=Counter(cached['ten_preloaded']);diff.subtract(cached['eight']);lo=hi=0
 for r,c in diff.items():
  a,b=enclose(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 need(lo>0,'optional preloaded ten costs more than eight')
 cert={'schema':'owned-lifetime-elimination-certificate-v1','source_sha256':PIN,
       'current_certificate_sha256':CURRENT,'baseline_unread_lifetimes':base_rounds,'variants':evidence}
 cb=(json.dumps(cert,sort_keys=True,indent=2)+'\n').encode();(outdir/'CERTIFICATE.json').write_bytes(cb)
 result={'status':'PASS_OWNED_LIFETIME_ELIMINATION_AND_COMPLETE_CONDITIONAL_PROFILES',
         'source_sha256':PIN,'invoice_sha256':INVOICE,'current_certificate_sha256':CURRENT,
         'certificate_sha256':hashbytes(cb),'input_domain':'400independent main differences; common entering helpers arbitrary and equal',
         'public_endpoint_rows_checked_per_variant':1480,'source_owned_moves':47,'source_owned_lifetimes':54,
         'baseline_unread_lifetimes':1,'baseline_unread_route_saving':0,'baseline_reference':basebill,
         'variants':results,'optional_preloaded_ten_paid_premium_over_eight_per_native':{
          'numerator_bounds':[str(lo),str(hi)],'denominator':str(10**15)},
         'scope':'Unread lifetime elimination is a universal typed-word equivalence. The current reconstructions '
                 'are conditional on actual observers and the400-input equal-helper domain. Profile feasibility '
                 'is not supplier admission. Changed intermediate-return obligations are intentionally removed; '
                 'all shared-native, ordinary/precision/compiler, BIT and foundational obligations remain. No new kappa.'}
 (outdir/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['source','invoice','certificate','outdir']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args();r=run(a.source,a.invoice,a.certificate,a.outdir)
 print(r['status'])

