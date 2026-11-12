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
 base=a.repo/'research/moonshot-005-program/results';sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=base/'paired-cohort/output/WORD.json.gz';wp=a.package/'output/WORD.json.gz'
 need(sha(sp.read_bytes())=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');need(sha(gzip.decompress(pp.read_bytes()))=='bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a','parent pin')
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
 for x in U:
  y=x+112;need(new[raw[x]]=={raw[x]:Q(1),x:Q(-1),raw[y]:Q(-1),y:Q(1)},'exact coupled reverse')
 need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'unchanged suffix')
 _,oloc,oc,orr,oraw,opk=run(p,s,False);_,nloc,nc,nrr,nraw,npk=run(w,s,False);need(oloc==nloc and set(nloc)==set(range(1880)),'full final charts and retirement');need(oraw==nraw,'raw unchanged')
 delta={k:nc.get(k,0)-oc.get(k,0) for k in nc.keys()|oc.keys()};need({k:v for k,v in delta.items() if v}=={'ADD':16,'SCALE':-8,'MOVE':8,'INIT':8,'CLEAR':8},'complete ordinary delta')
 pr=json.loads((base/'paired-cohort/output/RESULT.json').read_text());rr=json.loads((a.package/'output/RESULT.json').read_text());T={int(k):v for k,v in pr['conditional_caller']['T4'].items()};P={int(k):v for k,v in pr['conditional_caller']['P_partial'].items()};P[1]+=144
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
 report={'status':'PASS_INDEPENDENT_COUPLED_PRETERMINAL_REVIEW','source_sha256':sha(sp.read_bytes()),'parent_payload_sha256':sha(gzip.decompress(pp.read_bytes())),'word_payload_sha256':sha(gzip.decompress(wp.read_bytes())),'author_generator_sha256':sha((a.package/'build_preterminal.py').read_bytes()),'instructions':len(w['program']),'all_input_columns':1880,'coupled_reverse_completed':8,'complete_ordinary_delta':delta,'peak_owned':npk,'owned_lifetimes':nc['INIT'],'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'moment_per_native_lower':str(lo/18),'moment_per_native_upper':str(hi/18),'negative_controls':negative,'scope':'Independent input-map proof and separate whole-word reconstruction, rational prefix, complete types, inverse and tariff. No supplier or kappa.'}
 a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
