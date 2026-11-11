import gzip,json,collections,bisect,time
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib
from verify import PIN,space as canon,need,add
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();SOURCE=args.source;need(hashlib.sha256(SOURCE.read_bytes()).hexdigest()==PIN,'source pin')
w=json.loads(gzip.decompress(SOURCE.read_bytes()));P=w['program'];end=len(P);M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);C=[canon(f) for f in w['frames']];write=collections.defaultdict(list);touch=collections.defaultdict(list);motion=collections.defaultdict(list);visits={};state={i:(-1,w['initial'][i]) for i in M}
for i,f in enumerate(w['initial']):motion[i].append((-1,f))
for k,e in enumerate(P):
 tag,r=e[:2];touch[r].append(k);
 if tag in ('MOVE','INIT','CLEAR'):write[r].append(k)
 if tag in ('ADD','COPY'):touch[e[2]].append(k)
 if tag=='MOVE':
  motion[r].append((k,e[3]))
  if r in M:
   a,f=state[r];visits[r,C[f]]=(a,k);state[r]=(k,e[3])
 elif tag=='INIT':motion[r].append((k,e[2]))
 elif tag=='CLEAR':motion[r].append((k,None))
for i,(a,f) in state.items():visits[i,C[f]]=(a,end)
def current(r,k):return motion[r][bisect.bisect_right(motion[r],(k,10**6))-1][1]
# Indexed scalar events suffice; MOVE transports the same pending coefficient.
scalar=[(k,e) for k,e in enumerate(P) if e[0]!='MOVE'];times=[k for k,e in scalar]
candidates=[];valid=[];quiet=[];counts=collections.Counter();start=time.time()
for k,e in enumerate(P):
 if e[0]!='MOVE' or e[1] in M:continue
 h,s,d=e[1:4];i=bisect.bisect_right(write[h],k);deadline=write[h][i] if i<len(write[h]) else end
 for q in sorted(M):
  a,b=visits.get((q,C[s])),visits.get((q,C[d]))
  if not(a and b and a[0]<k<a[1] and k<b[0]<deadline):continue
  close=b[0];nread=sum(1 for j in touch[h] if k<j<close)
  if not nread:counts['quiet']+=1;quiet.append(k);continue
  counts['scalar_active_candidates']+=1;alpha={h:F(1)};suppressed=[];copybad=False
  for ix in range(bisect.bisect_right(times,k),bisect.bisect_right(times,close)):
   j,op=scalar[ix];tag,r=op[:2]
   if tag in ('INIT','CLEAR'):alpha.pop(r,None)
   elif tag=='SCALE':
    if r in alpha:alpha[r]*=F(op[2])
   elif tag in ('ADD','COPY'):
    v=op[2]
    if tag=='COPY' and alpha.get(r):copybad=True;break
    if v==h:suppressed.append(j)
    z=alpha.get(r,F(0))+F(op[3])*alpha.get(v,F(0))
    if z:alpha[r]=z
    else:alpha.pop(r,None)
  if copybad:counts['bad_COPY']+=1;continue
  wrong=[r for r,v in alpha.items() if r!=h and current(r,close)!=d]
  rec={'start':k,'close':close,'next_helper_MOVE_or_lifecycle':deadline,'helper':h,'donor':q,'from':s,'to':d,'suppressed_reads':suppressed,'pending_coefficients':{str(r):str(v) for r,v in sorted(alpha.items()) if r!=h},'out_of_chart':wrong}
  candidates.append(rec)
  if not wrong:rec['helper_pending_coefficient']=str(alpha.get(h,F(0)));valid.append(rec);counts['valid']+=1
need(dict(counts)=={'scalar_active_candidates':80,'quiet':354,'valid':34},'finite candidate census')
rows=[{i:F(1)} if i in M else {} for i in range(w['public']+w['owned_fields'])]
for e in P:
 tag,r=e[:2]
 if tag in ('INIT','CLEAR'):rows[r]={}
 elif tag=='SCALE':rows[r]={i:F(e[2])*v for i,v in rows[r].items()}
 elif tag in ('ADD','COPY'):rows[r]=add(rows[r],rows[e[2]],F(e[3]))
cases={}
for name,extra in [('quiet',set(quiet)),('quiet_plus_all_immediate_closure',set(quiet)|{r['start'] for r in valid})]:
 B=collections.defaultdict(int)
 for i in M:B[C[w['initial'][i]]]|=1<<i
 for k,e in enumerate(P):
  if e[0]=='MOVE' and (e[1] in M or e[4] or k in extra):B[C[e[3]]]|=B[C[e[2]]]
 cases[name]=[(i,j,str(v)) for i in sorted(M) for j,v in sorted(rows[i].items()) if not(B[C[w['final'][i]]]>>j&1)]
need(cases['quiet']==cases['quiet_plus_all_immediate_closure'] and len(cases['quiet'])==102,'no endpoint reach gain from all34 windows')
wraw=Path(__file__).with_name('ENDPOINT-WITNESS.json').read_bytes();need(hashlib.sha256(wraw).hexdigest()=='a980369a753febb491038c82f6e88f553efc5fbd7c6049abc0101d71c8659c7c','inherited46 witness pin');cert=json.loads(wraw);pairs=cert['witness_pairs'];K=sum(1<<r['input'] for r in pairs);det=F(1)
for z in pairs:
 need(not(B[C[w['final'][z['output']]]]&K),'all2116 exclusions survive active windows');need({j:v for j,v in rows[z['output']].items() if K>>j&1}=={z['input']:F(z['coefficient'])},'same diagonal endpoint restriction');det*=F(z['coefficient'])
need(len(pairs)==46 and det==F(1,8),'same46-rank witness')
alpha={151:F(1)}
for e in P[30774:]:
 tag,r=e[:2]
 if tag in ('INIT','CLEAR'):alpha.pop(r,None)
 elif tag=='SCALE':
  if r in alpha:alpha[r]*=F(e[2])
 elif tag in ('ADD','COPY'):
  z=alpha.get(r,F(0))+F(e[3])*alpha.get(e[2],F(0))
  if z:alpha[r]=z
  else:alpha.pop(r,None)
need(len(alpha)==425 and sum(w['final'][i]==127 for i in alpha)==373,'uncorrected151 shadow debt')
out={'status':'PASS_SCOPED_IMMEDIATE_CLOSURE_CENSUS','source_sha256':PIN,'counts':dict(counts),'valid_windows':valid,'distinct_valid_starts':len({r['start'] for r in valid}),'rejected_candidates':[r for r in candidates if r not in valid],'quiet_starts':len(set(quiet)),'inherited_endpoint_witness_sha256':hashlib.sha256(wraw).hexdigest(),'selected_excluded_pairs':2116,'selected_endpoint_rank':46,'selected_endpoint_determinant':'1/8','missing_endpoint_coefficients':cases,'helper151_uncorrected_continuation':{'nonzero_final_debt_roles':425,'at_chart127':373,'other_final_roles':52},'scope':'One raw main donor, one helper before its next MOVE/INIT/CLEAR, no debt-bearing COPY destination, all surviving scalar debts cochart at donor arrival. No intermediate correction, paid repair, paused common calendar, encoded donor, or multi-escrow code. All34 simultaneously granted only as a generous impossibility relaxation; not claimed jointly composable.'}
args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'counts':out['counts'],'distinct_valid_starts':out['distinct_valid_starts'],'missing_endpoint_coefficients':102},indent=2))
