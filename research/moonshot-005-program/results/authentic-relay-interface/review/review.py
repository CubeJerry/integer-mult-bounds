import argparse,bisect,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from source_rows import PIN,need,adjoint,combine

def reconstruct_quiet(word, main):
    """Use per-role position histories and contacts, not a moving cohort."""
    positions = {q: [(-1, word['initial'][q])] for q in main}
    arrival = defaultdict(list)
    contacts = defaultdict(set)
    for q in main:
        arrival[q, word['initial'][q]].append(-1)
    for t, e in enumerate(word['program']):
        contacts[e[1]].add(t)
        if e[0] in ('ADD', 'COPY'):
            contacts[e[2]].add(t)
        if e[0] == 'MOVE' and e[1] in main:
            positions[e[1]].append((t, e[3]))
            arrival[e[1], e[3]].append(t)
    contacts = {h: sorted(times) for h, times in contacts.items()}
    position_times = {q: [x[0] for x in hist] for q, hist in positions.items()}
    windows = []
    for t, e in enumerate(word['program']):
        if e[0] != 'MOVE' or e[1] in main:
            continue
        _, h, origin, destination, _ = e
        next_index = bisect.bisect_right(contacts[h], t)
        next_use = contacts[h][next_index] if next_index < len(contacts[h]) else len(word['program'])
        for q in sorted(main):
            position_index = bisect.bisect_left(position_times[q], t) - 1
            if positions[q][position_index][1] != origin:
                continue
            visits = arrival[q, destination]
            later = bisect.bisect_right(visits, t)
            if later < len(visits) and visits[later] < next_use:
                windows.append({'start': t, 'close': visits[later], 'next_use': next_use,
                                'donor': q, 'helper': h, 'from': origin, 'to': destination})
    return windows

def frame_space(frame):
 s={0}
 for v in frame:s.update(x^v for x in tuple(s))
 return frozenset(s)

