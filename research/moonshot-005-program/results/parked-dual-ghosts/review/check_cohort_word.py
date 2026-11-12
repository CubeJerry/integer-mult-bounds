#!/usr/bin/env python3
"""Independent literal reconstruction, input-row and tariff audit of cohort8."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from cohort_geometry import derive,space,require,SOURCE_PIN,FRAME

PARENT_PIN='1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153'
PARENT_PAYLOAD='05b503f0c2f219f328353b984ca821db9d6c3cc0225ff3380c551708d247e8d8'
WORD_PAYLOAD='b729da0247aac10019ce6bdd93017b64d185e00101c57f655165a44c4d445f3b'
INVOICE_PIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(path,compressed=False,pin=None,payload=None):
 b=path.read_bytes()
 if pin:require(sha(b)==pin,'immutable source pin '+str(path))
 if compressed:b=gzip.decompress(b)
 if payload:require(sha(b)==payload,'exact payload pin '+str(path))
 return json.loads(b)
def inverse(a):
 n=len(a);z=[list(map(F,r))+[F(i==j) for j in range(n)] for i,r in enumerate(a)]
 for c in range(n):
  k=next((k for k in range(c,n) if z[k][c]),None)
  if k is None:return None
  z[k],z[c]=z[c],z[k];v=z[c][c];z[c]=[x/v for x in z[c]]
  for k in range(n):
   if k!=c:
    v=z[k][c];z[k]=[x-v*y for x,y in zip(z[k],z[c])]
 return [r[n:] for r in z]
def rowadd(a,b,c=F(1)):
 z=a.copy()
 for i,v in b.items():
  q=z.get(i,F(0))+c*v
  if q:z[i]=q
  else:z.pop(i,None)
 return z
def combine(coeff,rows):
 out={}
 for c,row in zip(coeff,rows):
  if c:out=rowadd(out,row,F(c))
 return out

def reconstruct(source,parent,geometry):
 old=parent['program'];raw={int(k):v for k,v in parent['private_role_map'].items()}
 require(len(old)==74757 and parent['marks']['common_starts']==2046,'parent source boundary')
 hoist={o[1]:e for e,o in enumerate(old[410:514],410)}
 require(set(hoist)=={raw[x] for x in source['live']},'exact104 donor hoist block')
 out=old[:410].copy();lineage=list(range(410));groups=[]
 collectors={r+112:1937+i for i,r in enumerate(FRAME)};facets={r+112:source['final'][r+112] for r in FRAME}
 def emit(op,event=None):
  if event is None and op[0]=='MOVE' and op[1] in hoist:event=hoist[op[1]]
  out.append(op);lineage.append(event)
 for y in sorted(collectors):emit(['INIT',collectors[y],facets[y]])
 for x in FRAME:emit(old[hoist[raw[x]]],hoist[raw[x]])
 for gi,g in enumerate(geometry['groups']):
  donors=g['donors'];ys=[r+112 for r in g['receivers']];chart=1095+gi;A=[list(map(F,row)) for row in g['A']];candidates=[]
  for cols in combinations(range(len(donors)),4):
   minor=[[row[j] for j in cols] for row in A];inv=inverse(minor)
   if inv is not None:candidates.append((sum(bool(x) for row in inv for x in row),tuple(donors[j] for j in cols),cols,minor,inv))
  require(candidates,'independently derived invertible minor')
  _,pivots,cols,minor,inv=min(candidates);pivots=list(pivots);nonpivots=[d for d in donors if d not in pivots];column={d:i for i,d in enumerate(donors)}
  gc=dict(donors=donors,receivers=ys,chart=chart,pivots=pivots,nonpivots=nonpivots,matrix=A,pivot_minor=minor,inverse_minor=inv,begin=len(out))
  acc=list(range(1945,1949));snaps=list(range(1949,1953))
  for a in acc:emit(['INIT',a,chart])
  for d in nonpivots:
   emit(['MOVE',raw[d],source['initial'][d],chart,False])
   for i in range(4):
    if A[i][column[d]]:emit(['ADD',acc[i],raw[d],str(A[i][column[d]]),chart])
   emit(['MOVE',raw[d],chart,127,False])
  for d in pivots:emit(['MOVE',raw[d],source['initial'][d],chart,False])
  for s,d in zip(snaps,pivots):emit(['INIT',s,chart]);emit(['ADD',s,raw[d],'1',chart])
  gc['snapshots']=len(out)
  for i,d in enumerate(pivots):
   emit(['ADD',raw[d],snaps[i],'-1',chart])
   for j,s in enumerate(snaps):
    if minor[i][j]:emit(['ADD',raw[d],s,str(minor[i][j]),chart])
   emit(['ADD',raw[d],acc[i],'1',chart])
  gc['payloads']=len(out)
  for s in acc+snaps:emit(['CLEAR',s,chart])
  for d,y in zip(pivots,ys):
   emit(['MOVE',raw[d],chart,facets[y],False]);emit(['ADD',collectors[y],raw[d],'1',facets[y]]);emit(['MOVE',raw[d],facets[y],127,False])
  gc['payloads_at_hub']=len(out)
  for i,d in enumerate(pivots):
   for n in nonpivots:
    if A[i][column[n]]:emit(['ADD',raw[d],raw[n],str(-A[i][column[n]]),127])
  for s,d in zip(snaps,pivots):emit(['INIT',s,127]);emit(['ADD',s,raw[d],'1',127])
  gc['inverse_snapshots']=len(out)
  for i,d in enumerate(pivots):
   emit(['ADD',raw[d],snaps[i],'-1',127])
   for j,s in enumerate(snaps):
    if inv[i][j]:emit(['ADD',raw[d],s,str(inv[i][j]),127])
  gc['originals_restored']=len(out)
  for s in snaps:emit(['CLEAR',s,127])
  gc['end']=len(out);groups.append(gc)
 require(len(out)==2018,'literal2018 restoration boundary')
 reads=[]
 for e,o in enumerate(old[514:],514):
  emit(o,e)
  if o[0]=='MOVE':
   for y in collectors:
    if o[1]==raw[y] and o[3]==facets[y]:
     reads.append(dict(receiver=y,parent_move=e,read=len(out)));emit(['ADD',raw[y],collectors[y],'1',facets[y]]);emit(['CLEAR',collectors[y],facets[y]])
 require(len(reads)==8,'one actual collector read per receiver')
 return out,lineage,groups,reads

def typed(source,word):
 frames=source['frames']+[x['frame'] for x in word.get('additional_charts',[])];spaces=list(map(space,frames));loc=dict(enumerate(word['initial']));counts=Counter();ranks=Counter();rawranks=Counter();peak=0
 for e,o in enumerate(word['program']):
  kind,j=o[:2];counts[kind]+=1;require(0<=j<word['public']+word['owned_fields'],'role namespace')
  if kind=='INIT':require(j>=1880 and j not in loc,'fresh owned lifetime');loc[j]=o[2]
  elif kind=='CLEAR':require(j>=1880 and loc.get(j)==o[2],'actual owned retirement');del loc[j]
  elif kind=='MOVE':
   _,j,s,t,owned=o;require(loc.get(j)==s and type(owned)is bool and owned==(j>=1880),'actual MOVE source/owner')
   require(spaces[s]<spaces[t] or owned and spaces[t]<spaces[s],'proper nested actual MOVE');r=abs(len(frames[t])-len(frames[s]));ranks[r]+=1
   if 1480<=j<1880:rawranks[r]+=1
   loc[j]=t
  elif kind in ('ADD','COPY'):
   _,j,k,c,chart=o;require(j!=k and loc.get(j)==loc.get(k)==chart,'actual complete cochart');F(c)
  elif kind=='SCALE':require(loc.get(j)==o[3] and F(o[2])!=0,'valid SCALE')
  else:raise ValueError('unknown opcode '+kind)
  peak=max(peak,len(loc)-1880)
 require(set(loc)==set(range(1880)),'all owned lifetimes closed')
 return dict(counts=counts,ranks=ranks,rawranks=rawranks,peak=peak,final=loc)

def prefix_execute(word,stop,check=None):
 rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(word['initial']))
 for e,o in enumerate(word['program'][:stop]):
  if check:check(e,rows,loc,o)
  kind,j=o[:2]
  if kind=='INIT':rows[j]={};loc[j]=o[2]
  elif kind=='CLEAR':del rows[j];del loc[j]
  elif kind=='MOVE':loc[j]=o[3]
  elif kind=='SCALE':rows[j]={i:F(o[2])*v for i,v in rows[j].items()}
  else:
   if kind=='COPY':require(not rows[j],'exact COPY guard')
   rows[j]=rowadd(rows[j],rows[o[2]],F(o[3]))
 if check:check(stop,rows,loc,None)
 return rows,loc

def root_bounds(r):
 den=1<<192;target=r**199*den**200;lo=0;hi=r*den+1
 while hi-lo>1:
  m=(hi+lo)//2
  if m**200<=target:lo=m
  else:hi=m
 require(lo**200<=target<(lo+1)**200,'exact root bracket')
 return F(lo,den),F(lo if lo**200==target else lo+1,den)

def moment(profile):
 low=high=F(0)
 for r,n in profile.items():
  a,b=root_bounds(r);low+=n*(a if n>=0 else b);high+=n*(b if n>=0 else a)
 return low,high

def semantic(source,parent,word,groups,lineage,reads):
 raw={int(k):v for k,v in word['private_role_map'].items()};q={d:{raw[d]:F(1),d:F(-1)} for d in raw};xs=source['live'];lookup={}
 for g in groups:
  for name in ('snapshots','payloads','payloads_at_hub','inverse_snapshots','originals_restored'):
   lookup[g[name]]=(name,g)
 e8_reads=[];check_count=0
 def check(e,state,loc,op):
  nonlocal check_count
  if e in lookup:
   name,g=lookup[e];I=g['pivots'];D=g['donors'];A=g['matrix']
   if name=='snapshots':wanted={1949+i:q[d] for i,d in enumerate(I)}
   elif name in ('payloads','payloads_at_hub'):wanted={raw[d]:combine(A[i],[q[n] for n in D]) for i,d in enumerate(I)}
   elif name=='inverse_snapshots':wanted={1949+i:combine(g['pivot_minor'][i],[q[d] for d in I]) for i in range(4)}
   else:wanted={raw[d]:q[d] for d in D}
   for j,row in wanted.items():require(state[j]==row,'actual full-input checkpoint '+name);check_count+=1
  if e==2018:
   for d in xs:require(state[raw[d]]==q[d] and loc[raw[d]]==127,'all104 originals restored before E8');check_count+=1
  if op and lineage[e] is not None and 514<=lineage[e]<parent['marks']['initial_decoders'] and op[0]=='ADD' and op[2] in {raw[d] for d in xs}:
   d=next(d for d in xs if raw[d]==op[2]);require(state[op[2]]==q[d] and loc[op[2]]==127,'actual later E8 read sees original q');e8_reads.append(e)
 before,prefixloc=prefix_execute(parent,parent['marks']['common_starts'])
 after,newloc=prefix_execute(word,word['marks']['common_starts'],check)
 require(len(e8_reads)==520,'all520 retained E8 source reads')
 require(prefixloc==newloc and set(after)==set(before),'same complete live prefix interface')
 deltas={}
 from cohort_geometry import root
 roots={d:root(source['frames'][source['initial'][d]][0]) for d in xs}
 for x in FRAME:
  y=x+112;row={}
  for d in xs:
   if d!=x:
    coefficient=-F(sum(a*b for a,b in zip(roots[x],roots[d])),8)
    if coefficient:row=rowadd(row,q[d],coefficient)
  deltas[raw[y]]=row
 for j in before:require(after[j]==rowadd(before[j],deltas.get(j,{})),'all1880-column prefix difference exactly stated')
 require(word['program'][word['marks']['common_starts']:]==parent['program'][parent['marks']['common_starts']:],'entire common-and-final suffix literal identity')
 suffix=word['program'][word['marks']['common_starts']:]
 final_touches={j:[] for j in deltas}
 for e,o in enumerate(suffix,word['marks']['common_starts']):
  operands=o[1:3] if o[0] in ('ADD','COPY') else [o[1]]
  for j in final_touches:
   if j in operands:final_touches[j].append((e,o))
 for j,touches in final_touches.items():
  y=next(y for y in raw if raw[y]==j)
  require(len(touches)==1 and touches[0][1]==['ADD',j,y,'1',source['final'][y]],'changed receiver is isolated until authentic final recoupling')
 return dict(checkpoint_rows=check_count,full_input_columns=1880,E8_original_reads=len(e8_reads),prefix_delta_rows=len(deltas),unchanged_suffix_instructions=len(suffix),completed_receivers=[x+112 for x in FRAME],difference_rows={str(j):[[i,str(v)] for i,v in sorted(row.items())] for j,row in deltas.items()})

def private_inverse(source,parent,word):
 from cohort_geometry import root
 logical={int(r) for r in word['private_role_map']};xs=sorted(source['live']);roots={d:root(source['frames'][source['initial'][d]][0]) for d in xs};coupled=set(range(104))-set(source['hosted']['Dports'])
 matrix={r:{r:F(1)} for r in logical};remaining=0
 for i,x in enumerate(xs):
  y=x+112;c=F(1,2) if i in coupled else F(1);row={y:c}
  for d in xs:
   v=c*F(sum(a*b for a,b in zip(roots[x],roots[d])),8)
   if v:row[d]=v
  for d,v in parent['corrections'].get(str(y),[]):row=rowadd(row,{d:F(v)})
  if x in FRAME:row={y:F(1),x:F(1)}
  matrix[y]=row;remaining+=sum(bool(v) for d,v in row.items() if d not in (x,y))
 inv={r:{r:F(1)} for r in logical}
 for x in xs:
  y=x+112;c=matrix[y][y];inv[y]={y:1/c}
  for d,v in matrix[y].items():
   if d!=y:inv[y][d]=-v/c
 for r,row in inv.items():require(combine(list(row.values()),[matrix[k] for k in row])=={r:F(1)},'explicit400-row private inverse')
 require(remaining==4601,'exact final offdiagonal residual count')
 serial=lambda d:{str(r):[[j,str(v)] for j,v in sorted(row.items())] for r,row in sorted(d.items())}
 return dict(rows=400,remaining=remaining,matrix_sha256=sha(json.dumps(serial(matrix),sort_keys=True).encode()),inverse_sha256=sha(json.dumps(serial(inv),sort_keys=True).encode()),scope='Exact terminal difference map from authenticated parent and checked cohort delta; explicit left inverse of all400 rows.')

def mutants(source,parent,word,groups,lineage,reads):
 rejected={};g=groups[0]
 def trial(name,mutant,algebra=False):
  try:
   typed(source,mutant)
   if algebra:semantic(source,parent,mutant,groups,lineage,reads)
  except ValueError as e:rejected[name]=str(e)
  require(name in rejected,'negative control escaped '+name)
 for name,event in [('wrong_aggregate_coefficient',g['snapshots']+1),('wrong_inverse_coefficient',g['inverse_snapshots']+1)]:
  ops=[o.copy() for o in word['program']];ops[event][3]=str(-F(ops[event][3]));trial(name,dict(word,program=ops),True)
 ops=[o.copy() for o in word['program']];ops[g['snapshots']+7][2]=int(word['private_role_map'][str(g['pivots'][0])]);trial('stale_partially_transformed_pivot',dict(word,program=ops),True)
 firstmove=next(e for e in range(g['payloads'],g['payloads_at_hub']) if word['program'][e][0]=='MOVE')
 for name,event in [('omit_facet_arrival',firstmove),('omit_final_pivot_leg',firstmove+2)]:
  trial(name,dict(word,program=[o.copy() for e,o in enumerate(word['program']) if e!=event]))
 ops=[o.copy() for o in word['program']];clear=next(e for e in range(g['payloads'],firstmove) if ops[e][:2]==['CLEAR',1949]);op=ops.pop(clear);ops.insert(g['snapshots']+6,op);trial('premature_snapshot_retirement',dict(word,program=ops))
 charts=[dict(c) for c in word['additional_charts']];charts[0]['frame']=charts[0]['frame'][1:];trial('missing_acquisition_chart_direction',dict(word,additional_charts=charts))
 return rejected

def main(a):
 base=a.repo/'research/moonshot-005-program/results';parentdir=base/'eight-packet-seven-corrections-fused'
 source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,SOURCE_PIN)
 parent=load(parentdir/'WORD.json.gz',True,PARENT_PIN,PARENT_PAYLOAD);word=load(a.package/'WORD.json.gz',True,payload=WORD_PAYLOAD);report=load(a.package/'RESULT.json')
 prior=load(parentdir/'review/REVIEW-RESULT.json',pin='a0ad37e09f691e57128d0eda773aaeb3bea62a757759c7cba0059686cae9ea6e')
 require(prior['all1480_common_outputs_preserved'] and prior['private_inverse_rows_preserved']==400 and prior['all_other4985_residual_coefficients_preserved'],'authenticated independent parent facts')
 geom=derive(source);expected,lineage,groups,reads=reconstruct(source,parent,geom)
 require(word['program']==expected and word['parent_event_of_output']==lineage,'complete literal76277 word and every parent instruction independently reconstructed')
 require(len(expected)==76277 and word['initial']==parent['initial'] and word['public']==1880 and word['owned_fields']==73,'complete public/owned namespace')
 for i,g in enumerate(groups):
  got=word['cohort_collection']['groups'][i]
  for key,val in g.items():
   if key in ('matrix','pivot_minor','inverse_minor'):val=[[str(x) for x in row] for row in val]
   require(got[key]==val,'source-derived group metadata '+key)
  add=word['additional_charts'][i];require(add['index']==1095+i and space(add['frame'])==space(geom['groups'][i]['intersection_basis']),'exact added group chart')
 positions={e:i for i,e in enumerate(lineage) if e is not None}
 require(word['native_event_to_physical']==[positions[e] for e in parent['native_event_to_physical']],'all71261 actual source events correctly mapped')
 for key,e in parent['marks'].items():require(word['marks'][key]==positions[e],'inherited exact boundary '+key)
 require(word['marks']['all_active_donors_restored']==2018,'restoration metadata')
 bill=typed(source,word);before=typed(source,parent)
 require(bill['final']==before['final'] and bill['peak']==43,'all final charts and real peak occupancy')
 require(bill['counts']=={'ADD':65243,'SCALE':3670,'MOVE':6877,'INIT':243,'CLEAR':243,'COPY':1},'all real operations counted')
 raw_expected={1:61,2:58,3:40,5:97,6:1,7:4,8:298}
 require(bill['rawranks']==raw_expected and sum(bill['rawranks'].values())==559,'all559 raw MOVEs');require(sum(r*n for r,n in bill['rawranks'].items())==3200,'raw rank mass')
 sem=semantic(source,parent,word,groups,lineage,reads);inverse_check=private_inverse(source,parent,word);negative=mutants(source,parent,word,groups,lineage,reads)
 raw={int(k):v for k,v in word['private_role_map'].items()};logical=set(raw);oldraw=Counter(abs(len(source['frames'][o[2]])-len(source['frames'][o[3]])) for o in source['program'] if o[0]=='MOVE' and o[1] in logical)
 require(sum(oldraw.values())==1710 and oldraw=={1:990,2:360,3:105,4:112,5:133,6:8,7:2},'original raw profile independently from literal source')
 native=Counter(abs(len(source['frames'][o[2]])-len(source['frames'][o[3]])) for o in source['program'] if o[0]=='MOVE')
 extra=bill['ranks'].copy();extra.subtract(native);extra.subtract(bill['rawranks']);require({r:n for r,n in extra.items() if n}=={9:8},'all eight paid rank9 packets retained exactly once')
 inv=load(parentdir/'INPUT-INVOICE.json',pin=INVOICE_PIN);T={int(k):v for k,v in inv['T4'].items()};P={int(k):v for k,v in inv['P4'].items()};newP={r:P.get(r,0)+18*(bill['rawranks'][r]-oldraw[r])+18*(8 if r==9 else 0) for r in P.keys()|oldraw.keys()|bill['rawranks'].keys()|{9}}
 require(all(n>=0 for n in newP.values()) and sum(newP.values())==131850 and sum(T.values())==27344,'complete nonnegative paid/target histograms')
 require(sum(r*(T.get(r,0)-newP.get(r,0)) for r in T.keys()|newP.keys())==3760,'complete rank surplus')
 require(newP=={int(k):v for k,v in report['conditional_caller']['P_partial'].items()},'author complete caller independently matched')
 margin=tuple(x/18 for x in moment({r:T.get(r,0)-newP.get(r,0) for r in T.keys()|newP.keys()}))
 require(F(report['conditional_caller']['remaining_moment_per_native_lower'])<=margin[0]<=margin[1]<=F(report['conditional_caller']['remaining_moment_per_native_upper']),'independent directed exact native-margin bracket')
 require(F(4391,100)<margin[0]<margin[1]<F(43911,1000),'strict43.910.. target margin')
 # The selected ordinary receivers had none of the prior seven corrections.
 require(set(parent['corrections']).isdisjoint(map(str,[x+112 for x in FRAME])),'no old corrections double counted')
 require(len(sem['difference_rows'])==8 and report['remaining_residual_terms']==4985-8*48==4601,'exact384 new coefficient cancellations and remaining4601')
 maps=load(a.package/'CHART-MAPS.json');oldmaps={(o[2],o[3]) for o in parent['program'] if o[0]=='MOVE'};newmaps={(o[2],o[3]) for o in expected if o[0]=='MOVE'};introduced=newmaps-oldmaps
 require({(r['source'],r['target']) for r in maps['recipes']}==introduced and len(introduced)==164,'all164 actual introduced maps covered')
 frames=source['frames']+[x['frame'] for x in word['additional_charts']]
 for r in maps['recipes']:require(r['recipe']['rank']==len(frames[r['target']])-len(frames[r['source']]),'all introduced map ranks')
 require(maps['word_sha256']==sha((a.package/'WORD.json.gz').read_bytes()) and maps['parent_sha256']==PARENT_PIN and maps['source_sha256']==SOURCE_PIN and maps['wrong_global_phase_rejected'],'actual recipe input pins and phase control')
 for name,pin in maps['engine_pins'].items():require(sha((a.repo/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'retained exact engine '+name)
 result=dict(status='PASS_INDEPENDENT_EIGHT_COHORT_RECONSTRUCTION',source_sha256=SOURCE_PIN,parent_sha256=PARENT_PIN,parent_payload_sha256=PARENT_PAYLOAD,word_payload_sha256=WORD_PAYLOAD,word_sha256=sha((a.package/'WORD.json.gz').read_bytes()),independent_checker_sha256=sha(Path(__file__).read_bytes()),groups=14,actual_pivot_minors=14,raw_calls=559,raw_rank_mass=3200,counts=dict(bill['counts']),owned_peak=43,owned_lifetimes=243,semantics=sem,remaining_residual_coefficients=4601,completed_first_pairs=8,all1480_common_outputs_preserved=True,all1880_input_directions_retained=True,private_inverse_rows=400,conditional_paid_profile=newP,conditional_target_profile=T,paid_positions=131850,target_positions=27344,rank_surplus=3760,remaining_moment_exact=[str(x) for x in margin],remaining_moment_approx=float(margin[0]),introduced_map_coverage=164,chart_engine_scope='Retained exact engines credited from authenticated author run; recipe coverage and rank independently checked here.',scope='New-provenance finite source construction: exact1880-column prefix, unchanged isolated suffix and authenticated parent imply all input/output claims. No uniform native, supplier, completed reverse family or new kappa.')
 result['private_inverse']=inverse_check;result['negative_controls']=negative
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('semantics','conditional_paid_profile','conditional_target_profile')},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
