"""Independent modular demand history; capacities merged in a separate time-line pass."""
from independent import *
from bisect import bisect_right

def review(source,author):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));expected=json.loads(author.read_text());n=w['public'];m=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 modes=('all_main_current','main_departure_and_endpoint','endpoint_only');rows=[[{r:1} if r<n else {} for r in range(n+w['owned_fields'])],[{r:1} if r in m else {} for r in range(n+w['owned_fields'])]];groups={};keys=[groups.setdefault(canon(f),i) for i,f in enumerate(w['frames'])];frame=w['initial'][:]+[None]*w['owned_fields'];cb=defaultdict(dict);db={k:defaultdict(dict) for k in modes};demand={k:defaultdict(list) for k in modes};funded=defaultdict(list);history={k:[] for k in modes}
 for r in range(n):
  f=keys[frame[r]];insert(rows[0][r],cb[f])
  for mode in modes:insert(rows[1][r],db[mode][f])
 def ask(mode,f,time,amount):
  if amount:
   demand[mode][f].append((time,amount));history[mode].append([time[0],f,amount,{0:'departure',2:'arrival',3:'main-update',4:'endpoint'}[time[1]]])
 for i,e in enumerate(w['program']):
  op,r=e[:2]
  if op in ('INIT','CLEAR'):
   need(r>=n and (frame[r] is None if op=='INIT' else frame[r]==e[2]),'lifetime');frame[r]=e[2] if op=='INIT' else None;rows[0][r]={};rows[1][r]={}
  elif op=='MOVE':
   need(frame[r]==e[2] and bool(e[4])==(r>=n),'MOVE guard');src,dst=keys[e[2]],keys[e[3]];kind='main' if r in m else 'helper' if r<n else 'owned'
   if r in m:ask('main_departure_and_endpoint',src,(i,0),insert(rows[1][r],db['main_departure_and_endpoint'][src]))
   funded[dst].append(((i,1),2 if kind=='main' else 1,2 if kind in ('main','owned') else 1));common=insert(rows[0][r],cb[dst]);frame[r]=e[3]
   for mode in modes:ask(mode,dst,(i,2),common+(insert(rows[1][r],db[mode][dst]) if r in m and mode=='all_main_current' else 0))
  elif op=='SCALE':
   factor=c(e[2]);need(frame[r]==e[3] and factor,'SCALE')
   for j in (0,1):rows[j][r]={k:factor*x%P for k,x in rows[j][r].items()}
  elif op in ('ADD','COPY'):
   s=e[2];need(r!=s and frame[r]==frame[s]==e[4],'cochart')
   for j in (0,1):
    if op=='COPY':need(not rows[j][r],'COPYzero')
    add(rows[j][r],rows[j][s],c(e[3]))
   if r in m:
    mode='all_main_current';f=keys[frame[r]];ask(mode,f,(i,3),insert(rows[1][r],db[mode][f]))
 for r in sorted(m):
  f=keys[frame[r]]
  for mode in modes:ask(mode,f,(len(w['program']),4),insert(rows[1][r],db[mode][f]))
 calendars={}
 for f,entries in funded.items():
  dates=[x[0] for x in entries];totals=[[0],[0]]
  for _,a,b in entries:totals[0].append(totals[0][-1]+a);totals[1].append(totals[1][-1]+b)
  calendars[f]=(dates,totals)
 floors={};bychart={}
 for mode in modes:
  floors[mode]={};bychart[mode]={}
  for k in (1,2):
   results={}
   for f,entries in demand[mode].items():
    dates,totals=calendars.get(f,([],[ [0],[0] ]));required=best=0;where=None
    for time,amount in entries:
     required+=amount;used=totals[k-1][bisect_right(dates,time)];deficit=required-used
     if deficit>best:best=deficit;where=time[0]
    if best:results[str(f)]=[best,where]
   bychart[mode][str(k)]=results;floors[mode][str(k)]=sum(v[0] for v in results.values())
 need(floors==expected['extra_arrival_floors'],'all three demand floors')
 need(bychart==expected['by_chart'],'all chart prefix maxima/argmaxes')
 need(history==expected['records'],'all weaker innovation records')
 return {'status':'PASS_INDEPENDENT_MODULAR_DEPARTURE_AND_WEAKER_DEMAND_FLOORS','prime':P,'native_sha256':PIN,'author_result_sha256':hashlib.sha256(author.read_bytes()).hexdigest(),'method':'Finite-field max-pivot replay; separate demand-history/funded-calendar merge using ordered event phases and bisect','extra_arrival_floors':floors,'records_compared':{k:len(v) for k,v in history.items()},'chronology':'Departure phase0, funding phase1, arrival demand phase2, main update phase3, endpoint phase4. Future arrivals do not fund departure observations.','scope':'Common first-copy current rows always decoded, fixed funded calendar. Endpoint-only zero means this relaxation gives no obstruction; it proves no physical feasibility.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=review(a.source,a.author);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