def run(source,author):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw))
 main=set(w['live'])|{q+112 for q in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 cert=json.loads((author/'SOURCE-ROWS.json').read_text());prefix=json.loads((author/'CONDITIONAL-PREFIX.json').read_text())
 rows={}
 for key,claimed in cert['snapshot_rows'].items():
  cut,role=map(int,key.split(':'));row=adjoint(w,role,cut,main)
  need(row=={int(i):F(v) for i,v in claimed.items()},'fresh adjoint source row '+key);rows[key]=row
 A=rows['30773:151'];B=rows['30776:399'];M=rows['30773:130'];G=rows['30808:1507'];r=rows['30824:1481'];q130={130:F(1)};b={55:F(1,2),101:F(-1,2)}
 U=combine((1,M),(-1,B),(1,G),(F(-1,2),q130));W=combine((1,M),(1,B),(F(1,2),q130))
 need(A==combine((1,b),(F(1,2),q130)),'source entry row')
 need(r==combine((F(1,2),U),(F(-1,2),b)),'terminal source row after all local updates')
 need(U=={int(i):F(v) for i,v in cert['fused_U'].items()} and W=={int(i):F(v) for i,v in cert['fused_W_for_current_main130'].items()},'exact U/W rows')
 need([len(x) for x in [A,M,B,G,r,U,W]]==[3,15,9,34,59,57,24],'source supports')
 complete_reads=[]
 for t,e in enumerate(w['program']):
  if e[0] in ['ADD','COPY'] and e[2]==1481:
   need(30820<t<40843,'single complete source lifetime');value=adjoint(w,1481,t,main)
   need(value==r,'same original carrier at every source read')
   complete_reads.append({'event':t,'receiver':e[1],'coefficient':str(F(e[3])),'chart':e[4],
                         'row':{str(i):str(F(e[3])*v) for i,v in sorted(value.items())}})
 need(complete_reads==cert['all13_source_reads'] and len(complete_reads)==13,'all13 exact consumer records')
 need(w['program'][40843]==['CLEAR',1481,594],'true retirement event')
 spaces=list(map(frame_space,w['frames']));windows=reconstruct_quiet(w,main);extra={z['start'] for z in windows}
 need(len(windows)==354 and len(extra)==141,'independent quiet census')
 needed={spaces[541]}
 for t in range(30823,-1,-1):
  e=w['program'][t]
  if e[0]=='MOVE' and (e[1] in main or e[1]>=w['public'] or t in extra) and spaces[e[3]] in needed:needed.add(spaces[e[2]])
 reachable={q for q in main if spaces[w['initial'][q]] in needed};missing=sorted(set(U)-reachable)
 need(missing==cert['missing_U_input_roles_in_funded_graph_at30824'] and len(missing)==50,'independent reverse graph missing coordinates')
 need(4 not in reachable and 7 not in reachable,'minor inputs unreachable atcut')
 det=U[7]*W[4]-U[4]*W[7];need(det==F(-1,2),'two-observable missing minor')
 need(A[55]/2==F(1,4) and r[55]==F(-1,4),'chronology sign control')
 need(r[7]==F(-1,4) and A.get(7,0)==G.get(7,0)==0,'missing local raw-input control')
 # Independent dense four-coordinate interpreter for the conditional prefix.
 value={i:[F(i==j) for j in range(4)] for i in range(4)};chart={i:541 for i in range(4)};ops=Counter();hist=Counter()
 for e in prefix['program']:
  tag,h=e[:2];ops[tag]+=1
  if tag=='INIT':need(h>=4 and h not in chart,'fresh owned module output');chart[h]=e[2];value[h]=[F(0)]*4
  elif tag=='MOVE':
   a,d,owned=e[2:];need(h>=4 and owned is True and chart[h]==a and (spaces[a]<spaces[d] or spaces[d]<spaces[a]),'proper typed owned MOVE')
   hist[abs(len(w['frames'][a])-len(w['frames'][d]))]+=1;chart[h]=d
  elif tag=='SCALE':need(chart[h]==e[3] and F(e[2])!=0,'SCALE type');value[h]=[F(e[2])*x for x in value[h]]
  elif tag=='ADD':need(h!=e[2] and chart[h]==chart[e[2]]==e[4],'live cochart ADD');value[h]=[a+F(e[3])*b0 for a,b0 in zip(value[h],value[e[2]])]
  else:raise ValueError('unexpected prefix operation')
 expected=[F(-1,2),F(-1,2),F(1,2),F(1,2)]
 need(value[4]==expected and value[5]==[4*x for x in expected] and value[6]==expected,'three owned record values')
 need(value[0]==[2*x for x in expected] and value[2]==[F(1),F(1),F(1),F(0)],'both updated local public ports')
 need(chart[4]==594 and chart[5]==534 and chart[6]==117,'output record charts')
 need(ops==Counter({'ADD':7,'INIT':3,'MOVE':3,'SCALE':2}) and hist==Counter({1:2,4:1}),'complete15instruction bill')
 for read,obs in zip(complete_reads,prefix['observations']):
  need(read['event']==obs['event'] and read['receiver']==obs['receiver'] and read['chart']==obs['chart'],'observer source chronology')
  rec=obs['record'];need(chart[rec]==read['chart'],'record physical cochart')
  need([F(obs['multiplier'])*x for x in value[rec]]==[F(read['coefficient'])*x for x in expected],'all13 increments factor through records')
 need(len(prefix['observations'])==13 and len(chart)-4==3 and prefix['clear_operations_implemented']==0,'three live owned outputs; no hidden cleanup')
 files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(author.iterdir()) if p.is_file()}
 return {'status':'PASS_INDEPENDENT_AUTHENTIC_RELAY_REDUCTION_REVIEW','source_sha256':PIN,'reviewed_author_files':files,
  'methods':['fresh reverse-adjoint source rows at all cuts and13 reads','reverse-time funded graph and independent quiet windows','dense4-input typed module interpreter'],
  'actual_relay_support':59,'U_support':57,'W_support':24,'complete_source_reads':13,'retirement_event':40843,
  'missing_U_coordinates':50,'two_observable_minor':'-1/2','prefix_instructions':15,'prefix_counts':dict(ops),
  'prefix_owned_move_histogram':dict(hist),'live_owned_outputs':3,'implemented_CLEARs':0,
  'controls':{'incorrect_half_entry_q55':'1/4 versus required−1/4','q7_only_missing_boundary':'required−1/4 with raw localq and G zero'},
  'scope':'Exact source reduction and conditional four-port prefix only. Actual input acquisition, receiver-state continuation, chronological composition and retirement remain obligations. No global1880-input word, source-authentic supplier or kappa is established.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source,a.author)
 a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='reviewed_author_files'},sort_keys=True,indent=2))


