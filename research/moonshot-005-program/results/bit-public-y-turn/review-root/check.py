#!/usr/bin/env python3
"""Independent native matrix, all-route replay, actual cut and cost review.
Imports only root's previously published all-route engine; no producer code.
"""
import argparse, copy, hashlib, importlib.util, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PINS={'gauge':{'PARTIAL-WORD.json.gz':'2821160a7f62985e86e52ad022722502b84e535b3f79074b21cb769dac059ae1','CLOSED-WORD.json.gz':'8da6974eedf7637381b2190c12bca1b68051214951bff73df59eb192685db89b'},'canonical':{'PARTIAL-WORD.json.gz':'9198bb8e7ecbb5f1a47393cfb2340f79a2e0e3038c660bb81700ec57024db65c','CLOSED-WORD.json.gz':'24647446fa276637768abeedc89ba0f5c047231c00435fc681183e325925e833'}}
DONE=[92,36,54,38,55,23,110,41,61]
def main(a):
 spec=importlib.util.spec_from_file_location('root_all_route_engine',a.engine);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e);need=e.need
 need(e.digest(a.native)=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
 n=e.read(a.native);roots=[tuple(map(F,n['frames'][str(c)]['B'][0]))for c in n['start'][:111]]
 K=[sum(1<<j for j,u in enumerate(roots)if i==j or sum(x*y for x,y in zip(v,u))==0)for i,v in enumerate(roots)]
 G=[K[i]for i in [0,1,2,4,8,9,14,30,59]];co={e.linear(m,G):m for m in range(512)};need(len(co)==512 and e.rank(K)==9,'canonical9')
 groups={}
 for i,v in enumerate(roots[8:],8):groups.setdefault((tuple(j for j,x in enumerate(v)if x),sum(x<0 for x in v)%2),[]).append(i)
 piv=[10,11,20,21,28,24,36,37,38,39,50,49,55,54,59,65,67,70,79,74,81,84,88,92,101,97,108,107]
 need(len(groups)==28 and all(p in g for p,g in zip(piv,groups.values())),'pinned gauge pivots')
 E=[]
 for row in K:
  z=row&~255
  for p,g in zip(piv,groups.values()):
   if row>>p&1:z^=sum(1<<j for j in g)
  E.append(z)
 need(e.rank(E)==3,'native gauge core rank3')
 receipts={};controls=[];profile_expected={1:26,2:3,3:2,4:2,5:3,6:8,7:209,8:3}
 def coalesce(w,re):
  active={};prof=Counter();own=Counter();pub=Counter()
  def close(i):
   if i not in active:return
   start,end=active.pop(i);q=abs(end-start);need(q>0,'positive call');prof[q]+=1
   if i>=222:own[q]+=1
   elif end<start:pub[q]+=1
  for ev in re['events']:
   i=ev['i']
   if ev['op']=='MOVE':
    b,d=len(ev['C']),len(ev['Cnext']);need(b!=d,'strict movement')
    if i in active:
     s,t=active[i];need(t==b,'continuous physical path')
     if (t-s)*(d-b)>0:active[i]=(s,d)
     else:close(i);active[i]=(b,d)
    else:active[i]=(b,d)
   else:
    close(i)
    if ev['op']=='ADD':close(ev['j'])
  for i in list(active):close(i)
  return dict(prof),dict(own),dict(pub)
 for name in ['gauge','canonical']:
  B=[E[i]for i in [8,14,30]]if name=='gauge'else G[:3]
  R=E if name=='gauge'else[e.linear(co[row]&7,B)for row in K]
  public={i:1<<i for i in range(222)}
  for i,row in enumerate(R):public[111+i]^=(1<<i)if i in DONE else row
  owned={222+i:1<<i for i in range(111)}|{336+i:row for i,row in enumerate(B)}|{341:(1<<23)^(1<<110),342:(1<<41)^(1<<61)}
  def expected(w,re,closed):
   need(re['val']==(public if closed else public|owned),'all222 public and116 retained rows')
   counts={'INIT':121,'ADD':463 if name=='gauge' else 514,'MOVE':1596 if closed else 882,'CLEAR':121 if closed else 5}
   need(dict(re['counts'])==counts and re['peak']==118,'counts and peak')
   need(all(re['loc'][i]==n['final'][i]for i in range(111)),'all X pure at Hub')
   if closed:need(w['final']==n['final'][:222] and len(re['loc'])==222,'closed physical endpoints')
   else:
    need(all(re['loc'][111+i]==(n['final'][111+i]if i in DONE else n['start'][111+i])for i in range(111)),'nine correct and102 unfinished locations')
    need(all(re['loc'][222+i]==n['start'][i]for i in range(111))and all(re['loc'][336+i]==0 for i in range(3)),'actual point/core positions')
    for record,ij in [(341,[23,110]),(342,[41,61])]:need(re['frames'][re['loc'][record]]==e.rref([roots[i]for i in ij]),'actual rank2 pair-bank chart')
   down=[ev for ev in re['events']if ev['op']=='MOVE'and ev['delta']<0 and not ev['owned']]
   need(len(down)==1 and down[0]['i']==149 and down[0]['delta']==-1,'unique paid public turn')
   need(all(ev['delta']<0 for ev in re['events']if ev['op']=='MOVE'and ev['owned']),'owned paths downward')
  results={};words={};replays={}
  for fn,pin in PINS[name].items():
   p=a.author/name/fn;need(e.digest(p)==pin,'exact frozen word');w=e.read(p);re=e.replay(w,n);closed=fn.startswith('CLOSED');expected(w,re,closed)
   norm,hist=e.normalize(w,n,re);need(norm['historical_x_rank']==12,'three core and nine coordinate histories')
   need(e.rank([v&((1<<111)-1)for v in hist]+B+[1<<i for i in DONE])==12,'actual history span equality')
   need(norm['public_downward_moves']==1 and norm['owned_moves']==40,'actual uncoalesced occurrence counts')
   prof,own,pub=coalesce(w,re)
   if closed:need(prof==profile_expected and pub=={1:1} and sum(q*c for q,c in own.items())==40,'independent actual coalescence')
   results[fn]={'counts':dict(re['counts']),'peak':re['peak'],'owned_live':len(re['loc'])-222,'normalization':norm,'coalesced_profile':prof,'owned_coalesced_profile':own,'public_downward_profile':pub}
   words[fn]=w;replays[fn]=re
  w=words['PARTIAL-WORD.json.gz'];re=replays['PARTIAL-WORD.json.gz'];S=[8,9,14,15,30,31,59]if name=='gauge'else[4,8,9,14,30,73]
  facets=[e.rref(n['frames'][str(n['final'][111+i])]['B'])for i in S]
  obs=[row for i,row in re['val'].items()if any(e.contained(re['frames'][re['loc'][i]],f)for f in facets)]
  tar=[(1<<i)^(1<<(111+i))for i in S];before=e.rank(obs);after=e.rank(obs+tar);need((before,after)==(207,213),'literal residual deficit6')
  need(e.rank(obs+[1<<i for i in range(111,222)]+tar)-e.rank(obs+[1<<i for i in range(111,222)])==6,'even all nuisance Y granted')
  predicates=[('public_down',lambda o:o[0]=='MOVE'and o[1]==149 and len(re['frames'][o[3]])<len(re['frames'][o[2]])),('feedback_first',lambda o:o[:3]==['ADD',149,339]),('feedback_completion',lambda o:o[:3]==['ADD',149,340]),('feedback_restore_packet',lambda o:o[:3]==['ADD',340,149]),('bank_copy',lambda o:o[0]=='ADD'and o[1]==341),('bank_refill',lambda o:o[:3]==['ADD',339,341]),('second_bank_refill',lambda o:o[:3]==['ADD',340,342]),('point_copy',lambda o:o[:3]==['ADD',230,8]),('core_cache',lambda o:o[:3]==['ADD',336,333]),('core_encoder',lambda o:o[0]=='ADD'and o[1]==333)]
  for label,predicate in predicates:
   z=copy.deepcopy(w);idx=next(k for k,o in enumerate(z['program'])if predicate(o));del z['program'][idx]
   try:expected(z,e.replay(z,n),False)
   except (ValueError,KeyError):controls.append(name+':'+label)
   else:raise ValueError('mutant accepted '+name+':'+label)
  receipts[name]={'words':results,'residual_cut':{'receivers':S,'inside_rank':before,'target_augmented_rank':after,'deficit':6,'all_Y_granted_deficit':6}}
 # Independent exact rational 200th-root enclosure, not Decimal transcendental arithmetic.
 grid=1<<176;lo=hi=F(0)
 for k,v in profile_expected.items():
  z=k**199*grid**200;l,h=0,k*grid+1
  while h-l>1:
   m=(l+h)//2
   if m**200<=z:l=m
   else:h=m
  need(l**200<=z<h**200,'outward algebraic root');lo+=v*F(l,grid);hi+=v*F(h,grid)
 for name in receipts:
  au=json.loads((a.author/name/'BUDGET.json').read_text())['moment'];need(F(au['lower_rational'])<=lo<=hi<=F(au['upper_rational']),'tighter independent moment bounds')
 out={'status':'PASS_INDEPENDENT_PUBLIC_Y_TURN_NINE_TARGET_SOURCE','native_sha256':e.digest(a.native),'engine_sha256':e.digest(a.engine),'proof_sha256':e.digest(a.author/'PROOF.md'),'word_pins':PINS,'receipts':receipts,'negative_controls':controls,'moment':{'grid':'2^-176','lower':str(lo),'upper':str(hi)},'scope':'Independent replay of all222 original columns,116 actual retained fields, real rational geometry and every paid public/owned occurrence, explicit six-channel residual cut, actual coalesced invoice. Producer code is neither executed nor imported. Scalar source tensors with identity for all characteristic-two fields and widths; no complete decoder.','new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'controls':len(controls),'history_x_rank':12,'remaining_cut_deficit':6,'moment':float(lo)}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in['native','author','engine','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
