import argparse,gzip,hashlib,json
from bisect import bisect_right
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT='d46db515a5fead49b752b8d798472c883aff7698d7e5e948f0d4e336ec99054b'
BUDGET='6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51'
def need(b,s):
 if not b:raise ValueError(s)
def rank(rows):
 B={}
 for a0 in rows:
  a=dict(a0)
  while a:
   k=min(a)
   if k not in B:
    c=a[k];B[k]={j:v/c for j,v in a.items()};break
   c=a[k]
   for j,v in B[k].items():
    a[j]=a.get(j,Q(0))-c*v
    if not a[j]:del a[j]
 return len(B)
def span(f):
 s={0}
 for v in f:s|={x^v for x in s}
 return tuple(sorted(s))
def quiet(w,M):
 uses=defaultdict(list);visits=defaultdict(list);cohort=defaultdict(set)
 for q in M:visits[q,w['initial'][q]].append(-1);cohort[w['initial'][q]].add(q)
 for i,e in enumerate(w['program']):
  uses[e[1]].append(i)
  if e[0] in ('ADD','COPY'):uses[e[2]].append(i)
  if e[0]=='MOVE' and e[1] in M:visits[e[1],e[3]].append(i)
 loans=[]
 for i,e in enumerate(w['program']):
  if e[0]!='MOVE':continue
  _,h,a,b,_=e
  if h not in M:
   j=bisect_right(uses[h],i);end=uses[h][j] if j<len(uses[h]) else len(w['program'])
   for q in sorted(cohort[a]):
    ts=visits[q,b];j=bisect_right(ts,i)
    if j<len(ts) and ts[j]<end:loans.append({'start':i,'close':ts[j],'next_use':end,'donor':q,'helper':h,'from':a,'to':b})
  else:cohort[a].remove(h);cohort[b].add(h)
 need(len(loans)==354 and len({x['start'] for x in loans})==141,'quiet census');return loans
def propagate(w,M,canon,want,extra):
 K=[0]*(max(canon.values())+1)
 for q in M:K[canon[w['initial'][q]]]|=1<<q
 demand={};sources=[]
 for t,e in enumerate(w['program']):
  if t in want:demand[t]=K[canon[want[t]['to']]]
  if e[0]!='MOVE':continue
  if e[1] not in M and e[1]<w['public'] and t<max(want) and t not in extra:sources.append((t,e[1],e[2],e[3],K[canon[e[2]]]))
  if e[1] in M or e[1]>=w['public'] or t in extra:K[canon[e[3]]]|=K[canon[e[2]]]
 return demand,sources
def run(source,certificate,budget):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');cr=certificate.read_bytes();need(hashlib.sha256(cr).hexdigest()==CERT,'historical pin');br=budget.read_bytes();need(hashlib.sha256(br).hexdigest()==BUDGET,'budget pin');w=json.loads(gzip.decompress(raw));cs=json.loads(cr);paid=json.loads(br);M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(len(M)==400,'400q inputs');frames=list(map(span,w['frames']));idx={f:i for i,f in enumerate(sorted(set(frames)))};canon={i:idx[f] for i,f in enumerate(frames)};want={c['event']:c for c in cs};loans=quiet(w,M);edges={x['start'] for x in loans};plain,ps=propagate(w,M,canon,want,set());hybrid,hs=propagate(w,M,canon,want,edges);need(plain==hybrid,'hybrid demand knowledge equality');union=0
 for v in hybrid.values():union|=v
 U=sorted(q for q in M if not(union>>q)&1);us=set(U);R=[{int(k):Q(v) for k,v in c['target_row'].items() if int(k) in us} for c in cs];need(len(U)==134 and rank(R)==4,'common-unreachable rank');need(all(w['initial'][q]!=3 for q in U),'preloads vanish onU');need([len(r) for r in R]==[32,29,34,36],'row supports');cols=[4,2,1,0];minor=[[str(r.get(k,Q(0))) for k in cols] for r in R];need(minor==[['-3/4','0','0','0'],['0','-1/4','0','0'],['1/2','1/2','1/2','0'],['0','0','0','-8']],'rank4 minor');demands=[]
 for c in cs:
  known=hybrid[c['event']];missing=sorted(int(k) for k in c['target_row'] if w['initial'][int(k)]!=3 and not(known>>int(k))&1);demands.append({'event':c['event'],'destination':c['to'],'base_reachable_q':sorted(q for q in M if(known>>q)&1),'missing_distributed_q':missing,'missing_count':len(missing)})
 need([d['missing_count'] for d in demands]==[32,37,49,52],'four misses');relevant=set().union(*(set(r) for r in R));classes=defaultdict(list);records=[]
 for t,h,a,b,known in hs:
  remaining=rank([{k:v for k,v in r.items() if not(known>>k)&1} for r in R]);need(remaining==4,'onehelper acquisition intersection');support=tuple(sorted(q for q in relevant if(known>>q)&1));classes[support].append(t);records.append([t,h,a,b,list(support),remaining])
 need(len(ps)==2277 and len(hs)==2221,'allhelper source census');den=int(paid['additional_per_native_headroom']['denominator']);lo,hi=map(int,paid['additional_per_native_headroom']['numerator_bounds']);need(3*den<lo<=hi<4*den,'strict paid ceiling3');need(rank(R[:3])==3,'3broadcast control');need(rank([{k:v for k,v in r.items() if k not in R[0]} for r in R])==3,'synthetic sender control')
 return {'status':'PASS_TEMPORAL_FOUR_RETURN_RANK_BARRIER','source_sha256':PIN,'historical_certificate_sha256':CERT,'budget_sha256':BUDGET,'funded_main_moves':sum(e[0]=='MOVE' and e[1] in M for e in w['program']),'funded_owned_moves':sum(e[0]=='MOVE' and e[1]>=w['public'] for e in w['program']),'quiet_windows':loans,'quiet_window_count':354,'quiet_unique_timed_arcs':141,'quiet_improves_demand_knowledge':False,'demands':demands,'common_unreachable_q':U,'common_unreachable_count':134,'restricted_rows':[{str(k):str(v) for k,v in r.items()} for r in R],'restricted_supports':[len(r) for r in R],'restricted_rank':4,'rank_minor_columns':cols,'rank_minor':minor,'rank_minor_determinant':'-3/4','plain_helper_sources_before_deadline':len(ps),'additional_nonquiet_helper_sources_examined':len(hs),'helper_source_classes':[{'known_relevant_q':list(s),'events':es,'remaining_rank':4} for s,es in sorted(classes.items())],'helper_source_record_sha256':hashlib.sha256((json.dumps(records,separators=(',',':'))+'\n').encode()).hexdigest(),'minimum_new_message_fields':4,'paid_extra_arrival_ceiling':3,'minimum_nonquiet_U_informative_helper_messages_if_paid_extras_at_most3':2,'controls':{'3global_rows':'rank3','4global_rows':'rank4_free_broadcast_only','synthetic_source_first_row_support':'intersection_dimension1'},'scope':'Fixed main/owned calendar plus allquiet arcs with unlimitedcapacity; four returnedrows decodedbyreturn deadlines; original chart3-only preloads. Atmost3newpaidfields cannot suffice with0or1additional U-informative helper messages. Changedtiming/geometry,deferredowneddecoding and fulljointcode remainopen. No newkappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--budget',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();d=run(a.source,a.certificate,a.budget);s=json.dumps(d,sort_keys=True,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in d.items() if k not in ('quiet_windows','demands','common_unreachable_q','restricted_rows','helper_source_classes','rank_minor')},sort_keys=True,indent=2))
