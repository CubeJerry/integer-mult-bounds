import argparse,gzip,hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT='7b915321a6e9afc2a83fd79f95e0c9605d28dc578d69d4b0700ee6fd37f739b9'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
PREPAID='6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51'
def need(b,s):
 if not b:raise ValueError(s)
def read(p,pin):
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'dependency pin '+p.name);return b
def span(f):
 s={0}
 for q in f:s|={x^q for x in s}
 return s
def replay(w,ops,M,capture=None,dirty=None):
 p=w['public'];n=p+w['owned_fields'];x=[{i:F(1)} if i in M or i==dirty else {} for i in range(n)];loc=w['initial'][:]+[None]*(n-p);live=set(range(p));frames=list(map(span,w['frames']));counts=Counter();moves=Counter();peak=life=0;out={}
 for i,e in enumerate(ops):
  if capture and i in capture:out[i]=x[capture[i]].copy()
  op,r=e[:2];need(0<=r<n,'field bound');counts[op]+=1
  if op=='INIT':need(r>=p and r not in live,'INIT owned fresh');live.add(r);loc[r]=e[2];x[r]={};life+=1
  elif op=='CLEAR':need(r>=p and r in live and loc[r]==e[2],'CLEAR owned chart');live.remove(r);loc[r]=None;x[r]={}
  elif op=='MOVE':
   need(r in live and loc[r]==e[2] and type(e[4]) is bool and e[4]==(r>=p),'MOVE actual ownership/chart');a,b=frames[e[2]],frames[e[3]];need(a<b or r>=p and b<a,'MOVE strict legal nesting');loc[r]=e[3];moves[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
  elif op=='SCALE':need(r in live and loc[r]==e[3] and F(e[2])!=0,'SCALE');x[r]={j:v*F(e[2]) for j,v in x[r].items()}
  elif op in ('ADD','COPY'):
   q=e[2];need(0<=q<n and r!=q and r in live and q in live and loc[r]==loc[q]==e[4],'actual live cochart operands');c=F(e[3]);need(c!=0,'nonzero coefficient')
   if op=='COPY':need(not x[r],'zero COPY')
   for j,v in x[q].items():
    x[r][j]=x[r].get(j,F(0))+c*v
    if not x[r][j]:del x[r][j]
  else:raise ValueError(op)
  peak=max(peak,len(live)-p)
 need(live==set(range(p)) and loc[:p]==w['final'],'final chart cleanup');return x,{'counts':dict(counts),'MOVE_histogram':{str(r):c for r,c in sorted(moves.items())},'owned_lifetimes':life,'peak_live_owned':peak,'final_live_owned':0,'declared_owned_labels':w['owned_fields']},out
def power(r):
 D=2**88;N=r**199*D**200
 with localcontext() as c:c.prec=100;a=int(Decimal(r)**(Decimal(199)/200)*D)
 while a**200>N:a-=1
 while(a+1)**200<=N:a+=1
 need(a**200<=N<(a+1)**200,'exact power enclosure');return F(a,D),F(a if a**200==N else a+1,D)
def expanded_records(w,W,selected,preload):
 out=[];newroles={};nextrole=w['public']+w['owned_fields'];cuts={}
 def emit(t,kind,op):out.append({'source_event':t,'kind':kind,'instruction':op})
 if preload:
  for t in (33272,33281):
   a=W[t];h=nextrole;nextrole+=1;newroles[t]=h;emit(-1,'preload_init',['INIT',h,3])
   for q,c in a['target_row']:
    need(w['initial'][q]==3,'initial cochart preload');emit(-1,'preload_input',['ADD',h,q,c,3])
   emit(-1,'preload_move',['MOVE',h,3,a['move'][3],True])
 for t,e in enumerate(w['program']):
  if t not in selected:emit(t,'source',e[:]);continue
  need(e==W[t]['move'],'selected occurrence pin');r,a,b=e[1:4];emit(t,'macro_clear',['CLEAR',r,a]);emit(t,'macro_init',['INIT',r,b])
  if t in newroles:
   h=newroles[t];emit(t,'preload_observation',['ADD',r,h,'1',b]);cuts[len(out)]=(t,r);emit(t,'preload_clear',['CLEAR',h,b])
  else:
   for h,c in W[t]['witness']:emit(t,'external_observation',['ADD',r,h,c,b])
   cuts[len(out)]=(t,r)
 ww=dict(w);ww['owned_fields']=nextrole-w['public'];return out,ww,cuts,newroles

def dependency_graph(records,public):
 live={};nodes={};owner_of={};edges={};roots=set()
 for k,z in enumerate(records):
  e=z['instruction'];op,r=e[:2]
  if op=='INIT':
   need(r>=public and r not in live,'graph INIT fresh');live[r]=k;nodes[k]={'owner':r,'birth':k,'death':None,'writes':[],'reads':[]};edges[k]=set()
  if r>=public:
   need(r in live,'graph owned target live');a=live[r];nodes[a]['writes'].append(k);owner_of[k]=a
  if op in ('ADD','COPY') and e[2]>=public:
   need(e[2] in live and e[2]!=r,'graph source live/nonalias');a=live[e[2]];nodes[a]['reads'].append(k)
   if r<public:roots.add(a)
   else:edges[a].add(live[r])
  if op=='CLEAR':a=live.pop(r);nodes[a]['death']=k
 need(not live,'graph all lifetimes closed');return nodes,edges,roots,owner_of

def independent_delete(records,public):
 nodes,edges,roots,owner=dependency_graph(records,public);dead=set();waves=[]
 while True:
  layer={a for a in nodes if a not in dead and a not in roots and edges[a]<=dead}
  if not layer:break
  waves.append(sorted(layer,key=lambda a:nodes[a]['death']));dead|=layer
 # A second algorithm checks the full backward dependency closure; it can detect
 # a mutually reading dead SCC which zero-outdegree elimination would miss.
 needed=set(roots)
 while True:
  bigger=needed|{a for a,bs in edges.items() if bs&needed}
  if bigger==needed:break
  needed=bigger
 need(dead==set(nodes)-needed,'no inaccessible owned SCC after sink peeling')
 kept=[z for k,z in enumerate(records) if owner.get(k) not in dead]
 evidence=[]
 for layer in waves:
  evidence.append([{'owner':nodes[a]['owner'],'birth':records[nodes[a]['birth']],'death':records[nodes[a]['death']], 'external_read_count':0,'deleted_operations':[records[k] for k in nodes[a]['writes']]} for a in layer])
 return kept,evidence,{'lifetimes':len(nodes),'public_rooted_lifetimes':len(needed),'deleted_lifetimes':len(dead),'round_sizes':list(map(len,waves))}

def rational_moment(coeffs,powers):
 lo=hi=F(0)
 for r,c in coeffs.items():
  u,v=powers[r];lo+=c*(u if c>=0 else v);hi+=c*(v if c>=0 else u)
 return lo,hi

def run(source,cert,invoice,packet):
 w=json.loads(gzip.decompress(read(source,NATIVE)));W={x['before_event']:x for x in json.loads(read(cert,CERT))['witnesses']};iv=json.loads(read(invoice,INVOICE));author=json.loads((packet/'RESULT.json').read_text());cr=(packet/'CERTIFICATE.json').read_bytes();need(hashlib.sha256(cr).hexdigest()==author['certificate_sha256'],'author certificate hash');certificate=json.loads(cr)
 M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(len(M)==400,'400 independent q');x,basebill,snap=replay(w,w['program'],M,{t:W[t]['move'][1] for t in W});need(basebill==author['baseline_reference'],'baseline exact bill')
 for t,a in W.items():need(snap[t]=={q:F(c) for q,c in a['target_row']},'source target identity '+str(t))
 base_records=[{'source_event':t,'kind':'source','instruction':e} for t,e in enumerate(w['program'])];basekeep,basewaves,basegraph=independent_delete(base_records,w['public']);need(basewaves==certificate['baseline_unread_lifetimes'],'baseline wave certificate');need(not any(z['instruction'][0]=='MOVE' for layer in basewaves for life in layer for z in life['deleted_operations']),'baseline saves no route')
 T=Counter({int(k):v for k,v in iv['T4'].items()});P4=Counter({int(k):v for k,v in iv['P4'].items()});original_owned={t:e for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]>=w['public']};configs={'seven':(set(W)-{33272,33281,37606},False),'eight':(set(W)-{33272,33281},False),'ten':(set(W),False),'ten_preloaded':(set(W),True)};result={};prices={}
 dirtybase,_,_=replay(w,w['program'],M,dirty=400)
 for name,(selected,preload) in configs.items():
  a=author['variants'][name];records,ww,cuts,preloads=expanded_records(w,W,selected,preload);expanded,_,checked=replay(ww,[z['instruction'] for z in records],M,{k:r for k,(t,r) in cuts.items()});need(expanded[:w['public']]==x[:w['public']] and all(checked[k]==snap[t] for k,(t,r) in cuts.items()),'expanded full reference and each local row')
  kept,waves,graph=independent_delete(records,w['public']);need(waves==certificate['variants'][name]['deletion_rounds'],'all exact wave operations '+name);need(graph['round_sizes']==a['deletion_round_lifetimes'],'wave sizes')
  payload=gzip.decompress((packet/(name+'.json.gz')).read_bytes());word=json.loads(payload);program=[z['instruction'] for z in kept];need(word['program']==program and word['source_map']==[[z['source_event'],z['kind']] for z in kept],'complete instruction/lineage equality');need(word['owned_fields']==ww['owned_fields'] and word['frames']==w['frames'] and word['initial']==w['initial'] and word['final']==w['final'] and word['main_roles']==sorted(M),'transcript metadata');need(hashlib.sha256(payload).hexdigest()==a['transcript_payload_sha256'],'transcript payload pin')
  y,bill,_=replay(ww,program,M);need(y[:w['public']]==x[:w['public']],'1480 endpoint rows');need(bill==a['actual_reference'],'exact primitive and lifecycle bill');need([e for e in program if e[0]=='MOVE' and e[1]<w['public']]==[e for e in w['program'] if e[0]=='MOVE' and e[1]<w['public']],'all public routes retained in order')
  alive={z['source_event'] for z in kept if z['kind']=='source'};removed=sorted(set(original_owned)-alive);owned=Counter(abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])) for e in program if e[0]=='MOVE' and e[1]>=w['public']);saved=Counter(abs(len(w['frames'][original_owned[t][2]])-len(w['frames'][original_owned[t][3]])) for t in removed);need(removed==a['removed_original_owned_moves'] and {str(k):v for k,v in sorted(saved.items())}==a['saved_owned_histogram'],'actual source MOVE savings');need({str(k):v for k,v in sorted(owned.items())}==a['retained_and_added_owned_histogram'],'actual remaining/preloaded MOVE histogram')
  ext=[z for z in kept if z['kind']=='external_observation'];kind=Counter(W[z['source_event']]['observer_kinds'][str(z['instruction'][2])] for z in ext);need(len(ext)==a['external_observer_terms'] and dict(kind)==a['external_observer_kinds'],'surviving observer terms');P=Counter(P4)
  for r,c in owned.items():P[r]+=18*c
  need(P==Counter({int(k):v for k,v in a['new_P'].items()}) and T==Counter({int(k):v for k,v in a['new_T'].items()}),'complete paid and target profiles');powers={r:power(r) for r in set(T)|set(P)};margin=rational_moment({r:T[r]-P[r] for r in set(T)|set(P)},powers);need(0<F(a['raw_margin_numerator_bounds'][0],) / 10**15<=margin[0]<=margin[1]<=F(a['raw_margin_numerator_bounds'][1])/10**15,'independent dyadic directed margin');ceiling=margin[1]//18;need(ceiling==a['additional_per_native_headroom']['positive_rank_arrival_ceiling'],'arrival ceiling');need(sum(P.values())==a['paid_count'] and sum(T.values())==a['target_count'] and sum(r*(T[r]-P[r]) for r in set(T)|set(P))==a['rank_surplus'],'whole profile census');prices[name]=P
  controls=[];bad=[e[:] for e in program];j=next(k for k,z in enumerate(kept) if z['kind']=='external_observation');bad[j][3]=str(F(bad[j][3])+1);z,_,_=replay(ww,bad,M);need(z[:w['public']]!=x[:w['public']],'changed live observer must fail endpoint');controls.append('changed surviving observer coefficient changes endpoint')
  nodes,edges,roots,owner=dependency_graph(kept,w['public']);life=next(iter(roots));bad=[z['instruction'] for k,z in enumerate(kept) if owner.get(k)!=life]
  try:replay(ww,bad,M)
  except (ValueError,TypeError):controls.append('deleting publicly read owned lifetime rejected')
  else:raise ValueError('illegal owned deletion accepted')
  dirty,_,_=replay(ww,program,M,dirty=400);mismatch=sum(a!=b for a,b in zip(dirty[:w['public']],dirtybase[:w['public']]));need(mismatch>0,'independent helper400 final-output counterexample');controls.append({'independent_helper400_changed_public_outputs':mismatch})
  if preload:
   j=next(k for k,z in enumerate(kept) if z['kind']=='preload_input');bad=[e[:] for e in program];bad[j][2]=0
   try:replay(ww,bad,M)
   except ValueError:controls.append('noncochart preload input rejected')
   else:raise ValueError('illegal preload accepted')
   need(sum(z['kind']=='preload_input' for z in kept)==96 and sum(z['kind']=='preload_observation' for z in kept)==2,'full preload tariff')
  result[name]={'instructions':len(program),'exact_reference_bill':bill,'source_owned_moves_removed':removed,'surviving_external_observer_terms':len(ext),'observer_kinds':dict(kind),'independent_graph':graph,'paid_positions':sum(P.values()),'targets':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in set(T)|set(P)),'independent_raw_margin_bounds':[str(z) for z in margin],'additional_per_native_headroom_bounds':[str(z/18) for z in margin],'positive_rank_arrival_ceiling':ceiling,'negative_controls':controls,'transcript_payload_sha256':hashlib.sha256(payload).hexdigest()}
  print('independently checked '+name,flush=True)
 diff={r:prices['ten_preloaded'][r]-prices['eight'][r] for r in set(prices['ten_preloaded'])|set(prices['eight'])};premium=rational_moment(diff,{r:power(r) for r in diff});need(premium[0]>0,'preloaded ten costs more than eight');return {'status':'PASS_INDEPENDENT_OWNED_DEPENDENCY_CLOSURE_AND_PRICES','source_sha256':NATIVE,'author_result_sha256':hashlib.sha256((packet/'RESULT.json').read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(cr).hexdigest(),'reference_domain':'400 independent q inputs; helper differences zero; all 1480 public endpoints checked','baseline_graph':basegraph,'variants':result,'preloaded_ten_premium_over_eight_per_native_bounds':[str(z/18) for z in premium],'scope':'Whole-owned-lifetime deletion is universal noninterference; inserted current observations remain conditional. No source oracle, 1880-input shared native, supplier, foundational closure or new kappa is claimed.'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for s in ('source','cert','invoice','packet'):p.add_argument('--'+s,type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=run(a.source,a.cert,a.invoice,a.packet);a.output.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');print(d['status'])
