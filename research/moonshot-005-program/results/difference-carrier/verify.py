#!/usr/bin/env python3
"""Symbolic verification of illustrative typed words, not a new native."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def add(a,b,c):
 z=a.copy()
 for i,v in b.items():
  t=z.get(i,F(0))+c*v
  if t:z[i]=t
  else:z.pop(i,None)
 return z
def show(a):return {str(i):str(v) for i,v in sorted(a.items())}
def replay(P,initial,pub,owned=0):
 rows={i:{i:F(1)} for i in range(pub)};chart=dict(enumerate(initial));bill=collections.Counter();peak=life=0
 for e in P:
  tag,j=e[:2];need(0<=j<pub+owned,'declared field');bill[tag]+=1
  if tag=='INIT':need(j>=pub and j not in chart,'fresh owned INIT');chart[j]=e[2];rows[j]={};life+=1
  elif tag=='CLEAR':need(j>=pub and chart.get(j)==e[2],'owned CLEAR');chart.pop(j);rows.pop(j)
  elif tag=='MOVE':
   a,b,o=e[2:];need(chart.get(j)==a and type(o)is bool and o==(j>=pub),'typed MOVE');need(a<b or o and b<a,'proper nested toy MOVE');chart[j]=b
  elif tag in ('ADD','COPY'):
   s,c,f=e[2:];need(j!=s and chart.get(j)==chart.get(s)==f,'live cochart arithmetic');need(F(c)!=0,'nonzero scalar')
   if tag=='COPY':need(not rows[j],'zero COPY destination')
   rows[j]=add(rows[j],rows[s],F(c))
  else:raise ValueError('unknown instruction')
  peak=max(peak,len(chart)-pub)
 return rows,chart,{'instructions':len(P),'counts':dict(sorted(bill.items())),'declared_owned':owned,'owned_lifetimes':life,'peak_owned':peak,'final_owned':len(chart)-pub}
def stationary_word():
 return [['ADD',3,0,'-1',0],['ADD',0,3,'1',0],['MOVE',3,0,1,False],['INIT',5,1],['ADD',5,3,'1',1],['MOVE',3,1,2,False],['MOVE',0,0,1,False],['ADD',4,0,'1',1],['ADD',2,0,'1',1],['ADD',2,5,'-1',1],['CLEAR',5,1],['MOVE',0,1,2,False],['MOVE',1,0,1,False],['MOVE',1,1,2,False],['ADD',0,3,'-1',2],['ADD',3,0,'1',2]]
def gamma_zero_word():
 return [['INIT',5,0],['ADD',5,0,'1',0],['ADD',3,0,'-1',0],['ADD',0,3,'1',0],['MOVE',0,0,1,False],['ADD',4,0,'1',1],['MOVE',1,0,1,False],['MOVE',3,0,1,False],['MOVE',5,0,1,True],['ADD',0,5,'1',1],['ADD',5,0,'-1',1],['ADD',0,5,'1',1],['CLEAR',5,1],['ADD',3,0,'1',1]]
def itinerant_owned_word():
 # H0,Y1,X2,Q3,R4,source-ownedP5. Charts0<1<2.
 return [['INIT',5,0],['ADD',5,0,'1',0],['MOVE',5,0,2,True],['ADD',3,0,'-1',0],['ADD',0,3,'1',0],['MOVE',3,0,2,False],['ADD',5,3,'1',2],['MOVE',0,0,1,False],['ADD',4,0,'1',1],['ADD',1,0,'1',1],['MOVE',0,1,2,False],['MOVE',5,2,1,True],['ADD',1,5,'-1',1],['CLEAR',5,1],['MOVE',2,0,2,False],['ADD',0,3,'-1',2],['ADD',3,0,'1',2]]
def two_loan_word(reverse=True):
 P=[['ADD',2,0,'-1',0],['ADD',0,2,'1',0],['ADD',4,0,'1',0],['ADD',1,0,'2',0],['ADD',3,1,'-1',0],['ADD',1,3,'1',0],['ADD',5,1,'1',0],['ADD',0,2,'-1',0],['ADD',1,2,'-2',0],['ADD',1,3,'-1',0]]
 r1=[['ADD',2,0,'1',0]];r2=[['ADD',3,1,'1',0],['ADD',3,2,'2',0]]
 return P+(r2+r1 if reverse else r1+r2)
def run(source,packet,write):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));M=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 meta={'source_sha256':PIN,'native_instructions':len(w['program']),'native_public':w['public'],'native_declared_owned':w['owned_fields'],'main_roles':len(M),'raw_main_reservations':sum(e[0]=='MOVE' and e[1] in M for e in w['program']),'COPY_events':[(k,e) for k,e in enumerate(w['program']) if e[0]=='COPY']}
 need(meta['native_instructions']==71261 and meta['raw_main_reservations']==1710,'baseline counts');need(meta['COPY_events']==[(31737,['COPY',1504,770,'1',115])],'COPY pin')
 S=stationary_word();sr,sc,sb=replay(S,[0,0,1,0,1],5,1);sw={0:{0:F(1)},1:{1:F(1)},2:{2:F(1),0:F(1)},3:{3:F(1)},4:{4:F(1),3:F(1)}}
 need(sr==sw and sc=={0:2,1:2,2:1,3:2,4:1},'stationary full five-input endpoint/chart identity');need(sb['counts']=={'ADD':8,'CLEAR':1,'INIT':1,'MOVE':6},'stationary tariff')
 G=gamma_zero_word();gr,gc,gb=replay(G,[0,0,1,0,1],5,1);gw={0:{0:F(1)},1:{1:F(1)},2:{2:F(1)},3:{3:F(1)},4:{4:F(1),3:F(1)}};need(gr==gw,'gamma-zero five-input identity')
 h={0:F(1),5:F(1)};p={0:F(1)};h=add(h,p,F(1));p=add(p,h,F(-1));h=add(h,p,F(1));need(h=={0:F(1)} and p=={0:F(-1),5:F(-1)},'zero public suffix response with owned perturbation retirement')
 I=itinerant_owned_word();ir,ic,ib=replay(I,[0,1,0,0,1],5,1);iw={0:{0:F(1)},1:{1:F(1)},2:{2:F(1)},3:{3:F(1)},4:{4:F(1),3:F(1)}};need(ir==iw and ic=={0:2,1:1,2:2,3:2,4:1},'itinerant existing-owned five-input identity');need(ib['counts']=={'ADD':9,'CLEAR':1,'INIT':1,'MOVE':6},'itinerant tariff')
 T=two_loan_word();tr,tc,tb=replay(T,[0]*6,6);tw={0:{0:F(1)},1:{1:F(1),0:F(2)},2:{2:F(1)},3:{3:F(1)},4:{4:F(1),2:F(1)},5:{5:F(1),3:F(1)}};need(tr==tw,'two-loan six-input identity')
 br,_,_=replay(two_loan_word(False),[0]*6,6);err=add(br[3],tw[3],F(-1));need(err=={0:F(2)},'wrong-order exact2h1 error');neg=[{'mutation':'forward_donor_restoration','exact_Q2_error':show(err)}]
 for name,P,k,init,pub,own,want in [('omit_stationary_control',S,9,[0,0,1,0,1],5,1,sw),('omit_snapshot_copy',S,4,[0,0,1,0,1],5,1,sw),('omit_terminal_common_correction',S,14,[0,0,1,0,1],5,1,sw),('omit_donor_restoration',S,15,[0,0,1,0,1],5,1,sw),('omit_future_owned_control',I,6,[0,1,0,0,1],5,1,iw)]:
  bad=[e.copy() for e in P];bad.pop(k)
  try:z,_,_=replay(bad,init,pub,own);need(z==want,'full symbolic endpoints')
  except ValueError as exc:neg.append({'mutation':name,'rejection':str(exc)})
  else:raise ValueError('accepted '+name)
 for name,P in [('public_CLEAR',[['CLEAR',3,0]]),('nonzero_COPY_destination',[['INIT',5,0],['ADD',5,0,'1',0],['COPY',5,1,'1',0]])]:
  try:replay(P,[0,0,1,0,1],5,1)
  except ValueError as exc:neg.append({'mutation':name,'rejection':str(exc)})
  else:raise ValueError('accepted '+name)
 result={'status':'PASS_UNIVERSAL_DIFFERENCE_CARRIER_EXAMPLES','scope':'Universal proof plus complete symbolic input-column checks of explicit toy words; not a frozen-native crossing construction.','source_metadata':meta,'stationary_snapshot':{'word':S,'tariff':sb,'endpoint_rows':{str(i):show(r) for i,r in sr.items()},'baseline_native_operations':5,'baseline_raw_MOVEs':2,'extra_operations':9,'extra_MOVEs':0},'gamma_zero':{'word':G,'tariff':gb,'public_suffix_response':{},'gamma':'0','legacy_signed_swap_recovery_numerator':'0','difference_carrier_succeeds':True},'future_existing_owned_control':{'word':I,'tariff':ib,'endpoint_rows':{str(i):show(r) for i,r in ir.items()},'baseline_native_operations':10,'baseline_raw_MOVEs':1,'extra_ADDs':6,'extra_MOVEs':0,'extra_owned_lifetimes':0},'two_loans':{'word':T,'tariff':tb,'b21':'2','W':[['1','0'],['2','1']],'z_columns':[['1','2'],['0','1']],'endpoint_rows':{str(i):show(r) for i,r in tr.items()}},'negative_controls':neg,'new_complete_kappa':None,'source_crossing_constructed':False}
 text=json.dumps(result,indent=2,sort_keys=True)+'\n';path=packet/'CERTIFICATE.json'
 if write:path.write_text(text)
 else:need(path.read_text()==text,'certificate reconstruction')
 return {'status':result['status'],'source_sha256':PIN,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'symbolic_input_dimensions':[5,5,5,6],'negative_controls':len(neg),'source_crossing_constructed':False,'new_complete_kappa':None}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--write-certificate',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.packet,a.write_certificate);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
