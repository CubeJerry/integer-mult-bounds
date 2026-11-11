import argparse,gzip,hashlib,json
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CERT='7b915321a6e9afc2a83fd79f95e0c9605d28dc578d69d4b0700ee6fd37f739b9'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
PREPAID='6a1d608dc4b0947cd1d47e2869ceafc72498813a8ceba5d7a09cc1e7ec5bad51'
def need(b,s):
 if not b:raise ValueError(s)
def read(p,pin):
 b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'dependency pin '+p.name);return b
def span(f):
 s={0}
 for q in f:s|={x^q for x in s}
 return s
def replay(w,ops,M,capture=None,dirty=None):
 p=w['public'];n=p+w['owned_fields'];x=[{i:F(1)} if i in M or i==dirty else {} for i in range(n)];loc=w['initial'][:]+[None]*(n-p);live=set(range(p));frames=list(map(span,w['frames']));counts=Counter();moves=Counter();peak=life=0;out={}
 for i,e in enumerate(ops):
  if capture and i in capture:out[i]=x[capture[i]].copy()
  op,r=e[:2];need(0<=r<n,'field bound');counts[op]+=1
  if op=='INIT':need(r>=p and r not in live,'INIT owned fresh');live.add(r);loc[r]=e[2];x[r]={};life+=1
  elif op=='CLEAR':need(r>=p and r in live and loc[r]==e[2],'CLEAR owned chart');live.remove(r);loc[r]=None;x[r]={}
  elif op=='MOVE':
   need(r in live and loc[r]==e[2] and type(e[4]) is bool and e[4]==(r>=p),'MOVE actual ownership/chart');a,b=frames[e[2]],frames[e[3]];need(a<b or r>=p and b<a,'MOVE strict legal nesting');loc[r]=e[3];moves[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
  elif op=='SCALE':need(r in live and loc[r]==e[3] and F(e[2])!=0,'SCALE');x[r]={j:v*F(e[2]) for j,v in x[r].items()}
  elif op in ('ADD','COPY'):
   q=e[2];need(0<=q<n and r!=q and r in live and q in live and loc[r]==loc[q]==e[4],'actual live cochart operands');c=F(e[3]);need(c!=0,'nonzero coefficient')
   if op=='COPY':need(not x[r],'zero COPY')
   for j,v in x[q].items():
    x[r][j]=x[r].get(j,F(0))+c*v
    if not x[r][j]:del x[r][j]
  else:raise ValueError(op)
  peak=max(peak,len(live)-p)
 need(live==set(range(p)) and loc[:p]==w['final'],'final chart cleanup');return x,{'counts':dict(counts),'MOVE_histogram':{str(r):c for r,c in sorted(moves.items())},'owned_lifetimes':life,'peak_live_owned':peak,'final_live_owned':0,'declared_owned_labels':w['owned_fields']},out
def power(r):
 D=2**88;N=r**199*D**200
 with localcontext() as c:c.prec=100;a=int(Decimal(r)**(Decimal(199)/200)*D)
 while a**200>N:a-=1
 while(a+1)**200<=N:a+=1
 need(a**200<=N<(a+1)**200,'exact power enclosure');return F(a,D),F(a if a**200==N else a+1,D)
def run(source,cert,invoice,prepaid,transcript,author):
 w=json.loads(gzip.decompress(read(source,NATIVE)));c=json.loads(read(cert,CERT));iv=json.loads(read(invoice,INVOICE));pr=json.loads(read(prepaid,PREPAID));payload=gzip.decompress(transcript.read_bytes());t=json.loads(payload);a=json.loads(author.read_text());M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(len(M)==400 and 400 not in M,'domain400');chosen={28169,33558,34479,39217,40094,40096,41758};W={v['before_event']:v for v in c['witnesses']};need(chosen<set(W),'7of10');ops=[];cuts={};kinds=Counter()
 for i,e in enumerate(w['program']):
  if i not in chosen:ops.append(e[:]);continue
  need(e==W[i]['move'] and e[1]>=w['public'] and e[4] is True,'source occurrence');r,src,dst=e[1:4];ops.extend([['CLEAR',r,src],['INIT',r,dst]])
  for q,v in W[i]['witness']:need(q!=r,'nonalias observer');ops.append(['ADD',r,q,v,dst]);kinds[W[i]['observer_kinds'][str(q)]]+=1
  cuts[len(ops)]=(i,r)
 need(t['program']==ops and len(ops)==71294,'all71294 instructions');need(t['main_roles']==sorted(M) and t['owned_fields']==w['owned_fields'] and t['frames']==w['frames'] and t['initial']==w['initial'],'metadata');need(a['transcript_payload_sha256']==hashlib.sha256(payload).hexdigest(),'payload pin');x,xb,xc=replay(w,w['program'],M,{i:w['program'][i][1] for i in chosen});y,yb,yc=replay(w,ops,M,{k:r for k,(i,r) in cuts.items()});need(x[:w['public']]==y[:w['public']],'1480 endpoints');need(all(yc[k]==xc[i] for k,(i,r) in cuts.items()),'7exact macro rows');need(xb==a['baseline_reference'] and yb==a['rewritten_reference'],'complete bills');need(kinds==Counter({'main':4,'helper':19,'owned':3}),'26 observationterms');O=Counter();S=Counter();T=Counter({int(k):v for k,v in iv['T4'].items()});P=Counter({int(k):v for k,v in iv['P4'].items()})
 for i,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1]>=w['public']:
   r=abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]));O[r]+=1
   if i in chosen:S[r]+=1
 for r in set(O)|set(S):P[r]+=18*(O[r]-S[r])
 need(S==Counter({1:4,3:1,4:1,6:1}) and P==Counter({int(k):v for k,v in a['new_P'].items()}),'source derived fullprice');Q={r:power(r) for r in set(T)|set(P)}
 def moment(ds):
  lo=hi=F(0)
  for r,c in ds.items():u,v=Q[r];lo+=c*(u if c>=0 else v);hi+=c*(v if c>=0 else u)
  return lo,hi
 margin=moment({r:T[r]-P[r] for r in set(T)|set(P)});need(F(3)<margin[0]/18<=margin[1]/18<F(3889495420926,10**12),'headroom');need(F(a['raw_margin_numerator_bounds'][0])/10**15<=margin[0]<=margin[1]<=F(a['raw_margin_numerator_bounds'][1])/10**15,'independent dyadic interval');PP=Counter({int(k):v for k,v in pr['new_P'].items()});premium=moment({r:P[r]-PP[r] for r in set(P)|set(PP)});need(premium[0]>0,'positivepremium');need(sum(P.values())==153144 and sum(T.values())==27344 and sum(r*(T[r]-P[r]) for r in set(T)|set(P))==3346,'counts/surplus');controls=[]
 for label in ['wrong_coefficient','wrong_owned_flag','wrong_INIT_chart']:
  bad=[e[:] for e in ops]
  if label=='wrong_coefficient':bad[min(cuts)-1][3]=str(F(bad[min(cuts)-1][3])+1)
  elif label=='wrong_owned_flag':next(e for e in bad if e[0]=='MOVE' and e[1]>=w['public'])[4]=False
  else:bad[min(cuts)-len(W[min(chosen)]['witness'])-1][2]=W[min(chosen)]['move'][2]
  try:z,_,_=replay(w,bad,M);need(z[:w['public']]==x[:w['public']],'mutant endpoint')
  except(ValueError,TypeError) as ex:controls.append({'mutation':label,'rejection':str(ex)})
  else:raise ValueError('accepted mutant '+label)
 dx,_,_=replay(w,w['program'],M,dirty=400);dy,_,_=replay(w,ops,M,dirty=400);different=[i for i in range(w['public']) if dx[i]!=dy[i]];need(different,'helper400 domain counterexample');controls.append({'mutation':'independent_helper400_difference','different_public_outputs':different})
 return {'status':'PASS_INDEPENDENT_SEVEN_REFERENCE_AND_DYADIC_PRICE','source_sha256':NATIVE,'author_result_sha256':hashlib.sha256(author.read_bytes()).hexdigest(),'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'instructions':len(ops),'formal_difference_inputs':400,'public_endpoint_rows':1480,'macro_rows':7,'primitive_bill':yb,'observer_terms_by_kind':dict(kinds),'paid_positions':sum(P.values()),'targets':sum(T.values()),'rank_surplus':3346,'dyadic_denominator':str(2**88),'raw_margin_bounds':[str(z) for z in margin],'headroom_per_native_bounds':[str(z/18) for z in margin],'premium_vs_prepaid14_per_native_bounds':[str(z/18) for z in premium],'negative_controls':controls,'scope':'Conditional400-input referenceword andcomplete provisionalpaid invoice.26physicalobserverterms,sharednative,ordinary/compiler/precision/ownedservices andfivefoundations remainopen. No dominance ornewkappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for s in ('source','cert','invoice','prepaid','transcript','author'):p.add_argument('--'+s,type=Path,required=True)
 p.add_argument('--output',type=Path);a=p.parse_args();d=run(a.source,a.cert,a.invoice,a.prepaid,a.transcript,a.author);s=json.dumps(d,sort_keys=True,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
