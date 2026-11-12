#!/usr/bin/env python3
"""Complete all first-pair duties with direct raw routes; hosted96 remain open."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
def need(v,m):
 if not v:raise ValueError(m)
def axpy(a,b,c):
 for k,v in b.items():
  v=a.get(k,F(0))+c*v
  if v:a[k]=v
  else:a.pop(k,None)
def space(vs):
 a={0}
 for v in vs:a|={x^v for x in tuple(a)}
 return a
def endpoints(w):
 T={i:{i:F(1)} for i in range(1480)};L={r:{r:F(1)} for r in mains(w)}
 for k,x in enumerate(w['live']):
  y=x+112
  if k in w['hosted']['Dports']:T[y]={y:F(1),x:F(1)};L[y]=T[y].copy()
  else:
   T[x]={x:F(1),y:F(-1)};T[y]={x:F(1,2),y:F(1,2)};L[x]=T[x].copy();L[y]=T[y].copy()
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):T[x]={x:F(1),y:F(-1)}
 return T,L
def mains(w):return sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
def build(w):
 M=mains(w);need(len(M)==400,'400 independent private mains');q={r:1480+i for i,r in enumerate(M)};ops=[];marks={};routes=[];native=[];packets=[];tmp=1480+400+w['owned_fields']
 for r in M:ops.append(['ADD',q[r],r,'-1',w['initial'][r]])
 marks['differences']=len(ops)
 for r in M:
  routes.append({'physical_event':len(ops),'role':r,'source_events':[i for i,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]==r]})
  ops.append(['MOVE',q[r],w['initial'][r],w['final'][r],False])
 marks['raw_final']=len(ops)
 for e in w['program']:
  native.append(len(ops));x=e.copy();x[1]+=400 if x[1]>=1480 else 0
  if x[0] in ('ADD','COPY'):x[2]+=400 if x[2]>=1480 else 0
  ops.append(x)
 marks['common_finished']=len(ops)
 for k,x in enumerate(w['live']):
  y=x+112;at=w['final'][y];need(w['final'][x]==127 and len(w['frames'][at])==8,'first endpoint geometry');c='1' if k in w['hosted']['Dports'] else '1/2'
  start=len(ops);ops.extend([['INIT',tmp,127],['ADD',tmp,q[x],'1',127],['MOVE',tmp,127,at,True]])
  if c!='1':ops.append(['SCALE',q[y],c,at])
  ops.extend([['ADD',q[y],tmp,c,at],['CLEAR',tmp,at]])
  packets.append({'kind':'forward','x':x,'y':y,'start':start,'stop':len(ops)})
 marks['all_first_Y_correct']=len(ops)
 for k,x in enumerate(w['live']):
  if k in w['hosted']['Dports']:continue
  y=x+112;at=w['final'][y];start=len(ops)
  ops.extend([['INIT',tmp,at],['ADD',tmp,q[y],'1',at],['MOVE',tmp,at,127,True],['SCALE',q[x],'2',127],['ADD',q[x],tmp,'-2',127],['CLEAR',tmp,127]])
  packets.append({'kind':'coupled_reverse','x':x,'y':y,'start':start,'stop':len(ops)})
 marks['all_first_pairs_correct']=len(ops)
 for r in M:ops.append(['ADD',q[r],r,'1',w['final'][r]])
 return {'schema':'moonshot-complete-first-family-v1','source_sha256':PIN,'public':1880,'owned_fields':w['owned_fields']+1,'initial':w['initial']+[w['initial'][r] for r in M],'difference_role_map':q,'program':ops,'marks':marks,'raw_route_lineage':routes,'native_event_to_physical':native,'new_packets':packets,'scope':'All104 first-Y and8 coupled-X duties complete;96 hosted reverse duties open; no complete supplier.'},q

def replay(w,word,q,T,L):
 rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(word['initial']));spaces=list(map(space,w['frames']));counts=Counter();ranks=Counter();peak=life=0
 for t,e in enumerate(word['program']):
  op,r=e[:2];counts[op]+=1;need(0<=r<1880+word['owned_fields'],'declared role')
  if op=='INIT':need(r>=1880 and r not in loc,'fresh owned field');loc[r]=e[2];rows[r]={};life+=1
  elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'dirty owned retirement');del rows[r];del loc[r]
  elif op=='MOVE':
   a,b,owned=e[2:];need(loc.get(r)==a and owned==(r>=1880),'MOVE source and ownership')
   need(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'proper nested transport');ranks[abs(len(w['frames'][b])-len(w['frames'][a]))]+=1;loc[r]=b
  elif op=='SCALE':need(loc.get(r)==e[3] and F(e[2]),'cochart nonzero scale');rows[r]={i:F(e[2])*c for i,c in rows[r].items()}
  elif op in ('ADD','COPY'):
   s,c,at=e[2:];need(r!=s and loc.get(r)==loc.get(s)==at,'cochart arithmetic')
   if op=='COPY':need(not rows[r],'all-input COPY guard')
   axpy(rows[r],rows[s],F(c))
  else:raise ValueError(op)
  peak=max(peak,len(loc)-1880)
  if t+1==word['marks']['common_finished']:need(all(rows[i]==T[i] for i in range(1480)),'all1480 native outputs')
 need(set(rows)==set(range(1880)),'every owned lifetime closed')
 for i in range(1480):need(rows[i]==T[i] and loc[i]==w['final'][i],'all common outputs unchanged')
 for r,phys in q.items():
  expected=T[r].copy()
  for j,c in L[r].items():axpy(expected,{q[j]:F(1),j:F(-1)},c)
  need(rows[phys]==expected and loc[phys]==w['final'][r],'all400 exact private endpoint rows')
 # Explicit inverse of the complete400-dimensional private operator.
 for r in q:
  inv={r:F(1)}
  for k,x in enumerate(w['live']):
   y=x+112
   if r not in (x,y):continue
   if k in w['hosted']['Dports']:
    if r==y:inv={y:F(1),x:F(-1)}
   elif r==x:inv={x:F(1,2),y:F(1)}
   else:inv={y:F(1),x:F(-1,2)}
  check={}
  for j,c in inv.items():axpy(check,L[j],c)
  need(check=={r:F(1)},'exact400-row private inverse')
 return {'instructions':len(word['program']),'counts':dict(sorted(counts.items())),'MOVE_rank_histogram':dict(sorted(ranks.items())),'owned_lifetimes':life,'peak_owned':peak,'final_owned':0,'common_rows':1480,'private_rows':400,'private_inverse_rows':400}

def power(r):
 D=10**30;n=r**199*D**200;a,b=0,r*D+1
 while b-a>1:
  m=(a+b)//2
  if m**200<=n:a=m
  else:b=m
 need(a**200<=n<(a+1)**200,'integer200th root bracket')
 return F(a,D),F(a if a**200==n else a+1,D)
def interval(profile,powers):
 lo=hi=F(0)
 for r,c in profile.items():
  a,b=powers[r];lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
def invoice(w,q,word,source):
 old=Counter(abs(len(w['frames'][e[3]])-len(w['frames'][e[2]])) for e in w['program'] if e[0]=='MOVE' and e[1] in q);new=Counter({8:400});T={int(k):v for k,v in source['T4'].items()};P={int(k):v for k,v in source['P4'].items()};paid=P.copy()
 need(sum(old.values())==1710 and sum(r*c for r,c in old.items())==3200,'original raw profile')
 for r in old.keys()|new.keys():paid[r]=paid.get(r,0)+18*(new[r]-old[r])
 paid[1]+=18*112
 powers={r:power(r) for r in T.keys()|P.keys()|paid.keys()};saving=interval({r:old[r]-new[r] for r in old.keys()|new.keys()},powers);margin=tuple(v/18 for v in interval({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()},powers))
 need(margin[0]>6 and margin[1]<7,'six-new-field ceiling for this fixed paid profile')
 need(sum(paid.values())==130860 and sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys())==3040,'full caller counts')
 return {'old_raw_profile':dict(sorted(old.items())),'new_raw_profile':dict(new),'new_packet_profile':{1:112},'new_packet_duties':{'forward':104,'coupled_reverse':8},'saved_moment_bounds':list(map(str,saving)),'saved_moment_approximate':float(saving[0]),'T4':T,'paid_histogram':paid,'target_positions':sum(T.values()),'paid_positions':sum(paid.values()),'rank_surplus':3040,'remaining_moment_per_native_bounds':list(map(str,margin)),'remaining_moment_approximate':float(margin[0]),'strict_additional_positive_rank_field_ceiling':6,'remaining_hosted_duties':96,'scope':'Conditional full H4 caller profile only; physical ordinary/precision services and all supplier foundations remain. A field-count ceiling does not establish a96-call lower bound.'}
def main(a):
 b=a.source.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,'native source pin');w=json.loads(gzip.decompress(b));ib=a.invoice.read_bytes();need(hashlib.sha256(ib).hexdigest()==IPIN,'H4 invoice pin');I=json.loads(ib)
 word,q=build(w);T,L=endpoints(w);bill=replay(w,word,q,T,L);cost=invoice(w,q,word,I)
 need(len(word['new_packets'])==112 and Counter(p['kind'] for p in word['new_packets'])=={'forward':104,'coupled_reverse':8},'every required first packet once')
 need(bill['instructions']==73037 and bill['peak_owned']==43 and bill['counts']['MOVE']==6822,'complete emitted counts')
 badx=w['live'][next(i for i in range(104) if i not in w['hosted']['Dports'])];bady=badx+112
 negatives={'wrong_coupled_reverse_coefficient':{'x':badx,'y':bady,'residual_when_minus2_replaced_by_minus1':{str(badx):'1/2',str(bady):'1/2'}},'omitted_hosted_corrections':{'count':96,'first_x':w['hosted']['X2'][0],'missing_raw_y':w['hosted']['Y2'][0],'residual_coefficient':'1'},'forgotten_reverse_fees':{'omitted_calls':8,'spurious_margin_increase':8},'deleted_access':'No raw carrier has an intermediate chart visit; adding a decoder there is not authorized by this word.'}
 result={'status':'PASS_ALL104_FIRST_Y_AND8_COUPLED_X_WITH_EXACT_PARTIAL_INVOICE','source_sha256':PIN,'invoice_sha256':IPIN,'full_input_directions':1880,'word':bill,'completed_first_Y':104,'completed_coupled_X':8,'completed_first_pairs':104,'remaining_hosted_reverse':96,'cost':cost,'negative_controls':negatives,'classification':'Exact finite source construction and conditional profile reduction; no complete shared native or new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);payload=json.dumps(word,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(payload,mtime=0);(a.output/'WORD.json.gz').write_bytes(compressed);result['word_payload_sha256']=hashlib.sha256(payload).hexdigest();result['word_compressed_sha256']=hashlib.sha256(compressed).hexdigest();(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--invoice',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
