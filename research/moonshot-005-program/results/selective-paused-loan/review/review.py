import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
HOIST={30832,30848,42670,43452}
def need(p,m):
 if not p:raise ValueError(m)
def span(vs):
 s={0}
 for v in vs:s.update(x^v for x in tuple(s))
 return frozenset(s)
def adjoint(w,role,cut):
 row={role:F(1)}
 for e in reversed(w['program'][:cut]):
  op,h=e[:2]
  if op in ['INIT','CLEAR']:row.pop(h,None)
  elif op=='SCALE':
   if h in row:row[h]*=F(e[2])
  elif op in ['ADD','COPY']:
   c=row.get(h,F(0))
   if op=='COPY':row.pop(h,None)
   if c:
    s=e[2];v=row.get(s,F(0))+c*F(e[3])
    if v:row[s]=v
    else:row.pop(s,None)
 return {q:v for q,v in row.items() if q<w['public'] and v}
def build(w):
 main=sorted(set(w['live'])|{q+112 for q in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
 qm={q:1480+j for j,q in enumerate(main)};K=1880+w['owned_fields'];D=qm[101];Y=qm[213]
 def common(e):
  e=e.copy();e[1]+=400 if e[1]>=1480 else 0
  if e[0] in ['ADD','COPY']:e[2]+=400 if e[2]>=1480 else 0
  return e
 def source_chunk(start,end,skip=frozenset()):
  result=[]
  for t in range(start,end):
   e=w['program'][t];result.append(common(e))
   if e[0]=='MOVE' and e[1] in qm and t not in skip:result.append(['MOVE',qm[e[1]],e[2],e[3],False])
  return result
 entering=[['ADD',qm[q],q,'-1',w['initial'][q]] for q in main]
 leaving=[['ADD',qm[q],q,'1',w['final'][q]] for q in main]
 base=entering+source_chunk(0,len(w['program']))+leaving
 prefix=entering+source_chunk(0,30773)
 opening=[['ADD',151,D,'1',327],['ADD',D,151,'-1',327],['ADD',151,D,'1',327]]
 bridge=[['MOVE',151,327,541,False],['INIT',K,541],['ADD',K,151,'1',541]]
 for t in [30824,30826,30830]:
  e=w['program'][t];need(e[0]=='MOVE' and e[1]==1481 and e[4] is True,'funded source route')
  bridge.append(['MOVE',K,e[2],e[3],True])
 e=w['program'][30832];need(e==['MOVE',213,3,594,False],'receiver route')
 bridge.extend([['MOVE',Y,3,594,False],['ADD',Y,K,'1',594],['CLEAR',K,594]])
 for t in [30848,42670,43452]:
  e=w['program'][t];need(e[0]=='MOVE' and e[1]==101,'donor source route');bridge.append(['MOVE',D,e[2],e[3],False])
 repair=[['INIT',K,127],['ADD',K,D,'1',127],['MOVE',K,127,541,True],
         ['ADD',151,K,'-1',541],['ADD',K,151,'1',541],['ADD',151,K,'-1',541],['ADD',K,151,'1',541],
         ['MOVE',K,541,127,True],['ADD',D,K,'1',127],['CLEAR',K,127]]
 local=opening+bridge+repair;program=prefix+local+source_chunk(30774,len(w['program']),HOIST)+leaving
 return main,qm,K,base,program,local,len(prefix)+len(local)-1,len(prefix)
def typed(meta,program,capture):
 space=list(map(span,meta['frames']));p=meta['public'];cur=list(meta['initial'])+[None]*meta['owned_fields'];counts=Counter();hist=Counter();born=peak=0;used=set();snapshot=None
 for t,e in enumerate(program):
  op,h=e[:2];need(0<=h<len(cur),'role bounds');counts[op]+=1
  if op=='INIT':need(h>=p and cur[h] is None,'fresh INIT');cur[h]=e[2];born+=1;used.add(h)
  elif op=='CLEAR':need(h>=p and cur[h]==e[2],'owned CLEAR');cur[h]=None
  elif op=='MOVE':
   a,b,owned=e[2:];need(cur[h]==a and type(owned) is bool and owned==(h>=p),'typed MOVE source/owner')
   need(space[a]<space[b] or owned and space[b]<space[a],'proper permitted MOVE')
   hist[abs(len(meta['frames'][a])-len(meta['frames'][b]))]+=1;cur[h]=b
  elif op in ['ADD','COPY']:
   s,c,f=e[2:];need(h!=s and cur[h] is not None and cur[s] is not None and cur[h]==cur[s]==f and F(c)!=0,'live cochart ADD/COPY')
  elif op=='SCALE':need(cur[h]==e[3] and F(e[2])!=0,'SCALE type')
  else:raise ValueError('unknown operation')
  peak=max(peak,sum(q is not None for q in cur[p:]))
  if t==capture:snapshot=cur.copy()
 need(cur[:p]==meta['final'] and all(q is None for q in cur[p:]),'all final charts and cleanup')
 return {'counts':dict(counts),'move_histogram':{str(k):v for k,v in sorted(hist.items())},'owned_lifetimes':born,'peak_owned':peak,'owned_labels_used':len(used),'final_owned':0},snapshot

def local_algebra(ops,qm,K):
 # Three arbitrary complete fields h,x,y; stronger than any fixed1480-input h row.
 D=qm[101];Y=qm[213];v={151:[F(1),F(0),F(0)],D:[F(0),F(1),F(0)],Y:[F(0),F(0),F(1)]};loc={151:327,D:327,Y:3}
 for e in ops:
  op,h=e[:2]
  if op=='INIT':need(h==K and h not in loc,'local init');loc[h]=e[2];v[h]=[F(0)]*3
  elif op=='CLEAR':need(loc[h]==e[2],'local clear');loc.pop(h);v.pop(h)
  elif op=='MOVE':need(loc[h]==e[2],'local move source');loc[h]=e[3]
  elif op=='ADD':
   s,c,f=e[2:];need(h!=s and loc[h]==loc[s]==f,'local cochart');v[h]=[a+F(c)*b for a,b in zip(v[h],v[s])]
  else:raise ValueError('unexpected local op')
 need(v[151]==[F(1),F(0),F(0)] and v[D]==[F(0),F(1),F(0)] and v[Y]==[F(0),F(1),F(1)],'exact h,x,y resumption map')
 need(loc=={151:541,D:127,Y:594} and K not in v,'local charts and retiredscratch')
 return v

def run(source,author):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));receipt=json.loads((author/'RESULT.json').read_text());data=gzip.decompress((author/'selective-paused-word.json.gz').read_bytes());meta=json.loads(data)
 main,qm,K,base,program,local,cut,prefix_len=build(w)
 need(len(main)==400 and len(program)==73791 and len(base)==73771,'whole source-derived dimensions')
 need(program==meta['program'],'independent entire literal schedule')
 need(meta['initial']==w['initial']+[w['initial'][q] for q in main] and meta['final']==w['final']+[w['final'][q] for q in main],'physical input/output chart maps')
 need(meta['public']==1880 and meta['owned_fields']==52 and meta['frames']==w['frames'],'physical role/frame declarations')
 need(meta['difference_role_map']=={str(q):h for q,h in qm.items()},'full raw-role map')
 need(meta['restoration_checkpoint']['loan_physical_event']==cut and meta['restoration_checkpoint']['baseline_physical_event']==prefix_len,'exact resume cut')
 need([x['source_event'] for x in meta['retimed_main_MOVEs']]==sorted(HOIST),'exact four hoisted occurrences')
 for record in meta['retimed_main_MOVEs']:
  e=w['program'][record['source_event']];at=record['physical_event']
  need(prefix_len<=at<=cut and program[at]==['MOVE',qm[e[1]],e[2],e[3],False],'exact hoisted physical index')
 bill,atcut=typed(meta,program,cut);basebill,basecut=typed(meta,base,prefix_len)
 need(bill==receipt['loan_bill'] and basebill==receipt['baseline_bill'],'independent full operation/lifecycle bill')
 local_algebra(local,qm,K)
 common=[h for h in range(len(basecut)) if (h<1480 or h>=1880) and basecut[h] is not None]
 need(len(common)==1492 and all(atcut[h]==basecut[h] for h in common),'all common cut charts')
 for q,h in qm.items():need(atcut[h]==(127 if q==101 else 594 if q==213 else basecut[h]),'all400 selective raw cut charts')
 # Every common operation outside the paused three-field macro is exact source;
 # COPY's sole zero precondition is checked independently at its original cut.
 copies=[]
 for t,e in enumerate(w['program']):
  if e[0]=='COPY':need(not adjoint(w,e[1],t),'source COPY destination identicallyzero on all1480 inputs');copies.append(t)
 need(len(copies)==1,'COPY census')
 need(adjoint(w,213,len(w['program']))=={213:F(1),101:F(1)},'original selected common endpoint')
 # Preserve each raw field's complete ordered itinerary; four calls only are advanced.
 for q,h in qm.items():
  original=[e[2:] for e in w['program'] if e[0]=='MOVE' and e[1]==q]
  actual=[e[2:] for e in program if e[0]=='MOVE' and e[1]==h]
  need(original==actual,'every raw-main ordered itinerary')
 delta=Counter(bill['counts']);delta.subtract(basebill['counts']);delta={k:v for k,v in delta.items() if v}
 need(delta=={'ADD':11,'MOVE':5,'INIT':2,'CLEAR':2},'complete operation delta')
 # Independent integer-power check for the claimed incremental2rank2price.
 D=10**18;lo=3986161051311471336;hi=3986161051311471337
 need(lo**200<2**399*D**200<hi**200,'strict new paid-moment enclosure')
 controls=[]
 bad=[e[:] for e in local];j=next(i for i,e in enumerate(bad) if e[:3]==['ADD',qm[213],K]);bad[j][3]='-1'
 try:local_algebra(bad,qm,K)
 except ValueError:controls.append('wrong receiver shear rejected')
 else:raise ValueError('wrong receiver accepted')
 bad=[e[:] for e in local];j=max(i for i,e in enumerate(bad) if e[0]=='ADD' and e[1]==qm[101]);bad.pop(j)
 try:local_algebra(bad,qm,K)
 except ValueError:controls.append('missing donor restoration rejected')
 else:raise ValueError('unrestored donor accepted')
 bad=[e[:] for e in local];j=next(i for i,e in enumerate(bad) if e==['MOVE',qm[213],3,594,False]);bad.pop(j)
 try:local_algebra(bad,qm,K)
 except ValueError:controls.append('missing receiver hoist rejected by chart')
 else:raise ValueError('missing receiver hoist accepted')
 bad=[e[:] for e in program];j=next(i for i,e in enumerate(bad) if e==['MOVE',K,127,541,True]);bad[j][4]=False
 try:typed(meta,bad,cut)
 except ValueError:controls.append('false public descent rejected')
 else:raise ValueError('false descent accepted')
 files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(author.iterdir()) if p.is_file()}
 return {'status':'PASS_INDEPENDENT_SELECTIVE_PAUSE_REVIEW','source_sha256':PIN,'reviewed_author_files':files,
 'methods':['independent prefix/macro/suffix reconstruction of all73791 instructions','full typed chart/lifecycle and raw itinerary checks','exact3-field universal resumption algebra','reverse-adjoint COPY and selected common endpoint checks'],
 'endpoint_proof':'Composition proves all1880 independent-input endpoint rows; this reviewer does not rerun a full1880-column forward matrix interpreter.',
 'common_rows_preserved_by_resumption':1492,'raw_states_and_charts_certified':400,'hoisted_source_events':sorted(HOIST),'physical_instructions':len(program),'bill':bill,'operation_delta':delta,
 'selected_second_endpoint':{str(qm[213]):'1',str(qm[101]):'1'},'new_paid_moment_interval':[str(F(lo,D)),str(F(hi,D))],
 'controls':controls,'scope':'Exact partial q101-to-q213 endpoint map with arbitrary dirty common inputs and four selective hoists. Originaldelta1481 duties and composition with the full difference native remain unproved. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source,a.author);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='reviewed_author_files'},sort_keys=True,indent=2))
