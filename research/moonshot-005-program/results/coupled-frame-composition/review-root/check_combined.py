#!/usr/bin/env python3
"""Independent reconstruction of the source preconditioner; no author imports."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(gzip.decompress(p.read_bytes()))
def add(a,b,c):
 r=dict(a)
 for k,v in b.items():
  t=r.get(k,Q(0))+c*v
  if t:r[k]=t
  else:r.pop(k,None)
 return r
def space(vs):
 s={0}
 for v in vs:s.update([w^v for w in tuple(s)])
 return s

def run(w,s,linear=True):
 frames=s['frames']+[x['frame'] for x in w['additional_charts']];spaces=list(map(space,frames));loc=dict(enumerate(w['initial']));rows={i:{i:Q(1)} for i in range(1880)};cnt=Counter();ranks=Counter();rawrank=Counter();raw=set(w['private_role_map'].values());peak=0
 stop=w['marks']['common_starts'] if linear else len(w['program'])
 for t,o in enumerate(w['program'][:stop]):
  k,d=o[:2];cnt[k]+=1;need(0<=d<1880+w['owned_fields'],'role bound')
  if k=='INIT':
   need(d>=1880 and d not in loc,'fresh owned');loc[d]=o[2]
   if linear:rows[d]={}
  elif k=='CLEAR':
   need(d>=1880 and loc.get(d)==o[2],'owned retirement');del loc[d]
   if linear:del rows[d]
  elif k=='MOVE':
   a,b,own=o[2:];need(loc.get(d)==a and type(own)is bool and own==(d>=1880),'route binding');need(spaces[a]<spaces[b] or own and spaces[b]<spaces[a],'nesting');loc[d]=b;rank=abs(len(frames[a])-len(frames[b]));ranks[rank]+=1
   if d in raw:rawrank[rank]+=1
  elif k=='SCALE':
   need(Q(o[2]) and loc.get(d)==o[3],'scale');
   if linear:rows[d]={i:Q(o[2])*v for i,v in rows[d].items()}
  elif k in ('ADD','COPY'):
   r,c,at=o[2:];need(r!=d and loc.get(r)==loc.get(d)==at,'read '+str(t))
   if linear:need(k!='COPY' or not rows[d],'zero COPY');rows[d]=add(rows[d],rows[r],Q(c))
  else:raise ValueError(k)
  peak=max(peak,len(loc)-1880)
 return rows,loc,dict(cnt),dict(ranks),dict(rawrank),peak

def bound(r,D=10**18):
 target=r**199*D**200;l=0;h=r*D+1
 while l+1<h:
  m=(l+h)//2
  if m**200<=target:l=m
  else:h=m
 need(l**200<=target<(l+1)**200,'root bound');return Q(l,D),Q(l if l**200==target else l+1,D)

def main(a):
 base=a.repo/'research/moonshot-005-program/results';sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=base/'orthogonal-frame-feedback/output/WORD.json.gz';wp=a.package/'output/WORD.json.gz'
 need(sha(sp.read_bytes())=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');need(sha(gzip.decompress(pp.read_bytes()))=='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','parent pin')
 s,p,w=load(sp),load(pp),load(wp);raw={int(k):v for k,v in p['private_role_map'].items()};H={s['live'][k] for k in s['hosted']['Dports']};U=[x for x in s['live'] if x not in H];need(U==[17,19,30,38,40,47,52,60],'coupled set')
 drop=set();pre=[];sub={}
 for x in U:
  y=x+112;need(s['initial'][y]==3 and len(s['frames'][s['initial'][x]])==1,'source line')
  j,o=next((j,o) for j,o in enumerate(p['program'][400:],400) if o[1]==raw[y] or o[0] in ('ADD','COPY') and o[2]==raw[y]);need(o==['SCALE',raw[y],'1/2',3],'first-use half');drop.add(j)
  pre.extend([['INIT',1880,3],['ADD',1880,raw[y],'1',3],['MOVE',1880,3,s['initial'][x],True],['ADD',raw[x],1880,'-1',s['initial'][x]],['CLEAR',1880,s['initial'][x]]])
  sub[raw[x]]={raw[x]:Q(1),raw[y]:Q(-1),y:Q(1)};sub[raw[y]]={raw[y]:Q(2),y:Q(-1)}
 need(w['program']==p['program'][:400]+pre+[o for j,o in enumerate(p['program'][400:],400) if j not in drop],'independently rebuilt entire word')
 need(w['marks']['common_starts']==p['marks']['common_starts']+32,'common boundary');old,oloc,*_=run(p,s);new,nloc,*_=run(w,s);need(oloc==nloc,'same entry locations');prefixloc=nloc.copy()
 for r,row in old.items():
  want={}
  for j,c in row.items():want=add(want,sub.get(j,{j:Q(1)}),c)
  need(new[r]==want,'all1880 source directions '+str(r))
 need(all(new[r]==old[r] for r in range(1480)),'all1480 original common rows unchanged')
 for x in U:
  y=x+112;need(new[raw[x]]=={raw[x]:Q(1),x:Q(-1),raw[y]:Q(-1),y:Q(1)},'exact coupled reverse')
 need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'unchanged suffix')
 host={s['live'][i]:(x,y) for i,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
 order=list(host);matrix=[]
 for x in order:
  need(new[raw[host[x][0]]]==old[raw[host[x][0]]],'hosted reverse row literally preserved')
  need(new[raw[host[x][1]]]==old[raw[host[x][1]]],'hosted dual input literally preserved')
  matrix.append([Q(x==y)+new[raw[host[x][0]]].get(raw[host[y][1]],Q(0)) for y in order])
 piv=0
 for j in range(96):
  t=next((i for i in range(piv,96) if matrix[i][j]),None)
  if t is None:continue
  matrix[piv],matrix[t]=matrix[t],matrix[piv];v=matrix[piv][j];matrix[piv]=[a/v for a in matrix[piv]]
  for i in range(piv+1,96):
   if matrix[i][j]:v=matrix[i][j];matrix[i]=[a-v*b for a,b in zip(matrix[i],matrix[piv])]
  piv+=1
 need(piv==88,'fresh actual reverse residual rank')
 need(w['additional_charts']==p['additional_charts'],'all inherited charts identical')
 for y in p['newly_completed_firstY_receivers']:
  need(new[raw[y]]=={raw[y]:Q(1),y:Q(-1),raw[y-112]:Q(1),y-112:Q(-1)},'all completed forward receivers survive')
 eventmap={};event=0
 for j,o in enumerate(p['program']):
  if j==400:event+=40
  if j in drop:continue
  eventmap[j]=event;event+=1
 need(w['native_event_to_physical']==[eventmap[j] for j in p['native_event_to_physical']],'native event lineage')
 cm=json.loads((a.package/'output/CHART-MAPS.json').read_text());prior=json.loads((base/'preterminal-coupled-eight/output/CHART-MAPS.json').read_text())
 need(cm['maps']==prior['maps'] and cm['engine_pins']==prior['engine_pins'],'eight exact new chart maps identical')
 need(len(w['program'])==78155,'actual combined operation count')
 def r9(h):
  v=s['frames'][s['initial'][h]][0];bits=[i for i in range(9) if v>>i&1]
  if len(bits)==3:return [Q(2 if i in bits else -1) for i in range(9)]
  need(len(bits)==7,'source root');i,j=[k for k in range(9) if k not in bits];return [Q(3*(int(k==i)-int(k==j))) for k in range(9)]
 rt={h:r9(h) for h in s['live']};residual={}
 for h in s['live']:
  c=Q(1,2) if h in U else Q(1);rr={k:c*(sum(x*y for x,y in zip(rt[h],rt[k]))/18-int(h==k)) for k in s['live']}
  for k,v in p['corrections'].get(str(h+112),[]):rr[k]+=Q(v)
  residual[h]={k:v for k,v in rr.items() if v}
 changed_count=sum(len(v) for v in residual.values());expanded_count=changed_count+sum(sum(k in U for k in row) for row in residual.values())
 need((changed_count,expanded_count)==(4569,4920),'exact residual counts in both input bases')


 _,oloc,oc,orr,oraw,opk=run(p,s,False);_,nloc,nc,nrr,nraw,npk=run(w,s,False);need(oloc==nloc and set(nloc)==set(range(1880)),'full final charts and retirement');need(oraw==nraw,'raw unchanged')
 delta={k:nc.get(k,0)-oc.get(k,0) for k in nc.keys()|oc.keys()};need({k:v for k,v in delta.items() if v}=={'ADD':16,'SCALE':-8,'MOVE':8,'INIT':8,'CLEAR':8},'complete ordinary delta')
 pr=json.loads((base/'orthogonal-frame-feedback/output/RESULT.json').read_text());rr=json.loads((a.package/'output/RESULT.json').read_text());T={int(k):v for k,v in pr['conditional_caller']['T4'].items()};P={int(k):v for k,v in pr['conditional_caller']['P_partial'].items()};P[1]+=144
 need(rr['conditional_caller']['P_partial']=={str(k):v for k,v in P.items()},'complete paid profile');lo=hi=Q(0)
 for r in T.keys()|P.keys():
  c=T.get(r,0)-P.get(r,0);l,h=bound(r);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 need(lo/18<=Q(rr['conditional_caller']['remaining_moment_per_native_lower'])<=Q(rr['conditional_caller']['remaining_moment_per_native_upper'])<=hi/18,'fresh integer price enclosure')
 negative={}
 for name,event,value in [('wrong_sign',403,'1'),('wrong_line',402,s['initial'][19]),('retained_half',None,None)]:
  bad=json.loads(json.dumps(w))
  if event is None:bad['program'].insert(440,['SCALE',raw[U[0]+112],'1/2',3]);bad['marks']['common_starts']+=1
  else:bad['program'][event][3]=value
  try:
   br,bl,*_=run(bad,s);need(br==new and bl==prefixloc,'wrong precomposition')
  except ValueError:negative[name]=True
  else:raise ValueError('mutant survived '+name)
 report={'status':'PASS_INDEPENDENT_COMBINED_RANK88_PRETERMINAL_REVIEW','source_sha256':sha(sp.read_bytes()),'parent_payload_sha256':sha(gzip.decompress(pp.read_bytes())),'word_payload_sha256':sha(gzip.decompress(wp.read_bytes())),'author_generator_sha256':sha((a.package/'build_combined.py').read_bytes()),'instructions':len(w['program']),'all_input_columns':1880,'coupled_reverse_completed':8,'actual_hosted_reverse_rank':piv,'all1480_common_prefix_rows_unchanged':True,'residual_coefficients_changed_basis':changed_count,'residual_coefficients_original_basis':expanded_count,'completed_forward_receivers_preserved':len(p['newly_completed_firstY_receivers']),'inherited_chart_maps_identical':True,'complete_ordinary_delta':delta,'peak_owned':npk,'owned_lifetimes':nc['INIT'],'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'moment_per_native_lower':str(lo/18),'moment_per_native_upper':str(hi/18),'negative_controls':negative,'scope':'Independent input-map proof and whole78155-word reconstruction; fresh rank88 elimination; all1880 columns, coupled and previous forward outputs, full types, native clocks, chart-map reuse and tariff. No new supplier or kappa.'}
 a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
