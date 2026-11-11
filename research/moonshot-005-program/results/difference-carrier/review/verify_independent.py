#!/usr/bin/env python3
"""Independent dense exact replay of four difference-carrier toy words."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def execute(word,initial,public,owned):
 n=public;v={i:[F(int(i==j)) for j in range(n)] for i in range(public)};c=dict(enumerate(initial));peak=life=0;counts=collections.Counter()
 for e in word:
  op,d=e[:2];need(0<=d<public+owned,'declared destination');counts[op]+=1
  if op=='INIT':need(d>=public and d not in c,'fresh owner');c[d]=e[2];v[d]=[F(0)]*n;life+=1
  elif op=='CLEAR':need(d>=public and c.get(d)==e[2],'typed owned retirement');del c[d];del v[d]
  elif op=='MOVE':
   a,b,own=e[2:];need(c.get(d)==a and type(own)is bool and own==(d>=public),'typed actual MOVE');need(a!=b and (a<b or own),'public ascent or owned proper transfer');c[d]=b
  elif op in ('ADD','COPY'):
   s,k,f=e[2:];k=F(k);need(d!=s and c.get(d)==c.get(s)==f and k,'live cochart operation')
   if op=='COPY':need(not any(v[d]),'zero COPY target');v[d]=[k*y for y in v[s]]
   else:v[d]=[x+k*y for x,y in zip(v[d],v[s])]
  else:raise ValueError('unexpected toy operation')
  peak=max(peak,len(c)-public)
 return v,c,{'counts':dict(sorted(counts.items())),'instructions':len(word),'peak_owned':peak,'owned_lifetimes':life,'final_owned':len(c)-public}
def show(v):return {str(i):{str(j):str(z) for j,z in enumerate(r) if z} for i,r in sorted(v.items())}
def run(a):
 pins=json.loads((a.review/'REVIEWED-FILES.json').read_text())
 for f,p in pins.items():need(sha(a.packet/f)==p,'frozen file '+f)
 src=a.repository/'research/shared-wire-split-composition/data/final.json.gz';need(sha(src)==PIN,'source pin');w=json.loads(gzip.decompress(src.read_bytes()))
 need([(k,e) for k,e in enumerate(w['program']) if e[0]=='COPY']==[(31737,['COPY',1504,770,'1',115])],'source COPY guard')
 cert=json.loads((a.packet/'CERTIFICATE.json').read_text())
 specs={'stationary_snapshot':([0,0,1,0,1],5,1),'gamma_zero':([0,0,1,0,1],5,1),'future_existing_owned_control':([0,1,0,0,1],5,1),'two_loans':([0]*6,6,0)}
 expected={'stationary_snapshot':{0:{0:1},1:{1:1},2:{0:1,2:1},3:{3:1},4:{3:1,4:1}},'gamma_zero':{0:{0:1},1:{1:1},2:{2:1},3:{3:1},4:{3:1,4:1}},'future_existing_owned_control':{0:{0:1},1:{1:1},2:{2:1},3:{3:1},4:{3:1,4:1}},'two_loans':{0:{0:1},1:{0:2,1:1},2:{2:1},3:{3:1},4:{2:1,4:1},5:{3:1,5:1}}}
 receipts={}
 for name,spec in specs.items():
  rows,charts,bill=execute(cert[name]['word'],*spec);want={str(i):{str(j):str(v) for j,v in sorted(r.items())} for i,r in expected[name].items()}
  need(show(rows)==want,'all input columns '+name)
  if 'endpoint_rows' in cert[name]:need(show(rows)==cert[name]['endpoint_rows'],'certificate endpoints '+name)
  need(bill['counts']==cert[name]['tariff']['counts'] and bill['peak_owned']==cert[name]['tariff']['peak_owned'] and bill['final_owned']==0,'complete tariff and lifetime '+name)
  receipts[name]={'input_dimension':spec[1],'endpoint_rows':show(rows),'final_charts':{str(i):c for i,c in charts.items()},'tariff':bill}
 # Independent vector derivation, not a replay of the proposed two-loan word.
 h1,h2,q1,q2=[[F(int(i==j)) for j in range(4)] for i in range(4)]
 add=lambda x,y,k=F(1):[a+k*b for a,b in zip(x,y)]
 d1=add(q1,h1,F(-1));actual_h2=add(h2,q1,F(2));d2=add(q2,actual_h2,F(-1))
 y1=add(q1,d1,F(-1));y2=add(add(q2,d1,F(-2)),d2,F(-1))
 goodq2=add(add(d2,y2),d1,F(2));goodq1=add(d1,y1)
 need(goodq1==q1 and goodq2==q2,'causal two-loan restoration')
 wrongq2=add(add(d2,y2),goodq1,F(2));err=add(wrongq2,q2,F(-1));need(err==[F(2),F(0),F(0),F(0)],'forward order exact error2h1')
 bad=[e[:] for e in cert['stationary_snapshot']['word']];bad.insert(6,['CLEAR',5,1])
 try:execute(bad,*specs['stationary_snapshot'])
 except (ValueError,KeyError):early_rejected=True
 else:early_rejected=False
 need(early_rejected,'early snapshot retirement must fail')
 future=cert['future_existing_owned_control']['word'];at=next(i for i,e in enumerate(future) if e[:3]==['ADD',5,3]);bad=future[:at]+future[at+1:];rows,_,_=execute(bad,*specs['future_existing_owned_control']);err2=[rows[1][j]-F(int(j==1)) for j in range(5)]
 need(err2==[F(-1),F(0),F(0),F(1),F(0)],'missing future-owned control leaves offterminal delta')
 need(cert['gamma_zero']['gamma']=='0' and cert['gamma_zero']['public_suffix_response']=={},'gamma zero example')
 return {'status':'PASS_INDEPENDENT_DIFFERENCE_CARRIER_REVIEW','source_sha256':PIN,'reviewed_files_manifest_sha256':sha(a.review/'REVIEWED-FILES.json'),'method':'Fresh dense Fraction matrices on every toy input plus independent chronological two-loan algebra; exact chart, ownership, lifecycle and tariff checks; no author or predecessor code imported.','toy_receipts':receipts,'controls':{'forward_restoration_Q2_error':[str(v) for v in err],'early_snapshot_retirement_rejected':early_rejected,'omitted_future_owned_control_offterminal_error':[str(v) for v in err2],'zero_gamma_example_valid':True},'scope':'Accept conditional all-field-volume typed interface and four illustrative words. No frozen-native crossing, full1880-input continuation, complete cost profile or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--review',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
