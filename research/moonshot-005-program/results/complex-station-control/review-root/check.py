#!/usr/bin/env python3
"""Independent dense adjoints and formal-arrival map; no author imports."""
import argparse,gzip,hashlib,json,importlib.util,math
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
def need(x,s):
 if not x:raise ValueError(s)
def read(p,h):
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==h,'pin '+str(p));return json.loads(gzip.decompress(b))
def rank(A):
 b={}
 for v in A:
  v=list(v)
  for p,r in sorted(b.items()):
   if v[p]:
    c,d=v[p],r[p];v=[d*x-c*y for x,y in zip(v,r)];g=math.gcd(*v)
    if g>1:v=[x//g for x in v]
  p=next((p for p,x in enumerate(v) if x),None)
  if p is not None:
   g=math.gcd(*v);b[p]=[x//g for x in v]
 return len(b)
def adjoints(ops,final_loc,final,den):
 loc=dict(final_loc);a={i:[int(i==208+j) for j in range(96)] for i in range(400)};dd=1;influence=set();states=0
 def inspect(i):
  nonlocal states
  if 304<=i<400:return
  states+=1
  if any(a[i]):influence.add(loc[i])
 def multiply_to(i,j,c,replace=False):
  nonlocal dd
  c=F(c);num,div=c.numerator,c.denominator
  if any((num*x)%div for x in a[j]):
   dd*=div
   for r in a:a[r]=[x*div for x in a[r]]
  z=[num*x//div for x in a[j]];a[i]=z if replace else [x+y for x,y in zip(a[i],z)]
 for i in loc:inspect(i)
 for e in reversed(ops):
  op,i=e[:2]
  if op=='ADD':multiply_to(e[2],i,e[3]);inspect(e[2])
  elif op=='SCALE':multiply_to(i,i,e[2],True);inspect(i)
  elif op=='MOVE':loc[i]=e[2];inspect(i)
  elif op=='CLEAR':loc[i]=e[2];a[i]=[0]*96;inspect(i)
  elif op=='INIT':del loc[i];del a[i]
  else:raise ValueError(op)
 for i in range(400):need(all(a[i][j]*den==final[208+j][i]*dd for j in range(96)),'dense adjoint/forward identity')
 return influence,states,loc
def hub_formal(word,ops):
 loc=dict(enumerate(word['initial']));rows={};dd=1;arrivals=[];departures=[]
 need(all(c!=127 for c in loc.values()),'no initial Hub field')
 for t,e in enumerate(ops):
  op,i=e[:2]
  if op=='MOVE':
   if e[2]==127:need(i>=400,'public Hub departure');departures.append([t,i,e[3]]);del rows[i]
   if e[3]==127:
    need(i<400,'owned Hub arrival');j=len(arrivals);need(j<200,'arrival count');rows[i]=[dd*int(k==j) for k in range(200)];arrivals.append([t,i,e[2]])
   loc[i]=e[3]
  elif op=='INIT':
   loc[i]=e[2]
   if e[2]==127:rows[i]=[0]*200
  elif op=='CLEAR':
   if e[2]==127:del rows[i]
   del loc[i]
  elif op in ('ADD','SCALE') and loc[i]==127:
   j=e[2] if op=='ADD' else i;c=F(e[3] if op=='ADD' else e[2]);num,div=c.numerator,c.denominator
   if any((num*x)%div for x in rows[j]):
    dd*=div
    for r in rows:rows[r]=[x*div for x in rows[r]]
   z=[num*x//div for x in rows[j]];rows[i]=z if op=='SCALE' else [x+y for x,y in zip(rows[i],z)]
 need(set(rows)==set(range(104))|set(range(208,304)),'final Hub roles');need(len(arrivals)==200,'200 arrivals');need(rank(rows.values())==200,'formal Hub map invertible')
 return rows,dd,arrivals,departures
def main(a):
 need(hashlib.sha256(a.engine.read_bytes()).hexdigest()=='c4389c80322c875c4739af6ee558619f01da6112682c565e4f638a01750e5ec1','independent dense engine pin')
 spec=importlib.util.spec_from_file_location('dense_engine',a.engine);eng=importlib.util.module_from_spec(spec);spec.loader.exec_module(eng)
 n=read(a.native,'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883');p=read(a.parent,'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc');f=read(a.four,'20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f')
 results={}
 for variant,w in [('parent',p),('four',f)]:
  w=dict(w);w['program']=p['program'][:p['consumer']['begin']] if variant=='parent' else [o for o,t in zip(f['program'],f['parent_event_of_output']) if t is None or t<p['consumer']['begin']]
  ops=w['program'];final,den,loc,bill,_=eng.run(w,list(map(eng.span,w['frames'])))
  stations={d:{w['initial'][d]} for d in range(304,400)}
  for o in ops:
   if 304<=o[1]<400:
    need(o[0]=='MOVE','original D never modified');stations[o[1]].add(o[3])
  need(all(127 not in v for v in stations.values()),'no original D Hub station')
  influence,states,start=adjoints(ops,loc,final,den);need(start==dict(enumerate(w['initial'])),'reverse topology')
  protected=sorted(d for d in stations if not stations[d]&influence);need(len(protected)==(74 if variant=='parent' else 66),'protected count')
  roles={int(k):v for k,v in p['source_role_map'].items()};host=sorted((n['live'][i],roles[b],roles[d]) for i,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2']));bd={d:b for _,b,d in host}
  need(set(bd)==set(stations) and set(bd.values())==set(range(208,304)),'native hosted roles')
  need(all(final[b][d]==0 for d in protected for b in bd.values()),'protected B columns identically zero')
  nuisance=list(range(104))+list(range(208,304));need(rank([[final[i][j] for j in nuisance] for i in nuisance])==200,'actual nuisance block invertible')
  H,hd,arr,dep=hub_formal(w,ops)
  cert=json.loads((a.bundle/('exact-'+variant)/'CERTIFICATE.json').read_text());auth=json.loads((a.bundle/('exact-'+variant)/'RESULT.json').read_text())
  need(auth['protected_D_roles']==protected and auth['B_influence_charts']==sorted(influence),'independent support agreement')
  need({int(d):set(cs) for d,cs in auth['original_D_station_charts'].items()}==stations,'independent station sets')
  for i,r in H.items():
   got={int(j):F(x) for j,x in cert['Hub_map'][str(i)].items()};need(all(F(x,hd)==got.get(j,0) for j,x in enumerate(r)),'independent dense formal map')
  need(auth['Hub_structural_certificate']['public_arrivals']==arr and auth['Hub_structural_certificate']['owned_departures']==dep,'arrival topology')
  controls={'deleting_a_protected_role_rejected':protected[:-1]!=auth['protected_D_roles'],'adding_Hub_to_a_protected_station_changes_support':not((stations[protected[0]]|{127})&influence==set()),'forcing_a_zero_Hub_row_lowers_rank':rank([v if i else [0]*200 for i,v in enumerate(H.values())])==199,'claiming_protected_B_coefficient_nonzero_rejected':final[bd[protected[0]]][protected[0]]==0}
  need(all(controls.values()),'negative controls')
  results[variant]=dict(protected_count=len(protected),protected_roles=protected,checked_adjoint_states=states,influence_chart_count=len(influence),formal_Hub_rank=200,actual_nuisance_rank=200,all400_forward_adjoint_columns_equal=True,identity_minor_size=len(protected),bill=bill,negative_controls=controls)
 out=dict(status='PASS_INDEPENDENT_ALL_TIME_SOURCE_CONTROL',engine_sha256=hashlib.sha256(a.engine.read_bytes()).hexdigest(),results=results,proof_scope='Retained old-source D-station insertions and capture/return messages only; no D recoding, changed unknown-input mixing or travelling distributors. Universal all-width proof separately reviewed.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'counts':{k:v['protected_count'] for k,v in results.items()}}))
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for k in ['native','parent','four','bundle','engine','output']:ap.add_argument('--'+k,type=Path,required=True)
 main(ap.parse_args())
